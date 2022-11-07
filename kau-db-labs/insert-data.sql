insert into public."Smuggler" ("Name", "Passport", "Address", "Family")
values
    ('name 1', 'smuggler1', 'address 1', 'family1'), ('name 2', 'smuggler2', 'address 2', 'family2'), ('name 3', 'smuggler3', 'address 3', 'family3'),
    ('name 4', 'smuggler4', 'address 4', 'family4'), ('name 5', 'smuggler5', 'address 5', 'family5'), ('name 6', 'smuggler6', 'address 6', 'family6'),
    ('name 7', 'smuggler7', 'address 7', 'family7'), ('name 8', 'smuggler8', 'address 8', 'family8'), ('name 9', 'smuggler9', 'address 9', 'family9'),
    ('name 10', 'smuggler10', 'address10', 'family10'), ('name 11', 'smuggler11', 'address 11', 'family11'), ('name 12', 'smuggler12', 'address 12', 'family12');

insert into public."Dealer" ("Name", "Passport", "Birthday", "Family", "Sex")
values
    ('name dealer 1', 'dealer1', '2011-10-10', 'family1', 'M'), ('name dealer 2', 'dealer2', '2010-10-10', 'family2', 'F'),
    ('name dealer 3', 'dealer3', '2010-01-01', 'family3', 'M'), ('name dealer 4', 'dealer4', '2010-10-10', 'family4', 'F'),
    ('name dealer 5', 'dealer5', '2010-01-01', 'family5', 'M'), ('name dealer 6', 'dealer6', '2010-10-10', 'family6', 'F'),
    ('name dealer 7', 'dealer7', '2010-01-01', 'family7', 'M'), ('name dealer 8', 'dealer8', '2010-10-10', 'family8', 'F'),
    ('name dealer 9', 'dealer9', '2010-01-01', 'family9', 'M'), ('name dealer 10', 'dealer10', '2010-10-10', 'family10', 'F'),
    ('name dealer 11', 'dealer11', '2010-01-01', 'family11', 'M'), ('name dealer 12', 'dealer12', '2010-10-10', 'family12', 'F');

insert into public."Head" ("Name", "Birthday", "Passport", "CartelName")
values
    ('Perrin Almaro', '1963-04-07', 'TE113121', 'cartelname1'), ('Cico Lavezz', '1968-10-07', 'TK213122', 'cartelname2'),
    ('Bonucci', '1999-01-07', 'TR313123', 'cartelname3'), ('Messi', '1979-10-07', 'TL413124', 'cartelname4'),
    ('Jr Messi', '1999-12-31', 'TG513125', 'cartelname5'), ('Biden', '1942-11-20', 'OL613126', 'cartelname6');

insert into public."DrugsBaron" ("Name", "Birthday", "Passport", "Family", "PartitionName")
values
    ('DB1', '1999-01-21', 'QW111111', 'family1', 'partitionname1'), ('DB2', '1999-01-21', 'QW111112', 'family2', 'partitionname2'),
    ('DB3', '1999-01-21', 'QW111113', 'family3', 'partitionname3'), ('DB4', '1999-01-21', 'QW111114', 'family4', 'partitionname4'),
    ('DB5', '1999-01-21', 'QW111115', 'family5', 'partitionname5'), ('DB6', '1999-01-21', 'QW111116', 'family6', 'partitionname6'),
    ('DB7', '1999-01-21', 'QW111117', 'family7', 'partitionname7'), ('DB8', '1999-01-21', 'QW111118', 'family8', 'partitionname8'),
    ('DB9', '1999-01-21', 'QW111119', 'family9', 'partitionname9'), ('DB10', '1999-01-21', 'QW1111121', 'family10', 'partitionname10'),
    ('DB11', '1999-01-21', 'QW111122', 'family11', 'partitionname11'), ('DB12', '1999-01-21', 'QW111123', 'family12', 'partitionname12');

insert into public."Cartel" ("CartelName", "MainOfficeAddress")
values
    ('cartelname1', 'someaddress1'), ('cartelname2', 'someaddress2'), ('cartelname3', 'someaddress3'),
    ('cartelname4', 'someaddress4'), ('cartelname5', 'someaddress5'), ('cartelname6', 'someaddress6');

