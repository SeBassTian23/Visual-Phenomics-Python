"""
Get info from the DataFrame with Visual Phenomics data. 
"""

import pkg_resources

def info(df=None):
    """Print DataFrame Information.

    :param df: DataFrame
    """

    if df is None:
        raise Exception('No DataFrame selected.')

    df.info(memory_usage='deep')


def samples(df=None):
    """List with unique sample names from the DataFrame.

    Requires the columns 'name'.

    :param df: DataFrame
    :returns: unique sample names (list)
    """

    if df is None:
        raise Exception('No DataFrame selected.')
    
    if 'name' not in df:
        raise Exception('Column "name" not found.')

    return df['name'].unique()


def description(df=None):
    """Description of the experiments content.

    Requires the columns 'experiment', 'sample', 'name', and 'time'.

    :param df: DataFrame
    """

    if df is None:
        raise Exception('No DataFrame selected.')
    
    if 'name' not in df:
        raise Exception('Column "name" not found.')
    
    for col in ['experiment','sample','name', 'time']:
        if col not in df:
            raise Exception('Column "%s" is required but not found.' % col)

    light = 'n/a'
    if 'light_intensity' in df:
        light = df['light_intensity'].max()

    folders = ""
    if 'folder' in df:
        folders = ", combined from {0} folder(s) [{1}]".format(len(df['folder'].unique()), ", ".join(df['folder'].unique().tolist()))

    description = 'The current DataFrame contains {0} experiment(s) with {1} sample(s) of {2} individual lines{8}. The duration of the experiment was {4} hours ({5} day(s)) with a maximum light intensity of {6} uE.\n\n# Lines:\n{3}\n\n# Experiments:\n{7}'.format(
        len(df['experiment'].unique()),
        len(df['sample'].unique()),
        len(df['name'].unique()),
        ", ".join(sorted(df['name'].unique().tolist(), key=str.casefold)),
        df['time'].max(),
        (df['time'].max()/24),
        light,
        ", ".join(
            sorted(df['experiment'].unique().tolist(), key=str.casefold)),
        folders
    )
    print(description)


def version():
    """Return Package Version
    """
    return pkg_resources.require("visual_phenomics_py")[0].version