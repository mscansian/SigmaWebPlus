<?php
	
	$username = $_SERVER['HTTP_USERNAME'];
	$password = $_SERVER['HTTP_PASSWORD'];
	$hash = $_SERVER['HTTP_HASH'];
	
	echo "$username - $password - $hash";
	
	/*
	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL, "https://drpexe.com/downloads");
	curl_setopt($ch, CURLOPT_HEADER, 0);
	curl_exec($ch);
	curl_close($ch);
	*/
?>
