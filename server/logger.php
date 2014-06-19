<?php
ini_set('default_charset','UTF-8');

class Logger
{
	function Logger($username, $version, $msg, $nome="", $centro="")
	{
		file_put_contents('logs/access.htm', date("d/m/y H:i")." | ".getenv("REMOTE_ADDR")." | ".$username." | <b>".$nome."</b> | ".$centro." | ".$version." | ".$msg."<br>", FILE_APPEND | LOCK_EX);
	}
}
