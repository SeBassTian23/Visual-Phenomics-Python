"""
Creates accessible dataframes from DEPI data files saved by Visual Phenomics.
"""

import csv
from numpy import nan, isnan, ceil
import os
import pandas as pd
import re


def dataframe(path=None, prefix=None):
    """Build DataFrame from Visual Phenomics output.

    Get a DataFrame for an Experiment from a set of text files with calculated parameters.

    :param path: the path to the directory with calulated parameter text files
    :returns: a dataframe containing parameters from all files
    :raises Exception: if the path is invalid or the data is malformed
    """

    if path is None:
        raise Exception('Path not defined.')

    paths = []
    if isinstance(path, str):
        paths.append(path)

    elif isinstance(path, list):
        paths += path

    for idx, p in enumerate(paths):
        files = os.listdir(p)

        dfheader = ['sample', 'name', 'time', 'light_intensity']
        dfbody = []
        dfdict = {}
        dflightint = {}

        for f in files:

            if prefix is None:
                prefix = r'^all'
            else:
                prefix = r'{0}'.format(prefix)

            file_name = re.sub(prefix, '', os.path.splitext(f)[0], 1)
            file_ext = os.path.splitext(f)[1]
            if file_ext == '.txt':
                # opening the CSV file
                with open(p+f, mode='r') as file:

                    # reading the CSV file
                    csvFile = csv.DictReader(file, delimiter='\t')

                    # define possible sample header column names
                    sampleNameHeader = 'name[position][flat][experiment][camera][replicate]'
                    sampleNameHeaderOld = 'name[flat][experiment][camera][replicate]'

                    # Get the header from the first column
                    sampleNameHeaderUse = str(csvFile.fieldnames[0])

                    # New Header format
                    if (sampleNameHeader in csvFile.fieldnames):
                        sampleNameHeaderUse = sampleNameHeader

                    # Old sample header format
                    elif (sampleNameHeader not in csvFile.fieldnames) & (sampleNameHeaderOld in csvFile.fieldnames):
                        sampleNameHeaderUse = sampleNameHeaderOld

                    # Not matching the standard header format
                    else:
                        print('File "{0}" does not support the standard annotation format, falling back to simple import.'.format(f))

                    # add column header
                    dfheader.append(file_name)

                    # looping through the rows in the csv file
                    for lines in csvFile:

                        # get the sample name
                        sample = lines[sampleNameHeaderUse]

                        # if the sample name is empty or null, skip the row
                        if (sample[0] == '[') or (re.match(r'^null', sample)):
                            continue

                        # get all items
                        for key, value in lines.items():

                            # Skip the first row
                            if (key == sampleNameHeaderUse):
                                continue

                            if (sample == '*light_intensity'):

                                # check if time value is a number or nan
                                try:
                                    value = float(value)
                                except:
                                    value = nan

                                if str(key) not in dflightint:
                                    dflightint[str(key)] = value

                                elif isnan(dflightint[str(key)]) & ~isnan(value):
                                    dflightint[str(key)] = value

                                continue

                            # Create a dict entry for sample+time if it doesn't exist
                            if sample+key not in dfdict:

                                if (sampleNameHeader in csvFile.fieldnames) | (sampleNameHeaderOld in csvFile.fieldnames):
                                    meta = re.findall(
                                        r"\[(.*?)\]", sample)

                                    # Some samples seem to miss the position
                                    if len(meta) == 4:
                                        meta.insert(0, "n/a")
                                    if meta[0] == '':
                                        meta[0] = "n/a"

                                    dfdict[sample+key] = {'name': sample.split('[')[0], 'sample': sample, 'light_intensity': nan, 'time': float(
                                        key), 'position': meta[0], 'flat': meta[1], 'experiment': meta[2], 'camera': meta[3], 'replicate': meta[4]}

                                else:
                                    dfdict[sample+key] = {'name': sample, 'sample': sample, 'light_intensity': nan, 'time': float(key)}

                            # Add nan if float value parsing fails
                            try:
                                dfdict[sample +
                                        key][file_name] = float(value)
                            except:
                                dfdict[sample+key][file_name] = nan

        dfheader += ['position', 'flat',
                     'experiment', 'camera', 'replicate']

        for row in dfdict:
            if 'light_intensity' in dfdict[row]:
                if str(dfdict[row]['time']) in dflightint:
                    dfdict[row]['light_intensity'] = dflightint[str(
                        dfdict[row]['time'])]
            dfbody.append(dfdict[row])

        dfTMP = pd.DataFrame(dfbody, columns=dfheader)

        # Change specific columns to category type to save memory
        categories = ['name', 'sample', 'position', 'flat', 'experiment', 'camera', 'replicate']

        # Add folder column and category
        if len(paths) > 1:
            dfTMP['folder'] = p
            categories += ['folder']

        dfTMP[categories] = dfTMP[categories].astype("category")

        for col in list(dfTMP):
            if dfTMP[col].dropna().size == 0:
                dfTMP.drop(col, axis=1, inplace=True)
                print('Empty column "{0}" was dropped'.format(col))

        # Add initial dataframe or append if multiple are present
        if idx == 0:
            df = dfTMP
        else:
            df = pd.concat([df, dfTMP], sort=False, ignore_index=True)

        # Get the maximum number of days from the experiment time
        days = int( ceil( df['time'].max() / 24 ) )
        if df['time'].max() % 24 == 0:
            days = days + 1

        ## Fill columns with NaN to start with
        df['day'] = nan
        df['hours_day'] = nan

        ## Go through data by day
        for col in range(0, days):
            ## unique times for the day
            times = df[(df['time'] >= col * 24) & (df['time'] < col * 24 +24)]['time'].unique()
            for row in df[(df['time'] >= col * 24) & (df['time'] < col * 24 +24)].itertuples():
                ## Add day
                df.at[row.Index, 'day'] = int(col+1)
                ## Add day_hour
                df.at[row.Index, 'hours_day'] = round( getattr(row, 'time') - (col * 24), 4 )

    return df


def save(df=None, path=None, compress='zip'):
    """Save current DataFrame

    Save the current DataFrame in the pickle format to avoid re-import and re-calculations.

    :param df: DataFrame
    :param path: the path to the directory where the DataFrame is saved (as dataframe.pkl).
    :param compression: Compression algorithm (default: zip)
    """

    if df is None:
        raise Exception('No DataFrame selected.')

    if path is None or path == '':
        raise Exception('Path not defined.')

    if not os.path.exists(path):
        os.makedirs(path)

    filepath = os.path.join(path, 'dataframe.pkl')

    df.to_pickle(filepath, compression=compress)


def load(filepath=None, compress='zip'):
    """Read saved DataFrame

    Read a saved DataFrame from file. If you have selected a specific compression to save the DataFrame, make sure to provide the same when loading the DataFrame

    :param df: DataFrame
    :param path: the path to the file with the saved DataFrame.
    :param compression: Compression algorithm (default: zip)
    :returns: Dataframe
    """

    if filepath is None or filepath == '':
        raise Exception('Filepath not defined.')

    if not os.path.exists(filepath):
        raise Exception('Filepath provided does not exist.')

    return pd.read_pickle(filepath, compression=compress)
