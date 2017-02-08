from libmango import *
import shlex, subprocess

class pan(m_node):
    def __init__(self):
        super().__init__(debug=True)
        self.interface.add_interface('pan.yaml',{'scan':self.scan})
        self.run()
    def scan(self,header,args):
        cmd_args = ""
        
        if 'ports' in args:
            cmd_args += " -p " + args['ports']
            
        if not args['scans'].get('ping', False): cmd_args += " -Pn"
            
        if args['scans'].get('tcp_connect', False): cmd_args += " -sT"
        if args['scans'].get('udp', False): cmd_args += " -sU"
        if args['scans'].get('sctp', False): cmd_args += " -sY"
        if args['scans'].get('ip_proto', False): cmd_args += " -sO"
        if args['scans'].get('sctp_init', False): cmd_args += " -sY"
        if args['scans'].get('sctp_cookie_echo', False): cmd_args += " -sZ"
        if args['scans'].get('window', False): cmd_args += " -sW"

        if 'ftp' in args['scans']: cmd_args += " -b "+args['scans']['ftp']['bounce_host']
        if 'idle' in args['scans']: cmd_args += " -b "+args['scans']['ftp']['zombie_host']

        if 'tcp_flags' in args['scans']:
            flags = args['scans']['tcp_flags']['flags']
            cmd_args += " --scanflags \"" + "".join([f for f in flags if flags[f]]) + "\""
            if args['scans']['tcp_flags']['scan_type'].get('no_response_filtered',False):
                cmd_args += " -sA"
            else:
                cmd_args += " -sF"
        
        cmd_args += " " + args['targets']
        cmd = "nmap " + cmd_args
        print(cmd)
        subprocess.Popen(shlex.split(cmd), env=nenv)
        return {'excited':args['str']+'!'}

pan()
