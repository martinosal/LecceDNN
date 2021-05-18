import matplotlib.pyplot as plt
import configparser
import re
import ast
from colorama import init, Fore
from Functions import checkCreateDir, ShufflingData
import pandas as pd
import numpy as np

### Reading from config file
config = configparser.ConfigParser()
config.read('MyConfig.txt')
inputFiles = ast.literal_eval(config.get('config', 'inputFiles'))
dataType = ast.literal_eval(config.get('config', 'dataType'))
rootBranchSubSample = ast.literal_eval(config.get('config', 'rootBranchSubSample'))
dfPath = config.get('config', 'dfPath')
print (format('Output directory: ' + Fore.GREEN + dfPath), checkCreateDir(dfPath))

analysis='resolved'
channel='ggF'
PreselectionCuts=''

def find(str_jets):
    n=0
    for i in df['origin']==str_jets:
        if i==True:
            n+=1
    return n

df=pd.read_pickle(dfPath + 'MixData_PD_' + analysis + '_' + channel + '.pkl')

samples=['Zjets','Wjets','stop','Diboson','ttbar','Radion','VBFRSG','RSG','VBFRadion','VBFHVTWZ']

x=np.array([])
for var in samples:
    x=np.append(x,find(var))

plt.figure(1,figsize=(18,6))
plt.bar(samples,x)
#plt.text(3, 80, analysis+' '+channel , fontsize=12,horizontalalignment='center',verticalalignment='center')
plt.suptitle(analysis+' '+channel+' composition')
plt.yscale('log')
plt.savefig(analysis+'_'+channel+'_composition.pdf')
#plt.show()
