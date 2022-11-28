# syntax=docker/dockerfile:1

## Build
FROM golang:1.19 AS BUILD

WORKDIR /app

COPY go.mod .
COPY go.sum .
RUN go mod download

COPY . .
COPY /keys /keys

RUN go build -o /service-auth

# Deploy 

FROM debian:latest

WORKDIR /usr/local/bin

COPY --from=build /keys /usr/local/bin/keys

COPY --from=build /service-auth /usr/local/bin/service-auth

EXPOSE 8002

ENTRYPOINT [ "/usr/local/bin/service-auth" ]