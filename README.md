# 🎮 Preditor de FPS & Otimizador de PC (CS:GO)

Este é um projeto full stack integrado a um modelo de **Machine Learning** desenvolvido para a disciplina de Aprendizado de Máquina. O sistema é capaz de prever o FPS médio esperado para o jogo CS:GO (1080p Low) com base em configurações de hardware, além de otimizar e recomendar montagens completas de computadores que respeitem um limite de orçamento.

O repositório está estruturado como um monorepo, contendo o backend em Django na raiz e o frontend em React dentro da pasta `/frontend`.

---

## 🛠️ Tecnologias Utilizadas

### Backend
* **Linguagem:** Python 3.10+
* **Framework Web:** Django & Django REST Framework (DRF)
* **Machine Learning:** Scikit-Learn & Joblib (Gradient Boosting Regressor)
* **Manipulação de Dados:** Pandas & Numpy
* **Documentação:** OpenAPI 3 & Swagger (via `drf-spectacular`)
* **Banco de Dados:** SQLite (padrão de desenvolvimento)

### Frontend
* **Ambiente de Execução:** Node.js (v22.19+) & TypeScript
* **Biblioteca Principal:** React
* **Estilização:** Tailwind CSS

---

## 🚀 Como Rodar o Projeto Localmente

### 1. Clonar o Repositório
```bash
git clone [https://github.com/oJoaoNeto/fps_predict.git](https://github.com/oJoaoNeto/fps_predict.git)
cd fps_predict

```

### 2. Configurando o Backend (Django)

**Criar e ativar o ambiente virtual (venv):**

* *No Windows (PowerShell):*
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1

```


* *No Linux/macOS:*
```bash
python3 -m venv venv
source venv/bin/activate

```



**Instalar as dependências do Python:**

```bash
pip install -r requirements.txt

```

**Executar as migrações e alimentar o banco de dados (Seed):**

```bash
python manage.py migrate
python manage.py seed_data

```

**Iniciar o servidor do Backend:**

```bash
python manage.py runserver

```

O backend estará disponível em: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

### 3. Configurando o Frontend (React)

Abra um novo terminal, navegue até a pasta do frontend e instale as dependências do Node:

```bash
cd frontend
npm install

```

**Iniciar o servidor de desenvolvimento do Frontend:**

```bash
npm run dev

```

O terminal indicará a URL local onde o frontend está rodando (geralmente [http://localhost:5173/](http://localhost:5173/)).

---

## 📖 Documentação da API

### Documentação Interativa (Swagger)

Com o servidor do backend rodando, acesse a interface interativa para testar os endpoints diretamente pelo navegador:

* **Swagger UI:** [http://127.0.0.1:8000/api/schema/swagger-ui/](http://127.0.0.1:8000/api/schema/swagger-ui/)
* **ReDoc:** [http://127.0.0.1:8000/api/schema/redoc/](http://127.0.0.1:8000/api/schema/redoc/)

---

## 🧠 Integração com Machine Learning

O modelo de previsão utiliza um regressor do tipo **Gradient Boosting** treinado a partir de dados reais do UserBenchmark agregados por combinação única de hardware (CPU + GPU). O treinamento do modelo é feito via Jupyter Notebook.

Se você precisar retreinar o modelo ou atualizar os arquivos `.pkl` após mudanças no dataset (`csv_result-fps-in-video-games.csv`), basta executar o script auxiliar na raiz do projeto:

```bash
python train_model.py

```

*(Nota: Certifique-se de baixar o dataset utilizando o link indicado no arquivo `requirements(1).pdf`).*

---

## 🧪 Como Executar os Testes Automatizados

O projeto conta com testes unitários no backend para validar a consistência física da predição de FPS e a lógica de compatibilidade de peças e orçamento do otimizador de PC. Na raiz do projeto, execute:

```bash
python manage.py test

```
