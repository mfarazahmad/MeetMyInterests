package models

import "service-backend/grpc/blog"

type GetResponseObject struct {
	POSTS []*blog.BlogPost `json:"posts"`
	MSG   string           `json:"msg"`
	ERR   string           `json:"err"`
}

type ModifyReponseObject struct {
	MSG string `json:"msg"`
	ERR string `json:"err"`
}
