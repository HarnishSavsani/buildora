import { Result } from '@/request/Result'
import { get, post, del, put } from '@/request/index'
import type { User, ResetPasswordRequest, CheckCodeRequest } from '@/api/type/user'
import type { Ref } from 'vue'
import type { KeyValue, pageRequest } from '@/api/type/common'
import useStore from '@/stores'
import type { TriggerData } from '../type/trigger'
const prefix: any = { _value: '/workspace/' }
Object.defineProperty(prefix, 'value', {
  get: function () {
    const { user } = useStore()
    return this._value + user.getWorkspaceId() + '/trigger'
  },
})

const prefixWorkspace: any = { _value: '/workspace/' }
Object.defineProperty(prefixWorkspace, 'value', {
  get: function () {
    const { user } = useStore()
    return this._value + user.getWorkspaceId()
  },
})

/**
 * triggerList
 * @param data
 * @param loading
 * @returns
 */
const getTriggerList: (data?: any, loading?: Ref<boolean>) => Promise<Result<any>> = (
  data,
  loading,
) => {
  return get(`${prefix.value}`, data, loading)
}

/**
 * triggerDetails
 * @param trigger_id
 * @param loading
 * @returns
 */
const getTriggerDetail: (trigger_id: string, loading?: Ref<boolean>) => Promise<Result<any>> = (
  trigger_id,
  loading,
) => {
  return get(`${prefix.value}/${trigger_id}`, {}, loading)
}

/**
 * Create a trigger
 * @param data
 * @param loading
 * @returns
 */
const postTrigger: (data: TriggerData, loading?: Ref<boolean>) => Promise<Result<any>> = (
  data,
  loading,
) => {
  return post(`${prefix.value}`, data, undefined, loading)
}

/**
 * Modify trigger
 * @param trigger_id
 * @param data
 * @param loading
 * @returns
 */
const putTrigger: (
  trigger_id: string,
  data: TriggerData,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (trigger_id, data, loading) => {
  return put(`${prefix.value}/${trigger_id}`, data, undefined, loading)
}

/**
 * Delete trigger
 * @param trigger_id
 * @param loading
 * @returns
 */
const deleteTrigger: (trigger_id: string, loading?: Ref<boolean>) => Promise<Result<any>> = (
  trigger_id,
  loading,
) => {
  return del(`${prefix.value}/${trigger_id}`, undefined, {}, loading)
}

/**
 * Batch deletion trigger
 * @param data
 * @param loading
 * @returns
 */
const delMulTrigger: (data: any, loading?: Ref<boolean>) => Promise<Result<boolean>> = (
  data: any,
  loading,
) => {
  return put(`${prefix.value}/batch_delete`, { id_list: data }, undefined, loading)
}

/**
 * Batch activation/deactivationtrigger
 * @param data
 * @param loading
 * @returns
 */
const activateMulTrigger: (data: any, loading?: Ref<boolean>) => Promise<Result<boolean>> = (
  data: any,
  loading,
) => {
  return put(
    `${prefix.value}/batch_activate`,
    { id_list: data.id_list, is_active: data.is_active },
    undefined,
    loading,
  )
}

/**
 * PagingQuerytrigger
 * @param page    Pagingparameter
 * @param param   Queryparameter
 * @param loading loader
 * @returns
 */
const pageTrigger = (page: pageRequest, param: any, loading?: Ref<boolean>) => {
  return get(`${prefix.value}/${page.current_page}/${page.page_size}`, param, loading)
}
/**
 * Pagination Querytrigger execution task
 * @param trigger_id triggerid
 * @param page       Pagingparameter
 * @param param      Queryparameter
 * @param loading    Recorder
 * @returns
 */
const pageTriggerTaskRecord = (
  trigger_id: string,
  page: pageRequest,
  param: any,
  loading?: Ref<boolean>,
) => {
  return get(
    `${prefix.value}/${trigger_id}/task_record/${page.current_page}/${page.page_size}`,
    param,
    loading,
  )
}

const getTriggerTaskRecordDetails = (
  trigger_id: string,
  trigger_task_id: string,
  trigger_task_record_id: string,
  loading?: Ref<boolean>,
) => {
  return get(
    `${prefix.value}/${trigger_id}/trigger_task/${trigger_task_id}/trigger_task_record/${trigger_task_record_id}`,
    {},
    loading,
  )
}

/**
 * Resource-side creation trigger
 * @param source_type  Resource type
 * @param source_id    resourceid
 * @param data         NumberAccording to
 * @param loading      loader
 * @returns
 */
const postResourceTrigger: (
  source_type: string,
  source_id: string,
  data: TriggerData,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (source_type, source_id, data, loading) => {
  return post(
    `${prefixWorkspace.value}/${source_type}/${source_id}/trigger`,
    data,
    undefined,
    loading,
  )
}

/**
 * resourceendtriggerList
 * @param source_type
 * @param source_id
 * @param loading
 * @returns
 */
const getResourceTriggerList: (
  source_type: string,
  source_id: string,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (source_type, source_id, loading) => {
  return get(
    `${prefixWorkspace.value}/${source_type}/${source_id}/trigger`,
    undefined,
    loading
  )
}

/**
 * resourceendtriggerDetails
 * @param source_type
 * @param source_id
 * @param trigger_id
 * @param loading
 * @returns
 */
const getResourceTriggerDetail: (
    source_type: string,
  source_id: string,
  trigger_id: string,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (source_type, source_id, trigger_id, loading) => {
  return get(
    `${prefixWorkspace.value}/${source_type}/${source_id}/trigger/${trigger_id}`,
    undefined,
    loading
  )
}

/**
 * resourceendDelete trigger
 * @param source_type
 * @param source_id
 * @param trigger_id
 * @param loading
 * @returns
 */
const deleteResourceTrigger: (
    source_type: string,
  source_id: string,
  trigger_id: string,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (source_type, source_id, trigger_id, loading) => {
  return del(
    `${prefixWorkspace.value}/${source_type}/${source_id}/trigger/${trigger_id}`,
    undefined,
    {},
    loading
  )
}

/**
 * resourceendModify trigger
 * @param source_type Resource type
 * @param source_id   resourceid
 * @param trigger_id  triggerid
 * @param data        triggerNumberAccording to
 * @param loading     loader
 * @returns
 */
const putResourceTrigger: (
  source_type: string,
  source_id: string,
  trigger_id: string,
  data: TriggerData,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (source_type, source_id, trigger_id, data, loading) => {
  return put(
    `${prefixWorkspace.value}/${source_type}/${source_id}/trigger/${trigger_id}`,
    data,
    undefined,
    loading,
  )
}

export default {
  pageTrigger,
  getTriggerList,
  postTrigger,
  getTriggerDetail,
  putTrigger,
  deleteTrigger,
  delMulTrigger,
  activateMulTrigger,
  pageTriggerTaskRecord,
  getTriggerTaskRecordDetails,
  postResourceTrigger,
  putResourceTrigger,
  getResourceTriggerList,
  getResourceTriggerDetail,
  deleteResourceTrigger
}
