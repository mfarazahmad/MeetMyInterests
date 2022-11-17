package models

import (
	"net/http"
)

type API_DEFINITION struct {
	Verb       string
	Endpoint   string
	Controller func(resp http.ResponseWriter, req *http.Request)
}
