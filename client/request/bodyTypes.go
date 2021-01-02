package request

type Message struct {
	SenderLogin    string `json:"sender_login"`
	RecipientLogin string `json:"recipient_login"`
	Data string `json:"data"`
	SendingDate int `json:"sending_date"`
}

type ErrorBody struct {
	Code    int
	Message string
}

type AuthBody struct {
	Token string
}


type BatchBody struct {
	Messages []Message
}