import React, {ReactNode, useRef, useEffect} from 'react';

interface ScrollableComponentProps {
    children: ReactNode;
}

export function ScrollableComponent({children}: ScrollableComponentProps) {
    const contentRef = useRef<HTMLDivElement>(null);
    const topScrollbarRef = useRef<HTMLDivElement>(null);
    const bottomScrollbarRef = useRef<HTMLDivElement>(null);

    // Synchronize the scroll position of the top scrollbar with the main content
    const syncScroll = (source: HTMLDivElement, target: HTMLDivElement) => {
        if (target && source.scrollLeft !== target.scrollLeft) {
            target.scrollLeft = source.scrollLeft;
        }
    };

    // Attach scroll event listener to sync scroll positions
    useEffect(() => {
        const contentElement = contentRef.current;
        const topScrollbarElement = topScrollbarRef.current;
        const bottomScrollbarElement = bottomScrollbarRef.current;

        const handleScroll = () => {
            if (contentElement && topScrollbarElement && bottomScrollbarElement) {
                syncScroll(contentElement, topScrollbarElement);
                syncScroll(contentElement, bottomScrollbarElement);
            }
        };

        contentElement?.addEventListener('scroll', handleScroll);

        return () => {
            contentElement?.removeEventListener('scroll', handleScroll);
        };
    }, []);

    return (
        <div>
            <div ref={topScrollbarRef} className="overflow-x-scroll" aria-hidden="true">
                <div className="h-px" style={{width: `2000px`}}/>
            </div>
            <div ref={contentRef} className="overflow-x-scroll">
                <div className={'bg-gradient-to-r from-pink-50 to-teal-600 h-52 w-[2000px] mx-4'}></div>
            </div>
            <div ref={bottomScrollbarRef} className="overflow-x-scroll" aria-hidden="true">
                <div className="h-px" style={{width: `2000px`}}/>
            </div>
        </div>
    );
}
