package user

import (
	"client/tcp"
	"golang.org/x/crypto/bcrypt"
	"strings"
)


type Profile struct {
	Name string `json:"name"`
	Login string `json:"login"`
	Password string `json:"password"`
	tcp.Connector
}

func checkQuitCommand(data string) bool{
	data = strings.TrimSuffix(data, "\n")
	if data == "q" || data == "quit" || data == "exit"{
		return true
	}
	return false
}

func NewProfile(name string, login string, password string) *Profile {
	hashPassword, err := HashPassword(password)
	if err != nil{
		panic(err)
	}
	return &Profile{Name: name, Login: login, Password: hashPassword}
}

func HashPassword(password string) (string, error) {
	bytes, err := bcrypt.GenerateFromPassword([]byte(password), 14)
	return string(bytes), err
}



