# Demo Project Quick Guide 

## Structure
- /src
  - Contians all microservices
  - Each microservice is in its own directory with a Dockerfile
- /docker-compose
  - Contains config files to run docker compose
- /k8s: NOT USED
  - Contains config files to run a k8s cluster

## Expectation
- To run docker compose, a basic idea of what docker is and how to use it is expected.
- Spend some time learning how to build images and running containers so that you have context 

## Running Docker-Compose
- See this video for to learn about docker compose: https://www.youtube.com/watch?v=SXwC9fSwct8
1) Download Docker Desktop
   - This comes with docker compose built in
2) Ensure docker engine is running and is working
3) Clone the demo repository onto your machine
4) In the terminal, navigate to DEMO/docker-compose
5) Run `docker compose -f demo-app.yaml build`
   - This may take a while to download all dependancies and images
6) Run `docker compose -f demo-app.yaml up -d`
   - This will start all the microservices, you should see an output like:
7) Browse to localhost:8089 to see it in action
   - The default un&pw is "admin"
```
 [+] Running 7/7
 ✔ Container docker-compose-accounts-1       Started 
 ✔ Container docker-compose-webapp-1         Started 
 ✔ Container docker-compose-permissions-1    Started 
 ✔ Container docker-compose-sessions-1       Started 
 ✔ Container docker-compose-nginx-1          Started 
 ✔ Container docker-compose-mongo-1          Started 
 ✔ Container docker-compose-mongo-express-1  Started 
 ```

## Understanding docker-compose
[This file](docker-compose/demo-app.yaml) contains the blueprint for which docker images to create and run

For example, 
```
accounts:
    build: ../src/Accounts
    ports:
      - 50001:8080
```

### "accounts:"
This will create a docker container for the "accounts" service.
- By default, the service will only be available inside the cluster. 
- Other services can access this one by using http://[name] `http://accounts`
- Docker compose will use an internal DNS system to route traffic within the cluster

### "build: ../src/Accounts"
This tells docker compose where to get (or build) the docker image
This will build and run a dockerfile at DEMO/src/accounts/Dockerfile
- You can replace it with `image: my-dockerhub-image:tag` to get remote images

### "ports: - 50001:8080"
This will give your host (main computer) direct access to the service
- Ie, you can use your browser to go to http://localhost:50001 to interact with the service directly
- This is only for debugging & development. In production, we want to only allow ingress through our ingress controller (nginx)


## Useful commands
You've already seen a couple useful commands from docker compose, but here are some more:
- `docker compose -f demo-app.yaml build` : this must be run to before `up` for your changes to be visible
  - the -f flag can be used with a file path if you are not in the docker-compose directory
- `docker compose -f demo-app.yaml up -d` starts the cluster and spins up all services
  - -d is used to detach the cluster from your terminal, it is not necessary
- `docker compose -f demo-app.yaml down` used to shut down the cluster
- `docker container logs {container ID}` Used to view the stdio output from a specific container
  - Use with `docker container ls -a` to get a list of docker containers with their names and IDs


### Docker Compose
- Docker compose is very powerful, please explore and learn about it as much as you want. 

## Nginx
Nginx is a tool to route and control traffic into a server. It is very powerful, and we are only using a small part of its capabilities.

In the docker compose yaml file, we have an entry like
```
nginx:
  image: nginx:stable-alpine-slim
  ports:
    - 8089:80
    - 80:80
  volumes:
    - ./configs/nginx.conf:/etc/nginx/nginx.conf
```

This will:
- get the nginx image from docker hub
- redirect traffic from ports 8089 80 from your localhost into port 80 of Nginx
- It give nginx access to the nginx.conf file where routing information is stored

### Nginx.conf
```
events {}

http {
    server {
        listen 80;

        location / {
            proxy_pass http://webapp:8080;
        }

        location /accounts/ {
            proxy_pass http://accounts:8080;
        }
        
        location /permissions/ {
            proxy_pass http://permissions:8080;
        }
        
        location /sessions/ {
            proxy_pass http://sessions:8080;
        }
    }
}
```
This is a very basic Nginx configuration. It is simply redirects incoming traffic to the various servers based on the url.

For example, `http://nginx/accounts` will be redirected to `http://accounts:8080/accounts`

NOTE: when browsing, `http://[anySite]`, it is identical to browsing to `http://[anySite]:80`. So if you want to not use explicit port numbers, ensure your service listens on port 80.
