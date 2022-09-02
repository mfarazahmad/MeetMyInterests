package controller

import (
	"context"
	"encoding/json"
	"net/http"
	"time"

	"github.com/rs/zerolog/log"

	"service-backend/config"
	"service-backend/grpc/auth"
	m "service-backend/models"
)

func Login(resp http.ResponseWriter, req *http.Request) {
	log.Print("Triggering POST /user/login")

	var jsonData []byte
	var respData m.AuthReponseObject

	newCreds := auth.Credentials{}

	decoder := json.NewDecoder(req.Body)
	decoder.DisallowUnknownFields()
	err := decoder.Decode(&newCreds)
	if err != nil {
		log.Print(err.Error())
		respData = m.AuthReponseObject{
			MSG: "",
			ERR: err.Error(),
		}
	}
	log.Print(&newCreds)

	serviceInfo := config.CFG.CLIENTS["auth"]
	service := auth.NewAuthServiceClient(serviceInfo.CONNECTION)

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	status, err := service.Login(ctx, &newCreds)
	if err != nil {
		log.Print("Service Authentication Failed: %v", err)
		respData = m.AuthReponseObject{
			MSG: "",
			ERR: err.Error(),
		}
	} else {
		respData = m.AuthReponseObject{
			MSG: status.Jwt.EncodedJWT,
			ERR: "",
		}
	}
	log.Print(status)

	//defer serviceInfo.CONNECTION.Close()
	jsonData, _ = json.MarshalIndent(respData, "", "    ")
	resp.Write(jsonData)
}

func SaveCredentials(resp http.ResponseWriter, req *http.Request) {
	log.Print("Triggering POST /user/new")

	var jsonData []byte
	var respData m.AuthReponseObject

	newCreds := auth.Credentials{}

	decoder := json.NewDecoder(req.Body)
	decoder.DisallowUnknownFields()
	err := decoder.Decode(&newCreds)
	if err != nil {
		log.Print(err.Error())
		respData = m.AuthReponseObject{
			MSG: "",
			ERR: err.Error(),
		}
	}
	log.Print(&newCreds)

	serviceInfo := config.CFG.CLIENTS["auth"]
	service := auth.NewAuthServiceClient(serviceInfo.CONNECTION)

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	status, err := service.CreateUser(ctx, &newCreds)
	if err != nil {
		log.Print("Service Create New User Failed: %v", err)
		respData = m.AuthReponseObject{
			MSG: "",
			ERR: err.Error(),
		}
	} else {
		respData = m.AuthReponseObject{
			MSG: status.Jwt.EncodedJWT,
			ERR: "",
		}
	}
	log.Print(status)

	//defer serviceInfo.CONNECTION.Close()
	jsonData, _ = json.MarshalIndent(respData, "", "    ")
	resp.Write(jsonData)
}
