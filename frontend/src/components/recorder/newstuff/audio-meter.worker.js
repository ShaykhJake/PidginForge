class MyWorkletProcessor extends AudioWorkletProcessor {
   constructor() {
       console.log('Constructing myworkletprocessor');
       super();
   }

   process(inputs, outputs, parameters) {
       console.log(`current time: ${currentTime}`);
       // True to keep running
       return true;
   }
}

console.log('Registering processor');
registerProcessor('audio-meter', MyWorkletProcessor);
