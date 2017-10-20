import sys, os, re, time, zmq, traceback, json
from libmango import *

class emacs_agent(m_node):
      def __init__(self):  
            super().__init__(debug=True)
            self.pid = os.getpid()
            self.emacs_bind = "tcp://*:55521"

            self.interface.add_interface('emacs.yaml',{'insert':self.insert,
                                                       'buffer':self.get_buffer})

            self.emacs_socket = self.context.socket(zmq.STREAM)
            self.emacs_socket.bind(self.emacs_bind)
            self.add_socket(self.emacs_socket, self.emacs_input, self.emacs_error)
            self.sender = None
            self.recv_buffer = ""
            self.run()

      def insert(self,header,args):
            if self.sender is None:
                  self.debug_print("NO SENDER")
                  return
            self.emacs_send("insert",{"text":args['str']})

      
      def get_buffer(self,header,args):
            if self.sender is None:
                  self.debug_print("NO SENDER")
                  return
            self.emacs_send("buffer",{})
            
      def emacs_send(self, name, args):
            args['_name'] = name
            data = json.dumps(args)
            msg = str(len(data)) + "\n" + data
            self.debug_print("SENDING",msg,"TO",self.sender)
            self.emacs_socket.send(self.sender,flags=zmq.SNDMORE)
            self.emacs_socket.send_string(msg,flags=zmq.SNDMORE)
            
      def emacs_error(self,msg):
            self.debug_print("EMACSSHOCK DX")

      def check_buffer(self):
            try:
                  l,d = self.recv_buffer.split("\n",1)
                  l = int(l)
                  if l > len(d):
                        return None
                  print("SPLITTING",d[:l],d[l:])
                  self.recv_buffer = d[l:]
                  return d[:l]
            except:
                  traceback.print_exc()
                  return None
            
      def emacs_input(self):
            sender = self.emacs_socket.recv()
            if self.sender is None:
                  self.m_send("message",{"str":"Connected"})
            self.sender = sender
            msg = self.emacs_socket.recv().decode('utf-8')
            if len(msg) == 0: return
            self.recv_buffer += msg
            print("GOT",msg)
            
            data = self.check_buffer()
            while not data is None:
                  print("DATA",data)
                  self.m_send("message",{"str":data})
                  data = self.check_buffer()
            print("done")

emacs_agent()
