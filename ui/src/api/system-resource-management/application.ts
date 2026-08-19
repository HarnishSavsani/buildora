import { Result } from '@/request/Result'
import { get, post, postStream, del, put, request, download, exportFile } from '@/request/index'
import type { pageRequest } from '@/api/type/common'
import type { ApplicationFormType } from '@/api/type/application'
import { type Ref } from 'vue'

const prefix = '/system/resource/application'

/**
 * getallapplication
 * @param param
 * @param loading
 */
const getAllApplication: (param?: any, loading?: Ref<boolean>) => Promise<Result<any[]>> = (
  param,
  loading,
) => {
  return get(`${prefix}`, param, loading)
}
/**
 * getPagingapplication
 * param {
 "name": "string",
 }
 */
const getApplication: (
  page: pageRequest,
  param: any,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (page, param, loading) => {
  return get(`${prefix}/${page.current_page}/${page.page_size}`, param, loading)
}

/**
 * Reviseapplication
 * @param parameter
 */
const putApplication: (
  application_id: string,
  data: ApplicationFormType,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (application_id, data, loading) => {
  return put(`${prefix}/${application_id}`, data, undefined, loading)
}

/**
 * Deleteapplication
 * @param parameter application_id
 */
const delApplication: (
  application_id: string,
  loading?: Ref<boolean>,
) => Promise<Result<boolean>> = (application_id, loading) => {
  return del(`${prefix}/${application_id}`, undefined, {}, loading)
}

/**
 * applicationDetails
 * @param parameter application_id
 */
const getApplicationDetail: (
  application_id: string,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (application_id, loading) => {
  return get(`${prefix}/${application_id}`, undefined, loading)
}

/**
 * getAccessToken
 * @param parameter application_id
 */
const getAccessToken: (application_id: string, loading?: Ref<boolean>) => Promise<Result<any>> = (
  application_id,
  loading,
) => {
  return get(`${prefix}/${application_id}/access_token`, undefined, loading)
}
/**
 * ReviseAccessToken
 * @param parameter application_id
 * data {
 *  "is_active": true
 * }
 */
const putAccessToken: (
  application_id: string,
  data: any,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (application_id, data, loading) => {
  return put(`${prefix}/${application_id}/access_token`, data, undefined, loading)
}

/**
 * Replace community version-ReviseAccessToken
 * @param parameter application_id
 * data {
 *  "show_source": boolean,
 *  "show_history": boolean,
 *  "draggable": boolean,
 *  "show_guide": boolean,
 *  "avatar": file,
 *  "float_icon": file,
 * }
 */
const putXpackAccessToken: (
  application_id: string,
  data: any,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (application_id, data, loading) => {
  return put(`${prefix}/${application_id}/setting`, data, undefined, loading)
}

/**
 * statistics
 * @param parameter application_id, data
 */
const getStatistics: (
  application_id: string,
  data: any,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (application_id, data, loading) => {
  return get(`${prefix}/${application_id}/application_stats`, data, loading)
}
/**
 * statisticstokenconsume
 */
const getTokenUsage: (
  application_id: string,
  data: any,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (application_id, data, loading) => {
  return get(`${prefix}/${application_id}/application_token_usage`, data, loading)
}
const topQuestions: (
  application_id: string,
  data: any,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (application_id, data, loading) => {
  return get(`${prefix}/${application_id}/top_questions`, data, loading)
}
/**
 * OpenDebuggingConversationid
 * @param application_id applicationid
 * @param loading loader
 * @returns
 */
const open: (application_id: string, loading?: Ref<boolean>) => Promise<Result<string>> = (
  application_id,
  loading,
) => {
  return get(`${prefix}/${application_id}/open`, {}, loading)
}

/**
 * Generate prompt words
 * @param application_id
 * @param model_id
 * @param data
 * @returns
 */
const generate_prompt: (application_id:string, model_id:string, data: any) => Promise<any> = (
  application_id,
  model_id,
  data
) => {
  const prefix = (window.MaxKB?.prefix ? window.MaxKB?.prefix : '/admin') + '/api'
  return postStream(`${prefix}/system/resource/application/${application_id}/model/${model_id}/prompt_generate`, data)
}


/**
 * applicationPublish
 * @param application_id
 * @param loading
 * @returns
 */
const publish: (
  application_id: string,
  data: any,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (application_id, data, loading) => {
  return put(`${prefix}/${application_id}/publish`, data, {}, loading)
}

/**
 *
 * @param application_id
 * @param data
 * @param loading
 * @returns
 */
const playDemoText: (application_id: string, data: any, loading?: Ref<boolean>) => Promise<any> = (
  application_id,
  data,
  loading,
) => {
  return download(`${prefix}/${application_id}/play_demo_text`, 'post', data, undefined, loading)
}

/**
 * textConvert to voice
 */
const postTextToSpeech: (
  application_id: string,
  data: any,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (application_id, data, loading) => {
  return download(`${prefix}/${application_id}/text_to_speech`, 'post', data, undefined, loading)
}
/**
 * voice to speechtext
 */
const speechToText: (
  application_id: string,
  data: any,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (application_id, data, loading) => {
  return post(`${prefix}/${application_id}/speech_to_text`, data, undefined, loading)
}

/**
 * getapplicationSettings
 * @param application_id applicationid
 * @param loading loader
 * @returns
 */
const getApplicationSetting: (
  application_id: string,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (application_id, loading) => {
  return get(`${prefix}/${application_id}/setting`, undefined, loading)
}

/**
 * Exportapplication
 */

const exportApplication = (
  application_id: string,
  application_name: string,
  loading?: Ref<boolean>,
) => {
  return exportFile(
    application_name + '.mk',
    `${prefix}/${application_id}/export`,
    undefined,
    loading,
  )
}

/**
 * importapplication
 */
const importApplication: (data: any, loading?: Ref<boolean>) => Promise<Result<any>> = (
  data,
  loading,
) => {
  return post(`${prefix}/import`, data, undefined, loading)
}

/**
 * Conversation
 * @param parameter
 * chat_id: string
 * data
 */
const chat: (chat_id: string, data: any) => Promise<any> = (chat_id, data) => {
  const prefix = (window.MaxKB?.prefix ? window.MaxKB?.prefix : '/admin') + '/api'
  return postStream(`${prefix}/chat_message/${chat_id}`, data)
}
/**
 * getDialogue user authenticationType
 * @param loading loader
 * @returns
 */
const getChatUserAuthType: (loading?: Ref<boolean>) => Promise<any> = (loading) => {
  return get(`/chat_user/auth/types`, {}, loading)
}

/**
 * Get platform status
 */
const getPlatformStatus: (application_id: string) => Promise<Result<any>> = (application_id) => {
  return get(`${prefix}/${application_id}/platform/status`)
}
/**
 * Update platform status
 */
const updatePlatformStatus: (application_id: string, data: any) => Promise<Result<any>> = (
  application_id,
  data,
) => {
  return post(`${prefix}/${application_id}/platform/status`, data)
}
/**
 * Get platform configuration
 */
const getPlatformConfig: (application_id: string, type: string) => Promise<Result<any>> = (
  application_id,
  type,
) => {
  return get(`${prefix}/${application_id}/platform/${type}`)
}
/**
 * Update platform configuration
 */
const updatePlatformConfig: (
  application_id: string,
  type: string,
  data: any,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (application_id, type, data, loading) => {
  return post(`${prefix}/${application_id}/platform/${type}`, data, undefined, loading)
}

/**
 * mcp Node
 */
const getMcpTools: (application_id: string, loading?: Ref<boolean>) => Promise<Result<any>> = (
  application_id,
  loading,
) => {
  return get(`${prefix}/${application_id}/mcp_tools`, undefined, loading)
}

export default {
  getAllApplication,
  getApplication,
  putApplication,
  delApplication,
  getApplicationDetail,
  getAccessToken,
  putAccessToken,
  exportApplication,
  importApplication,
  getStatistics,
  open,
  chat,
  getChatUserAuthType,
  getApplicationSetting,
  getPlatformStatus,
  updatePlatformStatus,
  getPlatformConfig,
  publish,
  updatePlatformConfig,
  playDemoText,
  postTextToSpeech,
  speechToText,
  getMcpTools,
  putXpackAccessToken,
  generate_prompt,
  getTokenUsage,
  topQuestions
}
