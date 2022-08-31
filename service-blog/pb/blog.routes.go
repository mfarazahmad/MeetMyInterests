package pb

import (
	context "context"
	"fmt"
	"math/rand"
	"strconv"
	"time"

	"github.com/rs/zerolog/log"

	emptypb "google.golang.org/protobuf/types/known/emptypb"
)

type BloggerServer struct {
	UnimplementedBloggerServiceServer
}

var newPost = &BlogPost{
	BlogId:   555,
	Title:    "Test",
	SubTitle: "SubLife",
	Category: "CS",
	Post:     "Testing this paragraph",
	Date:     time.Now().Format("2006-01-02"),
}

var postStorage = []*BlogPost{newPost, newPost, newPost}

func (s *BloggerServer) GetBlog(ctx context.Context, blogid *BlogID) (*BlogPost, error) {
	log.Printf("Getting Blog %v", blogid)
	blogID, _ := strconv.Atoi(blogid.BlogId)

	for _, post := range postStorage {
		if int32(blogID) == post.BlogId {
			return post, nil
		}
	}
	return nil, fmt.Errorf("could not find blog with id: %d", blogID)
}

func (s *BloggerServer) GetBlogs(ctx context.Context, _ *emptypb.Empty) (*BlogPosts, error) {
	log.Printf("Getting All Blogs ")
	postObj := &BlogPosts{Blogs: postStorage}
	return postObj, nil
}

func (s *BloggerServer) SaveBlog(ctx context.Context, post *BlogPost) (*BlogMessage, error) {
	log.Printf("Saving Blog ")
	log.Print(post)
	post.BlogId = int32(rand.Intn(1000))
	postStorage = append(postStorage, post)
	newMessage := &BlogMessage{Message: "New Blog saved sucessfully!"}
	return newMessage, nil
}

func (s *BloggerServer) UpdateBlog(ctx context.Context, post *BlogPost) (*BlogMessage, error) {
	log.Printf("Updating Blog %d", post.BlogId)
	log.Print(post)

	for i, currentPost := range postStorage {
		if int32(post.BlogId) == currentPost.BlogId {
			postStorage[i] = postStorage[len(postStorage)-1]
			postStorage = postStorage[:len(postStorage)-1]
		}
	}

	postStorage = append(postStorage, post)
	newMessage := &BlogMessage{Message: "Blog updated sucessfully!"}
	return newMessage, nil
}

func (s *BloggerServer) DeleteBlog(ctx context.Context, blogid *BlogID) (*BlogMessage, error) {
	log.Printf("Deleting Blog %s", blogid)
	log.Print(blogid)
	blogID, _ := strconv.Atoi(blogid.BlogId)

	for i, post := range postStorage {
		if int32(blogID) == post.BlogId {
			postStorage[i] = postStorage[len(postStorage)-1]
			postStorage = postStorage[:len(postStorage)-1]

			newMessage := &BlogMessage{Message: "Blog sucessfully deleted!"}
			return newMessage, nil
		}
	}
	return nil, fmt.Errorf("could not find blog with id: %d", blogID)
}
