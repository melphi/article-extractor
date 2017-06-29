[![Build Status](https://travis-ci.org/melphi/article-extractor.svg?branch=master)](https://travis-ci.org/melphi/article-extractor)

# Article Extractor
Extracts the article content from web pages.

## Installation

### Prerequisites
- [Docker](https://docs.docker.com/engine/installation/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Easy installation
This will download the pre built images from Docker hub.

`sudo docker-compose -f docker-compose.hub.yml up`

### Custom installation
This will build a local image and then run the application. From the source folders run:

`sudo docker-compose -f docker-compose.dev.yml up`

## Usage

Check if the service is up with by pointing the broswer at http://localhost:8000/health. A healthy message should appear.

From command line run (replace the url value with the url to scrape):<br/>

`curl -H "Content-Type: application/json" -X POST -d '{"url":"http://www.stopfake.org/en/top-5-russian-fakes-about-us"}' http://localhost:8000/extract`

## Known issues
* Non article like pages are not parsed.
* An agent header should be sent to avoid to be blacklisted.