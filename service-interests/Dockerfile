# syntax=docker/dockerfile:1

## Build
FROM golang:1.19 AS BUILD

WORKDIR /app

COPY go.mod ./
COPY go.sum ./
RUN go mod download

COPY . ./

ARG REPO
ARG BRANCH
ARG COMMIT
ARG MESSAGE

ENV GIT_REPO=$REPO
ENV GIT_BRANCH=$BRANCH
ENV GIT_COMMIT=$COMMIT
ENV GIT_MESSAGE=$MESSAGE

RUN go build -o /service-backend

EXPOSE 9100

CMD ["/service-interests"]