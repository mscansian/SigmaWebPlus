<?php
	//Seta o charset para UTF8 para suportar acentos
	ini_set('default_charset','UTF-8');
	
	require 'requestHandler.php';
	require 'aluno.php';
	require_once 'logger.php';
	
	
	try
	{
		//Get data from request and validate
		$myRequest = new Request();
		$myRequest->validate();
		
		//Create new Aluno and get data from SigmaWeb
		$myAluno = new Aluno($myRequest->getUsername(), $myRequest->getPassword());
		$myAluno->refresh();
		
		//Constroi resposta
		$output = $myRequest->buildResponse($myAluno);
		$myRequest->sendOutput($output);
	}
	catch (Exception $e)
	{
		if ($e->getMessage() == 'Too many requests')
		{
			$myRequest->sendOutput($myRequest->getCache()); die('');			
		}
		elseif ($e->getMessage() == 'Auth error')
		{
			$myRequest->close(False);
		}
		new Logger($myRequest->getUsername(), $myRequest->getVersion(), 'ERRO: '.$e->getMessage());
		echo '<error>'.$e->getMessage().'</error>';
	}

?>
