 ## How to install MLFlow with Docker

```
docker compose up -d
```
## To Enter CMD in Docker Container

fist you need to know container id or container name
```
docker ps
```

then you can enter the cmd
```
docker exec -it <container_id_or_name> /bin/bash

```



you can go to http://localhost:5000/ for MLFlow UI
you can go to http://localhost:8900/buckets for Minio Object Store
you can go to http://localhost:8888 for jupyterlab notebook

credit to https://blog.vidio.com/create-ml-workflows-with-mlflow-and-docker/ for the installation
