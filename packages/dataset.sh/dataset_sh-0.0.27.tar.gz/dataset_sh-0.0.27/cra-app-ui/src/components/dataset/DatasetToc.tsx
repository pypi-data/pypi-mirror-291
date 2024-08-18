import {ArrowRightIcon} from "@heroicons/react/20/solid";
import React from "react";
import {Link} from "react-router-dom";
import {QueueListIcon} from "@heroicons/react/24/solid";
import {VariableIcon} from "@heroicons/react/24/outline";


type DatasetTOCItem = {
    id: string,
    title: string,
    level: number,
}

function createTOC(id: string,
                   title: string,
                   level: number,
) {
    return {
        id,
        title,
        level,
    }
}

export function VersionTagDescriptor({version, tag}: { version?: string, tag?: string }) {
    // const [open, setOpen] = React.useState(false)
    if (version) {
        return <span
            className={'text-wrap break-all\t'}
            // onMouseEnter={() => setOpen(true)}
            // onMouseLeave={() => setOpen(false)}
        >
            version: {
            version}
        </span>
    } else if (tag) {
        return <>
            tag: {tag}
        </>
    } else {
        return <>
            latest
        </>
    }
}

export function DatasetTOC({collections, username, datasetName, tag, version}: {
    collections: string[],
    datasetName: string,
    username: string,
    version?: string
    tag?: string
}) {
    const tocList: DatasetTOCItem[] = [
        createTOC('readme', 'About This Dataset', 2),

        createTOC('download', 'How to Download', 2),
        createTOC('download-cli', 'Download via cli', 3),
        createTOC('download-python', 'Download via python', 3),
    ]

    if (collections) {
        tocList.push(
            createTOC('collections', 'Collections', 2)
        )
    }


    return <div className={'bg-gradient-to-t from-orange-300 via-teal-300 to-orange-400 mt-40 rounded-b-lg'}>

        <div className={'flex flex-col items-start text-sm ml-2 pl-4 border-green-400 bg-white py-4'}>

            <div className={`mt-1 text-gray-900 text-sm font-bold mb-2 w-full`}>

                <div className={'flex flex-row items-center '}>
                    <img src={'/logo.png'} alt="Logo" style={{height: '20px'}}/>
                    <span className={'ml-2 text-amber-800 text-sm'}>dataset.sh</span>
                </div>
                <div className={'mb-2'}>{username}/{datasetName}</div>
                <Link className={'text-gray-600 text-xs mt-1 hover:underline'}
                      to={`/dataset/${username}/${datasetName}/version`}>
                    <VariableIcon className="inline h-4 w-4 text-teal-600 mr-1"/>
                    <VersionTagDescriptor tag={tag} version={version}/>
                </Link>
            </div>

            {tocList.map(toc => {
                if (toc.level == 2) {
                    return <div key={toc.id} className={`mt-4 text-gray-900 text-sm`}>
                        <a href={`#${toc.id}`}> {toc.title} </a>
                    </div>
                } else if (toc.level == 3) {
                    return <div key={toc.id} className={`mt-2 ml-6 text-gray-600`}>
                        <a href={`#${toc.id}`}>  {toc.title} </a>
                    </div>
                } else {
                    return undefined;
                }

            })}
        </div>
    </div>
}

export function TOCBlocks({
                              datasetName, namespace,
                              collections, sampleUrl
                          }: {
    collections: string[], sampleUrl?: string, datasetName: string, namespace: string
}) {
    const tocList: DatasetTOCItem[] = [
        createTOC('readme', 'About This Dataset', 2),
        createTOC('download', 'How to Download', 2),
        createTOC('collections', 'Collections', 2),
    ]
    return <>
        <div className={'grid grid-cols-1 gap-4 sm:grid-cols-4 mt-2'}>


            {
                tocList.map(toc => {
                    return <div
                        key={toc.id}
                        className="relative flex items-center space-x-3 rounded-lg w-full
                                border-2
                                border-blue-200
                                text-gray-700
                                px-2 py-3 shadow-sm focus-within:ring-2 focus-within:ring-indigo-500 focus-within:ring-offset-2 hover:border-gray-400"
                    >
                        <div className="min-w-0 flex-1">
                            <Link
                                onClick={() => {
                                    handleScroll(toc.id)
                                }}
                                to={`#${toc.id}`}
                                className="focus:outline-none ">
                                <span className="absolute inset-0" aria-hidden="true"/>
                                <p className="text-sm font-medium text-inherit">{toc.title}</p>
                            </Link>
                        </div>
                        <Link to=""><ArrowRightIcon className="h-5 w-5 text-teal-600"
                                                    aria-hidden="true"/></Link>
                    </div>
                })
            }

        </div>
    </>
}


function handleScroll(id: string) {
    const element = document.getElementById(id);
    if (element) {
        element.scrollIntoView({behavior: 'smooth'});
    }
};
