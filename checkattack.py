import os
import cv2
import argparse
import datetime
import csv
import glob
import numpy as np
import random
import csv
import argparse
import numpy
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.spatial import distance
import pandas as pd


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--infile", default="test_data.csv", help="template video file list.")
    parser.add_argument("--upscale", default=1, type=int, help="template video file list.")
    args = parser.parse_args()
    infile = args.infile
    upscale = args.upscale

    #read csv file with pandas
    dfdata = pd.read_csv(infile)
    dfdata = dfdata[~dfdata.rendition.str.contains("rotate")]
    dfdata = dfdata.sort_values(by=['source', 'dimension_x'])

    print(dfdata.shape[0])

    presource = ""
    prewidth = 0
    preheight = 0
    cosinedist = []
    l2dist = []
    for i in range(dfdata.shape[0]):
        print(i)
        if dfdata.iloc[i]['target'] == 0:
            presource = dfdata.iloc[i]['source']
            prewidth = dfdata.iloc[i]['dimension_x']
            preheight = dfdata.iloc[i]['dimension_y']

            prediff = []

            prediff.append(dfdata.iloc[i]['size_dimension_ratio'])
            prediff.append(dfdata.iloc[i]['temporal_dct-mean'])
            prediff.append(dfdata.iloc[i]['temporal_gaussian_mse-mean'])
            prediff.append(dfdata.iloc[i]['temporal_gaussian_difference-mean'])
            prediff.append(dfdata.iloc[i]['temporal_threshold_gaussian_difference-mean'])
            prediff.append(dfdata.iloc[i]['temporal_histogram_distance-mean'])

            if upscale > 0:
                prediff[1] = prediff[1] * prewidth * preheight
                prediff[2] = prediff[2] * prewidth * preheight
                prediff[3] = prediff[3] * prewidth * preheight
                prediff[5] = prediff[5] * prewidth * preheight

        else:
            if presource == dfdata.iloc[i][ 'source'] and prewidth == dfdata.iloc[i][ 'dimension_x'] \
                and preheight == dfdata.iloc[i]['dimension_y']:
                #calc distance

                valdiff = []

                valdiff.append(dfdata.iloc[i]['size_dimension_ratio'])
                valdiff.append(dfdata.iloc[i]['temporal_dct-mean'])
                valdiff.append(dfdata.iloc[i]['temporal_gaussian_mse-mean'])
                valdiff.append(dfdata.iloc[i]['temporal_gaussian_difference-mean'])
                valdiff.append(dfdata.iloc[i]['temporal_threshold_gaussian_difference-mean'])
                valdiff.append(dfdata.iloc[i]['temporal_histogram_distance-mean'])

                if upscale > 0:
                    valdiff[1] = valdiff[1] * prewidth * preheight
                    valdiff[2] = valdiff[2] * prewidth * preheight
                    valdiff[3] = valdiff[3] * prewidth * preheight
                    valdiff[5] = valdiff[5] * prewidth * preheight

                cosinedist.append(distance.cosine(numpy.array(prediff), numpy.array(valdiff)))
                l2dist.append(distance.euclidean(numpy.array(prediff), numpy.array(valdiff)))
            else:
                pass
        pass

    npcosdist = numpy.array(cosinedist)
    print("cosine dis min max mean:", numpy.min(npcosdist), numpy.max(npcosdist), numpy.mean(npcosdist))
    # ax = sns.distplot(npdist)
    # seaborn histogram ?histplot
    sns.distplot(npcosdist, hist=True, kde=False,
                 bins=int(100), color='blue',
                 hist_kws={'edgecolor': 'black'})

    plt.title('cosine distance evaluation')
    plt.xlabel('cosine distance')
    plt.ylabel('count')
    # plt.tight_layout()
    plt.show()

    npl2dist = numpy.array(l2dist)
    print("l2 dis min max mean:", numpy.min(npl2dist), numpy.max(npl2dist), numpy.mean(npl2dist))
    # ax = sns.distplot(npdist)
    # seaborn histogram ?histplot
    sns.distplot(npl2dist, hist=True, kde=False,
                 bins=int(100), color='blue',
                 hist_kws={'edgecolor': 'black'})

    plt.title('l2 distance evaluation')
    plt.xlabel('l2 distance')
    plt.ylabel('count')
    # plt.tight_layout()
    plt.show()
    #calculate distance for tamper
