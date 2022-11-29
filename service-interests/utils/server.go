package utils

import (
	"net/http"

	c "service-backend/config"

	"github.com/gorilla/handlers"

	"github.com/rs/zerolog/log"
)

func CreateRESTServer() {
	log.Print("Starting Mux Server at Port :9100")
	router := createRouting()

	credentials := handlers.AllowCredentials()
	methods := handlers.AllowedMethods([]string{"GET", "POST", "PUT", "DELETE"})
	origins := handlers.AllowedOrigins(c.CFG.WHITELIST)
	log.Print(origins)

	// Adding GZIP Compression to Responses for Faster Payloads
	app := http.Server{Addr: ":9100",
		Handler: handlers.CompressHandler(handlers.CORS(credentials, methods, origins)(router))}
	errorWrapper(app.ListenAndServe())
}
