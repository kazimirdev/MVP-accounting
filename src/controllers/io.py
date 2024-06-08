from lxml import etree


# Function to parse the XML file
def parse_xml(file_path: str) -> etree.ElementTree:
    return etree.parse(file_path)


# Function to write to the XML file
def write_xml(tree: etree.ElementTree, file_path: str) -> None:
    tree.write(file_path, pretty_print=True, xml_declaration=True, encoding='UTF-8')


def next_gen_id(elements, type_element: str):
    max_id = 0
    if type_element not in ("Account",
                            "Transaction"):
        return max_id
    for elem in elements.findall(type_element):
        elem_id = int(elem.findtext(f'{type_element}ID'))
        if elem_id >= max_id:
            max_id = elem_id + 1
    return max_id
