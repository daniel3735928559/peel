(defun 'start-mango (port) (make-network-process :name "mangoserver" :buffer "*mango*" :family 'ipv4 :service port :filter (lambda (process event) (insert event)) :server 't))

(defun 'stop-mango () (delete-process "mangoserver"))
