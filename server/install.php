<?php 
define('VALID_ENTRY_POINT', '1');
date_default_timezone_set('America/Sao_Paulo');

require 'config.php';
require 'database.php';

if (!isset($CONFIG['SYSTEM']['install_time']))
{
	if ($_SERVER['REQUEST_METHOD']=="GET")
	{
		//Primeiro acesso na pagina
		echo '<!DOCTYPE html><html>';
		echo '<head><title>SigmaWebPlus Server - Instalacao</title></head>';
		
		echo '<body><form action="?" method="POST">';
		echo '<h1>Instalacao do SigmaWebPlus Server</h1>';
		echo '<h2>Dados de conexao no mySQL</h2>';
		echo '<input type"text" size="70" name="DB_hostname" placeholder="Endereco do host (ex: mysql.sigmawebplus.com.br)" required/><br/>';
		echo '<input type"text" size="70" name="DB_name" placeholder="Nome da database" required/><br/>';
		echo '<input type"text" size="70" name="DB_username" placeholder="Usuario" required/><br/>';
		echo '<input type"text" size="70" name="DB_password" placeholder="Senha" required/><br/>';
		echo '<h2>Dados da chave RSA</h2>';
		echo '<input type"text" size="70" name="RSA_keypath" placeholder="Local do arquivo contendo a chave privada (caminho absoluto)" required/><br/>';
		echo '<h2>Politicas de uso do servidor</h2>';
		echo '<input type"number" min="0" name="SERVER_cachelifetime" size="70" placeholder="Tempo de vida do cache em minutos (default: 5)" required/><br/>';
		echo '<h2>Politicas de seguranca</h2>';
		echo '<input type"number" min="0" name="SEC_maxuserlogin" size="70" placeholder="Num. maximo de login incorretos por usuario (default: 5)" required/><br/>';
		echo '<input type"number" min="0" name="SEC_maxiplogin " size="70" placeholder="Num. maximo de login incorretos por IP (default: 10)" required/><br/>';
		echo '<input type"number" min="0" name="SEC_userbantime" size="70" placeholder="Tempo de bloqueio (em minutos) do usuario por login incorreto (default: 30)" required/><br/>';
		echo '<input type"number" min="0" name="SEC_ipbantime" size="70" placeholder="Tempo de bloqueio (em minutos) do IP por login incorreto (default: 360)" required/><br/>';
		echo '<br/><input type="submit" value="Iniciar instalacao"/></form>';
		echo '</body></html>';
	}
	elseif ($_SERVER['REQUEST_METHOD']=="POST")
	{
		//Inicia a instalacao
		$contents = "<?php\n";
		$contents .= 'defined(\'VALID_ENTRY_POINT\') or die(\'\');'."\n";
		foreach($_POST as $key => $value)
		{
			$key_array = explode('_', $key);
			$contents .= '$CONFIG[\''.$key_array[0].'\'][\''.$key_array[1].'\'] = \''.$value.'\';'."\n";
		}
		$contents .= '$CONFIG[\'SYSTEM\'][\'install_time\'] = \''.time().'\';'."\n";
		$contents .= "?>";
		
		$config_file = fopen('config.php', 'w');
		if ($config_file)
		{
			fwrite($config_file, $contents);
			fclose($config_file);
			require 'config.php';
		}
		else
		{
			die ('<h2 style="background-color:red;">Erro: Nao foi possivel escrever no arquivo config.php. Verifique as permissoes do arquivo.</h2>');
		}
		
		$sqlquery1 = 'DROP TABLE IF EXISTS users, requests, cache;';
		$sqlquery2 = 'CREATE TABLE users (
			matricula INT(9) NOT NULL PRIMARY KEY,
			nome VARCHAR(70) NOT NULL,
			centro VARCHAR(20) NOT NULL,
			tipo VARCHAR(50) NOT NULL
		);';
		
		$sqlquery3 = 'CREATE TABLE requests (
			matricula INT(9) NOT NULL,
			data TIMESTAMP NOT NULL,
			hash VARCHAR(32) NULL,
			newhash VARCHAR(32) NULL,
			ip VARCHAR(16) NOT NULL,
			versao VARCHAR(16) NOT NULL,
			error BOOLEAN NOT NULL,
			notes VARCHAR(50) NULL,
			invalidcredentials BOOLEAN NOT NULL,
			fromcache BOOLEAN NOT NULL
		);';
		
		$sqlquery4 = 'CREATE TABLE cache (
			matricula INT(9) NOT NULL PRIMARY KEY,
			data TIMESTAMP NOT NULL,
			dados TEXT NOT NULL
		);';
		
		$database = new cDatabase();
		$result = $database->query($sqlquery1);
		$result = $result && $database->query($sqlquery2);
		$result = $result && $database->query($sqlquery3);
		$result = $result && $database->query($sqlquery4);
		if ($result)
		{
			echo '<h2>Instalacao realizada com sucesso!';
		}
		else
		{
			die ('<h2 style="background-color:red;">Erro: Nao foi possivel criar as tabelas no banco de dados</h2>');
		}
		$database->disconnect();
	}
}
else
{
	die('<h2 style="background-color:red;">Erro: Instalacao ja realizada em '.date("d/m/Y H:i:s",$CONFIG['SYSTEM']['install_time']).'</h2>');
}
?>