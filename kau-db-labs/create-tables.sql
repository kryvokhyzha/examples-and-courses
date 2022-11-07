CREATE TABLE IF NOT EXISTS "Head"(
    "Name" TEXT NOT NULL,
    "Birthday" DATE NOT NULL,
    "Passport" TEXT PRIMARY KEY,
    "CartelName" TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS "Cartel"(
    "CartelName" TEXT PRIMARY KEY,
    "MainOfficeAddress" TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS "DrugsBaron"(
    "Name" TEXT NOT NULL,
    "Birthday" DATE NOT NULL,
    "Passport" TEXT PRIMARY KEY,
    "Family" TEXT NOT NULL,
    "PartitionName" TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS "Partition"(
    "PartitionName" TEXT NOT NULL UNIQUE,
    "CartelName" TEXT NOT NULL,
    "SoldDrugs" TEXT NOT NULL,
    "Placement" TEXT NOT NULL,
    PRIMARY KEY ("PartitionName", "CartelName")
);

CREATE TABLE IF NOT EXISTS "Dealer"(
    "Name" TEXT NOT NULL,
    "Passport" TEXT PRIMARY KEY,
    "Birthday" DATE NOT NULL,
    "Family" TEXT NOT NULL,
    "Sex" TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS "Contract"(
    "PartitionName" TEXT NOT NULL,
    "IdDrugs" INTEGER NOT NULL,
    "Dealer" TEXT NOT NULL,
    "Smuggler" TEXT NOT NULL,
    "IdContract" INTEGER PRIMARY KEY,
    "IdStock" INTEGER NOT NULL,
    "Weight" INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS "Drugs"(
    "IdDrugs" INTEGER PRIMARY KEY,
    "Type" TEXT NOT NULL,
    "IdLab" INTEGER NOT NULL,
    "Price" DOUBLE PRECISION NOT NULL,
    "Quality" DOUBLE PRECISION NOT NULL
);

CREATE TABLE IF NOT EXISTS "Stock"(
    "IdStock" INTEGER PRIMARY KEY,
    "Smuggler" TEXT NOT NULL,
    "IdDrugs" INTEGER NOT NULL,
    "Weight" INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS "Lab"(
    "IdLab" INTEGER PRIMARY KEY,
    "Address" TEXT NOT NULL,
    "Cartel" TEXT NOT NULL,
    "IdStock" INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS "Smuggler"(
    "Name" TEXT NOT NULL,
    "Passport" TEXT PRIMARY KEY,
    "Address" TEXT NOT NULL,
    "Family" TEXT NOT NULL
);

ALTER TABLE
    "Cartel" ADD CONSTRAINT "cartel_cartelname_foreign" FOREIGN KEY("CartelName") REFERENCES "Head"("CartelName");

ALTER TABLE
    "Lab" ADD CONSTRAINT "lab_cartel_foreign" FOREIGN KEY("Cartel") REFERENCES "Cartel"("CartelName");

ALTER TABLE
    "Partition" ADD CONSTRAINT "partition_partitionname_foreign" FOREIGN KEY("PartitionName") REFERENCES "DrugsBaron"("PartitionName");

ALTER TABLE
    "Partition" ADD CONSTRAINT "partition_cartelname_foreign" FOREIGN KEY("CartelName") REFERENCES "Cartel"("CartelName");

ALTER TABLE
    "Contract" ADD CONSTRAINT "contract_partitionname_foreign" FOREIGN KEY("PartitionName") REFERENCES "Partition"("PartitionName");

ALTER TABLE
    "Contract" ADD CONSTRAINT "contract_dealer_foreign" FOREIGN KEY("Dealer") REFERENCES "Dealer"("Passport");

ALTER TABLE
    "Contract" ADD CONSTRAINT "contract_iddrugs_foreign" FOREIGN KEY("IdDrugs") REFERENCES "Drugs"("IdDrugs");

ALTER TABLE
    "Contract" ADD CONSTRAINT "contract_smuggler_foreign" FOREIGN KEY("Smuggler") REFERENCES "Smuggler"("Passport");

ALTER TABLE
    "Contract" ADD CONSTRAINT "contract_idstock_foreign" FOREIGN KEY("IdStock") REFERENCES "Stock"("IdStock");

ALTER TABLE
    "Drugs" ADD CONSTRAINT "drugs_idlab_foreign" FOREIGN KEY("IdLab") REFERENCES "Lab"("IdLab");

ALTER TABLE
    "Stock" ADD CONSTRAINT "stock_smuggler_foreign" FOREIGN KEY("Smuggler") REFERENCES "Smuggler"("Passport");

ALTER TABLE
    "Stock" ADD CONSTRAINT "stock_iddrugs_foreign" FOREIGN KEY("IdDrugs") REFERENCES "Drugs"("IdDrugs");

-- -- видаляємо цю залежність, щоб прибрати циклічність в схемі
-- ALTER TABLE
--     "Lab" ADD CONSTRAINT "lab_idstock_foreign" FOREIGN KEY("IdStock") REFERENCES "Stock"("IdStock");
