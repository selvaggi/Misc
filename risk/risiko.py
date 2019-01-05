import math
import random
import matplotlib.pyplot as plt
import numpy as np
from numpy import array
from scipy import stats
from matplotlib.ticker import FuncFormatter, MaxNLocator
from matplotlib.colors import BoundaryNorm
import multiprocessing as mp


#random.seed(40)

#_______________________________________
def frequency(a, x):
    count = 0
    for i in a:
        if i == x: count += 1
    return float(count)/len(a)

#_______________________________________
def frequencyGtr(a, x):
    count = 0
    for i in a:
        if i >= x: count += 1
    return float(count)/len(a)

#_______________________________________
def roll_dice():
    return random.randint(1, 6)

#_______________________________________
def roll(n):
    outs = []
    for i in range(n):
        outs.append(roll_dice())
    # sort descending
    outs.sort(reverse=True)
    return outs

# case I - equal dice numbering
def losses(attack, defence):
    n_dice = len(attack)
    n_lost_a = 0
    n_lost_d = 0
    for i in range (n_dice):
        if attack[i] > defence[i]:
            n_lost_d += 1
        else:
            n_lost_a += 1
    return (n_lost_a, n_lost_d)


# more general
#print '---- testing ----'
def gen_losses(attack, defence, opt_gen=False, opt_mar=False):
    n_dice = len(attack)
    n_lost_a = 0
    n_lost_d = 0

    opt_alive = True

    #print 'attack', attack
    #print 'defence', defence
    #print 'gen,mar', opt_gen, opt_mar
    #print 'alive', opt_alive

    #print len(defence)
    for i in range(n_dice):
        #print i
        if i < len(defence):
            #print i, attack[i], defence[i]

            att = attack[i]
            dif = defence[i]

            if opt_gen and i==0:
                att += 1
                if att <= dif:
                    #print 'here'
                    opt_alive = False
            if opt_mar and i==0:
                dif += 1
                if att > dif:
                    opt_alive = False

            #print 'att, diff', att, dif
            if att > dif:
                n_lost_d += 1
            else:
                n_lost_a += 1
    return (n_lost_a, n_lost_d), opt_alive

'''attack = roll(3)
defence = roll(2)

print attack
print defence
print gen_losses(attack, defence)
'''

#______________ compute probabilites _____________
def compute_sequence(n, na, nd, opt_gen, opt_mar):

    dl = []

    # simulate fight
    for i in range(n):
        attack = roll(na)
        defence = roll(nd)
        dl.append(gen_losses(attack, defence, opt_gen, opt_mar)[1])

    array_dl = np.array(dl)
    print stats.describe(array_dl)

    freqs = []
    nbins = 4
    for i in range(nbins):
        freqs.append(frequency(dl, i))

    #print freqs[0], freqs[1]

    return array_dl


# pre-computed probabilities
def read_probabilities(na, nd):
    probs = [] # first entry is 0 losses for defence, 2nd is 1 lost, etc ...
    if na == 3 and nd == 3:
        probs.append(0.383286)
        probs.append(0.265047)
        probs.append(0.214469)
        probs.append(0.137198)

    if na == 3 and nd == 2:
        probs.append(0.292765)
        probs.append(0.335264)
        probs.append(0.371971)
        probs.append(0.0)

    if na == 3 and nd == 1:
        probs.append(0.339015)
        probs.append(0.660985)
        probs.append(0.0)
        probs.append(0.0)

    if na == 2 and nd == 3:
        probs.append(0.619133)
        probs.append(0.254732)
        probs.append(0.126135)
        probs.append(0.0)

    if na == 2 and nd == 2:
        probs.append(0.44711)
        probs.append(0.324465)
        probs.append(0.228425)
        probs.append(0.0)

    if na == 2 and nd == 1:
        probs.append(0.421499)
        probs.append(0.578501)
        probs.append(0.0)
        probs.append(0.0)

    if na == 1 and nd == 3:
        probs.append(0.825707)
        probs.append(0.174293)
        probs.append(0.0)
        probs.append(0.0)

    if na == 1 and nd == 2:
        probs.append(0.745547)
        probs.append(0.254453)
        probs.append(0.0)
        probs.append(0.0)

    if na == 1 and nd == 1:
        probs.append(0.583314)
        probs.append(0.416686)
        probs.append(0.0)
        probs.append(0.0)

    return probs

