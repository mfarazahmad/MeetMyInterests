package main

import (
	"net"
	"service-blog/pb"

	"github.com/rs/zerolog/log"
	"google.golang.org/grpc"
)

func main() {
	lis := createServer()
	grpcServer := createGrpcServer()
	registerRoutesToGRPC(lis, grpcServer)
}

func createServer() net.Listener {
	log.Print("Listen to TCP on port 8001")

	lis, err := net.Listen("tcp", ":8001")
	if err != nil {
		log.Print("Failed to listen: %v", err)
	}

	return lis
}

func createGrpcServer() *grpc.Server {
	log.Print("Creating GRPC Server")

	var opts []grpc.ServerOption
	grpcServer := grpc.NewServer(opts...)

	return grpcServer
}

func registerRoutesToGRPC(lis net.Listener, grpcServer *grpc.Server) {
	log.Print("Registering Routes on GRPC Server")

	pb.RegisterBloggerServiceServer(grpcServer, &pb.BloggerServer{})
	log.Print("GRPC Server Listening at %v", lis.Addr())

	err := grpcServer.Serve(lis)
	if err != nil {
		log.Print("Failed to serve: %v", err)
	}
}
