import { Node } from "tiptap";
import YouTubePlayerEmbed from "@/components/tiptaptoo/YouTubePlayerEmbed.vue";

export default class YouTubeEmbed extends Node {
  get name() {
    return "youtubeembed";
  }

  get schema() {
    return {
      attrs: {
        src: {
          default: null
        },
        float: {
          default: "right"
        }
      },
      excludes: "_",
      group: "inline",
      inline: "true",
      // group: 'block',
      selectable: true,
      draggable: true,
      parseDOM: [
        {
          tag: "iframe",
          getAttrs: dom => ({
            src: dom.getAttribute("src")
          })
        }
      ],
      toDOM: node => [
        "iframe",
        {
          src: node.attrs.src,
          style: `float: ${node.attrs.float}`,
          frameborder: 0,
          allowfullscreen: "true"
        }
      ]
    };
  }

  get view() {
    return {
      props: ["node", "updateAttrs", "view"],
      components: {
        YouTubePlayerEmbed
      },
      computed: {
        float: {
          get() {
            if (this.node.attrs.float === "none") {
              return `text-align: center; direction: ltr;`;
            } else {
              return `margin: 5px 5px 5px 5px;float: ${this.node.attrs.float};`;
            }
          },
          set(float) {
            this.updateAttrs({
              float
            });
          }
        },
        src: {
          get() {
            return this.node.attrs.src;
          },
          set(src) {
            this.updateAttrs({
              src
            });
          }
        },
        floatDirection: {
          get() {
            return this.node.attrs.float;
          }
        }
      },
      methods: {
        updateWrap(direction) {
          this.float = direction;
        }
      },
      // VueComponents seems to be working well now...need to create a completely different
      // embed component simply for the lesson
      template: `
         <div :style="float">
            <div style="text-align: left; direction: ltr">
               <YouTubePlayerEmbed
                  videoid="XIMLoLxmTDw"
                  :src="src"
                  :float="floatDirection"

                  :editing="view.editable"
                  @updateWrap="updateWrap"
               />
            </div>
         </div>
         `
    };
    // the below was originally part of the above template
    //  <div v-if="view.editable">
    //     <input class="iframe__input" @paste.stop type="text" v-model="src" />
    //    </div>
  }
}
