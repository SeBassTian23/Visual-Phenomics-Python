# Visual Phenomics | DataFrame

> Import data output from [Visual Phenomics] into a convenient [DataFrame] for subsequent analysis in [Python].

## Installation
Install using pip in the terminal. If you are using [Anaconda], make sure, you are using the Conda environment, activating it using the `conda activate` command in the terminal.

```bash
pip install git+https://github.com/SeBassTian23/Visual-Phenomics-Python.git --upgrade --no-cache-dir
```

Install package from local source by downloading the package and installing it manually using the command below.

```bash
python setup.py install --user
```

***

## Getting started

Once the package is installed, 

### Import Single Experiment

Import one experiment processed by Visual Phenomics.

```py
import visual_phenomics_py as vppy

vppy.dataframe('./path/to/experiment-data')
```

### Import Multiple Experiments

```py
import visual_phenomics_py as vppy

df = vppy.dataframe(['./path/to/experiment_01','./path/to/experiment_02'])
```

## Additional Functions

### Dataframe Info

Information about the DataFrame. This includes columns, data types and memory consumption.

```py
## DataFrame info using vppy
vppy.info(df)

## DataFrame info using pandas
df.info(memory_usage='deep')
```

### Sample Names

This function returns a list of unique sample names found within the experiment or experiments.

```py
samples = vppy.samples(df)
```

### DataFrame Description

This function returns a worded description of the DataFrame content in regards to the experiment(s).

```py
vppy.description(df)
```

### Plot Data

This function allow to quickly plot a single parameter versus time. If needed, the values for each sample can be averaged and the standard deviation is indicated as well. Data for each day is displayed in a separate plot.

```py
## Plot individual samples for the parameter Phi2
vppy.plot(df, 'phi2')

## Plot averaged values for samples for the parameter Phi2
vppy.plot(df, 'phi2', avg=True)
```

The light intensities defined and used in the experiment can be plotted in a single plot.

```py
## Plot individual samples for the parameter Phi2
vppy.plot_light(df)
```

### Calculations

Based of the available data imported into the dataframe, parameters can be calculated or re-calculated. Two functions are available. One to calculate parameters from the basic parameters directly derived from the images using Visual Phenomics and parameters, that are based on additional information like light intensity. The other one is for calculations based on parameters returned by the fist one.

#### Basic Calculations

For the calculation of basic parameters, the following parameters are available: `Fvfm`, `NPQ`, `NPQt`, `Phi2`, `PhiNO`, `PhiNOt`, `PhiNPQ`, `PhiNPQt`, `qE`, `qEsv`, `qEt`, `qI`, `qIt`, `qL`, and `qP`.

```py
calculate(df=None, param='', *, fm='fm', f0='f0', fmp='fmp', f0p='f0p', fs='fs', fmpp='fmpp', f0pp='f0pp', fmf0=4.88, alias=None)
```

Examples for calculations:

```py
# Calculating Phi2
vppy.calculate_additional(df,'Phi2')

# Calculating Phi2 and redefine the used column names
vppy.calculate(df,'Phi2', fmp='FMP')

# Calculating Phi2 and redefine the value for Fm/F0 (default 4.88)
vppy.calculate(df,'Phi2', fmf0=4.0)

# Calculating Phi2 and renaming the column returned
vppy.calculate(df,'Phi2', alias='YII')
```

#### Additional Calculations

These additional calculations are for parameters that were calculated using the parameters returned by the basic calculation function. The parameters include `LEF`, `Vx`, `SPhi2`, `SNPQ`, and `deltaNPQ`.

```py
calculate_additional(df=None, param='', *, v_phino='PhiNOt', v_phi2='Phi2', v_ql='qL', v_par='light_intensity', phinoopt=0.2, absorptivity=0.5, fmf0=4.88, alias=None)
```

Examples for calculations:

```py
# Calculating LEF
vppy.calculate_additional(df,'LEF')

# Calculating LEF and redefine the used column names
vppy.calculate_additional(df,'LEF', v_phi2='YII')

# Calculating LEF and redefine the value for absorptivity (default 0.5)
vppy.calculate_additional(df,'LEF', absorptivity=0.45)

# Calculating LEF and renaming the column returned
vppy.calculate_additional(df,'LEF', alias='PPFD')
```

#### Custom Calculations

It also allows to create custom functions and apply the calculations to a dataframe column.

```py
calculate_custom(df=None, name='', fn=None , *, cols=[], params={})
```

Examples for calculations:

```py
## Function with not parameters
def func():
  return 'Hello World'

vppy.calculate_custom(df, 'CustomFn', func )

## Function requiring data from columns to calculate Phi2
def func( fmp, fs ):
  return (fmp - fs) / fmp

vppy.calculate_custom(df, 'CustomPhi2', func, cols=['fmp', 'fs'] )

## Function requiring data from columns and parameters to calculate LEF
def func( fmp, fs, light, absorptivity=0.5 ):
  return ( (fmp - fs) / fmp ) * light * absorptivity

vppy.calculate_custom(df, 'CustomLEF', func, cols=['fmp', 'fs', 'light_intensity'], params={'absorptivity': 0.45} )

```

[DataFrame]: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html "DataFrame"

[Python]: https://www.python.org/ "Python"

[Anaconda]: https://www.continuum.io/downloads "Anaconda"

[DataFrame]: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html "DataFrame"

[Visual Phenomics]: https://caapp-msu.bitbucket.io/projects/visualphenomics5.0 "Visual Phenomics 5"
