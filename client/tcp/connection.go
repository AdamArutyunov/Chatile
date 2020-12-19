package tcp

import (
	"net"
	"strconv"
)

type Connector struct {
	connection net.Conn
	Addr string
}

func NewConnector() *Connector {
	addr := HOST + ":" + strconv.Itoa(PORT)
	return &Connector{Addr: addr}
}

func (c *Connector) GetConnection() net.Conn{
	return c.connection
}

func (c *Connector) Connect() (net.Conn, error){
	var err error
	conn, err := net.Dial("tcp", c.Addr)
	if err != nil{
		return nil ,err
	}
	return conn, nil
}


