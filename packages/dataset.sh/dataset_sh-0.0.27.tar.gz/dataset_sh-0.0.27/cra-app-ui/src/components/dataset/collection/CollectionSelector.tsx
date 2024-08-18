import React, {useState, useMemo} from "react";
import {MinusIcon, PlusIcon, XMarkIcon} from "@heroicons/react/24/outline";
import {SingleContent} from "./content/SingleContent";
import {MultipleContent} from "./content/MultipleContent";
import {classNames} from "../../../utils/common";
import {useClickOutsideRef} from "../../../utils/useClickOutside";


function joinStrings(...strings: string[]): string {
    return strings.join(" ");
}


function MinimizeButton({isMinimized, onClick}: {
    isMinimized: boolean; // Indicates if the target content is currently minimized
    onClick: () => void
}) {
    return (
        <button onClick={onClick}
                className="p-2 rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
            {isMinimized ? (
                <PlusIcon className="w-5 h-5 text-gray-700" aria-hidden="true"/>
            ) : (
                <MinusIcon className="w-5 h-5 text-gray-700" aria-hidden="true"/>
            )}
        </button>
    );
}


export function CollectionSelector(
    {
        collectionNames,
        setSelected,
        selected,
        baseUrl
    }: {
        baseUrl: string
        collectionNames: string[];
        selected: string[]
        setSelected: (selected: string[]) => void;
    }) {
    const [query, setQuery] = useState<string>("");
    const [oneCollMode, setOneCollMode] = useState<boolean>(false);
    const [collapse, setCollapse] = useState<boolean>(true);
    const outsideRef = useClickOutsideRef({
        onOutsideClick: () => {
            setCollapse(true)
        }
    })
    // Memoize filtered collection names
    const filteredCollectionNames = useMemo(() => {
        return collectionNames.filter((name) =>
            (!selected.includes(name)) && name.toLowerCase().includes(query.toLowerCase())
        );
    }, [collectionNames, query]);


    let selector;
    if (collectionNames.length > 1) {
        selector = oneCollMode ? <SingleContent
            filteredCollectionNames={filteredCollectionNames}
            oneCollMode={oneCollMode}
            setQuery={setQuery}
            setSelected={setSelected}
            selected={selected}
            query={query}
        /> : <MultipleContent
            filteredCollectionNames={filteredCollectionNames}
            oneCollMode={oneCollMode}
            setQuery={setQuery}
            setSelected={setSelected}
            selected={selected}
            query={query}
        />
    } else {
        selector = <div></div>;
    }
    let main = collapse ? <div></div> : selector

    return (
        <div ref={outsideRef} className={'sticky top-0 z-50'}>
            {(!collapse) && <div className={'h-10 bg-white z-50 w-full'}></div>}
            <div
                className={joinStrings('bg-blue-50 border-2 border-gray-500 rounded-md px-2', collapse ? 'py-2' : 'shadow-lg py-4')}>

                <div className={'flex flex-row'}>
                    <a className={
                        classNames(
                            "pl-2 text-xl font-bold underline text-slate-900",
                            collectionNames.length > 1 ? 'cursor-pointer' : 'cursor-auto'
                        )
                    } id={'collections'}
                       href={'#collections'}
                       onClick={() => {
                           if (collectionNames.length > 1) {
                               setCollapse(collapse => !collapse)
                           }
                       }}
                    >
                        <span>This dataset has {collectionNames.length} {collectionNames.length > 1 ? "collections" : "collection"}</span>
                        {(!oneCollMode) &&
                            <span>(showing {oneCollMode ? Math.min(selected.length, 1) : selected.length})</span>}.
                    </a>
                    <div className="flex-grow"></div>
                    {
                        collectionNames.length > 1 && <div className="flex items-center me-4">
                            <input
                                onChange={e => {
                                    if (e.target.checked) {
                                        setSelected(selected.slice(0, 1))
                                    }
                                    setOneCollMode(e.target.checked)
                                }}
                                checked={oneCollMode} id="red-checkbox" type="checkbox"
                                className="w-4 h-4 text-red-600 bg-gray-100 border-gray-300 rounded focus:ring-red-500  focus:ring-2  "/>
                            <label htmlFor="red-checkbox"
                                   className="ms-2 text-sm font-medium text-gray-900">Single Collection Mode</label>
                        </div>
                    }

                    {
                        collectionNames.length > 1 && <div>
                            <MinimizeButton
                                isMinimized={collapse}
                                onClick={() => {
                                    setCollapse(collapse => !collapse)
                                }}
                            />
                        </div>
                    }

                </div>


                {main}

            </div>

        </div>
    );
}
