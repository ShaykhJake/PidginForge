(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-6bd5691b"],{"5b4f":function(e,t,i){"use strict";var o=i("610a"),a=i.n(o);a.a},"610a":function(e,t,i){},c0f8:function(e,t,i){"use strict";i.r(t);var o=function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("div",[i("v-card",{staticClass:"calligraphy desertsand--text",attrs:{align:"left"}},[i("div",{ref:"ytdiv",staticClass:"responsive"},[i("youtube",{key:e.youTubePlayerKey,ref:"youtube",attrs:{"video-id":e.videoid,height:e.YTheight,width:e.YTwidth},on:{playing:e.playing,ready:function(t){e.loadingVideo=!1}}})],1)]),i("v-overlay",{attrs:{value:e.loadingVideo,absolute:"",color:"calligraphy",opacity:"0.75"}},[i("v-progress-circular",{attrs:{indeterminate:"",size:"64"}})],1)],1)},a=[],r={name:"YouTubePlayerComponent",props:{videoid:String},components:{},data:function(){return{player:{},heightText:"Start",youTubeEditorLoaded:!1,showYouTubeEditor:!1,showAudioEditor:!1,audioEditorLoaded:!1,editorDialog:!1,profileDialog:!1,elementObject:{curator:{},transcripts:{}},video:{curator:{}},max:100,youTubePlayerKey:0,next:null,flaggerDialog:!1,loadEditor:!1,loadingVideo:!1,loadingAudio:!1,fitParent:!0,YTwidth:275,YTheight:200,userHidden:!1,saving:!1,hiding:!1,voteScore:0,youTubeHeight:0}},methods:{setVideoSize:function(){var e=this.$refs.ytdiv.clientWidth;this.YTwidth=e-10,this.YTheight=.65*e},playVideo:function(){this.player.playVideo()},skipToTime:function(e){this.player.seekTo(e,!0)},skipSeek:function(e){var t=this;this.player.getCurrentTime().then((function(i){var o=i+e;t.player.seekTo(o,!0)}))},togglePlay:function(){var e=this;this.player.getPlayerState().then((function(t){1===t?e.player.pauseVideo():e.player.playVideo()}))},triggerTimeStamp:function(){var e=this;this.player.getCurrentTime().then((function(t){console.log(t),e.$emit("recordTimeStamp",t)}))},playing:function(){}},hide:function(){this.player.destroy()},mounted:function(){this.player=this.$refs.youtube.player},beforeDestroy:function(){document.removeEventListener("keydown",this._keyListener)}},n=r,s=(i("5b4f"),i("2877")),l=i("6544"),d=i.n(l),u=i("b0af"),c=i("a797"),y=i("490a"),h=Object(s["a"])(n,o,a,!1,null,null,null);t["default"]=h.exports;d()(h,{VCard:u["a"],VOverlay:c["a"],VProgressCircular:y["a"]})}}]);
//# sourceMappingURL=chunk-6bd5691b.4edd8d19.js.map