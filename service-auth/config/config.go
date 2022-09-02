package config

import (
	"os"

	"github.com/joho/godotenv"
	"github.com/rs/zerolog/log"
)

var (
	CFG APP
)

type APP struct {
	APP_PORT string
	APP_DB   DATABASE
}

type DATABASE struct {
	HOST       string
	DB         string
	COLLECTION string
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
	}
}
