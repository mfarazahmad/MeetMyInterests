package utils

import (
	"net/http"

	"github.com/rs/zerolog/log"
)

func CreateRESTServer() {
	log.Print("Starting Mux Server at Port :9100")
	router := createRouting()
	app := http.Server{Addr: ":9100", Handler: router}
	errorWrapper(app.ListenAndServe())
}
