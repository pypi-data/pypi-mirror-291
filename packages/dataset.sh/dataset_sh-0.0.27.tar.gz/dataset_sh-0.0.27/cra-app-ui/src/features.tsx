import axios from "axios";
import {useQuery} from "@tanstack/react-query";

export type FieldDefinition = {
    name: string
    type: any
}
export type ClassDefinition = {
    name: string
    fields: FieldDefinition[]
}
export type EnumDefinition = {
    name: string
    enum_entries: any[]
}
export type ClassOrEnumDefinition = ClassDefinition | EnumDefinition

export type DatasetSchema = {
    entry_point: string
    classes: ClassOrEnumDefinition[]
}

export function getMainEntryPointClass(schema: DatasetSchema) {
    return schema.classes.find(c => c.name === schema.entry_point) as (ClassDefinition | undefined)
}

export type CollectionConfig = {
    name: string
    data_format: 'jsonl'
    data_schema: DatasetSchema
    entry_model: string
}

export type DatasetMeta = {
    author?: string
    authorEmail?: string
    description?: string
    collections: CollectionConfig[]
    createdAt: number
    fileSize: number
}

export type DatasetMetaList = {
    items: {
        namespace: string,
        dataset: string,
        readme: string
    }[]
}

export type DatasetSample = Record<string, any>[]

export type CodeSample = {
    code: string
}

const axiosInstance = axios.create({});

axiosInstance.interceptors.request.use(
    (config) => {
        // You can add any request-specific logic here
        return config;
    },
    (error) => {
        // Handle request errors here
        return Promise.reject(error);
    }
);


axiosInstance.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        if (error.response) {
            if (error.response.status === 401) {
                window.location.href = '/login';
            }
            console.error('Response Error:', error.response.status, error.response.data);
        } else if (error.request) {
            console.error('Request Error:', error.request);
        } else {
            console.error('General Error:', error.message);
        }
        return Promise.reject(error);
    }
);


export const Features = {
    async login(username: string, password: string) {
        return axiosInstance.post('/api/login', {username, password})
    },

    async logout() {
        return axiosInstance.post('/api/logout')
    },

    async listDatasets() {
        return axiosInstance.get<DatasetMetaList>('/api/dataset')
    },


    getDatasetDownloadUrl(userName: string, datasetName: string) {
        return `/api/dataset/${userName}/${datasetName}/file`
    },


    listDatasetsForStore(userName: string) {
        return axiosInstance.get<DatasetMetaList>(`/api/dataset/${userName}`)
    },
}

export const datasetHooks = {}

export const OtherHooks = {
    useHostName() {
        return useQuery({
            queryKey: ['hostname'], queryFn: async () => {
                return axiosInstance.get<{ hostname: string }>(`/api/hostname`)
            }
        })
    }
}

export type VersionListing = {
    items: { version: string }[]
}

export type TagListing = {
    items: { tag: string, version: string }[]
}

export const DatasetLatestTagHooks = {
    useLatestDatasetMeta(userName: string, datasetName: string) {
        return DatasetTagHooks.useDatasetMetaByTag(userName, datasetName, 'latest')
    },

    useLatestDatasetSample(userName: string, datasetName: string, collName: string) {
        return DatasetTagHooks.useDatasetSampleByTag(userName, datasetName, 'latest', collName)
    },

    useLatestDatasetCodeExample(userName: string, datasetName: string, collName: string) {
        return DatasetTagHooks.useDatasetCodeExampleByTag(userName, datasetName, 'latest', collName)
    },
    useLatestDownloadCode(userName: string, datasetName: string, lang: string) {
        return DatasetTagHooks.useDownloadCodeByTag(userName, datasetName, 'latest', lang)

    },
}

