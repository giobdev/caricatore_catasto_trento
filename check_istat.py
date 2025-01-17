import os
import geopandas as gpd
from pathlib import Path
from config import mydb

# -------------------------------------------------------
# VERIFICA CHE I CODICI ISTAT SIANO PRESENTI NEL DATABASE
# -------------------------------------------------------

mycursor = mydb.cursor()

input_dir = Path("/boundaryconv")

mycursor.execute("SELECT codice_istat FROM public.istat")
istat_db = set(row[0] for row in mycursor.fetchall())
istat_geo= set()

for file in os.listdir(input_dir):
	geodf = gpd.read_file(input_dir / file)
	istat_geo.add(str(geodf.iloc[0]["BD_ISTAT"]).zfill(6))
	
delta= istat_geo.difference(istat_db)
print(delta)
