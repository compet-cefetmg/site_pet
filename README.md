# site-pet
### Ambiente virtual
Para executar a aplicação, é recomendada a utilização de um ambiente virtual, por meio do `virtualenvwrapper`.
Após instalar o `virtualenvwrapper`, faça o seguinte cvomando para criar um ambiente virtual:
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
Adicionar as variáveis de ambiente ao arquivo `~/.virtualenvs/site-pet/bin/activate`, substituindo pelas informações da sua conexão ao banco de dados.
```
export DATABASE_NAME='database-name'
export DATABASE_USER='database-user'
export DATABASE_PASSWORD='database-password'
export SECRET_KEY='django-secret-key'
```

### Execução
```
./manage.py runserver
```
