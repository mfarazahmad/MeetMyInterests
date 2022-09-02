package repo

import (
	"context"
	c "service-auth/config"

	"github.com/rs/zerolog/log"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type db struct {
	HOST       *mongo.Client
	CLIENT     *mongo.Database
	COLLECTION *mongo.Collection
}

var (
	ctx context.Context
)

func ConnectToDB() (db, error) {
	log.Print("Connecting to Database")
	log.Print(c.CFG.APP_DB.COLLECTION)
	host, err := mongo.Connect(ctx, options.Client().ApplyURI(c.CFG.APP_DB.HOST))
	if err != nil {
		log.Print("Failed to connect to DB")
		return db{}, err
	}

	client := host.Database(c.CFG.APP_DB.DB)
	coll := client.Collection(c.CFG.APP_DB.COLLECTION)

	return db{
		HOST:       host,
		CLIENT:     client,
		COLLECTION: coll,
	}, nil
}
