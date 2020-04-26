import { Mark } from "tiptap";
import { toggleMark, markInputRule, markPasteRule } from "tiptap-commands";

export default class Highlighter extends Mark {
  get name() {
    return "highlighter";
  }

  get schema() {
    return {
      // parseDOM: [
      //   {
      //     tag: 'span',
      //   },
      //   {
      //     style: 'color',
      //     getAttrs: value => value === 'blue',
      //   },
      // ],
      toDOM: () => [
        "span",
        {
          style: "background-color: orange;"
        },
        `hello`
      ]
    };
  }

  keys({ type }) {
    return {
      "Mod-d": toggleMark(type)
    };
  }

  commands({ type }) {
    return () => toggleMark(type);
  }

  inputRules({ type }) {
    return [markInputRule(/~([^~]+)~$/, type)];
  }

  pasteRules({ type }) {
    return [markPasteRule(/~([^~]+)~/g, type)];
  }
}
