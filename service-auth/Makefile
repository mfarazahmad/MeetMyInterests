# VARIABLES
IMAGEFULLNAME = service-auth

setup:
	go mod download
	go mod tidy
	go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest

dockerlocal:
	docker build \
	-f Dockerfile \
	-t ${IMAGEFULLNAME} \
	.

testcoverage:
	go vet
	go test ./... -coverprofile=coverage.out

lint: setup
	golangci-lint run ./...