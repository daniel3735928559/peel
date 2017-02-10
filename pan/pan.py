from libmango import *
import shlex, subprocess, tempfile, os

class pan(m_node):
    def __init__(self):
        super().__init__(debug=True)
        self.interface.add_interface('pan.yaml',{'scan':self.scan})
        self.run()
    def scan(self,header,args):
        cmd_args = ""
        
        if 'ports' in args['targets']:
            cmd_args += " -p " + args['targets']['ports']
            
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
            if args['scans']['tcp_flags']['scan_type'] == "filtered":
                cmd_args += " -sS"
            else:
                cmd_args += " -sF"
        
        cmd_args += " " + args['targets']['ip']

        fd, filename = tempfile.mkstemp();
        os.close(fd);
        print("FN",filename)
        cmd = "nmap -oX " + filename + cmd_args
        print("CMD",cmd)
        proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        print("OUTPUT",out,err)
        with open(filename) as f:
            xml_result = f.read()
        self.m_send("results",{"raw":out.decode('ascii') + "\n" + err.decode('ascii'),'xml':xml_result})
        print("DONE")
pan()
