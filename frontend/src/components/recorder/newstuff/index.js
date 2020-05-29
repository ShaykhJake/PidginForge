import {AudioMeterNodeFactory} from "./audio-meter.js";

let audioContext;

document.querySelector('button').addEventListener('click', function() {

    if(!audioContext) {
        audioContext = new AudioContext();
        startVolumeAnalyzer(audioContext).then(()=>console.log('Volume analyzer started'));
        return;
    }

    if(audioContext.state === 'running') {
        console.log('suspending');
        audioContext.suspend().then(function() {
            // Audio suspended
        });
    } else if(audioContext.state === 'suspended') {
        console.log('resuming');
        audioContext.resume().then(function() {
            // Audio resumed
        });
    }
});

async function startVolumeAnalyzer(audioContext) {

    let mikeStream = await openMike();
    let mikeNode = audioContext.createMediaStreamSource(mikeStream);

    let meterNode = await AudioMeterNodeFactory.create(audioContext);
    mikeNode.connect(meterNode);

    // If it isn't connected to destination, the worklet is not executed
    meterNode.connect(audioContext.destination);
}

async function openMike() {

    try {
        let stream = await navigator.mediaDevices.getUserMedia(
            {
                "audio": {
                    "mandatory": {
                        "googEchoCancellation": "false",
                        "googAutoGainControl": "false",
                        "googNoiseSuppression": "false",
                        "googHighpassFilter": "false"
                    },
                    "optional": []
                },
            });
        return stream;
    } catch (e) {
        alert('getUserMedia threw exception :' + e);
    }
}



