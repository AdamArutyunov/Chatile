package main

import (
	"client/tcp"
	"client/user"
	"fmt"
	"github.com/turret-io/go-menu/menu"
)




func auth(args ...string) error {
	fmt.Println("Output of cmd1")
	return nil
}


func main() {
	handler := tcp.ConnectionHandler{}

	userHandler := user.Handler{ConnectionHandler: handler}
	commandOptions := []menu.CommandOption{
		{"login", "Login", auth},
		{"register", "Register", userHandler.Register},
	}

	menuOptions := menu.NewMenuOptions("'menu' for help > ", 0)


	switcher := menu.NewMenu(commandOptions, menuOptions)
	switcher.Start()



}