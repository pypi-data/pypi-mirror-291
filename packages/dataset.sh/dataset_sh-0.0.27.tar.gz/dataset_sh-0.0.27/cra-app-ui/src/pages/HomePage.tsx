import {useQuery} from "@tanstack/react-query";
import {Features, OtherHooks, PostHooks} from "../features";
import React from "react";
import {Link as RouterLink, useLocation, useParams} from "react-router-dom";
import {PostViewer} from "../components/posts/PostViewer";
import {
    FolderOpenIcon
} from '@heroicons/react/24/outline'
import {Helmet} from "react-helmet-async";

export function HomePage() {

    const homePostQuery = PostHooks.usePost('index')
    const hostnameLoader = OtherHooks.useHostName()
    const hostName = hostnameLoader.data?.data.hostname || 'your-hostname'

    let main;
    if (homePostQuery.status === 'loading') {
        main = null;
    } else if (homePostQuery.status === 'success') {
        main = <div>
            <PostViewer post={homePostQuery.data.data} projectName={'index'} hideProject={true} hostName={hostName}/>
        </div>
    } else {
        main = null;
    }

    return <>

        <Helmet>
            <title> dataset.sh </title>
        </Helmet>

        <div className={'min-h-screen'}>
            <div className={'bg-gradient-to-l from-pink-50 to-green-50 py-2 pl-4'}>
                <div className={'flex flex-row container mx-auto max-w-screen-xl my-6'}>
                    <div>Welcome to dataset.sh server.</div>
                </div>

                <div className={'flex flex-col items-start container mx-auto max-w-screen-xl mb-10'}>
                    <RouterLink
                        className={'flex flex-row items-center p-2 border-2 border-r-4 hover:border-amber-400 border-purple-500 rounded-md my-2'}
                        to={'/dataset'}>
                        <span className={'h-5 w-5 mr-2'}><FolderOpenIcon/></span>
                        <span
                            className={'bg-gradient-to-r from-red-500 to-green-500 inline-block text-transparent bg-clip-text'}
                        >
                        View Datasets
                        </span>

                    </RouterLink>
                    <RouterLink
                        to={'/post'}
                        className={'flex flex-row items-center p-2 border-2 border-r-4 hover:border-amber-400 border-purple-500 rounded-md'}>
                        <span className={'h-5 w-5 mr-2'}><FolderOpenIcon/></span>
                        <span
                            className={'bg-gradient-to-r from-red-500 to-green-500 inline-block text-transparent bg-clip-text'}
                        >View Dataset Posts</span>
                    </RouterLink>
                </div>
            </div>


            <div className={'container mx-auto max-w-screen-xl mt-6 px-4'}>
                {main || <div>
                    You can edit this welcome message by following this tutorial.
                </div>}
            </div>


        </div>
    </>
}