#______________ compute probabilites _____________
def simulate_attack(na, nd, opt):

    opt_gen = False
    opt_mar = False

    if opt == 'gen':
        opt_gen = True
    if opt == 'mar':
        opt_mar = True

    n_disp_att = na - 1
    n_disp_def = nd

    # find out X vs Y
    natt=-1
    ndef=-1

    opt_alive = True
    while (n_disp_att>0 and n_disp_def>0):

        #print ' --- new round --- '

        #print n_disp_att, n_disp_def
        # attack with 3 if more than 3, else with number available -1
        if n_disp_att > 2:
            natt=3
        else:
            natt=n_disp_att

        # defend with 3 if avail., else with whatever available
        if n_disp_def > 2:
            ndef=3
        else:
            ndef=n_disp_def

        # simulate fight
        # readProba = True
        readProba = False

        # this means that at least one fight has been done, and we can update
        # state of marshall/general
        if 'losses' in locals():
            opt_alive = losses[1]
            if opt_gen:
                opt_gen = False
            if opt_mar:
                opt_mar = False

        if not readProba:
            attack = roll(natt)
            defence = roll(ndef)
            losses = gen_losses(attack, defence, opt_gen, opt_mar)

        else:
            ps = read_probabilities(natt, ndef)
            # need integers to fill array
            rounding = 3
            p0 = int(round(ps[0],3)*1e3)
            p1 = int(round(ps[1],3)*1e3)
            p2 = int(round(ps[2],3)*1e3)
            p3 = int(round(ps[3],3)*1e3)

            plist = [0]*p0 + [1]*p1 + [2]*p2 + [3]*p3
            def_lost = random.choice(plist)
            att_lost = natt - def_lost
            losses = ((att_lost, def_lost),True)

        #print 'attacker has ', n_disp_att+1, 'and attacks with', natt
        #print 'defender has ', n_disp_def, 'and defends with', ndef

        #print attack
        #print defence

        #print 'lost:', gen_losses(attack, defence, False, False)[0], gen_losses(attack, defence, False, False)[1]

        #print 'losses', losses
        n_disp_att -= losses[0][0]
        n_disp_def -= losses[0][1]

        #print 'left for next round:', n_disp_att, n_disp_def

    return (n_disp_att+1, n_disp_def)
    #print 'final result', n_disp_att, n_disp_def



#_________ plotting _____________

def plot(n, na, nd, opt_gen, opt_mar):

    dl = compute_sequence(n, na, nd, opt_gen, opt_mar)

    ax = plt.figure().gca()
    ax.set_yticks([x for x in np.arange(0,1.0,0.05)])

    labels=('0', '1', '2', '3')

    def format_fn(tick_val, tick_pos):
        if int(tick_val) in [0,1,2,3]:
            return labels[int(tick_val)]
        else:
            return ''

    ax.xaxis.set_major_formatter(FuncFormatter(format_fn))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    plt.hist(dl, normed=True, bins=4, range=(-.5,3.5), rwidth=0.9, color='#607c8e')
    #plt.figtext(1.0, 0.2, stats.describe(dl))
    plt.ylabel('Probability')
    plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)

    plt.ylim(top=1.0)  # adjust the top leaving bottom unchanged
    plt.ylim(bottom=0.0)  # adjust the bottom leaving top unchanged
    #plt.xlabel('N lost (A)')
    ax.set_title('{} vs {}    <N>={:.1f}, std={:.1f}'.format(na,nd,np.mean(dl), np.std(dl)))


    fin_lab = ''
    if opt_gen: fin_lab = '_gen'
    if opt_mar: fin_lab = '_mar'

    #ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.savefig('plots/{}v{}{}.png'.format(na,nd,fin_lab))


#__________________________
def computeFrequencies(n, na, nd, quants, opt):
    xa = []
    ya = []

    # define frequencies for various quantiles
    freqs = dict()
    # "quantile" is defined by how many tanks left to the attacker (min 2)


    for i in range(n):
        pair = simulate_attack(na,nd,opt)
        xa.append(pair[0])
        ya.append(pair[1])

    x = np.array(xa)
    y = np.array(ya)

    for q in quants:
        freq = frequencyGtr(x, q)
        freqs[q] = freq

    return freqs


#________________________________________________________________`
def computeMatrices(n, nmax, quants, opt):

    z = dict()
    for q in quants:
        z[q] = np.zeros((nmax,nmax))

    #defences
    for j in range(1,nmax+1):
        # attacks
        for i in range(1,nmax+1):
            freqs = computeFrequencies(n, i, j, quants, opt)
            for q in quants:
                z[q][i-1,j-1] = freqs[q]

    #print z[2]

    return z


#_____________________________________________________________________________________________________
def runMT_pool(args=('','','','','')):
    n, i, j, quants, opt=args
    print "running (i,j): {},{}".format(i,j)
    freqs = computeFrequencies(n, i, j, quants, opt)
    return ((i, j), freqs)

