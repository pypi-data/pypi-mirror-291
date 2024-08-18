import React from 'react';
import {UseQueryResult} from "@tanstack/react-query";
import {Link, useLocation} from "react-router-dom";

export function ReloadOrLoginMsg() {

    const pathname = useLocation().pathname;

    return <div>
        <div className={'p-4 bg-red-50 m-4'}>
            <h2 className={'font-bold text-3xl text-red-400 pb-2'}>
                Something went wrong!
            </h2>
            <div>
                You may want to <button
                className={'underline text-yellow-800'}
                onClick={() => {

                    location.reload()
                }}>
                reload this page
            </button> or try <Link
                className={'underline text-blue-600'}
                to={`/login?redirect=${pathname}`}>login again</Link>.
            </div>
        </div>
    </div>
}

export function LoadingMessage() {
    return <div>
        {/*Loading...*/}
        <div
            className="m-12 inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-current border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]"
            role="status">
    <span
        className="!absolute !-m-px !h-px !w-px !overflow-hidden !whitespace-nowrap !border-0 !p-0 ![clip:rect(0,0,0,0)]"
    >Loading...</span>
        </div>
    </div>
}

interface QueryDisplayProps<T> {
    queryResult: UseQueryResult<T>;
    onSuccess: (data: T) => React.ReactElement;
}

export const QueryDisplay = <T, >({queryResult, onSuccess}: QueryDisplayProps<T>) => {
    const {isError, isLoading, data, error} = queryResult;

    if (isError) {
        console.log(error)
        return <ReloadOrLoginMsg/>;
    }

    if (isLoading) {
        return <LoadingMessage/>;
    }

    if (data) {
        return onSuccess(data);
    }

    return <>
    </>;
};

