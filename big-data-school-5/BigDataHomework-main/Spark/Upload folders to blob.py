from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient,PublicAccess
import os


def upload_to_blob(r, path_remove, file, container):
    file_path_on_azure = os.path.join(r,file).replace(path_remove,"")
    file_path_on_local = os.path.join(r,file)
    #print(file_path_on_local)

    blob_client = container.get_blob_client(file_path_on_azure)

    with open(file_path_on_local,'rb') as data:
        blob_client.upload_blob(data)

def run_sample():    
    conn_str="DefaultEndpointsProtocol=https;AccountName=mlstorageall;AccountKey=djvx9juh6EJZWqx7T3U2D61BwhPWyEx4BcVyzbt/AQhaNR8hGmVBtzaJnbbG2w4c67p4dZkZIAWK6kq1PbV8Zg==;EndpointSuffix=core.windows.net"
    container_name="samoshyn"    
    
    path_remove = "D:\\Big_Data_School_5\DataFrame\Lesson_2\Geolife_Trajectories_1_3\\"
    local_path = "D:\\Big_Data_School_5\DataFrame\Lesson_2\Geolife_Trajectories_1_3\AllData_preprocess" #the local folder

    service_client=BlobServiceClient.from_connection_string(conn_str)
    container_client = service_client.get_container_client(container_name)  
    
    file_check = 0
    file = None
    total = 0
    for r,d,f in os.walk(local_path):
        
        if file_check==1:
            #print(r)
            total = total + 1
            for file in f:
                #print(os.path.join(r,file))
                upload_to_blob(r, path_remove, file, container_client)
            print('Upload user:', total)
            file_check = 0
        if f:
            
            for file in f:
               #print(file)    
               if file=='labels_csv.csv':
                    #print(os.path.join(r,file))
                    upload_to_blob(r, path_remove, file, container_client)
                    file_check = 1
    print('----Total users:', total)



if __name__ == '__main__':
    '''file_check = None
    for r,d,f in os.walk("D:\\testfolder01"):
        if file_check==1:
            print(r,'next get upload')
        for file in f:
            if file=='labels.txt':
                print(r,'get upload')
                file_check = 1'''
    run_sample()
    print("**completed**")