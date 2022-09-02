package controller

import (
	"encoding/json"
	"net/http"
)

func responder(resp http.ResponseWriter, respData interface{}) {
	jsonData, _ := json.MarshalIndent(respData, "", "    ")
	resp.Write(jsonData)
}
