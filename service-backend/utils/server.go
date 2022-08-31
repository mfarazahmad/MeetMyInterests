package utils

import (
	"net/http"

	"github.com/gorilla/handlers"

	"github.com/rs/zerolog/log"
)

func CreateRESTServer() {
	log.Print("Starting Mux Server at Port :9100")
	router := createRouting()

	credentials := handlers.AllowCredentials()
	methods := handlers.AllowedMethods([]string{"GET", "POST"})
	origins := handlers.AllowedOrigins([]string{"http://localhost:3000"})

	app := http.Server{Addr: ":9100", Handler: handlers.CORS(credentials, methods, origins)(router)}
	errorWrapper(app.ListenAndServe())
}
