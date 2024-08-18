import React from "react";
import {classNames} from "../../../../utils/common";

export function QueryResultSelector({
                                 filteredCollectionNames, setSelected, addSelected, oneCollMode
                             }: {
    setSelected: (ns: string[]) => void,
    addSelected: (n: string) => void,
    oneCollMode: boolean,
    filteredCollectionNames: string[]
}) {
    return <div className={
        classNames(' overflow-y-scroll p-4 my-2 border rounded-md', oneCollMode ? 'max-h-[10em]' : 'h-[20em]')
    }>
        <div className={'mb-2 text-gray-600 text-xs font-bold'}>Collection Search Results:</div>
        {filteredCollectionNames.length > 0 ? (
            <ul className={'flex flex-col gap-y-1'}>
                {filteredCollectionNames.slice(0, 50).map((name) => (
                    <li
                        key={name}
                        className="bg-white border rounded-md px-4 hover:bg-blue-100 cursor-pointer"
                        onClick={() => {
                            if (oneCollMode) {
                                setSelected([name])
                            } else {
                                addSelected(name)
                            }
                        }}
                    >
                                <span
                                    className={'w-fit underline  hover:text-blue-600'}
                                    // to={`${baseUrl}/collection/${collectionNames}`}
                                >
                                    {name}
                                </span>
                    </li>
                ))}
            </ul>
        ) : (
            <div>No collections match your search.</div>
        )}

        {filteredCollectionNames.length > 50 && <div
            className={'mt-2 text-gray-600'}
        >{Math.max(filteredCollectionNames.length - (50), 0)} more collections...
        </div>}
    </div>
}
