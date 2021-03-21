import { Mark, Plugin } from "tiptap";
import { updateMark, removeMark, pasteRule } from "tiptap-commands";
import { getMarkAttrs } from "tiptap-utils";

export default class Lexeme extends Mark {
  get name() {
    return "lexeme";
  }

  get defaultOptions() {
    return {
      openOnClick: true
    };
  }

  get schema() {
    return {
      attrs: {
        href: {
          default: "#"
        },
        translation: {
          default: null
        }
      },
      inclusive: false,
      parseDOM: [
        {
          tag: "a[translation]",
          getAttrs: dom => ({
            translation: dom.getAttribute("translation")
          })
        }
      ],
      toDOM: node => [
        "a",
        {
          ...node.attrs,
          class: "lexeme",
          title: node.attrs.translation,
          style: "color: darkorange; font-weight: bold; text-decoration: none;",
          rel: "noopener noreferrer nofollow"
        },
        0
      ]
    };
  }

  commands({ type }) {
    return attrs => {
      if (attrs.translation) {
        return updateMark(type, attrs);
      }
      return removeMark(type);
    };
  }

  pasteRules({ type }) {
    return [
      pasteRule(
        /https?:\/\/(www\.)?[-a-zA-Z0-9@:%._+~#=]{2,256}\.[a-zA-Z]{2,}\b([-a-zA-Z0-9@:%_+.~#?&//=]*)/g,
        type,
        url => ({ href: url })
      )
    ];
  }

  get plugins() {
    if (!this.options.openOnClick) {
      return [];
    }

    return [
      new Plugin({
        props: {
          handleClick: (view, pos, event) => {
            const { schema } = view.state;
            const attrs = getMarkAttrs(view.state, schema.marks.lexeme);

            if (attrs.href && event.target instanceof HTMLAnchorElement) {
              event.stopPropagation();
              window.open(attrs.href);
            }
          }
        }
      })
    ];
  }
}
