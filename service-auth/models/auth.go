package models

import "github.com/golang-jwt/jwt/v4"

type User struct {
	Name string
	Kind string
}

type UserClaims struct {
	*jwt.RegisteredClaims
	TokenType string
	User
}
