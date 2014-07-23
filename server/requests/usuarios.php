
          <div class="table-responsive">
            <table class="table table-striped">
              <thead>
                <tr>
                  <th>Nome</th>
                  <th>Matricula</th>
                  <th>Centro</th>
                  <th>Versao</th>
                  <th># Acessos</th>
                </tr>
              </thead>
              <tbody>
              <?php
	              $result = $database->query("SELECT nome, sr.matricula, centro, versao, totalreq FROM users INNER JOIN (SELECT tab1.matricula, versao, totalreq FROM (SELECT requests.matricula, versao FROM requests INNER JOIN (SELECT requests.matricula, MAX(data) AS maxdata FROM requests GROUP BY matricula) as tab1 ON tab1.matricula = requests.matricula AND maxdata = data) AS tab1 INNER JOIN (SELECT matricula, COUNT(data) AS totalreq FROM requests GROUP BY matricula) AS tab2 ON tab1.matricula = tab2.matricula) AS sr ON users.matricula = sr.matricula ORDER BY totalreq DESC");
				  while ($item = $database->fetch($result))
				  {
	              	echo '<tr><td>'.$item['nome'].'</td><td>'.$item['matricula'].'</td><td>'.$item['centro'].'</td><td>'.$item['versao'].'</td><td>'.$item['totalreq'].'</td></tr>';
				  }
	             
              ?>
              </tbody>
            </table>
          </div>