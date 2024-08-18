import React from "react";
import {LightCodeBlock} from "../CodeBlock";


export type CodeUsageWithTitle = {
    name: string,
    code: string,
    language: string,
    id: string
}


function PythonDownloadCode({code}: {code: string }) {

    return <div
        id='download-python'
        className={'mb-2'}>
        <LightCodeBlock
            code={code} language={'python'} title={'Download With Python'}/>
    </div>
}

function BashDownloadCode({code}: {code: string }) {

    return <div
        id='download-cli'
        className={'mb-2'}>
        <LightCodeBlock

            code={code} language={'shell'} title={'Download With Cli'}/>
    </div>

}

export function DownloadTabs({pyCode, bashCode}: { pyCode: string, bashCode: string }) {

    return <>
        <PythonDownloadCode code={pyCode}/>
        <BashDownloadCode code={bashCode}/>
    </>
}
