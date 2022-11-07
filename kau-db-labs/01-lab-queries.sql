-- Побудувати базу даних наркокартелей. У кожного наркокартелю є тільки один глава.
-- Кожен наркокартель має підрозділи, кожним з яких керує один наркобарон.
-- Наркокартель має лабораторії, в яких виготовляються різні типи наркоти.
-- Наркота має певну ціну і якість від 0 до 100 відсотків. Наркота зберігається на складах.
-- Підрозділи наркокартелю укладають договір з дилерами та контрабандистами.
-- Дилери за контрактом торгують наркотою, а контрабандисти відповідають за перевезення наркоти зі складу.
-- Хитрі дилери можуть укладати контракти з кількома підрозділами.

-- DealerQuery
-- Вивести імена таких дилерів, що мають контракти з такими підрозділами на наркоту Х,
-- які мають контракти на наркоту, якість якої не менше, ніж 70%, та їх підрозділи.
select dealer."Name", partit."PartitionName"
from public."Dealer" as dealer
    inner join public."Contract" contract on dealer."Passport" = contract."Dealer"
    inner join public."Partition" partit on contract."PartitionName" = partit."PartitionName"
    inner join "Drugs" drugs on drugs."IdDrugs" = contract."IdDrugs"
where 1=1
    and drugs."Quality" >= 70
    and partit."PartitionName" in (:X); -- e.g. X: ('partitionname1', 'partitionname7')

-- DealerWithSuchDrugsTypesAs
-- Вивести дилерів, які торгують хоч одним типом наркоти таким же, як і диллер Х, та їхні дати народження.
with same_drugs as (
    select distinct contract."IdDrugs"
    from public."Contract" as contract
    where contract."Dealer" = :X
)
select distinct dealer."Name", dealer."Birthday"
from public."Dealer" as dealer
    inner join public."Contract" contract on dealer."Passport" = contract."Dealer"
    inner join same_drugs sd on sd."IdDrugs" = contract."IdDrugs"
where 1=1
    and contract."Dealer" <> :X; -- e.g. X: 'dealer5'

-- ContrabandistQuery
-- Вивести імена та паспорти дилерів, які працюють зі складами,
-- на яких є наркота типу Х, і вага наркоти на складі більша, ніж Y.

select distinct dealer."Name", dealer."Passport"
from public."Dealer" as dealer
    inner join "Contract" contract on dealer."Passport" = contract."Dealer"
    inner join "Stock" stock on stock."IdStock" = contract."IdStock"
where 1=1
    and stock."IdDrugs" in (:X)
    and  stock."Weight" > :Y; -- e.g. X: (3, 8, 5); Y: 100;

-- DealerWithOnlySuchDrugTypesAs
-- Вивести імена і дати народження диллерів, які торгують тими і тільки тими типами наркоти, якими торгує диллер Х.
with same_drugs as (
    select distinct contract."IdDrugs"
    from public."Contract" as contract
    where contract."Dealer" = :X
), valid_dealers as (
    select distinct dealer."Passport"
    from public."Dealer" as dealer
        inner join public."Contract" contract on dealer."Passport" = contract."Dealer"
        inner join same_drugs sd on sd."IdDrugs" = contract."IdDrugs"
    where 1=1
        and contract."Dealer" <> :X
    group by dealer."Passport"
    having count(distinct contract."IdDrugs") in (select count("IdDrugs") from same_drugs)
)
select dealer."Name", dealer."Birthday"
from public."Dealer" as dealer
    inner join valid_dealers vd on vd."Passport" = dealer."Passport"; -- e.g. X: 'dealer5'

-- DealerOfSuchCountOfTypesAs
-- Вивести дилерів з такою ж кількістю типів наркоти, як і дилер Х, та кількість цих типів.
with same_drugs_type_count as (
    select count(distinct drugs."Type") as "TypesCount"
    from public."Contract" as contract
        inner join public."Drugs" drugs on contract."IdDrugs" = drugs."IdDrugs"
    where contract."Dealer" = :X
), valid_dealers as (
    select distinct dealer."Passport", count(distinct drugs."Type") as "TypesCount"
    from public."Dealer" as dealer
        inner join public."Contract" contract on dealer."Passport" = contract."Dealer"
        inner join public."Drugs" drugs on contract."IdDrugs" = drugs."IdDrugs"
    where 1=1
        and contract."Dealer" <> :X
    group by dealer."Passport"
)
select dealer.*, vd."TypesCount"
from public."Dealer" as dealer
    inner join valid_dealers vd on vd."Passport" = dealer."Passport"
where 1=1
    and vd."TypesCount" in (select "TypesCount" from same_drugs_type_count); -- e.g. X: 'dealer1'

-- LabWithDrugsQualityGEQ
-- Вивести всі лабораторії, які виготовляють наркоту з якістю не менше, ніж Х.
select distinct lab.*
from public."Drugs" drugs
    inner join public."Lab" lab on lab."IdLab" = drugs."IdLab"
where 1=1
    and drugs."Quality" >= :X; -- e.g. X: 80