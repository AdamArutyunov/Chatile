package main

import (
	"client/menu"
	"client/tcp"
	"client/user"
	"errors"
	"fmt"
	"github.com/fatih/color"
	"log"
	"os"
	"os/signal"
	"syscall"
)

func main() {
	handler := tcp.ConnectionHandler{}
	err := handler.OpenConnection()
	if err != nil {
		log.Fatalln(err)
	}
	defer handler.CloseConnection()

	// handle ctrl c
	c := make(chan os.Signal)
	signal.Notify(c, os.Interrupt, syscall.SIGTERM)
	go func() {
		<-c
		shutdown(handler)
		os.Exit(1)
	}()

	state := menu.State{MenuDict: map[string]menu.Menu{}}
	mainMenu := menu.Menu{
		Commands: []menu.Command{
			{"help", func(s *menu.State, menuDict map[string]menu.Menu) error {
				fmt.Println("help command")
				return nil
			}},
			{Name: "login", Handler: func(s *menu.State, menuDict map[string]menu.Menu) error {
				var login, password string
				ask(&login, "login")
				ask(&password, "password")
				ok, profile, err := user.Login(login, password, handler)
				if err != nil {
					return err
				}
				err = user.UpdateOnline(handler, profile)
				if err != nil {
					return err
				}
				if ok {
					s.Profile = profile
					s.SetMenu(menuDict["loggedMenu"])
				}
				return nil

			}},
			{"register", func(s *menu.State, menuDict map[string]menu.Menu) error {
				var name, login, password, password2 string
				ask(&name, "name")
				ask(&login, "login")
				ask(&password, "password")
				ask(&password2, "repeat password")
				if password != password2 {
					return errors.New("passwords do not match")
				}
				profile := user.NewProfile(name, login, password)
				err := user.Register(*profile, handler)
				if err != nil {
					return err
				}
				color.Green("Регистрация прошла успешно, поздравляем")
				color.Green("Теперь авторизуйтесь!")
				return nil
			}},
		},
	}
	loggedMenu := menu.Menu{Commands: []menu.Command{
		{"test", func(s *menu.State, menuDict map[string]menu.Menu) error {
			fmt.Println("Hello, user")
			fmt.Println(s.Profile)
			return nil
		}},
		{"logout", func(s *menu.State, menuDict map[string]menu.Menu) error {
			s.Profile = user.Profile{}
			s.SetMenu(menuDict["mainMenu"])
			return nil
		}},
	}}

	state.SetMenu(mainMenu)
	state.MenuDict["mainMenu"] = mainMenu
	state.MenuDict["loggedMenu"] = loggedMenu

	for {
		m := state.GetMenu()
		printCommands(m.Commands)
		var input string
		_, _ = fmt.Scanln(&input)
		// global quit command in menu
		if input == "q" || input == "quit" {
			handler.CloseConnection()
			os.Exit(0)
		}
		found := false
		for _, command := range m.Commands {

			if input == command.Name {
				found = true
				err := command.Handler(&state, state.MenuDict)
				if err != nil {
					color.Red(err.Error())
				}
			}
		}
		if !found {
			color.Red("Такой команды нет :( Повторите попытку")
		}
	}

}

func ask(variable *string, varName string) {
	fmt.Print(color.CyanString("Enter "+varName) + ": ")
	_, _ = fmt.Scan(variable)
}

func printCommands(commands []menu.Command) {
	fmt.Println("==============")
	color.Blue("Меню. Доступные команды: ")
	for _, command := range commands {
		color.Yellow(command.Name)
	}
	fmt.Println("==============")
}

func shutdown(handler tcp.ConnectionHandler) {
	fmt.Println("Shutdown")
	handler.CloseConnection()
}
