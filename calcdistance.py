import csv
import argparse
import numpy
from scipy.spatial import distance
import seaborn as sns
import matplotlib.pyplot as plt
import datetime

vprofiles = ["P720p60fps16x9", "P720p30fps16x9", "P720p25fps16x9", "P720p30fps4x3", "P576p30fps16x9", "P576p25fps16x9",
             "P360p30fps16x9", "P360p25fps16x9", "P360p30fps4x3", "P240p30fps16x9", "P240p25fps16x9", "P240p30fps4x3",
             "P144p30fps16x9"]

resolutions =  [921600, 921600, 921600, 691200, 589824, 589824, 230400, 230400, 172800, 102240, 102240, 76800, 36864]



def getfieldcount(fname):
    with open(fname) as csv_file:
        lval = 0
        csv_reader = csv.reader(csv_file, delimiter=',')
        flag = True
        for row in csv_reader:
            lval = len(row)
            break
    return lval

def getvallist(fname):
    with open(fname) as csv_file:
        lval = []
        csv_reader = csv.reader(csv_file, delimiter=',')
        flag = True
        for row in csv_reader:
            if flag == True:
                flag = False
                continue
            lval.append(row)
    return lval

def covertdigitlist(slist, index):
    listdisit = []
    for row in slist:
        positions = row[index].replace('"',"")
        lpos = positions.split(',')
        disitpos = [float(i) for i in lpos]
        listdisit.append(disitpos)

    return listdisit

def write_distfile(incsv1, ofile, npdist, target):

    fileout = open(ofile, 'w', newline='')
    wr = csv.writer(fileout)
    wr.writerow(['filepath', 'width', 'height', 'fps', 'bitrate', 'profile', 'devmode', 'framecount',
                 'indices','rendpath', 'position', 'length', 'features', 'target', 'distance', 'target'])

    brheader = False
    index = 0
    with open(incsv1) as csvfile:
        rd = csv.reader(csvfile, delimiter=',')
        for row in rd:
            #print(row)
            wrow = []
            if brheader == False:
                brheader = True
            else:
                wrow = row
                wrow.append(npdist[index])
                wrow.append(target)
                wr.writerow(wrow)
                index = index + 1

    fileout.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--inf1", default="in1.csv", help="1st csv file for evaluation.")
    parser.add_argument("--inf2", default="in2.csv", help="2nd csv file for evaluation.")
    parser.add_argument("--target", type=int, default=0, help='target value for true or false')
    parser.add_argument("--ofile", default="", help="distance matrix for .")
    parser.add_argument("--type",type=int, default=0, help="parameter that distinguish seek position from diff feature")
    args = parser.parse_args()
    incsv1 = args.inf1
    incsv2 = args.inf2
    target = args.target
    ofile = args.ofile
    outtype = args.type
    if target is not None:
        if ofile == "":
            ofile = "distance_" + datetime.datetime.now().strftime("d%H%M") + ".csv"
    else:
        ofile = ""

    #check path
    fieldnum = getfieldcount(incsv1)
    listvall = getvallist(incsv1)
    listval2 = getvallist(incsv2)

    assert(len(listvall) == len(listval2))

    if outtype == 0: #position type
        posidx = fieldnum - 2
        listpos1 = numpy.array(covertdigitlist(listvall,posidx))
        listlen1 = numpy.array(covertdigitlist(listvall,posidx+1))
        listpos2 = numpy.array(covertdigitlist(listval2,posidx))
        listlen2 = numpy.array(covertdigitlist(listval2,posidx+1))

        diffpos = listpos1 - listpos2
        difflen = listlen1 - listlen2

        #calc cosine distance
        cosinedist = []
        for i in range(0, len(listpos1)):
            cosinedist.append(distance.cosine(listpos1[i],listpos2[i]))

        npdist = numpy.array(cosinedist)

        # ax = sns.distplot(npdist)
        # seaborn histogram ?histplot
        sns.distplot(npdist, hist=True, kde=False,
                     bins=int(1000), color='blue',
                     hist_kws={'edgecolor': 'black'})

        # Add labels
        plt.title('Acceptable Distance')
        plt.xlabel('cosine distance')
        plt.ylabel('count')
        #plt.tight_layout()
        plt.show()

        print("pos min max mean:", numpy.min(diffpos),numpy.max(diffpos),numpy.mean(diffpos))
        print("len min max mean:", numpy.min(difflen),numpy.max(difflen),numpy.mean(difflen))


        #write distance file each video file
        if len(ofile) > 0:
            fileout = open(ofile, 'w', newline='')
            wr = csv.writer(fileout)
            wr.writerow(['filepath', 'width', 'height', 'fps', 'bitrate', 'profile', 'devmode', 'framecount',
                         'indices', 'position', 'length', 'cosdis', 'target'])

            brheader = False
            index = 0
            with open(incsv1) as csvfile:
                rd = csv.reader(csvfile, delimiter=',')
                for row in rd:
                    print(row)
                    wrow = []
                    if brheader == False:
                        brheader = True
                    else:
                        wrow = row
                        wrow.append(npdist[index])
                        wrow.append(target)
                        wr.writerow(wrow)
                        index = index + 1

            fileout.close()
    else:
        prefix = ""

        posidx = fieldnum - 2
        #upscale
        diffs1 = numpy.array(covertdigitlist(listvall, posidx))
        diffs2 = numpy.array(covertdigitlist(listval2, posidx))

        if target == 1:
            diffs2[:,0] =  diffs1[:,0]
            prefix = "Negative "
        else:
            prefix = "Positive "

        # calc cosine distance
        cosinedist = []
        for i in range(0, len(diffs1)):
            cosinedist.append(distance.cosine(diffs1[i], diffs2[i]))

        npcosdist = numpy.array(cosinedist)
        print("cosine dis min max mean:", numpy.min(npcosdist), numpy.max(npcosdist), numpy.mean(npcosdist))
        # ax = sns.distplot(npdist)
        # seaborn histogram ?histplot
        sns.distplot(npcosdist, hist=True, kde=False,
                     bins=int(1000), color='blue',
                     hist_kws={'edgecolor': 'black'})

        plt.title(prefix + 'cosine distance evaluation')
        plt.xlabel('cosine distance')
        plt.ylabel('count')
        # plt.tight_layout()
        plt.show()

        #write csv file
        ofile = "distance_cos_" + prefix + datetime.datetime.now().strftime("%d%H%M") + ".csv"
        write_distfile(incsv1,ofile,npcosdist,target)

        l2dist = []
        for i in range(0, len(diffs1)):
            l2dist.append(distance.euclidean(diffs1[i], diffs2[i]))

        npl2dist = numpy.array(l2dist)

        # ax = sns.distplot(npdist)
        # seaborn histogram ?histplot
        print("L2 dis min max mean:", numpy.min(npl2dist), numpy.max(npl2dist), numpy.mean(npl2dist))
        sns.distplot(npl2dist, hist=True, kde=False,
                     bins=int(1000), color='blue',
                     hist_kws={'edgecolor': 'black'})

        ofile = "distance_l2_" + prefix + datetime.datetime.now().strftime("%d%H%M") + ".csv"
        write_distfile(incsv1, ofile, npl2dist, target)

        plt.title(prefix + 'L2 distance evaluation')
        plt.xlabel('L2 distance')
        plt.ylabel('count')
        # plt.tight_layout()
        plt.show()
        #normal

        pass

    print('Success!')