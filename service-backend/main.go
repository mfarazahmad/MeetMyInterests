package main

import (
	"service-backend/config"
	"service-backend/utils"
)

func main() {
	config.Bootstrap()
	utils.CreateRESTServer()
}
