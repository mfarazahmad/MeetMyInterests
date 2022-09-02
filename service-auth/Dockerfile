# syntax=docker/dockerfile:1

## Build
FROM golang:1.19-alpine AS BUILD

WORKDIR /app

COPY go.mod ./
COPY go.sum ./
RUN go mod download

COPY . ./

RUN go build -o /service-auth

EXPOSE 9100

CMD ["/service-auth"]