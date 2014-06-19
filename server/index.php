<?php
	//Seta o charset para UTF8 para suportar acentos
	ini_set('default_charset','UTF-8');
	
	require 'requestHandler.php';
	require 'aluno.php';
	
	//Get data from request and validate
	$myRequest = new Request();
	$myRequest->validadeRequest();
	
	//Create new Aluno and get data from SigmaWeb
	$myAluno = new Aluno($myRequest->getRequestUsername(), $myRequest->getRequestPassword(), $myRequest);
	$myAluno->refresh();
	
	
	//Generate the output
	$output = "<SigmaWeb>
	<Aluno>
		<Nome>"     .$myAluno->getDados('Nome')     ."</Nome>
		<Matricula>".$myAluno->getDados('Matricula')."</Matricula>
		<TipoAluno>".$myAluno->getDados('TipoAluno')."</TipoAluno>
		<Status>"   .$myAluno->getDados('Status')   ."</Status>
		<Semestre>" .$myAluno->getDados('Semestre') ."</Semestre>
		<Centro>"   .$myAluno->getDados('Centro')   ."</Centro>
	</Aluno>
	<Materias>\n";

	foreach ($myAluno->getDados('Materias') as $Turma)
	{
		$output .= "		<Materia COD='".$Turma['Codigo']."' Nome='".$Turma['Nome']."' Turma='".$Turma['Turma']."' Centro='".$Turma['Centro']."'>\n";
		if (isset($Turma['Notas']))
		{
			foreach ($Turma['Notas'] as $Nota)
			{
				$output .= "			<Nota Peso='".$Nota['Peso']."' Desc='".$Nota['Nome']."'>".$Nota['Nota']."</Nota>\n";
			}
			$output .= "			<Exame>".$Turma['Exame']."</Exame>\n";
			$output .= "			<MediaFinal>".$Turma['MediaFinal']."</MediaFinal>\n";
		}
		$output .= "		</Materia>\n";
	}
	$output .= "	</Materias>\n";
	$output .= "</SigmaWeb>";
	
	//Save request
	$myRequest->saveValidRequest($output);
	
	//Hash the output and respond
	$output_hash = md5($output); #Debug
	
	if ($myRequest->hash == $output_hash)
	{
		die('Up-to-date');
	}
	else
	{
		echo $output_hash."\n";
		echo $output;
	}

?>
