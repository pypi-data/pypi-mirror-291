import React, {useMemo} from "react";

import {CollectionConfig} from "../../../features";
import {DatasetTOC, TOCBlocks, VersionTagDescriptor} from "../DatasetToc";
import {DownloadTabs} from "../DownloadTabs";
import {ReadmeViewer} from "./DatasetReadmeViewer";
import {CollectionDocumentViewer} from "../collection/CollectionDocumentViewer";
import {CollectionSelector} from "../collection/CollectionSelector";
import {formatFileSize} from "../../../utils/common";
import {VariableIcon} from "@heroicons/react/24/outline";
import {Link} from "react-router-dom";

export function DatasetDocumentationViewer(
    {
        namespace,
        datasetName,
        collections,
        pythonDownloadCode,
        bashDownloadCode,
        readmeContent,
        tag, version,
        showCollectionCount,
        fileSize
    }: {
        namespace: string,
        datasetName: string,
        collections: CollectionConfig[],
        pythonDownloadCode: string,
        bashDownloadCode: string,
        tag?: string, version?: string,
        readmeContent: string,
        showCollectionCount?: number
        fileSize: number
    }) {

    const [selected, setSelected] = React.useState<string[]>(
        collections.slice(0, 4).map(x => x.name)
    )
    const showCollCount = showCollectionCount || 4;

    const selectedCollections = useMemo(() => {
        return collections.filter((x) => selected.includes(x.name)).slice(0, showCollCount)
    }, [collections, selected, showCollCount])

    const collectionNames = collections?.map(x => x.name) || []
    let baseUrl = ''
    if (tag) {
        baseUrl = `/dataset/${namespace}/${datasetName}/tag/${tag}`
    } else if (version) {
        baseUrl = `/dataset/${namespace}/${datasetName}/version/${version}`
    } else {
        baseUrl = `/dataset/${namespace}/${datasetName}`
    }
    return <div className={'mt-4 pt-2 flex flex-row mb-32 container-lg mx-auto '}>
        <>
            <div className={'mr-4 w-full xl:pr-64'}>
                <div className={'mr-4 '}>
                    <Link
                        className={'border w-fit bg-gray-50 text-gray-600 text-xs mt-1 hover:underline flex flex-row items-end py-1 px-4 rounded-md mb-2'}
                        to={`/dataset/${namespace}/${datasetName}/version`}>
                        <VariableIcon className="inline h-4 w-4 text-teal-600"/>
                        <span className={'mx-1'}><span className={'text-red-300'}>(click here to switch)</span></span>
                        <VersionTagDescriptor tag={tag} version={version}/>
                    </Link>
                    <TOCBlocks
                        namespace={namespace}
                        datasetName={datasetName}
                        sampleUrl={collectionNames.length > 0 ? `${baseUrl}/collection/${collectionNames[0]}/sample` : undefined}
                        collections={collectionNames}/>
                </div>

                <div className="mt-8">
                    <div className={'my-2 text-gray-500'}>File Size: {formatFileSize(fileSize)}</div>
                    <ReadmeViewer namespace={namespace} datasetName={datasetName} readmeContent={readmeContent}/>
                </div>

                <div className={'mt-16'}>
                    <a className={"text-3xl font-bold underline text-slate-900"} id={'download'}
                       href={'#download'}>
                        Download this dataset
                    </a>

                    <div className={'mt-2'}>
                        You can download this dataset using the following scripts.
                    </div>

                    <div className={'mt-2'}>
                        <DownloadTabs
                            pyCode={pythonDownloadCode || '# loading python script'}
                            bashCode={bashDownloadCode || '# loading bash script'}
                        />
                    </div>
                </div>

                {collections && <div className={'mt-16'}>


                    <CollectionSelector
                        baseUrl={baseUrl}
                        collectionNames={collections.map(c => c.name)}
                        selected={selected}
                        setSelected={setSelected}
                    />

                    <div className={'mt-2'}>
                        {
                            selectedCollections.map((collectionConfig, idx) => {
                                return <CollectionDocumentViewer
                                    key={collectionConfig.name}
                                    idx={idx}
                                    namespace={namespace}
                                    datasetName={datasetName}
                                    collectionConfig={collectionConfig}
                                    tag={tag}
                                    version={version}
                                />
                            })
                        }
                    </div>
                </div>
                }
            </div>
            <div
                className={'flex-none w-64 h-screen sticky top-0 right-0 hidden xl:block'}
            >
                <div className={'mt-16'}>
                    <DatasetTOC collections={collectionNames} datasetName={datasetName} username={namespace} tag={tag}
                                version={version}/>
                </div>
            </div>
        </>
    </div>
}

