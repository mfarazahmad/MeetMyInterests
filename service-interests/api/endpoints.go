package api

import (
	c "service-backend/controller"
	m "service-backend/models"
)

var API_CONFIG = []m.API_DEFINITION{
	{Verb: "GET", Endpoint: "/api/v1/post", Controller: c.GetPosts},
	{Verb: "GET", Endpoint: "/api/v1/post/{postID}", Controller: c.GetPost},
	{Verb: "POST", Endpoint: "/api/v1/post/new", Controller: c.SavePost},
	{Verb: "PUT", Endpoint: "/api/v1/post/{postID}", Controller: c.UpdatePost},
	{Verb: "DELETE", Endpoint: "/api/v1/post/{postID}", Controller: c.DeletePost},
	{Verb: "POST", Endpoint: "/api/v1/user/login", Controller: c.Login},
	{Verb: "POST", Endpoint: "/api/v1/user/logout", Controller: c.Logout},
	{Verb: "GET", Endpoint: "/api/v1/user/oauth", Controller: c.Oauth},
	{Verb: "POST", Endpoint: "/api/v1/user/oauth/callback", Controller: c.OauthCallback},
	{Verb: "POST", Endpoint: "/api/v1/user/new", Controller: c.SaveCredentials},
}
