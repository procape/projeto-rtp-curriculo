# projeto-rtp-curriculo

Aplicação web para gerenciamento de currículos com arquitetura modular.

## 🏗️ Arquitetura

O projeto segue uma arquitetura modular inspirada em boas práticas como Clean Architecture.

A aplicação é dividida por domínios (modules) e por camadas internas, garantindo separação de responsabilidades e facilidade de manutenção.

### Conceitos aplicados

- Separação por domínio (modules)
- Camadas bem definidas (Controller → Service → Repository)
- Reutilização de código (core)
- Controle de acesso por roles (USER / ADMIN)
- Configuração via variáveis de ambiente (.env)

---

## 🔄 Fluxo da aplicação

Request → Route → Controller → Service → Repository → Database

### Explicação

- Route: define os endpoints
- Controller: recebe a requisição HTTP
- Service: aplica regras de negócio
- Repository: acessa o banco de dados
- Database: persistência

---

## 📂 Estrutura de Pastas

backend/
├── config/
├── core/
├── database/
├── modules/
├── routes/
├── main.py
├── server.py
└── Dockerfile

---

## ⚙️ config/

Responsável pelas configurações da aplicação.

config/
└── settings.py

Funções:
- leitura de variáveis de ambiente
- configuração do banco
- configuração do JWT

---

## 🧠 core/

Contém código reutilizável em toda a aplicação.

core/
├── database/
├── exceptions/
├── middlewares/
├── security/
└── utils/

- database: conexão com banco
- exceptions: tratamento de erros
- middlewares: autenticação e autorização
- security: JWT e hash de senha
- utils: funções auxiliares

---

## 🐬 database/

database/
└── init.sql

Responsável pela criação das tabelas e estrutura do banco.

---

## 📦 modules/

modules/
├── auth/
├── users/
├── curriculos/
└── admin/

Cada módulo representa um domínio da aplicação.

---

## 🔐 auth/

auth/
├── auth_controller.py
├── auth_service.py
└── auth_routes.py

Responsável por login, registro e geração de JWT.

---

## 👤 users/

users/
├── user_controller.py
├── user_service.py
├── user_repository.py
├── user_model.py
└── user_routes.py

Responsável pelo CRUD de usuários.

---

## 📄 curriculos/

curriculos/
├── curriculo_controller.py
├── curriculo_service.py
├── curriculo_repository.py
├── curriculo_model.py
└── curriculo_routes.py

Responsável pelo CRUD de currículos.

---

## 🛠️ admin/

admin/
├── admin_controller.py
├── admin_service.py
└── admin_routes.py

Responsável por ações administrativas como:

- criação de usuários
- reset de senha
- dashboard

---

## 🌐 routes/

routes/
└── router.py

Centraliza todas as rotas da aplicação.

---

## 🚀 main.py

Ponto de entrada da aplicação.

Responsável por iniciar o servidor.

---

## 🖥️ server.py

Responsável por subir o servidor HTTP e tratar as requisições.

---

## 🔐 Autenticação

- JWT implementado manualmente
- controle de acesso por roles:
  - USER
  - ADMIN

---

## 🐳 Docker

A aplicação é containerizada com:

- backend (Python)
- frontend (Bootstrap)
- MySQL

---

## ⚙️ Variáveis de ambiente

O projeto utiliza:

- backend/.env (desenvolvimento backend)
- frontend/.env (desenvolvimento frontend)
- .env (docker/produção)
- .env.example (template)

Para o segundo banco de dados MySQL remoto, você pode usar as variáveis:

- `MYSQL2_HOST`
- `MYSQL2_PORT`
- `MYSQL2_USER`
- `MYSQL2_PASSWORD`
- `MYSQL2_DATABASE`
- `DATABASE2_URI` (opcional: cadeia de conexão completa)

---

## 🎯 Benefícios da arquitetura

- código organizado
- fácil manutenção
- escalável
- baixo acoplamento
- preparado para microserviços