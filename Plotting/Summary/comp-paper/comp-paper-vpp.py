from matplotlib import pyplot as plt
import sys
import math
import numbers
import numpy as np

from scipy.interpolate import interp1d

def loaderVpp(readfile, l_container={}): 

	l_container={'size':[], 'thr':[], 'clock':[], 'us':[], 'part':[]}
	cline=-1
	count=0
	firstime=0
	for line in readfile:
		for s in line.split():
			element = []
			if count > 0 :
				if ((firstime) == 0) :
					if cline == 0:
						element = l_container['size']
						element.append(s)
					if cline == 1:
						element = l_container['thr']
						element.append(float(s))
					if cline == 2:
						element = l_container['clock']
						element.append(float(s))
					if cline == 3:
						element = l_container['us']
						element.append(float(s))
					if cline == 4:
						element = l_container['part']
						element.append(float(s))
				else :
					if cline == 1:
						element = l_container['thr'][(count-1)]
						element = element +float(s)
						l_container['thr'][(count-1)] = element
					if cline == 2:
						element = l_container['clock'][(count-1)]
						element = element +float(s)
						l_container['clock'][(count-1)] = element
					if cline == 3:
						element = l_container['us'][(count-1)]
						element = element +float(s)
						l_container['us'][(count-1)] = element
					if cline == 4:
						element = l_container['part'][(count-1)]
						element = element +float(s)
						l_container['part'][(count-1)] = element

				count = count + 1
			else: count = count + 1
		cline=cline + 1
		count=0
		if cline > 4: 
		   	cline=-1
			firstime = firstime + 1

	readfile.close

	for column in range(len(l_container['size'])):
		element = l_container['thr'][(column-1)]
		element = element/firstime
		l_container['thr'][(column-1)] = element
		element = l_container['clock'][(column-1)]
		element = element/firstime
		l_container['clock'][(column-1)] = element
		element = l_container['us'][(column-1)]
		element = element/firstime
		l_container['us'][(column-1)] = element
		element = l_container['part'][(column-1)]
		element = element/firstime
		l_container['part'][(column-1)] = element
	return l_container

def loader(readfile, l_container={}): 

	l_container={'size':[], 'thr':[], 'clock':[], 'us':[], 'part':[]}
	cline=0
	count=0
	for line in readfile:
		for s in line.split():
			element = []
			if count > 0 :
				if cline == 0:
					element = l_container['size']
					element.append(s)
				if cline == 1:
					element = l_container['thr']
					element.append(float(s))
				if cline == 2:
					element = l_container['us']
					element.append(float(s))
				if cline == 3:
					element = l_container['clock']
					element.append(float(s))
				if cline == 4:
					element = l_container['part']
					element.append(int(s))
			else: count = 1
		cline=cline + 1
		count=0

	readfile.close

	return l_container

def seed_interpol(seed_line):
	seed_interpol=[]
	
	#x_raw=[1, 2, 10, 100, 500, 1000, 2000, 4000, 8000]
	x_raw=[2, 10, 100, 500, 1000, 2000, 4000, 8000, 16000, 32000]
	x=[float(math.log(elem, 2.0)) for elem in x_raw]
	min_x=min(x)
	max_x=max(x)
	print(str(x))
	y=seed_line
	print(str(seed_line))
	#del y[0]

	#f_interpol = interp1d(x, y, kind='cubic') 
	f_interpol = interp1d(x, y, kind='linear') 

	xnew = np.linspace(min_x, max_x, num=36, endpoint=True)
	seed_interpol = f_interpol(xnew)
	
		
	exp=float(35.0/(max_x))
	x_exp= [elem*exp for elem in x]
	print(str(exp) +" " + str(x_exp) +" " + str(len(seed_line)))

	return seed_interpol,xnew,x


try:
        print("file1: \t" + str(sys.argv[1]))
        print("file2: \t" + str(sys.argv[2]))

        f1 = str(sys.argv[1])
        f2 = str(sys.argv[2])

        fr1 = open(f1, 'r')
        fr2 = open(f2, 'r')
except IndexError:
        print("Error: no Filename")
        sys.exit(2)


seed1_line = {}
seed1_line = loaderVpp(fr1)
#seed1a, x1a, xxa = seed_interpol(seed1_line['thr'])
seed1b, x1b, xxb = seed_interpol(seed1_line['part'])

seed2_line = {}
seed2_line = loaderVpp(fr2)
#seed2a, x2a, xxa = seed_interpol(seed2_line['thr'])
seed2b, x2b, xxb = seed_interpol(seed2_line['part'])

seed3_line = {}
seed3_line = loaderVpp(fr3)
#seed3a, x3a, xxa = seed_interpol(seed3_line['thr'])
seed3b, x3b, xxb = seed_interpol(seed3_line['part'])

seed4_line = {}
seed4_line = loaderVpp(fr4)
#seed4a, x4a, xxa = seed_interpol(seed4_line['thr'])
seed4b, x4b, xxb = seed_interpol(seed4_line['part'])



plt.style.use('valerio-slide')

fig1, ax = plt.subplots(figsize=(14,8))

ax.plot(x1b, seed1b, '--C0', label='VPP 17.10')
ax.plot(x2b, seed2b, '--C1', label='VPP 17.10 - TM')
ax.plot(x3b, seed3b, '--C2', label='TupleMerge - Original')
ax.plot(x4b, seed4b, '--C3', label='TupleSpaceSearch')

ax.set_axisbelow(True)
ax.xaxis.grid(color='gray', linestyle='dashed', linewidth=0.5)
ax.yaxis.grid(color='gray', linestyle='dashed', linewidth=1)

#ax.set_ylim([0,6.5])
#ax.set_ylim([0,1])
ax.set_xlabel('Ruleset size')
ax.set_ylabel('Partition (Count.)')
ax.set_xticks(xxa)
ax.set_xticklabels(['1','10','100','500','1K','2K','4K','8K','16K','32K'])


handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1])


fig1.savefig('pps1.png')
#plt.show()

