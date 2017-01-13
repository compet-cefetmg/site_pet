# site-pet
### Ambiente virtual
Para executar a aplicação, é recomendada a utilização de um ambiente virtual, por meio do `virtualenvwrapper`.
Após instalar o `virtualenvwrapper`, faça o seguinte comando para criar um ambiente virtual:
```
mkvirtualenv -p python3 site-pet
```

Sempre que for executar o projeto, inicie o ambiente virtual:
```
workon site-pet
```

### Dependências
Para instalar as dependências da aplicação, utilize o seguinte comando:
```
pip install -r requirements.txt
```

### Variáveis de ambiente
Adicione a variável de ambiente `DATABASE_URL` ao arquivo `~/.virtualenvs/site-pet/bin/activate`, substituindo pelas informações da sua conexão ao banco de dados. Exemplo:
```
export DATABASE_URL='mysql://<user>:<password>@localhost:3306/<database>'
```

### Preparação do banco de dados
Execute o seguinte comando para criar as relações no seu banco de dados local:
```
./manage.py migrate
```

### Execução
```
./manage.py runserver
```
