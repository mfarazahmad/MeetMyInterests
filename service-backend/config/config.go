package config

import (
	"crypto/rsa"
	"fmt"
	"os"
	pb "service-backend/grpc"

	"github.com/golang-jwt/jwt/v4"
	"github.com/rs/zerolog/log"

	"google.golang.org/grpc"
)

var (
	CFG             APP
	NEW_WHITELIST   = []string{"http://localhost:3000"}
	PUBLIC_KEY_PATH = "keys/app.rsa.pub"
)

type APP struct {
	CLIENTS    map[string]GRPC_SERVERS
	APP_PORT   string
	WHITELIST  []string
	PUBLIC_KEY *rsa.PublicKey
}

type GRPC_SERVERS struct {
	CONNECTION *grpc.ClientConn
}

type GRPC_INIT_CONN struct {
	NAME string
	HOST string
	PORT string
}

func getPublicKey() *rsa.PublicKey {
	verifyBytes, err := os.ReadFile(PUBLIC_KEY_PATH)
	if err != nil {
		log.Print("No public key found!")
	}

	verifyKey, err := jwt.ParseRSAPublicKeyFromPEM(verifyBytes)
	if err != nil {
		log.Print("Failed to parse public key from file!")
	}

	return verifyKey
}

func connectToGRPCBackend() map[string]GRPC_SERVERS {
	serviceMap := []GRPC_INIT_CONN{
		{HOST: "localhost", PORT: "8001", NAME: "blog"},
		{HOST: "localhost", PORT: "8002", NAME: "auth"},
	}

	newClient := map[string]GRPC_SERVERS{}

	for _, service := range serviceMap {
		hostname := fmt.Sprintf("%s:%s", service.HOST, service.PORT)
		conn := pb.CreateGrpcConnnection(hostname, service.NAME)

		clientConnection := GRPC_SERVERS{CONNECTION: conn}
		newClient[service.NAME] = clientConnection
	}

	return newClient
}

func Bootstrap() {
	log.Print("Creating config!")

	GRPC_SERVERS := connectToGRPCBackend()

	CFG = APP{
		WHITELIST:  NEW_WHITELIST,
		CLIENTS:    GRPC_SERVERS,
		APP_PORT:   "9001",
		PUBLIC_KEY: getPublicKey(),
	}
}
