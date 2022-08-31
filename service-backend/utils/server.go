package utils

import (
	"net/http"

	c "service-portfolio/config"

	"github.com/gorilla/handlers"

	"github.com/rs/zerolog/log"
)

func CreateRESTServer() {
	log.Print("Starting Mux Server at Port :9100")
	router := createRouting()

	credentials := handlers.AllowCredentials()
	methods := handlers.AllowedMethods([]string{"GET", "POST", "PUT", "DELETE"})
	origins := handlers.AllowedOrigins(c.CFG.WHITELIST)

	app := http.Server{Addr: ":9100", Handler: handlers.CORS(credentials, methods, origins)(router)}
	errorWrapper(app.ListenAndServe())
}
