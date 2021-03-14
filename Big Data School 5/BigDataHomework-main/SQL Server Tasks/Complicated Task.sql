SELECT DISTINCT VendorID AS 'ID'
INTO samoshyn_schema.VendorID 
FROM samoshyn_schema.external_table

ALTER TABLE samoshyn_schema.VendorID
ADD Name VARCHAR(255) NOT NULL DEFAULT 'NULL'

UPDATE samoshyn_schema.VendorID_1 SET Name = 'Creative Mobile Technologies, LLC' WHERE ID = 1
UPDATE samoshyn_schema.VendorID_1 SET Name = 'VeriFone Inc.' WHERE ID = 2
GO

SELECT DISTINCT RateCodeID AS 'ID'
INTO samoshyn_schema.RateCodeID 
FROM samoshyn_schema.external_table

ALTER TABLE samoshyn_schema.RateCodeID
ADD Name VARCHAR(255) NOT NULL DEFAULT 'NULL'

UPDATE samoshyn_schema.RateCodeID SET Name = 'Standard rate' WHERE ID = 1
UPDATE samoshyn_schema.RateCodeID SET Name = 'JFK' WHERE ID = 2
UPDATE samoshyn_schema.RateCodeID SET Name = 'Newark' WHERE ID = 3
UPDATE samoshyn_schema.RateCodeID SET Name = 'Nassau or Westchester' WHERE ID = 4
UPDATE samoshyn_schema.RateCodeID SET Name = 'Negotiated fare' WHERE ID = 5
UPDATE samoshyn_schema.RateCodeID SET Name = 'Group ride' WHERE ID = 6
GO

SELECT DISTINCT Payment_type AS 'ID'
INTO samoshyn_schema.Payment_type 
FROM samoshyn_schema.external_table

ALTER TABLE samoshyn_schema.Payment_type
ADD Name VARCHAR(255) NOT NULL DEFAULT 'NULL'

UPDATE samoshyn_schema.Payment_type SET Name = 'Credit card' WHERE ID = 1
UPDATE samoshyn_schema.Payment_type SET Name = 'Cash' WHERE ID = 2
UPDATE samoshyn_schema.Payment_type SET Name = 'No charge' WHERE ID = 3
UPDATE samoshyn_schema.Payment_type SET Name = 'Dispute' WHERE ID = 4
UPDATE samoshyn_schema.Payment_type SET Name = 'Unknown' WHERE ID = 5
UPDATE samoshyn_schema.Payment_type SET Name = 'Voided trip' WHERE ID = 6
GO