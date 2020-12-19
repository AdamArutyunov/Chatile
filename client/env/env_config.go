package env

type Config struct {
	Host         string
	Port         int
}

func NewConfig() *Config {
	return &Config{Host: "192.168.0.109", Port: 1234}
}

