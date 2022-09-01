package config

import (
	"os"

	"github.com/rs/zerolog/log"

	"github.com/joho/godotenv"
)

var (
	CFG APP
)

type APP struct {
	APP_PORT string
	DATABASE DB
}

type DB struct {
	HOST       string
	CLIENT     string
	COLLECTION string
}

func Bootstrap() {
	log.Print("Creating config!")

	err := godotenv.Load()
	if err != nil {
		log.Print("No .env file found")
	}

	CFG = APP{
		APP_PORT: ":8001",
		DATABASE: DB{
			HOST:       os.Getenv("MONGO_URI"),
			CLIENT:     "blog",
			COLLECTION: "posts",
		},
	}
}
