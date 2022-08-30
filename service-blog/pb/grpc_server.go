package pb

import (
	"net"

	"github.com/rs/zerolog/log"
	grpc "google.golang.org/grpc"
)

func CreateTCPListener() net.Listener {
	log.Print("Listen to TCP on port 8001")

	lis, err := net.Listen("tcp", ":8001")
	if err != nil {
		log.Print("Failed to listen: %v", err)
	}

	return lis
}

func CreateGrpcServer() *grpc.Server {
	log.Print("Creating GRPC Server")

	var opts []grpc.ServerOption
	grpcServer := grpc.NewServer(opts...)

	return grpcServer
}

func RegisterRoutesToGRPC(lis net.Listener, grpcServer *grpc.Server) {
	log.Print("Registering Routes on GRPC Server")

	RegisterBloggerServiceServer(grpcServer, &BloggerServer{})
	log.Print("GRPC Server Listening at %v", lis.Addr())

	err := grpcServer.Serve(lis)
	if err != nil {
		log.Print("Failed to serve: %v", err)
	}
}
