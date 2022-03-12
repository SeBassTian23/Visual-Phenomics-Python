"""
Get info from the DataFrame with Visual Phenomics data. 
"""


def info(df=None):
    """Print DataFrame Information.

    :param df: DataFrame
    """

    if df is None:
        raise Exception('No DataFrame selected.')

    df.info(memory_usage='deep')


def samples(df=None):
    """List with unique sample names from the DataFrame.

    :param df: DataFrame
    :returns: unique sample names (list)
    """

    if df is None:
        raise Exception('No DataFrame selected.')

    return df['name'].unique()


def description(df=None):
    """Description of the experiments content.

    :param df: DataFrame
    """

    if df is None:
        raise Exception('No DataFrame selected.')

    light = 'n/a'
    if 'light_intensity' in df:
        light = df['light_intensity'].max()

    description = 'The current DataFrame contains {0} experiment(s) with {1} sample(s) of {2} individual lines. The duration of the experiment was {4} hours ({5} day(s)) with a maximum light intensity of {6} uE.\n\n# Lines: {3}\n\n# Experiments:\n{7}'.format(
        len(df['experiment'].unique()),
        len(df['sample'].unique()),
        len(df['name'].unique()),
        ", ".join(sorted(df['name'].unique().tolist(), key=str.casefold)),
        df['time'].max(),
        (df['time'].max()/24),
        light,
        "\n".join(
            sorted(df['experiment'].unique().tolist(), key=str.casefold)),
    )
    print(description)
