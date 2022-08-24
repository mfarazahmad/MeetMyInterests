package main

import (
	"service-blog/pb"

	"github.com/rs/zerolog/log"
	"google.golang.org/protobuf/proto"
)

func main() {
	log.Print("Starting GRPC Server")
	newPost := &pb.Blog{
		Title:    "Test",
		SubTitle: "SubLife",
		Category: "CS",
		Post:     "Testing this para",
	}
	log.Print(newPost)
	byteMessage, err := proto.Marshal(newPost)
	if err != nil {
		log.Print(err)
	}
	log.Print(byteMessage)
}
