<?php
//Precisamos de uma funcao RND com qualidade criptografica!
require 'crypto_rnd.php';

//Limpa o diretorio de cookies
foreach (glob('cookies/'."*") as $file) {
	if (filemtime($file) < time() - 3600) {
		unlink($file);
	}
}

class cUrl
{
	var $object;
	var $random;
	
	function cUrl()
	{
		$this->object = curl_init(); 
		curl_setopt($this->object, CURLOPT_RETURNTRANSFER, 1);
		curl_setopt($this->object, CURLOPT_HEADER, 0);
		$this->random = md5(crypto_rnd().getenv("REMOTE_ADDR").$_SERVER['HTTP_USERNAME']);
		
		/* AVISO: O certificado o SigmaWeb esta vencido desde 2006, para permitir a autenticacao eu desabilitei o check por host.
		 * A comunicacao continua criptografada, porem nao eh possivel verificar se o servidor eh autentico ou nao
		 */
		curl_setopt($this->object, CURLOPT_SSL_VERIFYPEER, 0);
		curl_setopt($this->object, CURLOPT_SSL_VERIFYHOST, 2);
		curl_setopt($this->object, CURLOPT_CAINFO, getcwd()."/UDESCCertificateAuthority.crt"); //Carrega certificado raiz do SigmaWeb
	}
	
	function requestPost($url, $post)
	{
		//Set request parameters
		curl_setopt($this->object, CURLOPT_URL, $url);
		curl_setopt($this->object, CURLOPT_POST, 1);		
		curl_setopt($this->object, CURLOPT_POSTFIELDS, $post);
		
		//Set cookies
		curl_setopt( $this->object, CURLOPT_COOKIESESSION, true );
		curl_setopt( $this->object, CURLOPT_COOKIEJAR, getcwd()."/cookies/".md5($this->random));
		curl_setopt( $this->object, CURLOPT_COOKIEFILE, getcwd()."/cookies/".md5($this->random));
		
		$result = curl_exec($this->object);
		return utf8_encode($result);
	}
	
	function requestGet($url)
	{
		//Set request parameters
		curl_setopt($this->object, CURLOPT_URL, $url);
		curl_setopt($this->object, CURLOPT_POST, 0);
		curl_setopt($this->object, CURLOPT_POSTFIELDS, "");
	
		//Set cookies
		curl_setopt( $this->object, CURLOPT_COOKIESESSION, true );
		curl_setopt( $this->object, CURLOPT_COOKIEJAR, getcwd()."/cookies/".md5($this->random));
		curl_setopt( $this->object, CURLOPT_COOKIEFILE, getcwd()."/cookies/".md5($this->random));
	
		$result = curl_exec($this->object);
		return utf8_encode($result);
	}
}
?>