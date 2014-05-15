<?php
/* crypto_rnd.php
 * Gera um md5 (32 bytes) aleatoria com qualidade criptografica
 * Testado somente no linux, mas deve funcionar tambem no windows
 * 
 * Não escrevi este código, apenas adaptei do seguinte link
 * http://stackoverflow.com/questions/1182584/secure-random-number-generation-in-php
 */


class crypto_rnd
{
	//rnd
	//$entropy: entropia adicional para gerar a string
	//$fetch_bytes: quantos bytes aleatorios devem vir do sistema (padrao: 32 bytes)
	function rnd($entropy, $fetch_bytes=32)
	{
		$pr_bits = '';
		
		// Unix/Linux platform?
		$fp = @fopen('/dev/urandom','rb');
		if ($fp !== FALSE) {
		    $pr_bits .= @fread($fp,$fetch_bytes);
		    @fclose($fp);
		}
		
		// MS-Windows platform?
		if (@class_exists('COM')) {
		    // http://msdn.microsoft.com/en-us/library/aa388176(VS.85).aspx
		    try {
		        $CAPI_Util = new COM('CAPICOM.Utilities.1');
		        $pr_bits .= $CAPI_Util->GetRandom($fetch_bytes,0);
		
		        // if we ask for binary data PHP munges it, so we
		        // request base64 return value.  We squeeze out the
		        // redundancy and useless ==CRLF by hashing...
		        if ($pr_bits) { $pr_bits = md5($pr_bits,TRUE); }
		    } catch (Exception $ex) {
		        die('crypto_rnd: Unable to generate RND');
		    }
		}
		
		if (strlen($pr_bits) < 16) {
		    // do something to warn system owner that
		    // pseudorandom generator is missing
		    die('crypto_rnd: Unable to generate RND');
		}
		
		//Return md5 of rnd bytes + entropy
		return md5($pr_bits.$entropy);
	}
}
?>