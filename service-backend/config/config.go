package config

import (
	"fmt"
	"service-portfolio/pb"

	"google.golang.org/grpc"
)

var (
	CFG APP
)

type APP struct {
	CLIENTS  map[string]GRPC_SERVERS
	APP_PORT string
}

type GRPC_SERVERS struct {
	CONNECTION *grpc.ClientConn
}

type GRPC_INIT_CONN struct {
	NAME string
	HOST string
	PORT string
}

func connectToGRPCBackend() map[string]GRPC_SERVERS {
	serviceMap := []GRPC_INIT_CONN{
		{HOST: "localhost", PORT: "8001", NAME: "blog"},
	}

	newClient := map[string]GRPC_SERVERS{}

	for _, service := range serviceMap {
		hostname := fmt.Sprintf("%s:%s", service.HOST, service.PORT)
		conn := pb.CreateGrpcConnnection(hostname)

		clientConnection := GRPC_SERVERS{CONNECTION: conn}
		newClient[service.NAME] = clientConnection
	}

	return newClient
}

func Bootstrap() {

	GRPC_SERVERS := connectToGRPCBackend()

	CFG = APP{
		CLIENTS:  GRPC_SERVERS,
		APP_PORT: "9001",
	}
}
