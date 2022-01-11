# Run project
1. Clone this repo

Create a new folder with project name, cd into it, and then run:

```
git init
git pull https://github.com/kryvokhyzha/basic-docker-container-for-ds.git
```

2. Add your favorite Python modules to ./docker/jupyter/requirements.txt. For example:

```
statsmodels
torch==1.3
```

3. Change image name in docker-compose file:
```
...
    image: docker_user/app_name:tag
...
```

4. Run containers:

```
docker-compose up
```
or
```
docker-compose up --build
```

5. Copy a jupyter url from terminal and open it in your browser

6. Create your notebook in _notebooks_ folder

7. Copy your data into ./data and read it in Jupyter. You also can upload data into PostgresSQL, which is running in it's own container along with Jupyter

8. Close terminal to stop running jupyter and postgres

9. Stop containers and removes containers, networks, volumes, and images:

```
docker-compose down
```

10. Clean Docker's mess:

```
docker rmi -f $(docker images -qf dangling=true)
```

Sometimes it is useful to remove all docker's data:

```
docker system prune
```

# Disable PostgreSQL server
1. Go to the file _docker-complose.yml_
2. Delete _volumes_ section under _db_
3. Delete whole _db_ section 
4. Run project (see previous paragraph)

Now, _docker-compose.yml_ looks like:
```
version: '3'
services: 
    jupyter:
        build: 
            context: ./docker/jupyter/
            dockerfile: Dockerfile
        volumes: 
            - .:/home/jovyan/
        ports: 
            - "8888:8888"
        environment: 
            - JUPYTER_ENABLE_LAB=yes
```

# Usefull commnads

### Show running containers
```
docker ps
```

### Show all containers
```
docker ps --all
```

### Show all top level images
```
docker images
```

### Build container
```
docker -t build <tag-name> .
```
_this command works, when Dockerfile is placed in current directory_

### Run container with volume
```
docker run --rm -p <local-port>:<docker-port> -e JUPYTER_ENABLE_LAB=yes -v "$PWD":/home/jovyan/ <tag-name>
```
_PWD_ - prints the path of the working directory, starting from the root

### Create volume for postgresql
```
docker volume create pgdata
```

_pgdata_ - is volume name for postgresql

### Docker compose up
```
docker-compose up
```

### Docker compose up with build
```
docker-compose up --build
```

### Docker compose down
```
docker-compose down
```

### Attach to running container
```
docker exec -it <mycontainerID> bash
```

### Copy file into the running container
```
docker cp <data-filename> <mycontainerID>:/home/jovyan/<data-filename>
```

