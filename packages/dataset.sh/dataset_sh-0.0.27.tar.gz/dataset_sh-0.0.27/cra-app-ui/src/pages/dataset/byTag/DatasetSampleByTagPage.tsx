import {useNavigate, useParams} from "react-router-dom";
import React from "react";
import {Helmet} from "react-helmet-async";
import {DatasetTagHooks} from "../../../features";
import {CollectionDocumentViewer} from "../../../components/dataset/collection/CollectionDocumentViewer";
import {StandaloneCollectionSelector} from "../../../components/dataset/collection/StandaloneCollectionSelector";
import {QueryDisplay} from "../../../components/QueryDisplay";


export function DatasetSampleByTagPage() {
    const navigate = useNavigate();
    const {namespace, datasetName, tag, collName} = useParams();

    const datasetInfoQuery = DatasetTagHooks.useDatasetMetaByTag(namespace!, datasetName!, tag!)
    const collMetaQuery = DatasetTagHooks.useDatasetSampleByTag(namespace!, datasetName!, tag!, collName!)


    // const collections = metaLoader.data?.data.collections || []
    // const selectedCollection = metaLoader.data?.data.collections.find(x => x.name === collName)
    const baseUrl = `/dataset/${namespace}/${datasetName}/tag/${tag}`

    return <div>
        <Helmet>
            <title> {collName} of {namespace}/{datasetName}:{tag} | dataset.sh </title>
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
                            tag={tag}
                        />}
                    </div>
                </div>
            }}/>
        }}/>


        {/*<div className={'mt-4 container-lg mx-auto max-w-screen-xl'}>*/}
        {/*    <StandaloneCollectionSelector*/}
        {/*        baseUrl={baseUrl}*/}
        {/*        collectionNames={collections.map(c => c.name)}*/}
        {/*        currentCollection={collName!}*/}
        {/*    />*/}
        {/*</div>*/}
        {/*<div className={'pt-4 mx-auto container max-w-screen-xl pb-32'}>*/}
        {/*    {(sampleDataLoader.data && collName && selectedCollection) && <CollectionDocumentViewer*/}
        {/*        namespace={namespace!}*/}
        {/*        datasetName={datasetName!}*/}
        {/*        tag={tag}*/}
        {/*        collectionConfig={selectedCollection}*/}
        {/*    />}*/}
        {/*</div>*/}

    </div>
}
