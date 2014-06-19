<?php

//Inclui a classe que faz as solicitacoes HTTP
require_once ('curl.php');

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

class Aluno
{	
	private $username, $password;
	private $dadosAluno;
	
	public function Aluno($username, $password)
	{
		$this->username = $username;
		$this->password = $password;
	}
	
	public function getDados($tipo)
	{
		return $this->dadosAluno[$tipo];
	}
	
	public function refresh()
	{
		$request = new cUrl();
		
		//Login
		$response = $request->requestPost("https://sigmaweb.cav.udesc.br/sw/sigmaweba.php", array(LSIST => "SigmaWeb",LUNID => "UDESC",lusid => $this->username,luspa => $this->password,opta => "Login"));
		if ($response == "") { throw new Exception('Connection error'); }
		elseif ($response == '<html><head><META HTTP-EQUIV="Refresh" CONTENT="0;URL=sigmaweb0.php"></head></html>') { /*Auth okay, proceed*/ }
		else
		{
			$HTML = new DOMDocument; @$HTML->loadHTML($response); @$XPATH = new DOMXPath($HTML);
			$ErrorMsg = utf8_decode($XPATH->query('*/td',$XPATH->query('*/table')->item(1))->item(1)->nodeValue);
			if ($ErrorMsg == "Matrícula e/ou senha inválida")
			{
				throw new Exception('Auth error');
			}
			else
			{
				throw new Exception('Custom error msg: '.$ErrorMsg);
			}
			unset($HTML); unset($XPATH);
		}
		
		//Get main page
		$response = $request->requestGet("https://sigmaweb.cav.udesc.br/sw/sigmaweb0.php");
		if ($response == "") { throw new Exception('Connection error'); }
		else
		{
			$HTML = new DOMDocument; @$HTML->loadHTML($response); @$XPATH = new DOMXPath($HTML);
			$this->dadosAluno['Centro'] = $XPATH->query('*/td',$XPATH->query('*/table')->item(0))->item(1)->nodeValue;
			
			$this->dadosAluno['Nome'] = explode("<br>",DOMinnerHTML($XPATH->query('*/td',$XPATH->query('*/table')->item(0))->item(2))); $this->dadosAluno['Nome'] = $this->dadosAluno['Nome'][0];
			$this->dadosAluno['Matricula'] = explode("<br>",DOMinnerHTML($XPATH->query('*/td',$XPATH->query('*/table')->item(0))->item(2))); $this->dadosAluno['Matricula'] = explode(" - ", $this->dadosAluno['Matricula'][1]); $this->dadosAluno['Matricula'] = $this->dadosAluno['Matricula'][0];
			$this->dadosAluno['TipoAluno'] = explode("<br>",DOMinnerHTML($XPATH->query('*/td',$XPATH->query('*/table')->item(0))->item(2))); $this->dadosAluno['TipoAluno'] = explode(" - ", $this->dadosAluno['TipoAluno'][1]); $this->dadosAluno['TipoAluno'] = $this->dadosAluno['TipoAluno'][1];
	
			
			$this->dadosAluno['Semestre'] = DOMinnerHTML($XPATH->query('td',$XPATH->query('*/tr',$XPATH->query('*/td',$XPATH->query('*/table')->item(2))->item(2))->item(4))->item(0));
			$this->dadosAluno['Status'] = DOMinnerHTML($XPATH->query('td',$XPATH->query('*/tr',$XPATH->query('*/td',$XPATH->query('*/table')->item(2))->item(2))->item(5))->item(0));
			unset($HTML); unset($XPATH);
		}
		
		//Get turmas
		$Turmas = array();
		$request->requestGet("https://sigmaweb.cav.udesc.br/sw/sigmaweb1.php?var=R6655");
		$response = $request->requestGet("https://sigmaweb.cav.udesc.br/sw/sigmaweb4.php");
		if ($response == "") { throw new Exception('Connection error'); }
		if (strstr($response,"Não há matrícula efetivada para "))
		{
			//Erro, nao ha materias!
		}
		else
		{
			$response = $request->requestGet("https://sigmaweb.cav.udesc.br/sw/sigmaweb5.php");
			if ($response == "") { throw new Exception('Connection error'); }
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
			if ($response == "") { throw new Exception('Connection error'); }
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
		
		//Buscar pela media final e nota do exame
		if (sizeof($Turmas) > 0);
		{
			$request->requestGet("https://sigmaweb.cav.udesc.br/sw/sigmaweb0.php");
			$request->requestGet("https://sigmaweb.cav.udesc.br/sw/sigmaweb1.php?var=R6645");
			$request->requestGet("https://sigmaweb.cav.udesc.br/sw/sigmaweb4.php");
			$request->requestGet("https://sigmaweb.cav.udesc.br/sw/sigmaweb6.php");
			$request->requestPost("https://sigmaweb.cav.udesc.br/sw/sigmaweb7.php", array(nseme => substr($this->getDados('Semestre'),-6), opta => 'Avancar'));
			$response = $request->requestGet("https://sigmaweb.cav.udesc.br/sw/sigmaweb7.php");
			if ($response == "") { throw new Exception('Connection error'); }
			
			$HTML = new DOMDocument; @$HTML->loadHTML($response); @$XPATH = new DOMXPath($HTML);
			for ($TurmaID=0; $TurmaID<sizeof($Turmas); $TurmaID++)
			{
				$totalColspan = 0;
				for ($Coluna=0; $Coluna<=11; $Coluna++)
				{
					switch ($Coluna)
					{
						case 9:
							$Turmas[$TurmaID]['Exame'] = DOMinnerHTML($XPATH->query("/html/body/table[2]/tr[".(3+$TurmaID)."]/td")->item($Coluna - $totalColspan));
							if (strlen($Turmas[$TurmaID]['Exame']) > 4) { $Turmas[$TurmaID]['Exame'] = "";}
							break;
						case 10:
							$Turmas[$TurmaID]['MediaFinal'] = DOMinnerHTML($XPATH->query("/html/body/table[2]/tr[".(3+$TurmaID)."]/td")->item($Coluna - $totalColspan));
							if (strlen($Turmas[$TurmaID]['MediaFinal']) > 4) { $Turmas[$TurmaID]['MediaFinal'] = ""; }
							break;
					}
					
					$colspan = $XPATH->query("/html/body/table[2]/tr[".(3+$TurmaID)."]/td")->item($Coluna - $totalColspan)->getAttribute('colspan');
					if ($colspan=="") { $colspan = 1; }
					
					
					$totalColspan += ($colspan - 1);
					$Coluna += ($colspan - 1);
				}
			}
			unset($HTML); unset($XPATH);
		}
		
		
		$this->dadosAluno['Materias'] = $Turmas;
	}
}
?>