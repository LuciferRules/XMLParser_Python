import xml.etree.ElementTree as ET
# caller_script.py
import subprocess

def read_reference_devices(file_path):
    """
    Reads ReferenceDevice elements from an XML file and extracts their coordinates.

    Args:
        file_path: Path to the XML file.

    Returns:
        A dictionary where keys are ReferenceDevice names and values are tuples of (X, Y) coordinates.
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        namespace = {'ns': 'urn:semi-org:xsd.E142-1.V1005.SubstrateMap'}

        # dict
        reference_devices = {}
        for device in root.findall(".//ns:ReferenceDevice", namespace):
            name = device.attrib.get("Name", "")
            coordinates = device.find(".//ns:Coordinates", namespace)
            if coordinates is not None:
                x = int(coordinates.attrib.get("X", 0))
                y = int(coordinates.attrib.get("Y", 0))
                reference_devices[name] = (x, y)

        return reference_devices

    except Exception as e:
        print(f"Error reading XML file: {e}")
        return {}

def calculate_offset(ref_dies, wafer_dies):
    """
    Calculates the offset (offsetX, offsetY) based on the closest reference die.

    Args:
        ref_dies: A list of tuples, where each tuple represents the coordinates
               of a reference die (e.g., [(7, 9), (33, 9)]).
        wafer_dies: A list of tuples, where each tuple represents the coordinates
               of the wafer die.

    Returns:
        A tuple containing the calculated offsetX and offsetY.
    """
    min_dist = float('inf')  # Initialize with infinity
    min_offset = (0, 0)  # Initialize with default offset
    for wafer_die in wafer_dies:
        for ref_die in ref_dies:
            dist = abs(wafer_die[0] - ref_die[0]) + abs(wafer_die[1] - ref_die[1])
            if dist < min_dist:
                min_dist = dist
                min_offset = (ref_die[0] - wafer_die[0], ref_die[1] - wafer_die[1])

    return min_offset


if __name__ == "__main__":
    file_paths = [
        "test-data/VE337661G01/E142_STRIPMAP_MKZ.20240712.072648.402861892/E142_STRIPMAP_VE337661G01_3308922737_ESW001_20240712T152317+08.xml",
        "test-data/VE337661G01/E142_STRIPMAP_MKZ.20240712.075619.729757635/E142_STRIPMAP_VE337661G01_3308922734_ESW001_20240712T152626+08.xml",
        "test-data/PDBSESE174/E142_STRIPMAP_VC339684G09_3138096869_PDBSESE174_20240130T123000+08.xml"
    ]

    for file_path in file_paths:
        UWMRefDieArray = []
        # Call the read_reference_devices function
        reference_devices = read_reference_devices(file_path)
        if reference_devices:
            print(f"Reference Devices in {file_path}:")
            for name, coords in reference_devices.items():
                tupleCoord = (coords[0], coords[1])  # Create a tuple directly
                print(f"  {name}: X={coords[0]}, Y={coords[1]}")
                UWMRefDieArray.append(tupleCoord)

        # Call the calculate_offset function
        # Define WaferDie coordinates
        WaferDie1 = (40, 13) # TODO: modify
        WaferDie2 = (6, 7)
        WaferDieArray = []
        WaferDieArray.append(WaferDie1)
        WaferDieArray.append(WaferDie2)

        if len(UWMRefDieArray):
            print(f"UWMRefDieArray= {UWMRefDieArray}")

            # Calculate Minimum offset for WaferDie
            min_offset = calculate_offset(UWMRefDieArray, WaferDieArray)
            print(f"Minimum offset for WaferDie: {min_offset}")

        # Call transferMapNormalizer.py only once after processing all files
        subprocess.run(["python", "transferMapNormalizer.py", file_path])
        print("-" * 30)
