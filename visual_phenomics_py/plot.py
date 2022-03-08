"""
Plot data from visual phenomics data
"""

from numpy import ceil
import matplotlib.pyplot as plt

def plot_light(df=None):
  """
  Plot light intensities 

  :param df: DataFrame
  :returns: Plot
  """
  if df is not None:
    df.groupby(['time','light_intensity'])[['time','light_intensity']].agg('mean').plot( 
      kind = 'scatter',
      x = 'time',
      y = 'light_intensity',
      title = 'Light Intensities'
    )
  else:
    print('No DataFrame selected.')


def plot(df=None, param=None, *, avg=False):
  """
  Plot a parameter, either for individual samples or as an average with standard-deviation
  for each sample name.
  Each day is represented in an individual plot.

  :param df: DataFrame
  :param param: Fluorescence based parameter (e.g. phi2)
  :param avg: average with standard-deviation (default: False)
  :returns: Plot
  """
  days = int(ceil(df['time'].max()/24))

  for i in range(0,days):
    df_tmp = df[(df['time'].between(i * 24, i * 24 + 24))]

    fig, ax = plt.subplots( figsize=(8,5))
    for strain in df['name'].unique():
      if avg:
        x = df_tmp[ (df_tmp['name'] == strain) ].groupby(['name','time'])['time']
        y = df_tmp[ (df_tmp['name'] == strain) ].groupby(['name','time'])[param]
    
        ax.errorbar( x.agg('mean'), y.agg('mean'), 
          yerr=y.agg('sem'), fmt='.-', markersize=10, capsize=4, 
          elinewidth=1, label= strain )
      else:
        ax.scatter( 
          df_tmp[df_tmp['name'] == strain]['time'],
          df_tmp[df_tmp['name'] == strain][param],
          label=strain
        )
        
    ax.set_title( 'Day {0}'.format(i+1) )
    ax.set_xlabel('Time [h]')
    ax.set_ylabel(param)
    plt.legend()
    plt.tight_layout()
    plt.show()

