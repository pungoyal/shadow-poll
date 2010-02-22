window.onload=function() {
    var canvasWidth = 420;
    var factor = (canvasWidth/107);

    var paper = Raphael(document.getElementById("voteBar"), canvasWidth, 120);
	var colors=["#ccff8a","#ea4cf4","#f8b088","#8bc0fa"];
	var fontColors=["#4CC552","magenta","orange","cornflowerblue"];
	var x = 0;
    var y = 5;
    var darkHeight = 10;
    var lightHeight = 40;
    var fillerWidth = 2;

	for (var i=0; i < data.length; i++) {
        var width = data[i]*factor;
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
    y = y+lightHeight;
    x=0;
    
    for (var i=0; i < country_data.length; i++) {
        var width = country_data[i]*factor;        
        var r = paper.rect(x, y+30, width, 5)
        r.attr({
            fill: colors[i],
            stroke: colors[i],
            opacity: 0.70
        });
        x = x + width;
        var filler = paper.rect(x,y,fillerWidth,darkHeight + lightHeight)
        filler.attr({
            fill: "white",
            stroke: "white"
        });

        x = x + fillerWidth;
    }
};