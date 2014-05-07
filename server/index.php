<?php
	ini_set('default_charset','UTF-8');
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
	
		return ($innerHTML);
	}
	
	//Get input data

	$hash = $_SERVER['HTTP_HASH'];
	
	$request = new cUrl(); 
	
	//Login
	$response = $request->requestPost("https://sigmaweb.cav.udesc.br/sw/sigmaweba.php", array(LSIST => "SigmaWeb",LUNID => "UDESC",lusid => $username,luspa => $password,opta => "Login"));
	if ($response == "") { die('<error>Connection error</error>'); }
	elseif ($response == '<html><head><META HTTP-EQUIV="Refresh" CONTENT="0;URL=sigmaweb0.php"></head></html>') { /*Auth okay, proceed*/ }
	else
	{
		$HTML = new DOMDocument; @$HTML->loadHTML($response); @$XPATH = new DOMXPath($HTML);
		$ErrorMsg = $XPATH->query('*/td',$XPATH->query('*/table')->item(1))->item(1)->nodeValue;
			
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
	$Turma = array(Codigo=>"FGE2001", Turma=>"A", Centro=>"CCT");
	//foreach ($Turmas as $Turma)
	//{
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
			$Nome = "GABRIEL SIMÕES"; //Debug
			$NotasAluno = array();
			$HTML = new DOMDocument; @$HTML->loadHTML($response); @$XPATH = new DOMXPath($HTML);
			$NumNotas = $XPATH->query("/html/body/table[2]/tr[@bgcolor='#D6D6FF']/th")->length;
			for ($a=3;$a<=($NumNotas-3);$a++)
			{
				$Nota = explode("<br>",DOMinnerHTML($XPATH->query("/html/body/table[2]/tr[@bgcolor='#D6D6FF']/th")->item($a)));
				array_push($NotasAluno, array(Nome=>substr($Nota[0],1,-1), Peso=>$Nota[1]));
			}
			print_r($NotasAluno);
			/*
			$NotasAluno = array($XPATH->query("/html/body/table[2]/tr/td[contains(., '".utf8_encode(strtoupper($Nome))."')]/..")->item(0));
			$NumNotas = $XPATH->query("td", $NotasAluno[0])->length;
			if ($NumLinhas > 1)
			{
				for ($a=2;$a<=$NumLinhas;$a++)
				{
					array_push($NotasAluno, $XPATH->query("following-sibling::*[1]", $NotasAluno[0])->item(0));
					$NumNotas += $XPATH->query("td", $NotasAluno[$a-1])->length;
				}				
			}
			echo $NumNotas;
			*/
		}
	//}
	
	echo "<hr id='comeca resposnse'>".$response;
	//echo $response;
	
	/*
	 <SigmaWeb>
	<Aluno>
	<Nome>Matheus</Nome>
	<Status>4 - Matriculas Fechadas</Status>
	<FotoHash>sdsdj3ne3hdsa</FotoHash>
	<Semestre>2014/1</Semestre>
	<Matriculado>2013/2</Matriculado>
	</Aluno>
	<Materia COD="CDI2001" Nome="Calculo Diferencial e Integral 2" Turma="E">
	<Nota Peso="30%" Desc="Minha nota 123">10.5</Nota>
	<Exame>5.0</Exame>
	</Materia>
	</SigmaWeb>
	*/
?>
