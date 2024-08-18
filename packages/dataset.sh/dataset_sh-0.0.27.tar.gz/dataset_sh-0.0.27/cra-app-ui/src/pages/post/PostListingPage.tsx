import {useQuery} from "@tanstack/react-query";
import {Features, PostHooks} from "../../features";
import React from "react";
import {Link as RouterLink, useLocation, useParams} from "react-router-dom";
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


export function PostListingPage() {
    const postListingQuery = PostHooks.usePostListing()

    let main;
    if (postListingQuery.status === 'loading') {
        main = <div>

        </div>
    } else if (postListingQuery.status === 'success') {
        main = <div>
            {postListingQuery.data?.data.items.map(item => {
                return <div key={item.name} className={'mb-2'}>
                    <RouterLink
                        className={'underline underline-offset-4 '}
                        to={`/post/${item.name}`}>
                        {slugToTitle(item.name)}
                    </RouterLink>
                </div>
            })}
        </div>
    } else {
        main = <div>
        </div>
    }

    return <>

        <Helmet>
            <title> articles | dataset.sh </title>
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
                            <RouterLink to={'/dataset'}
                                        className="ms-1 text-sm font-medium text-gray-800 md:ms-2">Post</RouterLink>
                        </div>
                    </li>
                </ol>
            </nav>

            <div className={'heading font-bold text-4xl my-4 text-slate-600 underline underline-offset-8 mb-4'}>
                POSTS:
            </div>


            <div className={'mt-8'}>
                {main}
            </div>

        </div>
    </>

}