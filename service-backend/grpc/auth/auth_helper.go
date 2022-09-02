package auth

import (
	"net/http"
	"time"

	"github.com/rs/zerolog/log"

	c "service-backend/config"
	m "service-backend/models"

	"github.com/golang-jwt/jwt/v4"
	"github.com/golang-jwt/jwt/v4/request"
)

func VerifyToken(r *http.Request) bool {
	token, err := parseToken(r)
	if err != nil {
		log.Print(err)
		return false
	}
	claims := token.Claims.(m.UserClaims)
	return claims == getAdminClaims(claims.User.Name)
}

func parseToken(r *http.Request) (*jwt.Token, error) {
	token, err := request.ParseFromRequest(r, request.OAuth2Extractor, func(token *jwt.Token) (interface{}, error) {
		return c.CFG.PUBLIC_KEY, nil
	}, request.WithClaims(&m.UserClaims{}))
	return token, err
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
