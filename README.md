# Araport Community API v 0.3 Tutorial

## Tutorial 4: Creating a passthrough-type service

This is remarkably simple, All you are going to do is establish a communications route between an API context provided by ADAMA and a remote service URL. The ADAMA service will act as a proxy, but will add value by providing CORS support, HTTPS, logging, OAuth2 authentication, and discoverability in the Araport Data API Store.

There are two ways to register a passthrough: you can just POST a form containing all the requisite parameters, which we will not cover, or you can create a small Git repo containing a metadata.yml file. We prefer the latter because its consistent with the other types, provides external documentation of the service, and opens up the capability in the future of using ADAMA's automatic documentation generation capability to describe how to invoke your API.

_Let's examine passthrough_demo/metadata.yml_

```
---
description: "Returns MapMan bin information for a given AGI locus identifier using the passthrough type of Araport web service"
name: pass_mapman_bin_by_locus
type: passthrough
url: "http://www.gabipd.org/services/rest/mapman/bin"
version: 0.1
whitelist:
  - www.gabipd.org
```

The major difference between this file and the ones we've used to date is that 'url' actually points to the most terminal endpoint of your remote service.

_Go ahead and register the service with ADAMA_

```
curl -skL -XPOST -H "Authorization: Bearer $TOKEN" -F "git_repository=https://github.com/*YOUR-GITHUB-UNAME*/workshop_tutorial_api.git" -F "metadata=passthrough_demo" $API/$NS/services
```

_Test that registration was successful_

```
curl -skL -XGET -H "Authorization: Bearer $TOKEN" https://api.araport.org/community/v0.3/${NS}/pass_mapman_bin_by_locus_v0.1
```

_Test that the passthrough works_

The remote service is invoked as follows: http://www.gabipd.org/services/rest/mapman/bin?request=[{"agi":"At4g25530"}] However, this URL is not safe because it's not URL-encoded. To create a URL-encoded string, cut and paste into this handy [URL Decoder/Encoder](http://meyerweb.com/eric/tools/dencoder/). Then, construct your URL.

```
curl -skL -XGET -H "Authorization: Bearer $TOKEN" https://api.araport.org/community/v0.3/${NS}/pass_mapman_bin_by_locus_v0.1/access?request=%5B%7B%22agi%22%3A%22At4g25530%22%7D%5D

[{"request":{"agi":"At4g25530"},"result":[{"code":"27.3.22","name":"RNA.regulation of transcription.HB,Homeobox transcription factor family","description":"no description","parent":{"code":"27.3","name":"RNA.regulation of transcription","description":"no description","parent":{"code":"27","name":"RNA","description":"no description","parent":null}}}]}]
```
