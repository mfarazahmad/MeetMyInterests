package grpc

import (
	"github.com/rs/zerolog/log"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

func CreateGrpcConnnection(serverAddr string) *grpc.ClientConn {
	var opts []grpc.DialOption
	opts = append(opts, grpc.WithTransportCredentials(insecure.NewCredentials()))
	log.Print("Connecting to service")
	conn, err := grpc.Dial(serverAddr, opts...)
	if err != nil {
		log.Print("Failed to dial to service: %v", err)
	}

	return conn
}
