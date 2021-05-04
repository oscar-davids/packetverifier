import csv
import argparse
import numpy
import multiprocessing
import subprocess

def getfilepaths(infile):
    filelist = []
    if infile != None:
        with open(infile) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                filelist.append(row['outpath'])

    return filelist

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--inf1", default="in1.csv", help="1st csv file for evaluation.")
    parser.add_argument("--inf2", default="in2.csv", help="2nd csv file for evaluation.")
    parser.add_argument("--target", type=int, default=None, help='target value for true or false')
    parser.add_argument("--ofile", default="", help="distance matrix for .")
    args = parser.parse_args()
    incsv1 = args.inf1
    incsv2 = args.inf2

    lpath1 = getfilepaths(incsv1)
    lpath2 = getfilepaths(incsv2)
    target = args.target
    ofile = args.ofile
    assert (len(lpath1) == len(lpath2))
    matchnum = 0
    errlist = []

    ffmpeg_command = []
    for i in range(0, len(lpath1)):
        out = None
        err = None
        try:
            ffmpeg_command = ['ffmpeg', '-hide_banner', '-y', '-i', '"' + lpath1[i] + '"', '-i',
                       '"' + lpath2[i]  + '"',
                       '-filter_complex',
                       '"[0:v][1:v] signature=nb_inputs=2:detectmode=full"',
                       '-map ' + ':v', '-f null -'
                       ]

            ffmpeg = subprocess.Popen(' '.join(ffmpeg_command), stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
            out, err = ffmpeg.communicate()
            status = ffmpeg.wait()
            print('{} -- FFMPEG status {}'.format(i, status))

            errstr = err.decode("utf-8")

            if "matching of video" in errstr:
                matchnum = matchnum  + 1
            else:
                errlist.append(lpath1[i])


        except Exception as e:
            print('Error processing ', i)
            print('The error was ', e)
            print('Executing ', ffmpeg_command)
            print('Out ', out)
            print('Error', err)

    print('match {} / all {}'.format(matchnum, len(lpath1)))