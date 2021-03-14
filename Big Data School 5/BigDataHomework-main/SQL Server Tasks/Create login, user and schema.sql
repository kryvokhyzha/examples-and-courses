use [master]
CREATE LOGIN samoshyn WITH PASSWORD='ДАННЫЕ УДАЛЕНЫ'
CREATE USER samoshyn FOR LOGIN samoshyn

use [sqldwschool]
CREATE SCHEMA samoshyn_schema 
GO
CREATE USER [samoshyn] FOR LOGIN [samoshyn] WITH DEFAULT_SCHEMA=[samoshyn_schema]
GO
EXEC sp_addrolemember N'db_owner', N'samoshyn'
GO
