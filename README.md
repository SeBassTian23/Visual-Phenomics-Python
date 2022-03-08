# Visual Phenomics | DataFrame

> Import data output from Visual Phenomics into a convenient [DataFrame] for subsequent analysis in [Python].

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

vppy.build_dataframe('./path/to/experiment-data')
```

### Import Multiple Experiments

```py
import visual_phenomics_py as vppy

df = vppy.build_dataframe(['./path/to/experiment_01','./path/to/experiment_02'])
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

*not availabl yet*

[DataFrame]: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html "DataFrame"

[Python]: https://www.python.org/ "Python"

[Anaconda]: https://www.continuum.io/downloads "Anaconda"

[DataFrame]: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html "DataFrame"
