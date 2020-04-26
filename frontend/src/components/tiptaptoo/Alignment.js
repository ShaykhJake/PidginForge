import { Node } from "tiptap";
import { wrapIn } from "prosemirror-commands";
import { findParentNode, findSelectedNodeOfType } from "prosemirror-utils";

export default class Alignment extends Node {
  get name() {
    return "alignment";
  }

  get defaultOptions() {
    return {
      orientations: ["left", "center", "right"]
    };
  }

  get schema() {
    return {
      attrs: {
        orientation: {
          default: "left"
        }
      },
      content: "block*",
      group: "block",
      defining: true,
      draggable: false,
      toDOM: node => [
        "div",
        { style: `text-align:${node.attrs.orientation};` },
        0
      ]
    };
  }

  commands({ type }) {
    return attrs => {
      return (state, dispatch, view) => {
        const predicate = node => node.type === type;
        const node =
          findSelectedNodeOfType(type)(state.selection) ||
          findParentNode(predicate)(state.selection);

        if (!Object.keys(attrs).length || !node) {
          return wrapIn(type, attrs)(state, dispatch, view);
        } else if (node.node.attrs.orientation !== attrs.orientation) {
          view.dispatch(view.state.tr.setNodeMarkup(node.pos, null, attrs));
        }
        return true;
      };
    };
  }
}
