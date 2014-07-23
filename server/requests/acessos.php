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
	              $result = $database->query("SELECT data, ip, requests.matricula AS mat, nome, versao FROM requests JOIN users ON users.matricula = requests.matricula ORDER BY data DESC");
				  while ($item = $database->fetch($result))
				  {
	              	echo '<tr><td>'.$item['data'].'</td><td>'.$item['ip'].'</td><td>'.$item['mat'].'</td><td>'.$item['nome'].'</td><td>'.$item['versao'].'</td></tr>';
				  }
	             
              ?>
              </tbody>
            </table>
          </div>