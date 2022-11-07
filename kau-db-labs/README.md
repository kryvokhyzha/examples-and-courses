# DB Labs

## 01-lab

### Report

1. Setup PostgreSQL
'''bash
docker run --rm --name pg-docker -e POSTGRES_PASSWORD=cramstack@2018 -d -p 5432:5432 -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data postgres
'''
2. DealerQuery
![DealerQuery](img/01-01-query.png)
3. DealerWithSuchDrugsTypesAs
![DealerWithSuchDrugsTypesAs](img/01-02-query.png)
4. ContrabandistQuery
![ContrabandistQuery](img/01-03-query.png)
5. DealerWithOnlySuchDrugTypesAs
![DealerWithOnlySuchDrugTypesAs](img/01-04-query.png)
6. DealerOfSuchCountOfTypesAs
![DealerOfSuchCountOfTypesAs](img/01-05-query.png)
7. LabWithDrugsQualityGEQ
![LabWithDrugsQualityGEQ](img/01-06-query.png)
