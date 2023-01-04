package config

import (
	"crypto/rsa"
	"fmt"
	"os"
	"path/filepath"
	pb "service-backend/grpc"

	"github.com/golang-jwt/jwt/v4"
	"github.com/rs/zerolog/log"

	"github.com/gorilla/sessions"
	"google.golang.org/grpc"

	"crypto/rand"
	"encoding/base32"
)

var (
	CFG           APP
	NEW_WHITELIST = []string{"http://localhost:3000"}
	STORE         = sessions.NewCookieStore([]byte(createSessionSecret(10)))
)

type APP struct {
	CLIENTS    map[string]GRPC_SERVERS
	APP_PORT   string
	WHITELIST  []string
	PUBLIC_KEY *rsa.PublicKey
	SESSION    *sessions.CookieStore
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
	publicKeyPath, _ := filepath.Abs("keys/app.rsa.pub") //openssl rsa -in app.rsa -out app.rsa.pub -pubout -outform PEM
	log.Print(publicKeyPath)

	verifyBytes, err := os.ReadFile(publicKeyPath)
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
	var serviceMap []GRPC_INIT_CONN

	if currentEnv := os.Getenv("ENV"); currentEnv == "staging" {
		serviceMap = []GRPC_INIT_CONN{
			{HOST: "blog-service", PORT: "8001", NAME: "blog"},
			{HOST: "auth-service", PORT: "8002", NAME: "auth"},
		}
	} else {
		serviceMap = []GRPC_INIT_CONN{
			{HOST: "localhost", PORT: "8001", NAME: "blog"},
			{HOST: "localhost", PORT: "8002", NAME: "auth"},
		}
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

func createSessionSecret(length int) string {
	randomBytes := make([]byte, 32)
	_, err := rand.Read(randomBytes)
	if err != nil {
		return "fun_times_shared_by_all"
	}
	return base32.StdEncoding.EncodeToString(randomBytes)[:length]
}

func Bootstrap() {
	log.Print("Creating config!")

	GRPC_SERVERS := connectToGRPCBackend()

	if currentEnv := os.Getenv("ENV"); currentEnv == "staging" {
		NEW_WHITELIST = append(NEW_WHITELIST, "http://ui-mmi-service:3000")
	}

	CFG = APP{
		WHITELIST:  NEW_WHITELIST,
		CLIENTS:    GRPC_SERVERS,
		APP_PORT:   "9001",
		PUBLIC_KEY: getPublicKey(),
		SESSION:    STORE,
	}
}
