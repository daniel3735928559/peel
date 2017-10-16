from libmango import *

class otto(m_node):
    def __init__(self):
        super().__init__(debug=True)
        self.interface.add_interface('otto.yaml',{'im_recv':self.im_recv})
        self.debug_print("running")
        self.run()
    def im_recv(self,header,args):
        return "im_send_to",{"msg":"otto here","conv":args['conv']}
    
otto()
