# Tinybird Workshop on ingesting MongoDB CDC events

This repository is a companion piece to the 'MongoDB CDC' workshop. The intended audience of this workshop are folks who have MongoDB data and are interested in streaming that data to Tinybird.

In this workshop we start with a MongoDB Atlas instance with a `weather-reports` collection in a `weather-data` database. We then configure and deploy an instance of the [Confluent MongoDB Atlas Source Connector](https://docs.confluent.io/cloud/current/connectors/cc-mongo-db-source.html), and then stream that data into Tinybird using its native Confluent Stream connector. 

Here is a look at what we are building:


![Diagram](images/diagram.png)


## Workshop topics

* Publishing MongoDB data to a Kafka stream:
  * Tour live MongoDB collection on Atlas.
  * Confluent MongoDB Atlas Source Connector
* Consume Kafka Topic in Tinybird.
* Manage duplicate data.
* Working with nested and varying JSON documents
* Build API endpoints that publish MongoDB data.

The `tinybird` folder contains:
* Data Source definitions.
* Pipe and Node definitions.
* Example Tinybird Playgrounds. 

## Session JSON objects

When working with nested JSON, there are two JSON documents ingested:

### Weather report objects
![JSON](images/report-object.png)

### Alert objects
![JSON](images/alert-object.png)



![MongoDB Atlas](images/mongodb-atlas.png)


![Confluent Connector](images/confluent-connector.png)
