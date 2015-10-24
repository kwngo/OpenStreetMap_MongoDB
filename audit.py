import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "example.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "Way", "Crescent", "Treeway", "Hillway", "Terrace", "Roadway", "Willoway", "Circle", "West", "East", "South", "Collegeway", "Path", "Line", "Gateway", 'Sideline', 'Ridge', 'Hills', 'Woodmount', 'Kingsway', 'Wheelway', 'Heights', 'Hill', 'Gate', 'Oaks', 'Appleway', 'Baseline', 'Mews', 'Landing', 'Front', 'Laneway',  'Sound', 'EHS', 'Island', 'Coles', 'Keep', 'Shepway', 'Liteway', 'Islands', 'Passage', 'Olympia', 'Queensville', 'Robinway', 'Wynd', 'Valleyway', 'Meadoway', 'Broadway', 'George', 'Chase', 'Glen', 'End', 'Puslinch', 'Crestway', 'Italia', 'Alley', 'Bypass', 'Orange', 'Walk', 'Pathway', 'Run', 'Loft', 'Larkway', 'Rise', 'Park', 'Townline', 'Link', 'Ho', 'Chisholm', 'Wrenway', 'Grassway', 'Grove', 'Plaza', 'Mall', 'Green', 'Circuit', 'Tecumseth', 'Lanes', 'Loop', 'Tosorontio', 'Outlook', 'Taylor', 'Ldg', 'Parade', 'Glenn', 'Winegarden', 'Sideroad', 'Harbour', 'Romanoway', 'Woods', 'Blvd', 'Graham', 'Row', 'Cressent', 'Glenway', 'Cove', 'Amaranth', 'Cabotway', 'Forest', 'Sageway', 'Queensway', 'Crest', 'Meadows', 'Greenery', 'North', 'Downs', 'Driver', 'Vale', 'Adjala', 'Amici', 'Beeton', 'Fernway', 'Ames', 'Alliston', 'Homestead', 'Lawn', 'Ben', 'Golfway', 'Erindale', 'Walkway', 'Marinoway',  'Starway', 'Myrtleway', 'Concession', 'Round', 'Point', 'Millway', 'Byron', 'Esplanade', 'Hollow', 'Hts', 'Woodlands', 'Birchway', 'Oval', 'Close', 'Carseway', 'Greenway', 'Vista', 'Fairways', 'Floor', 'Keanegate', 'Field', 'Wood', 'Gingerway', 'Vineway', 'Valley', 'Villaway', 'Royalway', 'Mainway', 'Garden', 'Manor', 'Club', 'Dell', 'Dufferin', 'Promenade', 'Oakway', 'Briarway', 'Coachway', 'Gallery', 'Firway', 'Hawkway', 'Garafraxa', 'Westway', 'Glade', 'Trailway', 'Common', 'Crossing', 'Quay', 'Morning', 'Gardens', 'Cir', 'Roseway', 'Milburough', 'Bend', 'Avens', 'Campanile', 'Mossway', 'Thicket']

# UPDATE THIS VARIABLE
MAPPING = { "St": "Street",
            "street": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Rd.": "Road",
            "Cres.": "Crescent",
            "Pkwy": "Parkway",
            "Blvd": "Boulevard",
            "Dr": "Drive",
            "Hrbr": "Harbour",
            "W.": "West",
            "W": "West",
            "N": "North",
            "N.": "North",
            "S": "South",
            "S.": "South",
            "E": "East",
            "E.": "East"
            }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types

def update_name(name, mapping=MAPPING):
    words = name.split(" ")
    road_names = words[1:]

    # update street names
    for road_name, i in enumerate(road_names):
        if road_name in mapping.keys():
            words[i] = mapping[road_name]

    return " ".join(words)

if __name__ == "__main__":
    audit('sample_toronto.osm')
