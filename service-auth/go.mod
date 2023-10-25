module service-auth

go 1.19

require (
	github.com/golang-jwt/jwt/v4 v4.4.3
	github.com/joho/godotenv v1.4.0
	github.com/rs/zerolog v1.28.0
	go.mongodb.org/mongo-driver v1.10.1
	golang.org/x/crypto v0.0.0-20220622213112-05595931fe9d
	google.golang.org/grpc v1.14.0
	google.golang.org/protobuf v1.31.0
)

require (
	cloud.google.com/go/compute/metadata v0.2.0 // indirect
	github.com/golang/glog v1.1.1 // indirect
	google.golang.org/genproto/googleapis/rpc v0.0.0-20230731193218-e0aa005b6bdf // indirect
)

require (
	github.com/golang/protobuf v1.5.3 // indirect
	github.com/golang/snappy v0.0.1 // indirect
	github.com/klauspost/compress v1.13.6 // indirect
	github.com/mattn/go-colorable v0.1.13 // indirect
	github.com/mattn/go-isatty v0.0.16 // indirect
	github.com/montanaflynn/stats v0.0.0-20171201202039-1bf9dbcd8cbe // indirect
	github.com/pkg/errors v0.9.1 // indirect
	github.com/xdg-go/pbkdf2 v1.0.0 // indirect
	github.com/xdg-go/scram v1.1.1 // indirect
	github.com/xdg-go/stringprep v1.0.3 // indirect
	github.com/youmark/pkcs8 v0.0.0-20181117223130-1be2e3e5546d // indirect
	golang.org/x/net v0.9.0 // indirect
	golang.org/x/oauth2 v0.7.0
	golang.org/x/sync v0.0.0-20210220032951-036812b2e83c // indirect
	golang.org/x/sys v0.7.0 // indirect
	golang.org/x/text v0.9.0 // indirect
	google.golang.org/appengine v1.6.7 // indirect
)

replace cloud.google.com/go => cloud.google.com/go v0.100.2