#________________________________________________________________`
def computeMatricesMT(n, nmax, quants, opt):
    print 'NUMBER OF CORES    ', mp.cpu_count()
    print ''

    z = dict()
    for q in quants:
        z[q] = np.zeros((nmax,nmax))

    threads = []

    #defences
    for j in range(1,nmax+1):
        # attacks
        for i in range(1,nmax+1):
            thread = (n, i, j, quants, opt)
            threads.append(thread)

    pool = mp.Pool(mp.cpu_count())
    jobs = pool.map(runMT_pool,threads)

    for j in range(1,nmax+1):
        # attacks
        for i in range(1,nmax+1):
            for job in jobs:
                if job[0] == (i,j):
                    freqs = job[1]
                    for q in quants:
                        z[q][i-1,j-1] = freqs[q]

    return z


#__________________________________________________________
def produceMatrixPlot(z, q):

    sx = z.shape[0]
    sy = z.shape[1]

    #print z
    # make these smaller to increase the resolution
    dx, dy = 1, 1

    y, x = np.mgrid[slice(1, sy + dy, dy),
                    slice(1, sx + dx, dx)]

    levels = MaxNLocator(nbins=11).tick_values(z.min(), z.max())

    cmap = plt.get_cmap('Reds')
    norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

    fig, ax0 = plt.subplots(nrows=1)

    ax0.set_xlabel('N(defence)')
    ax0.set_ylabel('N(attack)')

    im = ax0.pcolormesh(x, y, z, cmap=cmap, norm=norm)
    fig.colorbar(im, ax=ax0)
    ax0.set_title('P(N > {})'.format(q))
    plt.savefig('plots/matrix_{}x{}_{}.png'.format(z.shape[0], z.shape[1], q))


#__________________________________________________________
def produceSlicePlot(data, name):

    #print data

    # filter out subset of lines
    # add A=D, A=2D, A = 3D lines (dashed)
    # compute matrix once and store np array

    data_AeqD = []
    data_Aeq2D = []
    data_Aeq3D = []

    for x in range(0, data.shape[0]):
        for y in range(0, data.shape[1]):
            if (x+1) == (1*(y+1)): data_AeqD.append(data[x,y])
            if (x+1) == (2*(y+1)): data_Aeq2D.append(data[x,y])
            if (x+1) == (3*(y+1)): data_Aeq3D.append(data[x,y])
    data_AeqD = np.array(data_AeqD)
    data_Aeq2D = np.array(data_Aeq2D)
    data_Aeq3D = np.array(data_Aeq3D)


    xmax = 30
    # create x vals
    nd = np.arange(1,xmax+1)
    fig, ax = plt.subplots(figsize=(7, 5))

    print len(nd), len(data_AeqD), len(data_Aeq2D), len(data_Aeq3D)


    att_vals = [5, 7, 10, 15, 20, 30]

    print data[5]
    for i in att_vals:
        ax.plot(nd, data[i-1][:xmax], label='A={}'.format(i), linewidth=2)

    ax.plot(nd, data_AeqD[:xmax], label='A=D'.format(i), linestyle='--', linewidth=2)
    ax.plot(nd, data_Aeq2D[:xmax], label='A=2D'.format(i), linestyle='--', linewidth=2)
    ax.plot(nd, data_Aeq3D[:xmax], label='A=3D'.format(i), linestyle='--', linewidth=2)

    ax.set_title('A winning probabilities')
    ax.legend(loc='upper right')
    ax.set_ylabel('P(A wins)')
    ax.set_xlabel('D: initial number of defending armies')
    ax.set_xlim(xmin=nd[0], xmax=nd[-1])

    ax.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
    ax.grid(True, 'major', 'x', ls='--', lw=.5, c='k', alpha=.3)

    fig.tight_layout()
    #fig.show()
    fig.savefig('plots/{}.png'.format(name))

