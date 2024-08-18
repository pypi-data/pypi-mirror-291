import {useQuery} from "@tanstack/react-query";
import {Features} from "../features";
import {Link as RouterLink} from 'react-router-dom'
import _ from 'lodash'
import React from "react";
import {Helmet} from "react-helmet-async";

export function DatasetListingPage() {

    const datasetQuery = useQuery({
        queryKey: ['datasets'], queryFn: async () => {
            return Features.listDatasets();
        }
    })

    const byNamespace = _.groupBy(datasetQuery.data?.data.items, x => x.namespace)

    let main;

    if (datasetQuery.status === 'loading') {
        main = <>
        </>
    } else if (byNamespace && Object.keys(byNamespace).length > 0) {
        main = <>


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
                                        className="ms-1 text-sm font-medium text-gray-800 md:ms-2">Dataset</RouterLink>
                        </div>
                    </li>
                </ol>
            </nav>


            <div>
                {
                    _.map(byNamespace, (datasets, store) => {
                        const sortedDatasets = _.sortBy(datasets, x => x.dataset)
                        return <div
                            className={'mt-4 p-4 rounded-md bg-gray-100'}
                            key={store}>
                            <RouterLink
                                to={`/dataset/${store}`}
                                className={'font-bold text-teal-700'}
                            >Namespace: {store}</RouterLink>
                            {
                                sortedDatasets.map(x => {
                                    return <div
                                        key={store + '/' + x.dataset}
                                        className={'my-1 ml-2'}
                                    >
                                        <RouterLink
                                            to={`/dataset/${x.namespace}/${x.dataset}`}
                                            key={`${x.namespace}/${x.dataset}`}>
                                            {x.namespace}/{x.dataset}
                                        </RouterLink>
                                    </div>
                                })
                            }
                        </div>
                    })
                }
            </div>
        </>
    } else {
        main = <div className={'mt-32 p-8 border-2 border-green-200'}>
            <div className="flex flex-col items-center">
                <div>
                    <p className="text-lg font-semibold text-orange-600">Hello, </p>
                    <h1 className="mt-2 text-2xl font-bold tracking-tight text-indigo-900 sm:text-3xl">Welcome to
                        dataset.sh server</h1>
                </div>
                <p className="mt-1 text-base leading-7 text-gray-500">
                    You currently have 0 dataset managed by this server.
                </p>

                <div className="mt-10 flex">
                    <a href="https://dataset.sh" className="text-sm font-semibold text-gray-900">
                        See Documentation <span aria-hidden="true">&rarr;</span>
                    </a>
                </div>
            </div>
        </div>
    }

    return <>

        <Helmet>
            <title>datasets | dataset.sh browser</title>
        </Helmet>


        <div className={'container mx-auto max-w-screen-xl mt-8 p-4'}>
            {main}
        </div>
    </>
}
