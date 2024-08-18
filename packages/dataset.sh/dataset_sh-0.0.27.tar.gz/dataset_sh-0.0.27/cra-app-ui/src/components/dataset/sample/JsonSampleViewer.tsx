import {ClassDefinition, CollectionConfig, DatasetSample, DatasetSchema} from "../../../features";
import React, {useMemo} from "react";
import {MinusCircleIcon, MinusIcon, PlusCircleIcon, PlusIcon} from "@heroicons/react/24/outline";
import {classNames} from "../../../utils/common";

const PADDING = 4

export function JsonSampleViewer(
    {
        items,
        schema
    }: {
        items: object[],
        schema: DatasetSchema,
    }) {

    const [idx, setIdx] = React.useState(1)
    return <div className={'bg-gray-100'}>
        <div className={'flex flex-row gap-x-4 p-2 border-b'}>
            <span className={'px-2'}>Current: {idx}/{items.length}</span>
            <button
                onClick={() => {
                    setIdx(idx => Math.max(idx - 1, 1))
                }}
                className={'border hover:bg-teal-200 bg-slate-300 px-1'}>Prev
            </button>
            <button
                onClick={() => {
                    setIdx(idx => Math.min(idx + 1, items.length))
                }}
                className={'border hover:bg-teal-200 bg-slate-300 px-1'}>Next
            </button>
        </div>
        <div className={'pt-2'}>
            <JsonObjectOrArrayViewer value={items[idx - 1]} indent={0}/>
        </div>
        <div className="mt-2 border-t border-orange-800 px-4 pb-1 font-bold text-orange-800 text-sm">
            <span>Showing only {items.length} items, download to see more.</span>
        </div>

    </div>
}

function JsonArrayViewer(
    {indent, items}: { items: object[], indent: number }
) {
    const [hide, setHide] = React.useState(false)
    return <div className={'flex flex-col'}>
        <div>
            {
                hide ? <PlusCircleIcon
                    className={'h-5 w-5 mx-0.5 inline cursor-pointer text-green-500 hover:text-green-700'}
                    onClick={() => setHide(h => !h)}
                /> : <MinusCircleIcon
                    className={'h-5 w-5 mx-0.5 inline cursor-pointer text-red-500 hover:text-red-700'}
                    onClick={() => setHide(h => !h)}
                />
            }
            {'['}
        </div>

        {!hide && <div className={'pl-12'}>
            {
                items.map((x, idx) => {
                    return <JsonArrayIndexViewer index={idx} value={x} key={idx} indent={indent}/>
                })
            }
        </div>}


        <div>{']'}</div>

    </div>
}

function JsonArrayIndexViewer({index, value, indent}: { index: number, value: object | object[], indent: number }) {
    return <div className={'flex flex-row'}>
        <span className={'font-bold'}>{index}: </span>
        <JsonObjectOrArrayViewer value={value} indent={indent}/>
    </div>
}

function JsonObjectViewer({value, indent}: { value: object, indent: number }) {
    const [hide, setHide] = React.useState(false)
    const entries = useMemo(() => {
        return value ? Object.entries(value) : [];
    }, [value]);
    return <div className={'flex flex-col'}>
        <div>

            {
                hide ? <PlusCircleIcon
                    className={'h-5 w-5 mx-0.5 inline cursor-pointer text-green-500 hover:text-green-700'}
                    onClick={() => setHide(h => !h)}
                /> : <MinusCircleIcon
                    className={'h-5 w-5 mx-0.5 inline cursor-pointer text-red-500 hover:text-red-700'}
                    onClick={() => setHide(h => !h)}
                />
            }
            {'{'}
        </div>
        {
            !hide && entries.map(([keyName, keyValue]) => {
                return <JsonFieldViewer key={keyName} keyName={keyName} value={keyValue} indent={indent + 1}/>
            })
        }
        <div>{'}'}</div>
    </div>
}

function JsonFieldViewer({keyName, value, indent}: { keyName: string, value: object | object[], indent: number }) {

    return <div className={`flex flex-row gap-x-1 pl-4 my-0.5`}>
        <span className={'text-blue-600 bg-gray-50 h-fit px-1 underline rounded-md'}>{keyName}: </span>
        <JsonObjectOrArrayViewer value={value} indent={indent}/>
    </div>
}

function JsonObjectOrArrayViewer({value, indent}: { value: object | object[], indent: number }) {
    const valueType = useMemo(() => {
        return checkValueType(value)
    }, [
        value
    ])

    let main;

    if (valueType === 'array') {
        main = <JsonArrayViewer items={value as object[]} indent={indent}/>
    } else if (valueType === 'object') {
        main = <JsonObjectViewer value={value} indent={indent}/>
    } else {
        main =
            <span className={'bg-white px-2 border border-gray-300 rounded-md break-all'}>{JSON.stringify(value)}</span>
    }
    return <>
        {
            main
        }
    </>
}

function checkValueType(value: any): string {
    if (Array.isArray(value)) {
        return 'array';
    } else if (typeof value === 'object' && value !== null) {
        return 'object';
    } else {
        return typeof value;
    }
}
