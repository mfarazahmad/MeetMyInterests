package grpc

import (
	context "context"
	"time"

	"github.com/rs/zerolog/log"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

func CreateGrpcConnnection(serverAddr string, serviceName string) *grpc.ClientConn {
	ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)

	var opts []grpc.DialOption
	opts = append(opts, grpc.WithTransportCredentials(insecure.NewCredentials()))
	log.Printf("Connecting to service %s", serviceName)
	conn, err := grpc.DialContext(ctx, serverAddr, opts...)
	if err != nil {
		log.Printf("Failed to dial to service: %v", err)
	}

	return conn
}
