from libmango import *
import random

class otto(m_node):
    def __init__(self):
        super().__init__(debug=True)
        self.interface.add_interface('otto.yaml',{'goaway':self.goaway, 'im_recv':self.im_recv})

        # For help message
        self.help_text = self.read_whole_file("./help")

        # For jokes
        self.jokes = []
        f = open("./jokes","r")
        for l in f:
            self.jokes += [l[:-1].split("...")]

        # For idle/away reporting
        self.check_idle = shlex.shlex("echo $(($(xssstate -i)/1000))")
        self.away_msg = None
        
        self.run()
        
    def read_whole_file(self,fn):
        with open(fn) as f: return f.read()

    def goaway(self, header, args):
        self.away_msg = args.get('msg',None)
        
    def im_recv(self,header,args):
        cmd = args['message']
        
        if cmd == "!joke":
            j = random.choice(self.jokes)
            self.debug_print("JOKE",j)
            self.m_send("im_send_to",{"msg":"[otto.joke]: " + j[0],"conv":args['conv']})
            for line in j[1:]:
                time.sleep(2)
                self.m_send("im_send_to",{"msg":"[otto.joke]: " + line,"conv":args['conv']})
                
        elif cmd == "!idle":
            if not self.away_msg is None:
                ans = "[otto.away]: {}".format(self.away_msg)
            else:
                secs = int(subprocess.check_output(self.check_idle).decode('utf-8'))
                if secs > self.idle_cutoff:
                    ans = "[otto.idle]: Idling for over 15 minutes"
                else:
                    ans = "[otto.idle]: Idling for {}:{:02}".format(int(secs/60),secs % 60)
            self.m_send("im_send_to",{"msg":ans,"conv":args['conv']})
            
        elif cmd == '!away':
            ans = '[otto.away]: {}'.format('[None]' if self.away_msg is None else self.away_msg)
            self.m_send("im_send_to",{"msg":ans,"conv":args['conv']})
            
        else:
            self.m_send("im_send_to",{"msg":"[otto.help]: " + self.help_text,"conv":args['conv']})
    
otto()
