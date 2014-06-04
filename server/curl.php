<?php
/*	curl.php
	Este código descreve a classe usada para acessar os metodos do cURL
	Essa classe tem suporte nativo a cookies e está com o certificado da UDESC hard-coded
	O header HTTP_USERNAME utilizado pelo SigmaWeb+ também está hard-coded
*/ 

//Para gerar o nome do arquivo de cookies precisamos de uma funcão RND com qualidade criptografica
require 'crypto_rnd.php';

//Limpa o diretorio de cookies
//Deleta arquivos na pasta cookie que não foram modificados a mais de 1 hora
foreach (glob('cookies/'."*") as $file) {
	if (filemtime($file) < time() - 3600) {
		unlink($file);
	}
}

class cUrl
{
	var $object; //Objeto do cURL
	var $random; //Nome do arquivo de cookies
	
	
	//Constructor
	//Cria o objeto cURL e seta as principais configs
	function cUrl()
	{
		$this->object = curl_init();
		curl_setopt($this->object, CURLOPT_RETURNTRANSFER, 1); //Forca cURL a retornar a resposta do server (ao inves de dar print)
		curl_setopt($this->object, CURLOPT_HEADER, 0); //Forca cURL a retirar os HEADERS da resposta
		
		//Cria nome do arquivo de cookies usando 3 parametros: crypto_rnd, ip de acesso e matricula (o md5 serve para deixar o nome com um formato padrao)
		$crypto_object = new crypto_rnd();
		$this->random = $crypto_object->rnd(getenv("REMOTE_ADDR").$_SERVER['HTTP_USERNAME']);
		
		/* AVISO: O certificado o SigmaWeb esta vencido desde 2006, para permitir a autenticacao eu desabilitei o check por host.
		 * A comunicacao continua criptografada, porem nao eh possivel verificar se o servidor eh autentico ou nao
		 */
		curl_setopt($this->object, CURLOPT_SSL_VERIFYPEER, 0); //Desabilitado (não verifica se o certificado é valido)
		curl_setopt($this->object, CURLOPT_SSL_VERIFYHOST, 2);
		curl_setopt($this->object, CURLOPT_CAINFO, getcwd()."/UDESCCertificateAuthority.crt"); //Carrega certificado raiz do SigmaWeb
	}
	
	//Faz uma request POST e retorna uma string com o resultado
	//$url: string url da pagina
	//$post: array dados do request post
	function requestPost($url, $post)
	{
		//Set request parameters
		curl_setopt($this->object, CURLOPT_URL, $url);
		curl_setopt($this->object, CURLOPT_POST, 1);		
		curl_setopt($this->object, CURLOPT_POSTFIELDS, $post);
		
		//Set cookies
		curl_setopt( $this->object, CURLOPT_COOKIESESSION, true );
		curl_setopt( $this->object, CURLOPT_COOKIEJAR, getcwd()."/cookies/".($this->random));
		curl_setopt( $this->object, CURLOPT_COOKIEFILE, getcwd()."/cookies/".($this->random));
		
		//Request and return
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
		curl_setopt( $this->object, CURLOPT_COOKIEJAR, getcwd()."/cookies/".($this->random));
		curl_setopt( $this->object, CURLOPT_COOKIEFILE, getcwd()."/cookies/".($this->random));
	
		//Request and return
		$result = curl_exec($this->object);
		return utf8_encode($result);
	}
}
?>