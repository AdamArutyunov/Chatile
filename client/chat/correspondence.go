package chat

import (
	"client/request"
	"client/tcp"
	"client/user"
	"encoding/json"
	"errors"
	"github.com/fatih/color"
	"time"
)

type CommunicateHandler struct {
	Profile user.Profile
	Tcp tcp.ConnectionHandler
}

func (ch CommunicateHandler) GetHistory(recipientLogin string) ([]request.Message, error){
	data, err := json.Marshal(map[string]interface{}{"header": "get_messages", "body": map[string]string{"token": ch.Profile.Token, "login": recipientLogin}})
	if err != nil{
		return nil, err
	}
	err = ch.Tcp.Send(data)
	if err != nil{
		return nil, err
	}
	reply, err := ch.Tcp.ReadReply()
	if err != nil{
		return nil, err
	}
	batch, ok := reply.Body.(request.BatchBody)
	if !ok{
		return nil, errors.New("can't cast to batch body")
	}
	return batch.Messages, nil
}

func parseSendingDate(sendingDate int) string{
	return time.Unix(int64(sendingDate), 0).Format("06-01-02 15:01:05")
}

func (ch CommunicateHandler) PrintMessages(messages []request.Message) {
	for _, message := range messages{
		messageColor := color.New(color.FgCyan).Add(color.Bold)
		_, _ = messageColor.Println(parseSendingDate(message.SendingDate) + "||" + "[" + message.SenderLogin + "]" + " " + message.Data)
	}
}