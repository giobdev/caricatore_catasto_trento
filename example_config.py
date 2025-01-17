import psycopg2

# ---------------------------
# CONNESSIONE AL DB [ESEMPIO]
# ---------------------------

mydb = psycopg2.connect(
	host="xxx.xxx.xxx.xxx",
	user="[user]",
	password="[password]",
	database="[nome_db]",
	port="xxxxx"
)