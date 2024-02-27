package main

type MessageLog struct {
	text []string
}

// -----------------------------------------------------------------------
func NewMessageLog() *MessageLog {
	return &MessageLog{}
}

// -----------------------------------------------------------------------
func (mq *MessageLog) Add(m string) {
	mq.text = append(mq.text, m)
}

// -----------------------------------------------------------------------
func (mq *MessageLog) Tail(n int) []string {
	length := len(mq.text)
	if length <= 5 {
		return mq.text
	} else {
		return mq.text[length-n:]
	}

}
