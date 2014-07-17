<?php
define('VALID_ENTRY_POINT', '1');

ini_set('default_charset','UTF-8'); //Seta o charset para UTF8 para suportar acentos
date_default_timezone_set('America/Sao_Paulo');

require_once 'request.php';
require_once 'sigmaweb.php';

//Get data from request and validate
$request = new cRequest();

//Rotina de teste
if ($request->get_username() == 690690690)
{
	$output = file_get_contents('testfile.txt');
	$output_hash = md5($output);
	echo $output_hash."\n";
	echo $output;
	die('');
}

if ($request->is_valid())
{
	if (!$request->get_cache())
	{	
		$aluno = new cSigmaWeb($request->get_username(), $request->get_password());
		try
		{
			$aluno->refresh();
		}
		catch (Exception $e)
		{
			if ($e->getMessage() == 'Auth error')
			{
				$request->wrongpassword();
			}
			else
			{
				$request->error($e->getMessage());
			}
			echo '<error>'.$e->getMessage().'</error>';
			die('');
		}
		
		//Sucesso! Cria o codigo XML
		$output = "<SigmaWeb>
	<Aluno>
		<Nome>"     .$aluno->getDados('Nome')     ."</Nome>
		<Matricula>".$aluno->getDados('Matricula')."</Matricula>
		<TipoAluno>".$aluno->getDados('TipoAluno')."</TipoAluno>
		<Status>"   .$aluno->getDados('Status')   ."</Status>
		<Semestre>" .$aluno->getDados('Semestre') ."</Semestre>
		<Centro>"   .$aluno->getDados('Centro')   ."</Centro>
	</Aluno>
	<Materias>\n";
		
		foreach ($aluno->getDados('Materias') as $Turma)
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
		
		//Calcula o Hash e salva o request
		$output_hash = md5($output);
		$request->success($aluno->getDados('Nome'), $aluno->getDados('Centro'), $aluno->getDados('TipoAluno'), $output);
		
		if ($output_hash == $request->get_hash())
		{
			echo 'Up-to-date';
		}
		else
		{
			echo $output_hash."\n";
			echo $output;
		}
	}
	else
	{
		//Returning request from cache
		$output = $request->get_cache();
		$output_hash = md5($output);
		
		if ($output_hash == $request->get_hash())
		{
			echo 'Up-to-date';
		}
		else
		{
			echo $output_hash."\n";
			echo $output;
		}
	}
}
else
{
	//Error request not valid
	echo '<error>invalid request</error>';
}
?>
