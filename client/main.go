package main

import (
	"client/menu"
	"errors"
	"fmt"
	"strings"
)

func main() {
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
				if strings.TrimSuffix(password, "\n") != "123321"{
					return errors.New("wrong password")
				}
				fmt.Println("Успешная авторизация")
				s.SetMenu(menuDict["loggedMenu"])
				return nil

			}},
		},
	}
	loggedMenu := menu.Menu{Commands: []menu.Command{
		{"test", func(s *menu.State, menuDict map[string]menu.Menu) error {
			fmt.Println("Hello, user")
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

		for _, command := range m.Commands{
			if input == command.Name{
				err := command.Handler(&state, state.MenuDict)
				if err != nil{
					fmt.Println(err)
				}
			}
		}
	}

}

func printCommands(commands []menu.Command){
	fmt.Println("==============")
	fmt.Println("Меню. Доступные команды: ")
	for _, command := range commands{
		fmt.Println(command.Name)
	}
	fmt.Println("==============")
}
