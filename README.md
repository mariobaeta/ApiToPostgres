# 📈 Projeto ETL + Dashboard: API de Preço do Bitcoin para PostgreSQL e Visualização

Este projeto realiza um processo **ETL (Extract, Transform, Load)** de dados do preço do Bitcoin obtidos via API da Coinbase, armazenando-os em um banco de dados PostgreSQL e disponibilizando-os para visualização em um dashboard com Streamlit. O objetivo é demonstrar uma pipeline funcional de captura, persistência e visualização de dados para fins educativos e de prototipagem.

## 🔧 Tecnologias Utilizadas

- Python 3.12+
- Requests
- SQLAlchemy
- Psycopg2
- Pandas
- PostgreSQL
- Streamlit
- Power BI (planejado para integração futura)
- Docker (opcional)
- dotenv

## 📁 Estrutura do Projeto

```
├── src/
│   ├── pipeline_02.py       # Script principal ETL com extração da API, transformação e carga no banco
│   └── database.py          # Definições de modelo ORM e conexão com o PostgreSQL
├── dashboard/
│   └── app.py               # Dashboard interativo em Streamlit
├── exemplos/
│   └── exemplo_02.py        # Teste simples de extração do preço do Bitcoin
├── .env                     # Variáveis de ambiente para conexão segura ao banco
├── requirements.txt         # Dependências do projeto
└── README.md
```

## ⚙️ Como Executar o Projeto

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo
```

### 2. Configure o arquivo `.env`

Crie um arquivo `.env` na raiz do projeto com os seguintes dados:

```ini
POSTGRES_USER=seu_usuario
POSTGRES_PASSWORD=sua_senha
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=bitcoin_db
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute o ETL

```bash
python src/pipeline_02.py
```

### 5. Execute o Dashboard

```bash
streamlit run dashboard/app.py
```

## 🧠 Lógica do Projeto

- **Extração**: Pega o valor atual do Bitcoin na API da Coinbase.
- **Transformação**: Estrutura os dados com timestamp, moeda base e valor.
- **Carga**: Insere os dados no banco PostgreSQL com SQLAlchemy.
- **Visualização**: Streamlit lê os dados do banco e exibe gráfico, tabela e métricas.

## 🖼️ Exemplo do Dashboard

- Gráfico de evolução do preço
- Tabela com histórico
- Métricas de preço atual, mínimo e máximo

## 📌 Observações

- A frequência de coleta padrão é de **5 minutos** (`time.sleep(300)`) para manter dados relevantes e com bom intervalo para análise, evitando sobrecarga no banco.
- Ideal para uso como exemplo em projetos de **Data Engineering** ou **Business Intelligence**.

---

**Autor:** mariobaeta  
**Licença:** MIT
