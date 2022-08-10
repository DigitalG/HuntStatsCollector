import json
import xml.etree.ElementTree as ET

from steampath import get_steam_path

steam_path = get_steam_path()

xml_data_path = f"{steam_path}\\steamapps\\common\\Hunt Showdown\\user\\profiles\\default\\attributes.xml"


root = ET.parse(xml_data_path).getroot()
for tag in root.findall("Attr[starts-with(@name, 'MissionBag')]"):
    print(tag)