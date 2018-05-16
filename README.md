pip# site-pet

### Instalação
```
  - `sudo apt-get install build-essential` e `pip install --upgrade setuptools pip`
  - `sudo apt-get install python3`
  - `sudo apt-get install python3-venv`
  - `sudo apt-get install python3-pip`
  - `sudo apt-get install mysql-server`
  - `sudo apt-get install libmysqlclient-dev`
  - `sudo apt-get install libpq-dev python3-dev` // egg_info (psycopg2 requirement)
  - `sudo apt-get install libjpeg8-dev` // Pillow requirement

```
  -Alternative names for libraries:
```
    libmysqlclient-devel
    libjpeg8-devel
    libpq-devel
    python3-devel
```

Edite as configurações do mySqlServer(o caminho pode varia, ex: `/etc/mysql/my.cnf`):
```
sudo vi /etc/my.cnf  
```
```
[client]
password  = .compet2015
port       = 3306
socket     = /var/run/mysql/mysql.sock
```
ou 
```
[client]
password  = .compet2015
port       = 3306
socket     = /var/run/mysqld/mysqld.sock
```

### Ambiente virtual
Para executar a aplicação, é recomendada a utilização de um ambiente virtual, por meio do `virtualenvwrapper`.
Após instalar o `virtualenvwrapper`, faça o seguinte comando para criar um ambiente virtual:
```
mkvirtualenv -p python3 site-pet
```
ou
```
python3 -m venv site-pet
```

Sempre que for executar o projeto entre na pasta do projeto e execute e inicie o ambiente virtual:
```
source /bin/activate
```
ou 
```
workon site-pet
```


### Primeira Execução

Inicie o serviço do banco:
```
sudo /etc/init.d/mysql start
```
ou
```
sudo systemctl start mysql.service
```

Crie o banco de dados e o usuario:
```
sudo mysql -u root -p
mysql> CREATE USER 'compet'@'localhost' IDENTIFIED BY '.compet2015';
mysql> GRANT ALL PRIVILEGES ON * . * TO 'compet'@'localhost';
mysql> FLUSH PRIVILEGES;
mysql> CREATE DATABASE site_pet;
exit
```

Inicie o ambiente:
```
cd site_pite
source ../bin/activate
```

Adicione a variável de ambiente `DATABASE_URL` ao arquivo `site-pet/bin/activate`, substituindo pelas informações da sua conexão ao banco de dados.
```
export DATABASE_URL='mysql://compet:.compet2015@localhost:3306/site_pet'
```

Instale as dependencias do site:
```
pip3 install pymysql
pip3 install -r requirements.txt --user 
pip3 install -r requirements_trouble.txt
```
- Pode dar erro, os comandos abaixo devem solucionar caso tenha os problemas citados;
      - **Fail**: `Command python setup.py egg_info failed with error code 1` in psycopg2 installation in requirements.txt
        - `sudo apt-get install postgresql-server-dev-all` // Opcional
      - **Fail**: installation of Pillow in requeriments.txt
        - `sudo ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib` // link necessario em alguns casos, tente sem antes

Execute o seguinte comando para criar as relações no seu banco de dados local:
```
./manage.py migrate --run-syncdb
```
Carregue os dados essenciais do banco
```
./manage.py loadcefetdata
```

### Execução
Inicie o serviço do banco:
```
sudo /etc/init.d/mysql start
```
ou
```
sudo systemctl start mysql.service
```

Inicie o serviço do site:
```
./manage.py runserver
```


### Backup do banco
Use o comando abaixo para salvar o banco
```
python manage.py dumpdata > datadump.json
```
Use o comando abaixo para carregar o banco
```
python manage.py migrate --run-syncdb
python manage.py loaddata datadump.json
```
