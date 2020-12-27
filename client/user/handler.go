package user

import (
	"client/tcp"
	"encoding/json"
	"fmt"
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

func Login(login, password string, handler tcp.ConnectionHandler) (bool, error){
	var ans string
	data, err := json.Marshal(map[string]interface{}{"header": "login", "body": map[string]string{"login": login, "password": password}})
	if err != nil {
		return false, err
	}
	err = handler.Send(data)
	if err != nil {
		return false, err
	}
	ans, err = handler.ReadReply()
	fmt.Println(ans)
	return true, nil
}