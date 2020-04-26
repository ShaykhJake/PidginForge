import { Node } from "tiptap";
import { replaceText } from "tiptap-commands";

export default class TimeStamp extends Node {
  get name() {
    return "timestamp";
  }

  get schema() {
    return {
      // isLeaf: true,
      // content: "text*",
      inline: true,
      excludes: "_",
      group: "inline",
      attrs: {
        timehack: {}
      },
      draggable: true,

      toDOM: node => [
        "a",
        {
          href: "#",
          class: "timestamp",
          timehack: node.attrs.timehack,
          style:
            "text-decoration: none; margin-left: 2px; margin-right: 2px; border-style: dotted; border-width: 1px; border-radius: 3px; font-style: italic; color:firebrick; background-color: oldlace;"
        },
        ` ${node.attrs.timehack}s `
      ]
    };
  }

  commands({ schema }) {
    return attrs => replaceText(null, schema.nodes[this.name], attrs);
  }
  onClick() {
    console.log(true);
  }
}
