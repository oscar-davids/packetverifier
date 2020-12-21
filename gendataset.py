import os
import cv2
import argparse
import datetime
import csv
import glob
import numpy as np
import random

import pandas as pd

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default="testdataset", help="directory of video dataset.")
    parser.add_argument('--maxcount', type=int, default=5000, help="sample count of checking")
    args = parser.parse_args()
    testdir = args.dir
    maxcount = args.maxcount

    vprofiles = ["P720p60fps16x9", "P720p30fps16x9", "P720p25fps16x9", "P720p30fps4x3", "P576p30fps16x9","P576p25fps16x9",
                     "P360p30fps16x9", "P360p25fps16x9", "P360p30fps4x3", "P240p30fps16x9", "P240p25fps16x9", "P240p30fps4x3",
                     "P144p30fps16x9"]
    vprofilenum = len(vprofiles)
    devmodes = ["nv","sw"]

    fileset = [file for file in glob.glob(testdir + "/**/*.*", recursive=True)]
    filecount = len(fileset) - 1
    if filecount < 1:
        print('There is no video files in your selected directory!')
        exit(-1)

    binit = False
    gencount = 0

    outcsv = "testlist" + datetime.datetime.now().strftime("d%H%M") + ".csv"
    fileout = open(outcsv, 'w', newline='')
    wr = csv.writer(fileout)
    wr.writerow(['filepath', 'width', 'height', 'fps', 'bitrate', 'profile', 'devmode', 'framecount', 'indices'])
    max_posnum = 10

    while gencount < maxcount:

        ##for file in fileset:
            #fname = os.path.basename(file)

        findex = gencount % filecount
        file = fileset[findex]
        fname = os.path.basename(file)

        print(fname + ": ")

        try:
            cap = cv2.VideoCapture(file, cv2.CAP_FFMPEG)
            frelpath = file.replace(testdir + "\\", "")
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            bitrate = int(cap.get(cv2.CAP_PROP_BITRATE))
            vproid = random.choice(vprofiles)
            dmode = random.choice(devmodes)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            #generate randomize 10 indices

            indexes = np.sort(np.random.choice(frame_count, max_posnum, False))
            #exclude 0
            if indexes[0] == 0:
                indexes[0] = 1
            strindices = '"' + str(indexes[0])
            for i in range(1, max_posnum):
                strindices += ("," + str(indexes[i]))
            strindices += '"'

            #write dataset list
            wr.writerow([frelpath, width, height, fps, bitrate, vproid, dmode, frame_count, strindices])
            gencount += 1

        except Exception as e:
            print(e)
        #finally:
            #if cap is not None:
            #    cap.release()

    fileout.close()
    print('Success!')



