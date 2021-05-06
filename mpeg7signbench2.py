import csv
import argparse
import numpy
import multiprocessing
import subprocess
import datetime
import glob
import os


profile = ['144p','240p','360p','480p','720p']
attacklist = ['black_and_white','chroma_subsampling_yuv422p','flip_horizontal','flip_vertical','low_bitrate_4',
          'low_bitrate_8','rotate_90_clockwise','rotate_90_counterclockwise','vignette', 'watermark']

def getfilepaths(infile):
    filelist = []
    if infile != None:
        with open(infile) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                filelist.append(row['outpath'])

    return filelist

def compare(path1, path2):
    result = True
    ffmpeg_command = []

    out = None
    err = None
    try:
        ffmpeg_command = ['ffmpeg', '-hide_banner', '-y', '-i', '"' + path1 + '"', '-i',
                          '"' + path2 + '"', '-filter_complex',
                          '"[0:v][1:v] signature=nb_inputs=2:detectmode=full"',
                          '-map ' + ':v', '-f null -']

        ffmpeg = subprocess.Popen(' '.join(ffmpeg_command), stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                                  shell=True)
        out, err = ffmpeg.communicate()
        status = ffmpeg.wait()
        print('FFMPEG status {}'.format(status))

        errstr = err.decode("utf-8")

        if "no matching of video" in errstr:
            result = False
        else:
            print("matching!")


    except Exception as e:
        print('The error was ', e)
        print('Executing ', ffmpeg_command)
        print('Out ', out)
        print('Error', err)

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--indir", default="/home/livepeer-verifier-renditions", help="1st csv file for evaluation.")
    parser.add_argument("--target", default="360p", help='target value for true or false')
    parser.add_argument("--ofile", default="", help="distance matrix for .")
    args = parser.parse_args()
    indir = args.indir
    target = args.target
    ofile = args.ofile
    samplemax = 100

    target = target

    outcsv = target + "_phashanal_" + datetime.datetime.now().strftime("%d%H%M") + ".csv"
    fileout = open(outcsv, 'w', newline='')
    wr = csv.writer(fileout)
    wr.writerow([target, 'attack', 'matchcount', 'no match', 'total'])

    for attack in attacklist:
        notamperpath = indir + "/" + "tamperfalse" + "/" + target + "/"
        tamperpath = indir + "/" + "tampertrue" + "/" + target + "_" + attack

        fileset = [file for file in glob.glob(tamperpath + "/*.mp4", recursive=True)]
        count = len(fileset) - 1
        if count <= 0:
            continue

        print(tamperpath, count)

        totalcount = 0
        matchcount = 0
        idcount = 0

        selcount = min(count,600)

        subindex = numpy.random.choice(count, selcount, False)

        for id in subindex:
            ftamper = fileset[id]
            fname = os.path.basename(ftamper)
            fnotamper = notamperpath + fname

            print("processing ---",target, attack, idcount)

            if os.path.exists(ftamper) and os.path.exists(fnotamper):
                print("notamper-", fnotamper)
                print("tamper-", ftamper)
                try:
                   bres = compare(ftamper,fnotamper)

                   idcount = idcount + 1
                   if bres == True:
                       matchcount = matchcount + 1

                except Exception as e:
                    pass

            if idcount >= samplemax:
                break
        #write csv file

        wr.writerow([target, attack, matchcount, idcount - matchcount, idcount])


    fileout.close()
    print('Success!')


