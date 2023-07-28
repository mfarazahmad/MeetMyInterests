package service

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"

	c "service-auth/config"
	m "service-auth/models"

	"github.com/rs/zerolog/log"

	"golang.org/x/oauth2"
	"golang.org/x/oauth2/google"
)

func GetAuthURL() string {
	googleOauthConfig := &oauth2.Config{
		RedirectURL:  c.CFG.AUTH.REDIRECT_URI,
		ClientID:     c.CFG.AUTH.CREDS.CLIENT_ID,
		ClientSecret: c.CFG.AUTH.CREDS.CLIENT_SECRET,
		Scopes:       c.CFG.AUTH.SCOPES,
		Endpoint:     google.Endpoint,
	}
	log.Print(googleOauthConfig)

	return googleOauthConfig.AuthCodeURL("")
}

func GetAccessToken(code string) (string, error) {
	endpoint := "https://accounts.google.com/o/oauth2/token"

	data := m.OauthTokenRequest{
		CODE:          code,
		GRANT_TYPE:    "authorization_code",
		REDIRECT_URI:  c.CFG.AUTH.REDIRECT_URI,
		CLIENT_SECRET: c.CFG.AUTH.CREDS.CLIENT_SECRET,
		CLIENT_ID:     c.CFG.AUTH.CREDS.CLIENT_ID,
	}

	payload, err := json.Marshal(data)
	if err != nil {
		log.Print(err.Error())
		return "", err
	}

	resp, err1 := http.Post(endpoint, "application/json", bytes.NewBuffer(payload))
	if err1 != nil {
		log.Print(err.Error())
		return "", err
	}

	body, err2 := io.ReadAll(resp.Body)
	if err2 != nil {
		log.Print(err.Error())
		return "", err
	}

	authInfo := m.UserOauthInfo{}
	err3 := json.Unmarshal(body, &data)
	if err3 != nil {
		log.Print(err.Error())
		return "", err
	}

	return authInfo.TOKEN, nil
}

func GetUserInfo(token string) m.UserInfo {
	endpoint := "https://www.googleapis.com/oauth2/v1/userinfo"
	client := &http.Client{}

	req, _ := http.NewRequest("GET", endpoint, nil)
	req.Header.Add("Authorization", fmt.Sprintf("Bearer %s", token))
	resp, err := client.Do(req)
	if err != nil {
		log.Print(err.Error())
		return m.UserInfo{}
	}

	body, err2 := io.ReadAll(resp.Body)
	if err2 != nil {
		log.Print(err.Error())
		return m.UserInfo{}
	}

	user := m.UserInfo{}
	err3 := json.Unmarshal(body, &user)
	if err3 != nil {
		log.Print(err.Error())
		return m.UserInfo{}
	}

	return user
}
