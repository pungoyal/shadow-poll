
/* 
 * This is a bar chart of regional responses by category, shown on top of 
 * a bar chart of national responses by category
 * argument: regional_poll_responses 
 *           - list of responses by category for a region (what unit?)
 * arguments: national_poll_responses 
 *           - list of responses by category total (what unit?)
 */

window.onload=function() {
    var canvasWidth = 390;
    var factor = (canvasWidth/107);

    var paper = Raphael(document.getElementById("chart"), canvasWidth, 120);
	var colors=["#ccff8a","#ea4cf4","#f8b088","#8bc0fa"];
	var fontColors=["#75b907","#BC2EBC","#CC6633","#2966B8"];
	var x = 0;
    var y = 5;
    var darkHeight = 10;
    var lightHeight = 30;
    var fillerWidth = 2;

	for (var i=0; i < regional_poll_responses.length; i++) {
        var width = regional_poll_responses[i]*factor;
        var lightRectangle = paper.rect(x,y,width,lightHeight);
		lightRectangle.attr({
			fill: colors[i],
			stroke: colors[i],
			opacity: 0.30
		});

        var percentageText = paper.text(x+width/2.0,y+lightHeight/2.0,regional_poll_responses[i]+"%");
        percentageText.attr({
            fill: fontColors[i],
            stroke: fontColors[i],
            font: "12px 'Arial'",
            opacity: 1
        });

        var darkRectangle = paper.rect(x,y+lightHeight,width,darkHeight);
		darkRectangle.attr({
			fill: colors[i],
			stroke: colors[i],
			opacity: 1
		});
        x = x + width;
        
        var filler = paper.rect(x,y,fillerWidth,darkHeight + lightHeight);
        filler.attr({
            fill: "white",
            stroke: "white"
        });

        x = x + fillerWidth;
	};
    y = y+lightHeight;
    x=0;
    
    for (var i=0; i < national_poll_responses.length; i++) {
        var width = national_poll_responses[i]*factor;        
        var r = paper.rect(x, y+30, width, 5);
        r.attr({
            fill: colors[i],
            stroke: colors[i],
            opacity: 0.70
        });
        x = x + width;
        var filler = paper.rect(x,y+30,fillerWidth,5);
        filler.attr({
            fill: "white",
            stroke: "white"
        });

        x = x + fillerWidth;
    }
};