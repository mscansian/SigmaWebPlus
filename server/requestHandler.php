<?php 

class Request
{
	const USERNAME_MAXINVALID = 5;
	const USERNAME_MINTIME    = 600;
	const IP_MAXINVALID       = 20;
	const TIMEOUT_INVALID     = 1200;
	const PRIVATEKEY_PATH     = '/home/pexe/secure/sigmawebplus.com.br/sigmawebplus-server.key';
	
	private $username, $password, $hash;
	private $version, $ip;
	private $nome,$centro;
	
	public function Request()
	{	
		$this->username = intval($_SERVER['HTTP_USERNAME']);
		$this->password = base64_decode($_SERVER['HTTP_PASSWORD']);
		$this->hash     = preg_replace("/[^a-zA-Z0-9]+/", "", $_SERVER['HTTP_HASH']);
		$this->version  = $_SERVER['HTTP_VERSION'];
		$this->ip       = getenv("REMOTE_ADDR");
		
		#Decrypt password
		$key = openssl_get_privatekey(file_get_contents(self::PRIVATEKEY_PATH));
		openssl_private_decrypt($this->password, $this->password, $key, OPENSSL_PKCS1_OAEP_PADDING);
	}
	
	public function validate()
	{
		if (!(($this->username <> "") && ($this->password <> "") && ($this->username <> 0)))
		{
			throw new Exception('Username or password blank');
		}
		
		$this->updateValidationDB();
		$this->validateUsername();
		$this->validateIP();
	}
	
	private function updateValidationDB()
	{
		foreach (glob('requests/'."*") as $file) {
			if ($file != 'requests/index.php')
			{
				if (filemtime($file) < time() - self::TIMEOUT_INVALID) { 
					unlink($file);
				}
			}
		}
	}
	
	private function validateUsername()
	{
		if (file_exists('requests/'.$this->username))
		{
			$contents = file_get_contents('requests/'.$this->username);
			$contents = explode('|',$contents);
			
			$lastRequest = $contents[0];
			$invalidAttempts = $contents[1];
			
			if ($invalidAttempts >= self::USERNAME_MAXINVALID)  { throw new Exception('Max incorrect login'); }
			if (($lastRequest+self::USERNAME_MINTIME) > time()) { throw new Exception('Too many requests');   } 
		}
	}
	
	private function validateIP()
	{
		if (file_exists('requests/IP_'.$this->ip))
		{
			$contents = file_get_contents('requests/IP_'.$this->ip);
			$contents = explode('|',$contents);
			
			$invalidAttempts = $contents[0];
			
			if ($invalidAttempts >= self::IP_MAXINVALID) { throw new Exception('Max incorrect login from this IP'); }
		}
	}
	
	public function close($success, $data="")
	{
		if ($success)
		{
			file_put_contents('requests/'.$this->username, time().'|0');
			file_put_contents('requests/DATA_'.$this->username.'_'.md5($this->password), $data);
		}
		else
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
	}
	
	public function buildResponse($myAluno)
	{
		//Generate the output
		$output = "<SigmaWeb>
	<Aluno>
		<Nome>"     .$myAluno->getDados('Nome')     ."</Nome>
		<Matricula>".$myAluno->getDados('Matricula')."</Matricula>
		<TipoAluno>".$myAluno->getDados('TipoAluno')."</TipoAluno>
		<Status>"   .$myAluno->getDados('Status')   ."</Status>
		<Semestre>" .$myAluno->getDados('Semestre') ."</Semestre>
		<Centro>"   .$myAluno->getDados('Centro')   ."</Centro>
	</Aluno>
	<Materias>\n";
		
		foreach ($myAluno->getDados('Materias') as $Turma)
		{
			$output .= "		<Materia COD='".$Turma['Codigo']."' Nome='".$Turma['Nome']."' Turma='".$Turma['Turma']."' Centro='".$Turma['Centro']."'>\n";
			if (isset($Turma['Notas']))
			{
				foreach ($Turma['Notas'] as $Nota)
				{
					$output .= "			<Nota Peso='".$Nota['Peso']."' Desc='".$Nota['Nome']."'>".$Nota['Nota']."</Nota>\n";
				}
				$output .= "			<Exame>".$Turma['Exame']."</Exame>\n";
				$output .= "			<MediaFinal>".$Turma['MediaFinal']."</MediaFinal>\n";
			}
			$output .= "		</Materia>\n";
		}
		$output .= "	</Materias>\n";
		$output .= "</SigmaWeb>";
		
		$this->nome = $myAluno->getDados('Nome');
		$this->centro = $myAluno->getDados('Centro');
		
		return $output;
	}
	
	public function sendOutput($output)
	{
		//Save request
		$this->close(True, $output);
		
		//Hash the output and respond
		$output_hash = md5($output);
		
		if ($this->hash == $output_hash)
		{
			new Logger($this->getUsername(), $this->getVersion(), 'Up-to-date ('.$output_hash.')', $this->nome, $this->centro);
			echo 'Up-to-date';
		}
		else
		{
			new Logger($this->getUsername(), $this->getVersion(), 'New notas ('.$output_hash.')');
			echo $output_hash."\n";
			echo $output;
		}
	}
	
	public function getUsername()
	{
		return $this->username;
	}
	
	public function getPassword()
	{
		return $this->password;
	}
	
	public function getHash()
	{
		return $this->hash;
	}
	
	public function getVersion()
	{
		return $this->version;
	}
	
	public function getCache()
	{
		if (file_exists('requests/DATA_'.$this->username.'_'.md5($this->password)))
		{
			return file_get_contents('requests/DATA_'.$this->username.'_'.md5($this->password));
		}
		else
		{
			throw new Exception('No cache available');
		}
	}
}

?>