# VARIABLES
IMAGEFULLNAME := service-backend
GIT_REPO := '$(shell git config --get remote.origin.url)'
GIT_BRANCH := '$(shell git rev-parse --abbrev-ref HEAD)'
GIT_COMMIT := '$(shell git log -1 --format=format:"%H")'
GIT_MESSAGE := '$(shell git log -1 --pretty=%B)'

setup:
	go mod download
	go mod tidy
	go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest

dockerlocal:
	docker build \
	-f Dockerfile \
	-t ${IMAGEFULLNAME} \
	--build-arg REPO=$(GIT_REPO) \
	--build-arg BRANCH=$(GIT_BRANCH) \
	--build-arg COMMIT=$(GIT_COMMIT) \
	--build-arg MSG=$(GIT_MESSAGE) \
	.

testcoverage:
	go vet
	go test ./... -coverprofile=coverage.out

lint: setup
	golangci-lint run ./...