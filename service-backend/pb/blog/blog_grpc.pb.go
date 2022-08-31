// Code generated by protoc-gen-go-grpc. DO NOT EDIT.
// versions:
// - protoc-gen-go-grpc v1.2.0
// - protoc             v3.20.1
// source: blog.proto

package blog

import (
	context "context"
	grpc "google.golang.org/grpc"
	codes "google.golang.org/grpc/codes"
	status "google.golang.org/grpc/status"
	emptypb "google.golang.org/protobuf/types/known/emptypb"
)

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
// Requires gRPC-Go v1.32.0 or later.
const _ = grpc.SupportPackageIsVersion7

// BloggerServiceClient is the client API for BloggerService service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://pkg.go.dev/google.golang.org/grpc/?tab=doc#ClientConn.NewStream.
type BloggerServiceClient interface {
	// CRUD Operations on Blog
	GetBlog(ctx context.Context, in *BlogID, opts ...grpc.CallOption) (*BlogPost, error)
	GetBlogs(ctx context.Context, in *emptypb.Empty, opts ...grpc.CallOption) (*BlogPosts, error)
	SaveBlog(ctx context.Context, in *BlogPost, opts ...grpc.CallOption) (*BlogMessage, error)
	UpdateBlog(ctx context.Context, in *BlogPost, opts ...grpc.CallOption) (*BlogMessage, error)
	DeleteBlog(ctx context.Context, in *BlogID, opts ...grpc.CallOption) (*BlogMessage, error)
}

type bloggerServiceClient struct {
	cc grpc.ClientConnInterface
}

func NewBloggerServiceClient(cc grpc.ClientConnInterface) BloggerServiceClient {
	return &bloggerServiceClient{cc}
}

