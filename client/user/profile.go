package user

import (
	"golang.org/x/crypto/bcrypt"
)

type Profile struct {
	Name     string `json:"name"`
	Login    string `json:"login"`
	Password string `json:"password"`
	Token string `json:"-"`
}

func NewProfile(name string, login string, password string) *Profile {
	hashPassword, err := HashPassword(password)
	if err != nil {
		panic(err)
	}
	return &Profile{Name: name, Login: login, Password: hashPassword}
}

func HashPassword(password string) (string, error) {
	bytes, err := bcrypt.GenerateFromPassword([]byte(password), 14)
	return string(bytes), err
}
