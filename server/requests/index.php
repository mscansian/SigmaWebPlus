<?php 
	define('VALID_ENTRY_POINT', '1');
	ini_set('default_charset','UTF-8');
	date_default_timezone_set('America/Sao_Paulo');

	require_once '../database.php';
	$database = new cDatabase();
	
	if (empty($_GET['class']))
	{
		$_GET['class'] = 'geral';
	}
	
	$Menu = array("Geral", "Acessos", "Usuários");
	
?><!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="../favicon.ico">

    <title>Painel de Administração do SigmaWeb+</title>

    <!-- Bootstrap core CSS -->
    <link href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="dashboard.css" rel="stylesheet">

    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <!-- <script src="../../assets/js/ie10-viewport-bug-workaround.js"></script>-->

    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>

    <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
      <div class="container-fluid">
        <div class="navbar-header">
          <a class="navbar-brand" href="index.php">SigmaWeb+ Server</a>
        </div>
      </div>
    </div>

    <div class="container-fluid">
      <div class="row">
        <div class="col-sm-3 col-md-2 sidebar">
          <ul class="nav nav-sidebar">
          	<?php
          		foreach ($Menu as $item)
          		{
          			echo '<li'.((strtolower($item) == $_GET['class'])?(' class="active"'):('')).'><a href="?class='.strtolower($item).'">'.$item.'</a></li>';
          		} 
          	?>
          </ul>
        </div>
        <div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
          <?php
          switch($_GET['class'])
          {
          	case 'geral':
          		echo '<h1 class="page-header">Geral</h1>';
          		include 'geral.php';
          		break;
          	case 'acessos':
          		echo '<h1 class="page-header">Acessos</h1>';
          		include 'acessos.php';
          		break;
          	case 'usuários':
          		echo '<h1 class="page-header">Usuários</h1>';
          		include 'usuarios.php';
          		break;
          } 
	      ?>          
        </div>
      </div>
    </div>

    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <script src="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>
    <!--<script src="../../assets/js/docs.min.js"></script>-->
  </body>
</html>
?>