func (c *bloggerServiceClient) GetBlog(ctx context.Context, in *BlogID, opts ...grpc.CallOption) (*BlogPost, error) {
	out := new(BlogPost)
	err := c.cc.Invoke(ctx, "/blog.BloggerService/GetBlog", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *bloggerServiceClient) GetBlogs(ctx context.Context, in *emptypb.Empty, opts ...grpc.CallOption) (*BlogPosts, error) {
	out := new(BlogPosts)
	err := c.cc.Invoke(ctx, "/blog.BloggerService/GetBlogs", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *bloggerServiceClient) SaveBlog(ctx context.Context, in *BlogPost, opts ...grpc.CallOption) (*BlogMessage, error) {
	out := new(BlogMessage)
	err := c.cc.Invoke(ctx, "/blog.BloggerService/SaveBlog", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *bloggerServiceClient) UpdateBlog(ctx context.Context, in *BlogPost, opts ...grpc.CallOption) (*BlogMessage, error) {
	out := new(BlogMessage)
	err := c.cc.Invoke(ctx, "/blog.BloggerService/UpdateBlog", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *bloggerServiceClient) DeleteBlog(ctx context.Context, in *BlogID, opts ...grpc.CallOption) (*BlogMessage, error) {
	out := new(BlogMessage)
	err := c.cc.Invoke(ctx, "/blog.BloggerService/DeleteBlog", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// BloggerServiceServer is the server API for BloggerService service.
// All implementations must embed UnimplementedBloggerServiceServer
// for forward compatibility
type BloggerServiceServer interface {
	// CRUD Operations on Blog
	GetBlog(context.Context, *BlogID) (*BlogPost, error)
	GetBlogs(context.Context, *emptypb.Empty) (*BlogPosts, error)
	SaveBlog(context.Context, *BlogPost) (*BlogMessage, error)
	UpdateBlog(context.Context, *BlogPost) (*BlogMessage, error)
	DeleteBlog(context.Context, *BlogID) (*BlogMessage, error)
	mustEmbedUnimplementedBloggerServiceServer()
}

// UnimplementedBloggerServiceServer must be embedded to have forward compatible implementations.
type UnimplementedBloggerServiceServer struct {
}

func (UnimplementedBloggerServiceServer) GetBlog(context.Context, *BlogID) (*BlogPost, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetBlog not implemented")
}
func (UnimplementedBloggerServiceServer) GetBlogs(context.Context, *emptypb.Empty) (*BlogPosts, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetBlogs not implemented")
}
func (UnimplementedBloggerServiceServer) SaveBlog(context.Context, *BlogPost) (*BlogMessage, error) {
	return nil, status.Errorf(codes.Unimplemented, "method SaveBlog not implemented")
}
func (UnimplementedBloggerServiceServer) UpdateBlog(context.Context, *BlogPost) (*BlogMessage, error) {
	return nil, status.Errorf(codes.Unimplemented, "method UpdateBlog not implemented")
}
func (UnimplementedBloggerServiceServer) DeleteBlog(context.Context, *BlogID) (*BlogMessage, error) {
	return nil, status.Errorf(codes.Unimplemented, "method DeleteBlog not implemented")
}
func (UnimplementedBloggerServiceServer) mustEmbedUnimplementedBloggerServiceServer() {}

// UnsafeBloggerServiceServer may be embedded to opt out of forward compatibility for this service.
// Use of this interface is not recommended, as added methods to BloggerServiceServer will
// result in compilation errors.
type UnsafeBloggerServiceServer interface {
	mustEmbedUnimplementedBloggerServiceServer()
}

func RegisterBloggerServiceServer(s grpc.ServiceRegistrar, srv BloggerServiceServer) {
	s.RegisterService(&BloggerService_ServiceDesc, srv)
}

func _BloggerService_GetBlog_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(BlogID)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(BloggerServiceServer).GetBlog(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/blog.BloggerService/GetBlog",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(BloggerServiceServer).GetBlog(ctx, req.(*BlogID))
	}
	return interceptor(ctx, in, info, handler)
}

func _BloggerService_GetBlogs_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(emptypb.Empty)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(BloggerServiceServer).GetBlogs(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/blog.BloggerService/GetBlogs",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(BloggerServiceServer).GetBlogs(ctx, req.(*emptypb.Empty))
	}
	return interceptor(ctx, in, info, handler)
}

func _BloggerService_SaveBlog_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(BlogPost)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(BloggerServiceServer).SaveBlog(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/blog.BloggerService/SaveBlog",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(BloggerServiceServer).SaveBlog(ctx, req.(*BlogPost))
	}
	return interceptor(ctx, in, info, handler)
}

func _BloggerService_UpdateBlog_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(BlogPost)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(BloggerServiceServer).UpdateBlog(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/blog.BloggerService/UpdateBlog",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(BloggerServiceServer).UpdateBlog(ctx, req.(*BlogPost))
	}
	return interceptor(ctx, in, info, handler)
}

func _BloggerService_DeleteBlog_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(BlogID)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(BloggerServiceServer).DeleteBlog(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/blog.BloggerService/DeleteBlog",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(BloggerServiceServer).DeleteBlog(ctx, req.(*BlogID))
	}
	return interceptor(ctx, in, info, handler)
}

// BloggerService_ServiceDesc is the grpc.ServiceDesc for BloggerService service.
// It's only intended for direct use with grpc.RegisterService,
// and not to be introspected or modified (even as a copy)
var BloggerService_ServiceDesc = grpc.ServiceDesc{
	ServiceName: "blog.BloggerService",
	HandlerType: (*BloggerServiceServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "GetBlog",
			Handler:    _BloggerService_GetBlog_Handler,
		},
		{
			MethodName: "GetBlogs",
			Handler:    _BloggerService_GetBlogs_Handler,
		},
		{
			MethodName: "SaveBlog",
			Handler:    _BloggerService_SaveBlog_Handler,
		},
		{
			MethodName: "UpdateBlog",
			Handler:    _BloggerService_UpdateBlog_Handler,
		},
		{
			MethodName: "DeleteBlog",
			Handler:    _BloggerService_DeleteBlog_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "blog.proto",
}
