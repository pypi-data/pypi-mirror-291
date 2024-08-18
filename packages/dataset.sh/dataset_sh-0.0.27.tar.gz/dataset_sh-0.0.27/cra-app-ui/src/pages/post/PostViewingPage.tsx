import {useQuery} from "@tanstack/react-query";
import {Features, OtherHooks, PostHooks} from "../../features";

import React from "react";
import {PostViewer} from "../../components/posts/PostViewer";
import {Link as RouterLink, useParams} from "react-router-dom";
import {Helmet} from "react-helmet-async";


function slugToTitle(slug: string): string {
    // Split the slug into words by '-'
    const words = slug.split('-');

    // Capitalize the first letter of each word
    const capitalizedWords = words.map((word) => {
        return word.charAt(0).toUpperCase() + word.slice(1);
    });

    // Join the words to form the title
    const title = capitalizedWords.join(' ');

    return title;
}


export function PostViewingPage() {
    const {postName} = useParams();

    const contentQuery = PostHooks.usePost(postName!)
    const hostnameLoader = OtherHooks.useHostName()

    const hostName = hostnameLoader.data?.data.hostname || 'your-hostname'

    let main;

    if (contentQuery.status === 'loading') {
        main = <div>
            <div>Loading content.</div>
        </div>
    } else if (contentQuery.status === 'success') {
        main = <div>
            <PostViewer
                post={contentQuery.data.data} projectName={postName!}
                hostName={hostName}/>
        </div>
    } else {
        main = <div>
            <div>Something went wrong, please check log.</div>
        </div>
    }

    return <>

    <Helmet>
            <title> {postName} | dataset.sh </title>
        </Helmet>

        <div className={'container mx-auto max-w-screen-xl mt-8 px-4'}>

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
                            <RouterLink to={'/post'}
                                        className="ms-1 text-sm font-medium text-gray-500 md:ms-2">Post</RouterLink>
                        </div>
                    </li>

                    <li aria-current="page">
                        <div className="flex items-center">
                            <svg className="rtl:rotate-180 w-3 h-3 text-gray-400 mx-1" aria-hidden="true"
                                 xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 6 10">
                                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"
                                      stroke-width="2" d="m1 9 4-4-4-4"/>
                            </svg>
                            <RouterLink to={`/post/${postName}`}
                                        className="ms-1 text-sm font-medium text-gray-800 md:ms-2">{slugToTitle(postName!)}</RouterLink>
                        </div>
                    </li>

                </ol>
            </nav>

            <div className={'mt-8'}>
                {main}
            </div>

        </div>
    </>

}