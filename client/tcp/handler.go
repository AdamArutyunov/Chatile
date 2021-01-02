package tcp

import (
	"client/request"
	"encoding/json"
	"net"
)

type ConnectionHandler struct {
	connector  Connector
	connection net.Conn
}

func (h *ConnectionHandler) OpenConnection() error {
	var err error
	h.connector = *NewConnector()
	h.connection, err = h.connector.Connect()
	if err != nil {
		return err
	}
	return nil
}

func (h *ConnectionHandler) CloseConnection() {
	_ = h.connection.Close()
}

func (h *ConnectionHandler) Send(data []byte) error {
	_, err := h.connection.Write(data)
	if err != nil {
		return err
	}
	return nil
}

func (h *ConnectionHandler) ReadReply() (interface{}, error) {
	var r request.Req
	err := json.NewDecoder(h.connection).Decode(&r)
	if err != nil {
		return r, err
	}
	err = r.ParseReq()
	if err != nil{
		return nil, err
	}
	return r, nil
}
