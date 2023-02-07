"""
Plot data from visual phenomics data
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors


def plot_light(df=None):
    """Plot light intensities

    Light intensities plotted over time in a single figure.

    :param df: DataFrame
    :returns: Plot
    """

    if df is None:
        raise Exception('No DataFrame selected.')

    if 'light_intensity' not in df:
        raise Exception('No "light_intensity" column found.')

    df.drop_duplicates(['time', 'light_intensity'])[['time', 'light_intensity']].plot(
        kind='scatter',
        x='time',
        y='light_intensity',
        title='Light Intensities',
        figsize=(15,5)
    )


def plot(df=None, param=None, *, avg=False, err='sem', days=[]):
    """Plot a single parameter over time.

    Plot a parameter, either for individual samples or as an average with standard-deviation
    for each sample name.

    :param df: DataFrame
    :param param: Fluorescence based parameter (e.g. phi2)
    :param avg: average with error (default: False)
    :param err: error indication, "sem" standard error  or "std" standard deviation (default: sem)
    :param days: list with the days to plot (e.g. [1,3] for day 1 and 3)
    :returns: Plot
    """

    if df is None:
        raise Exception('No DataFrame selected.')

    df_tmp = df

    if len(days) > 0:

        alltimes = df['time'].unique()
        selectedtimes = np.array([])

        for i in days:
            idx = (alltimes > ((i-1) * 24)) * (alltimes < ((i-1) * 24 + 23.9))
            selectedtimes = np.append(
                selectedtimes, [alltimes[n] for n in np.where(idx)])

        df_tmp = df[df['time'].isin(selectedtimes)]

    if avg:
        pmean = df_tmp.groupby(['name', 'time'])[param].agg('mean')
        psem = df_tmp.groupby(['name', 'time'])[param].agg(err)

    fig, ax = plt.subplots(figsize=(12, 8))

    for strain in df_tmp['name'].unique():

        # Plot averages with standard deviation
        if avg:
            if strain not in pmean:
                continue

            # drop nan values for averages and replace stdev with
            # 0 if it is a nan value
            ptime = pmean[strain].index.get_level_values('time')

            x = []
            y = []
            yerror = []

            for idx, val in enumerate(pmean[strain].values):
                if np.isnan(val):
                    continue
                else:
                    x.append(ptime[idx])
                    y.append(val)
                    if np.isnan(psem[strain].values[idx]):
                        yerror.append(0)
                    else:
                        yerror.append(psem[strain].values[idx])

            # Add plot
            ax.errorbar(x, y,
                        yerr=yerror, fmt='.:', markersize=10, capsize=4,
                        elinewidth=1, linewidth=.25, label=strain)
        else:
            ax.scatter(
                df_tmp[df_tmp['name'] == strain]['time'],
                df_tmp[df_tmp['name'] == strain][param],
                label=strain,
                s=10
            )

    if len(days) > 0:
        ax.set_title('{0} - Day(s): {1}'.format(param,
                                                ", ".join(map(str, days))))
    else:
        ax.set_title('{0}'.format(param))
    ax.set_xlabel('Time [h]')
    ax.set_ylabel(param)
    plt.legend()
    plt.tight_layout()
    plt.show()


def heatmap(df=None, param='', days=[], cmap=None, column='name'):
    """Plot parameter as a heat map

    Plot a parameter as a phenotype-over-time heat map. Samples are avagered and represented as one row in the heat map.

    :param df: DataFrame
    :param param: Fluorescence based parameter (e.g. phi2)
    :param days: list with the days to plot (e.g. [1,3] for day 1 and 3)
    :param cmap: matplotlib colormap
    :param column: column used to group the measurements (default: name)
    :returns: Plot
    """

    if df is None:
        raise Exception('No DataFrame selected.')

    if column is None or type(column) is not str:
        raise Exception('Selected column needs to be a string.')

    if column not in df.columns:
        raise Exception('No column or non existing column selected to group measurements.')

    alldays = int(df['day'].max())
    strains = df[column].unique()

    if len(days) == 0:
        days = range(1, alldays+1)

    if cmap is None:
        cmap = cm.rainbow

    height = (int(np.ceil(len(strains) / 3)))

    if height < 2:
        height = 2

    fig, axes = plt.subplots(1, len(days), figsize=(12, height), sharey=True)

    if len(days) > 1:
        ax = axes.flat
        a = 0

    ranges = []

    df_range = df[df['day'].isin(days)][[column, 'time', param]]

    ranges.append(df_range.groupby([column, 'time'])[
                    param].agg('mean').min())
    ranges.append(df_range.groupby([column, 'time'])[
                    param].agg('mean').max())

    ranges = np.array(ranges)

    for i in range(0, alldays):

        if (len(days) > 0) & (i+1 not in days):
            continue

        df_tmp = df[(df['day'] == (i+1))].groupby(
                [column, 'time'])[param].agg('mean')

        heatmap = []

        for strain in strains:
            heatmap.append(np.array(df_tmp[strain].values, dtype=float))

        if len(days) == 1:
            axis = axes
        else:
            axis = ax[a]
            a += 1

        # Plot Heatmap
        axis.imshow(heatmap, aspect='auto', vmin=ranges.min(),
                    vmax=ranges.max(), cmap=cmap)

        # Add y-axis ticks
        axis.set_yticks(np.arange(len(strains)))
        axis.set_yticklabels(strains)

        # Remove x-axis ticks
        axis.set_xticks([])

        # Add label
        axis.set_title('Day {0}'.format(i+1))

    # Clean up layout
    plt.tight_layout()

    # now add the colorbar
    fig.subplots_adjust(bottom= (0.65 / height) )

    # Create a new axis to contain the color bar
    cbar_ax = fig.add_axes([0.3, 0, 0.4,  (0.2 / height) ])
    norm = colors.Normalize(vmin=ranges.min(), vmax=ranges.max())
    plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap),
                 cax=cbar_ax, orientation='horizontal', label=param)

    plt.show()
