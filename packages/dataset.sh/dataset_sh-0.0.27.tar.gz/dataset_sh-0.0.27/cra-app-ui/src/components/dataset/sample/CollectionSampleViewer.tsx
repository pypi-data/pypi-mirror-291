import {CollectionConfig, DatasetSample, getMainEntryPointClass} from "../../../features";
import React from "react";
import {CodeBlock} from "../../CodeBlock";
import {CollectionViewer} from "../../DatasetSampleViewer";
import {Link} from "react-router-dom";
import {ArrowUpOnSquareIcon} from "@heroicons/react/24/outline";
import {JsonSampleViewer} from "./JsonSampleViewer";
import {classNames} from "../../../utils/common";


export type SampleViewerMode = 'json' | 'table' | 'text'


export function CollectionSampleViewer(
    {
        collectionConfig, sampleData, collectionName, collectionUrl, showLink
    }: {
        collectionConfig?: CollectionConfig,
        sampleData: DatasetSample,
        collectionName: string,
        collectionUrl: string,
        showLink: boolean
    }) {
    const [mode, setMode] = React.useState<SampleViewerMode>('table')
    const mainClzSchema = collectionConfig && getMainEntryPointClass(collectionConfig.data_schema)
    let main;
    if (!mainClzSchema || mode === 'text') {
        main = <>
            <CodeBlock
                language={'json'}
                code={JSON.stringify(sampleData)}
                title={`Data sample from collection ${collectionName}`}/>
            <div className="px-4 pb-1 font-bold text-orange-800 text-sm">
                <span>Showing only {sampleData.length} items, download to see more.</span>
            </div>
        </>
    } else {
        if (mode === 'json') {
            main = <JsonSampleViewer
                items={sampleData}
                schema={collectionConfig.data_schema}
            ></JsonSampleViewer>
        } else {
            main = <CollectionViewer
                items={sampleData}
                keys={mainClzSchema.fields.map(x => x.name)}
            />
        }

    }
    return <>
        <div className={'flex flex-row-reverse items-center bg-gray-50 px-4'}>
            <Link
                to={collectionUrl}
                className={'border px-4 py-2  m-2 flex flex-row items-center rounded-md bg-gray-100 text-gray-900 hover:bg-gray-300 hover:ring-1 ring-amber-400'}
            >
                Open <ArrowUpOnSquareIcon className={'h-5 w-5 ml-1'}/>
            </Link>

            <div className={'flex-grow'}></div>

            <div className={'flex flex-row gap-x-3'}>
                <button
                    onClick={() => {
                        setMode('table')
                    }}
                    className={classNames('border py-2 px-2 bg-gray-100 text-md text-gray-900 rounded-md hover:bg-green-200', mode === 'table' ? 'bg-green-200 border-green-500' : '')}>
                    Table
                </button>

                <button
                    onClick={() => {
                        setMode('json')
                    }}
                    className={classNames('border py-2 px-2 bg-gray-100 text-md text-gray-900 rounded-md hover:bg-green-200', mode === 'json' ? 'bg-green-200 border-green-500' : '')}>
                    JSON
                </button>

                <button
                    onClick={() => {
                        setMode('text')
                    }}
                    className={classNames('border py-2 px-2 bg-gray-100 text-md text-gray-900 rounded-md hover:bg-green-200', mode === 'text' ? 'bg-green-200 border-green-500' : '')}>
                    JSON Text
                </button>
            </div>


        </div>
        {main}

    </>


}