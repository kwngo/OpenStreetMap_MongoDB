import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
import audit

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
is_address = re.compile(r'addr:')
is_street = re.compile(r'addr:street')
second_colon = re.compile(r'^addr:\w+:\w+$')

def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        # YOUR CODE HERE
        node["id"] = element.get("id")
        node["type"] = element.tag

        if element.get('visible') is not None: node['visible'] = element.get('visible')

        if element.get("lat") and element.get("lon"):
           node["pos"] = [float(element.get("lat")), float(element.get("lon"))]

        node["created"] = { "version": element.get("version"), "changeset": element.get("changeset"), "timestamp": element.get("timestamp"), "user": element.get("user"), "uid": element.get("uid") }





        descendants = list(element.iter())

        nd_array = []
        address = {}
        for nd in element.findall('nd'):
            nd_array.append(nd.get("ref"))
            node["node_refs"] = nd_array

        for t in element.findall('tag'):
            k = t.get("k")
            if problemchars.search(k):
               continue
            else:
               if is_address.search(k) and not second_colon.search(k):
                    if is_street.search(k):
                        address.update({"street": audit.update_name(t.get("v"))})
                    else:
                        prop = k.split(":")[-1]
                        address.update({prop: t.get("v")})
               else:
                   node[k] = t.get("v")


        if bool(address): node["address"] = address
        address = {}
        nd_array = []
        print node
        return node
    else:
        return None

def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def main(filename):
    data = process_map(filename, True)
    return data

if __name__ == "__main__":
    main('toronto_canada.osm')
