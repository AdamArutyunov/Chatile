package user

import (
	"client/tcp"
	"encoding/json"
	"github.com/fatih/color"
)

func Register(profile Profile, handler tcp.ConnectionHandler) error {
	data, err := json.Marshal(map[string]interface{}{"header": "register", "body": profile})
	if err != nil {
		return err
	}

	err = handler.Send(data)
	if err != nil {
		return err
	}
	return nil
}

func Login(login, password string, handler tcp.ConnectionHandler) (bool, Profile, error){
	var p Profile
	data, err := json.Marshal(map[string]interface{}{"header": "login", "body": map[string]string{"login": login, "password": password}})
	if err != nil {
		return false, p, err
	}
	err = handler.Send(data)
	if err != nil {
		return false, p, err
	}
	ans, err := handler.ReadReply()
	if err != nil{
		return false, p, nil
	}
	if ans.Header == "error"{
		color.Red("Ошибка авторизации")
		return false, p, nil
	}
	token, ok := ans.Body["token"].(string)
	if !ok{
		return false, p, nil
	}
	p.Login, p.Password, p.Token =  login, password, token
	return true, p, nil
}