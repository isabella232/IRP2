# International Research Portal Project (IRP2)

This application delivers a research dashboard that assists users in conducting provenance-based discovery of looted Holocaust assets. It queries and aggregates results from many collecting institutions, giving the user an overview of available records and collections for further research.

## Install Steps

1. Checkout the code:
```
git clone https://github.com/CI-BER/LHARP.git
```
1. Install Python and PIP:
```
sudo apt-get install python python-pip
```
1. Install Python packages:
```
sudo pip install logging lxml re requests bs4 json
```
1. Run the Flask Application in project dir:
```
python dashboard.py
```
1. Point your browser at localhost:5000

## Debugging

The application is currently configured in Flask debug mode, which means it will restart upon changes made to the python files. It will not restart automatically after changes to the web templates. To see you changes, either edit a python file or kill (CTRL-C) and re-run the program.

An error log is written to */tmp/LHARP.log*. If you need to add logging output, do so using the Flask app logger, for instance:

    app.logger.debug("results: \n"+json.dumps(results))

## Components

The application is currently broken into two function areas, collection search code
and the HTTP request handler code that uses Flask.

* dashboard.py - Handles application setup and web requests.
* archives - A module containing collection search code
* archives.core - The main services module for collections, contains high-level functions for querying all of the collections.
* archives.collection - Contains the class module used to create searchable collections.

Collections will vary in how they deliver search results, from JSON APIs to HTML replies that require "screen scrape" treatment. Some collections even require multiple requests within a session to obtain results, for an example see gettyri.py. The archives.core module also includes a list of archival institutions as dictionaries with metadata. This information is passed into the web templates and is the starting point for rendering the results.

## Tasks Ahead

+ Initial technical improvements (Greg 9/4)
 + [x] Document project for better collaboration
 + [x] Make collection searches more modular and pluggable
 + [ ] Make query service REST/JSON
 + [ ] Setup a persistent demonstration site (virtual farm or VCL)
+ Add collections to search (Anuj 10/2)
 + [ ] UK
 + [ ] Berlin
 + [ ] Netherlands
 + [ ] Austria
 + [ ] Divide the USHMM into two result sets (what is 2nd?)
 + [ ] More compact display of results
+ Add query expansion back-end services (Greg 10/2)
 + [ ] Translate terms into language of collection descriptions
 + [ ] Suggest artist name variations (Getty DB)
 + [ ] Suggest art object types (Getty TGM thesaurus)
 + [ ] Suggest place name variations
+ Redesign user experience for query expansion (Anuj 10/23)
 + [ ] Presentation of query refinement options
 + [ ] Auto-suggestion of terms from thesauri (via back-end service)
 + [ ] AJAX updated results, updated upon selection of a query expansion
