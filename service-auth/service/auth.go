package service

import (
	"crypto"
	"time"

	"github.com/golang-jwt/jwt/v4"
	"github.com/rs/zerolog/log"
	"golang.org/x/crypto/argon2"

	c "service-auth/config"
	m "service-auth/models"
)

func GenerateAdminToken(username string) (string, error) {
	log.Print("Generating Token")
	token := jwt.New(jwt.GetSigningMethod("RS256"))
	token.Claims = getAdminClaims(username)
	return token.SignedString(c.CFG.PRIVATE_KEY)
}

func HashPassword(pass string) (string, error) {
	log.Print("Hashing Password")
	salt := crypto.BLAKE2b_256.New().Sum([]byte(pass))
	key := argon2.IDKey([]byte(pass), salt, 1, 15*1024, 4, 32)
	return string(key), nil
}

func VerifyClaims(claims m.UserClaims) bool {
	return claims == getAdminClaims(claims.User.Name)
}

func getAdminClaims(username string) m.UserClaims {
	claims := m.UserClaims{
		RegisteredClaims: &jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(time.Now().Add(time.Minute * 1)),
		},
		TokenType: "level2",
		User:      m.User{Name: username, Kind: "Admin"},
	}
	return claims
}

func validatePassword(pass string) bool {
	log.Print("Validating Password")
	return true
}

func validateUsername(username string) bool {
	log.Print("Validating Username")
	return true
}
