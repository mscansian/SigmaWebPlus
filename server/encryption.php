<?php 
defined('VALID_ENTRY_POINT') or die('');
require_once 'config.php';

class cEncryption
{
	private $key;
	
	private function load_key()
	{
		global $CONFIG;
		
		if (!$this->key)
		{
			$keyfile = file_get_contents($CONFIG['RSA']['keypath']);
			if (!$keyfile)
			{
				die('Fatal: Could not load private key');
			}
			$this->key = openssl_get_privatekey($keyfile);
		}
	}
	
	public function encrypt($text)
	{
		$this->load_key();
		openssl_private_encrypt($text, $text, $this->key, OPENSSL_PKCS1_OAEP_PADDING);
		$text = base64_decode($text);
		return $text;
	}
	
	public function decrypt($text)
	{
		$this->load_key();
		$text = base64_decode($text);
		openssl_private_decrypt($text, $text, $this->key, OPENSSL_PKCS1_OAEP_PADDING);
		return $text;
	}
}