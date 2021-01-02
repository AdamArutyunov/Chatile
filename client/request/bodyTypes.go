package request

type ErrorBody struct {
	Code    int
	Message string
}

type AuthBody struct {
	Token string
}
