package utils

import "github.com/rs/zerolog/log"

func errorWrapper(err error) {
	if err != nil {
		log.Print(err.Error())
	}
}
