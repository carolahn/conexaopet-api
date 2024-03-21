from django.contrib.auth.hashers import make_password

# Senha em texto plano
plain_password = '123456'

# Calculando o hash da senha
hashed_password = make_password(plain_password)

print(hashed_password)
