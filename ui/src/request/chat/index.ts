import axios, { type InternalAxiosRequestConfig, AxiosHeaders } from 'axios'
import { MsgError } from '@/utils/message'
import type { NProgress } from 'nprogress'
import type { Ref } from 'vue'
import type { Result } from '@/request/Result'
import useStore from '@/stores'

import { ref, type WritableComputedRef } from 'vue'

const axiosConfig = {
  baseURL: (window.MaxKB?.prefix ? window.MaxKB?.prefix : '/chat') + '/api',
  withCredentials: false,
  timeout: 600000,
  headers: {},
}

const instance = axios.create(axiosConfig)

/* Settingsrequest interceptor */
instance.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    if (config.headers === undefined) {
      config.headers = new AxiosHeaders()
    }
    const { chatUser } = useStore()
    const token = chatUser.getToken()
    const language = chatUser.getLanguage()
    config.headers['Accept-Language'] = `${language}`
    if (token) {
      config.headers['AUTHORIZATION'] = `Bearer ${token}`
    }
    return config
  },
  (err: any) => {
    return Promise.reject(err)
  },
)

//Settingsresponse interceptor
instance.interceptors.response.use(
  (response: any) => {
    if (response.data) {
      if (response.data.code !== 200 && !(response.data instanceof Blob)) {
        MsgError(response.data.message)
        return Promise.reject(response.data)
      }
    }
    return response
  },
  (err: any) => {
    if (err.code === 'ECONNABORTED') {
      MsgError(err.message)
      console.error(err)
    }
    return Promise.reject(err)
  },
)

export const request = instance

/* Simplify request methods, unify ProcessingReturn results, and add loadingProcessing, here{success,data,message}FormattedReturnvalueforFor example, specific project rootAccording toactual demandRevise */
const promise: (
  request: Promise<any>,
  loading?: NProgress | Ref<boolean> | WritableComputedRef<boolean>,
) => Promise<Result<any>> = (request, loading = ref(false)) => {
  return new Promise((resolve, reject) => {
    if ((loading as NProgress).start) {
      ;(loading as NProgress).start()
    } else {
      ;(loading as Ref).value = true
    }
    request
      .then((response) => {
        // blobTypeofReturnstateYesresponse.status
        if (response.status === 200) {
          resolve(response?.data || response)
        } else {
          reject(response?.data || response)
        }
      })
      .catch((error) => {
        reject(error)
      })
      .finally(() => {
        if ((loading as NProgress).start) {
          ;(loading as NProgress).done()
        } else {
          ;(loading as Ref).value = false
        }
      })
  })
}

/**
 * Send get request   Generally used to requestresource
 * @param url    resourceurl
 * @param params parameter
 * @param loading loading
 * @returns differentstep promise object
 */
export const get: (
  url: string,
  params?: unknown,
  loading?: NProgress | Ref<boolean>,
  timeout?: number,
) => Promise<Result<any>> = (
  url: string,
  params: unknown,
  loading?: NProgress | Ref<boolean>,
  timeout?: number,
) => {
  return promise(request({ url: url, method: 'get', params, timeout: timeout }), loading)
}

/**
 * faso postask Generally usedAdd toresource
 * @param url    resourceurl
 * @param params parameter
 * @param data   Add toNumberAccording to
 * @param loading loading
 * @returns differentstep promise object
 */
export const post: (
  url: string,
  data?: unknown,
  params?: unknown,
  loading?: NProgress | Ref<boolean>,
  timeout?: number,
) => Promise<Result<any> | any> = (url, data, params, loading, timeout) => {
  return promise(request({ url: url, method: 'post', data, params, timeout }), loading)
}

/**
 * Upload fileof post Request, support upload progress callback and Medium disconnection
 * @param url        resourceurl
 * @param data       UploadNumberAccording to（Generalfor FormData）
 * @param onProgress Upload progress callback, parameterfor percentage(0-100)
 * @param params     Queryparameter
 * @param loading    loading
 * @param timeout    timeout
 * @returns Return { request, abort }，request fordifferentstep promise object，abort Used for Medium uploads
 */
export const postUpload: (
  url: string,
  data?: unknown,
  onProgress?: (percent: number, event: any) => void,
  params?: unknown,
  loading?: NProgress | Ref<boolean>,
  timeout?: number,
) => { request: Promise<Result<any> | any>; abort: () => void } = (
  url,
  data,
  onProgress,
  params,
  loading,
  timeout,
) => {
  const controller = new AbortController()
  const request = promise(
    instance({
      url: url,
      method: 'post',
      data,
      params,
      timeout,
      signal: controller.signal,
      onUploadProgress: (event) => {
        if (onProgress) {
          const percent = event.total ? Math.round((event.loaded * 100) / event.total) : 0
          onProgress(percent, event)
        }
      },
    }),
    loading,
  )
  return {
    request,
    abort: () => controller.abort(),
  }
}

