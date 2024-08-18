import {useNavigate, useParams} from "react-router-dom";
import {DatasetVersionHooks} from "../../../features";
import React from "react";
import {Helmet} from "react-helmet-async";
import {CollectionDocumentViewer} from "../../../components/dataset/collection/CollectionDocumentViewer";
import {StandaloneCollectionSelector} from "../../../components/dataset/collection/StandaloneCollectionSelector";
import {QueryDisplay} from "../../../components/QueryDisplay";


export function DatasetSampleByVersionPage() {
    const navigate = useNavigate();
    const {namespace, datasetName, version, collName} = useParams();


    const datasetInfoQuery = DatasetVersionHooks.useDatasetMetaByVersion(namespace!, datasetName!, version!)
    const collMetaQuery = DatasetVersionHooks.useDatasetSampleByVersion(namespace!, datasetName!, version!, collName!)

    // const collections = metaLoader.data?.data.collections || []
    // const selectedCollection = metaLoader.data?.data.collections.find(x => x.name === collName)
    const baseUrl = `/dataset/${namespace}/${datasetName}/version/${version}`

    return <div>


        <Helmet>
            <title> {collName} of {namespace}/{datasetName}:{version} | dataset.sh </title>
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
                            version={version}
                        />}
                    </div>
                </div>
            }}/>
        }}/>

        {/*<div className={'px-1 mt-4 container-lg mx-auto max-w-screen-xl'}>*/}
        {/*    <StandaloneCollectionSelector*/}
        {/*        baseUrl={baseUrl}*/}
        {/*        collectionNames={collections.map(c => c.name)}*/}
        {/*        currentCollection={collName!}*/}
        {/*    />*/}

        {/*</div>*/}
        {/*<div className={'px-1 pt-4 mx-auto container max-w-screen-xl pb-32'}>*/}
        {/*    {(sampleDataLoader.data && collName && selectedCollection) && <CollectionDocumentViewer*/}
        {/*        namespace={namespace!}*/}
        {/*        datasetName={datasetName!}*/}
        {/*        version={version}*/}
        {/*        collectionConfig={selectedCollection}*/}
        {/*    />}*/}
        {/*</div>*/}

    </div>
}
