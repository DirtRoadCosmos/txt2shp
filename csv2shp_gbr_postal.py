import csv

def csv2shp():



def usage():
    s = 'csv2shp_gbr_postal.py [csvfile | dir]'
    return s
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print usage()
    name = sys.argv[1]
    if os.path.isdir(name):
        for filename in glob.glob(name + '/*.csv'):
            print filename
            csv2shp(filename)
    else:
        csv2shp(name)