#!/usr/bin/emacs --script

(require 'json)

(defun start-mango (host port) (make-network-process :name "mangoclient" :buffer "*mango*" :host host :family 'ipv4 :service port :sentinel 'mango-err :filter 'mango-recv))

(defun mango-recv (process event) (insert event))

(defun mango-err (&rest args) (message "err" args))

(defun stop-mango () (delete-process "mangoclient"))

(defun mx () (process-send-string "mangoclient" (read-string "mx: ")))

(start-mango "127.0.0.1" 55521)

(mx)
;(json-read-from-string "{\"asda\":\"4\",\"asd\":2}")

