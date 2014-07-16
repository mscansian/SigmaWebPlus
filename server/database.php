<?php 
defined('VALID_ENTRY_POINT') or die('');
require_once 'config.php';

class cDatabase
{
	private $connection;
	
	public function connect()
	{	
		if (!$this->connection)
		{
			$this->connection = mysql_connect($CONFIG['DB']['hostname'], $CONFIG['DB']['username'], $CONFIG['DB']['password']);
			if (!$this->connection)
			{
				die('Fatal: Could not connect to the datatabase');
			}
			
			if (!mysql_select_db($CONFIG['DB']['name'], $this->connection))
			{
				die('Fatal: Could not select specified database');
			}
		}
	}
	
	public function disconnect()
	{
		if ($this->connection)
		{
			mysql_close($this->connection);
		} 
	}
	
	public function query($sql_query, $fetch=false)
	{
		$this->connect();
		$result = mysql_query($sql_query, $this->connection);
		if ($fetch)
		{
			return $this->fetch($result);
		}
		else
		{
			return $result;
		}
	}
	
	public function fetch($result)
	{
		return mysql_fetch_array($result);
	}
	
	public function rows($result)
	{
		return mysql_num_rows($result);
	}
}
?>