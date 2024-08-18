import {UseQueryResult} from "@tanstack/react-query";
import {AxiosResponse} from "axios";

export function readmeQueryToString(query: UseQueryResult<AxiosResponse<string, any>, any>): string {
    if (query.isSuccess) {
        if (query.data) {
            return query.data.data
        }
    } else if (query.isLoading) {
        return '**Loading content...**'
    }
    return ''
}

export function classNames(...strings: string[]): string {
    return strings.join(" ");
}

export function formatFileSize(bytes: number, decimalPoint = 2) {
    if (bytes === 0) return '0 Bytes';

    const k = 1024,
        dm = decimalPoint < 0 ? 0 : decimalPoint,
        sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
        i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

