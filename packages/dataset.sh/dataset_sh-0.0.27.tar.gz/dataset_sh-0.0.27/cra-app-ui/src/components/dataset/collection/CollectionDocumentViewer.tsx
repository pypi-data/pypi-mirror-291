import {
    CollectionConfig,
    DatasetLatestTagHooks,
    DatasetTagHooks,
    DatasetVersionHooks
} from "../../../features";
import {ConnectedSchemaCodeViewer} from "../meta/SchemaVodeViewer";
import React from "react";
import {CollectionSampleViewer} from "../sample/CollectionSampleViewer";
import {Link} from "react-router-dom";


function ConnectedSampleViewer({
                                   namespace,
                                   datasetName,
                                   collectionConfig,
                                   tag, version,
                                   showLink
                               }:
                                   {
                                       namespace: string,
                                       datasetName: string,
                                       collectionConfig: CollectionConfig,
                                       showLink: boolean,
                                       tag?: string, version?: string
                                   }) {
    if (tag) {
        return <ConnectedSampleViewerForTag showLink={showLink} tag={tag} collectionConfig={collectionConfig}
                                            datasetName={datasetName}
                                            namespace={namespace}/>
    } else if (version) {
        return <ConnectedSampleViewerForVersion
            showLink={showLink}
            collectionConfig={collectionConfig} datasetName={datasetName}
            namespace={namespace} version={version}
        />
    } else {
        return <ConnectedSampleViewerForLatest showLink={showLink} collectionConfig={collectionConfig}
                                               datasetName={datasetName}
                                               namespace={namespace}/>
    }

}

function ConnectedSampleViewerForTag({
                                         namespace,
                                         datasetName,
                                         collectionConfig, showLink,
                                         tag

                                     }:
                                         {
                                             namespace: string,
                                             datasetName: string,
                                             collectionConfig: CollectionConfig,
                                             showLink: boolean,
                                             tag: string
                                         }) {
    const sampleDataLoader = DatasetTagHooks.useDatasetSampleByTag(namespace!, datasetName!, tag!, collectionConfig.name)
    const baseUrl = `/dataset/${namespace}/${datasetName}/tag/${tag}`

    return <div>
        {sampleDataLoader.data && <CollectionSampleViewer
            showLink={showLink}
            collectionUrl={`${baseUrl}/collection/${collectionConfig.name}`}
            collectionName={collectionConfig.name}
            collectionConfig={collectionConfig} sampleData={sampleDataLoader.data.data}
        />}
    </div>
}

function ConnectedSampleViewerForVersion({
                                             namespace,
                                             datasetName,
                                             collectionConfig, showLink,
                                             version
                                         }:
                                             {
                                                 namespace: string,
                                                 datasetName: string,
                                                 collectionConfig: CollectionConfig,
                                                 showLink: boolean,
                                                 version: string
                                             }) {
    const sampleDataLoader = DatasetVersionHooks.useDatasetSampleByVersion(namespace!, datasetName!, version!, collectionConfig.name)
    const baseUrl = `/dataset/${namespace}/${datasetName}/version/${version}`

    return <div>
        {sampleDataLoader.data && <CollectionSampleViewer
            showLink={showLink}
            collectionUrl={`${baseUrl}/collection/${collectionConfig.name}`}
            collectionName={collectionConfig.name}
            collectionConfig={collectionConfig} sampleData={sampleDataLoader.data.data}
        />}
    </div>
}

function ConnectedSampleViewerForLatest({
                                            namespace,
                                            datasetName,
                                            collectionConfig,
                                            showLink,
                                        }:
                                            {
                                                namespace: string,
                                                datasetName: string,
                                                showLink: boolean,
                                                collectionConfig: CollectionConfig,
                                            }) {
    const sampleDataLoader = DatasetLatestTagHooks.useLatestDatasetSample(namespace!, datasetName!, collectionConfig.name)
    const baseUrl = `/dataset/${namespace}/${datasetName}`

    return <div>
        {sampleDataLoader.data && <CollectionSampleViewer
            showLink={showLink}
            collectionUrl={`${baseUrl}/collection/${collectionConfig.name}`}
            collectionName={collectionConfig.name}
            collectionConfig={collectionConfig} sampleData={sampleDataLoader.data.data}
        />}
    </div>
}


export function CollectionDocumentViewer(
    {
        namespace,
        datasetName,
        collectionConfig,
        tag, version,
        hideLink,
        idx
    }: {
        namespace: string,
        datasetName: string,
        collectionConfig: CollectionConfig,
        tag?: string,
        version?: string,
        hideLink?: boolean,
        idx?: number
    }) {

    const showLink = !hideLink;
    return <div
        key={collectionConfig.name}
        className="mt-12 pl-4"
    >
        <Link className={"text-xl font-bold underline pt-12 -ml-4"}
              id={`collection-${collectionConfig.name}`}
              to={`#collection-${collectionConfig.name}`}>
            {
                (idx !== null && idx !== undefined) && <span>{idx + 1}.</span>
            } Collection: {collectionConfig.name}
        </Link>

        <div className={'mt-4'}>
            <ConnectedSampleViewer
                namespace={namespace} datasetName={datasetName}
                collectionConfig={collectionConfig}
                tag={tag} version={version}
                showLink={showLink}
            />
        </div>

        <div
            className={'px-2 py-2 my-2'}
        >After downloading this dataset, you can use the following code to read the
            collection {collectionConfig.name}.
        </div>


        {collectionConfig && <>
            <ConnectedSchemaCodeViewer
                namespace={namespace}
                datasetName={datasetName}
                tag={tag} version={version}
                collectionName={collectionConfig.name}
                collectionConfig={collectionConfig}
            />
        </>}
    </div>

}