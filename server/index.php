<?php
	//Seta o charset para UTF8 para suportar acentos
	ini_set('default_charset','UTF-8');
	
	//Inclui a classe que faz as solicitacoes HTTP
	require 'curl.php';
	
	//Get InnerHTML for DOM
	//http://stackoverflow.com/questions/2087103/innerhtml-in-phps-domdocument
	function DOMinnerHTML(DOMNode $element)
	{
		$innerHTML = "";
		$children  = $element->childNodes;
	
		foreach ($children as $child)
		{
			$innerHTML .= $element->ownerDocument->saveHTML($child);
		}
	
		return preg_replace('/[\x00-\x1F\x80-\xFF]/','',$innerHTML);
	}
	
	//Get input data
	$username = $_SERVER['HTTP_USERNAME'];
	$password = $_SERVER['HTTP_PASSWORD'];
	$hash = $_SERVER['HTTP_HASH'];
	
	if (!($username <> "" && $password <> ""))
	{
		die('<error>Username or password blank</error>');
	}
	
	$request = new cUrl();
	
	//Login
	$response = $request->requestPost("https://sigmaweb.cav.udesc.br/sw/sigmaweba.php", array(LSIST => "SigmaWeb",LUNID => "UDESC",lusid => $username,luspa => $password,opta => "Login"));
	if ($response == "") { die('<error>Connection error</error>'); }
	elseif ($response == '<html><head><META HTTP-EQUIV="Refresh" CONTENT="0;URL=sigmaweb0.php"></head></html>') { /*Auth okay, proceed*/ }
	else
	{
		$HTML = new DOMDocument; @$HTML->loadHTML($response); @$XPATH = new DOMXPath($HTML);
		$ErrorMsg = utf8_decode($XPATH->query('*/td',$XPATH->query('*/table')->item(1))->item(1)->nodeValue);
			
		if ($ErrorMsg == "Matrícula e/ou senha inválida")
		{
			die('<error>Auth error</error>');
		}
		else
		{
			die('<error>Custom error msg</error>');
		}
		unset($HTML); unset($XPATH);
	}
	
	//Get main page
	$response = $request->requestGet("https://sigmaweb.cav.udesc.br/sw/sigmaweb0.php");
	if ($response == "") { die('<error>Connection error</error>'); }
	else
	{
		$HTML = new DOMDocument; @$HTML->loadHTML($response); @$XPATH = new DOMXPath($HTML);
		$Centro = $XPATH->query('*/td',$XPATH->query('*/table')->item(0))->item(1)->nodeValue;
		
		$Nome = explode("<br>",DOMinnerHTML($XPATH->query('*/td',$XPATH->query('*/table')->item(0))->item(2))); $Nome = $Nome[0];
		$Matricula = explode("<br>",DOMinnerHTML($XPATH->query('*/td',$XPATH->query('*/table')->item(0))->item(2))); $Matricula = explode(" - ", $Matricula[1]); $Matricula = $Matricula[0];
		$TipoAluno = explode("<br>",DOMinnerHTML($XPATH->query('*/td',$XPATH->query('*/table')->item(0))->item(2))); $TipoAluno = explode(" - ", $TipoAluno[1]); $TipoAluno = $TipoAluno[1];

		
		$Semestre = DOMinnerHTML($XPATH->query('td',$XPATH->query('*/tr',$XPATH->query('*/td',$XPATH->query('*/table')->item(2))->item(2))->item(4))->item(0));
		$Status = DOMinnerHTML($XPATH->query('td',$XPATH->query('*/tr',$XPATH->query('*/td',$XPATH->query('*/table')->item(2))->item(2))->item(5))->item(0));
		unset($HTML); unset($XPATH);
	}
	
	//Get turmas
	$Turmas = array();
	$request->requestGet("https://sigmaweb.cav.udesc.br/sw/sigmaweb1.php?var=R6655");
	$response = $request->requestGet("https://sigmaweb.cav.udesc.br/sw/sigmaweb4.php");
	if (strstr($response,"Não há matrícula efetivada para "))
	{
		//Erro, nao ha materias!
	}
	else
	{
		$response = $request->requestGet("https://sigmaweb.cav.udesc.br/sw/sigmaweb5.php");
		
		$HTML = new DOMDocument; @$HTML->loadHTML($response); @$XPATH = new DOMXPath($HTML);
		$NumTurmas = substr_count(DOMinnerHTML($XPATH->query('/html/body/form/table/tr[3]/td/select')->item(0)),"</option>");
		for ($a=0; $a <= $NumTurmas-1; $a++)
		{
			$TurmaNome = explode(" - ",DOMinnerHTML($XPATH->query('/html/body/form/table/tr[3]/td/select/option')->item($a))); $TurmaNome = $TurmaNome[1];
			$TurmaCod = explode("/",$XPATH->query('/html/body/form/table/tr[3]/td/select/option')->item($a)->getAttribute('value')); $TurmaLetra = $TurmaCod[1]; $TurmaCentro = $TurmaCod[2]; $TurmaCod = $TurmaCod[0];
			array_push($Turmas, array(Nome=>$TurmaNome, Codigo=>$TurmaCod, Turma=>$TurmaLetra, Centro=>$TurmaCentro));
		}
		unset($TurmaNome); unset($TurmaCod); unset($NumTurmas);
	}
	
	//Get resultados parciais de cada turma
	//Nota: Eu tenho vergonha de mim mesmo por este codigo!!! (Nao perca seu tempo aqui)
	foreach ($Turmas as &$Turma)
	{
		$request->requestGet("https://sigmaweb.cav.udesc.br/sw/sigmaweb1.php?var=R6655");
		$request->requestGet("https://sigmaweb.cav.udesc.br/sw/sigmaweb4.php");
		$request->requestGet("https://sigmaweb.cav.udesc.br/sw/sigmaweb5.php");
		$request->requestPost("https://sigmaweb.cav.udesc.br/sw/sigmaweb7.php", array(nagru => $Turma['Codigo']."/".$Turma['Turma']."/".$Turma['Centro'], opta => 'Enter'));
		$response = $request->requestGet("https://sigmaweb.cav.udesc.br/sw/sigmaweb7.php");
		if (strstr($response, "Não há registro de notas parciais"))
		{
			//Erro, parte para a proxima!
		}
		else
		{
			$NotasAluno = array();
			$HTML = new DOMDocument; @$HTML->loadHTML($response); @$XPATH = new DOMXPath($HTML);
			$NumNotas = $XPATH->query("/html/body/table[2]/tr[@bgcolor='#D6D6FF']/th")->length;
			$NumLinhas = ceil(($NumNotas-5)/5);
			for ($a=3;$a<=($NumNotas-2);$a++)
			{
				$Nota = explode("<br>",DOMinnerHTML($XPATH->query("/html/body/table[2]/tr[@bgcolor='#D6D6FF']/th")->item($a)));
				array_push($NotasAluno, array(Nome=>substr($Nota[0],1,-1), Peso=>$Nota[1]));
			}
			
			$NotasAluno_Table = $XPATH->query("/html/body/table[2]/tr/td[contains(., '".utf8_encode(strtoupper($Nome))."')]/..")->item(0);
			for ($a=0; $a<=$NumLinhas-1;$a++)
			{
				for ($b=($a*5); ($b<=($a*5)+4) && ($b<=$NumNotas-4-$NumLinhas); $b++)
				{
					$NumColuna = ($b+(3*($a==0))-(5*$a));
					$NotasAluno[$b]['Nota'] = DOMinnerHTML($XPATH->query("td", $NotasAluno_Table)->item($NumColuna));
				}
				
				if ($b<=$NumNotas-4-$NumLinhas)
				{
					$NotasAluno_Table = $XPATH->query("following-sibling::*[1]", $NotasAluno_Table)->item(0);
				}
			}
			
			$Turma['Notas'] = $NotasAluno;
		}
	}
	unset($Turma);

	//Generate the output
		
	$output = "<SigmaWeb>
	<Aluno>
		<Nome>".$Nome."</Nome>
		<Matricula>".$Matricula."</Matricula>
		<TipoAluno>".$TipoAluno."</TipoAluno>
		<Status>".$Status."</Status>
		<Semestre>".$Semestre."</Semestre>
		<Centro>".$Centro."</Centro>
	</Aluno>
	<Materias>\n";

	foreach ($Turmas as $Turma)
	{
		$output .= "		<Materia COD='".$Turma['Codigo']."' Nome='".$Turma['Nome']."' Turma='".$Turma['Turma']."' Centro='".$Turma['Centro']."'>\n";
		if (isset($Turma['Notas']))
		{
			foreach ($Turma['Notas'] as $Nota)
			{
				$output .= "			<Nota Peso='".$Nota['Peso']."' Desc='".$Nota['Nome']."'>".$Nota['Nota']."</Nota>\n";
			}
			$output .= "			<Exame></Exame>\n";
		}
		$output .= "		</Materia>\n";
	}
	$output .= "	</Materias>\n";
	$output .= "</SigmaWeb>";
	
	//Hash the output and respond
	$output_hash = md5($output);
	
	if ($hash == $output_hash)
	{
		die('Up-to-date');
	}
	else
	{
		echo $output_hash."\n";
		echo $output;
	}

?>
