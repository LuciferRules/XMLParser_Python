1. Git control
$ git remote add origin https://github.com/LuciferRules/XMLParser_Python.git

$ git branch -M master

$ git commit -m "first commit"

$ git push -u origin master

2. Program flow
a) readReferenceDevice.py: read_reference_devices reads ReferenceDevice elements from an XML file and extracts their coordinates.
eg. UWMRefDie1: X=7, Y=9
    UWMRefDie2: X=33, Y=9
    UWMRefDieArray= [(7, 9), (33, 9)]

b) readReferenceDevice.py: calculate_offset calculates the offset (offsetX, offsetY) based on the closest reference die.
                            Please modify the WaferDie1 and WaferDie2 coordinates accordingly.
eg. Minimum offset for WaferDie: (1, 2)

c) readReferenceDevice.py: call subprocess transferMapNormalizer.py with arguments file_path, offsetX, offsetY.

d) transferMapNormalizer.py: read_transferMap reads a transfer map and normalize_transferMap normalizes the coordinates using offsetX, offsetY.
eg. Before normalized: {'VE337661.04': [(26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0), (26, 0)]}
    After normalized: {'VE337661.04': [(25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2), (25, -2)]}

e) transferMapNormalizer.py: extract_strip_id extracts the strip ID from the given file path.
eg. stripID= 3308922737

f) transferMapNormalizer.py: data_to_csv writes the normalized transfer map to a CSV file.
eg. normalizedWaferCoordinatesMap written into output/3308922737_VE337661.04_tableau_data.csv file
