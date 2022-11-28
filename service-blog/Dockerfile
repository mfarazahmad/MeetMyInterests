# syntax=docker/dockerfile:1

## Build
FROM golang:1.19 AS BUILD

WORKDIR /app

COPY go.mod .
COPY go.sum .
RUN go mod download

COPY . .

RUN go build -o /service-blog

# Deploy 

FROM debian:latest

WORKDIR /usr/local/bin

COPY --from=build /service-blog /usr/local/bin/service-blog

EXPOSE 8001

ENTRYPOINT [ "/usr/local/bin/service-blog" ]