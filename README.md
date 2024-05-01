# Conexão Pet - API  
[![Linkedin Badge](https://img.shields.io/badge/-Carol_Ahn-0077b5?labelColor=0077b5&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/carolina-ahn/)](https://www.linkedin.com/in/carolina-ahn/) 
![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=fff) 
![Django](https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=green) 
![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-336790?style=flat-square&logo=PostgreSQL&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=flat-square&logo=docker&logoColor=white)  

## Sobre  
Este projeto foi desenvolvido no curso de Pós Graduação em Desenvolvimento Full Stack da PUCRS, em 2024.  
Trata-se de uma aplicação web para a divulgação de animais e feiras de adoção, com o diferencial de enviar atualizações por e-mail aos interessados e de fornecer cupons de desconto em lojas do ramo aos usuários cadastrados na plataforma.  
O repositório do front-end encontra-se em: https://github.com/carolahn/conexaopet-web  

Utiliza-se a ferramenta GitHub Actions para realizar as rotinas de CI/CD, fazendo o deploy em uma instância EC2 da AWS, onde ocorre a execução dos contêineres do servidor Nginx, da API Rest Django e do banco de dados PostgreSQL.  
![image](https://github.com/carolahn/conexaopet-api/assets/62309069/f33c77b0-b6b3-4780-90e2-c07eccb3db36)

## Como reproduzir  

### Desenvolvimento local:

Clonar este repositório  
`git clone https://github.com/carolahn/conexaopet-api.git`

Acessar o diretório do projeto:  
`cd conexaopet-api`  

Executar contêineres  
`docker compose up --build`  

Teste a API realizando uma solicitação GET para  
`http://localhost:8000/api/addresses/all/`  

### Servir na EC2:  

Clonar este repositório  
`git clone https://github.com/carolahn/conexaopet-api.git`

Criar um novo repositório em branco no GitHub.  

Criar uma instância EC2 no site da AWS    
passo a passo: `https://youtu.be/W3CQ485oJKI`  
Configuração do grupo de segurança da instância EC2:  
![image](https://github.com/carolahn/conexaopet-api/assets/62309069/4818ccee-5f59-4ab3-ad44-d5ff44498d9f)  

Inserir os secrets no repositório GitHub, seguindo `.env.example.`  
Usar o endereço IP público da instância EC2 em `EC2_HOST_DNS`  
Em `EMAIL_HOST_PASSWORD`, se for gmail, é necessário criar uma "Senha de app" seguindo o passo a passo de `https://support.google.com/accounts/answer/185833?hl=pt-BR`  

Executar o push para o seu repositório e iniciar automaticamente a rotina do GitHub Actions e o deploy na instância AWS  
```
git add .
git commit "Initial commit"
git push origin main
```

Após finalizar o deploy, teste a API realizando uma solicitação GET (substitua pelo IP da sua instância EC2)   
`http://ec2-3-90-29-93.compute-1.amazonaws.com:8008/api/addresses/all/`  

