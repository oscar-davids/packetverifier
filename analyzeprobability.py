from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import argparse
import random
import seaborn as sns

def alalyseprob_nmk():
    lxlist = []
    lylist = []

    for i in range(5, 100):
        N = i # total number of the T
        M = int(N / 2 + 1) # total number of honest T
        #M = i # total number of honest T
        #M = N * 0.9 # total number of honest T
        k=3
        # scipy 
        po=stats.hypergeom(N,M,k)
        x=np.arange(k+1)
        px = 0.0
        for j in range( int(k/2), k+1):
            px += po.pmf(j)
    

        lxlist.append(i)
        lylist.append(px)

    # figure
    fig = plt.figure()
    ax = plt.gca()
    line1 = ax.stem(lxlist,lylist,basefmt='k',label='K = 3, M = N / 2 + 1, N: increase');
    ax.set_xlabel('# of total nodes');
    ax.set_ylabel('probability (honest nodes >= K/2)');
    ax.set_title('hypergeometry probability');

    lxlist.clear()
    lylist.clear()

    for i in range(5, 100):
        N = 100 # total number of the T
        #M = int(N / 2 + 1) # total number of honest T
        M = i # total number of honest T
        #M = N * 0.9 # total number of honest T
        k=3
        # scipy 
        po=stats.hypergeom(N,M,k)
        x=np.arange(k+1)
        px = 0.0
        for j in range( int(k/2), k+1):
            px += po.pmf(j)
    

        lxlist.append(i)
        lylist.append(px)

    ax2=plt.twinx()

    #line1 = ax2.stem(lxlist,lylist,basefmt='k', markerfmt='D',label='probability of honest nodes');
    line2 = ax2.plot(lxlist,lylist,'r',label='K = 3, M increase, N=100')
    #ax2.set_ylabel('cumulative probability',color='r')
    #ax.set_xlabel('# of total nodes');
    #ax.set_ylabel('probability honest >= K/2');
    #ax.set_title('hypergeometry probability K = 3, M = i, N=100');

    ax.legend(loc=(0.7,0.6));
    ax2.legend(loc=(0.7,0.5))

    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=int, default=0, help="select analyse mode")    
    args = parser.parse_args()
    mode = args.mode
    
    #indexes = np.sort(np.random.choice(lptmaxstake, N, False))
    N = 5
    #lptmaxstake = int(2147483647 / 4) - 1
    #lptmaxstake = 65536
    lptmaxstake = 50000

    selstake = []

    for x in range(0, 1000000): 
        liststake = []       
        for i in range(0,N):
            liststake.append(random.randint(1, lptmaxstake))

        #print(liststake)
    
        totalStake = 0
        for stake in liststake:
            totalStake += stake        

        r = 0
        # Generate a random stake weight between 1 and totalStake
        #random.seed()
        if totalStake > 0:
            r = 1 + random.randint(1, totalStake)        

        for stake in liststake:
            r -= stake
            if r <= 0:
                selstake.append(stake)
                #selstake.append(stake / totalStake)
                #selstake.append(totalStake)
                break
        

    npdist = np.array(selstake)

    # ax = sns.distplot(npdist)
    # seaborn histogram ?histplot
    sns.distplot(npdist, hist=True, kde=False,
                    bins=int(10), color='blue',
                    hist_kws={'edgecolor': 'black'})

    # Add labels
    plt.title('Probability')
    plt.xlabel('Stake')
    plt.ylabel('Selected Count')
    #plt.tight_layout()
    plt.show()
