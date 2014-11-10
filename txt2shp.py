# python txt2shp.py C:\Data\Postal\gbr\g28\gbrg28_oscpwl_sm.txt
import csv
import sys
import os
from shapely.geometry import Point, Polygon, mapping
from fiona import collection

class BBox(Polygon):
    def __init__(self, minx, miny, maxx, maxy):
        minx = float(minx)
        miny = float(miny)
        maxx = float(maxx)
        maxy = float(maxy)
        Polygon.__init__(self, [(minx, miny), (minx, maxy), (maxx, maxy), (maxx, miny)])


def createPoints():
    schema = { 'geometry': 'Point', 'properties': {'postcode': 'str'} }
    with collection('points.shp', 'w', 'ESRI Shapefile', schema) as output:
        with open(name, 'rb') as f:
            reader = csv.DictReader(f, delimiter = '|')
            for row in reader:
                x = row['X-coord']
                y = row['Y-coord']
                if x and y:
                    point = Point(float(x), float(y))
                    if not 'thisBBox' in globals() or (thisBBox and point.within(thisBBox)):
                        print 'added', point
                        output.write({
                            'properties': {
                                'postcode': row['Main+Sub postal code']
                            },
                            'geometry': mapping(point)
                        })                    
                    else:
                        print 'not added', point
        # //find duplicate rule ids
        # var unique_values = {};
        # var duplicate_rule_ids = [];
        # $.each(ruleList_raw, function(index, rule) { 
                # ruleString = rule.id;
                # if ( ! unique_values[ruleString] ) {
                    # unique_values[ruleString] = true;
                    # ruleList_unique.push(rule);
                # } else {
                    # duplicate_rule_ids.push(ruleString);
                # }
            # });
        
        # //examine the duplicates
        # $.each(duplicate_rule_ids, function(index, value) {
            # var result = $.grep(ruleList_raw, function(e){ return e.id === value; });
            # console.log(result);
        # });


def usage():
    s = 'txt2shp.py [txtfile | dir] minx miny maxx maxy'
    return s
    
if __name__ == '__main__':
    if len(sys.argv) == 2:
        name = sys.argv[1]
    elif len(sys.argv) == 6:
        thisBBox = BBox(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        name = sys.argv[1]
    else:
        print usage()
        sys.exit(0)
    
    if os.path.isdir(name):
        print 'opening dir:', name
        for filename in glob.glob(name + '/*.txt'):
            print '  file:', filename
            createPoints()
    else:
        print 'opening file:', name
        createPoints()