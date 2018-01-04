### this module generates (and plots) simulated anomalous timeseries

import pandas as pd
import numpy as np

def get_simulated_data(n_series=6, p_anomaly = 10E-6, max_noise_amplitude = 0.025, max_anomaly_offset=0.3, max_anomaly_duration = 4*3600, start_date = '2017-08-01 00:00:00', end_date = '2017-08-07 23:59:59', seed=38):
   
    # generate normal data
    np.random.seed(seed)
    dti = pd.DatetimeIndex(start=start_date, end=end_date, freq='s')
    n_timesteps = len(dti)
    df = pd.DataFrame()
    for s in range(n_series):
        # gaussian with mean between 0 and 0.6, and amplitude in one of 8 steps of max
        v = np.random.normal(np.random.uniform(0,0.6), max_noise_amplitude/np.random.randint(1, 8), n_timesteps) 
        df['link '+str(s)] = pd.Series(v)
    df.index = dti
    df['flag']=0
    
    # add anomalies
    to_generate = int(n_timesteps * p_anomaly)
    for a in range(to_generate):
        affects = np.random.choice(n_series, np.random.randint(1, n_series), replace=False)
        duration = int(max_anomaly_duration * np.random.random_sample())
        start = np.random.randint(1, n_timesteps)
        end = min(start + duration, n_timesteps)
        print('affected:', affects, df.iloc[start].name, df.iloc[end].name)
        for s in affects:
            df.iloc[start:end,s] = df.iloc[start:end,s] + np.random.uniform(0, max_anomaly_offset)
        df.iloc[start:end,n_series]=1
    
    # enforce range
    df[df<0] = 0
    df[df>1] = 1
    
    return df

def get_simulated_fixed_data(n_series=6, max_noise_amplitude = 0.025, start_date = '2017-08-01 00:00:00', end_date = '2017-08-07 23:59:59', seed=38):
    # generate normal data
    np.random.seed(seed)
    dti = pd.DatetimeIndex(start=start_date, end=end_date, freq='s')
    n_timesteps = len(dti)
    df = pd.DataFrame()
    mean = np.random.uniform(0, 0.6, n_series)
    sigma = max_noise_amplitude / np.random.randint(1, 8, n_series)
    print('mean: ', mean)
    print('sigma: ', sigma)
    for s in range(n_series):
        # gaussian with mean between 0 and 0.6, and amplitude in one of 8 steps of max
        v = np.random.normal(mean[s], sigma[s], n_timesteps) 
        df['link '+str(s)] = pd.Series(v)
    df.index = dti
    df['flag']=0
    
    # add fixed anomalies
    
    # moving just a little
    affects = [0]
    duration = 1 * 3600
    start = 25 * 3600
    end = min(start + duration, n_timesteps)
    print('affected:', affects, df.iloc[start].name, df.iloc[end].name)
    for s in affects:
        df.iloc[start:end,s] = df.iloc[start:end,s] + sigma[s] * 2
    df.iloc[start:end, n_series]=1
    
    affects = [0]
    duration = 3 * 3600
    start = 49 * 3600
    end = min(start + duration, n_timesteps)
    print('affected:', affects, df.iloc[start].name, df.iloc[end].name)
    for s in affects:
        df.iloc[start:end,s] = df.iloc[start:end,s] + sigma[s] * 2
    df.iloc[start:end, n_series]=1
    
    affects = [0, 3, 4]
    duration = 1 * 3600
    start = 73 * 3600
    end = min(start + duration, n_timesteps)
    print('affected:', affects, df.iloc[start].name, df.iloc[end].name)
    for s in affects:
        df.iloc[start:end,s] = df.iloc[start:end,s] + sigma[s] * 2
    df.iloc[start:end, n_series]=1
    
    # moving a lot 
    affects = [0]    
    duration = 1 * 3600
    start = 97 * 3600
    end = min(start + duration, n_timesteps)
    print('affected:', affects, df.iloc[start].name, df.iloc[end].name)
    for s in affects:
        df.iloc[start:end,s] = df.iloc[start:end,s] + sigma[s] * 5
    df.iloc[start:end, n_series]=1
    
    affects = [0]
    duration = 3 * 3600
    start = 121 * 3600
    end = min(start + duration, n_timesteps)
    print('affected:', affects, df.iloc[start].name, df.iloc[end].name)
    for s in affects:
        df.iloc[start:end,s] = df.iloc[start:end,s] + sigma[s] * 5
    df.iloc[start:end, n_series]=1
    
    affects = [0, 3, 4]
    duration = 1 * 3600
    start = 145 * 3600
    end = min(start + duration, n_timesteps)
    print('affected:', affects, df.iloc[start].name, df.iloc[end].name)
    for s in affects:
        df.iloc[start:end,s] = df.iloc[start:end,s] + sigma[s] * 5
    df.iloc[start:end, n_series]=1
    
    
    # enforce range
    df[df<0] = 0
    df[df>1] = 1
    
    return df