insert into public."Partition" ("PartitionName", "CartelName", "SoldDrugs", "Placement")
values
    ('partitionname1', 'cartelname1', 'some val 1', 'some pl 1'), ('partitionname2', 'cartelname1', 'some val 2', 'some pl 1'),
    ('partitionname3', 'cartelname2', 'some val 2', 'some pl 2'), ('partitionname4', 'cartelname2', 'some val 2', 'some pl 1'),
    ('partitionname5', 'cartelname3', 'some val 2', 'some pl 2'), ('partitionname6', 'cartelname3', 'some val 1', 'some pl 1'),
    ('partitionname7', 'cartelname4', 'some val 2', 'some pl 2'), ('partitionname8', 'cartelname4', 'some val 1', 'some pl 1'),
    ('partitionname9', 'cartelname5', 'some val 2', 'some pl 2'), ('partitionname10', 'cartelname5', 'some val 1', 'some pl 1'),
    ('partitionname11', 'cartelname6', 'some val 2', 'some pl 2'), ('partitionname12', 'cartelname6', 'some val 1', 'some pl 1');

insert into public."Lab" ("IdLab", "Address", "Cartel", "IdStock")
values
    (1, 'address 1', 'cartelname1', 5), (2, 'address 2', 'cartelname1', 5), (3, 'address 3', 'cartelname1', 1),
    (4, 'address 4', 'cartelname2', 2), (5, 'address 5', 'cartelname3', 4), (6, 'address 6', 'cartelname4', 3),
    (7, 'address 7', 'cartelname5', 6), (8, 'address 8', 'cartelname5', 6), (9, 'address 9', 'cartelname5', 7),
    (10, 'address 10', 'cartelname6', 8), (11, 'address 11', 'cartelname6', 9), (12, 'address 12', 'cartelname6', 12);

insert into public."Drugs" ("IdDrugs", "Type", "IdLab", "Price", "Quality")
values
    (1, 'some type 1', 1, 10, 75.5), (2, 'some type 2', 2, 11, 71.0), (3, 'some type 3', 3, 15, 99.0),
    (4, 'some type 4', 4, 9, 44), (5, 'some type 5', 5, 11.2, 72.0), (6, 'some type 6', 6, 16, 99.1),
    (7, 'some type 7', 7, 9, 45), (8, 'some type 5', 8, 11.8, 72.9), (9, 'some type 9', 9, 7, 31.1),
    (10, 'some type 10', 10, 9, 45), (11, 'some type 11', 11, 11.9, 73.9), (12, 'some type 12', 12, 7, 31.1);

insert into public."Stock" ("IdStock", "Smuggler", "IdDrugs", "Weight")
values
    (1, 'smuggler1', 1, int4(random() * 1000)), (2, 'smuggler2', 2, int4(random() * 1000)), (3, 'smuggler3', 3, int4(random() * 1000)),
    (4, 'smuggler4', 4, int4(random() * 1000)), (5, 'smuggler5', 5, int4(random() * 1000)), (6, 'smuggler6', 6, int4(random() * 1000)),
    (7, 'smuggler7', 7, int4(random() * 1000)), (8, 'smuggler8', 8, int4(random() * 1000)), (9, 'smuggler9', 9, int4(random() * 1000)),
    (10, 'smuggler10', 10, int4(random() * 1000)), (11, 'smuggler11', 11, int4(random() * 1000)), (12, 'smuggler12', 12, int4(random() * 1000));

insert into "Contract" ("PartitionName", "IdDrugs", "Dealer", "Smuggler", "IdContract", "IdStock", "Weight")
values
    ('partitionname1', 1, 'dealer1', 'smuggler1', 1, 1, int4(random() * 1000)), ('partitionname2', 2, 'dealer1', 'smuggler2', 2, 2, int4(random() * 1000)),
    ('partitionname3', 3, 'dealer2', 'smuggler3', 3, 3, int4(random() * 1000)), ('partitionname4', 5, 'dealer2', 'smuggler4', 4, 4, int4(random() * 1000)),
    ('partitionname5', 5, 'dealer3', 'smuggler5', 5, 5, int4(random() * 1000)), ('partitionname6', 8, 'dealer4', 'smuggler6', 6, 6, int4(random() * 1000)),
    ('partitionname7', 8, 'dealer5', 'smuggler7', 7, 7, int4(random() * 1000)), ('partitionname8', 8, 'dealer6', 'smuggler7', 8, 8, int4(random() * 1000)),
    ('partitionname9', 9, 'dealer7', 'smuggler9', 9, 9, int4(random() * 1000)), ('partitionname10', 10, 'dealer8', 'smuggler10', 10, 10, int4(random() * 1000));
