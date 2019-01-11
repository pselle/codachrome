let audioCtx, osc, gainNode;

// midi stuff


if (navigator.requestMIDIAccess) {
    console.log('This browser supports WebMIDI!');

} else {
    console.log('WebMIDI is not supported in this browser.');
}

enableButtonExplanation();

navigator.requestMIDIAccess()
    .then(onMIDISuccess, onMIDIFailure);

octave = 4;

let keysDown = {
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

let userInputNotes = [];

// initialize function that runs on user-init launch

function initAudio(){
  // for legacy browsers
  console.log('init!')
  const AudioContext = window.AudioContext || window.webkitAudioContext;


  // create a new audio context
  audioCtx = new AudioContext();

  // Try making an oscillator
  osc = audioCtx.createOscillator();
  gainNode = audioCtx.createGain();
  osc.type = 'sawtooth';
  osc.start();


  // connect the oscillator to gain node, and the gain node to the audio context
  osc.connect(gainNode);
  gainNode.connect(audioCtx.destination);
  gainNode.gain.value = 0; // start silently

  // enable key listeners
  console.log('a')
  enableKeyboardKeys();
  enableRequestButton();
}

function enableKeyboardKeys(){

    console.log("enabling!");

    // translate keyboard key code to midi pitch code
    let keyboardPitchCodes = {
      "65": 60,
      "83": 62,
      "68": 64,
      "70": 65,
      "71": 67,
      "72": 69,
      "74": 71,
      "75": 72,

      "87": 61,
      "69": 63,
      "84": 66,
      "89": 68,
      "85": 70
    }

    document.querySelector("body").addEventListener("keydown", function(e){

      let keyboardCode = e.keyCode;
      let pitchCode = keyboardPitchCodes[keyboardCode];
      let noteInfo = codeInfo(pitchCode);
      
      // ensure that our keydown doesn't keep triggering the same note again and again
      if(typeof(pitchCode) != "undefined" && !keysDown[noteInfo.name].playing){
          getMIDIMessage({data: [144, pitchCode, 100]});
      }
    });

    document.querySelector("body").addEventListener("keyup", function(e){
      let keyboardCode = e.keyCode;
      let pitchCode = keyboardPitchCodes[keyboardCode];
      if(typeof(pitchCode) != "undefined"){
          getMIDIMessage({data: [128, pitchCode, 0]});
      }
    });
}

function enableRequestButton(){
    document.querySelector("#run").addEventListener("click", function(e){
        console.log("running!");
        console.log(userInputNotes);

        if(userInputNotes.length){
          fetch(
            '/nextnote', {
              method: "POST",
              headers: {
                'Content-Type':'application/json'
              },
              body: JSON.stringify(userInputNotes)
            })
            .then(function(response) {
              return response.json();
            }).then(function(data) {
              playArrayOfNotes(data.nextNotes);
            });
        }
    });
}



function playFrequency(freq, velocity){

  // set the pitch
  osc.frequency.setValueAtTime(freq, audioCtx.currentTime);

  gainNode.gain.value = 0;

  if(velocity > 0){
    gainNode.gain.value = 1;
    console.log(velocity);

  }

}
function notesBeingPlayed(){

  let notesPressed = 0;

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

  for (let input of midiAccess.inputs.values())
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
    console.log(noteInfo);
    // console.log(onOffCode + ", " + noteInfo.name);
    keysDown[noteInfo.name] = (onOffCode == 144) ? true : false;


    if(typeof(pitchCode) != "undefined" &&  onOffCode == 144){
      userInputNotes.push(pitchCode);
    }

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

  let arrCopy = arr.slice();
  playNoteFromArray(arrCopy);
}


function playNotes(array) {
  return playNotes(arr.slice(arr.length-1));
}

function playNoteFromArray(arr){
  console.log('called with', arr)

  setTimeout(function(){
      // simulate a MIDI keyboard
      const firstItem = arr[0];

      getMIDIMessage({data: [144, firstItem, 100]});

      // stop playing the note after 300ms
      setTimeout(function(){
        getMIDIMessage({data: [128, firstItem, 0]});
      }, 300)

      if(arr.length > 0){
        console.log(arr)
        const newArray = arr.slice(1);
        console.log(newArray);
        return playNoteFromArray(newArray);
      } else {
        console.log("We're out of notes!");
      }

  }, 500)
}



document.getElementById('get-goin').addEventListener('click', function() {
  document.getElementById('user-action-modal').style.display = "none";
  initAudio();

  document.getElementById('run').style.display = "block";
});


/* */




function enableButtonExplanation(){

  console.log("enabling");
  document.getElementById('why-the-button-tho').addEventListener('click', function() {
    
    let modal = document.getElementById('chrome-autoplay-discoveries');
    console.log(modal.style.display);
    modal.style.display = (modal.style.display == "block") ? "none" : "block";

  })
}
