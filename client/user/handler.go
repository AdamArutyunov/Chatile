package user

import (
	"client/request"
	"client/tcp"
	"encoding/json"
	"errors"
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

func Login(login, password string, handler tcp.ConnectionHandler) (bool, Profile, error) {
	var p Profile
	data, err := json.Marshal(map[string]interface{}{"header": "login", "body": map[string]string{"login": login, "password": password}})
	if err != nil {
		return false, p, err
	}
	err = handler.Send(data)
	if err != nil {
		return false, p, err
	}
	req, err := handler.ReadReply()
	if err != nil {
		return false, p, nil
	}
	if req.Header == "error"{
		return false, p, request.HandleError(req)
	}
	authBody, ok := req.Body.(request.AuthBody)
	if !ok{
		return false, p, errors.New("can't decode req to struct")
	}

	p.Login, p.Password, p.Token = login, password, authBody.Token
	return true, p, nil
}


func UpdateOnline(handler tcp.ConnectionHandler, p Profile) error {
	data, err := json.Marshal(map[string]interface{}{"header": "online", "body": map[string]string{"token": p.Token}})
	if err != nil{
		return err
	}
	err = handler.Send(data)
	if err != nil{
		return err
	}
	req, err := handler.ReadReply()
	if err != nil{
		return err
	}
	if req.Header != "ok"{
		return request.HandleError(req)
	}
	return nil
}