import { Node } from "tiptap";
import { wrapIn } from "prosemirror-commands";
// import { setBlockType } from 'tiptap-commands'
import { findParentNode, findSelectedNodeOfType } from "prosemirror-utils";

export default class TextDirection extends Node {
  get name() {
    return "text_direction";
  }

  get defaultOptions() {
    return {
      directions: ["ltr", "rtl"]
    };
  }

  get schema() {
    return {
      attrs: {
        direction: {
          default: "ltr"
        }
      },
      content: "block*",
      group: "block",
      defining: true,
      draggable: false,
      toDOM: node => ["p", { style: `direction: ${node.attrs.direction};` }, 0]
    };
  }

  // commands({ type, schema }) {
  //   return () => toggleBlockType(type, schema.nodes.paragraph)
  // }

  commands({ type }) {
    return attrs => {
      return (state, dispatch, view) => {
        const predicate = node => node.type === type;
        const node =
          findSelectedNodeOfType(type)(state.selection) ||
          findParentNode(predicate)(state.selection);

        if (!Object.keys(attrs).length || !node) {
          return wrapIn(type, attrs)(state, dispatch, view);
        } else if (node.node.attrs.direction !== attrs.direction) {
          view.dispatch(view.state.tr.setNodeMarkup(node.pos, null, attrs));
        }
        return true;
      };
    };
  }
}
