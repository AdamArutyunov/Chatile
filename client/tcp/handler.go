package tcp

import (
	"io/ioutil"
	"net"
)

type ConnectionHandler struct {
	connector Connector
	connection net.Conn
}

func (h *ConnectionHandler) openConnection() error{
	var err error
	h.connector = *NewConnector()
	h.connection, err = h.connector.Connect()
	if err != nil{
		return err
	}
	return nil
}

func (h *ConnectionHandler) closeConnection(){
	h.connection.Close()
}

func (h *ConnectionHandler) Send(data []byte) error{
	err := h.openConnection()
	if err != nil{
		return nil
	}
	_, err = h.connection.Write(data)
	if err != nil{
		return err
	}
	return nil
}

func (h *ConnectionHandler) ReadReply() (string, error){
	message, err := ioutil.ReadAll(h.connection)
	if err != nil{
		return "", err
	}
	h.closeConnection()
	return string(message), nil
}

