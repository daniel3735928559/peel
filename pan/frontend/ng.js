var app = angular.module('app',[]);

app.controller("ElderberryController", ['$scope','$http', '$window', '$timeout', '$location', function($scope, $http, $window, $timeout, $location){    
    $scope.scans = {
	"tcp_flags":
	{
	    "flags":["URG","ACK","PSH","RST","SYN","FIN"],
	    "scan_type":["No response = filtered","No response = open|filtered"],
	    "help":"Select the TCP flags you want to scan.  Common combinations include: \n* SYN: For half-opening a connection.  This should elicit a response without making a full connection to the server, likely not appearing in the server's logs.\n* ACK: "
	},
	"udp":{"help":"Send a UDP packet to the host"},
	"idle":{
	    "options":["zombie_host"]},
	"sctp":{"help":""},
	"ip_proto":{"help":""},
	"ftp":{"help":""}
    };
    $scope.speeds = {}
    $scope.top_ports = 1000;
    $scope.scan_type = "No response = filtered";
    $scope.ports = "asd";

    // Evasion options
    $scope.scan_in_order = false;
    $scope.mtu = 0;
    $scope.decoys = [];

    $scope.flag_flags = {"URG":false,"ACK":false,"PSH":false,"RST":false,"SYN":true,"FIN":false};
    $scope.flag_toggle_flag = function(flag){
	$scope.flag_flags[flag] = !$scope.flag_flags[flag];
	console.log($scope.flag_flags);
    }
    $scope.flag_set_type = function(t){
	$scope.scan_type = t;
    }
    $scope.scan = function(){
	socket.emit('scan', data);
    }
}]);
