(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-4b646bea"],{"4a2d":function(t,i,e){"use strict";e.r(i);var s=function(){var t=this,i=t.$createElement,e=t._self._c||i;return e("v-card",{attrs:{align:"center"}},[e("v-card-text",{staticClass:"py-1"},[e("v-btn",{staticClass:"ma-1",attrs:{outlined:"",icon:""},on:{click:function(i){return t.stepPosition(-2)},keyup:function(i){return!i.type.indexOf("key")&&t._k(i.keyCode,"space",32,i.key,[" ","Spacebar"])?null:t.stepPosition(-2)}}},[e("v-icon",[t._v("mdi-undo")])],1),e("v-btn",{staticClass:"ma-1",attrs:{outlined:"",icon:"",color:t.color,disabled:!t.loaded},nativeOn:{click:function(i){return t.stop()}}},[e("v-icon",[t._v("mdi-stop")])],1),e("v-btn",{staticClass:"ma-1",attrs:{outlined:"",icon:"",color:t.color,disabled:!t.loaded},nativeOn:{click:function(i){t.playing?t.pause():t.play()}}},[t.paused||!t.loaded?e("v-icon",[t._v("mdi-play")]):e("v-icon",[t._v("mdi-pause")])],1),t.loaded?t._e():e("v-btn",{staticClass:"ma-1",attrs:{outlined:"",icon:"",color:t.color},nativeOn:{click:function(i){t.loaded?t.download():t.reload()}}},[e("v-icon",[t._v("mdi-refresh")])],1),t.loaded&&t.downloadable?e("v-btn",{staticClass:"ma-1",attrs:{outlined:"",icon:"",color:t.color},nativeOn:{click:function(i){t.loaded?t.download():t.reload()}}},[e("v-icon",[t._v("mdi-download")])],1):t._e(),e("v-btn",{staticClass:"ma-1",attrs:{outlined:"",icon:""},on:{click:function(i){return t.stepPosition(2)}}},[e("v-icon",[t._v("mdi-redo")])],1),e("p",{staticClass:"title py-0 my-0"},[t._v(t._s(t.currentTime)+" / "+t._s(t.duration))]),e("v-slider",{staticClass:"mb-0 pb-0",attrs:{color:t.color,step:"0.2","thumb-label":"",min:t.min,max:t.totalDuration,disabled:!t.loaded,height:"1",dense:""},on:{click:t.setPosition},model:{value:t.slideTime,callback:function(i){t.slideTime=i},expression:"slideTime"}}),e("v-btn",{staticClass:"ma-1",attrs:{outlined:"",icon:"",color:t.color,disabled:!t.loaded,hidden:""},nativeOn:{click:function(i){return t.mute()}}},[t.isMuted?e("v-icon",[t._v("mdi-volume-mute")]):e("v-icon",[t._v("mdi-volume-high")])],1)],1),e("audio",{key:t.playerKey,ref:"player",attrs:{id:"player",src:t.file,hidden:""},on:{ended:t.ended,canplay:t.canPlay}})],1)},a=[],n=function(t){return new Date(1e3*t).toISOString().substr(11,8)},l={name:"AudioPlayerComponent",props:{file:{type:[String,File],default:null},autoPlay:{type:Boolean,default:!1},ended:{type:Function,default:function(){}},canPlay:{type:Function,default:function(){}},color:{type:String,default:null},downloadable:{type:Boolean,default:!1}},computed:{duration:function(){return this.audio?n(this.totalDuration):""}},data:function(){return{alive:!0,audioKey:0,playerKey:0,firstPlay:!0,isMuted:!1,loaded:!1,playing:!1,paused:!0,percentage:0,currentTime:"00:00:00",audio:{},totalDuration:0,min:0,max:100,slideTime:0}},methods:{resumePlay:function(){this.setPosition(),this.play()},slidePosition:function(){this.audio.currentTime=parseInt(this.slideTime),this.play()},stepPosition:function(t){this.audio.currentTime=this.audio.currentTime+t},setPosition:function(){this.audio.currentTime=parseInt(this.slideTime)},stop:function(){this.audio.pause(),this.paused=!0,this.playing=!1,this.audio.currentTime=0},togglePlay:function(){this.playing?(this.pause(),this.playing=!1):this.play()},skipToTime:function(t){this.audio.currentTime=t},skipSeek:function(t){this.audio.currentTime=this.audio.currentTime+t},triggerTimeStamp:function(){this.$emit("recordTimeStamp",this.audio.currentTime)},play:function(){var t=this;this.playing||(this.audio.play().then((function(){t.playing=!0})),this.paused=!1)},pause:function(){this.paused=!this.paused,this.paused?this.audio.pause():this.audio.play()},download:function(){this.audio.pause(),window.open(this.file,"download")},mute:function(){this.isMuted=!this.isMuted,this.audio.muted=this.isMuted,this.volumeValue=this.isMuted?0:75},reload:function(){this.audio.load()},_handleLoaded:function(){var t=this;if(!(this.audio.readyState>=2))throw new Error("Failed to load sound file");this.audio.duration===1/0?(this.audio.currentTime=1e101,this.audio.ontimeupdate=function(){t.audio.ontimeupdate=function(){},t.audio.currentTime=0,t.totalDuration=parseInt(t.audio.duration),t.loaded=!0}):(this.totalDuration=parseInt(this.audio.duration),this.$emit("passDuration",this.totalDuration),this.loaded=!0),this.autoPlay&&this.audio.play()},_handlePlayingUI:function(){this.percentage=this.audio.currentTime/this.audio.duration*100,this.slideTime=this.audio.currentTime,this.currentTime=n(this.audio.currentTime),this.playing=!0},_handlePlayPause:function(t){"play"===t.type&&this.firstPlay&&(this.audio.currentTime=0,this.firstPlay&&(this.firstPlay=!1)),"pause"===t.type&&!1===this.paused&&!1===this.playing&&(this.currentTime="00:00:00")},_handleEnded:function(){this.paused=this.playing=!1},init:function(){this.audio.addEventListener("timeupdate",this._handlePlayingUI),this.audio.addEventListener("loadeddata",this._handleLoaded)},emitTimeStamp:function(){this.$emit("recordTimeStamp",this.audio.currentTime)}},mounted:function(){this.audio=this.$refs.player,this.init()},beforeDestroy:function(){this.audio.removeEventListener("timeupdate",this._handlePlayingUI),this.audio.removeEventListener("loadeddata",this._handleLoaded),this.audio.removeEventListener("pause",this._handlePlayPause),this.audio.removeEventListener("play",this._handlePlayPause),this.audio.removeEventListener("ended",this._handleEnded)}},o=l,r=e("2877"),u=e("6544"),h=e.n(u),d=e("8336"),c=e("b0af"),m=e("99d9"),p=e("132d"),v=(e("9e29"),e("c37a")),b=e("0789"),y=e("58df"),f=e("297c"),k=e("a293"),g=e("80d2"),C=e("d9bd"),T=Object(y["a"])(v["a"],f["a"]).extend({name:"v-slider",directives:{ClickOutside:k["a"]},mixins:[f["a"]],props:{disabled:Boolean,inverseLabel:Boolean,max:{type:[Number,String],default:100},min:{type:[Number,String],default:0},step:{type:[Number,String],default:1},thumbColor:String,thumbLabel:{type:[Boolean,String],default:void 0,validator:t=>"boolean"===typeof t||"always"===t},thumbSize:{type:[Number,String],default:32},tickLabels:{type:Array,default:()=>[]},ticks:{type:[Boolean,String],default:!1,validator:t=>"boolean"===typeof t||"always"===t},tickSize:{type:[Number,String],default:2},trackColor:String,trackFillColor:String,value:[Number,String],vertical:Boolean},data:()=>({app:null,oldValue:null,keyPressed:0,isFocused:!1,isActive:!1,noClick:!1}),computed:{classes(){return{...v["a"].options.computed.classes.call(this),"v-input__slider":!0,"v-input__slider--vertical":this.vertical,"v-input__slider--inverse-label":this.inverseLabel}},internalValue:{get(){return this.lazyValue},set(t){t=isNaN(t)?this.minValue:t;const i=this.roundValue(Math.min(Math.max(t,this.minValue),this.maxValue));i!==this.lazyValue&&(this.lazyValue=i,this.$emit("input",i))}},trackTransition(){return this.keyPressed>=2?"none":""},minValue(){return parseFloat(this.min)},maxValue(){return parseFloat(this.max)},stepNumeric(){return this.step>0?parseFloat(this.step):0},inputWidth(){const t=(this.roundValue(this.internalValue)-this.minValue)/(this.maxValue-this.minValue)*100;return t},trackFillStyles(){const t=this.vertical?"bottom":"left",i=this.vertical?"top":"right",e=this.vertical?"height":"width",s=this.$vuetify.rtl?"auto":"0",a=this.$vuetify.rtl?"0":"auto",n=this.disabled?`calc(${this.inputWidth}% - 10px)`:`${this.inputWidth}%`;return{transition:this.trackTransition,[t]:s,[i]:a,[e]:n}},trackStyles(){const t=this.vertical?this.$vuetify.rtl?"bottom":"top":this.$vuetify.rtl?"left":"right",i=this.vertical?"height":"width",e="0px",s=this.disabled?`calc(${100-this.inputWidth}% - 10px)`:`calc(${100-this.inputWidth}%)`;return{transition:this.trackTransition,[t]:e,[i]:s}},showTicks(){return this.tickLabels.length>0||!(this.disabled||!this.stepNumeric||!this.ticks)},numTicks(){return Math.ceil((this.maxValue-this.minValue)/this.stepNumeric)},showThumbLabel(){return!this.disabled&&!(!this.thumbLabel&&!this.$scopedSlots["thumb-label"])},computedTrackColor(){if(!this.disabled)return this.trackColor?this.trackColor:this.isDark?this.validationState:this.validationState||"primary lighten-3"},computedTrackFillColor(){if(!this.disabled)return this.trackFillColor?this.trackFillColor:this.validationState||this.computedColor},computedThumbColor(){return this.thumbColor?this.thumbColor:this.validationState||this.computedColor}},watch:{min(t){const i=parseFloat(t);i>this.internalValue&&this.$emit("input",i)},max(t){const i=parseFloat(t);i<this.internalValue&&this.$emit("input",i)},value:{handler(t){this.internalValue=t}}},beforeMount(){this.internalValue=this.value},mounted(){this.app=document.querySelector("[data-app]")||Object(C["c"])("Missing v-app or a non-body wrapping element with the [data-app] attribute",this)},methods:{genDefaultSlot(){const t=[this.genLabel()],i=this.genSlider();return this.inverseLabel?t.unshift(i):t.push(i),t.push(this.genProgress()),t},genSlider(){return this.$createElement("div",{class:{"v-slider":!0,"v-slider--horizontal":!this.vertical,"v-slider--vertical":this.vertical,"v-slider--focused":this.isFocused,"v-slider--active":this.isActive,"v-slider--disabled":this.disabled,"v-slider--readonly":this.readonly,...this.themeClasses},directives:[{name:"click-outside",value:this.onBlur}],on:{click:this.onSliderClick}},this.genChildren())},genChildren(){return[this.genInput(),this.genTrackContainer(),this.genSteps(),this.genThumbContainer(this.internalValue,this.inputWidth,this.isActive,this.isFocused,this.onThumbMouseDown,this.onFocus,this.onBlur)]},genInput(){return this.$createElement("input",{attrs:{value:this.internalValue,id:this.computedId,disabled:this.disabled,readonly:!0,tabindex:-1,...this.$attrs}})},genTrackContainer(){const t=[this.$createElement("div",this.setBackgroundColor(this.computedTrackColor,{staticClass:"v-slider__track-background",style:this.trackStyles})),this.$createElement("div",this.setBackgroundColor(this.computedTrackFillColor,{staticClass:"v-slider__track-fill",style:this.trackFillStyles}))];return this.$createElement("div",{staticClass:"v-slider__track-container",ref:"track"},t)},genSteps(){if(!this.step||!this.showTicks)return null;const t=parseFloat(this.tickSize),i=Object(g["g"])(this.numTicks+1),e=this.vertical?"bottom":"left",s=this.vertical?"right":"top";this.vertical&&i.reverse();const a=i.map(i=>{const a=this.$vuetify.rtl?this.maxValue-i:i,n=[];this.tickLabels[a]&&n.push(this.$createElement("div",{staticClass:"v-slider__tick-label"},this.tickLabels[a]));const l=i*(100/this.numTicks),o=this.$vuetify.rtl?100-this.inputWidth<l:l<this.inputWidth;return this.$createElement("span",{key:i,staticClass:"v-slider__tick",class:{"v-slider__tick--filled":o},style:{width:`${t}px`,height:`${t}px`,[e]:`calc(${l}% - ${t/2}px)`,[s]:`calc(50% - ${t/2}px)`}},n)});return this.$createElement("div",{staticClass:"v-slider__ticks-container",class:{"v-slider__ticks-container--always-show":"always"===this.ticks||this.tickLabels.length>0}},a)},genThumbContainer(t,i,e,s,a,n,l,o="thumb"){const r=[this.genThumb()],u=this.genThumbLabelContent(t);return this.showThumbLabel&&r.push(this.genThumbLabel(u)),this.$createElement("div",this.setTextColor(this.computedThumbColor,{ref:o,staticClass:"v-slider__thumb-container",class:{"v-slider__thumb-container--active":e,"v-slider__thumb-container--focused":s,"v-slider__thumb-container--show-label":this.showThumbLabel},style:this.getThumbContainerStyles(i),attrs:{role:"slider",tabindex:this.disabled||this.readonly?-1:this.$attrs.tabindex?this.$attrs.tabindex:0,"aria-label":this.label,"aria-valuemin":this.min,"aria-valuemax":this.max,"aria-valuenow":this.internalValue,"aria-readonly":String(this.readonly),"aria-orientation":this.vertical?"vertical":"horizontal",...this.$attrs},on:{focus:n,blur:l,keydown:this.onKeyDown,keyup:this.onKeyUp,touchstart:a,mousedown:a}}),r)},genThumbLabelContent(t){return this.$scopedSlots["thumb-label"]?this.$scopedSlots["thumb-label"]({value:t}):[this.$createElement("span",[String(t)])]},genThumbLabel(t){const i=Object(g["f"])(this.thumbSize),e=this.vertical?`translateY(20%) translateY(${Number(this.thumbSize)/3-1}px) translateX(55%) rotate(135deg)`:"translateY(-20%) translateY(-12px) translateX(-50%) rotate(45deg)";return this.$createElement(b["e"],{props:{origin:"bottom center"}},[this.$createElement("div",{staticClass:"v-slider__thumb-label-container",directives:[{name:"show",value:this.isFocused||this.isActive||"always"===this.thumbLabel}]},[this.$createElement("div",this.setBackgroundColor(this.computedThumbColor,{staticClass:"v-slider__thumb-label",style:{height:i,width:i,transform:e}}),[this.$createElement("div",t)])])])},genThumb(){return this.$createElement("div",this.setBackgroundColor(this.computedThumbColor,{staticClass:"v-slider__thumb"}))},getThumbContainerStyles(t){const i=this.vertical?"top":"left";let e=this.$vuetify.rtl?100-t:t;return e=this.vertical?100-e:e,{transition:this.trackTransition,[i]:`${e}%`}},onThumbMouseDown(t){t.preventDefault(),this.oldValue=this.internalValue,this.keyPressed=2,this.isActive=!0;const i=!g["w"]||{passive:!0,capture:!0},e=!!g["w"]&&{passive:!0};"touches"in t?(this.app.addEventListener("touchmove",this.onMouseMove,e),Object(g["a"])(this.app,"touchend",this.onSliderMouseUp,i)):(this.app.addEventListener("mousemove",this.onMouseMove,e),Object(g["a"])(this.app,"mouseup",this.onSliderMouseUp,i)),this.$emit("start",this.internalValue)},onSliderMouseUp(t){t.stopPropagation(),this.keyPressed=0;const i=!!g["w"]&&{passive:!0};this.app.removeEventListener("touchmove",this.onMouseMove,i),this.app.removeEventListener("mousemove",this.onMouseMove,i),this.$emit("end",this.internalValue),Object(g["i"])(this.oldValue,this.internalValue)||(this.$emit("change",this.internalValue),this.noClick=!0),this.isActive=!1},onMouseMove(t){const{value:i}=this.parseMouseMove(t);this.internalValue=i},onKeyDown(t){if(this.disabled||this.readonly)return;const i=this.parseKeyDown(t,this.internalValue);null!=i&&(this.internalValue=i,this.$emit("change",i))},onKeyUp(){this.keyPressed=0},onSliderClick(t){if(this.noClick)return void(this.noClick=!1);const i=this.$refs.thumb;i.focus(),this.onMouseMove(t),this.$emit("change",this.internalValue)},onBlur(t){this.isFocused=!1,this.$emit("blur",t)},onFocus(t){this.isFocused=!0,this.$emit("focus",t)},parseMouseMove(t){const i=this.vertical?"top":"left",e=this.vertical?"height":"width",s=this.vertical?"clientY":"clientX",{[i]:a,[e]:n}=this.$refs.track.getBoundingClientRect(),l="touches"in t?t.touches[0][s]:t[s];let o=Math.min(Math.max((l-a)/n,0),1)||0;this.vertical&&(o=1-o),this.$vuetify.rtl&&(o=1-o);const r=l>=a&&l<=a+n,u=parseFloat(this.min)+o*(this.maxValue-this.minValue);return{value:u,isInsideTrack:r}},parseKeyDown(t,i){if(this.disabled)return;const{pageup:e,pagedown:s,end:a,home:n,left:l,right:o,down:r,up:u}=g["s"];if(![e,s,a,n,l,o,r,u].includes(t.keyCode))return;t.preventDefault();const h=this.stepNumeric||1,d=(this.maxValue-this.minValue)/h;if([l,o,r,u].includes(t.keyCode)){this.keyPressed+=1;const e=this.$vuetify.rtl?[l,u]:[o,u],s=e.includes(t.keyCode)?1:-1,a=t.shiftKey?3:t.ctrlKey?2:1;i+=s*h*a}else if(t.keyCode===n)i=this.minValue;else if(t.keyCode===a)i=this.maxValue;else{const e=t.keyCode===s?1:-1;i-=e*h*(d>100?d/10:10)}return i},roundValue(t){if(!this.stepNumeric)return t;const i=this.step.toString().trim(),e=i.indexOf(".")>-1?i.length-i.indexOf(".")-1:0,s=this.minValue%this.stepNumeric,a=Math.round((t-s)/this.stepNumeric)*this.stepNumeric+s;return parseFloat(Math.min(a,this.maxValue).toFixed(e))}}}),_=Object(r["a"])(o,s,a,!1,null,null,null);i["default"]=_.exports;h()(_,{VBtn:d["a"],VCard:c["a"],VCardText:m["b"],VIcon:p["a"],VSlider:T})},"9e29":function(t,i,e){}}]);
//# sourceMappingURL=chunk-4b646bea.516d3838.js.map