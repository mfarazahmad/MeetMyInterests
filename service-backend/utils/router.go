package utils

import (
	a "service-portfolio/api"

	"github.com/gorilla/mux"
)

func createRouting() *mux.Router {
	router := mux.NewRouter()

	for _, api := range a.API_CONFIG {
		router.HandleFunc(api.Endpoint, api.Controller).Methods(api.Verb)
	}

	return router
}
