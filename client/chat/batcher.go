package chat

import (
	"client/request"
	"context"
	"fmt"
	"log"
)

func (ch CommunicateHandler) StartBatch(ctx context.Context, wait chan struct{}) {
	defer func() {
		close(wait)
	}()
	for {
		select {
		case <-ctx.Done():
			fmt.Println("Batcher stopped")
			return
		default:
			reply, err := ch.Tcp.ReadReply()
			if err != nil{
				log.Fatalln(err)
			}
			if reply.Header != "message"{
				continue
			}
			messageBody := reply.Body.(request.MessageBody)
			ch.PrintMessages([]request.Message{messageBody.Message})
		}
	}
}





