from libmango import *
import random

class otto(m_node):
    def __init__(self):
        super().__init__(debug=True)
        self.interface.add_interface('otto.yaml',{'im_recv':self.im_recv})
        self.help_text = self.read_whole_file("./help")
        self.jokes = []
        f = open("./jokes","r")
        for l in f:
            self.jokes += [l[:-1].split("...")]
        self.run()
        
    def read_whole_file(self,fn):
        with open(fn) as f: return f.read()

    def im_recv(self,header,args):
        cmd = args['message']
        if(cmd == "!joke"):
            j = random.choice(self.jokes)
            self.debug_print("JOKE",j)
            i = 0
            l = len(j)
            for line in j:
                self.m_send("im_send_to",{"msg":"[otto.joke]: " + line,"conv":args['conv']})
                i += 1
                if i < l and l > 1:
                    time.sleep(2)

        else:
            self.m_send("im_send_to",{"msg":"[otto.help]: " + self.help_text,"conv":args['conv']})
    
otto()
