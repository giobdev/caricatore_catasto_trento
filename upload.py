import os
import psycopg2
import geopandas as gpd
from pathlib import Path

from config import mydb

# ----------------------------------------------
# CARICAMENTO MASSIVO DEGLI EDIFICI SUL DATABASE
# ----------------------------------------------

polyconv_dir = Path("/example_files/polyconv")
boundaryconv_dir = Path("/example_files/boundaryconv")

ids = {}

def check_files():
	file_caricati = []
	with open("file_caricati.txt", "r") as f:
		for line in f:
			file_caricati.append(line.split()[-1])
		return file_caricati
	
file_uploaded = check_files()

def letture_edifici():
	count = len(file_uploaded)
	for file in os.listdir(polyconv_dir):

		if file in file_uploaded:
			print("file già caricato", file)
			continue
		print("iniziato caricamento file: ", file)

		geodf = gpd.read_file(os.path.join(os.getcwd(), "/example_files/polyconv", file))
		geodf = geodf.to_crs(epsg=4326)        
		edifici = []

		for item in list(geodf.iloc):
			if item["PT_FABB"] == "S" :
				edifici.append((item["geometry"].centroid.wkt, item["geometry"].wkt, str(ids[item["PT_CCAT"]]).zfill(6)))

		args_str = ','.join(mycursor.mogrify("(%s,%s,%s)", edificio).decode("utf-8") for edificio in edifici)

		if len(args_str) == 0:
			f.write("caricato file con 0 fabbricati: " + file + "\n")
			print("terminato", count)
			continue
		mycursor.execute("insert into edificio (posizione, perimetro, codice_istat) values " + args_str)

		try:
			mydb.commit()
		except psycopg2.DatabaseError as e:
			print(f"Error committing to the database: {e}")
			f.write("crashato file: " + file + "\n")
			mydb.rollback()
			return
		
		f.write("caricato file: " + file + "\n")
		count += 1

		print("terminato", count)

for file in os.listdir(boundaryconv_dir):
	geodf = gpd.read_file(os.path.join(os.getcwd(), "/example_files/boundaryconv", file))
	ids[geodf.iloc[0]["BD_CCAT"]] = geodf.iloc[0]["BD_ISTAT"]

mycursor = mydb.cursor()

f = open("file_caricati.txt", "a+")
letture_edifici()
f.close()