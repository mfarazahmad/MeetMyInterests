package controller

import (
	"context"
	"encoding/json"
	"net/http"
	"strconv"
	"time"

	"github.com/rs/zerolog/log"

	"service-backend/config"
	"service-backend/grpc/auth"
	"service-backend/grpc/blog"
	m "service-backend/models"

	emptypb "google.golang.org/protobuf/types/known/emptypb"

	"github.com/gorilla/mux"
)

func GetPosts(resp http.ResponseWriter, req *http.Request) {
	log.Print("Triggering GET /post")

	limit_param := req.URL.Query().Get("limit")
	if limit_param != "" {
		limit, _ := strconv.Atoi(limit_param)
		log.Printf("Limit is: %d \n", limit)
	}

	serviceInfo := config.CFG.CLIENTS["blog"]
	service := blog.NewBloggerServiceClient(serviceInfo.CONNECTION)

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	posts, err := service.GetBlogs(ctx, &emptypb.Empty{})
	if err != nil {
		log.Print("Service GetAll Posts Failed: %v", err)
		respData := &m.ModifyReponseObject{MSG: "", ERR: err.Error()}
		responder(resp, respData)
	}
	log.Print(posts)
	respData := &m.GetResponseObject{
		POSTS: posts.Blogs,
		MSG:   "",
		ERR:   "",
	}
	responder(resp, respData)
	//defer serviceInfo.CONNECTION.Close()
}

func GetPost(resp http.ResponseWriter, req *http.Request) {
	log.Print("Triggering GET /post/[postID]")

	vars := mux.Vars(req)
	postID := vars["postID"]
	if postID == "" {
		log.Print("Do something")
		respData := m.ModifyReponseObject{MSG: "", ERR: "Incorrect POST ID"}
		responder(resp, respData)
	}
	log.Printf("PostID is: %s", postID)

	serviceInfo := config.CFG.CLIENTS["blog"]
	service := blog.NewBloggerServiceClient(serviceInfo.CONNECTION)

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	post, err := service.GetBlog(ctx, &blog.BlogID{BlogId: postID})
	if err != nil {
		log.Print("Service GetPost Failed: %v", err)
		respData := &m.ModifyReponseObject{MSG: "", ERR: err.Error()}
		responder(resp, respData)
	}

	log.Print(post)
	respData := &m.GetResponseObject{
		POSTS: []*blog.BlogPost{post},
		MSG:   "",
		ERR:   "",
	}
	responder(resp, respData)
	//defer serviceInfo.CONNECTION.Close()
}

func SavePost(resp http.ResponseWriter, req *http.Request) {
	log.Print("Triggering POST /post/new")

	var respData m.ModifyReponseObject
	if !auth.VerifyToken(req) {
		respData = m.ModifyReponseObject{
			MSG: "",
			ERR: "Failed to verify user!",
		}
		jsonData, _ := json.MarshalIndent(respData, "", "    ")
		resp.Write(jsonData)
	}

	newBlog := blog.BlogPost{}

	decoder := json.NewDecoder(req.Body)
	decoder.DisallowUnknownFields()
	err := decoder.Decode(&newBlog)
	if err != nil {
		log.Print(err.Error())
		respData = m.ModifyReponseObject{
			MSG: "",
			ERR: err.Error(),
		}
		jsonData, _ := json.MarshalIndent(respData, "", "    ")
		resp.Write(jsonData)
	}

	log.Print(&newBlog)

	serviceInfo := config.CFG.CLIENTS["blog"]
	service := blog.NewBloggerServiceClient(serviceInfo.CONNECTION)

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	msg, err := service.SaveBlog(ctx, &newBlog)
	if err != nil {
		log.Print("Service SavePost Failed: %v", err)
		respData = m.ModifyReponseObject{
			MSG: "",
			ERR: err.Error(),
		}
		jsonData, _ := json.MarshalIndent(respData, "", "    ")
		resp.Write(jsonData)
	}

	respData = m.ModifyReponseObject{
		MSG: msg.Message,
		ERR: "",
	}

	log.Print(msg)

	jsonData, _ := json.MarshalIndent(respData, "", "    ")
	resp.Write(jsonData)
	//defer serviceInfo.CONNECTION.Close()
}

func UpdatePost(resp http.ResponseWriter, req *http.Request) {
	log.Print("Triggering PUT /post/[postID]")

	var respData m.ModifyReponseObject
	if !auth.VerifyToken(req) {
		respData = m.ModifyReponseObject{MSG: "", ERR: "Failed to verify user!"}
		responder(resp, respData)
	}

	newBlog := blog.BlogPost{}

	decoder := json.NewDecoder(req.Body)
	decoder.DisallowUnknownFields()
	err := decoder.Decode(&newBlog)

	if err != nil {
		log.Print(err.Error())
		respData = m.ModifyReponseObject{MSG: "", ERR: err.Error()}
		responder(resp, respData)
	}

	log.Print(&newBlog)

	vars := mux.Vars(req)
	postID := vars["postID"]
	if postID == "" {
		respData = m.ModifyReponseObject{MSG: "", ERR: "Invalid PostID"}
		responder(resp, respData)
	}
	log.Printf("PostID is: %s", postID)

	serviceInfo := config.CFG.CLIENTS["blog"]
	service := blog.NewBloggerServiceClient(serviceInfo.CONNECTION)

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	msg, err := service.UpdateBlog(ctx, &newBlog)
	if err != nil {
		log.Print("Service UpdatePost Failed: %v", err)
		respData = m.ModifyReponseObject{MSG: "", ERR: err.Error()}
		responder(resp, respData)
	}

	log.Print(msg)
	respData = m.ModifyReponseObject{MSG: msg.Message, ERR: ""}
	responder(resp, respData)
	//defer serviceInfo.CONNECTION.Close()
}

func DeletePost(resp http.ResponseWriter, req *http.Request) {
	log.Print("Triggering DEL /post/[postID]")

	var respData m.ModifyReponseObject
	if !auth.VerifyToken(req) {
		respData = m.ModifyReponseObject{MSG: "", ERR: "Failed to verify user!"}
		responder(resp, respData)
	}

	vars := mux.Vars(req)
	postID := vars["postID"]
	if postID == "" {
		respData = m.ModifyReponseObject{MSG: "", ERR: "Incorrect POST ID"}
		responder(resp, respData)
	}
	log.Printf("PostID is: %s", postID)
	blogId := blog.BlogID{BlogId: postID}

	serviceInfo := config.CFG.CLIENTS["blog"]
	service := blog.NewBloggerServiceClient(serviceInfo.CONNECTION)

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	msg, err := service.DeleteBlog(ctx, &blogId)
	if err != nil {
		log.Print("Service DeletePost Failed: %v", err)
		respData = m.ModifyReponseObject{MSG: "", ERR: err.Error()}
		responder(resp, respData)
	}
	log.Print(msg)
	respData = m.ModifyReponseObject{MSG: msg.Message, ERR: ""}
	responder(resp, respData)
	//defer serviceInfo.CONNECTION.Close()
}
