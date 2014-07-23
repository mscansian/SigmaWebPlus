<h2 class="sub-header">Detalhes do usuário <?php  echo $_GET['matricula'];?></h2>
          <div class="table-responsive">
            <table class="table table-striped">
              <thead>
                <tr>
                  <th>Descrição</th>
                  <th>#</th>
                </tr>
              </thead>
              <tbody>
              <?php
              	  $matricula = intval($_GET['matricula']);
              
	              $result = $database->query("SELECT nome, centro, tipo, versao, totalreq, update_auto, update_timeout FROM users INNER JOIN (SELECT tab1.matricula, versao, totalreq FROM (SELECT requests.matricula, versao FROM requests INNER JOIN (SELECT requests.matricula, MAX(data) AS maxdata FROM requests GROUP BY matricula) as tab1 ON tab1.matricula = requests.matricula AND maxdata = data) AS tab1 INNER JOIN (SELECT matricula, COUNT(data) AS totalreq FROM requests GROUP BY matricula) AS tab2 ON tab1.matricula = tab2.matricula) AS sr ON users.matricula = sr.matricula WHERE users.matricula = $matricula ORDER BY totalreq DESC");
				  $item = $database->fetch($result);
				  echo '<tr><td>Matricula</td><td>'.$matricula.'</td></tr>';
				  echo '<tr><td>Nome</td><td>'.(($item['nome']!='')?($item['nome']):('[não disponível]')).'</td></tr>';
				  echo '<tr><td>Centro</td><td>'.(($item['centro']!='')?($item['centro']):('[não disponível]')).'</td></tr>';
				  echo '<tr><td>Tipo Aluno</td><td>'.(($item['tipo']!='')?($item['tipo']):('[não disponível]')).'</td></tr>';
				  echo '<tr><td>Versão</td><td>'.(($item['versao']!='')?($item['versao']):('[não disponível]')).'</td></tr>';
				  echo '<tr><td>Total de acessos</td><td>'.(($item['totalreq']!='')?($item['totalreq']):('[não disponível]')).'</td></tr>';
				  echo '<tr><td>Total de acessos com senha incorreta</td><td>[não disponível]</td></tr>';
				  echo '<tr><td>Total de acessos resultantes em erro</td><td>[não disponível]</td></tr>';
				  echo '<tr><td>Config: Atualizar automaticamente</td><td>'.(($item['update_auto']=='1')?('Sim'):(($item['update_auto']=='0')?('Não'):('[não disponível]'))).'</td></tr>';
				  echo '<tr><td>Config: Timeout de atualização</td><td>'.(($item['update_timeout']=='')?('[não disponível]'):($item['update_timeout'])).'</td></tr>';
	             
              ?>
              </tbody>
              </table>
          </div>
<h2 class="sub-header">Acessos do usuário</h2>
          <div class="table-responsive">
            <table class="table table-striped">
              <thead>
                <tr>
                  <th>Data</th>
                  <th>IP</th>
                  <th>Versão</th>
                  <th>Manual</th>
                </tr>
              </thead>
              <tbody>            
              <?php
              
              $result = $database->query("SELECT CONVERT_TZ(data,'UCT','Brazil/East') AS data, ip, versao, update_force, hash FROM requests WHERE matricula = $matricula ORDER BY data DESC");
              while ($item = $database->fetch($result))
              {
              	echo '<tr><td>'.$item['data'].'</td><td><a href="?class=ip&ip='.$item['ip'].'">'.$item['ip'].'</a></td><td>'.$item['versao'].'</td><td>'.(($item['update_force']=='1')?('Sim'):(($item['hash']=='')?('Primeiro acesso'):('Não'))).'</td></tr>';
              }
              
              ?>
            </table>
          </div>