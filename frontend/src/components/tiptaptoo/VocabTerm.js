import { Mark } from "tiptap";
import { toggleMark, markInputRule, markPasteRule } from "tiptap-commands";

export default class VocabTerm extends Mark {
  get name() {
    return "vocabterm";
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
      excludes: '_',
      toDOM: () => [
        "span",
        {
          style:
            "border: 1px solid orange; border-radius: 5px; font-style: italic; color:orange; background-color: oldlace;"
        },
        0
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
