import {useQuery} from "@tanstack/react-query";
import {Features} from "../features";
import {Link as RouterLink, useParams} from 'react-router-dom'
import React from "react";
import {Helmet} from "react-helmet-async";
import _ from "lodash";

export function SingleStoreListingPage() {

    const {namespace} = useParams();


    const datasetQuery = useQuery({
        queryKey: ['datasets', namespace], queryFn: async () => {
            return Features.listDatasetsForStore(namespace!);
        }
    })
    const sortedDatasets = datasetQuery.data?.data.items ? _.sortBy(datasetQuery.data?.data.items, x => x.dataset) : [];

    return <>

        <Helmet>
            <title> datasets of {namespace} | dataset.sh </title>
        </Helmet>


        <div className={'container mx-auto max-w-screen-xl mt-8 p-4'}>
            <nav className="flex" aria-label="Breadcrumb">
                <ol className="inline-flex items-center space-x-1 md:space-x-2 rtl:space-x-reverse">
                    <li className="inline-flex items-center">
                        <RouterLink to="/"
                                    className="inline-flex items-center text-sm font-medium text-gray-500 hover:text-blue-600">
                            <svg className="w-3 h-3 me-2.5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
                                 fill="currentColor" viewBox="0 0 20 20">
                                <path
                                    d="m19.707 9.293-2-2-7-7a1 1 0 0 0-1.414 0l-7 7-2 2a1 1 0 0 0 1.414 1.414L2 10.414V18a2 2 0 0 0 2 2h3a1 1 0 0 0 1-1v-4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v4a1 1 0 0 0 1 1h3a2 2 0 0 0 2-2v-7.586l.293.293a1 1 0 0 0 1.414-1.414Z"/>
                            </svg>
                            Home
                        </RouterLink>
                    </li>
                    <li aria-current="page">
                        <div className="flex items-center">
                            <svg className="rtl:rotate-180 w-3 h-3 text-gray-400 mx-1" aria-hidden="true"
                                 xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 6 10">
                                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"
                                      stroke-width="2" d="m1 9 4-4-4-4"/>
                            </svg>
                            <RouterLink to={'/dataset'}
                                        className="ms-1 text-sm font-medium text-gray-500 md:ms-2">Dataset</RouterLink>
                        </div>
                    </li>

                    <li aria-current="page">
                        <div className="flex items-center">
                            <svg className="rtl:rotate-180 w-3 h-3 text-gray-400 mx-1" aria-hidden="true"
                                 xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 6 10">
                                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"
                                      stroke-width="2" d="m1 9 4-4-4-4"/>
                            </svg>
                            <RouterLink to={`/dataset/${namespace}`}
                                        className="ms-1 text-sm font-medium text-gray-800 md:ms-2">{namespace}</RouterLink>
                        </div>
                    </li>

                </ol>
            </nav>

            <div className={'bg-gray-100 min-h-screen pb-8 px-8 mt-3 pt-1 mx-2 rounded-md'}>
                <div className={'mt-6 font-bold text-teal-700'}>
                    Namespace {namespace}:
                </div>

                <div>
                    {sortedDatasets.map(x => {
                        return <div
                            className={'my-2'}
                            key={x.dataset}
                        >
                            <RouterLink
                                to={`/dataset/${x.namespace}/${x.dataset}`}
                                key={`${x.namespace}/${x.dataset}`}>
                                {x.namespace}/{x.dataset}
                            </RouterLink>
                        </div>
                    })}
                </div>
            </div>


        </div>
    </>
}
