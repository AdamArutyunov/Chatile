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
			var errBody ErrorBody
			err := json.Unmarshal(r.RawBody, &errBody)
			r.Body = errBody
			return err
		}
	case "auth":
		{
			var authBody AuthBody
			err := json.Unmarshal(r.RawBody, &authBody)
			r.Body = authBody
			return err
		}
	case "message_batch":
		{
			var batchBody BatchBody
			err := json.Unmarshal(r.RawBody, &batchBody)
			r.Body = batchBody
			return err
		}

	}

	return nil
}


func HandleError(r Req) error {
	errBody, ok := r.Body.(ErrorBody)
	if !ok{
		return errors.New("can't cast errorBody")
	}
	return errors.New(strconv.Itoa(errBody.Code) + "||" + errBody.Message)
}