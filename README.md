# Welcome to MeetMyInterests!

## This application serves as a portal into my professional background and interests.

![](MeetMyInterests.png)

## Coming Soon v1.0
- Terraform Scripts for EKS
- Datadog Dashboard Link

## Coming One Day v2.0
- Streaming & Transcoding for service-media-stream

## Services
- Services Broken into a Domain Driven Microservices Architecture 
    - **golang**
        - service-interests 
        - service-blog 
        - service-fitness-tracker
        - service-auth
    - **python**
        - service-analytics
    - **node/typescript**
        - service-notifcation
        - service-email
        - service-media-stream

Service-Blog has a CQRS (Command-Query Responsbility Segregation) Architecture to Seperate Read & Writes operations for better scalability. An event bus via Kafka is used for sync across the write to read database.

- Responsive, Interactive UI to Showcase Professional Experience (ui-meetmyinterests)
    - React/ Next.js (SSR)
    - HTML5 Canvas
    - Media Queries
    - Grid/Flexbox
    - Antd Design
    - Webp Image Formats

## Technologies
- Containerization via Docker & Managed by Kubernetes & Helm Charts
- Isitio leveraged as API Gateway for Load Balancing
- Isitio used as Service Mesh for service discovery
- Deployed on Amazon EKS via Terraform
- Pipeline Orchestrator via Harness w/ Sonarcube Integration
- Utilizing Redis for Cacheing of Media for Streaming
- Sensitive Configuration stored/ retrieved in Hasicorp Vault
- MongoDB Cluster Sharding w/ 3 nodes
- Logging using Datadog
- 100% Code Coverage
- Linters used: 
- Passwords are hashed using a Argon2id hash function using Blake2.
- Oauth2 Integration w/ Google
- Canary integrations for gradual rollouts

## Local Setup

### Languages
```
choco install golang
choco install nodejs
choco install python
choco install protoc

```

### How to use the .proto files to generate code for your application
* Notice about PBs
1. PBs and .proto files are used to define messaging and the functions utilized in a GRPC service. 

2. The PB file is generated by running the below command in the communicating service's language. It can then be imported, registered to a GRPC server, and then invoked from the client.

* Make sure your GoPath is set before generating these
```
vi ~./zshrc
    export GOPATH=$HOME/go
    export PATH=$PATH:$GOPATH/bin
```

```
brew install protobuf
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest

protoc \
--go_out=. --go_opt=paths=source_relative \
--go-grpc_out=. --go-grpc_opt=paths=source_relative \
blog.proto

protoc \
--go_out=. --go_opt=paths=source_relative \
--go-grpc_out=. --go-grpc_opt=paths=source_relative \
auth.proto
```

## Credential Setup
* In order to run these services you will need to create credentials

### Create Service Credentials
```
cd service-auth
mkdir keys
cd keys
openssl genrsa -out app.rsa 1024

cd service-interets
mkdir keys
cd keys
openssl rsa -in app.rsa -out app.rsa.pub -pubout -outform PEM
```

### Create Oauth Credentials
1. Go to Google Cloud Credentials Page
2. Click Create New Credentials and in the Drop Down Select Oauth2
3. Select Web Application as the application type
4. Entire in http://localhost:3000 as the the redirect uri
5. Save and download the credentials and place in the root of service-auth

### Infrastructure
```
choco install aws-cli
choco install docker
choco install terraform
choco install kubernetes-cli
choco install kubernetes-helm
choco install minikube
```

## Running Containers Locally
```
docker run -p 9100:9100 service-interests
docker run -p 8001:8001 service-blog
docker run -p 8002:8002 service-auth
docker run -p 3000:3000 meetmyinterests
```

## Running Locally with Minikube & Helm
```
helm repo add mongodb https://mongodb.github.io/helm-charts
helm install community-operator mongodb/community-operator

docker login
minikube start
minikube tunnel

. deploy/deploy.sh - Start all services
. deploy/takedown.sh - Takedown all services
```

# Encoding & Decoding Secrets
echo "devopscube" | base64 
//after encoding it, this becomes ZGV2b3BzY3ViZQo=

echo "ZGV2b3BzY3ViZQo=" | base64 --decode
//after decoding it, this will give devopscube

To get Docker Private Repository Key
1. ```docker login```
2. ```cat ~/.docker/config.json | base64```  
3. Copy above to dockerBase64Token in values.yaml

### Swagger

### Linter
Linting is utilized to maintain a safe, readable, and consistent coding standard throughout the services.

- golangci-lint is used as the primary linter for the go services as it has many different types of linters avaiable.
- eslinter is used as the linter for the node/next.js project

```
make testcoverage && make lint
```