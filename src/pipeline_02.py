import requests
import time
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database import BitcoinPreco, Base
import os
from dotenv import load_dotenv

# Importar Base e BitcoinPreco do database.py
from database import Base, BitcoinPreco

INTERVALO = int(os.getenv("SLEEP_INTERVAL", 60))  # Padrão: 5 minutos


# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

print("POSTGRES_USER:", os.getenv("POSTGRES_USER"))  # Teste de leitura


# Leia as variáveis de ambiente
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

# Monta a URL de conexão ao banco PostgreSQL (sem SSL)
DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Criar a engine com ajustes na pool de conexões
engine = create_engine(
    DATABASE_URL,
    pool_size=10,        # Tamanho da pool de conexões
    max_overflow=20,     # Quantidade máxima de conexões extras
    pool_timeout=30,     # Tempo limite para obter uma conexão
)
# Crie a fábrica de sessões (Session)
Session = sessionmaker(bind=engine)

# Função para criar a tabela no banco de dados
def create_table():
    Base.metadata.create_all(engine)
    # Crie a tabela no banco de dados 
    print("Tabela criada com sucesso!")


def extract():
    """
    Função para extrair dados da API do Coinbase
    """
    url = 'https://api.coinbase.com/v2/prices/spot'
    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()
    else:
        raise Exception(f"Erro na API: {response.status_code} - {response.text}")
    return dados


def transform(dados):
    """
    Função para transformar os dados extraídos
    """
    valor = dados['data']['amount']
    criptomoeda = dados['data']['base']
    moeda = dados['data']['currency']
    timestamp = datetime.now()
    
    return {
        'valor': valor,
        'criptomoeda': criptomoeda,
        'moeda': moeda,
        'timestamp': timestamp

    }

def load(dados):
    """
    Função para carregar os dados transformados no banco de dados
    """
    # Crie a tabela no banco de dados
    create_table()

      # Crie a sessão com contexto
    with Session() as session:
        try:
            # Crie um novo registro
            novo_registro = BitcoinPreco(
                valor=dados['valor'],
                criptomoeda=dados['criptomoeda'],
                moeda=dados['moeda'],
                timestamp=dados['timestamp']  # Timestamp transformado
            )
            
            # Adicione o registro à sessão
            session.add(novo_registro)
            
            # Salve as alterações no banco de dados
            session.commit()
            print(f"[{dados['timestamp']}] Dados carregados com sucesso no banco de dados!")
        
        except Exception as e:
            session.rollback()
            print(f"Erro ao carregar dados: {e}")

# Substituído o loop infinito while True por execução única.
# Motivo: GitHub Actions não suporta jobs que rodam continuamente ou indefinidamente.
# Agora, o pipeline roda uma vez a cada minuto, conforme agendado no workflow (.yml).
# A cada execução:
# 1. Cria a tabela se necessário,
# 2. Extrai os dados da API,
# 3. Transforma e carrega no banco,
# 4. Finaliza imediatamente.
#
# O bloco abaixo foi substituído:

"""
if __name__ == "__main__":
    # Crie a tabela no banco de dados
    create_table()
    print("Iniciando o pipeline com atualização a cada 15 segundos...(CTRL+C para parar)")
    # Extrair os dados da API
    while True:
        try:
            dados_json = extract()
            if dados_json:
                # Transformar os dados
                dados_transformados = transform(dados_json)
                print("Dados transformados:", dados_transformados)
                # Carregar os dados transformados no banco de dados
                load(dados_transformados)
                # Aguardar 15 segundos antes de fazer a próxima requisição
                time.sleep(INTERVALO)  
        except KeyboardInterrupt:
            print("\nPipeline interrompido pelo usuário.")
            break
        except Exception as e:
            print(f"Erro: {e}")
            # Extrair os dados da API
            dados_json = extract()                
            # Transformar os dados
            time.sleep(INTERVALO)
"""

# Este bloco __main__ foi adaptado para funcionar em conjunto com o GitHub Actions.
# Em vez de rodar continuamente (loop infinito), ele executa uma única vez por chamada.
# Isso se alinha ao agendamento definido no workflow (cron a cada 1 minuto).
# A sequência é:
# 1. Cria a tabela (se não existir),
# 2. Extrai os dados da API,
# 3. Transforma os dados,
# 4. Carrega no banco de dados,
# 5. Encerra a execução (sem time.sleep).

if __name__ == "__main__":
    try:
        # Cria a tabela (se ainda não existir)
        create_table()
        
        # Extrai os dados da API
        dados_json = extract()

        if dados_json:
            # Transforma os dados
            dados_transformados = transform(dados_json)
            print("Dados transformados:", dados_transformados)

            # Carrega no banco de dados
            load(dados_transformados)

    except Exception as e:
        print(f"Erro no pipeline: {e}")
