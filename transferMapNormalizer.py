# called_script.py
import sys
import os
import xml.etree.ElementTree as ET
from ExcelWorksheet_Transformer.excelTransformer import data_to_csv


def read_transferMap(file_path):
    """
    Reads TransferMap elements from an XML file and extracts their coordinates.

    Args:
        file_path: Path to the XML file.

    Returns:
        A dictionary where keys are FromSubstrateId names and values are tuples of (FX, FY) coordinates.
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        namespace = {'ns': 'urn:semi-org:xsd.E142-1.V1005.SubstrateMap'}

        # dict
        waferCoordinatesMap = {}
        for TransferMap in root.findall(".//ns:TransferMap", namespace):
            FromSubstrateId = TransferMap.attrib.get("FromSubstrateId", "")
            waferCoordinatesMap[FromSubstrateId] = []  # Initialize as a list to store multiple coordinates

            for T in TransferMap.findall(".//ns:T", namespace):
                x = int(T.attrib.get("FX", 0))
                y = int(T.attrib.get("FY", 0))
                waferCoordinatesMap[FromSubstrateId].append((x, y))

        return waferCoordinatesMap

    except Exception as e:
        print(f"Error reading XML file: {e}")
        return {}

def normalize_transferMap(rawWaferCoordinatesMap, offsetX, offsetY):
    """
    Normalizes the transfer map coordinates by subtracting the specified offsets.

    Args:
        rawWaferCoordinatesMap: A dictionary containing raw transfer map coordinates.
        offsetX: The X-axis offset to be applied.
        offsetY: The Y-axis offset to be applied.

    Returns:
        A new dictionary containing the normalized transfer map coordinates.
    """

    # Create a new dictionary to store normalized coordinates
    normalizedWaferCoordinatesMap = {}

    # Iterate through each key-value pair in the raw data
    for key, coordinates_list in rawWaferCoordinatesMap.items():
        normalized_coordinates = []
        for x, y in coordinates_list:
            transformed_x = x - offsetX
            transformed_y = y - offsetY
            normalized_coordinates.append((transformed_x, transformed_y))
        normalizedWaferCoordinatesMap[key] = normalized_coordinates

    return normalizedWaferCoordinatesMap

def extract_strip_id(file_path):
    """
    Extracts the strip ID from the given file path.

    Args:
      file_path: The path to the file.

    Returns:
      The extracted strip ID, or None if it cannot be found.
    """
    try:
        file_name = os.path.basename(file_path)
        parts = file_name.split("_")
        strip_id = parts[3]
        return strip_id
    except IndexError:
        return None


# Retrieve the arguments passed from the caller script
arg1 = sys.argv[1] # file_path
arg2 = sys.argv[2] # offsetX
arg3 = sys.argv[3] # offsetY
print(f"arg1= {arg1}:")
print(f"arg2= {arg2}")
print(f"arg3= {arg3}")

# min_offset (X, Y), convert to integer
if len(arg2) | len(arg3):
    offsetX = int(arg2)
    offsetY = int(arg3)
else:
    offsetX = 0
    offsetY = 0

# read transferMap and normalize
nonNormalizedWaferCoordinatesMap= read_transferMap(arg1)
normalizedWaferCoordinatesMap= normalize_transferMap(nonNormalizedWaferCoordinatesMap, offsetX, offsetY)
print(f"Before normalized: {nonNormalizedWaferCoordinatesMap}")
print(f"After normalized: {normalizedWaferCoordinatesMap}")

# read strip id from filename
stripId = extract_strip_id(arg1)
print(f"stripID= {stripId}")

# write to csv file
# get key from normalizedWaferCoordinatesMap
waferId = list(normalizedWaferCoordinatesMap.keys())[0]
print(f"waferID= {waferId}")
data_to_csv(normalizedWaferCoordinatesMap, f"output/{stripId}_{waferId}_tableau_data.csv")
print(f"normalizedWaferCoordinatesMap written into output/{stripId}_{waferId}_tableau_data.csv file")