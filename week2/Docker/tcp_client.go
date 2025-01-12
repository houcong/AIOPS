package main

import (
	"fmt"
	"io"
	"net"
	"os"
)

const (
	CONN_HOST = "localhost"
	CONN_PORT = "3333"
	CONN_TYPE = "tcp"
)

func main() {
	conn, err := net.Dial(CONN_TYPE, CONN_HOST+":"+CONN_PORT)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	ReadNWrite(conn)
	err = conn.Close()
	if err != nil {
		fmt.Println("failed to close connection:", err)
	}
}

func ReadNWrite(conn net.Conn) {
	message := "Test Request\n"
	_, write_err := conn.Write([]byte(message))
	if write_err != nil {
		fmt.Println("failed:", write_err)
		return
	}
	buf, read_err := io.ReadAll(conn)
	if read_err != nil {
		fmt.Println("failed:", read_err)
		return
	}
	conn.(*net.TCPConn).CloseWrite()
	buf, read_err = io.ReadAll(conn)
	if read_err != nil {
		fmt.Println("failed:", read_err)
		return
	}
	fmt.Println(string(buf))
}