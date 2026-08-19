import {Result} from '@/request/Result'
import {get, post, put} from '@/request/index'
import {type Ref} from 'vue'

const prefix = '/system/auth'
/**
 * getCertificationSettings
 */
const getAuthSetting: (auth_type: string, loading?: Ref<boolean>) => Promise<Result<any>> = (auth_type, loading) => {
  return get(`${prefix}/${auth_type}/detail`, undefined, loading)
}

/**
 * ldapconnecttest
 */
const postAuthSetting: (data: any, loading?: Ref<boolean>) => Promise<Result<any>> = (
  data,
  loading
) => {
  return post(`${prefix}/connection`, data, undefined, loading)
}

/**
 * ReviseEmail settings
 */
const putAuthSetting: (auth_type: string, data: any, loading?: Ref<boolean>) => Promise<Result<any>> = (
  auth_type,
  data,
  loading
) => {
  return put(`${prefix}/${auth_type}/info`, data, undefined, loading)
}

export default {
  getAuthSetting,
  postAuthSetting,
  putAuthSetting
}
