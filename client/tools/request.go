package tools

import "client/tcp"

func HandleOK(h *tcp.ConnectionHandler) (bool, error) {
	reply, err := h.ReadReply()
	if err != nil{
		return false, err
	}
	if reply.Header == "ok"{
		return true, nil
	}
	return false, nil
}

