package models

import "time"

type Blog struct {
	Title    string
	SubTitle string
	Category string
	Date     time.Time
	Post     string
}
