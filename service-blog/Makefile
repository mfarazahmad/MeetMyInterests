# VARIABLES
IMAGEFULLNAME = service-blog

setup:
	go mod download
	go mod tidy
	go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest

dockerlocal:
	docker build \
	-f Dockerfile \
	-t ${IMAGEFULLNAME} \
	.

dockerstage:
	docker build \
	-f Dockerfile \
	-t questmaster991/meetmyinterests:${IMAGEFULLNAME} \
	.

	docker push questmaster991/meetmyinterests:${IMAGEFULLNAME}
	
testcoverage:
	go vet
	go test ./... -coverprofile=coverage.out

lint: setup
	golangci-lint run ./...