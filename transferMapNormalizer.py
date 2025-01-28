# called_script.py
import sys
import os
import xml.etree.ElementTree as ET


def read_transferMap(file_path):
    """
    Reads ReferenceDevice elements from an XML file and extracts their coordinates.

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


# Retrieve the arguments passed from the caller script
arg1 = sys.argv[1]
print(f"{arg1}:")

# Calculate offset
offsetX = 1
offsetY = 1

nonNormalizedWaferCoordinatesMap= read_transferMap(arg1)
normalizedWaferCoordinatesMap= normalize_transferMap(nonNormalizedWaferCoordinatesMap, offsetX, offsetY)
print(f"Before normalized: {nonNormalizedWaferCoordinatesMap}")
print(f"After normalized: {normalizedWaferCoordinatesMap}")