import React, {useEffect, useRef} from 'react';


export function useClickOutsideRef(props: {
    onOutsideClick: () => void
}) {
    const ref = useRef<any>(null); // Step 1: Create a ref for your element

    // Step 2: Attach event listener
    useEffect(() => {
        function handleClickOutside(event: any) {
            if (ref.current && !ref.current.contains(event.target)) {
                // Call the function passed in props if a click outside is detected
                props.onOutsideClick();
            }
        }

        // Attach the event listener
        document.addEventListener('mousedown', handleClickOutside);

        // Step 3: Remove event listener on cleanup
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, [props]); // Ensure the effect runs only once or when props change
    return ref;
}

function OutsideClickListener({onOutsideClick, children}: {
    children: React.ReactNode,
    onOutsideClick: () => void
}) {
    const ref = useClickOutsideRef({onOutsideClick}); // Ensure the effect runs only once or when props change

    return <div ref={ref}>{children}</div>; // Attach the ref to your element
}

export default OutsideClickListener;
