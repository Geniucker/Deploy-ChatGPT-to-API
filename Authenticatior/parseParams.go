package main

import (
	"flag"
)

func ParseParams() (listenAddr string, forwardAddr string, key string) {
	flag.StringVar(&listenAddr, "listenAddr", ":8080", "address to listen on")
	flag.StringVar(&forwardAddr, "forwardAddr", "http://localhost:8079", "address to forward to")
	flag.StringVar(&key, "key", "", "custom key for authentication")
	flag.Parse()
	return
}
