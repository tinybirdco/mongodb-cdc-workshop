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

## Resources
* [A practical guide to real-time CDC with MongoDB](https://www.tinybird.co/blog-posts/mongodb-cdc)
* [Lambda CDC processing with Tinybird](https://www.tinybird.co/docs/guides/querying-data/lambda-example-cdc)

## Session JSON objects

When working with nested JSON, there are two JSON documents ingested:

### Weather report objects
![JSON](images/report-object.png)

### Alert objects
![JSON](images/alert-object.png)

## Landing Data Sources 

### `mongo_cdc_events` Data Source

#### `insert` events

MongoDB CDC events land in a `mondo_cdc_events` Data Source. If the event has `operationType = insert`, there is a `fullDocument` JSON object that contains the weather report. 

Report attributes are parsed with the `JSONExtract` functions:
    * JSONExtractString(payload, 'description') AS description
    * JSONExtractFloat(payload, 'temp_f') AS temp_f
    * JSONExtractInt(payload, 'humidity') AS humidity

```bash
DESCRIPTION >
    CDC Events coming from a MongoDB instance.

SCHEMA >
    `_id__data` String `json:$._id._data`,
    `clusterTime` Int64 `json:$.clusterTime`,
    `documentKey__id` String `json:$.documentKey._id`,
    `fullDocument__id` String `json:$.fullDocument._id`,
    `site_name` String `json:$.fullDocument.site_name`,
    `timestamp` DateTime `json:$.fullDocument.timestamp`,
    `payload` String `json:$.fullDocument`,
    `ns_coll` String `json:$.ns.coll`,
    `ns_db` String `json:$.ns.db`,
    `operationType` String `json:$.operationType`,
    `wallTime` Int64 `json:$.wallTime`

ENGINE "MergeTree"
ENGINE_PARTITION_KEY "toYYYYMM(timestamp)"
ENGINE_SORTING_KEY "timestamp, site_name"
```

#### `delete` events
If the event has `operationType = delete`, there is no `fullDocument` JSON object. Since that violates the schema specification, the event is quarantined and written to a `mongo_cdc_events_quarantine` table. That table is used to materizlize `delete` events into a `deletes_mv` Data Source. 

Then the `deletes_mv` Data Source is referenced when applying deletes to create the `weather_reports_mv` Data Source:

```sql
SELECT * 
FROM mongo_cdc_events
WHERE documentKey__id NOT IN (
    SELECT documentKey__id 
    FROM deletes_mv
)
```



### `nested_json` Data Source

The `report` and `alert` objects are ingested with the following Data Source schema. Here the common `message` JSON attribute, that contains the different JSON structures, is assigned to a `payload` string. From there, the `JSONExtract` set of functions are used to parse and access the JSON attributes in the `message` sections. 

```bash
SCHEMA >
    `event_type` String `json:$.event_type`,
    `timestamp` DateTime `json:$.timestamp`,
    `site_name` String `json:$.site_name`,
    `payload` String `json:$.message`

ENGINE "MergeTree"
ENGINE_PARTITION_KEY "toYear(timestamp)"
ENGINE_SORTING_KEY "event_type, timestamp, site_name"
```




## Demo components

This workshop starts with a MongoDB Atlas database with a `weather-reports` collection. 

![MongoDB Atlas](images/mongodb-atlas.png)

The Confluent MongoDB Atlas Source Connector is used to publish CDC events onto a Kafka stream.

![Confluent Connector](images/confluent-connector.png)
