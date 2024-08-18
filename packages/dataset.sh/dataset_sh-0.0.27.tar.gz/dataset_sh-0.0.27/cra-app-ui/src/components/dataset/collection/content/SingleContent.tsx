import React from "react";
import {SingleSelectedView} from "../selected/SelectedView";
import {QueryEditor} from "../query/QueryEditor";
import {QueryResultSelector} from "../query/QueryResult";

export function SingleContent(
    {
        selected,
        setSelected,
        query,
        setQuery,
        filteredCollectionNames,
        oneCollMode
    }:
        {
            oneCollMode: boolean,
            selected: string[],
            setSelected: (q: string[]) => void,
            query: string,
            setQuery: (q: string) => void,
            filteredCollectionNames: string[]
        }
) {
    const addSelected = (itemToAdd: string) => {
        // Prevent adding duplicates
        if (!selected.includes(itemToAdd)) {
            setSelected([...selected, itemToAdd]);
        }
    };
    return <div>
        <SingleSelectedView setSelected={setSelected} selected={selected}/>
        <QueryEditor setQuery={setQuery} query={query}/>
        <QueryResultSelector
            addSelected={addSelected}
            setSelected={setSelected}
            filteredCollectionNames={filteredCollectionNames}
            oneCollMode={oneCollMode}
        />
    </div>
}
