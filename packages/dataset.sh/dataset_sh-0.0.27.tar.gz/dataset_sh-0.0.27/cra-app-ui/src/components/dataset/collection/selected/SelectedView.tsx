import {XMarkIcon} from "@heroicons/react/24/outline";
import React, {useMemo} from "react";

export function SingleSelectedView({selected, setSelected}: {
    selected: string[],
    setSelected: (q: string[]) => void
}) {
    return <div className={'flex flex-col p-4'}>
        {selected && selected.slice(0, 1).map(s => {
            return <div
                onClick={() => setSelected([])}
                className={'rounded-md px-2 py-1 cursor-pointer flex flex-row items-center border hover:bg-red-300'}>
                <div
                    key={s} className={'text-red-600'}>
                    <XMarkIcon className={'h-4 w-4'}></XMarkIcon>
                </div>
                <div>
                    {s}
                </div>
            </div>
        })}
    </div>
}

export function MultipleSelectedView({selected, setSelected}: {
    selected: string[],
    setSelected: (q: string[]) => void
}) {

    const removeSelected = useMemo(() => {
        return (itemToRemove: string) => {
            setSelected(selected.filter(item => item !== itemToRemove));
        }
    }, [selected, setSelected])

    return <>
        <div>
            Selected {selected.length} collection(s):
        </div>
        <div className={'flex flex-row flex-wrap max-w-full gap-y-1 m-2 '}>
            {selected.map(s => {
                return <div
                    onClick={() => removeSelected(s)}
                    className={'border bg-white rounded-md px-2 py-1 cursor-pointer flex flex-row items-center hover:bg-red-300'}>
                    <div
                        key={s} className={'text-red-600'}>
                        <XMarkIcon className={'h-4 w-4'}>

                        </XMarkIcon>
                    </div>
                    <div>
                        {s}
                    </div>
                </div>
            })}
        </div>
    </>
}