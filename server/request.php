<?php
defined('VALID_ENTRY_POINT') or die('');
require_once 'config.php';
require_once 'database.php';
require_once 'encryption.php';

class cRequest
{
	private $encryption, $database;
	
	private $saved;
	private $username, $password, $hash, $newhash;
	private $force, $timeout, $auto;
	private $version, $ip;
	private $valid, $cache, $notes, $wrongpw;
	
	public function __construct()
	{
		$this->database = new cDatabase(); 
		$this->encryption = new cEncryption();
		
		$this->username = intval($_SERVER['HTTP_USERNAME']);
		$this->password = $this->encryption->decrypt($_SERVER['HTTP_PASSWORD']);
		$this->hash     = preg_replace("/[^a-zA-Z0-9]+/", "", $_SERVER['HTTP_HASH']);
		$this->version  = $_SERVER['HTTP_VERSION'];
		$this->ip       = getenv("REMOTE_ADDR");
		
		$this->force    = (($_SERVER['HTTP_FORCE'] == '')?('NULL'):("'".$_SERVER['HTTP_FORCE']."'"));
		$this->timeout  = (($_SERVER['HTTP_TIMEOUT'] == '')?('NULL'):("'".$_SERVER['HTTP_TIMEOUT']."'"));
		$this->auto     = (($_SERVER['HTTP_AUTO'] == '')?('NULL'):("'".$_SERVER['HTTP_AUTO']."'"));
		
		$this->validate();
		$this->check_cache();
	}
	
	public function is_valid() { return $this->valid; }
	public function get_cache() { return $this->cache; }
	public function get_username() { return $this->username; }
	public function get_password() { return $this->password; }
	public function get_hash() { return $this->hash; }
	public function get_version() { return $this->version; }
	
	public function error($errormsg)
	{
		$this->valid = false;
		$this->notes = $errormsg;
		$this->save();
	}
	
	public function wrongpassword()
	{
		$this->wrongpw = true;
		$this->save();
	}
	
	public function success($nome, $centro, $tipo, $dados)
	{
		//Verifica se o user ja existe na database
		$result = $this->database->query("SELECT nome, centro, tipo FROM users WHERE matricula='$this->username'");
		$user = $this->database->fetch($result);
		
		if ($user)
		{
			//Usuario existe! Atualiza a informacao
			//Sim, eu sei que ninguem vai mudar de nome! Isso esta aqui apenas para se mais para frente essa tabela tiver informacoes mais volateis
			$this->database->query("UPDATE users SET nome='$nome', centro='$centro', tipo='$tipo', update_auto=$this->auto, update_timeout=$this->timeout WHERE matricula=$this->username");
		}
		else
		{
			//Usuario nao existe! Cria um novo usuario
			$this->database->query("INSERT INTO users VALUES ('$this->username', '$nome', '$centro', '$tipo', $this->auto, $this->timeout)");
		}
		
		//Salva dados no cache
		$this->database->query("INSERT INTO cache VALUES ('$this->username', UTC_TIMESTAMP, '$dados')");
		
		$this->newhash = md5($dados);
		$this->save();
	}
	
	private function save()
	{
		if (!$this->saved)
		{
			$this->database->query("INSERT INTO requests VALUES ('$this->username', UTC_TIMESTAMP, '$this->hash', '$this->newhash', '$this->ip', '$this->version', '".(($this->valid)?('0'):('1'))."', '$this->notes', '".(($this->wrongpw)?('1'):('0'))."', '".(($this->cache)?('1'):('0'))."', $this->force)");
			$this->saved = true;
		}   
	}
	
	private function check_cache()
	{
		global $CONFIG;
		
		//Deleta dados antigos do cache (cache antigo = informacao inutil!)
		$this->database->query("DELETE FROM cache WHERE data<=DATE_SUB(UTC_TIMESTAMP, INTERVAL ".$CONFIG['SERVER']['cachelifetime']." MINUTE)");
		
		//Pega o valor do cache e coloca na variavel do request
		$result = $this->database->query("SELECT dados FROM cache WHERE matricula='$this->username'");
		$result_fetch = $this->database->fetch($result);
		$this->cache = $result_fetch[0];
		
		if ($this->cache)
		{
			$this->database->query("UPDATE users SET update_auto=$this->auto, update_timeout=$this->timeout WHERE matricula=$this->username");
			$this->newhash = md5($this->cache);
			$this->save();
		}
	}
	
	private function validate()
	{
		global $CONFIG;
		if ((strlen($this->username) < 8) || ($this->password == '') || ($this->version == '') || ((strlen($this->hash) != 32) && (strlen($this->hash) != 0)))
		{
			$this->valid = false;
			$this->notes = "username, password or version invalid";
			$this->save();
			return;
		}
		
		$result = $this->database->query("SELECT COUNT(*) FROM requests WHERE matricula='$this->username' AND invalidcredentials=1 AND data>=DATE_SUB(UTC_TIMESTAMP, INTERVAL ".$CONFIG['SEC']['userbantime']." MINUTE)");
		$result_fetch = $this->database->fetch($result);
		$invalid_attempts_user = $result_fetch[0];
		
		$result = $this->database->query("SELECT COUNT(*) FROM requests WHERE ip='$this->ip' AND invalidcredentials=1 AND data>=DATE_SUB(UTC_TIMESTAMP, INTERVAL ".$CONFIG['SEC']['ipbantime']." MINUTE)");
		$result_fetch = $this->database->fetch($result);
		$invalid_attempts_ip = $result_fetch[0];
		
		if (($invalid_attempts_user >= $CONFIG['SEC']['maxuserlogin']) || ($invalid_attempts_ip >= $CONFIG['SEC']['maxiplogin']))
		{
			$this->valid = false;
			$this->notes = "username or ip banned";
			$this->save();
			return;
		}
		
		$this->valid = true;
	}
}
?>
