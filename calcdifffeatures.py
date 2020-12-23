import os
import argparse
import datetime
import csv
from verifier import Verifier

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--srcdir", default="", help="source video file directory")
    parser.add_argument("--renddir", default="", help="rendition video file directory")
    parser.add_argument("--infile", default="in.csv", help="csv file to calculate diff features.")
    args = parser.parse_args()

    infile = args.infile
    srcdir = args.srcdir
    renddir = args.renddir

    outcsv = "difffeature" + datetime.datetime.now().strftime("%m%d%H") + ".csv"
    fileout = open(outcsv, 'w', newline='')
    wr = csv.writer(fileout)
    wr.writerow(['filepath', 'width', 'height', 'fps', 'bitrate',
                 'profile', 'devmode', 'framecount', 'indices', 'outpath', 'position', 'length', 'features'])
    max_samples = 10
    debug = False

    verifier = Verifier(10, 'verification-metamodel-2020-07-06.tar.xz', False, False, debug)

    brheader = False
    with open(infile) as csvfile:
        rd = csv.reader(csvfile, delimiter=',')
        for row in rd:
            print(row)
            wrow = []
            if brheader == False:
                brheader = True
            else:
                srcfile = srcdir + "/" + row[0]
                rendfile = renddir + "/" + row[9]

                file_stats = os.stat(srcfile)

                difffeatures = verifier.getfeature(srcfile, [{'uri': rendfile}])

                wrow = row
                wrow.append(difffeatures)
                wr.writerow(wrow)

    fileout.close()
    print('Success calculation diff features!')