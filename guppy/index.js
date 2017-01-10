var mango;
window.onload = function() {
    mango = new Mango("6001",{"dostuff":function(header,args){console.log("DOING STUFF",header,args);}});

    document.getElementById('xml_btn').onclick = function() {
        output('xml');
    };
    document.getElementById('text_btn').onclick = function() {
        output('text');
    };
    document.getElementById('latex_btn').onclick = function() {
        output('latex');
    };
    document.getElementById('clear_btn').onclick = function() {
	document.getElementById('stuff').innerHTML = '';
    };

    Guppy.get_symbols(["builtins","guppy/sym/symbols.json","guppy/sym/extra_symbols.json"]);
    var g1 = new Guppy("guppy1", {
	//'debug':10,
        'right_callback': function() {},
        'left_callback': function() {},
        'done_callback': function() { output('latex'); },
        //'blank_caret': "[?]",
        'empty_content': "\\color{gray}{\\text{Click here to start typing a mathematical expression}}"
    });
};

function output(texttype) {
    document.getElementById('stuff').innerHTML = texttype.toUpperCase() + ": <br />" + Guppy.instances.guppy1.get_content(texttype);
    mango.m_send("maths",{"latex":Guppy.instances.guppy1.get_content("latex"),
			  "text":Guppy.instances.guppy1.get_content("text"),
			  "xml":Guppy.instances.guppy1.get_content("xml")
			 });    
}
