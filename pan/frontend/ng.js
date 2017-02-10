var app = angular.module('app',[]);

app.controller("PanController", ['$scope', '$sce', function($scope, $sce){    
    $scope.scans = {
	"tcp_flags":
	{
	    "flags":["URG","ACK","PSH","RST","SYN","FIN"],
	    "scan_type":["filtered","open|filtered"],
	},
    };
    
    $scope.help_text = {
	"tcp_flags":$sce.trustAsHtml("Send a single packet with specified TCP flags set.  Common combinations include: <ul> \
<li>SYN: Should elicit a response without making a full connection.</li> \
<li>ACK: Used to determine firewalled ports.</li> \
<li>FIN: </li> \
<li>FIN/ACK: Used to identify BSD systems.</li> \
<li>FIN/PSH/URG: </li> \
<li>[None]: </li></ul>"),
	"idle":"Spoofs the scan as coming from the idle \"zombie\" host and queries \
the zombie host for its IP ID to determine which ports are open.",
	"udp":"Send a UDP packet to the host",
	"tcp_connect":"Attempt a full TCP connection with the target port",
	"ftp":"Spoofs the scan as coming from a host that supports FTP proxying by \
using the (now rare) FTP proxy feature.",
	"window":"This is an ACK scan except it notes that some OSes will distinguish \
open ports from closed ones by setting the window size to a nonzero \
value for open ports and zero for closed ports, even on RST packets. \
This scan watches for this behaviour.",
	"sctp_init":"Send SCTP INIT chunks to the target ports.",
	"sctp_cookie":"Send SCTP COOKIE ECHO chunks to the target ports.",
	"ip_proto":"Determine what IP protocols are supported by the target",
	
    }
    $scope.speeds = {}
    $scope.top_ports = 1000;
    $scope.scan_type = "filtered";
    $scope.ports = "asd";

    // Evasion options
    $scope.scan_in_order = false;
    $scope.mtu = 0;
    $scope.decoys = [];

    $scope.targets = {"ips":"127.0.0.1", "ports":"9999"};
    
    $scope.params = {'tcp_flags':{"flags":{"URG":false,"ACK":false,"PSH":false,"RST":false,"SYN":true,"FIN":false},
				  "scan_type":"filtered"},
		     'idle':{"zombie":""},
		     'ftp':{"bounce":""},
		     'udp':true,
		     'sctp_init':true,
		     'sctp_cookie_echo':true,
		     'window':true,
		     'ip_proto':true,
		     "ping":true,
		     "tcp_connect":true,
		    };
    $scope.active_scans = {'tcp_flags':true, 'udp':false, 'idle':false, 'sctp_init':false, 'sctp_cookie_echo':false, 'ip_proto':false, 'ftp':false, "window":false, "ping":true, "tcp_connect":false};
    
    $scope.flag_toggle_flag = function(flag){
	$scope.params.tcp_flags.flags[flag] = !$scope.params.tcp_flags.flags[flag];
	console.log($scope.params.tcp_flags);
    }
    $scope.flag_set_type = function(t){
	$scope.params.tcp_flags.scan_type = t;
    }
    $scope.get_params = function(){
	var scans = {}
	for(var s in $scope.active_scans){
	    if($scope.active_scans[s]){
		scans[s] = $scope.params[s];
	    }
	}
	return {"scans":scans, "targets":$scope.targets,"hiding":{}};
    }
}]);
