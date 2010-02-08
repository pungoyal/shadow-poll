window.onload=function() {
	var paper = Raphael(10, 50, 320, 200);
	var data=[10,20,65,5];
	var colors=["red","blue","green","yellow"]
	var x = 20;
	for (var i=0; i < data.length; i++) {
		var rect = paper.rect(x,80,data[i]*2,10,2);
		rect.attr({
			fill: colors[i],
			stroke: colors[i],
			opacity: 0.80
		});
		x = x + data[i]*2;
	};
};