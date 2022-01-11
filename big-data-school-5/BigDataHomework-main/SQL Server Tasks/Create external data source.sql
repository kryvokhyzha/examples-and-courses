CREATE DATABASE SCOPED CREDENTIAL AzureStorageKey
WITH IDENTITY = 'ADLS_Any_String', Secret = 'ДАННЫЕ УДАЛЕНЫ';
GO

CREATE EXTERNAL DATA SOURCE samoshyn_blob 
with (  
      TYPE = HADOOP,
      LOCATION ='wasbs://container01@samoshyn01.blob.core.windows.net',  
      CREDENTIAL = AzureStorageKey
);  
GO
