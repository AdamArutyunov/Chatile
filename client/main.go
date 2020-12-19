package main

import (
	"bufio"
	"client/env"
	"client/tcp"
	"client/user"
	"fmt"
	"github.com/fatih/color"
	"log"
	"os"
	"strings"
)


func checkQuitCommand(data string) bool{
	data = strings.TrimSuffix(data, "\n")
	if data == "q" || data == "quit" || data == "exit"{
		return true
	}
	return false
}

func auth(args ...string) error {
	// Do something
	fmt.Println("Output of cmd1")
	return nil
}

func prepareRegister(args ...string) error{
	var name, login, password, password2 string
	scanner := bufio.NewReader(os.Stdin)

	fmt.Print(color.WhiteString("Enter name: " ))
	name, _ = scanner.ReadString('\n')
	if checkQuitCommand(name){
		color.Cyan("Go to menu")
		return nil
	}

	fmt.Print(color.WhiteString("Enter login: " ))
	login, _ = scanner.ReadString('\n')
	if checkQuitCommand(login){
		color.Cyan("Go to menu")
		return nil
	}

	fmt.Print(color.WhiteString("Enter password: " ))
	password, _ = scanner.ReadString('\n')
	if checkQuitCommand(password){
		color.Cyan("Go to menu")
		return nil
	}

	fmt.Print(color.WhiteString("Repeat password: " ))
	password2, _ = scanner.ReadString('\n')
	if checkQuitCommand(password2){
		color.Cyan("Go to menu")
		return nil
	}
	if password != password2{
		color.Red("Пароли не совпадают, выходим в главное меню....")
		return nil
	}
	profile := user.NewProfile(name, login, password)
	color.Yellow("Вы действительно хотите зарегестрироваться?")
	color.Yellow("Введите y, если да, иначе любую другую букву")
	ask, _ := scanner.ReadString('\n')
	if strings.ToLower(strings.TrimSuffix(ask, "\n")) != "y"{
		return nil
	}
	fmt.Println(profile)
	return nil
}

func main() {
	config := env.NewConfig()
	connection := tcp.NewConnector(*config)
	err := connection.Connect()
	if err != nil{
		log.Fatalln(err)
	}
	err = connection.Send("hello")
	if err != nil{
		log.Fatalln(err)
	}

	data, err := connection.ReadReply()
	if err != nil{
		log.Fatalln(err)
	}
	fmt.Println(data)
	/*
	commandOptions := []menu.CommandOption{
		{"login", "Login", auth},
		{"register", "Register", prepareRegister},
	}

	menuOptions := menu.NewMenuOptions("'menu' for help > ", 0)


	switcher := menu.NewMenu(commandOptions, menuOptions)
	config := env.NewConfig()
	fmt.Println(config)
	switcher.Start()
	*/

}