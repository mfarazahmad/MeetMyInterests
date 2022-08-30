package main

import (
	"service-portfolio/config"
	"service-portfolio/utils"
)

func main() {
	config.Bootstrap()
	utils.CreateRESTServer()
}
