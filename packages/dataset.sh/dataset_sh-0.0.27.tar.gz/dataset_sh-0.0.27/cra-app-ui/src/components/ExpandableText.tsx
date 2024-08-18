import React, {useMemo, useState} from 'react';

interface ExpandableTextProps {
    text: string;
    maxLength: number;
}

const ExpandableText: React.FC<ExpandableTextProps> = ({text, maxLength}) => {
    const [isExpanded, setIsExpanded] = useState(false);
    const toggleExpansion = () => {
        setIsExpanded(isExpanded => !isExpanded);
    };

    const truncatedText = useMemo(() => {
        const truncated = text.split('\n')[0].slice(0, 50)
        if (truncated === text) {
            return truncated
        } else {
            return truncated + '...'
        }
    }, [text])

    const showButton = useMemo(() => {
        return truncatedText !== text
    }, [truncatedText, text])

    return (
        <div className={''}>
            {!isExpanded && showButton && (
                <button
                    onClick={toggleExpansion}
                    className="text-sm font-bold text-blue-500 hover:underline cursor-pointer"
                >
                    Read more
                </button>
            )}

            {isExpanded && showButton && (
                <button
                    onClick={toggleExpansion}
                    className="text-sm font-bold text-red-600 hover:underline cursor-pointer"
                >
                    Read less
                </button>
            )}
            <div
                className={` ${isExpanded ? 'whitespace-pre-line' : 'w-[350px]'}`}
            >
                {isExpanded ? text : truncatedText}
            </div>

        </div>
    );
};

export default ExpandableText;
