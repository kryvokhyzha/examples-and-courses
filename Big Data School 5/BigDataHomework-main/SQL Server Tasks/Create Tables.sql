CREATE TABLE samoshyn_schema.VendorID
(
	[ID] INT NOT NULL,
	[Name] VARCHAR (255) NOT NULL 
)
WITH
(
    DISTRIBUTION = HASH([ID]),
    CLUSTERED COLUMNSTORE INDEX
)

INSERT INTO samoshyn_schema.VendorID VALUES (1, 'Creative Mobile Technologies, LLC')
INSERT INTO samoshyn_schema.VendorID VALUES (2, 'VeriFone Inc.')

CREATE TABLE samoshyn_schema.RateCodeID
(
	[ID] INT NOT NULL,
	[Name] VARCHAR (255) NOT NULL 
)
WITH
(
    DISTRIBUTION = HASH([ID]),
    CLUSTERED COLUMNSTORE INDEX
)

INSERT INTO samoshyn_schema.RateCodeID VALUES (1, 'Standard rate')
INSERT INTO samoshyn_schema.RateCodeID VALUES (2, 'JFK')
INSERT INTO samoshyn_schema.RateCodeID VALUES (3, 'Newark')
INSERT INTO samoshyn_schema.RateCodeID VALUES (4, 'Nassau or Westchester')
INSERT INTO samoshyn_schema.RateCodeID VALUES (5, 'Negotiated fare')
INSERT INTO samoshyn_schema.RateCodeID VALUES (6, 'Group ride')

CREATE TABLE samoshyn_schema.Payment_type
(
	[ID] INT NOT NULL,
	[Name] VARCHAR (255) NOT NULL 
)
WITH
(
    DISTRIBUTION = HASH([ID]),
    CLUSTERED COLUMNSTORE INDEX
)

INSERT INTO samoshyn_schema.Payment_type VALUES (1, 'Credit card')
INSERT INTO samoshyn_schema.Payment_type VALUES (2, 'Cash')
INSERT INTO samoshyn_schema.Payment_type VALUES (3, 'No charge')
INSERT INTO samoshyn_schema.Payment_type VALUES (4, 'Dispute')
INSERT INTO samoshyn_schema.Payment_type VALUES (5, 'Unknown')
INSERT INTO samoshyn_schema.Payment_type VALUES (6, 'Voided trip')
GO



