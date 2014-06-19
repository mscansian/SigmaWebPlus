<?php 

class Request
{
	const USERNAME_MAXINVALID = 5;
	const USERNAME_MINTIME = 300;
	const IP_MAXINVALID = 20;
	const TIMEOUT_INVALID = 600;
	
	var $username, $password, $hash;
	var $ip;
	
	function Request()
	{
		$this->username = intval($_SERVER['HTTP_USERNAME']);
		$this->password = $_SERVER['HTTP_PASSWORD'];
		$this->hash     = preg_replace("/[^a-zA-Z0-9]+/", "", $_SERVER['HTTP_HASH']);
		$this->ip       = getenv("REMOTE_ADDR");
	}
	
	function validadeRequest()
	{
		if (!(($this->username <> "") && ($this->password <> "") && ($this->username <> 0)))
		{
			die('<error>Username or password blank</error>');
		}
		
		$this->updateRequestDB();
		if (!$this->checkUsernameRequest()) { die('<error>Refused request from this username</error>'); }
		if (!$this->checkIPRequest()) { die('<error>Refused request from this ip</error>'); } 		
		return True;
	}
	
	function updateRequestDB()
	{
		foreach (glob('requests/'."*") as $file) {
			if (filemtime($file) < time() - self::TIMEOUT_INVALID) { 
				unlink($file);
			}
		}
	}
	
	function checkUsernameRequest()
	{
		if (!file_exists('requests/'.$this->username)) { return True; }
	
		$contents = file_get_contents('requests/'.$this->username);
		$contents = explode('|',$contents);
		
		$lastRequest = $contents[0];
		$invalidAttempts = $contents[1];
		
		if ($invalidAttempts >= self::USERNAME_MAXINVALID) { return False; }
		if (($lastRequest+self::USERNAME_MINTIME) > time()) {
			$output = file_get_contents('requests/DATA_'.$this->username);
			
			//Hash the output and respond
			$output_hash = md5($output); #Debug
			
			if ($this->hash == $output_hash)
			{
				die('Up-to-date');
			}
			else
			{
				echo $output_hash."\n";
				echo $output;
				die('');
			}
		}
		return True;
	}
	
	function checkIPRequest()
	{
		if (!file_exists('requests/IP_'.$this->ip)) { return True; }
	
		$contents = file_get_contents('requests/IP_'.$this->ip);
		$contents = explode('|',$contents);
		
		$invalidAttempts = $contents[0];
		
		if ($invalidAttempts >= self::IP_MAXINVALID) { return False; }
		return True;
	}
	
	function saveValidRequest($data)
	{
		file_put_contents('requests/'.$this->username, time().'|0');
		file_put_contents('requests/DATA_'.$this->username, $data);
	}
	
	function saveInvalidRequest()
	{
		$lastRequest = 0;
		$invalidAttempts    = 0;
		$invalidAttempts_IP = 0;
		
		if (file_exists('requests/'.$this->username)) 
		{
			$contents = file_get_contents('requests/'.$this->username);
			$contents = explode('|',$contents);
		
			$lastRequest = $contents[0];
			$invalidAttempts = $contents[1];
		}
		
		if (file_exists('requests/IP_'.$this->ip))
		{
			$contents = file_get_contents('requests/IP_'.$this->ip);
			$contents = explode('|',$contents);
		
			$invalidAttempts_IP = $contents[0];
		}
		
		$invalidAttempts += 1;
		$invalidAttempts_IP += 1;
		
		file_put_contents('requests/'.$this->username, $lastRequest.'|'.$invalidAttempts);
		file_put_contents('requests/IP_'.$this->ip   , $invalidAttempts_IP);
	}
	
	function getRequestUsername()
	{
		return $this->username;
	}
	
	function getRequestPassword()
	{
		return $this->password;
	}
	
	function getRequestHash()
	{
		return $this->hash;
	}
}

?>