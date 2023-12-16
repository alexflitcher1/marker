import {$searchHost} from './index'

export const search = async (query) => {
    const response = await $searchHost.get(`/search`, {params: {query: query}})
    return response
}