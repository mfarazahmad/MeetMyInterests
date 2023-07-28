package grpc

import (
	"context"

	"service-auth/grpc/pb"
	"service-auth/service"

	"github.com/rs/zerolog/log"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
	"google.golang.org/protobuf/types/known/emptypb"
)

type AuthServiceServer struct {
	pb.UnimplementedAuthServiceServer
}

func (s *AuthServiceServer) Login(ctx context.Context, creds *pb.Credentials) (*pb.AuthStatus, error) {
	log.Printf("Logging in user: %d", creds.Username)
	token := &pb.Token{EncodedJWT: ""}
	currentStatus := &pb.AuthStatus{
		IsLoggedIn:   false,
		TimeToExpire: "",
		Jwt:          token,
	}

	isMatch, err := service.CompareCredentials(creds)
	if err != nil {
		return currentStatus, status.Errorf(codes.NotFound, err.Error())
	}

	if isMatch {
		tokenString, tokenErr := service.GenerateAdminToken(creds.Username)
		if tokenErr != nil {
			return currentStatus, status.Errorf(codes.Unauthenticated, tokenErr.Error())
		}

		currentStatus.IsLoggedIn = isMatch
		currentStatus.Jwt.EncodedJWT = tokenString
		return currentStatus, nil
	} else {
		return currentStatus, status.Errorf(codes.NotFound, "unable to login")
	}
}

func (s *AuthServiceServer) Oauth(ctx context.Context, _ *emptypb.Empty) (*pb.AuthURI, error) {
	log.Printf("Triggering Oauth RPC")

	authURI := &pb.AuthURI{}
	authURI.AuthURI = service.GetAuthURL()

	if authURI.AuthURI == "" {
		return authURI, status.Errorf(codes.Unauthenticated, "Error Getting Auth URL")
	}
	return authURI, nil
}

func (s *AuthServiceServer) OauthCallback(ctx context.Context, code *pb.AuthCode) (*pb.AuthStatus, error) {
	log.Printf("Triggering Oauth Callback RPC")

	token := &pb.Token{EncodedJWT: ""}
	currentStatus := &pb.AuthStatus{
		IsLoggedIn:   false,
		TimeToExpire: "",
		Jwt:          token,
	}
	strToken, err := service.GetAccessToken(code.AuthCode)
	if err != nil {
		return currentStatus, status.Errorf(codes.Unauthenticated, err.Error())
	}
	token = &pb.Token{EncodedJWT: strToken}
	currentStatus.IsLoggedIn = true
	currentStatus.Jwt = token

	return currentStatus, nil
}

func (s *AuthServiceServer) Logout(v context.Context, token *pb.Token) (*pb.AuthStatus, error) {
	log.Printf("Logging out user")
	return nil, status.Errorf(codes.Unauthenticated, "failed to logout")
}

func (s *AuthServiceServer) CreateUser(ctx context.Context, creds *pb.Credentials) (*pb.AuthStatus, error) {
	log.Printf("Creating user %s", creds.Username)
	token := &pb.Token{EncodedJWT: ""}
	currentStatus := &pb.AuthStatus{
		IsLoggedIn:   false,
		TimeToExpire: "",
		Jwt:          token,
	}

	saveStatus := service.SaveCredentials(creds)
	if saveStatus {
		tokenString, tokenErr := service.GenerateAdminToken(creds.Username)
		if tokenErr != nil {
			return currentStatus, status.Errorf(codes.Unauthenticated, tokenErr.Error())
		}

		currentStatus.IsLoggedIn = true
		currentStatus.Jwt.EncodedJWT = tokenString
		return currentStatus, nil
	} else {
		return nil, status.Errorf(codes.AlreadyExists, "failed to create user")
	}
}
