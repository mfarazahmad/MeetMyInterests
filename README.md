# Welcome to MeetMyInterests!

## This application serves as a portal into my professional background and interests.

![](MeetMyInterests.png)

## Services
- Responsive, Interactive UI to Showcase Professional Experience (ui-meetmyinterests)
    - React/ Next.js (SSR)
    - HTML5 Canvas
    - Media Queries
    - Grid/Flexbox
    - Antd Design
    - Webp Image Formats
- Services Broken into a Domain Driven Microservices Architecture (golang)
    - service-portfolio 
    - service-media
    - service-blog 
    - service-fitness-tracker
    - service-analytics
    - service-auth

## Technologies
- Containerization via Docker & Managed by Kubernetes & Helm Charts
- Isitio leveraged as API Gateway for Load Balancing
- Isitio used as Service Mesh for service discovery
- Deloyed on Azure AKS via Terraform
- Utilizing Redis for Cacheing of User Sessiom
- MongoDB Cluster Sharding w/ 3 nodes
- Logging using Datadog
- 100% Code Coverage
- Linters used: 
- Passwords are hashed using a Argon2id hash function using Blake2.
- Pipeline Orchestrator coming soon! (Harness)

## Local Setup

### Languages
```
choco install golang
choco install nodejs
choco install protoc

```

* Notice about PBs
1. PBs and .proto files are used to define messaging and the functions utilized in a GRPC service. 

2. The PB file is generated by running the below command in the communicating service's language. It can then be imported, registered to a GRPC server, and then invoked from the client.

```
protoc \
--go_out=. --go_opt=paths=source_relative \
--go-grpc_out=. --go-grpc_opt=paths=source_relative \
blog.proto

protoc \
--go_out=. --go_opt=paths=source_relative \
--go-grpc_out=. --go-grpc_opt=paths=source_relative \
auth.proto
```

### Infrastructure
```
choco install azure-cli
choco install docker
choco install terraform
choco install kubernetes-cli
choco install kubernetes-helm
choco install minikube
```

## Running Containers Locally
```
docker run -p 9100:9100 service-portfolio
docker run -p 9101:9101 service-blog
docker run -p 3000:3000 meetmyinterests
```

### Swagger

### Linter
Linting is utilized to maintain a safe, readable, and consistent coding standard throughout the services.

- golangci-lint is used as the primary linter for the go services as it has many different types of linters avaiable.
- eslinter is used as the linter for the node/next.js project

```
make testcoverage && make lint
```
## Coming Soon!
- Full Blog with Technical Tutorial Posts & Journey | Gifs, Images, Charts
- Fitness Tracker (For Weightlifting, Full Body | Upper-Lower | PPL)
- Photography Gallery
- Singing Videos
- Guitar Tracker