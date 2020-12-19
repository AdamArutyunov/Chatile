package tcp

import (
	"client/env"
	"fmt"
	"net"
	"strconv"
)

type Connector struct {
	config env.Config
	connection net.Conn
}

func NewConnector(config env.Config) *Connector {
	return &Connector{config: config}
}

func (c Connector) Connect() error{
	var err error
	connection, err := net.Dial("tcp", c.config.Host + ":" + strconv.Itoa(c.config.Port))
	c.connection = connection
	fmt.Println(c.connection)
	if err != nil{
		return err
	}
	return nil
}

func (c Connector) Send(data string) error{
	fmt.Println(c.connection, c.config)
	_, err := c.connection.Write([]byte("assayed"))
	if err != nil{
		return err
	}
	return nil
}

func (c Connector) ReadReply() (string, error){
	for {
		var reply string

		_, err := c.connection.Read([]byte(reply))
		if err != nil {
			return "", err
		}
		return reply, nil
	}
}