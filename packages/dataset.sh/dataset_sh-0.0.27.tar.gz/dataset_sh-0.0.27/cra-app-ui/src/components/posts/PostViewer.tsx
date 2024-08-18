import React from "react";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";
import ReactMarkdown from "react-markdown";
import {CodeBlock, LightCodeBlock} from "../CodeBlock";
import {Link as RouterLink} from "react-router-dom";
import {extractMentions, remarkMentions} from "../../remark-plugin/MentionPlugin";
import {Disclosure} from '@headlessui/react'
import {ArchiveBoxArrowDownIcon, ChevronRightIcon} from '@heroicons/react/24/outline'
import _ from 'lodash'
import {rehypeInlineCodeProperty} from "../../remark-plugin/InlineCode";


export function extractTitleValue(inputString: string) {
    // Regular expression to match the title attribute
    const regex = /title="([^"]+)"/;

    // Use the match method to find the match in the inputString
    const match = inputString.match(regex);

    // Check if a match was found
    if (match) {
        // The value of the title attribute is in the first capture group (index 1)
        return match[1];
    } else {
        // Return null if no match was found
        return null;
    }
}


type DatasetDependencyItem = {
    source: string
    target?: string
}

type DatasetDependencyHostGroup = {
    host: string
    datasets: DatasetDependencyItem[]
}

type DatasetDependencies = {
    dependencies: DatasetDependencyHostGroup[]
}

function MentionOverview({mentions, projectName, hostName}: {
    mentions: string[],
    projectName: string,
    hostName: string
}) {

    const code = React.useMemo(() => {
        const dep: DatasetDependencies = {
            dependencies: [
                {
                    host: hostName,
                    datasets: mentions.map(x => {
                        return {
                            source: x
                        }
                    })
                }
            ]
        }
        return JSON.stringify(dep, null, 4)
    }, [mentions])

    const downloadFile = () => {
        const blob = new Blob([code], {type: 'text/plain'});
        const url = URL.createObjectURL(blob);
        const anchor = document.createElement('a');
        anchor.href = url;
        anchor.download = `${projectName}.dataset-sh-project`;
        document.body.appendChild(anchor);
        anchor.click();

        document.body.removeChild(anchor);
        URL.revokeObjectURL(url);
    };


    // @ts-ignore
    return <div>
        <Disclosure>
            {({open}) => (
                /* Use the `open` state to conditionally change the direction of an icon. */
                <>
                    <Disclosure.Button
                        className="px-4 py-2 border-2 border-b-4 border-red-300 bg-gradient-to-r from-rose-400 via-fuchsia-500 to-indigo-500 inline-flex flex-row items-center text-transparent bg-clip-text rounded-md justify-between">

                        <div>
                            {!open ? <>
                                {mentions.length} {mentions.length > 1 ? 'datasets' : 'dataset'} mentioned in this post.
                            </> : <>
                                Click to hide project file.
                            </>}
                        </div>

                        <div>
                            {open ? <ChevronRightIcon
                                    className="ml-2 inline h-5 w-5 text-purple-700 rotate-90 transform"/>
                                : <ArchiveBoxArrowDownIcon className={'ml-2 inline h-5 w-5 text-purple-700'}/>}

                        </div>


                    </Disclosure.Button>
                    <Disclosure.Panel className="text-gray-500">
                        <div className={'m-6'}>
                            <LightCodeBlock code={code} language={'json'} title={'dataset.sh project file.'}/>
                            <div className={'mt-2'}>
                                <button
                                    onClick={downloadFile}
                                    className="text-white bg-gradient-to-r from-cyan-500 to-blue-500 hover:bg-gradient-to-bl focus:ring-4 focus:outline-none focus:ring-cyan-300 dark:focus:ring-cyan-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2 flex-row inline-flex items-center">
                                    <svg className="fill-current w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg"
                                         viewBox="0 0 20 20">
                                        <path d="M13 8V2H7v6H2l8 8 8-8h-5zM0 18h20v2H0v-2z"/>
                                    </svg>
                                    <span>Download Project File</span>
                                </button>
                            </div>

                            <div
                                className={'markdown-body mt-2'}
                            >
                                You can use <code>dataset.sh project install path-to-the-project-file</code> to
                                install all datasets mentioned in this article.
                            </div>

                        </div>
                    </Disclosure.Panel>
                </>
            )}


        </Disclosure>
    </div>
}

export function AnchorTitle({children, ...props}: any) {
    const level = Number(props.node.tagName.match(/h(\d)/)?.slice(1));
    if (level && children && typeof children[0] === "string") {
        const id = children[0].toLowerCase().replace(/[^a-z0-9]+/g, "-");
        const headingElm = React.createElement(
            props.node.tagName, {id}, children
        )
        return <RouterLink to={`#${id}`}>{headingElm}</RouterLink>
    } else {
        return React.createElement(props.node.tagName, props, children);
    }
};

function AuthLinkTarget(props: any) {
    if (props.href.startsWith('http')) {
        return (
            <a href={props.href} target="_blank">
                {props.children}
            </a>
        )
    } else {
        return (
            <RouterLink to={props.href}>
                {props.children}
            </RouterLink>
        )
    }

}

export function PostViewer(
    {
        post,
        projectName,
        hideProject,
        hostName,
    }: {
        post: string,
        projectName: string,
        hostName: string,

        hideProject?: boolean
    }) {

    const mentions = React.useMemo(() => {
        return _.uniq(extractMentions(post))
    }, [post])

    const renderers = {
        pre(props: any) {
            console.log(props)
            const {children, className, node, inline, ...rest} = props
            const title: string = (node?.data?.meta && extractTitleValue(node?.data?.meta)) || ''
            const match = /language-(\w+)/.exec(children.props.className || '')
            const language = (match && match[1]) || 'text'

            return <div className={'mb-2'}>
                <CodeBlock
                    title={title}
                    language={language}
                    code={children.props.children}
                />
            </div>
        },
        code(props: any) {
            // console.log(props)
            const {children, className, node, inline, ...rest} = props
            const title = node?.data?.meta && extractTitleValue(node?.data?.meta)
            const match = /language-(\w+)/.exec(className || '')
            const language = (match && match[1]) || 'text'
            return <code>{children}</code>
        },
        h2: AnchorTitle,
        h3: AnchorTitle,
        a: AuthLinkTarget,
    }

    return <div>

        {
            ((!hideProject) && mentions && mentions.length > 0) &&
            <MentionOverview mentions={mentions} projectName={projectName} hostName={hostName}/>
        }

        <ReactMarkdown
            remarkPlugins={[
                remarkGfm,
                [remarkMentions as any, {
                    usernameLink: (name: string) => `/dataset/${name}`,
                }],

            ]}
            rehypePlugins={[
                rehypeRaw,
                rehypeInlineCodeProperty()
            ] as any}
            components={renderers}
            className={'markdown-body'}
            children={post || 'Post is empty'}
        />
    </div>
}

