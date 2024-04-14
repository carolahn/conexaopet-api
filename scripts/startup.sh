#!/bin/bash

# Ativando o ambiente virtual
source /srv/app/venv/bin/activate

# Iniciando o serviço do PostgreSQL
service postgresql start

# Aguardando o serviço estar disponível
until pg_isready --timeout=10; do
    echo "Aguardando o PostgreSQL iniciar..."
    sleep 1
done

# Executando as migrações do Django
su - postgres -c "python /srv/app/manage.py makemigrations"

# Acessando o diretório do aplicativo
cd /srv/app

# Populando o banco de dados
su - postgres -c "psql -U postgres -d conexaopet_db -a -f scripts/populate_db.sql"

# Continuando com a execução padrão do contêiner
exec "$@"
