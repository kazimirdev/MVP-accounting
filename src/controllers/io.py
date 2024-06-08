from lxml import etree


# Function to parse the XML file
def parse_xml(file_path: str) -> etree.ElementTree:
    return etree.parse(file_path)


# Function to write to the XML file
def write_xml(tree: etree.ElementTree, file_path: str) -> None:
    tree.write(file_path, pretty_print=True, xml_declaration=True, encoding='UTF-8')
