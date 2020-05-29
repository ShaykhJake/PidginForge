// This is the way it should work, but gives an exception:
/*
DOMException: The user aborted a request.
audio-meter.js:13 Uncaught (in promise) DOMException: Failed to construct 'AudioWorkletNode': AudioWorkletNode cannot be created: The node name 'audio-meter' is not defined in AudioWorkletGlobalScope.
    at new AudioMeterNode (http://localhost:9999/bundle.js:9415:17)
    at Function.create (http://localhost:9999/bundle.js:9424:16)
 */
// import workletUrl from './audio-meter.worker.js';

// If you uncoment the line below this and comment the previous import, it works
const workletUrl = 'audio-meter.worker.js';

export class AudioMeterNodeFactory {

    static async create(context) {

        class AudioMeterNode extends AudioWorkletNode {
            constructor(context) {
                super(context, 'audio-meter');
            }
        }

        try {
            await context.audioWorklet.addModule(workletUrl);
        } catch(e) {
            console.log(e);
        }
        return new AudioMeterNode(context);
    }

}
