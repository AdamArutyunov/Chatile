package request

import (
	"errors"
	"strconv"
)

func HandleError(r Req) error {
	errBody, ok := r.Body.(ErrorBody)
	if !ok{
		return errors.New("can't cast errorBody")
	}
	return errors.New(strconv.Itoa(errBody.Code) + "||" + errBody.Message)
}
