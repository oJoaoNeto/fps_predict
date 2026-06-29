# 🎮 Preditor de FPS & Otimizador de PC (CS:GO)

Este é o backend desenvolvido em **Python + Django** integrado a um modelo de **Machine Learning** para a disciplina de Aprendizado de Máquina. O sistema é capaz de prever o FPS médio esperado para o jogo CS:GO (1080p Low) com base em configurações de hardware, além de otimizar e recomendar montagens completas de computadores que respeitem um limite de orçamento.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.10+
* **Framework Web:** Django & Django REST Framework (DRF)
* **Machine Learning:** Scikit-Learn & Joblib (Gradient Boosting Regressor)
* **Manipulação de Dados:** Pandas & Numpy
* **Documentação:** OpenAPI 3 & Swagger (via `drf-spectacular`)
* **Banco de Dados:** SQLite (padrão de desenvolvimento)

---

## 🚀 Como Rodar o Projeto Localmente

### 1. Clonar o Repositório
```bash
git clone https://github.com/oJoaoNeto/fps_predict.git
cd fps_predict
```

### 2. Configurar o Ambiente Virtual (venv)
Crie e ative o ambiente virtual para isolar as dependências do projeto:

**No Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**No Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar as Dependências
Com o ambiente virtual ativado, instale todas as bibliotecas necessárias:
```bash
pip install -r requirements.txt
```

### 4. Executar as Migrações do Banco de Dados
Gere a estrutura das tabelas no SQLite:
```bash
python manage.py migrate
```

### 5. Alimentar o Banco de Dados (Seed)
Carregue os dados realistas de hardware (CPUs, GPUs, RAMs, Fontes, Placas-mãe, SSDs) com as especificações exigidas para a predição do modelo ML:
```bash
python manage.py seed_data
```

### 6. Executar o Servidor de Desenvolvimento
Inicie o servidor local do Django:
```bash
python manage.py runserver
```

O servidor estará disponível em: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 📖 Documentação da API

### Documentação Interativa (Swagger)
Com o servidor rodando, acesse a interface interativa da API para testar os endpoints diretamente pelo navegador:
* **Swagger UI:** [http://127.0.0.1:8000/api/schema/swagger-ui/](http://127.0.0.1:8000/api/schema/swagger-ui/)
* **ReDoc:** [http://127.0.0.1:8000/api/schema/redoc/](http://127.0.0.1:8000/api/schema/redoc/)

### Contrato de API para o Frontend
Na raiz do projeto está disponível o arquivo [api_contract.json](./api_contract.json) detalhando o formato exato das requisições esperadas e as respostas JSON que o backend envia para o frontend.

---

## 🧠 Integração com Machine Learning

O modelo de previsão utiliza um regressor do tipo **Gradient Boosting** treinado a partir de dados reais do UserBenchmark agregados por combinação única de hardware (CPU + GPU). O treinamento do modelo é feito via Jupyter Notebook.

Se você precisar retreinar o modelo ou atualizar os arquivos `.pkl` após mudanças no dataset (`csv_result-fps-in-video-games.csv`), basta executar o script auxiliar:
```bash
python train_model.py
```
*(Nota: baixar o dataset com link nos requirements(1).pdf).*

---

## 🧪 Como Executar os Testes Automatizados
O projeto conta com testes unitários para validar a consistência física da predição de FPS e a lógica de compatibilidade de peças e orçamento do otimizador de PC:
```bash
python manage.py test
```
