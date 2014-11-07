# python txt2shp.py C:\Data\Postal\gbr\g28\gbrg28_oscpwl_sm.txt
import csv
import sys
import os
from shapely.geometry import Point, mapping
from fiona import collection

def createBbox(x1, y1, x2, y2):
    print x1, y1, x2, y2
    
def createPoints(path, northwestx, northwesty, southeastx, southeasty):
    bbox = createBbox(northwestx, northwesty, southeastx, southeasty)
    
    schema = { 'geometry': 'Point', 'properties': {'postcode': 'str'} }
    with collection('points.shp', 'w', 'ESRI Shapefile', schema) as output:
        with open(path, 'rb') as f:
            reader = csv.DictReader(f, delimiter = '|')
            for row in reader:
                x = row['X-coord']
                y = row['Y-coord']
                if x and y:
                    point = Point(float(x), float(y))
                    output.write({
                        'properties': {
                            'postcode': row['Main+Sub postal code']
                        },
                        'geometry': mapping(point)
                    })

def usage():
    s = 'txt2shp.py [txtfile | dir] northwestx northwesty southeastx southeasty'
    return s
    
if __name__ == '__main__':
    if len(sys.argv) == 2:
        name = sys.argv[1]
        northwestx = 0
        northwesty = 0
        southeastx = 0
        southeasty = 0
    elif len(sys.argv) == 6:
        name = sys.argv[1]
        northwestx = sys.argv[2]
        northwesty = sys.argv[3]
        southeastx = sys.argv[4]
        southeasty = sys.argv[5]
    else:
        print usage()
    name = sys.argv[1]
    if os.path.isdir(name):
        print 'opening dir:', name
        for filename in glob.glob(name + '/*.txt'):
            print filename
            createPoints(name, northwestx, northwesty, southeastx, southeasty)
    else:
        print 'opening file:', name
        createPoints(name, northwestx, northwesty, southeastx, southeasty)