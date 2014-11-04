# Araport Community API v 0.3 Tutorial

## Tutorial 3: Creating a query-type service 

Parameter handling and HTTP request management are the same between generic and query types. The difference is in how we process the response from the remote server. Open up query_demo/main.py in your editor and scroll down past the parameter handling code:

```
    ...
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
```

The response from the MapMan server is: 

```
[
    {"request":
        {"agi":"At4g25530"},
     "result":[
        {"code":"27.3.22",
         "name":"RNA.regulation of transcription.HB,Homeobox transcription factor family",
         "description":"no description",
         "parent":
            {"code":"27.3",
             "name":"RNA.regulation of transcription",
             "description":"no description",
             "parent":
                {"code":"27",
                 "name":"RNA",
                 "description":"no description",
                 "parent":null}}}]}]
```                 

For those not familiar with JSON, this is an array of responses, each one of which contains a pair of keys 'request' and 'result'. The 'result' key is an array of MapMap codes (and their parental lineage which we are ignoring). We will transform this response to an AIP locus_property, which is basically a data structure containing the locus identifier and an array of properties. At present, we don't proscribe the names of keys inside these properties but will soon offer a lookup service so one can see what other API developers have used. 

_Test out the code in a Python editor_

Change to the query_demo directory and launch a Python interpreter:

```
>>> import main
>>> main.search({'locus':'AT4G25530'})
{
    "properties": [
        {
            "type": "mapman_bin", 
            "value": "27.3.22"
        }, 
        {
            "type": "mapman_name", 
            "value": "RNA.regulation of transcription.HB,Homeobox transcription factor family"
        }
    ], 
    "class": "locus_property", 
    "locus": "AT4G25530"
}
---
```

_Register the query service with AIP_

Assuming you have been through the tutorial, you will be aware of the ENV variables referred to here:

1. POST your service
```
curl -skL -XPOST -H "Authorization: Bearer $TOKEN" -F "git_repository=https://github.com/*YOUR-GITHUB-UNAME*/workshop_tutorial_api.git" -F "metadata=query_demo" $API/$NS/services 
```

2. Check its status
```
curl -skL -XGET -H "Authorization: Bearer $TOKEN" https://api.araport.org/community/v0.3/$NS/query_mapman_bin_by_locus_v0.1
```

3. Test it out

```
curl -skL -XGET -H "Authorization: Bearer $TOKEN" https://api.araport.org/community/v0.3/$NS/query_mapman_bin_by_locus_v0.1/search?locus=AT4G25530

{"result":[
    {"locus":"AT4G25530",
     "properties":[
        {"type":"mapman_bin",
         "value":"27.3.22"},
        {"type":"mapman_name",
         "value":"RNA.regulation of transcription.HB,Homeobox transcription factor family"}],
     "class":"locus_property"}],
 "metadata":
    {"time_in_main":0.5226819515228271},
 "status":"success"}
```

_Moving on_

If you want to save your work on this branch, please do the following in your local workshop_tutorial_api directory

```
git add .
git commit -m "In progress!"
```

Checkout the next branch to begin work on a query service. Follow along with the instructions in the README.md file under that branch.

```
git checkout "tutorial/4"
```
