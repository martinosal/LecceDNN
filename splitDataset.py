from argparse import ArgumentParser
import configparser

parser = ArgumentParser()
parser.add_argument('-t', '--training', help = 'Relative size of the training sample, between 0 and 1', default = 0.7)

args = parser.parse_args()

print('  training = ', args.training)

trainingFraction = float(args.training)
if args.training and (trainingFraction < 0. or trainingFraction > 1.):
    parser.error('Training fraction must be between 0 and 1')
#logFile = open('logFile.txt', 'a')
#logFile.write('\nTraining fraction: ' + str(trainingFraction))
#logFile.close()

### Reading from config file
config = configparser.ConfigParser()
config.read('Config.txt')
dfPath = config.get('config', 'dfPath')

#### Loading data
import pandas as pd

df_total = pd.read_pickle(dfPath + 'MixData_PD.pkl')

### Splitting sample
Ntrain_stop = int(round(df_total.shape[0] * trainingFraction))
X_Train = df_total[:Ntrain_stop]
X_Test = df_total[Ntrain_stop:]
X_Train.to_pickle(dfPath + 'MixData_PD_Train.pkl')
print('Saved ' + dfPath + 'MixData_PD_Train.pkl')
print(X_Train[:10])
X_Test.to_pickle(dfPath + 'MixData_PD_Test.pkl')
print('Saved ' + dfPath + 'MixData_PD_Test.pkl')
print(X_Test[:10])

print('Size of the training saple: ', X_Train.shape)
print('Size of the testing saple: ', X_Test.shape)