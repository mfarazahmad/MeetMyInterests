package config

import (
	"crypto/rsa"
	"encoding/json"
	"os"
	"path/filepath"
	"strings"

	m "service-auth/models"

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
	AUTH        OAUTH
	PRIVATE_KEY *rsa.PrivateKey
}

type OAUTH struct {
	CREDS        m.OauthCredentials
	SCOPES       []string
	REDIRECT_URI string
}

type DATABASE struct {
	HOST       string
	DB         string
	COLLECTION string
}

func getPrivateKey() *rsa.PrivateKey {
	privateKeyPath, _ := filepath.Abs("keys/app.rsa") // openssl genrsa -out app.rsa 1024
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

func getOauthCreds() m.OauthCredentials {
	authCreds, _ := filepath.Abs("keys/client_secret.json")
	log.Print(authCreds)

	fileBytes, err := os.ReadFile(authCreds)
	if err != nil {
		log.Print("No oauth creds found!")
		return m.OauthCredentials{}
	}

	var creds m.OauthCredentials
	err = json.Unmarshal(fileBytes, &creds)
	if err != nil {
		log.Print("Error during Unmarshal(): ", err)
		return m.OauthCredentials{}
	}

	return creds
}

func Bootstrap() {
	log.Print("Setting up config!")

	if currentEnv := os.Getenv("ENV"); currentEnv != "staging" {
		err := godotenv.Load()
		if err != nil {
			log.Print("No .env file found")
		}
	}

	CFG = APP{
		APP_PORT: ":8002",
		APP_DB: DATABASE{
			HOST:       os.Getenv("MONGO_URI"),
			DB:         "auth",
			COLLECTION: "creds",
		},
		AUTH: OAUTH{
			CREDS:        getOauthCreds(),
			SCOPES:       strings.Split(os.Getenv("AUTH_SCOPES"), ","),
			REDIRECT_URI: os.Getenv("AUTH_REDIRECT_URL"),
		},
		PRIVATE_KEY: getPrivateKey(),
	}
}
