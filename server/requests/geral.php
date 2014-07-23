<h2 class="sub-header">Estatísticas de uso</h2>
          <div class="table-responsive">
            <table class="table table-striped">
              <thead>
                <tr>
                  <th>KPI</th>
                  <th>Valor</th>
                </tr>
              </thead>
              <tbody>
              <?php
	              $result = $database->query("SELECT COUNT(*) FROM requests");
	              $data = $database->fetch($result);
	              echo '<tr><td>Total de acessos ao servidor</td><td>'.$data[0].'</td></tr>';
	              
	              $result = $database->query("SELECT COUNT(*) FROM requests WHERE error='0' AND invalidcredentials='0'");
	              $data = $database->fetch($result); $requests = $data[0];
	              echo '<tr><td>Total de acessos completados com sucesso</td><td>'.$data[0].'</td></tr>';
	              
	              $result = $database->query("SELECT COUNT(*) FROM requests WHERE invalidcredentials='1'");
	              $data = $database->fetch($result);
	              echo '<tr><td>Total de acessos com matricula/senha incorretas</td><td>'.$data[0].'</td></tr>';
	              
	              $result = $database->query("SELECT COUNT(*) FROM requests WHERE error='1'");
	              $data = $database->fetch($result);
	              echo '<tr><td>Total de acessos resultantes em erro</td><td>'.$data[0].'</td></tr>';
	              
	              $result = $database->query("SELECT COUNT(*) FROM users");
	              $data = $database->fetch($result); $users = $data[0];
	              echo '<tr><td>Total de usuários diferentes cadastrados</td><td>'.$data[0].'</td></tr>';
	              
	              $result = $database->query("SELECT COUNT(*) FROM (SELECT DISTINCT centro FROM users) AS centros");
				  $data = $database->fetch($result);
				  echo '<tr><td>Total de centros diferentes cadastrados</td><td>'.$data[0].'</td></tr>';
              ?>
              </tbody>
            </table>
          </div>