package main

import (
	"service-blog/pb"
)

func main() {
	lis := pb.CreateTCPListener()
	grpcServer := pb.CreateGrpcServer()
	pb.RegisterRoutesToGRPC(lis, grpcServer)
}
