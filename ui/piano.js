var animationSpeed = 30;
var animationCycle;

var canvas = document.getElementById("canvas");
var ctx = canvas.getContext('2d');
var WIDTH = canvas.width;
var HEIGHT = canvas.height;



init();                                                 

function init(){
//    animationCycle = setTimeout(function(){ requestAnimationFrame(draw) }, animationSpeed);
    setInterval(draw, animationSpeed);

}


function draw(){
    clear();
    drawBackground();
    drawKeys();
}


function drawBackground(){
    rect(0, 0, WIDTH, HEIGHT, "#000000")
}

function drawKeys(){

    // draw white keys
    // 8 is the stroke width set in the rect function

    for(var i = 0; i < 7; i++){
        var xPosition = 8 + (WIDTH/7 * i);
        var notes = ["C", "D", "E", "F", "G", "A", "B"]
        var color = keysDown[notes[i]] ? "red" : "#ffffff";

        rect(xPosition, 8, WIDTH/7 - 16, HEIGHT - 16, color);
    }

    // Db, Eb
    for(var j = 0; j < 2; j++){  
        var xPosition = (8 + WIDTH/7/2) + (WIDTH/7 * j);
        var notes = ["Db", "Eb"]
        var color = keysDown[notes[j]] ? "red" : "#000000";

        rect(xPosition, 8, WIDTH/7 - 16, HEIGHT/1.5 - 16, color);
    }

    // Gb, Ab, Bb
    for(var k = 0; k < 3; k++){
        var notes = ["Gb", "Ab", "Bb"]
        var xPosition = (8 + WIDTH/7* 3 + WIDTH/7/2) + (WIDTH/7 * k);
        var color = keysDown[notes[k]] ? "red" : "#000000";

        rect(xPosition, 8, WIDTH/7 - 16, HEIGHT/1.5 - 16, color);
    }

}


// LIBRARY CODE

function clear() {
    ctx.clearRect(0, 0, WIDTH, HEIGHT);                 // creates a rectangle the size of the entire canvas that clears the area
}

function circle(x,y,r, color, stroke) {
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI*2, false);               // start at 0, end at Math.PI*2
    ctx.closePath();
    ctx.fillStyle = color;

    if(stroke){
        if(player.powerUps.hyperspeed.active){
            ctx.strokeStyle = "#F9B600";
        } else {
            ctx.strokeStyle = "#0197FF";
        }
        ctx.lineWidth = 2;
    }


    ctx.fill();
}

function rect(x,y,w,h, color) {
    ctx.beginPath();
    ctx.rect(x,y,w,h);
    ctx.closePath();

    ctx.lineWidth = 8;
    ctx.strokeStyle = "#4d4d4d";
    ctx.fillStyle = color;
    ctx.stroke();
    ctx.fill();
}

function text(text, x, y, size, color, centerAlign){
    ctx.font =  size + "px Arial";
    ctx.fillStyle = color;

    if(centerAlign){
        ctx.textAlign = "center";
    } else {
        ctx.textAlign = "left";
    }

    ctx.fillText(text, x, y);
}

function line(x1, y1, x2, y2){
    ctx.beginPath();
    ctx.strokeStyle = "rgba(250,250,250, 0.4)";
    ctx.moveTo(x1,y1);
    ctx.lineTo(x2,y2);
    ctx.stroke();
}

/* other functions */

function randBetween(min, max){
    return Math.random() * (max - min) + min;
}
