CREATE EXTERNAL FILE FORMAT skipHeader_CSV
WITH (FORMAT_TYPE = DELIMITEDTEXT,
      FORMAT_OPTIONS(
          FIELD_TERMINATOR = ',',
          STRING_DELIMITER = '"',
          FIRST_ROW = 2, 
          USE_TYPE_DEFAULT = True)
) 
GO


CREATE EXTERNAL TABLE samoshyn_schema.external_table
(
    [VendorID] INT NULL,
    [tpep_pickup_datetime] DATETIME NOT NULL,
    [tpep_dropoff_datetime] DATETIME NOT NULL,
    [passenger_count] INT NULL,
    [trip_distance] FLOAT(5) NOT NULL,
    [RatecodeID] INT NULL,
    [store_and_fwd_flag] CHAR(2) NULL,
    [PULocationID] INT NOT NULL,
    [DOLocationID] INT NOT NULL,
    [payment_type] FLOAT(5) NULL,
    [fare_amount] FLOAT(5) NOT NULL,
    [extra] FLOAT(5) NOT NULL,
    [mta_tax] FLOAT(5) NOT NULL,
    [tip_amount] FLOAT(5) NOT NULL,
    [tolls_amount] FLOAT(5) NOT NULL,
    [improvement_surcharge] FLOAT(5) NOT NULL,
    [total_amount] FLOAT(5) NOT NULL,
    [congestion_surcharge] FLOAT(5) NOT NULL
)
WITH
(  LOCATION='yellow_tripdata_2020-01.csv',
    DATA_SOURCE = samoshyn_blob,
  FILE_FORMAT = skipHeader_CSV
)
GO