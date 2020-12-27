package main

import (
	"client/menu"
	"client/tcp"
	"client/user"
	"errors"
	"fmt"
	"github.com/fatih/color"
	"strings"
)

func main() {
	handler := tcp.ConnectionHandler{}

	state := menu.State{MenuDict: map[string]menu.Menu{}}
	mainMenu := menu.Menu{
		Commands: []menu.Command{
			{"help", func(s *menu.State, menuDict map[string]menu.Menu) error {
				fmt.Println("help command")
				return nil
			}},
			{"login", func(s *menu.State, menuDict map[string]menu.Menu) error {
				var password string
				_, _ = fmt.Scanln(&password)
				if strings.TrimSuffix(password, "\n") != "123321" {
					return errors.New("wrong password")
				}
				fmt.Println("Успешная авторизация")
				s.SetMenu(menuDict["loggedMenu"])
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
				if err != nil{
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
			return nil
		}},
		{"logout", func(s *menu.State, menuDict map[string]menu.Menu) error {
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

		for _, command := range m.Commands {
			if input == command.Name {
				err := command.Handler(&state, state.MenuDict)
				if err != nil {
					color.Red(err.Error())
				}
			}
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
