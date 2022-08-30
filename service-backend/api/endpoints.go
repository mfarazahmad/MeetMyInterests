package api

import (
	c "service-portfolio/controller"
	m "service-portfolio/models"
)

var API_CONFIG = []m.API_DEFINITION{
	{Verb: "GET", Endpoint: "/post", Controller: c.GetPosts},
	{Verb: "GET", Endpoint: "/post/{postID}", Controller: c.GetPost},
	{Verb: "POST", Endpoint: "/post/new", Controller: c.SavePost},
	{Verb: "PUT", Endpoint: "/post/{postID}", Controller: c.UpdatePost},
	{Verb: "DELETE", Endpoint: "/post/{postID}", Controller: c.DeletePost},
}
