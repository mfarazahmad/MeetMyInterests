package pb

import (
	context "context"
	"fmt"
	"math/rand"
	"strconv"

	"service-blog/repository"

	"github.com/rs/zerolog/log"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"

	codes "google.golang.org/grpc/codes"
	status "google.golang.org/grpc/status"
	emptypb "google.golang.org/protobuf/types/known/emptypb"
)

type BloggerServer struct {
	UnimplementedBloggerServiceServer
}

func (s *BloggerServer) GetBlog(ctx context.Context, blogid *BlogID) (*BlogPost, error) {
	log.Printf("Getting Blog %d", blogid)
	blogID, _ := strconv.Atoi(blogid.BlogId)
	newPost := BlogPost{}

	repo := repository.ConnectToDB()
	err := repo.COLLECTION.FindOne(ctx, bson.D{{Key: "blogid", Value: blogID}}).Decode(&newPost)

	if err == mongo.ErrNoDocuments || err != nil {
		log.Print(err.Error())
		return nil, status.Errorf(codes.NotFound, fmt.Sprintf("could not find blog with id: %d", blogID))
	}

	return &newPost, nil
}

func (s *BloggerServer) GetBlogs(ctx context.Context, _ *emptypb.Empty) (*BlogPosts, error) {
	log.Printf("Getting All Blogs ")
	posts := []*BlogPost{}

	findOptions := options.Find()
	repo := repository.ConnectToDB()
	cur, err := repo.COLLECTION.Find(ctx, bson.D{{}}, findOptions)
	if err != nil {
		log.Print(err.Error())
		return nil, status.Errorf(codes.NotFound, "could not find any blogs")
	}

	for cur.Next(ctx) {
		newPost := BlogPost{}
		err := cur.Decode(&newPost)
		if err != nil {
			log.Print(err.Error())
			return nil, status.Errorf(codes.NotFound, "could not find any blogs")
		}

		posts = append(posts, &newPost)
	}

	if err := cur.Err(); err != nil {
		log.Print(err.Error())
		return nil, status.Errorf(codes.NotFound, "could not find any blogs")
	}

	//Close the cursor once finished
	cur.Close(ctx)

	return &BlogPosts{Blogs: posts}, nil
}

func (s *BloggerServer) SaveBlog(ctx context.Context, post *BlogPost) (*BlogMessage, error) {
	log.Printf("Saving Blog ")
	log.Print(post)

	post.BlogId = int32(rand.Intn(100521230))

	repo := repository.ConnectToDB()
	result, err := repo.COLLECTION.InsertOne(ctx, post)
	if err != nil {
		log.Print(err.Error())
		return nil, status.Errorf(codes.Aborted, "failed to save blog")
	}
	log.Print(result)

	newMessage := &BlogMessage{Message: "New Blog saved sucessfully!"}
	return newMessage, nil
}

func (s *BloggerServer) UpdateBlog(ctx context.Context, post *BlogPost) (*BlogMessage, error) {
	log.Printf("Updating Blog %d", post.BlogId)
	log.Print(post)

	repo := repository.ConnectToDB()
	filter := bson.D{{Key: "blogid", Value: post.BlogId}}
	update := bson.D{{Key: "$set", Value: post}}
	result, err := repo.COLLECTION.UpdateOne(ctx, filter, update)
	if err != nil {
		log.Print(err.Error())
		return nil, status.Errorf(codes.NotFound, "failed to update blog")
	}

	log.Print(result)

	newMessage := &BlogMessage{Message: "Blog updated sucessfully!"}
	return newMessage, nil
}

func (s *BloggerServer) DeleteBlog(ctx context.Context, blogid *BlogID) (*BlogMessage, error) {
	log.Printf("Deleting Blog %s", blogid)
	log.Print(blogid)
	blogID, _ := strconv.Atoi(blogid.BlogId)

	repo := repository.ConnectToDB()
	result, err := repo.COLLECTION.DeleteOne(ctx, bson.D{{Key: "blogid", Value: blogID}})
	if err != nil {
		log.Print(err.Error())
		return nil, status.Errorf(codes.NotFound, "failed to delete blog")
	}

	log.Print(result)

	newMessage := &BlogMessage{Message: "Blog sucessfully deleted!"}
	return newMessage, nil
}
