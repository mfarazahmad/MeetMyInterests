package config

import (
	"crypto/rsa"
	"os"
	"path/filepath"

	"github.com/golang-jwt/jwt/v4"
	"github.com/joho/godotenv"
	"github.com/rs/zerolog/log"
)

var (
	CFG APP
)

type APP struct {
	APP_PORT    string
	APP_DB      DATABASE
	PRIVATE_KEY *rsa.PrivateKey
}

type DATABASE struct {
	HOST       string
	DB         string
	COLLECTION string
}

func getPrivateKey() *rsa.PrivateKey {
	privateKeyPath, _ := filepath.Abs("keys/app.rsa") // openssl genrsa -out app.rsa keysize
	log.Print(privateKeyPath)

	signBytes, err := os.ReadFile(privateKeyPath)
	if err != nil {
		log.Print("No private key found!")
	}

	signKey, err := jwt.ParseRSAPrivateKeyFromPEM(signBytes)
	if err != nil {
		log.Print("Failed to parse private key from file!")
	}

	return signKey
}

func Bootstrap() {
	log.Print("Setting up config!")

	err := godotenv.Load()
	if err != nil {
		log.Print("No .env file found")
	}

	CFG = APP{
		APP_PORT: ":8002",
		APP_DB: DATABASE{
			HOST:       os.Getenv("MONGO_URI"),
			DB:         "auth",
			COLLECTION: "creds",
		},
		PRIVATE_KEY: getPrivateKey(),
	}
}
