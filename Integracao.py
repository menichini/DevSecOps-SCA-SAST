import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import psycopg2

# Autenticação e acesso ao Google Sheets
print("Autenticando e acessando o Google Sheets...")
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("gcloud.json", scope)
client = gspread.authorize(creds)
print("Autenticação concluída com sucesso.")

# Abrir a planilha e a aba correta
spreadsheet = client.open("Todos_projetos_COE")
sheet = spreadsheet.sheet1
print("Planilha 'Todos_projetos_COE' acessada com sucesso.")

# Extrair todos os dados da planilha
print("Extraindo dados da planilha...")
data = sheet.get_all_records()
print("Dados extraídos com sucesso.")

# Transformar os dados em um DataFrame do pandas
print("Transformando os dados em um DataFrame do pandas...")
df = pd.DataFrame(data)
print("Dados transformados em DataFrame com sucesso.")


print("Renomeando colunas...")
df.rename(columns={
    "Criado": "DATACRIACAO",
    "Data limite": "DATALIMITE",
    "Chave": "CHAVE",
    "Tipo de item": "TIPOITEM",
    "Resumo": "RESUMO",
    "Responsável": "RESPONSAVEL",
    "Relator": "RELATOR",
    "Prioridade": "PRIORIDADE",
    "Status": "STATUS",
    "Atualizado(a)": "DATAATUALIZACAO",
    "Σ de Tempo Gasto": "TEMPOGASTO",
    "Itens associados": "ITEMASSOCIADO",
    "Time Responsável": "TIMERESPONSAVEL",
    "Sprint": "SPRINT",
    "parent": "EPIC"
    # Adicione outros mapeamentos de colunas conforme necessário
}, inplace=True)
print("Colunas renomeadas com sucesso.")


print("Convertendo campos de data...")
def parse_date(date_str):
    for fmt in ("%d/%m/%Y %H:%M:%S", "%d/%m/%Y"):
        try:
            return pd.to_datetime(date_str, format=fmt, errors='coerce')
        except ValueError:
            pass
    return None  # Retornar None se não corresponder a nenhum formato

df['DATACRIACAO'] = df['DATACRIACAO'].apply(parse_date)
df['DATALIMITE'] = df['DATALIMITE'].apply(parse_date)

# Substituir NaT por None para compatibilidade com PostgreSQL
df['DATACRIACAO'] = df['DATACRIACAO'].where(pd.notnull(df['DATACRIACAO']), None)
df['DATALIMITE'] = df['DATALIMITE'].where(pd.notnull(df['DATALIMITE']), None)
print("Campos de data convertidos com sucesso.")

print("Configurando a conexão com o PostgreSQL...")
conn = psycopg2.connect(
    dbname="BDCOE",
    user="sheets",
    password="#fR@mework",
    host="",
    port="5432"
)
cur = conn.cursor()
print("Conexão com o PostgreSQL configurada com sucesso.")


print("Criando a tabela 'dados' no PostgreSQL, se não existir...")
cur.execute("""
    CREATE TABLE IF NOT EXISTS dados (
        CHAVE TEXT,
        TIPOITEM TEXT,
        RESUMO TEXT,
        RESPONSAVEL TEXT,
        RELATOR TEXT,
        PRIORIDADE TEXT,
        STATUS TEXT,
        DATACRIACAO TIMESTAMP,
        DATAATUALIZACAO TEXT,
        DATALIMITE TIMESTAMP,
        TEMPOGASTO TEXT,
        ITEMASSOCIADO TEXT,
        TIMERESPONSAVEL TEXT,
        SPRINT TEXT,
        EPIC TEXT
    )
""")
conn.commit()
print("Tabela 'dados' criada/verificada com sucesso.")

# Inserir os dados no PostgreSQL
print("Inserindo dados no PostgreSQL...")
for index, row in df.iterrows():
    cur.execute("""
        INSERT INTO dados (CHAVE, TIPOITEM, RESUMO, RESPONSAVEL, RELATOR, PRIORIDADE, STATUS, DATACRIACAO, DATAATUALIZACAO, DATALIMITE, TEMPOGASTO, ITEMASSOCIADO, TIMERESPONSAVEL, SPRINT, EPIC)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        row['CHAVE'], row['TIPOITEM'], row['RESUMO'], row['RESPONSAVEL'], row['RELATOR'], row['PRIORIDADE'], row['STATUS'],
        row['DATACRIACAO'] if pd.notnull(row['DATACRIACAO']) else None,
        row.get('DATAATUALIZACAO', None),
        row['DATALIMITE'] if pd.notnull(row['DATALIMITE']) else None,
        row.get('TEMPOGASTO', None),
        row.get('ITEMASSOCIADO', None),
        row.get('TIMERESPONSAVEL', None),
        row.get('SPRINT', None),
        row.get('EPIC', None)
    ))
print(f"Inserção de {index + 1} linhas concluída com sucesso.")

conn.commit()
cur.close()
conn.close()
print("Conexão com o PostgreSQL fechada com sucesso. Processo concluído.")