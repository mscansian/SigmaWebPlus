<?php 
	define('VALID_ENTRY_POINT', '1');
	date_default_timezone_set('America/Sao_Paulo');

	require_once '../database.php';
	
	$database = new cDatabase();
	
	$result = $database->query("SELECT COUNT(*) FROM requests");
	$data = $database->fetch($result);
	echo 'Total de '.$data[0].' requests<br>';
	
	$result = $database->query("SELECT COUNT(*) FROM users");
	$data = $database->fetch($result);
	echo 'Total de '.$data[0].' users<br>';
	
	$result = $database->query("SELECT COUNT(*) FROM requests WHERE error='0' AND invalidcredentials='0'");
	$data = $database->fetch($result);
	echo 'Total de '.$data[0].' requests validos<br>';
?>