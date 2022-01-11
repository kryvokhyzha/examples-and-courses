--https://docs.microsoft.com/en-us/azure/synapse-analytics/sql-data-warehouse/sql-data-warehouse-tables-distribute

CREATE TABLE samoshyn_schema.fact_tripdata  
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
(
    DISTRIBUTION = HASH([tpep_pickup_datetime]),
    CLUSTERED COLUMNSTORE INDEX
)
GO

INSERT INTO samoshyn_schema.fact_tripdata SELECT * FROM samoshyn_schema.external_table
GO
