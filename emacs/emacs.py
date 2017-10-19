import sys, os, re, time, zmq, traceback, json
from libmango import *

class emacs_agent(m_node):
      def __init__(self):  
            super().__init__(debug=True)
            self.pid = os.getpid()
            self.emacs_bind = "tcp://*:55521"

            self.interface.add_interface('emacs.yaml',{'insert':self.insert})

            self.emacs_socket = self.context.socket(zmq.STREAM)
            self.emacs_socket.bind(self.emacs_bind)
            self.add_socket(self.emacs_socket, self.emacs_input, self.emacs_error)
            self.sender = None
            self.run()

      def insert(self,header,args):
            if self.sender is None:
                  self.debug_print("NO SENDER")
                  return
            self.debug_print("SENDING",args['str'],"TO",self.sender)
            self.emacs_socket.send(self.sender,flags=zmq.SNDMORE)
            self.emacs_socket.send_string(args['str'],flags=zmq.SNDMORE)
            
      def emacs_error(self,msg):
            self.debug_print("EMACSSHOCK DX")
            
      def emacs_input(self):
            sender = self.emacs_socket.recv()
            if self.sender is None:
                  self.m_send("message",{"str":"Connected"})
            self.sender = sender
            msg = self.emacs_socket.recv().decode('utf-8')
            if len(msg) > 0: 
                  self.m_send("message",{"str":msg})

emacs_agent()
