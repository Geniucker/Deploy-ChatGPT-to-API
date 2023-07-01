package main

import (
	"log"
)

func main() {
	listenAddr, forwardAddr, key, certPath, keyPath := ParseParams()
	log.Printf("Listening on %s, forwarding to %s", listenAddr, forwardAddr)

	AuthenticationAndForward(listenAddr, forwardAddr, key, certPath, keyPath)
}
