package api

import (
	c "service-portfolio/controller"
	m "service-portfolio/models"
)

var API_CONFIG = []m.API_DEFINITION{
	{Verb: "GET", Endpoint: "/api/v1/post", Controller: c.GetPosts},
	{Verb: "GET", Endpoint: "/api/v1/post/{postID}", Controller: c.GetPost},
	{Verb: "POST", Endpoint: "/api/v1/post/new", Controller: c.SavePost},
	{Verb: "PUT", Endpoint: "/api/v1/post/{postID}", Controller: c.UpdatePost},
	{Verb: "DELETE", Endpoint: "/api/v1/post/{postID}", Controller: c.DeletePost},
}
