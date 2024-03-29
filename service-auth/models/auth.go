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

type OauthCredentials struct {
	PROJECT_ID    string   `json:"project_id"`
	AUTH_URI      string   `json:"auth_uri"`
	TOKEN_URI     string   `json:"token_uri"`
	AUTH_PROVIDER string   `json:"auth_provider_x509_cert_url"`
	CLIENT_ID     string   `json:"client_id"`
	CLIENT_SECRET string   `json:"client_secret"`
	REDIRECT_URIS []string `json:"redirect_uris"`
	JS_ORIGINS    []string `json:"javascript_origins"`
}

type UserOauthInfo struct {
	TOKEN string `json:"access_token"`
}

type UserInfo struct {
	PROFILE_PIC string `json:"profile_pic"`
}

type OauthTokenRequest struct {
	CODE          string `json:"code"`
	GRANT_TYPE    string `json:"grant_type"`
	REDIRECT_URI  string `json:"redirect_uri"`
	CLIENT_SECRET string `json:"client_secret"`
	CLIENT_ID     string `json:"client_id"`
}
