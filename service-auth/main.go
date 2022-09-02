package main

import (
	"service-auth/config"
	"service-auth/grpc"

	"github.com/rs/zerolog/log"
)

func main() {
	log.Print("Starting Auth Service")
	config.Bootstrap()
	lis := grpc.CreateTCPListener()
	server := grpc.CreateGrpcServer()
	grpc.RegisterRoutesToGRPC(lis, server)
}
