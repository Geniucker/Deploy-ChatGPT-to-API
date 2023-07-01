package main

import (
	"flag"
)

func ParseParams() (listenAddr string, forwardAddr string, key string, certPath string, keyPath string) {
	flag.StringVar(&listenAddr, "listenAddr", ":8080", "address to listen on")
	flag.StringVar(&forwardAddr, "forwardAddr", "http://localhost:8079", "address to forward to")
	flag.StringVar(&key, "key", "", "custom key for authentication")
	flag.StringVar(&certPath, "certPath", "", "path to certificate")
	flag.StringVar(&keyPath, "keyPath", "", "path to key")
	flag.Parse()
	return
}
