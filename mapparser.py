"""
We use iterative parsing to process the map file and find out what and how many tags there are, in order to get a feeling of
how of which data we can expect in our map.
"""

import xml.etree.cElementTree as ET
import pprint

def count_tags(filename):
    tags = {}
    for event, elem in ET.iterparse(filename):
        if elem.tag in tags.keys():
            tags[elem.tag] += 1
        else:
            tags[elem.tag] = 1
    print tags
    return tags

if __name__ == "__main__":
    count_tags('sample_toronto.osm')
