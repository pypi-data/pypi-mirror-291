import {useNavigate, useParams} from "react-router-dom";
import {DatasetLatestTagHooks} from "../../features";
import React from "react";
import {Helmet} from "react-helmet-async";
import {StandaloneCollectionSelector} from "../../components/dataset/collection/StandaloneCollectionSelector";
import {CollectionDocumentViewer} from "../../components/dataset/collection/CollectionDocumentViewer";
import {QueryDisplay} from "../../components/QueryDisplay";
import {useQuery} from "@tanstack/react-query";


export function DatasetSamplePage() {
    const navigate = useNavigate();
    const {namespace, datasetName, collName} = useParams();

    const datasetInfoQuery = DatasetLatestTagHooks.useLatestDatasetMeta(namespace!, datasetName!)
    const collMetaQuery = DatasetLatestTagHooks.useLatestDatasetSample(namespace!, datasetName!, collName!)

    const baseUrl = `/dataset/${namespace}/${datasetName}`

    return <div>


        <Helmet>
            <title> {collName} of {namespace}/{datasetName} | dataset.sh </title>
        </Helmet>

        <QueryDisplay queryResult={datasetInfoQuery} onSuccess={info => {
            return <QueryDisplay queryResult={collMetaQuery} onSuccess={collMeta => {
                const selectedCollection = info.data.collections.find(x => x.name === collName)

                return <div>
                    <div className={'mt-4 container-lg mx-auto max-w-screen-xl'}>
                        <StandaloneCollectionSelector
                            baseUrl={baseUrl}
                            collectionNames={info.data.collections.map(c => c.name)}
                            currentCollection={collName!}
                        />
                    </div>
                    <div className={'pt-4 mx-auto container max-w-screen-xl pb-32'}>
                        {selectedCollection && <CollectionDocumentViewer
                            namespace={namespace!}
                            datasetName={datasetName!}
                            collectionConfig={selectedCollection}
                        />}
                    </div>
                </div>
            }}/>
        }}/>

    </div>
}
