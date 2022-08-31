package controller

import (
	"context"
	"encoding/json"
	"net/http"
	"strconv"
	"time"

	"github.com/rs/zerolog/log"

	"service-portfolio/config"
	"service-portfolio/pb/blog"

	"github.com/gorilla/mux"
)

type PostResponseObject struct {
	POSTS []*blog.BlogPost `json:"posts"`
	MSG   string           `json:"msg"`
	ERR   string           `json:"err"`
}

func GetPosts(resp http.ResponseWriter, req *http.Request) {
	log.Print("Triggering GET /post")

	limit_param := req.URL.Query().Get("limit")
	if limit_param != "" {
		limit, _ := strconv.Atoi(limit_param)
		log.Printf("Limit is: %d \n", limit)
	}
	resp.WriteHeader(http.StatusOK)
}

func GetPost(resp http.ResponseWriter, req *http.Request) {
	log.Print("Triggering GET /post/[postID]")

	vars := mux.Vars(req)
	postID := vars["postID"]
	if postID == "" {
		log.Print("Do something")
	}
	log.Printf("PostID is: %s", postID)

	serviceInfo := config.CFG.CLIENTS["blog"]
	service := blog.NewBloggerServiceClient(serviceInfo.CONNECTION)

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	post, err := service.GetBlog(ctx, &blog.BlogID{BlogId: postID})
	if err != nil {
		log.Print("Service GetPost Failed: %v", err)
	}
	log.Print(post)

	respData := &PostResponseObject{
		POSTS: []*blog.BlogPost{post},
		MSG:   "",
		ERR:   "",
	}

	jsonData, _ := json.MarshalIndent(respData, "", "    ")
	//defer serviceInfo.CONNECTION.Close()

	resp.Write(jsonData)
}

func SavePost(resp http.ResponseWriter, req *http.Request) {
	log.Print("Triggering POST /post/new")

	resp.WriteHeader(http.StatusOK)
}

func UpdatePost(resp http.ResponseWriter, req *http.Request) {
	log.Print("Triggering PUT /post/[postID]")

	vars := mux.Vars(req)
	postID := vars["postID"]
	if postID == "" {
		log.Print("Do something")
	}
	log.Printf("PostID is: %s", postID)

	resp.WriteHeader(http.StatusOK)
}

func DeletePost(resp http.ResponseWriter, req *http.Request) {
	log.Print("Triggering DEL /post/[postID]")

	vars := mux.Vars(req)
	postID := vars["postID"]
	if postID == "" {
		log.Print("Do something")
	}
	log.Printf("PostID is: %s", postID)

	resp.WriteHeader(http.StatusOK)
}
