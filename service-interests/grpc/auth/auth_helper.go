package auth

import (
	"net/http"

	"github.com/rs/zerolog/log"

	c "service-backend/config"
	m "service-backend/models"

	"github.com/golang-jwt/jwt/v4"
	"github.com/golang-jwt/jwt/v4/request"
)

func VerifyToken(r *http.Request) bool {
	log.Print("Verifying token!")

	var token *jwt.Token

	// Check for user session or bearer token
	session, _ := c.CFG.SESSION.Get(r, "session")

	if auth, ok := session.Values["authenticated"].(bool); !ok || !auth {
		parsedToken, err := parseTokenFromRequest(r)
		if err != nil {
			log.Print(err)
			return false
		}

		token = parsedToken
	} else {
		tokenString := session.Values["token"].(string)
		parsedToken, err := parseTokenFromString(tokenString)
		if err != nil {
			log.Print(err)
			return false
		}
		token = parsedToken
	}

	return verifyClaims(token)

}

func parseTokenFromRequest(r *http.Request) (*jwt.Token, error) {
	token, err := request.ParseFromRequest(r, request.OAuth2Extractor, func(token *jwt.Token) (interface{}, error) {
		return c.CFG.PUBLIC_KEY, nil
	}, request.WithClaims(&m.UserClaims{}))
	return token, err
}

func parseTokenFromString(tokenString string) (*jwt.Token, error) {
	token, err := jwt.ParseWithClaims(tokenString, &m.UserClaims{}, func(token *jwt.Token) (interface{}, error) {
		return c.CFG.PUBLIC_KEY, nil
	})
	return token, err
}

func getAdminClaims(username string) *m.UserClaims {
	claims := &m.UserClaims{
		RegisteredClaims: &jwt.RegisteredClaims{},
		TokenType:        "level2",
		User:             m.User{Name: username, Kind: "Admin"},
	}
	return claims
}

func verifyClaims(token *jwt.Token) bool {
	claims := token.Claims.(*m.UserClaims)
	adminClaims := getAdminClaims(claims.User.Name)

	verification1 := claims.TokenType == adminClaims.TokenType
	verification2 := claims.User.Kind == adminClaims.User.Kind
	verification3 := claims.User.Name == adminClaims.User.Name

	if verification1 && verification2 && verification3 {
		return true
	}
	return false
}
