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

	newCreds := auth.Credentials{}

	decoder := json.NewDecoder(req.Body)
	decoder.DisallowUnknownFields()
	err := decoder.Decode(&newCreds)
	if err != nil {
		log.Print(err.Error() + "| Incorrect user credentials")
		respData := m.AuthReponseObject{
			MSG:        "",
			ISLOGGEDIN: false,
			TOKEN:      "",
			ERR:        err.Error() + "| Incorrect user credentials!",
		}
		responder(resp, respData)
		return
	}
	log.Print(&newCreds)

	serviceInfo := config.CFG.CLIENTS["auth"]
	service := auth.NewAuthServiceClient(serviceInfo.CONNECTION)

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	status, err := service.Login(ctx, &newCreds)
	if err != nil {
		log.Print("Service Authentication Failed: %v", err)
		respData := m.AuthReponseObject{
			MSG:        "",
			ISLOGGEDIN: false,
			TOKEN:      "",
			ERR:        err.Error(),
		}
		responder(resp, respData)
		return
	}

	log.Print(status)
	respData := m.AuthReponseObject{
		MSG:        "Successfully logged in user!",
		ISLOGGEDIN: status.IsLoggedIn,
		TOKEN:      status.Jwt.EncodedJWT,
		ERR:        "",
	}
	responder(resp, respData)
	//defer serviceInfo.CONNECTION.Close()
}

func SaveCredentials(resp http.ResponseWriter, req *http.Request) {
	log.Print("Triggering POST /user/new")

	newCreds := auth.Credentials{}

	decoder := json.NewDecoder(req.Body)
	decoder.DisallowUnknownFields()
	err := decoder.Decode(&newCreds)
	if err != nil {
		log.Print(err.Error() + "| Incorrect user credentials")
		respData := m.AuthReponseObject{
			MSG:        "",
			ISLOGGEDIN: false,
			TOKEN:      "",
			ERR:        err.Error() + "| Incorrect user credentials",
		}
		responder(resp, respData)
		return
	}
	log.Print(&newCreds)

	serviceInfo := config.CFG.CLIENTS["auth"]
	service := auth.NewAuthServiceClient(serviceInfo.CONNECTION)

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	status, err := service.CreateUser(ctx, &newCreds)
	if err != nil {
		log.Print("Service Create New User Failed: %v", err)
		respData := m.AuthReponseObject{
			MSG:        "",
			ISLOGGEDIN: false,
			TOKEN:      "",
			ERR:        err.Error(),
		}
		responder(resp, respData)
		return
	}

	respData := m.AuthReponseObject{
		MSG:        "Successfully saved user!",
		ISLOGGEDIN: status.IsLoggedIn,
		TOKEN:      status.Jwt.EncodedJWT,
		ERR:        "",
	}

	log.Print(status)
	responder(resp, respData)
	//defer serviceInfo.CONNECTION.Close()

}
