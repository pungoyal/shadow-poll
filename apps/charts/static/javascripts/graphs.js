window.onload=function() {
	var paper = Raphael(10, 50, 500, 200);
	var colors=["#ccff8a","#ea4cf4","#f8b088","#8bc0fa"]
	var fontColors=["#4CC552","magenta","orange","cornflowerblue"]
	var x = 20;
    var y = 80;
    var darkHeight = 10;
    var lightHeight = 40;
    var fillerWidth = 2;

	for (var i=0; i < data.length; i++) {
        var width = data[i]*4;
        var lightRectangle = paper.rect(x,y,width,lightHeight);
		lightRectangle.attr({
			fill: colors[i],
			stroke: colors[i],
			opacity: 0.30
		});

        var percentageText = paper.text(x+width/2.0,y+lightHeight/2.0,data[i]+"%")
        percentageText.attr({
            fill: fontColors[i],
            stroke: fontColors[i],
            fontSize: 20,
            opacity: 1
        });

        var darkRectangle = paper.rect(x,y+lightHeight,width,darkHeight);
		darkRectangle.attr({
			fill: colors[i],
			stroke: colors[i],
			opacity: 1
		});
        x = x + width;
        
        var filler = paper.rect(x,y,fillerWidth,darkHeight + lightHeight)
        filler.attr({
            fill: "white",
            stroke: "white"
        });

        x = x + fillerWidth;
	};
};