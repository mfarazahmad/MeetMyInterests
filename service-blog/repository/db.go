package repository

import (
	"context"
	c "service-blog/config"

	"github.com/rs/zerolog/log"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

var (
	ctx context.Context
)

type DB_CONNECTION struct {
	CLIENT     *mongo.Client
	DATABASE   *mongo.Database
	COLLECTION *mongo.Collection
}

func ConnectToDB() DB_CONNECTION {
	log.Print("Connecting to Mongo DB")

	client, err := mongo.Connect(ctx, options.Client().ApplyURI(c.CFG.DATABASE.HOST))
	if err != nil {
		log.Print(err.Error())
	}

	db := client.Database(c.CFG.DATABASE.CLIENT)
	col := db.Collection(c.CFG.DATABASE.COLLECTION)

	return DB_CONNECTION{
		CLIENT:     client,
		DATABASE:   db,
		COLLECTION: col,
	}
}
