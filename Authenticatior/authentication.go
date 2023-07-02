package main

import (
	"io"
	"log"
	"net/http"
	"os"
)

func authentication(key string, next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		log.Printf("Received %s request for %s", r.Method, r.URL.Path)
		if key != "" && r.Method != "OPTIONS" && r.Header.Get("Authorization") != "Bearer "+key {
			http.Error(w, "Unauthorized", http.StatusUnauthorized)
			log.Printf("Unauthorized %s request for %s", r.Method, r.URL.Path)
			return
		}

		next.ServeHTTP(w, r)
	})
}

func handleRequests(forwardAddr string) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// create new request to forwardAddr
		req, err := http.NewRequest(r.Method, forwardAddr+r.URL.Path, r.Body)
		if err != nil {
			log.Printf("Failed to create request: %s", err)
			http.Error(w, "Bad Gateway", http.StatusBadGateway)
			return
		}
		// copy request headers
		req.Header = r.Header.Clone()
		// send request
		client := &http.Client{}
		resp, err := client.Do(req)
		if err != nil {
			log.Printf("Failed to execute request: %s", err)
			http.Error(w, "Bad Gateway", http.StatusBadGateway)
			return
		}
		defer resp.Body.Close()

		// send data back to client
		// copy response headers
		for k, v := range resp.Header {
			w.Header()[k] = v
		}
		// use small buffer to flush immediately
		flusher, _ := w.(http.Flusher)
		buf := make([]byte, 64)
		for {
			n, err := resp.Body.Read(buf)
			if err == io.EOF {
				break
			} else if err != nil {
				http.Error(w, "Wrong streaming", http.StatusBadGateway)
				return
			} else {
				if n > 0 {
					w.Write(buf[:n])
					flusher.Flush()
				}
			}
		}

		log.Printf("Finished %s request for %s", r.Method, r.URL.Path)
	})
}

func AuthenticationAndForward(listenAddr string, forwardAddr string, key string, certPath string, keyPath string) {
	handler := authentication(key, handleRequests(forwardAddr))

	http.Handle("/", handler)

	log.Printf("Starting HTTP proxy on %s", listenAddr)
	var err error
	if fileExists(certPath) && fileExists(keyPath) {
		err = http.ListenAndServeTLS(listenAddr, certPath, keyPath, nil)
	} else {
		err = http.ListenAndServe(listenAddr, nil)
	}
	if err != nil {
		log.Fatalf("Failed to listen on %s: %s", listenAddr, err)
	}
}

func fileExists(path string) bool {
	if path == "" {
		return false
	}
	_, err := os.Stat(path)
	return !os.IsNotExist(err)
}
