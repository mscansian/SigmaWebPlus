SigmaWeb+
==============

SigmaWeb+ é um aplicativo direcionado aos alunos da Universidade do Estado de Santa Catarina (UDESC). O objetivo dele é fazer um monitoramento do [sistema academico](http://sigmaweb.cav.udesc.br) e avisar o usuário quando novos resultados de avaliações estão disponíveis.

Features
--------------
* **Fácil de utilizar:** Os menus são simples e instintivos
* **Multi-plataforma:** Funciona em Android, Windows e Linux
* **Seguro:** Todos os dados transmitidos são criptografados
* **Baixo trafego de dados:** Utiliza um servidor intermediário para otimizar o trafego de dados na rede (muito importante em conexões 3g)
* **Customizável:** Desenvolvido em python e publicado com o código aberto

Rodar aplicativo a partir do código fonte (Linux)
---------------------
Primeiramente é necessário fazer o download e instalar o [Android SDK](http://developer.android.com/sdk/index.html) e [Android NDK](http://developer.android.com/tools/sdk/ndk/index.html)

Copie o código fonte do SigmaWeb+ para o seu computador
```
$ git clone https://github.com/mscansian/SigmaWebPlus.git
$ cd SigmaWebPlus
$ git submodule update
```

Configure o arquivo env_var.sh 
```
export ANDROIDSDK=CAMINHO-DO-SDK
export ANDROIDNDK=CAMINHO-DO-NDK
export ANDROIDAPI=VERSAO-DO-SDK
export ANDROIDNDKVER=VERSAO-DO-NDK
export PATH=$ANDROIDNDK:$ANDROIDSDK/platform-tools:$ANDROIDSDK/tools:$PATH
```

Instale as dependências
```
$ make install
```

Iniciando o aplicativo no Linux
```
$ make
```

Iniciando o aplicativo no Android (ative 'USB debugging' no celular e conecte ele no computador)
```
$ make android
```
(Estes passos foram testados no Ubuntu 14.04 LTS)

Dependências
-----------
* [Android SDK](http://developer.android.com/sdk/index.html) [(Licença)](http://creativecommons.org/licenses/by/2.5/)
* [Android NDK](http://developer.android.com/tools/sdk/ndk/index.html) [(Licença)](http://creativecommons.org/licenses/by/2.5/)
* [kivy](https://github.com/kivy/kivy) (incluso no Makefile) [(Licença)](https://github.com/kivy/kivy/blob/master/LICENSE)
* [python-for-android](https://github.com/kivy/python-for-android) (incluso no Makefile) [(Licença)](https://github.com/kivy/python-for-android/blob/master/LICENSE)
* [python-singleinstance](https://github.com/mscansian/python-singleinstance) (incluso no GIT como submodule) [(Licença)](https://github.com/mscansian/python-singleinstance/blob/master/LICENSE)
* [python-threadcomm](https://github.com/mscansian/python-threadcomm) (incluso no GIT como submodule) [(Licença)](https://github.com/mscansian/python-threadcomm/blob/master/LICENSE)
* [notification-demo](https://github.com/brousch/kivy-notification-demo) (incluso no código)
* python-notify2 (incluso no Makefile)

Licença
-----------
[GNU LGPLv3](https://www.gnu.org/licenses/lgpl.html)
