#!/usr/bin/emacs --script

(require 'json)

(defvar *mango-buffer* "")

(defun mango-init (host port) (make-network-process :name "mangoclient" :buffer "*mango*" :host host :family 'ipv4 :service port :sentinel 'mango-err :filter 'mango-recv))
  
(defun mango-check-complete (input) 
  (let* ((match-index (string-match-p "\n" input))
	 (data-len (number-to-string (substring input 0 match-index)))
	 (data (substring input (+ 1 match-index)))
	 (current-len (if match-index (length data) -1)))
    (if (>= data-len current-len)
	(progn
	  (setq *mango-buffer* (substring input (+ match-index data-len)))
	  (substring input match-index (+ match-index data-len)))
      nil)))

(defun mango-handle (data)
  (let* ((args (json-read-from-string data))
	 (name (alist-get '_name args)))
    (cond ((equal name "insert") (mango-insert args))
	  ((equal name "buffer") (mango-buffer args)))))

(defun mango-recv (process event)
  (setq *mango-buffer* (concat *mango-buffer* event))
  (let ((data (mango-check-complete *mango-buffer*)))
    (when data (mango-handle data))
  
(defun mango-err (&rest args) (message "Disconnected. Reconnceting...") (sit-for 3) (mango-init))

(defun mango-stop () (delete-process "mangoclient"))

(defun mango-send (name args)
  (let* ((name-args (cons '('_name . name) args)
	 (data (json-encode name-args))
	 (len (length msg))
	 (msg (concat (number-to-string len) "\n" data)))
    (process-send-string "mangoclient" msg))))

(defun mx () (process-send-string "mangoclient" (read-string "mx: ")))

(defun mango-insert (args) (insert (alist-get 'text args)))

(defun mango-buffer (args) (mango-send ("buffer" (text . (let ((s (buffer-string))) (set-text-properties 0 (length s) nil s) (message s))))))

(mango-init "127.0.0.1" 55521)

(mx)
