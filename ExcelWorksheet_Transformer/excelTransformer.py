import sys

def data_to_csv(data, filename):
    """
    Converts a dictionary of data into a CSV file suitable for Tableau Desktop.

    Args:
      data: A dictionary where keys are column names and values are lists of data.
      filename: The name of the output CSV file (default: 'tableau_data.csv').
    """

    with open(filename, 'w', newline='') as csvfile:
        # Write the header row
        header = ','.join(data.keys()) + '\n'
        csvfile.write(header)
        csvfile.write('FX, FY \n')

        # Write the data rows
        for row in zip(*data.values()):
            row_str = ','.join(str(value) for value in row) + '\n'
            # Remove ( ) from tuples
            row_str = row_str.replace('(', '').replace(')', '')
            # print(row_str)
            csvfile.write(row_str)

# Example usage:
# data = {'VC339684.05': [(14, 55), (14, 53), (14, 51), (14, 50), (14, 49), (14, 48), (14, 47), (14, 46), (14, 44), (14, 43), (14, 42), (14, 41), (14, 45), (14, 40), (14, 39), (14, 38), (14, 37), (14, 36), (14, 35), (14, 34), (14, 33), (14, 32), (14, 31), (14, 30), (14, 29), (14, 28), (14, 27), (14, 26), (14, 25), (14, 23), (14, 22), (14, 21)]}
# data_to_csv(data)