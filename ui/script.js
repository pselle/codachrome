console.log("hey!");

// midi stuff

if (navigator.requestMIDIAccess) {
    console.log('This browser supports WebMIDI!');

} else {
    console.log('WebMIDI is not supported in this browser.');
}

navigator.requestMIDIAccess()
    .then(onMIDISuccess, onMIDIFailure);




octave = 4;

var keysDown = {
  "C": false,   
  "D": false,   
  "E": false,   
  "F": false,   
  "G": false,   
  "A": false,   
  "B": false,   
  "C": false,   

  "Db": false, 
  "Eb": false, 
  "Gb": false, 
  "Ab": false, 
  "Bb": false 
}

// initialize function that runs on page launch

function init(){

  // enable key listeners

  enableKeyboardKeys();
  enableSliders();


  var song = [63, 70, 78, 56, 34, 63];
  //playArrayOfNotes(song);

}

init();

attackTime = 0;
releaseTime = 0;


function enableKeyboardKeys(){


    var keyboardPitchCodes = {
      65 : "C",   
      83 : "D",   
      68 : "E",   
      70 : "F",   
      71 : "G",   
      72 : "A",   
      74 : "B",   
      75 : "C",   

      87 : "Db", 
      69 : "Eb", 
      84 : "Gb", 
      89 : "Ab", 
      85 : "Bb"
    }



    document.querySelector("body").addEventListener("keydown", function(e){


        let noteInfo = codeInfo(code);
      // CALL FUNCTION TO PLAY SOUND ... or do whatever with it :)
      
        keysDown[noteInfo.name] = (midiMessage.data[0] == 144) ? true : false;



      // ensure that our keydown doesn't keep triggering the same note again and again
      if(typeof(keyboardPitchCodes[e.keyCode]) != "undefined" && !keysDown[codeInfo(e.keyCode).name].playing){
          console.log("play " + codeInfo(e.keyCode).note);
          
          gainNode.connect(audioCtx.destination);
          noteData[e.keyCode].playing = true;

          // simulating a velocity of 127 - the loudest MIDI value
          playFrequency(noteData[e.keyCode].freq, 127);
      }
    });

    document.querySelector("body").addEventListener("keyup", function(e){
      if(typeof(keyboardPitchCodes[e.keyCode]) != "undefined"){
          console.log("stop " + codeInfo(e.keyCode).note);
          noteData[e.keyCode].playing = false;
          if(notesBeingPlayed() == 0){
            gainNode.gain.cancelScheduledValues(audioCtx.currentTime);
            gainNode.gain.linearRampToValueAtTime(0, audioCtx.currentTime + releaseTime);
          }
          
      }
      
    });
}

function enableSliders(){

    document.querySelector("#attack").addEventListener("change", function(e){
        attackTime = Number(e.target.value);
        document.querySelector("#attack-value").innerText = e.target.value;
    });

    document.querySelector("#release").addEventListener("change", function(e){
        releaseTime = Number(e.target.value);
        document.querySelector("#release-value").innerText = e.target.value;
    });
}

/* WebAudio API */

// for legacy browsers
const AudioContext = window.AudioContext || window.webkitAudioContext;


// create a new audio context
const audioCtx = new AudioContext();

// Try making an oscillator
const osc = audioCtx.createOscillator();
const gainNode = audioCtx.createGain();
osc.type = 'sawtooth';
osc.start();

setInterval(function(){

  document.getElementById("current-gain").innerText = Math.floor(gainNode.gain.value*100)/100;
}, 10)




// connect the oscillator to gain node, and the gain node to the audio context
osc.connect(gainNode);
gainNode.connect(audioCtx.destination);
gainNode.gain.value = 0;




function playFrequency(freq, velocity){

  console.log("playing ", freq);

  // set the pitch
  osc.frequency.setValueAtTime(freq, audioCtx.currentTime);

  gainNode.gain.value = 0;

  if(velocity > 0){
    gainNode.gain.cancelScheduledValues(audioCtx.currentTime);
    gainNode.gain.linearRampToValueAtTime(velocity/127, audioCtx.currentTime + attackTime);
  }

}

function notesBeingPlayed(){

  var notesPressed = 0;

  for(key in noteData){

    if(noteData[key].playing){
      notesPressed++;
    }
  }

  console.log("Notes still pressed: " + notesPressed);
  return notesPressed;

}



/* MIDI in */

function onMIDISuccess(midiAccess) {

  console.log(midiAccess.inputs);
  console.log(midiAccess.outputs);

  for (var input of midiAccess.inputs.values())
      input.onmidimessage = getMIDIMessage;
}

function onMIDIFailure() {
    console.log('Could not access your MIDI devices.');
}

function getMIDIMessage(midiMessage) {
    console.log(midiMessage.data);
    let onOffCode = midiMessage.data[0];
    let pitchCode = midiMessage.data[1];
    let velocity = midiMessage.data[2]
    
    let noteInfo = codeInfo(pitchCode);
  // CALL FUNCTION TO PLAY SOUND ... or do whatever with it :)
      
    console.log(onOffCode);
    keysDown[noteInfo.name] = (onOffCode == 144) ? true : false;

    playFrequency(noteInfo.frequency, velocity);
}


/* --------- */

function codeToFrequency(code) {
    let semitoneRatio = 2 ** (1/12);
    let baselineFrequency = 27.5;
    let baselineCode = 21; // MIDI code for lowest note on keyboard
    let stepsAboveBaseline = code - baselineCode;
    
    return baselineFrequency * (semitoneRatio ** stepsAboveBaseline);
}



// a function that takes a midi pitch code, and returns the frequency, octave info, and note name 
function codeInfo(code) {

    let notes = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

    let semitoneRatio = 2 ** (1/12);
    let baselineFrequency = 27.5;
    let baselineCode = 21; // MIDI code for lowest note on keyboard
    let stepsAboveBaseline = code - baselineCode;

    let thisOctave = Math.floor(code/12);
    let thisNoteName = notes[code%12];
    let thisFrequency = baselineFrequency * (semitoneRatio ** stepsAboveBaseline);

    let roundedFrequency = Math.floor(thisFrequency * 10000)/10000
    
    return {
      name: thisNoteName,
      frequency: roundedFrequency,
      octave: thisOctave
    }
}


/* playback */


// Play array of notes:


function playArrayOfNotes(arr){

  var arrCopy = arr.slice();
  playNoteFromArray(arrCopy);
}

function playNoteFromArray(arr){

  setTimeout(function(){

      // simulate a MIDI keyboard 
      
      var noteInfo = codeInfo(arr[0]);


      getMIDIMessage({data: [144, arr[0], 100]});

      //playFrequency(noteInfo.frequency, 100);     // midi code, velocity;

      setTimeout(function(){
        getMIDIMessage({data: [128, arr[0], 0]});
        //playFrequency(arr[0], 0);
      }, 300)



      arr.shift();

      if(arr.length > 0){
        console.log(arr.length);
        playNoteFromArray(arr);
      } else {
        console.log("We're out of notes!");
      }

  }, 500)

}
