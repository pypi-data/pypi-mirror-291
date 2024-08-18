import {visit} from 'unist-util-visit'

export function rehypeInlineCodeProperty() {
    /**
     * @param {import('hast').Root} tree
     * @returns {undefined}
     */
    return function (tree: any) {
        if (tree) {
            visit(tree, 'code', function (node, index, parent) {
                if (parent && parent.tagName === 'pre') {
                    node.properties.inline = false;
                } else {
                    node.properties.inline = true;
                }
            })
        }

    }
}
