#!/usr/bin/emacs --script

(require 'json)

(defvar *mango-buffer* "")

(defvar *mango-host* "")
(defvar *mango-port* "")

(defun mango-init (host port)
  (setq *mango-buffer* "")
  (setq *mango-host* host)
  (setq *mango-port* port)
  (make-network-process :name "mangoclient" :buffer "*mango*" :host host :family 'ipv4 :service port :sentinel 'mango-err :filter 'mango-recv))
  
(defun mango-check-complete (input) 
  (let* ((match-index (string-match-p "\n" input))
	 (data-len (string-to-number (substring input 0 match-index)))
	 (data-val (substring input (+ 1 match-index)))
	 (current-len (if match-index (length data-val) -1)))
    (if (>= current-len data-len)
	(progn
	  (message (concat "M1 " *mango-buffer*))
	  (setq *mango-buffer* (substring input (+ match-index data-len 1)))
	  (message (concat "M2 " *mango-buffer*))
	  (message (concat "M4 " (substring input (+ 1 match-index) (+ match-index data-len 1))))
	  (substring input (+ 1 match-index) (+ match-index data-len 1)))
      (message (concat "M3 " *mango-buffer* " " (number-to-string data-len) ":" (number-to-string current-len))) nil)))

(defun mango-handle (data)
  (let* ((args (json-read-from-string data))
	 (name (alist-get '_name args)))
    (cond ((equal name "insert") (mango-insert args))
	  ((equal name "buffer") (mango-buffer args)))))

(defun mango-recv (process event)
  (setq *mango-buffer* (concat *mango-buffer* event))
  (let* ((data (mango-check-complete *mango-buffer*)))
    (when data (mango-handle data))))
  
;; (defun mango-err (&rest args)
;;   (message "Disconnected. Reconnceting...")
;;   (sit-for 3)
;;   (mango-init *mango-host* *mango-port*))
(defun mango-err (&rest args) (message "Disconnected."))

(defun mango-stop () (delete-process "mangoclient"))

(defun mango-send (name args)
  (let* ((name-args (cons `(_name . ,name) args))
	 (data (json-encode-alist name-args))
	 (len (length data))
	 (x (message (concat "SENDING " data)))
	 (msg (concat (number-to-string len) "\n" data)))
    (process-send-string "mangoclient" msg)))

(defun mx () (process-send-string "mangoclient" (read-string "mx: ")))

(defun mango-insert (args) (insert (alist-get 'text args)))

(defun mango-buffer (args) (mango-send "buffer" (let ((s (buffer-string))) (set-text-properties 0 (length s) nil s) (list `(text . ,s)))))

(mx)

(mango-stop)

(mango-init "127.0.0.1" 55521)
