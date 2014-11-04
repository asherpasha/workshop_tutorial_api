# Araport Community API v 0.3 Tutorial

## Tutorial 2: Enrolling your web service with Araport

It is assumed that you have worked through "Getting Started with Araport" at the [Araport Devzone](https://www.araport.org/devzone)" before beginning this tutorial section.

_Define these ENV variables in your current terminal to make life easier_
```
export GITHUB_UNAME=*YOUR GITHUB USERNAME*
export NS=$GITHUB_UNAME
export API=https://api.araport.org/community/v0.3
```

_Use the Agave CLI to grab an OAuth2 token. Export it to ENV_
```
auth-tokens-create -S
> Token successfully refreshed and cached for 14400 seconds
> c1abb7c8326c33483e4a8a39a918ed7
export TOKEN=c1abb7c8326c33483e4a8a39a918ed7
```

Confirm status of and access to the ADAMA server
```
curl -H "Authorization: Bearer $TOKEN" -skL -X GET $API/status

{
    "api": "Adama v0.3",
    "hash": "1f82eeadf94d8cb5463f909a2b9a7039fcbbfe76",
    "status": "success"
}
```

_Assuming this is your first Araport API, create a namespace_

```
curl -H "Authorization: Bearer $TOKEN" -sk -X POST $API/namespaces \
-Fname=${NS} -Fdescription="Namespace for Github user ${NS}"
```

You should get back a response similar to this one:

```
{
    "result": "https://api.araport.org/community/v0.3/vaughn-dev",
    "status": "success"
}
```

_Post your new web service into your namespace_

Because we will be creating multiple APIs from a single repository, we must specify the path (relative to the root of the repo) where the metadata.yml file can be found. If this is ommitted, ADAMA looks at the root level. Also note that at present, ADAMA can only check out from the master branch. This will be addressed in a future release of the service. 

```
curl -skL -XPOST -H "Authorization: Bearer $TOKEN" -F "git_repository=https://github.com/*YOUR-GITHUB-UNAME*/data_api_examples.git" -F "metadata=generic" $API/$NS/services 
```

You should get back a response similar to this one:

```
{
    "message": "registration started", 
    "result": {
        "list_url": "https://api.araport.org/community/v0.3/vaughn-dev/generic_mapman_bin_by_locus_v0.1/list", 
        "notification": "", 
        "search_url": "https://api.araport.org/community/v0.3/vaughn-dev/generic_mapman_bin_by_locus_v0.1/search", 
        "state_url": "https://api.araport.org/community/v0.3/vaughn-dev/generic_mapman_bin_by_locus_v0.1"
    }, 
    "status": "success"
}
```

This tells you that the process of creating your service has begun. You should wait a minute and then poll the state_url endpoint to confirm that the new service has been properly deployed.

```
curl -skL -XGET -H "Authorization: Bearer $TOKEN" https://api.araport.org/community/v0.3/vaughn-dev/generic_mapman_bin_by_locus_v0.1
```

The result will resemble this JSON:

```
{
    "result": {
        "service": {
            "code_dir": "/tmp/tmpBMmBPk/user_code", 
            "description": "Returns MapMan bin information for a given AGI locus identifier using the generic type of Araport web service", 
            "json_path": "", 
            "language": "python", 
            "main_module": "generic_demo/main.py", 
            "metadata": "generic", 
            "name": "generic_mapman_bin_by_locus", 
            "namespace": "vaughn-dev", 
            "notify": "", 
            "requirements": [], 
            "self": "https://api.araport.org/community/v0.3/vaughn-dev/generic_mapman_bin_by_locus_v0.1", 
            "type": "generic", 
            "url": "http://www.gabipd.org/", 
            "version": 0.1, 
            "whitelist": [
                "www.gabipd.org", 
                "129.114.97.2", 
                "129.114.97.1", 
                "129.116.84.203"
            ], 
            "workers": [
                "7f3f1a32bbdeea510b5491ce03755dedda4efe7ed921e7632afb44b6f9e09adb"
            ]
        }
    }, 
    "status": "success"
}
```

_Testing your new service_

Finally, you will test the service by issuing an authenticated, parameterized GET to its search endpoint. Here's an example, though the namespace will be different for you. 

```
curl -skL -XGET -H "Authorization: Bearer $TOKEN" https://api.araport.org/community/v0.3/vaughn-dev/generic_mapman_bin_by_locus_v0.1/search?locus=At4g25530

[{"request":{"agi":"AT4G25530"},"result":[{"code":"27.3.22","name":"RNA.regulation of transcription.HB,Homeobox transcription factor family","description":"no description","parent":{"code":"27.3","name":"RNA.regulation of transcription","description":"no description","parent":{"code":"27","name":"RNA","description":"no description","parent":null}}}]}]
```

_Updating your service_

Inevitably, you will want to update your service, either to refresh the metadata or modify the code that powers it. 

1. Update by incrementing the version number and re-posting

2. Update by re-posting the service

_Moving on_

If you want to save your current work, please do the following in your local workshop_tutorial_api directory

```
git add .
git commit -m "In progress!"
```

Checkout the next branch to begin work on a query service. Follow along with the instructions in the README.md file under that branch.

```
git checkout "tutorial/3"
```
