"""
Creates accessible dataframes from DEPI data files saved by Visual Phenomics.
"""

import csv
from numpy import nan
import os
import pandas as pd
import re

def build_dataframe(path=None):
  """
  Get a DataFrame for an Experiment from a set of text files with calculated parameters.

  :param path: the path to the directory with calulated parameter text files
  :returns: a dataframe containing parameters from all files
  :raises Exception: if the path is invalid or the data is malformed
  """
  if path is not None:

    paths = []
    if isinstance(path, str):
      paths.append(path)

    elif isinstance(path, list):
      paths += path

    for p in paths:
      files = os.listdir(p)

      dfheader = ['sample', 'name', 'time', 'light_intensity']
      dfbody = []
      dfdict = {}
      dflightint = {}

      for f in files:
        file_name = re.sub(r'^all', '', os.path.splitext(f)[0], 1)
        file_ext = os.path.splitext(f)[1]
        if file_ext == '.txt':
          # opening the CSV file
          with open(p+f, mode ='r') as file:   
              
            # reading the CSV file
            csvFile = csv.DictReader(file, delimiter='\t')

            # add column header
            dfheader.append(file_name)
      
            # looping through the rows in the csv file
            for lines in csvFile:

              # get the sample name
              sample = lines['name[position][flat][experiment][camera][replicate]']
              
              # get all items
              for key, value in lines.items():

                # Skip the first row
                if (key == 'name[position][flat][experiment][camera][replicate]'):
                  continue

                if (sample == '*light_intensity'):
                  if key not in dflightint or dflightint[key] is nan:
                    try:
                      dflightint[key] = float(value)
                    except:
                      dflightint[key] = nan
                  continue

                # Create a dict entry for sample+time if it doesn't exist
                if sample+key not in dfdict:
                  meta = re.findall(r"(?<=\[).*?(?=\])", sample)
                  dfdict[sample+key] = { 'name': sample.split('[')[0], 'sample': sample, 'light_intensity': nan, 'time': float(key), 'position': meta[0], 'flat': meta[1], 'experiment': meta[2], 'camera': meta[3], 'replicate': meta[4] }

                dfdict[sample+key][file_name] = float(value)

      dfheader += ['position', 'flat', 'experiment', 'camera', 'replicate']

      for row in dfdict:
        if 'light_intensity' in dfdict[row]:
          dfdict[row]['light_intensity'] = dflightint[str(dfdict[row]['time'])]
        dfbody.append(dfdict[row])

      df = pd.DataFrame(dfbody, columns=dfheader)
      df[['name', 'sample', 'position', 'flat', 'experiment', 'camera', 'replicate']] = df[['name', 'sample', 'position', 'flat', 'experiment', 'camera', 'replicate']].astype("category")

      for col in list(df):
        if df[col].dropna().size == 0:
          df.drop(col, axis=1, inplace=True)
      
      return df
  else:
    print('Path not defined')
    return None