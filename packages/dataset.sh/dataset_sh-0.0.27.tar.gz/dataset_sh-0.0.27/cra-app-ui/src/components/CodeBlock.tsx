import React from "react";
import {Prism as SyntaxHighlighter} from 'react-syntax-highlighter';
import {coy as codeStyle} from 'react-syntax-highlighter/dist/esm/styles/prism';
import {
    CheckCircleIcon,
    ArrowsPointingInIcon,
    ChevronUpDownIcon
} from '@heroicons/react/20/solid'
import {
    ClipboardDocumentIcon,
} from '@heroicons/react/24/outline'

type CopiedValue = string | null
type CopyFn = (text: string) => Promise<boolean> // Return success

export function useCopyToClipboard(): [CopiedValue, CopyFn] {
    const [copiedText, setCopiedText] = React.useState<CopiedValue>(null)

    const copy: CopyFn = async text => {
        if (!navigator?.clipboard) {
            console.warn('Clipboard not supported')
            return false
        }

        try {
            await navigator.clipboard.writeText(text)
            setCopiedText(text)
            return true
        } catch (error) {
            console.warn('Copy failed', error)
            setCopiedText(null)
            return false
        }
    }

    return [copiedText, copy]
}

export function CodeBlock({code, title, language}: {
    code: string,
    title?: string,
    language: string
}) {
    const [copiedValue, copy] = useCopyToClipboard()
    const [copiedGuard, setCopiedGuard] = React.useState(false);
    const [enableFixLength, setEnableFixLength] = React.useState(true);
    const [enableLineWrap, setEnableLineWrap] = React.useState(true);

    const canMinimize = code && code.split('\n').length > 30;

    return <div className={'bg-transparent rounded border-4 border-teal-700'}>
        <div className={'pt-2 pb-2 px-2 font-bold flex flex-row bg-gray-100 items-center'}>
            <div>
                <button
                    onClick={() => {
                        setCopiedGuard(true)
                        copy(code)
                        setTimeout(() => {
                            setCopiedGuard(false)
                        }, 2500)
                    }}
                    type="button"
                    className="inline-flex items-center gap-x-1.5 rounded-md
                     px-2.5 py-1 text-sm shadow-sm
                     border
                     bg-white
                     hover:bg-gray-300 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                >
                    {(copiedValue && copiedGuard) ? 'Copied' : 'Copy'}
                    {(copiedValue && copiedGuard) ? <CheckCircleIcon className={'h-4 w-4 text-green-500'}/> :
                        <ClipboardDocumentIcon className={'h-4 w-4 text-amber-700'}/>}
                </button>
            </div>
            <div
                className={'inline-flex w-16 items-center rounded-full px-2 text-xs font-medium text-yellow-800  ml-2'}>
                {language}
            </div>

            <div className={'ml-2'}>{title}</div>

            <div className='flex-grow'></div>
            {
                (canMinimize) && <div>
                    <button
                        onClick={() => {
                            setEnableFixLength(!enableFixLength)
                        }}
                        type="button"
                        className="inline-flex items-center gap-x-1.5 rounded-md
                     px-2.5 py-1.5 text-sm font-semibold shadow-sm
                     border
                     bg-white
                     hover:bg-gray-300 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                    >
                        {enableFixLength ? <ArrowsPointingInIcon className={'h-5 w-5 text-blue-900'}/> :
                            <ChevronUpDownIcon className={'h-5 w-5 text-blue-900'}/>}
                    </button>
                </div>
            }

        </div>
        <div className={(canMinimize && enableFixLength) ? 'overflow-y-scroll h-[32rem] ' : ''}>
            <SyntaxHighlighter
                wrapLongLines={true}
                language={language} style={codeStyle}>
                {code}
            </SyntaxHighlighter>
        </div>

    </div>
}


export function LightCodeBlock({code, title, language, wrap}: {
    code: string,
    title?: string,
    language: string,
    wrap?: boolean
}) {
    const [copiedValue, copy] = useCopyToClipboard()
    const [copiedGuard, setCopiedGuard] = React.useState(false);
    const [enableFixLength, setEnableFixLength] = React.useState(true);
    const canMinimize = false;

    return <div className={'bg-transparent border border-gray-200'}>
        <div className={'px-2 flex flex-row bg-gray-100 items-center font-bold font-kode'}>

            <div className={'flex-grow truncate ml-2 text-sm text-gray-400'}>
                <span>
                {title}
                </span>
            </div>

            <div
                className={'inline-flex w-16 items-center rounded-full px-2 text-xs font-medium text-yellow-800  ml-2'}>
                {language}
            </div>

            <button
                onClick={() => {
                    setCopiedGuard(true)
                    copy(code)
                    setTimeout(() => {
                        setCopiedGuard(false)
                    }, 2500)
                }}
                type="button"
                className="inline-flex items-center gap-x-1.5 rounded-md
                     px-2.5 my-0.5 text-xs text-gray-600
                     border border-transparent
                     hover:text-teal-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
            >
                {(copiedValue && copiedGuard) ? 'Copied' : 'Copy'}
                {(copiedValue && copiedGuard) ? <CheckCircleIcon className={'h-4 w-4'}/> :
                    <ClipboardDocumentIcon className={'h-4 w-4'}/>}
            </button>

        </div>
        <div className={'overflow-x-scroll w-full text-sm'}>
            <SyntaxHighlighter
                language={language} style={codeStyle}>
                {code}
            </SyntaxHighlighter>
        </div>

    </div>
}