###_________________________________________________________________
def fightDistribution(n, na, nd):

    results = []
    for i in range(n):
        results.append(simulate_attack(na, nd))

    #print results

    labels = []
    xvalues = []
    pairs = []
    frequencies = []
    freq_dict = dict()
    map_val_lab = dict()

    for i in range(-nd,na,1):

        if i == 0:
            continue
        xvalues.append(i)

        #print i

        label = ''
        pair = ()
        if i < 0:
            label = '(1,{})'.format(-i)
            pair = (1,-i)
        elif i > 0:
            label = '({},0)'.format(i+1)
            pair = (i+1,0)

        labels.append(label)
        pairs.append(pair)
        map_val_lab[i] = label

        #print pair
        fr = frequency(results,pair)
        frequencies.append(fr)
        freq_dict[i] = fr

    #print map_val_lab
    #print frequencies
    #print xvalues

    def stats(freq_dict):
        mean = 0
        stddev = 0
        #### compute mean
        for val, freq in freq_dict.iteritems():
            #print val, freq
            mean += float(val)*freq
        #return mean
        #### compute stddev
        for val, freq in freq_dict.iteritems():

            stddev += freq*(float(val) - mean)**2
        stddev = math.sqrt(stddev)
        return mean, stddev

    sts = stats(freq_dict)
    print sts[0], sts[1]
    #print

    def format_fn(tick_val, tick_pos):
        if int(tick_val) in xvalues:
            return labels[int(tick_val)]
            #print labels[int(tick_val)]
        else:
            return ''

    size_x = float(na+nd)/2
    fig, ax = plt.subplots(figsize=(size_x, 5))

    #ax = plt.figure().gca()
    #ax.set_yticks([x for x in np.arange(0,1.0,0.05)])

    #ax.xaxis.set_major_formatter(FuncFormatter(format_fn))
    #ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    nbins = na+nd-1
    #range = (-nd-1,na)

    plt.bar(xvalues, frequencies, color='#607c8e')
        #plt.figtext(1.0, 0.2, stats.describe(dl))
    plt.ylabel('Probability')
    plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)

    plt.xticks(xvalues, labels, rotation=60)

    plt.margins(0.1, 0.1)
    #plt.ylim(top=1.0, bottom=0.0)  # adjust the bottom leaving top unchanged
        #plt.xlabel('N lost (A)')

    title = '{} vs {}  <N>={:.1f}, std={:.1f}'.format(na,nd,sts[0],sts[1])
    ax.set_title(title)
        #ax.xaxis.set_major_locator(MaxNLocator(integer=True)
    #plt.show()
    plt.tight_layout()
    plt.savefig('plots/attack{}vs{}.png'.format(na,nd))
    #input("Press Enter to continue...")

#________________________________________________________________________________

##__________ produce single-shot plots ___________###

'''
n=10000

plot(n, 3, 3, False, False)
plot(n, 3, 3, True, False) #General
plot(n, 3, 3, False, True) #Mar

plot(n, 3, 2, False, False)
plot(n, 3, 2, True, False) #General
plot(n, 3, 2, False, True) #Mar

plot(n, 3, 1, False, False)
plot(n, 3, 1, True, False) #General
plot(n, 3, 1, False, True) #Mar

plot(n, 2, 2, False, False)
plot(n, 2, 2, True, False) #General
plot(n, 2, 2, False, True) #Mar

plot(n, 2, 1, False, False)
plot(n, 2, 1, True, False) #General
plot(n, 2, 1, False, True) #Mar

plot(n, 1, 1, False, False)
plot(n, 1, 1, True, False) #General
plot(n, 1, 1, False, True) #Mar
'''

##__________ produce matrix and store it in ext file as np array___________###

'''
quants = [2]
matrices = computeMatricesMT(5000, 100, quants)
data = matrices[2]
np.savez_compressed('data/data.npz', data=data)
'''

'''
na = 3
nd = 3
attack = roll(na)
defence = roll(nd)

opt_alive= True
losses = gen_losses(attack, defence, opt_gen=False, opt_mar=True, opt_alive=opt_alive)
'''

'''simulate_attack(14,4,'gen')

quants = [8]
freqs = computeFrequencies(1000, 14, 4, quants, '')
print freqs
freqs = computeFrequencies(1000, 14, 4, quants, 'gen')
print freqs
freqs = computeFrequencies(1000, 14, 4, quants, 'mar')
print freqs
'''

'''
quants = [2]
matrices_gen = computeMatricesMT(5000, 100, quants, 'gen')
data = matrices_gen[2]
np.savez_compressed('data/data_gen.npz', data=data)


matrices_mar = computeMatricesMT(5000, 100, quants, 'mar')
data = matrices_mar[2]
np.savez_compressed('data/data_mar.npz', data=data)
'''

##__________ load pre-computed matrix __________________

#loaded = np.load('data/data.npz')
loaded = np.load('data/data.npz')
data = loaded['data']
produceSlicePlot(data, 'slices_def')

loaded = np.load('data/data_gen.npz')
data = loaded['data']
produceSlicePlot(data, 'slices_gen')

loaded = np.load('data/data_mar.npz')
data = loaded['data']
produceSlicePlot(data, 'slices_mar')

##__________ produce matrix plots __________________

#quants = [2]
#for q in quants:
#    produceMatrixPlot(matrices[q], q)

#$produceMatrixPlot(data, 2)


##_________ produce fight distribution ___________

'''
try:
  input = raw_input
except:
  pass

'''

#__________________________________________________________________
'''
listFights = [
(3,1),
(5,2),
(6,2),
(6,3),
(7,2),
(8,3),
(8,2),
(9,3),
(12,4),
(10,3),
(20,8),
(20,6),
(25,10),
(30,10),
(30,15),
]

for f in listFights:
    fightDistribution(10000, f[0], f[1])
'''
