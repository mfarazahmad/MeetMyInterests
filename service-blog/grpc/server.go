package grpc

import (
	"net"
	c "service-blog/config"
	"service-blog/grpc/pb"

	"github.com/rs/zerolog/log"
	grpc "google.golang.org/grpc"
)

func CreateTCPListener() net.Listener {
	log.Printf("Listen to TCP on port %s", c.CFG.APP_PORT)

	lis, err := net.Listen("tcp", c.CFG.APP_PORT)
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

	pb.RegisterBloggerServiceServer(grpcServer, &BloggerServer{})
	log.Print("GRPC Server Listening at %v", lis.Addr())

	err := grpcServer.Serve(lis)
	if err != nil {
		log.Print("Failed to serve: %v", err)
	}
}
