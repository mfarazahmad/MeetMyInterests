package utils

import (
	"crypto/rand"
	"math/big"

	"github.com/rs/zerolog/log"
)

func GenerateRandomString(n int) string {
	log.Print("Generating Random String")
	letters := "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-"
	random := make([]byte, n)

	for i := 0; i < n; i++ {
		num, err := rand.Int(rand.Reader, big.NewInt(int64(len(letters))))
		if err != nil {
			log.Print("Could not generate random string")
			return ""
		}
		random[i] = letters[num.Int64()]
	}

	return string(random)
}
