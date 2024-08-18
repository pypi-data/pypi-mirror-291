import {DatasetTagHooks, DatasetVersionHooks} from "../../../features";
import {Link, useParams} from "react-router-dom";
import React from "react";
import {Helmet} from "react-helmet-async";
import {ArrowRightIcon} from "@heroicons/react/20/solid";

export function DatasetVersionListingPage() {
    const {datasetName, namespace} = useParams();
    const versionListLoader = DatasetVersionHooks.useDatasetVersions(namespace!, datasetName!)
    const tagLoad = DatasetTagHooks.useDatasetTags(namespace!, datasetName!)

    function resolveTags(v: string): string[] {
        if (tagLoad.data) {
            return tagLoad.data.data.items.filter(({version}) => v === version).map(x => x.tag)
        }
        return []
    }

    return <>
        <Helmet>
            <title> versions of {namespace}/{datasetName} | dataset.sh </title>
        </Helmet>

        <div className={'container mx-auto mt-6 px-4 max-w-screen-xl'}>

            <Link
                className={'inline-flex flex-row my-2 border-gray-400 border-2 py-2 px-6 rounded-lg hover:bg-green-300 items-center'}
                to={`/dataset/${namespace}/${datasetName}`}>
                <span className={'mr-2'}>
                    Latest version
                </span>
                <ArrowRightIcon className="h-5 w-5 text-teal-600"
                                aria-hidden="true"/>
            </Link>

            <div className={'w-full'}>
                <div className={'grid grid-cols-1 md:grid-cols-2'}>
                    {versionListLoader.data && versionListLoader.data.data.items.map(v => {
                        return <React.Fragment key={v.version}>
                            <div>
                                <div>Version:</div>
                                <Link
                                    className={'hover:underline break-words'}
                                    to={`/dataset/${namespace}/${datasetName}/version/${v.version}`}>
                                    {v.version}
                                </Link>
                            </div>
                            <div>
                                <div>Tags:</div>
                                {resolveTags(v.version).map(t => {
                                    return <Link
                                        className={'hover:underline'}
                                        to={`/dataset/${namespace}/${datasetName}/tag/${t}`}>
                                        {t}
                                    </Link>
                                })}
                            </div>
                            <div className={'border-b my-2 col-span-1 md:col-span-2'}>

                            </div>
                        </React.Fragment>
                    })}
                </div>
            </div>
        </div>
    </>
}