package request

import (
	"encoding/json"
	"errors"
	"strconv"
)

type Req struct {
	Header string `json:"header"`
	RawBody   json.RawMessage `json:"body"`
	Body interface{}
}

func (r *Req) ParseReq() error{
	switch r.Header {
	case "error":
		{
			var eBody ErrorBody
			err := json.Unmarshal(r.RawBody, &eBody)
			r.Body = eBody
			return err
		}
	case "auth":
		{
			var aBody AuthBody
			err := json.Unmarshal(r.RawBody, &aBody)
			r.Body = aBody
			return err
		}
	}
	return errors.New("struct not found to decode")
}


func HandleError(r Req) error {
	errBody, ok := r.Body.(ErrorBody)
	if !ok{
		return errors.New("can't cast errorBody")
	}
	return errors.New(strconv.Itoa(errBody.Code) + "||" + errBody.Message)
}