export const DatasetTagHooks = {
    useDatasetTags(userName: string, datasetName: string) {
        return useQuery({
            queryKey: ['dataset', userName, datasetName, 'tag'],
            queryFn: async () => {
                return axiosInstance.get<TagListing>(`/api/dataset/${userName}/${datasetName}/tag`)
            }
        })
    },

    useDatasetMetaByTag(userName: string, datasetName: string, tag: string) {
        return useQuery({
            queryKey: ['dataset', userName, datasetName, 'tag', tag, 'meta'],
            queryFn: async () => {
                return axiosInstance.get<DatasetMeta>(`/api/dataset/${userName}/${datasetName}/tag/${tag}/meta`)
            }
        })
    },

    useDownloadCodeByTag(userName: string, datasetName: string, tag: string, lang: string) {
        return useQuery({
            queryKey: ['dataset', userName, datasetName, 'tag', tag, 'download-code', lang],
            queryFn: async () => {
                return axiosInstance.get<{
                    code: string
                }>(`/api/dataset/${userName}/${datasetName}/tag/${tag}/download-code?lang=${lang}`)
            }
        })
    },

    useDatasetSampleByTag(userName: string, datasetName: string, tag: string, collName: string) {
        return useQuery({
            queryKey: ['dataset', userName, datasetName, 'tag', tag, 'coll', collName, 'sample'],
            queryFn: async () => {
                return axiosInstance.get<DatasetSample>(`/api/dataset/${userName}/${datasetName}/tag/${tag}/collection/${collName}/sample`)
            }
        })
    },

    useDatasetCodeExampleByTag(userName: string, datasetName: string, tag: string, collName: string) {
        return useQuery({
            queryKey: ['dataset', userName, datasetName, 'tag', tag, 'coll', collName, 'code'],
            queryFn: async () => {
                return axiosInstance.get<CodeSample>(`/api/dataset/${userName}/${datasetName}/tag/${tag}/collection/${collName}/code`)
            }
        })
    }
}


export const DatasetVersionHooks = {
    useDatasetVersions(userName: string, datasetName: string) {
        return useQuery({
            queryKey: ['dataset', userName, datasetName, 'version'],
            queryFn: async () => {
                return axiosInstance.get<VersionListing>(`/api/dataset/${userName}/${datasetName}/version`)
            }
        })
    },

    useDatasetMetaByVersion(userName: string, datasetName: string, version: string) {
        return useQuery({
            queryKey: ['dataset', userName, datasetName, 'version', version, 'meta'],
            queryFn: async () => {
                return axiosInstance.get<DatasetMeta>(`/api/dataset/${userName}/${datasetName}/version/${version}/meta`)
            }
        })
    },

    useDownloadCodeByVersion(userName: string, datasetName: string, version: string, lang: string) {
        return useQuery({
            queryKey: ['dataset', userName, datasetName, 'version', version, 'download-code', lang],
            queryFn: async () => {
                return axiosInstance.get<{
                    code: string
                }>(`/api/dataset/${userName}/${datasetName}/version/${version}/download-code?lang=${lang}`)
            }
        })
    },

    useDatasetSampleByVersion(userName: string, datasetName: string, version: string, collName: string) {
        return useQuery({
            queryKey: ['dataset', userName, datasetName, 'version', version, 'coll', collName, 'sample'],
            queryFn: async () => {
                return axiosInstance.get<DatasetSample>(`/api/dataset/${userName}/${datasetName}/version/${version}/collection/${collName}/sample`)
            }
        })
    },

    useDatasetCodeExampleByVersion(userName: string, datasetName: string, version: string, collName: string) {
        return useQuery({
            queryKey: ['dataset', userName, datasetName, 'version', version, 'coll', collName, 'code'],
            queryFn: async () => {
                return axiosInstance.get<CodeSample>(`/api/dataset/${userName}/${datasetName}/version/${version}/collection/${collName}/code`)
            }
        })
    }
}

export const PostHooks = {
    usePostListing() {
        return useQuery({
            queryKey: ['post'],
            queryFn: async () => {
                return axiosInstance.get<{
                    items: {
                        name: string,
                        mtime: string
                    }[]
                }>(`/api/post`)
            }
        })
    },

    usePost(name: string) {
        return useQuery({
            queryKey: ['post', name],
            queryFn: async () => {
                return axiosInstance.get<string>(`/api/post/${name}`)
            }
        })
    },

    useReadmePost(name: string) {
        return useQuery({
            queryKey: ['post', name],

            queryFn: async () => {
                return axiosInstance.get<string>(`/api/post/${name}`)
            },
            retry: false
        })
    },

}