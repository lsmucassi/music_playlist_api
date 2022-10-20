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

---

## Questionaire

### Practical Questions (Coding challenge 2)

• Show how you would expose an endpoint to this microservice

> used Function URL from lambda or API Gateway

• Show how you implement metrics in this microservice

> use cloudwatch, quicksight and a dashboard management system to monitor (reliability, availability and latency)

• Show how you secured this microservice with JWT

> use API Gateway API key, or PyJWT, or Auth0

• Show how you implemented unit testing

> used pytest linbrary, and the fastAPI web interface

• Show how you would implement logging for exception management

> use cloudwatch, database table to log exceptions and faults

### Theoretical Questions

• List which principles you are following with this microservice

> single responsibility: The microservice is only responsible for the operations of playlist and nothing else
> Loosely coupled: The ms doesn't have to know about the structure of the song data or songs ms,
> Failure Isolation: With Exception handling, handle failure and make sure the ms doesn't affect the while architecture or app
> Security: To implement JWT to authorise operation on the ms resources

• List which design patterns you have used with this microservice and why

> using integration pattern (Gateway and Aggregator): With the approach used to deploy the ms on the cloud, the capability of a gateway allows for auth, routing, load balancing and elasticity or scaling.

• List where and why you used some characteristics of object-oriented programming

> It was used to define the playlist model, this is useful as the model can be reused amongst resources/functions/endpoints. This is also a good practice as it limits spaghetti code, when the code is organised in this manner it allows for a single point of fixing/config or addition of the model.

### Future improvements

- Connect API Gateway to the Lambda, to make handling auth easier and manage load balancing and scalability
- Implement or handle more exceptions on endpoint requests
- add more fields on the data model, such as date when tthe playlist was created, date when a song was added or removed, this would change the structure of songs from a list to a json/dict
- implement proper logging of all activities (requests/processing/response) done to the microservice
- implement metrices and alerting for any failure, downtime and scaling changes

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
