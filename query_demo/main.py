import requests
import re
import json

def search(arg):

# arg contains a dict with a single key:value
# locus is AGI identifier and is mandatory
    
    # Return nothing if client didn't pass in a locus parameter
    if not ('locus' in arg):
       return
    
    # Validate against a regular expression
    locus = arg['locus']
    locus = locus.upper()
    p = re.compile('AT[1-5MC]G[0-9]{5,5}', re.IGNORECASE)
    if not p.search(locus):
        return

    param = '[{%22agi%22:%22' + locus + '%22}]'
    r = requests.get('http://www.gabipd.org/services/rest/mapman/bin?request=' + param)
    
    # Instead of returning the JSON native to the MapMan service
    # we traverse it and transform it into an AIP locus_property
    #
    # Then, we print out individual records as JSON, separated by a '---' delimiter
    # This allows large results to be streamed back to the client
    
    if r.ok:
        for rec in r.json():
            for result in rec['result']:
                new_record = { 'class': 'locus_property', 
                'locus': locus,
                'properties': [ {'type':'mapman_bin', 'value': result['code'] },
                {'type':'mapman_name', 'value':result['name']}] }

                print json.dumps(new_record, indent=4)
                print '---'
    else:
        return

def list(arg):
    pass
