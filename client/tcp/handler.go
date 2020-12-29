package tcp

import (
	"encoding/json"
	"net"
)

type ConnectionHandler struct {
	connector  Connector
	connection net.Conn
}

type Answer struct {
	Header string `json:"header"`
	Body map[string]interface{}
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

func (h *ConnectionHandler) ReadReply() (Answer, error) {
	var ans Answer
	err := json.NewDecoder(h.connection).Decode(&ans)
	if err != nil{
		return ans, err
	}
	return ans, nil
}
