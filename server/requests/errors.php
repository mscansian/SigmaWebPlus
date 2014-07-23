<h2 class="sub-header">Acessos inválidos</h2>
          <div class="table-responsive">
            <table class="table table-striped">
              <thead>
                <tr>
                  <th>Data</th>
                  <th>IP</th>
                  <th>Matricula</th>
                  <th>Versao</th>
                  <th>Erro</th>
                </tr>
              </thead>
              <tbody>
              <?php
	              $result = $database->query("SELECT CONVERT_TZ(data,'UCT','Brazil/East') AS data, ip, matricula, versao, error, invalidcredentials, notes FROM requests WHERE error = 1 OR invalidcredentials = 1 ORDER BY data DESC");
				  while ($item = $database->fetch($result))
				  {
	              	echo '<tr><td>'.$item['data'].'</td><td><a href="?class=ip&ip='.$item['ip'].'">'.$item['ip'].'</a></td><td><a href="?class=usuario&matricula='.$item['matricula'].'">'.$item['matricula'].'</a></td><td>'.$item['versao'].'</td><td>'.(($item['error']==1)?($item['notes']):('Matrícula ou senha incorreta')).'</td></tr>';
				  }
	             
              ?>
              </tbody>
            </table>
          </div>