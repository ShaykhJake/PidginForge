import { Node } from "tiptap";
import KnowledgeCheckEmbed from "@/components/tiptaptoo/KnowledgeCheckEmbed.vue";

export default class KnowledgeCheck extends Node {
  get name() {
    return "knowledgecheck";
  }

  get schema() {
    return {
      attrs: {
        kcid: {
          default: null
        },
        kctype: {
          default: null
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
          tag: "knowledgecheck",
          getAttrs: dom => ({
            questionid: dom.getAttribute("kcid"),
            questiontype: dom.getAttribute("kctype")
          })
        }
      ],
      toDOM: node => [
        "knowledgecheck",
        {
          kcid: node.attrs.kcid,
          kctype: node.attrs.kctype
        }
      ]
    };
  }

  get view() {
    return {
      props: ["node", "updateAttrs", "view"],
      components: {
        KnowledgeCheckEmbed
      },
      computed: {
        kcid: {
          get() {
            return this.node.attrs.kcid;
          },
          set(kcid) {
            this.updateAttrs({
              kcid
            });
          }
        },
        kctype: {
          get() {
            return this.node.attrs.kctype;
          },
          set(kctype) {
            this.updateAttrs({
              kctype
            });
          }
        }
      },
      methods: {
        updateKCType(newType) {
          this.kctype = newType;
        },
        updateKCID(newID) {
          this.kcid = newID;
        }
      },
      // VueComponents seems to be working well now...need to create a completely different
      // embed component simply for the lesson
      template: `
         <div>
          <KnowledgeCheckEmbed 
            :kcid="kcid"
            :kctype="kctype"

            :editing="view.editable"
            @updateKCType="updateKCType"
            @updateKCTID="updateKCID"
          />
         </div>
         `
    };
    // the below was originally part of the above template
    //  <div v-if="view.editable">
    //     <input class="iframe__input" @paste.stop type="text" v-model="src" />
    //    </div>
  }
}
