import psycopg2

# Configurações do PostgreSQL
host = ""
dbname = "BDCOE"
user = "sheets"
password = "#fR@mework"
port = "5432"

# Conectando ao banco de dados
try:
    conn = psycopg2.connect(
        host=host,
        dbname=dbname,
        user=user,
        password=password,
        port=port
    )
    print("Conexão bem-sucedida")
except Exception as e:
    print(f"Erro ao conectar: {e}")

# Fechando a conexão
#conn.close()