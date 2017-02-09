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
	"idle":"Lorem ipsum",
	"udp":"Send a UDP packet to the host",
	"tcp_connect":"Attempt a full TCP connection with the target port",
	"ftp":"Lorem Ipsum",
	"window":"Lorem Ipsum",
	"sctp_init":"Lorem Ipsum",
	"sctp_cookie":"Lorem Ipsum",
	"ip_proto":"Lorem Ipsum",
	
    }
    $scope.speeds = {}
    $scope.top_ports = 1000;
    $scope.scan_type = "filtered";
    $scope.ports = "asd";

    // Evasion options
    $scope.scan_in_order = false;
    $scope.mtu = 0;
    $scope.decoys = [];

    $scope.active_scans = {'tcp_flags':true, 'udp':false, 'idle':false, 'sctp':false, 'ip_proto':false, 'ftp':false};
    $scope.flag_flags = {"URG":false,"ACK":false,"PSH":false,"RST":false,"SYN":true,"FIN":false};
    $scope.flag_toggle_flag = function(flag){
	$scope.flag_flags[flag] = !$scope.flag_flags[flag];
	console.log($scope.flag_flags);
    }
    $scope.flag_set_type = function(t){
	$scope.scan_type = t;
    }
}]);
