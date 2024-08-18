import {useQuery} from "@tanstack/react-query";
import {Features} from "../../../features";
import {AnchorTitle, extractTitleValue} from "../../posts/PostViewer";
import {CodeBlock} from "../../CodeBlock";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import {remarkMentions} from "../../../remark-plugin/MentionPlugin";
import rehypeRaw from "rehype-raw";
import React from "react";

export function ReadmeViewer({namespace, datasetName, readmeContent}: {
    namespace: string, datasetName: string, readmeContent: string
}) {

    const renderers = {
        code(props: any) {
            const {children, className, node, inline, ...rest} = props
            const title = node?.data?.meta && extractTitleValue(node?.data?.meta)
            const match = /language-(\w+)/.exec(className || '')
            const language = (match && match[1]) || 'text'
            if (inline) {
                return <code>{children}</code>
            }
            return <CodeBlock
                title={title}
                language={language}
                code={children}/>
        },
        h2: AnchorTitle,
        h3: AnchorTitle,
    }

    return <div className={'pt-8 pb-24 p-4 border-orange-100 border-8 rounded-lg '}>
        <a
            className={"text-2xl font-bold underline text-teal-600"}
            id={'readme'}
            href={'#readme'}
        >
            About this dataset
        </a>

        <div className={'my-2'}>
            <div className={'my-2'}>
                <ReactMarkdown
                    remarkPlugins={[remarkGfm, [remarkMentions as any, {
                        usernameLink: (name: string) => `/dataset/${name}`,
                    }]]}
                    rehypePlugins={[rehypeRaw] as any}
                    components={renderers}
                    className={'markdown-body'}
                    children={readmeContent || 'Readme not found.'}
                />
            </div>
        </div>
    </div>
}

