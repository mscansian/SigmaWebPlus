<h2 class="sub-header">Acessos válidos</h2>
          <div class="table-responsive">
            <table class="table table-striped">
              <thead>
                <tr>
                  <th>Data</th>
                  <th>IP</th>
                  <th>Matricula</th>
                  <th>Nome</th>
                  <th>Versao</th>
                </tr>
              </thead>
              <tbody>
              <?php
	              $result = $database->query("SELECT CONVERT_TZ(data,'UCT','Brazil/East') AS data, ip, requests.matricula AS mat, nome, versao FROM requests JOIN users ON users.matricula = requests.matricula ORDER BY data DESC");
				  while ($item = $database->fetch($result))
				  {
	              	echo '<tr><td>'.$item['data'].'</td><td><a href="?class=ip&ip='.$item['ip'].'">'.$item['ip'].'</a></td><td><a href="?class=usuario&matricula='.$item['mat'].'">'.$item['mat'].'</a></td><td>'.$item['nome'].'</td><td>'.$item['versao'].'</td></tr>';
				  }
	             
              ?>
              </tbody>
            </table>
          </div>