package main

import (
	"service-blog/config"
	"service-blog/pb"
)

func main() {
	config.Bootstrap()

	lis := pb.CreateTCPListener()
	grpcServer := pb.CreateGrpcServer()
	pb.RegisterRoutesToGRPC(lis, grpcServer)
}
