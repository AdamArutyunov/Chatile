package user

import (
	"client/tcp"
	"encoding/json"
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
