package user

import (
	"bufio"
	"client/tcp"
	"encoding/json"
	"fmt"
	"github.com/fatih/color"
	"os"
	"strings"
)

type Handler struct {
	tcp.ConnectionHandler
}

func (h *Handler) Register(args ...string) error{
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
	profile := NewProfile(strings.TrimSuffix(name, "\n"), strings.TrimSuffix(login, "\n"), strings.TrimSuffix(password, "\n"))
	color.Yellow("Вы действительно хотите зарегестрироваться?")
	color.Yellow("Введите y, если да, иначе любую другую букву")
	ask, _ := scanner.ReadString('\n')
	if strings.ToLower(strings.TrimSuffix(ask, "\n")) != "y"{
		return nil
	}
	data, err := json.Marshal(map[string]interface{}{"header": "register", "body": profile})
	if err != nil{
		return err
	}
	err = h.ConnectionHandler.Send(data)
	if err != nil{
		return err
	}

	ans, err := h.ReadReply()
	if err != nil{
		return err
	}
	fmt.Println("Результат, " + ans)


	return nil
}