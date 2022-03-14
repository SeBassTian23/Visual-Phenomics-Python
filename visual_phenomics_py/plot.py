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

    df.groupby(['time', 'light_intensity'])[['time', 'light_intensity']].agg('mean').plot(
        kind='scatter',
        x='time',
        y='light_intensity',
        title='Light Intensities'
    )


def plot(df=None, param=None, *, avg=False, days=[]):
    """Plot a single parameter over time in separate figures for each day.

    Plot a parameter, either for individual samples or as an average with standard-deviation
    for each sample name. Each day is represented in an individual figure.

    :param df: DataFrame
    :param param: Fluorescence based parameter (e.g. phi2)
    :param avg: average with standard-deviation (default: False)
    :param days: list with the days to plot (e.g. [1,3] for day 1 and 3)
    :returns: Plot
    """

    if df is None:
        raise Exception('No DataFrame selected.')

    alldays = int(np.ceil(df['time'].max()/24))

    for i in range(0, alldays):

        if (len(days) > 0) & (i+1 not in days):
            continue

        df_tmp = df[(df['time'].between(i * 24, i * 24 + 23.9))
                    ][['name', 'time', param]].dropna()

        fig, ax = plt.subplots(figsize=(8, 5))
        for strain in df['name'].unique():
            if avg:
                x = df_tmp[(df_tmp['name'] == strain)].groupby(
                    ['name', 'time'])['time']
                y = df_tmp[(df_tmp['name'] == strain)].groupby(
                    ['name', 'time'])[param]

                ax.errorbar(x.agg('mean'), y.agg('mean'),
                            yerr=y.agg('sem'), fmt='.:', markersize=10, capsize=4,
                            elinewidth=1, linewidth=.25, label=strain)
            else:
                ax.scatter(
                    df_tmp[df_tmp['name'] == strain]['time'],
                    df_tmp[df_tmp['name'] == strain][param],
                    label=strain
                )

        ax.set_title('Day {0}'.format(i+1))
        ax.set_xlabel('Time [h]')
        ax.set_ylabel(param)
        plt.legend()
        plt.tight_layout()
        plt.show()


def heatmap(df=None, param='', days=[], cmap=None):
    """Plot parameter as a heat map

    Plot a parameter as a phenotype-over-time heat map. Samples are avagered and represented as one row in the heat map.

    :param df: DataFrame
    :param param: Fluorescence based parameter (e.g. phi2)
    :param days: list with the days to plot (e.g. [1,3] for day 1 and 3)
    :param cmap: matplotlib colormap 
    :returns: Plot
    """
    alldays = int(np.ceil(df['time'].max()/24))
    strains = df['name'].unique()

    if len(days) == 0:
        days = range(1, alldays+1)

    if cmap is None:
        cmap = cm.rainbow

    fig, axes = plt.subplots(1, len(days), figsize=(
        12, (int(np.ceil(len(strains) / 3))) + 0.2), sharey=True)

    if len(days) > 1:
        ax = axes.flat
        a = 0

    ranges = []

    for i in range(0, alldays):

        if (len(days) > 0) & (i+1 not in days):
            continue

        df_range = df[(df['time'].between(0, i * 24 + 23.9))
                      ][['name', 'time', param]].dropna()

        ranges.append(df_range.groupby(['name', 'time'])[
                      param].agg('mean').dropna().min())
        ranges.append(df_range.groupby(['name', 'time'])[
                      param].agg('mean').dropna().max())

    ranges = np.array(ranges)

    for i in range(0, alldays):

        if (len(days) > 0) & (i+1 not in days):
            continue

        df_tmp = df[(df['time'].between(i * 24, i * 24 + 23.9))
                    ][['name', 'time', param]].dropna()

        heatmap = []

        for strain in strains:

            y = df_tmp[(df_tmp['name'] == strain)].groupby(
                ['name', 'time'])[param].agg('mean').dropna()

            heatmap.append(np.array(y))

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
    fig.subplots_adjust(bottom=0.2)

    # Create a new axis to contain the color bar
    cbar_ax = fig.add_axes([0.3, 0.05, 0.4, 0.05])
    norm = colors.Normalize(vmin=ranges.min(), vmax=ranges.max())
    plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap),
                 cax=cbar_ax, orientation='horizontal', label=param)

    plt.show()
