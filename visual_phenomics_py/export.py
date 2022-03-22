"""
Export data from the DataFrame into the Visual Phenomics 
text file format
"""

import os
import csv


def to_txt(df=None, folder=None, cols=[]):
    """Export DataFrame as text files.

    Each column of the DataFrame gets exported as a tab separated file.
    The first column in each file contains the sample information.
    The first row in each file contains the column headers. The column 
    headers are the timeing information as well.
    The last row contains the light intensity if available.

    :param df: DataFrame
    """

    if df is None:
        raise Exception('No DataFrame selected.')

    if folder is None:
        raise Exception('No output folder selected.')

    # Get parameters for files
    df_columns = df.columns.values.tolist()
    to_ignore = ['sample', 'name', 'position', 'flat', 'experiment',
                 'camera', 'replicate', 'time', 'light_intensity']

    # Test if all the custom columns exist
    if len(cols) > 0:

        # Test if any of the ignored columns are selected
        if not set(cols).isdisjoint(to_ignore):
            not_ignored = []
            for i in cols:
                if i in to_ignore:
                    not_ignored.append(i)
            raise Exception("The following column(s) cannot be exported: {0}.".format(
                ", ".join(not_ignored)))

        # Test if any of the selected columns not exist
        if len(set(cols).intersection(df_columns)) < len(cols):
            unknwown = []
            for i in cols:
                if i not in df_columns:
                    unknwown.append(i)
            raise Exception("The following column(s) cannot be found in the DataFrame: {0}.".format(
                ", ".join(unknwown)))

        # Overwrite all columns with selected ones
        df_columns = cols

    # first column header
    csv_first_column = 'name[position][flat][experiment][camera][replicate]'

    # Make sure folder exists, otherwise create it
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Lookup Table for light intensities by time
    light_and_times = {}

    for idx, row in df[['time', 'light_intensity']].drop_duplicates().iterrows():
        light_and_times[str(row['time'])] = row['light_intensity']

    # Loop through column names
    for column in df_columns:

        # Skip columns that need to be excluded
        if column in to_ignore:
            continue

        # Get the correct number of timepoints for each parameter
        csv_times = df.dropna(subset=[column]).sort_values(
            by='time')['time'].unique()

        # Build header with the correct number of timepoints
        csv_column_names = np.append([csv_first_column], csv_times)

        # Build the light intensity row based on the timepoints
        light_intensity_row = {}
        for name in csv_column_names:
            if name == csv_first_column:
                light_intensity_row[csv_first_column] = '*light_intensity'
            else:
                light_intensity_row[str(name)] = light_and_times[str(name)]

        # Build filepath and filename
        output_filename = os.path.join(folder, 'all{0}.txt'.format(column))

        # Open file and start writing
        with open(output_filename, 'w') as f:

            # Setup CSV writer
            writer = csv.DictWriter(
                f, fieldnames=csv_column_names, quoting=csv.QUOTE_NONE, delimiter='\t')

            # Write header column
            writer.writeheader()

            # Sample row list
            sample_rows = []

            # Write rows
            for sample in df['sample'].unique():

                sample_row = {}

                cols_df = ['sample', 'time', 'name', 'position',
                           'flat', 'experiment', 'camera', 'replicate', column]

                for row in df[df['sample'] == sample].dropna(subset=[column])[cols_df].itertuples():

                    # Add first column sample identifier
                    if csv_first_column not in sample_row:
                        first_col = "{0}[{1}][{2}][{3}][{4}][{5}]".format(
                            getattr(row, 'name'),
                            getattr(row, 'position'),
                            getattr(row, 'flat'),
                            getattr(row, 'experiment'),
                            getattr(row, 'camera'),
                            getattr(row, 'replicate')
                        )

                        sample_row[csv_first_column] = first_col

                    # Add time and datapoint
                    value = getattr(row, column)
                    if value == 'nan' or value == '':
                        value = 'NaN'
                    sample_row[str(getattr(row, 'time'))] = value

                # Add row to csv
                if sample_row:

                    # Check if all times exist and fill up accordingly
                    for i in csv_times:
                        if str(i) not in sample_row:
                            sample_row[str(i)] = 'NaN'

                    sample_rows.append(sample_row)

            # Write Data rows
            writer.writerows(sample_rows)

            # Add row with light intensities
            writer.writerow(light_intensity_row)
