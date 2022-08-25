package pb

import (
	context "context"

	"github.com/rs/zerolog/log"

	codes "google.golang.org/grpc/codes"
	status "google.golang.org/grpc/status"
	emptypb "google.golang.org/protobuf/types/known/emptypb"
)

type BloggerServer struct {
	UnimplementedBloggerServiceServer
}

func (s *BloggerServer) GetBlog(ctx context.Context, blogid *BlogID) (*BlogPost, error) {
	log.Print(blogid)
	newPost := &BlogPost{
		BlogId:   522,
		Title:    "Test",
		SubTitle: "SubLife",
		Category: "CS",
		Post:     "Testing this paragraph",
	}
	return newPost, nil
}
func (s *BloggerServer) GetBlogs(ctx context.Context, _ *emptypb.Empty) (*BlogPosts, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetBlogs not implemented")
}
func (s *BloggerServer) SaveBlog(ctx context.Context, newBlog *BlogSave) (*BlogMessage, error) {
	return nil, status.Errorf(codes.Unimplemented, "method SaveBlog not implemented")
}
func (s *BloggerServer) UpdateBlog(ctx context.Context, blogid *BlogPost) (*BlogMessage, error) {
	return nil, status.Errorf(codes.Unimplemented, "method UpdateBlog not implemented")
}
func (s *BloggerServer) DeleteBlog(ctx context.Context, blogid *BlogID) (*BlogMessage, error) {
	return nil, status.Errorf(codes.Unimplemented, "method DeleteBlog not implemented")
}
