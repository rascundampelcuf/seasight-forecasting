function drawbackground(canvas, context, onload) {
    var imagePaper = new Image();
        imagePaper.onload = function(){
            context.drawImage(imagePaper, 0, 0, 725, 500);
            onload(context);
        };

    imagePaper.src = "../static/seasight_forecasting/img/world_map.jpg";
}

function drawlines(ctx) {
    while(r = rects[i++]) {
        ctx.beginPath();
        ctx.lineWidth = "4";
        ctx.strokeStyle = "red";
        ctx.rect(r.x, r.y, r.w, r.h);
        ctx.stroke();
    }
}
var regionDict = {
    0: "--",
    1: "Atlantic North Ocean",
    2: "Atlantic South Ocean",
    3: "Indian Ocean",
    4: "West Pacific Ocean",
    5: "East Pacific Ocean"
}

function setRegion(region) {
    document.getElementById("region").value = regionDict[region];
}

var canvas = document.getElementById("myCanvas");
var ctx = canvas.getContext("2d");
var rects = [
    {x: 180, y: 100, w: 240, h: 200, r: 1},
    {x: 220, y: 304, w: 170, h: 140, r: 2},
    {x: 424, y: 220, w: 140, h: 224, r: 3},
    {x: 568, y: 120, w: 140, h: 324, r: 4},
    {x: 20, y: 150, w: 156, h: 294, r: 5},
], i = 0, r;
var region = 0;
ctx.clearRect(0, 0, canvas.width, canvas.height);
drawbackground(canvas, ctx, drawlines);

canvas.onclick  = function(e) {
    // important: correct mouse position:
    var rect = this.getBoundingClientRect(),
        x = e.clientX - rect.left,
        y = e.clientY - rect.top,
        i = 0, r;

    region = 0;
    while(r = rects[i++]) {
        ctx.beginPath();
        ctx.rect(r.x, r.y, r.w, r.h);
        if (ctx.isPointInPath(x, y)) {
            ctx.strokeStyle = "blue";
            region = r.r;
        } else {
            ctx.strokeStyle = "red";
        }
        ctx.stroke();
    }

    setRegion(region);
};