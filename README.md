# Playlist Microservice API

> Building a microservice to hadle playlist operations(requests)

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-360/)

This project aims to:

> cover the development of the following endpomts

- /create-playlist - POST: creates a playlist with a playlist id, user id and songs referenced by id
- /get-playlist/{playlist_id} - GET: returns a playlist searched by playlist id
- /get-playlists - GET: return all available playlists
- /update-playlist - PUT: updates a given playlist using playlist id, either removes a song id or add a song id
- /delete-playlist/{playlist_id} - DELETE: deletes a playlist by id

## Dependenacies & Requirements

- AWS Accoount
- AWS Lambda
- AWS Cloudformation
- AWS DynamoDB
- AWS CDK
- Python
- Pip
- boto3
- mangum
- fastapi
- requests

## Usage

All the description of how to query the API is in the link below, also includes testing

- https://vfadintjowlokam5vklcwimxyy0wprvb.lambda-url.us-east-1.on.aws/docs#/

## Development setup

The microservice was deveoped using python, fastAPI and AWS, by using AWS CDK which allows for the creation of resources/infrastructure similar to terrafom, a lambda ith a Function URL was created on a cloudformation stack, the Lambda hosts the FastAPI microservice which interacts with an AWS DynamoDB Table.

The Infrastructure was created using AWS CDK and Typscript, see at the end for commands

```sh
# create your environment first
pip install -r requirements
pytest
```

## Project Management History

- [x] /create-playlist - POST: creates a playlist with a playlist id, user id and songs referenced by id
- [x] /get-playlist/{playlist_id} - GET: returns a playlist searched by playlist id
- [x] /get-playlists - GET: return all available playlists
- [x] /update-playlist - PUT: updates a given playlist using playlist id, either removes a song id or add a song id
- [x] /delete-playlist/{playlist_id} - DELETE: deletes a playlist by id

## Meta

LINDA MUCASSI – [@lsmucassi](https://twitter.com/lsmucassi) – lindasmucassi@gmail.com

# Welcome to your CDK TypeScript project

This is a blank project for CDK development with TypeScript.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

## Useful commands

- `npm run build` compile typescript to js
- `npm run watch` watch for changes and compile
- `npm run test` perform the jest unit tests
- `cdk deploy` deploy this stack to your default AWS account/region
- `cdk diff` compare deployed stack with current state
- `cdk synth` emits the synthesized CloudFormation template
