'''
Heavily influenced by http://gis.stackexchange.com/questions/41465/generating-geojson-with-python
Couldn't get that version to work, and Fiona wouldn't install properly on OS X 10.9.2
'''

import json
import argparse
import ogr

parser = argparse.ArgumentParser(
    description="Convert many shapefiles to a single GeoJSON",
    epilog="Example usage: python dalhart.py -i file.shp file2.shp file3.shp -o output.json")

parser.add_argument("-i", "--input", dest="input",
    type=str, required=True, nargs="*",
    help="The input files")

parser.add_argument("-o", "--output", dest="output",
    type=str, required=True,
    help="The output file")

arguments = parser.parse_args()

# Define driver for reading shapefiles
driver = ogr.GetDriverByName("ESRI Shapefile")

# Output
outputLayer = {
    "type": "FeatureCollection",
    "features": []
}

# Function for converting a shapefile to a Python dictionary
def convert(shapefile):
    data = driver.Open(shapefile, 0)
    layer = data.GetLayer()
    layerCount = layer.GetFeatureCount()

    i = 0
    while i < layerCount:
        feature = layer.GetFeature(i)
        outputLayer["features"].append(feature.ExportToJson(as_object=True))
        i = i + 1

    print "Done with " + shapefile

# Convert each input file
for file in arguments.input:
    if file[-4:] == ".shp":
        convert(file)

# When done, write it out to a file
with open(arguments.output, "wb") as output:
    json.dump(outputLayer, output)
