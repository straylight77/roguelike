package main

type MessageQueue struct {
	text []string
}

func NewMessageQueue() *MessageQueue {
	return &MessageQueue{}
}

func (mq *MessageQueue) Add(m string) {
	mq.text = append(mq.text, m)
}

func (mq *MessageQueue) Tail(n int) []string {
	length := len(mq.text)
	if length <= 5 {
		return mq.text
	} else {
		return mq.text[length-n:]
	}

}
