package grpc

import (
	"context"

	"service-auth/grpc/pb"
	"service-auth/service"

	"github.com/rs/zerolog/log"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
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
		currentStatus.IsLoggedIn = isMatch
		tokenString := service.GenerateToken()
		currentStatus.Jwt.EncodedJWT = tokenString
		return currentStatus, nil
	} else {
		return currentStatus, status.Errorf(codes.NotFound, "unable to login")
	}
}

func (s *AuthServiceServer) Logout(v context.Context, token *pb.Token) (*pb.AuthStatus, error) {
	log.Printf("Logging out user")
	return nil, status.Errorf(codes.Unauthenticated, "failed to logout")
}
func (s *AuthServiceServer) CheckAuth(ctx context.Context, token *pb.Token) (*pb.AuthStatus, error) {
	log.Printf("Verifyinguser")
	return nil, status.Errorf(codes.PermissionDenied, "failed to verify user")
}
func (s *AuthServiceServer) CreateUser(ctx context.Context, creds *pb.Credentials) (*pb.AuthStatus, error) {
	log.Printf("Creating user %s", creds.Username)
	token := &pb.Token{EncodedJWT: ""}
	currentStatus := &pb.AuthStatus{
		IsLoggedIn:   false,
		TimeToExpire: "",
		Jwt:          token,
	}

	saveStatus := service.SaveUser(creds)
	if saveStatus {
		currentStatus.IsLoggedIn = true
		tokenString := service.GenerateToken()
		currentStatus.Jwt.EncodedJWT = tokenString
		return currentStatus, nil
	} else {
		return nil, status.Errorf(codes.AlreadyExists, "failed to create user")
	}
}
