package service

import (
	"github.com/rs/zerolog/log"
)

func GenerateToken() string {
	log.Print("Generating Token")
	return ""
}

func HashPassword(pass string) (string, error) {
	log.Print("Hashing Password")

	return "", nil
}

func CheckClaims(token string) {

}

func validatePassword(pass string) bool {
	log.Print("Validating Password")
	return true
}

func validateUsername(username string) bool {
	log.Print("Validating Username")
	return true
}
