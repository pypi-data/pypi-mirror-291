import {
    CollectionConfig,
    DatasetLatestTagHooks,
    DatasetTagHooks, DatasetVersionHooks,
    Features,
    getMainEntryPointClass
} from "../../../features";
import {useQuery} from "@tanstack/react-query";
import {LightCodeBlock} from "../../CodeBlock";
import React from "react";

function downloadCommand({
                             namespace, datasetName, version, tag
                         }: {
    namespace: string,
    datasetName: string,
    version?: string
    tag?: string
}) {

    if (version) {
        return `with dsh.dataset('${namespace}/${datasetName}').version('${version}').open() as reader:`
    } else if (tag) {
        return `with dsh.dataset('${namespace}/${datasetName}').tag('${tag}').open() as reader:`
    } else {
        return `with dsh.dataset('${namespace}/${datasetName}').latest().open() as reader:`
    }

}

export function SchemaCodeViewer(props: {
    collectionName: string, namespace: string,
    datasetName: string,
    collectionConfig?: CollectionConfig,
    code: string,
    version?: string
    tag?: string
}) {
    const {version, tag, collectionName, code, namespace, datasetName, collectionConfig} = props;

    const mainClzSchema = collectionConfig && getMainEntryPointClass(collectionConfig.data_schema)
    const readerLine = downloadCommand({namespace, datasetName, version, tag})
    let importCode = ''
    if (mainClzSchema?.name) {
        const parts = mainClzSchema?.name.split('.')
        const clzName = parts[parts?.length - 1]
        importCode = `import dataset_sh as dsh
${readerLine}
    print(reader.collections())
    for item in reader.coll('${collectionName}', model=${clzName}):
        print(item)
        break
`
    } else {
        importCode = `import dataset_sh as dsh
${readerLine}
    print(reader.collections())
    for item in reader.coll('${collectionName}'):
        print(item)
        break
`
    }


    return <>
        {
            <div className={'mt-2'}>
                <LightCodeBlock code={code} language={'python'}
                                title={`Data Models for ${collectionName}`}/>
            </div>
        }

        {
            <div className={'mt-2'}>
                <LightCodeBlock language={'python'} code={importCode} title={`Read Data`}/>
            </div>
        }
    </>
}

export function ConnectedSchemaCodeViewer({
                                              namespace, datasetName, collectionName,
                                              tag, version, collectionConfig
                                          }: {
    namespace: string,
    datasetName: string,
    tag?: string,
    version?: string,
    collectionName: string,
    collectionConfig?: CollectionConfig
}) {
    if (version) {
        return <ConnectedSchemaCodeViewerForVersion
            namespace={namespace}
            datasetName={datasetName}
            version={version}
            collectionName={collectionName}
            collectionConfig={collectionConfig}
        />
    } else if (tag) {
        return <ConnectedSchemaCodeViewerForTag
            namespace={namespace}
            datasetName={datasetName}
            tag={tag}
            collectionName={collectionName}
            collectionConfig={collectionConfig}

        />
    } else {
        return <ConnectedSchemaCodeViewerForLatest
            namespace={namespace}
            datasetName={datasetName}
            collectionName={collectionName}
            collectionConfig={collectionConfig}
        />
    }
}

export function ConnectedSchemaCodeViewerForTag({
                                                    namespace, datasetName, collectionName,
                                                    tag, collectionConfig
                                                }: {
    namespace: string, datasetName: string, tag: string, collectionName: string, collectionConfig?: CollectionConfig
}) {
    const codeLoader = DatasetTagHooks.useDatasetCodeExampleByTag(namespace, datasetName, tag, collectionName);
    return <>
        {codeLoader.data && <SchemaCodeViewer
            namespace={namespace}
            datasetName={datasetName}
            collectionName={collectionName}
            collectionConfig={collectionConfig}
            code={codeLoader.data?.data.code}
            tag={tag}
        />}
    </>
}

export function ConnectedSchemaCodeViewerForVersion({
                                                        namespace, datasetName, collectionName,
                                                        version, collectionConfig
                                                    }: {
    namespace: string,
    datasetName: string,
    version: string,
    collectionName: string,
    collectionConfig?: CollectionConfig
}) {
    const codeLoader = DatasetVersionHooks.useDatasetCodeExampleByVersion(namespace, datasetName, version, collectionName);
    return <>
        {codeLoader.data && <SchemaCodeViewer
            namespace={namespace}
            datasetName={datasetName}
            collectionName={collectionName}
            collectionConfig={collectionConfig}
            code={codeLoader.data?.data.code}
            version={version}
        />}
    </>

}

export function ConnectedSchemaCodeViewerForLatest({
                                                       namespace, datasetName, collectionName, collectionConfig
                                                   }: {
    namespace: string, datasetName: string, collectionName: string, collectionConfig?: CollectionConfig
}) {
    const codeLoader = DatasetLatestTagHooks.useLatestDatasetCodeExample(namespace, datasetName, collectionName);
    return <>
        {codeLoader.data && <SchemaCodeViewer
            namespace={namespace}
            datasetName={datasetName}
            collectionName={collectionName}
            collectionConfig={collectionConfig}
            code={codeLoader.data?.data.code}
        />}
    </>

}
