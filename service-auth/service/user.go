package service

import (
	"context"
	"fmt"
	"service-auth/grpc/pb"
	repo "service-auth/repository"

	"github.com/rs/zerolog/log"
	"go.mongodb.org/mongo-driver/bson"
)

var (
	ctx context.Context
)

func lookupUser(username string) (*pb.Credentials, error) {
	log.Print("Checking database for user %s", username)
	lookupCreds := &pb.Credentials{}

	db, err := repo.ConnectToDB()
	if err != nil {
		log.Print("Failed to connect to the database!")
		return lookupCreds, fmt.Errorf("failed to connect to the database")
	}

	err = db.COLLECTION.FindOne(ctx, bson.D{{Key: "username", Value: username}}).Decode(&lookupCreds)
	if err != nil {
		log.Print("Failed to find the user %s", username)
		return lookupCreds, fmt.Errorf("failed to to find the user")
	}

	return lookupCreds, nil
}

func CompareCredentials(creds *pb.Credentials) (bool, error) {
	lookupCreds, err := lookupUser(creds.Username)
	if err != nil {
		return false, err
	}

	hashedPass, err := HashPassword(creds.Password)
	if err != nil {
		return false, err
	}

	if hashedPass == lookupCreds.Password {
		return true, nil
	} else {
		return false, fmt.Errorf("credentials to not match")
	}

}

func SaveUser(creds *pb.Credentials) bool {
	isValidPass := validatePassword(creds.Password)
	isValidUserName := validateUsername(creds.Username)

	if isValidPass && isValidUserName {
		hashedCreds := &pb.Credentials{}

		hashedPass, err := HashPassword(creds.Password)
		if err != nil {
			return false
		}
		hashedCreds.Username = creds.Username
		hashedCreds.Password = hashedPass

		db, err := repo.ConnectToDB()
		if err != nil {
			return false
		}

		result, err := db.COLLECTION.InsertOne(ctx, hashedCreds)
		if err != nil {
			log.Print(err.Error())
			return false
		}
		log.Print(result)
		return true
	}

	return false
}

func updatePassword() {

}
