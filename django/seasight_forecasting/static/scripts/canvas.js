function drawbackground(canvas, context, onload) {
    var imagePaper = new Image();
        imagePaper.onload = function(){
            context.drawImage(imagePaper, 0, 0, 725, 500);
            onload(context);
        };

    imagePaper.src = "../static/img/world_map.jpg";
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
    1: "North Atlantic Ocean",
    2: "South Atlantic Ocean",
    3: "Indian Ocean",
    4: "West Pacific Ocean",
    5: "North-East Pacific Ocean",
    6: "South-East Pacific Ocean"
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
    {x: 20, y: 150, w: 156, h: 150, r: 5},
    {x: 20, y: 304, w: 196, h: 140, r: 6},
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

function validatePastForm() {
    var toreturn = 1;
    var region = document.forms["GenerateKML"]["region"].value;
    var dateFrom = document.forms["GenerateKML"]["dateFrom"].value;
    var check = document.forms["GenerateKML"]["check"].checked;
    var dateTo = document.forms["GenerateKML"]["dateTo"].value;
    document.getElementById("regionVal").innerHTML = "";
    document.getElementById("dateFromVal").innerHTML = "";
    document.getElementById("dateToVal").innerHTML = "";
    if (region == "--") {
        document.getElementById("regionVal").innerHTML = "Choose a region over the map.";
        toreturn = 0;
    }
    if (dateFrom == "") {
        document.getElementById("dateFromVal").innerHTML = "Choose a date.";
        toreturn = 0;
    }
    if (check == true && dateTo == "") {
        document.getElementById("dateToVal").innerHTML = "Choose a date.";
        toreturn = 0;
    }
    if (toreturn == 0) {
        return false;
    }
}

function validateForm() {
    var toreturn = 1;
    var region = document.forms["GenerateKML"]["region"].value;
    document.getElementById("regionVal").innerHTML = "";
    if (region == "--") {
        document.getElementById("regionVal").innerHTML = "Choose a region over the map.";
        toreturn = 0;
    }
    if (toreturn == 0) {
        return false;
    }
}

function onSubmit() {
    enableSpinner();
    return true;
}

function checkVerbose() {
    jQuery.get("../static/scripts/verbose.txt",function(data){$('#verbose').html(data);});
    setTimeout(function(){checkVerbose() },1000);
}

function enableSpinner() {
    $('#spinner').show();
}

function disableSpinner() {
    $('#spinner').hide();
}

$(document).ready(function() {
    disableSpinner();
});

checkVerbose();