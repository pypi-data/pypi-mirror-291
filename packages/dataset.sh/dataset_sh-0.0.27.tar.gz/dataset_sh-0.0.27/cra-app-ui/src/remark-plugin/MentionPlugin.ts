import {findAndReplace} from "mdast-util-find-and-replace";
import {PhrasingContent} from "remark-mentions/lib";

const userGroup = "[a-zA-Z][a-zA-Z0-9_\\-]*\\/[a-zA-Z][a-zA-Z0-9_\\-]*";
const mentionRegex = new RegExp(
    "(?:^|\\s)@(" + userGroup + ")",
    "gi"
);

export function extractMentions(document: string) {
    const mentionRegex = /@([a-zA-Z][a-zA-Z0-9_\-]*)\/([a-zA-Z][a-zA-Z0-9_\-]*)/g;

    const mentions = document.match(mentionRegex);

    if (mentions) {
        return mentions.map(mention => mention.slice(1));
    } else {
        return []
    }
}

export function remarkMentions(
    opts = {usernameLink: (username: string) => `/${username}`}
) {
    // @ts-ignore
    return (tree, _file) => {
        findAndReplace(tree, [[mentionRegex, replaceMention as any]]);
    };


    function replaceMention(value: string, username: string): PhrasingContent[] {
        let whitespace = [];

        // Separate leading white space
        if (value.indexOf("@") > 0) {
            whitespace.push({
                type: "text",
                value: value.substring(0, value.indexOf("@")),
            });
        }

        return [
            // @ts-ignore
            ...whitespace,
            {
                // @ts-ignore
                type: "link",
                url: opts.usernameLink(username),
                // @ts-ignore
                children: [
                    {type: "strong", children: [{type: "text", value: value.trim()}]}, // Trim the username here
                ],
            },
        ];
    }
}