/**|
 * Send put request for Revise serverresource
 * @param url     resourceaddress
 * @param params  paramsparameteraddress
 * @param data    Need ReviseNumberAccording to
 * @param loading Progress bar
 * @returns
 */
export const put: (
  url: string,
  data?: unknown,
  params?: unknown,
  loading?: NProgress | Ref<boolean>,
  timeout?: number,
) => Promise<Result<any>> = (url, data, params, loading, timeout) => {
  return promise(request({ url: url, method: 'put', data, params, timeout }), loading)
}

/**
 * Delete
 * @param url     Deleteurl
 * @param params  paramsparameter
 * @param loading Progress bar
 * @returns
 */
export const del: (
  url: string,
  params?: unknown,
  data?: unknown,
  loading?: NProgress | Ref<boolean>,
  timeout?: number,
) => Promise<Result<any>> = (url, params, data, loading, timeout) => {
  return promise(request({ url: url, method: 'delete', params, data, timeout }), loading)
}

/**
 * StreamProcessing
 * @param url  urladdress
 * @param data askbody
 * @returns
 */
export const postStream: (url: string, data?: unknown) => Promise<Result<any> | any> = (
  url,
  data,
) => {
  const { chatUser } = useStore()
  const token = chatUser.getToken()
  const language = chatUser.getLanguage()
  const headers: HeadersInit = { 'Content-Type': 'application/json' }
  if (token) {
    headers['AUTHORIZATION'] = `Bearer ${token}`
  }
  headers['Accept-Language'] = `${language}`
  return fetch(url, {
    method: 'POST',
    body: data ? JSON.stringify(data) : undefined,
    headers: headers,
  })
}

export const exportExcel: (
  fileName: string,
  url: string,
  params: any,
  loading?: NProgress | Ref<boolean>,
) => Promise<any> = (
  fileName: string,
  url: string,
  params: any,
  loading?: NProgress | Ref<boolean>,
) => {
  return promise(request({ url: url, method: 'get', params, responseType: 'blob' }), loading).then(
    (res: any) => {
      if (res) {
        const blob = new Blob([res], {
          type: 'application/vnd.ms-excel',
        })
        const link = document.createElement('a')
        link.href = window.URL.createObjectURL(blob)
        link.download = fileName
        link.click()
        //Release memory
        window.URL.revokeObjectURL(link.href)
      }
      return true
    },
  )
}

export const exportFile: (
  fileName: string,
  url: string,
  params: any,
  loading?: NProgress | Ref<boolean>,
) => Promise<any> = (
  fileName: string,
  url: string,
  params: any,
  loading?: NProgress | Ref<boolean>,
) => {
  return promise(request({ url: url, method: 'get', params, responseType: 'blob' }), loading).then(
    (res: any) => {
      if (res) {
        const blob = new Blob([res], {
          type: 'application/octet-stream',
        })
        const link = document.createElement('a')
        link.href = window.URL.createObjectURL(blob)
        link.download = fileName
        link.click()
        //Release memory
        window.URL.revokeObjectURL(link.href)
      }
      return true
    },
  )
}

export const exportExcelPost: (
  fileName: string,
  url: string,
  params: any,
  data: any,
  loading?: NProgress | Ref<boolean>,
) => Promise<any> = (
  fileName: string,
  url: string,
  params: any,
  data: any,
  loading?: NProgress | Ref<boolean>,
) => {
  return promise(
    request({
      url: url,
      method: 'post',
      params, // QuerycharacterStringparameter
      data, // Request bodyNumberAccording to
      responseType: 'blob',
    }),
    loading,
  ).then((res: any) => {
    if (res) {
      const blob = new Blob([res], {
        type: 'application/vnd.ms-excel',
      })
      const link = document.createElement('a')
      link.href = window.URL.createObjectURL(blob)
      link.download = fileName
      link.click()
      // Release memory
      window.URL.revokeObjectURL(link.href)
    }
    return true
  })
}

export const download: (
  url: string,
  method: string,
  data?: any,
  params?: any,
  loading?: NProgress | Ref<boolean>,
) => Promise<any> = (
  url: string,
  method: string,
  data?: any,
  params?: any,
  loading?: NProgress | Ref<boolean>,
) => {
  return promise(request({ url: url, method: method, data, params, responseType: 'blob' }), loading)
}

/**
 * Link to server Establishws
 * @param url websocketpath
 * @returns  ReturnonepieceswebsocketExample
 */
export const socket = (url: string) => {
  let protocol = 'ws://'
  if (window.location.protocol === 'https:') {
    protocol = 'wss://'
  }
  let uri = protocol + window.location.host + url
  if (!import.meta.env.DEV) {
    uri = protocol + window.location.host + import.meta.env.VITE_BASE_PATH + url
  }
  return new WebSocket(uri)
}
export default instance
