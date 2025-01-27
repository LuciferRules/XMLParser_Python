import xml.etree.ElementTree as ET
from collections import defaultdict

def main():
    # Call read_xml with file paths
    read_xml("test-data/PDBSESE174/E142_STRIPMAP_VC339684G09_3138096870_PDBSESE174_20240130T122947+08.xml")
    print("-" * 30)
    read_xml("test-data/PDBSESE174/E142_STRIPMAP_VC339684G09_3138096869_PDBSESE174_20240130T123000+08.xml")

def read_xml(file_path):
    try:
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        namespace = {'ns': 'urn:semi-org:xsd.E142-1.V1005.SubstrateMap'}

        # Step 2: Get all SubstrateMap elements
        substrate_maps = root.findall(".//ns:SubstrateMap", namespace)
        print(len(substrate_maps))
        for substrate_map in substrate_maps:
            substrate_type = substrate_map.attrib.get("SubstrateType", "")
            substrate_id = substrate_map.attrib.get("SubstrateId", "")
            print(f"SubstrateType: {substrate_type}")
            print(f"SubstrateId: {substrate_id}")

        # Step 3: Find Wafer ID
        transfer_maps = root.findall(".//ns:TransferMap", namespace)
        print(len(transfer_maps))
        for transfer_map in transfer_maps:
            print(transfer_map.attrib.get("FromSubstrateType", ""))  # Wafer
            print(transfer_map.attrib.get("FromSubstrateId", ""))    # VC339684.05

        # Step 4: Find T elements and count
        t_elements = root.findall(".//ns:T", namespace)
        print(f"T length: {len(t_elements)}")
        for t_map in t_elements:
            fx = t_map.attrib.get("FX", "")
            fy = t_map.attrib.get("FY", "")
            tx = t_map.attrib.get("TX", "")
            ty = t_map.attrib.get("TY", "")
            print(f"FX: {fx} FY: {fy} TX: {tx} TY: {ty}")

        # Find unique TX and TY combinations
        find_unique_tx_ty(t_elements)

    except Exception as e:
        print(f"Unexpected error occurred while reading XML file: {e}")

def find_unique_tx_ty(t_elements):
    # Create a dictionary to store unique TX and TY combinations and their counts
    tx_ty_counts = defaultdict(int)

    for t_map in t_elements:
        tx = t_map.attrib.get("TX", "")
        ty = t_map.attrib.get("TY", "")
        key = f"{tx}_{ty}"
        tx_ty_counts[key] += 1

    # Print the counts
    for key, count in tx_ty_counts.items():
        tx, ty = key.split("_")
        print(f"TX: {tx}, TY: {ty}, Count: {count}")

    # Print the total number of unique TX and TY combinations
    print(f"Total unique TX and TY combinations: {len(tx_ty_counts)}")

if __name__ == "__main__":
    main()
