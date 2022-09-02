package main

import (
	"service-blog/config"
	"service-blog/grpc"
)

func main() {
	config.Bootstrap()

	lis := grpc.CreateTCPListener()
	grpcServer := grpc.CreateGrpcServer()
	grpc.RegisterRoutesToGRPC(lis, grpcServer)
}
