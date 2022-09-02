package models

import (
	"github.com/golang-jwt/jwt/v4"
)

type User struct {
	Name string
	Kind string
}

type UserClaims struct {
	*jwt.RegisteredClaims
	TokenType string
	User
}

type AuthReponseObject struct {
	MSG        string `json:"msg"`
	TOKEN      string `json:"token"`
	ISLOGGEDIN bool   `json:"isloggedin"`
	ERR        string `json:"err"`
}
