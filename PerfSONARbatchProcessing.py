from os import listdir
from time import time

import numpy as np
import pandas as pd
import random

from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout

from sklearn.model_selection import train_test_split

from pandas.tseries.offsets import *



# tuning parameters
ref = 24
sub = 1
path='/data/'

chance = ref/(sub+ref)
cut = chance + (1-chance) * 0.05
print('chance:',chance, '\tcut:', cut)
ref = ref * Hour()
sub = sub * Hour()


def scaled_accuracy(accuracy, ref_samples, sub_samples):
    chance = float(ref_samples)/(ref_samples+sub_samples)
    rescale = 1/(1 - chance)
    return (accuracy-chance)*rescale

class ANN(object):
    def __init__(self, df, auc_df):
        self.n_series = df.shape[1]
        self.df = df
        self.auc_df = auc_df
        
        self.nn = Sequential()
        self.nn.add(Dense(units=self.n_series*2, input_shape=(self.n_series,), activation='relu' ))
#       self.nn.add(Dropout(0.5))
        self.nn.add(Dense(units=self.n_series, activation='relu'))
#       self.nn.add(Dropout(0.5))
        self.nn.add(Dense(units=1, activation='sigmoid'))
#       self.nn.compile(loss='hinge', optimizer='sgd', metrics=['binary_accuracy'])
#       self.nn.compile(loss='mse',optimizer='rmsprop', metrics=['accuracy'])
        self.nn.compile(loss='binary_crossentropy',optimizer='rmsprop', metrics=['accuracy'])
#       self.nn.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['binary_accuracy'])
        self.nn.summary()
    
    def check_for_anomaly(self,ref, sub, count):
    
        y_ref = pd.Series([0] * ref.shape[0])
        X_ref = ref
    
        y_sub = pd.Series([1] * sub.shape[0])
        X_sub = sub
        
        # separate Reference and Subject into Train and Test
        X_ref_train, X_ref_test, y_ref_train, y_ref_test = train_test_split(X_ref, y_ref, test_size=0.3, random_state=42)
        X_sub_train, X_sub_test, y_sub_train, y_sub_test = train_test_split(X_sub, y_sub, test_size=0.3, random_state=42)
    
        # combine training ref and sub samples
        X_train = pd.concat([X_ref_train, X_sub_train])
        y_train = pd.concat([y_ref_train, y_sub_train])

        # combine testing ref and sub samples
        X_test = pd.concat([X_ref_test, X_sub_test])
        y_test = pd.concat([y_ref_test, y_sub_test])
    
        X_train = X_train.reset_index(drop=True)
        y_train = y_train.reset_index(drop=True)
    
        X_train_s, y_train_s = shuffle(X_train, y_train)
    
#         with tf.device('/gpu:0'):
        hist = self.nn.fit(X_train_s.values, y_train_s.values, epochs=100, verbose=0, shuffle=True, batch_size=10)
        loss_and_metrics = self.nn.evaluate(X_test.values, y_test.values)#, batch_size=256)
        print(loss_and_metrics)
        
        return scaled_accuracy(loss_and_metrics[1], ref.shape[0], sub.shape[0])
    
    
    def loop_over_intervals(self):
        lstart = self.df.index.min()
        lend = self.df.index.max()

        #round start 
        lstart.seconds=0
        lstart.minutes=0

        # loop over them
        ti = lstart + ref + sub
        count = 0
        while ti < lend + 1 * Minute():
            print(count)
            startt = time()
            ref_start = ti-ref-sub
            ref_end = ti-sub
            ref_df = self.df[(self.df.index >= ref_start) & (self.df.index < ref_end)]
            sub_df = self.df[(self.df.index >= ref_end) & (self.df.index < ti)]
            if sub_df.shape[0]>60 * 0.7 and ref_df.shape[0]>24*60*0.7:
                score = self.check_for_anomaly(ref_df, sub_df, count)
            else:
                score = 0
            self.auc_df.loc[(self.auc_df.index >= ref_end) & (self.auc_df.index < ti), ['score']]  = score
            print('\n',ti,"\trefes:" , ref_df.shape, "\tsubjects:", sub_df.shape, '\tacc:', score)
            ti = ti + sub
            print("took:", time()-startt)
            count = count + 1
            #if count>2: break    
    
    
while True:
    objs = listdir(path)
    print(objs)
    toProcess=''
    for o in objs:
        if o.startswith('proc_') or o.startswith('res_'): continue
        if o.endswith('.h5') and "res_"+o not in objs and "proc_"+o not in objs:
            toProcess=o
            f  = open(path + 'proc_' + o, 'w')
            f.write(str(time()))
            f.close()
            break
    if toProcess=='': 
        break
    
    print('Processing:', toProcess)
    full_df = pd.read_hdf(path+toProcess,'data')
    print(full_df.shape)
    full_df = full_df[:3000]
    print(full_df.shape)
    print (full_df.index.min(), full_df.index.max())
    full_df.fillna(0, inplace=True)
    auc_df = pd.DataFrame(np.nan, index=full_df.index, columns=['score'])
    ann = ANN(full_df, auc_df)
    ann.loop_over_intervals()
                          
    hdf = pd.HDFStore( path + 'res_' + o)
    hdf.put('result', auc_df, format='table', data_columns=True)
    hdf.close()
