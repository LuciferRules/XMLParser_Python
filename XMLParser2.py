def main():
    # Call read_xml with file paths
    read_xml("test-data/PDBSESE174/E142_STRIPMAP_VC339684G09_3138096870_PDBSESE174_20240130T122947+08.xml")
    print("-" * 30)
    read_xml("test-data/PDBSESE174/E142_STRIPMAP_VC339684G09_3138096869_PDBSESE174_20240130T123000+08.xml")

def read_xml(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()

        # Step 2: Get SubstrateMap elements
        substrate_maps = find_elements(content, "SubstrateMap")
        print(len(substrate_maps))
        for element in substrate_maps:
            substrate_type = extract_attribute(element, "SubstrateType")
            substrate_id = extract_attribute(element, "SubstrateId")
            print(f"SubstrateType: {substrate_type}")
            print(f"SubstrateId: {substrate_id}")

        # Step 3: Get TransferMap elements
        transfer_maps = find_elements(content, "TransferMap")
        print(len(transfer_maps))
        for element in transfer_maps:
            from_type = extract_attribute(element, "FromSubstrateType")
            from_id = extract_attribute(element, "FromSubstrateId")
            print(from_type)
            print(from_id)

        # Step 4: Get T elements
        t_elements = find_elements(content, "T")
        print(f"T length: {len(t_elements)}")
        for element in t_elements:
            fx = extract_attribute(element, "FX")
            fy = extract_attribute(element, "FY")
            tx = extract_attribute(element, "TX")
            ty = extract_attribute(element, "TY")
            print(f"FX: {fx} FY: {fy} TX: {tx} TY: {ty}")

        # Pass t_elements to find_unique_tx_ty
        find_unique_tx_ty(t_elements)

    except Exception as e:
        print(f"Unexpected error occurred while reading XML file: {e}")

def find_elements(content, tag):
    """Find all elements with a specific tag in the XML content."""
    start_tag = f"<{tag} "
    end_tag = "/>"
    elements = []
    pos = 0

    while True:
        start_pos = content.find(start_tag, pos)
        if start_pos == -1:  # No more elements
            break

        end_pos = content.find(end_tag, start_pos)
        if end_pos == -1:  # Malformed tag, end tag missing
            print(f"Error: Missing end tag for '{tag}'")
            break

        end_pos += len(end_tag)  # Include the closing "/>"
        elements.append(content[start_pos:end_pos])
        pos = end_pos  # Update the position for the next search

    return elements


def extract_attribute(element, attribute):
    """Extract the value of a specific attribute from an XML element."""
    attr_pos = element.find(attribute + "=")
    if attr_pos == -1:
        return None  # Attribute not found

    # Locate the value, which is enclosed in double quotes
    start_pos = element.find('"', attr_pos) + 1
    end_pos = element.find('"', start_pos)
    if start_pos == 0 or end_pos == -1:
        return None  # Malformed attribute
    return element[start_pos:end_pos]


def find_unique_tx_ty(t_elements):
    """Find unique combinations of TX and TY from a list of <T> elements."""
    print(f"Total <T> elements found: {len(t_elements)}")

    unique_combinations = set()

    for element in t_elements:
        fx = extract_attribute(element, "FX")
        fy = extract_attribute(element, "FY")
        tx = extract_attribute(element, "TX")
        ty = extract_attribute(element, "TY")

        if fx and fy and tx and ty:
            print(f"FX: {fx}, FY: {fy}, TX: {tx}, TY: {ty}")
            unique_combinations.add((tx, ty))

    print(f"Total unique TX and TY combinations: {len(unique_combinations)}")
    print(f"Unique TX and TY combinations: {unique_combinations}")


if __name__ == "__main__":
    main()
