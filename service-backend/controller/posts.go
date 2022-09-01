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

	emptypb "google.golang.org/protobuf/types/known/emptypb"

	"github.com/gorilla/mux"
)

type GetResponseObject struct {
	POSTS []*blog.BlogPost `json:"posts"`
	MSG   string           `json:"msg"`
	ERR   string           `json:"err"`
}

type ModifyReponseObject struct {
	MSG string `json:"msg"`
	ERR string `json:"err"`
}

func GetPosts(resp http.ResponseWriter, req *http.Request) {
	log.Print("Triggering GET /post")

	jsonData := []byte{}

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
		respData := &ModifyReponseObject{
			MSG: "",
			ERR: err.Error(),
		}
		jsonData, _ = json.MarshalIndent(respData, "", "    ")
	} else {
		respData := &GetResponseObject{
			POSTS: posts.Blogs,
			MSG:   "",
			ERR:   "",
		}
		jsonData, _ = json.MarshalIndent(respData, "", "    ")
	}
	log.Print(posts)

	//defer serviceInfo.CONNECTION.Close()

	resp.Write(jsonData)
}

func GetPost(resp http.ResponseWriter, req *http.Request) {
	log.Print("Triggering GET /post/[postID]")

	jsonData := []byte{}

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
		respData := &ModifyReponseObject{
			MSG: "",
			ERR: err.Error(),
		}
		jsonData, _ = json.MarshalIndent(respData, "", "    ")
	} else {
		respData := &GetResponseObject{
			POSTS: []*blog.BlogPost{post},
			MSG:   "",
			ERR:   "",
		}
		jsonData, _ = json.MarshalIndent(respData, "", "    ")
	}
	log.Print(post)

	//defer serviceInfo.CONNECTION.Close()

	resp.Write(jsonData)
}

func SavePost(resp http.ResponseWriter, req *http.Request) {
	log.Print("Triggering POST /post/new")

	newBlog := blog.BlogPost{}

	decoder := json.NewDecoder(req.Body)
	decoder.DisallowUnknownFields()
	err := decoder.Decode(&newBlog)
	if err != nil {
		log.Print(err.Error())
	}

	log.Print(&newBlog)

	serviceInfo := config.CFG.CLIENTS["blog"]
	service := blog.NewBloggerServiceClient(serviceInfo.CONNECTION)

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	msg, err := service.SaveBlog(ctx, &newBlog)
	respData := ModifyReponseObject{}
	if err != nil {
		log.Print("Service SavePost Failed: %v", err)
		respData = ModifyReponseObject{
			MSG: "",
			ERR: err.Error(),
		}
	} else {
		respData = ModifyReponseObject{
			MSG: msg.Message,
			ERR: "",
		}
	}
	log.Print(msg)

	jsonData, _ := json.MarshalIndent(respData, "", "    ")
	//defer serviceInfo.CONNECTION.Close()

	resp.Write(jsonData)
}

func UpdatePost(resp http.ResponseWriter, req *http.Request) {
	log.Print("Triggering PUT /post/[postID]")

	newBlog := blog.BlogPost{}

	decoder := json.NewDecoder(req.Body)
	decoder.DisallowUnknownFields()
	err := decoder.Decode(&newBlog)

	respData := ModifyReponseObject{}
	if err != nil {
		log.Print(err.Error())
		respData = ModifyReponseObject{
			MSG: "",
			ERR: err.Error(),
		}
	}

	log.Print(&newBlog)

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

	msg, err := service.UpdateBlog(ctx, &newBlog)
	if err != nil {
		log.Print("Service UpdatePost Failed: %v", err)
		respData = ModifyReponseObject{
			MSG: "",
			ERR: err.Error(),
		}
	} else {
		respData = ModifyReponseObject{
			MSG: msg.Message,
			ERR: "",
		}
	}
	log.Print(msg)

	jsonData, _ := json.MarshalIndent(respData, "", "    ")
	//defer serviceInfo.CONNECTION.Close()

	resp.Write(jsonData)
}

func DeletePost(resp http.ResponseWriter, req *http.Request) {
	log.Print("Triggering DEL /post/[postID]")

	vars := mux.Vars(req)
	postID := vars["postID"]
	if postID == "" {
		log.Print("Do something")
	}
	log.Printf("PostID is: %s", postID)
	blogId := blog.BlogID{BlogId: postID}

	serviceInfo := config.CFG.CLIENTS["blog"]
	service := blog.NewBloggerServiceClient(serviceInfo.CONNECTION)

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	msg, err := service.DeleteBlog(ctx, &blogId)
	respData := ModifyReponseObject{}
	if err != nil {
		log.Print("Service DeletePost Failed: %v", err)
		respData = ModifyReponseObject{
			MSG: "",
			ERR: err.Error(),
		}
	} else {
		respData = ModifyReponseObject{
			MSG: msg.Message,
			ERR: "",
		}
	}
	log.Print(msg)

	jsonData, _ := json.MarshalIndent(respData, "", "    ")
	//defer serviceInfo.CONNECTION.Close()

	resp.Write(jsonData)
}
