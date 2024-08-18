import React, {useEffect, useRef, useState} from 'react';
import ExpandableText from "./ExpandableText";
import {
    ArrowUpOnSquareIcon,
    ChevronDoubleLeftIcon,
    ChevronDoubleRightIcon
} from '@heroicons/react/24/outline'
import {Link} from "react-router-dom";

function joinStrings(...items: string[]): string {
    return items.join(" ");
}


export function SmartTextView({text, minimize}: { text: string, minimize: boolean }) {
    const lines = text.split('\n')
    const numOfLines = lines.length
    const width = lines.map(line => line.length)
    const maxWidth = Math.max(...width)
    if (text.length > 4000 || minimize) {
        return <ExpandableText text={text} maxLength={4000}/>
    } else if (maxWidth > 80) {
        return <span
            className={'whitespace-pre-line'}
        >
            {text}
        </span>

    } else if (numOfLines > 4) {
        return <span
            className={'whitespace-pre'}
        >
            {text}
        </span>
    }

    return <span
        className={'whitespace-pre'}
    >
        {text}
    </span>
}

export function CollectionViewer(props: {
    items: Record<string, any>[],
    keys: string[],
}) {
    const {items, keys} = props;
    const tableContainerRef = useRef<HTMLTableElement>(null);
    const [width, setWidth] = useState(0); // State to store the width

    const refTop = useRef<HTMLDivElement>(null);


    const refInner = useRef<HTMLDivElement>(null);

    const [minimize, setMinimize] = useState(true)
    const syncScroll = (sourceRef: any, targetRef: any) => {
        let isUserScrolling = true;

        const sync = () => {
            if (isUserScrolling) {
                const scrollPercentage = sourceRef.current.scrollLeft / sourceRef.current.scrollWidth;
                targetRef.current.scrollLeft = scrollPercentage * targetRef.current.scrollWidth;
            }
            isUserScrolling = true; // Reset after the scroll has been synced
        };

        sourceRef.current.addEventListener('scroll', sync);
        return () => sourceRef.current.removeEventListener('scroll', sync);
    };

    useEffect(() => {
        // Ensure the div element is mounted
        if (tableContainerRef.current) {
            setWidth(tableContainerRef.current.offsetWidth); // Update the width state with the div's offsetWidth
        }
    }, []); // Empty dependency array means this effect runs once on mount
    useEffect(() => {
        // Synchronize scroll of content with top scrollbar
        const syncContentWithTop = () => {
            if (refInner.current && refTop.current) {
                const contentScrollWidth = refInner.current.scrollWidth;
                const topScrollWidth = refTop.current.scrollWidth;

                let isUserScrolling = true;

                // Sync top scroll to content
                const syncTopToContent = () => {
                    if (isUserScrolling) {

                        // @ts-ignore
                        refTop.current.scrollLeft = refInner.current?.scrollLeft;

                    }
                    isUserScrolling = true;
                };

                // Sync content to top scroll
                const syncContentToTop = () => {
                    isUserScrolling = false; // Prevent syncing back to the top scroll
                    // @ts-ignore
                    refInner.current.scrollLeft = refTop.current?.scrollLeft;
                };

                refTop.current?.addEventListener('scroll', syncContentToTop);
                refInner.current?.addEventListener('scroll', syncTopToContent);

                return () => {
                    refTop.current?.removeEventListener('scroll', syncContentToTop);
                    refInner.current?.removeEventListener('scroll', syncTopToContent);
                };
            }
        };

        const removeListeners = syncContentWithTop();
        return () => {
            if (removeListeners) {
                removeListeners();
            }
        };
    }, []);


    let main =
        <table className="overflow-x-scroll divide-y divide-gray-300 m-1 border-t border-gray-300"
               ref={tableContainerRef}>

            <thead>
            <tr>
                {keys.map((key) => (
                    <th key={key}
                        className="py-3.5 pl-8 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-8 border-r "
                    >{key}</th>
                ))}
            </tr>
            </thead>
            <tbody>
            {items.map((item, index) => (
                <tr

                    className={joinStrings("even:bg-gray-100", minimize ? 'h-1' : '')}
                    key={index}>
                    {keys.map((kn, idx) => {
                        const kv = item[kn];
                        if (kv !== undefined && kv !== null) {
                            if (typeof kv === 'string') {
                                return <td key={kn}
                                           className={joinStrings(' px-8 max-w-[30em]', minimize ? 'py-2 h-1' : 'py-4')}>
                                    <SmartTextView
                                        minimize={minimize}
                                        text={kv}
                                    />
                                </td>
                            }
                            return <td
                                className={joinStrings('overflow-y-auto px-8 min-w-[30em]', minimize ? 'py-2 h-1' : 'py-4')}
                                key={kn}>
                                <SmartTextView minimize={minimize}
                                               text={JSON.stringify(kv, null, 2)}
                                />
                            </td>
                        } else {
                            return <td key={kn}></td>
                        }

                    })}
                </tr>
            ))}


            </tbody>
        </table>

    return <>
        <div className="space-y-2 w-full border border-gray-200 mt-2">
            <div className="overflow-x-scroll" ref={refTop}
            >
                <div className="h-2" style={{width: width}}/>
            </div>

            <div
                ref={refInner} className={joinStrings('overflow-x-auto', minimize ? 'max-h-[50em]' : '')}
            >
                {main}
            </div>
            {/*<div className="px-4 pb-1 font-bold text-gray-600 text-sm">*/}
            {/*    <a href="#download">Download to see more.</a>*/}
            {/*</div>*/}
            <div className="px-4 pb-1 font-bold text-orange-800 text-sm">
                <span>Showing only {items.length} items, download to see more.</span>
            </div>

            {/*<div className="overflow-x-scroll bg-gradient-to-r from-red-100 to-blue-800" ref={refBottom}*/}
            {/*>*/}
            {/*    <div className="h-2" style={{width: width}}/>*/}
            {/*</div>*/}
        </div>
    </>

}
