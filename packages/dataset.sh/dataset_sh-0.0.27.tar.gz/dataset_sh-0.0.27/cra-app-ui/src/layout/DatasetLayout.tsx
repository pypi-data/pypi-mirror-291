import React from "react";
import {Link as RouterLink, Outlet, useLocation, useParams} from "react-router-dom";
 
export function DatasetLayout(props: {}) {
    const {namespace, datasetName} = useParams();
    const location = useLocation();
    const homeUrl = `/dataset/${namespace}/${datasetName}`
    let selectedPage = 0;
    const pathParts = location.pathname.split('/');
    if (location.pathname === `${homeUrl}/data`) {
        selectedPage = 1
    }

    return <div className={''}>
        <div className={'container mx-auto max-w-screen-xl mt-8 p-4 '}>
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
                                        className="ms-1 text-sm font-medium text-gray-500 md:ms-2">{namespace}</RouterLink>
                        </div>
                    </li>

                    <li aria-current="page">
                        <div className="flex items-center">
                            <svg className="rtl:rotate-180 w-3 h-3 text-gray-400 mx-1" aria-hidden="true"
                                 xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 6 10">
                                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"
                                      stroke-width="2" d="m1 9 4-4-4-4"/>
                            </svg>
                            <RouterLink to={`/dataset/${namespace}/${datasetName}`}
                                        className="ms-1 text-sm font-medium text-gray-800 md:ms-2">{datasetName}</RouterLink>
                        </div>
                    </li>

                </ol>
            </nav>
        </div>


        <div className={'mb-2'}>
            <Outlet/>
        </div>


    </div>
}

