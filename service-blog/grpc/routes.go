package grpc

import (
	context "context"
	"fmt"

	"service-blog/grpc/pb"
	"service-blog/repository"
	"service-blog/utils"

	"github.com/rs/zerolog/log"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"

	codes "google.golang.org/grpc/codes"
	status "google.golang.org/grpc/status"
	emptypb "google.golang.org/protobuf/types/known/emptypb"
)

type BloggerServer struct {
	pb.UnimplementedBloggerServiceServer
}

func (s *BloggerServer) GetBlog(ctx context.Context, blogid *pb.BlogID) (*pb.BlogPost, error) {
	log.Printf("Getting Blog %d", blogid)
	newPost := pb.BlogPost{}

	repo := repository.ConnectToDB()
	err := repo.COLLECTION.FindOne(ctx, bson.D{{Key: "blogid", Value: blogid.BlogId}}).Decode(&newPost)
	if err == mongo.ErrNoDocuments || err != nil {
		log.Print(err.Error())
		return nil, status.Errorf(codes.NotFound, fmt.Sprintf("could not find blog with id: %s", blogid.BlogId))
	}

	return &newPost, nil
}

func (s *BloggerServer) GetBlogs(ctx context.Context, _ *emptypb.Empty) (*pb.BlogPosts, error) {
	log.Printf("Getting All Blogs ")
	posts := []*pb.BlogPost{}

	findOptions := options.Find()
	repo := repository.ConnectToDB()
	cur, err := repo.COLLECTION.Find(ctx, bson.D{{}}, findOptions)
	if err != nil {
		log.Print(err.Error())
		return nil, status.Errorf(codes.NotFound, "could not find any blogs")
	}

	for cur.Next(ctx) {
		newPost := pb.BlogPost{}
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

	return &pb.BlogPosts{Blogs: posts}, nil
}

func (s *BloggerServer) SaveBlog(ctx context.Context, post *pb.BlogPost) (*pb.BlogMessage, error) {
	log.Printf("Saving Blog %s", post.Title)
	log.Print(post)

	post.BlogId = utils.GenerateRandomString(32)

	repo := repository.ConnectToDB()
	result, err := repo.COLLECTION.InsertOne(ctx, post)
	if err != nil {
		log.Print(err.Error())
		return nil, status.Errorf(codes.Aborted, "failed to save blog")
	}
	log.Print(result)

	newMessage := &pb.BlogMessage{Message: "New Blog saved sucessfully!"}
	return newMessage, nil
}

func (s *BloggerServer) UpdateBlog(ctx context.Context, post *pb.BlogPost) (*pb.BlogMessage, error) {
	log.Printf("Updating Blog %s", post.BlogId)
	log.Print(post)

	repo := repository.ConnectToDB()
	filter := bson.D{{Key: "blogid", Value: post.BlogId}}
	update := bson.D{{Key: "$set", Value: post}}
	result, err := repo.COLLECTION.UpdateOne(ctx, filter, update)
	if err != nil {
		log.Print(err.Error())
		return nil, status.Errorf(codes.NotFound, "failed to update blog")
	}

	if result.ModifiedCount == 0 {
		log.Printf("%d results found", result.MatchedCount)
		return nil, status.Errorf(codes.NotFound, "failed to update blog")
	}

	newMessage := &pb.BlogMessage{Message: "Blog updated sucessfully!"}
	return newMessage, nil
}

func (s *BloggerServer) DeleteBlog(ctx context.Context, blogid *pb.BlogID) (*pb.BlogMessage, error) {
	log.Printf("Deleting Blog %s", blogid.BlogId)

	repo := repository.ConnectToDB()
	result, err := repo.COLLECTION.DeleteOne(ctx, bson.D{{Key: "blogid", Value: blogid.BlogId}})
	if err != nil {
		log.Print(err.Error())
		return nil, status.Errorf(codes.NotFound, "failed to delete blog")
	}

	if result.DeletedCount == 0 {
		log.Printf("%d results found", result.DeletedCount)
		return nil, status.Errorf(codes.NotFound, "failed to update blog")
	}

	newMessage := &pb.BlogMessage{Message: "Blog sucessfully deleted!"}
	return newMessage, nil
}
