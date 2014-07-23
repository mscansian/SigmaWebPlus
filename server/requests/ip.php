<h2 class="sub-header">Detalhes do IP <?php  echo $_GET['ip'];?></h2>
          <div class="table-responsive">
            <table class="table table-striped">
              <thead>
                <tr>
                  <th>Data</th>
                  <th>Matricula</th>
                  <th>Versão</th>
                  <th>Manual</th>
                </tr>
              </thead>
              <tbody>            
              <?php
              if (filter_var($_GET['ip'], FILTER_VALIDATE_IP))
              {
              	$ip = $_GET['ip'];
              }
              
              $result = $database->query("SELECT CONVERT_TZ(data,'UCT','Brazil/East') AS data, matricula, versao, update_force, hash FROM requests WHERE ip = '$ip' ORDER BY data DESC");
              while ($item = $database->fetch($result))
              {
              	echo '<tr><td>'.$item['data'].'</td><td><a href="?class=usuario&matricula='.$item['matricula'].'">'.$item['matricula'].'</a></td><td>'.$item['versao'].'</td><td>'.(($item['update_force']=='1')?('Sim'):(($item['hash']=='')?('Primeiro acesso'):('Não'))).'</td></tr>';
              }
              
              ?>
            </table>
          </div>