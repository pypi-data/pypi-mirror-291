import React, {useState, useMemo} from "react";
import {MinusIcon, PlusIcon, XMarkIcon} from "@heroicons/react/24/outline";
import {ArrowLeftIcon, ArrowRightIcon} from "@heroicons/react/20/solid";
import {Link} from "react-router-dom";
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


export function StandaloneCollectionSelector(
    {
        collectionNames,
        currentCollection,
        baseUrl,
    }: {
        baseUrl: string,
        currentCollection: string
        collectionNames: string[];
    }) {
    const [query, setQuery] = useState<string>("");
    const [collapse, setCollapse] = useState<boolean>(true);
    const oneCollMode = true;
    // Memoize filtered collection names
    const filteredCollectionNames = useMemo(() => {
        return collectionNames.filter((name) =>
            name.toLowerCase().includes(query.toLowerCase())
        );
    }, [collectionNames, query]);
    const outsideRef = useClickOutsideRef({
        onOutsideClick: () => {
            setCollapse(true)
        }
    })

    let queryEditor = <form>
        <label htmlFor="search"
               className="mb-2 text-sm font-medium text-gray-900 sr-only ">Search</label>
        <div className="relative">
            <div className="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
                <svg className="w-4 h-4 text-gray-500 " aria-hidden="true"
                     xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"
                          stroke-width="2"
                          d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"/>
                </svg>
            </div>
            <input type="search"
                   id="search"
                   className="block w-full max-w-[40em] p-2 ps-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500  "
                   value={query}
                   onChange={(e) => setQuery(e.target.value)}
                   placeholder="Search collections..."
                   required/>
        </div>
    </form>


    let querySelector = <div className={
        joinStrings(' overflow-y-scroll p-4 my-2 border rounded-md', oneCollMode ? 'max-h-[10em]' : 'h-[20em]')
    }>
        <div className={'mb-2 text-gray-600 text-xs font-bold'}>Collection Search Results:</div>
        {filteredCollectionNames.length > 0 ? (
            <ul className={'flex flex-col gap-y-1'}>
                {filteredCollectionNames.slice(0, 50).map((name) => (
                    (currentCollection !== name) ? <li
                        key={name}
                        className="bg-white border rounded-md px-4 hover:bg-blue-100 cursor-pointer"
                    >
                        <Link
                            className={'w-fit underline  hover:text-blue-600'}
                            to={`${baseUrl}/collection/${name}`}
                        >
                            {name}
                        </Link>
                    </li> : <li
                        key={name}
                        className="border rounded-md px-4 bg-green-50  "
                    >
                        <span
                            className={'w-fit '}
                            // to={`${baseUrl}/collection/${name}`}
                        >
                            <span className={'text-green-800'}>(currently showing)</span> {name}
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


    let singleSelector = <div className={'mt-2'}>
        {collectionNames.length > 1 && <>
            {queryEditor}
            {querySelector}
        </>}

    </div>

    let main = collapse ? <div></div> : singleSelector


    return (
        <div className={'sticky top-0 z-50'} ref={outsideRef}>
            {(!collapse) && <div className={'h-10 bg-white z-50 w-full'}></div>}
            <div
                className={joinStrings('bg-blue-50 border-2 border-gray-500 rounded-md px-2', collapse ? 'py-2' : 'shadow-lg py-4')}>

                <div className={'flex flex-row'}>

                    <Link
                        to={baseUrl}
                        className={
                            'flex flex-row text-gray-700 items-center cursor-pointer bg-gray-300 px-4 py-1 rounded-md mx-4 hover:bg-indigo-400 hover:ring ring-amber-500'
                        }>
                        <ArrowLeftIcon className={'h-5 w-5'}/> Back
                    </Link>

                    <span
                        onClick={() => {
                            if (collectionNames.length > 1) {
                                setCollapse(collapse => !collapse)
                            }
                        }}
                        className={joinStrings(" pl-2 text-xl font-bold underline text-slate-900", collectionNames.length > 1 ? 'cursor-pointer' : "")}
                        id={'collections'}
                    >
                        <span>This dataset has {collectionNames.length} {collectionNames.length > 1 ? "collections" : "collection"}</span>
                    </span>
                    <div className="flex-grow"></div>

                    <div>
                        {collectionNames.length > 1 && <MinimizeButton
                            isMinimized={collapse}
                            onClick={() => {
                                setCollapse(collapse => !collapse)
                            }}
                        />}
                    </div>
                </div>
                {main}
            </div>

        </div>
    );
}
