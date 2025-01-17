import os
import geopandas as gpd
from pathlib import Path

# ----------------------------
# CONVERSIONE DA SHP A GEOJSON
# ----------------------------

boundary_input_dir = Path("/example_files/boundary")
boundary_output_dir = Path("/example_files/boundaryconv")
poly_input_dir = Path("/example_files/poly")
poly_output_dir = Path("/example_files/polyconv")

boundary_output_dir.mkdir(exist_ok=True)
poly_output_dir.mkdir(exist_ok=True)

def boundary_conversion():
	for file in os.listdir(boundary_input_dir):
		myshpfile = gpd.read_file(os.path.join(os.getcwd(),"example_files/boundary_complete", file))
		myshpfile.to_file("/example_files/boundaryconv/" + file[:-4] + '.geojson', driver='GeoJSON')

def poly_conversion():
	for file in os.listdir(poly_input_dir):
		myshpfile = gpd.read_file(os.path.join(os.getcwd(), "example_files/poly_complete", file))
		myshpfile.to_file("/example_files/polyconv/" + file[:-4] + '.geojson', driver='GeoJSON')

if __name__ == "__main__":
	...
	#boundary_conversion()
	#poly_conversion()