import { Result } from '@/request/Result'
import { get, post, del, put, exportFile, postStream, download } from '@/request/index'
import { type Ref } from 'vue'
import type { pageRequest } from '@/api/type/common'
import type { AddInternalToolParam, toolData } from '@/api/type/tool'

import useStore from '@/stores'
const prefix: any = { _value: '/workspace/' }
Object.defineProperty(prefix, 'value', {
  get: function () {
    const { user } = useStore()
    return this._value + user.getWorkspaceId() + '/tool'
  },
})

/**
 * toolListWith paging (no paging）
 * @params parameter {folder_id: string}
 */
const getToolList: (
  data?: any,
  loading?: Ref<boolean>,
) => Promise<Result<{ tools: any[]; folders: any[] }>> = (data, loading) => {
  return get(`${prefix.value}`, data, loading)
}

/**
 * toolListWith paging (no paging）
 */
const getAllToolList: (
  data?: any,
  loading?: Ref<boolean>,
) => Promise<Result<{ tools: any[]; folders: any[] }>> = (data, loading) => {
  return get(`${prefix.value}/tool_list`, data, loading)
}

/**
 * toolListWith paging
 * @param parameter
 * param  {
 "folder_id": "string",
 "name": "string",
 "tool_type": "string",
 }
 */
const getToolListPage: (
  page: pageRequest,
  param?: any,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (page, param, loading) => {
  return get(`${prefix.value}/${page.current_page}/${page.page_size}`, param, loading)
}

/**
 * Create tools
 * @param parameter
 */
const postTool: (data: toolData, loading?: Ref<boolean>) => Promise<Result<any>> = (
  data,
  loading,
) => {
  return post(`${prefix.value}`, data, undefined, loading)
}

/**
 * Revisetool
 * @param parameter

 */
const putTool: (tool_id: string, data: toolData, loading?: Ref<boolean>) => Promise<Result<any>> = (
  tool_id,
  data,
  loading,
) => {
  return put(`${prefix.value}/${tool_id}`, data, undefined, loading)
}

/**
 * @param parameter
 */
const postToolTestConnection: (data: toolData, loading?: Ref<boolean>) => Promise<Result<any>> = (
  data,
  loading,
) => {
  return post(`${prefix.value}/test_connection`, data, undefined, loading)
}

/**
 * Get toolsDetails
 * @param tool_id toolid
 * @param loading loader
 * @returns letterNumberDetails
 */
const getToolById: (tool_id: string, loading?: Ref<boolean>) => Promise<Result<any>> = (
  tool_id,
  loading,
) => {
  return get(`${prefix.value}/${tool_id}`, undefined, loading)
}

/**
 * Deletion tool
 * @param parameter tool_id
 */
const delTool: (tool_id: string, loading?: Ref<boolean>) => Promise<Result<boolean>> = (
  tool_id,
  loading,
) => {
  return del(`${prefix.value}/${tool_id}`, undefined, {}, loading)
}

const putToolIcon: (id: string, data: any, loading?: Ref<boolean>) => Promise<Result<any>> = (
  id,
  data,
  loading,
) => {
  return put(`${prefix.value}/${id}/edit_icon`, data, undefined, loading)
}

const exportTool = (id: string, name: string, loading?: Ref<boolean>) => {
  return exportFile(name + '.tool', `${prefix.value}/${id}/export`, undefined, loading)
}

/**
 * Debugging tools
 * @param parameter

 */
const postToolDebug: (data: any, loading?: Ref<boolean>) => Promise<Result<any>> = (
  data: any,
  loading,
) => {
  return post(`${prefix.value}/debug`, data, undefined, loading)
}

const postImportTool: (data: any, loading?: Ref<boolean>) => Promise<Result<any>> = (
  data,
  loading,
) => {
  return post(`${prefix.value}/import`, data, undefined, loading)
}

const postPylint: (code: string, loading?: Ref<boolean>) => Promise<Result<any>> = (
  code,
  loading,
) => {
  return post(`${prefix.value}/pylint`, { code }, {}, loading)
}

/**
 * tool store-Add toSystem built-in
 */
const addInternalTool: (
  tool_id: string,
  param: AddInternalToolParam,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (tool_id, param, loading) => {
  return post(`${prefix.value}/${tool_id}/add_internal_tool`, param, undefined, loading)
}

/**
 * tool store-Add to
 */
const addStoreTool: (
  tool_id: string,
  param: AddInternalToolParam,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (tool_id, param, loading) => {
  return post(`${prefix.value}/${tool_id}/add_store_tool`, param, undefined, loading)
}

const updateStoreTool: (
  tool_id: string,
  param: AddInternalToolParam,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (tool_id, param, loading) => {
  return post(`${prefix.value}/${tool_id}/update_store_tool`, param, undefined, loading)
}

const pageToolRecord = (tool_id: string, page: pageRequest, param: any, loading?: Ref<boolean>) => {
  return get(
    `${prefix.value}/${tool_id}/tool_record/${page.current_page}/${page.page_size}`,
    param,
    loading,
  )
}

const getToolRecordDetail = (tool_id: string, record_id: string) => {
  return get(`${prefix.value}/${tool_id}/tool_record/${record_id}`)
}

const uploadSkillFile: (data: toolData, loading?: Ref<boolean>) => Promise<Result<any>> = (
  data,
  loading,
) => {
  return put(`${prefix.value}/upload_skill_file`, data, undefined, loading)
}

const downloadSkillFile: (tool_id: string, loading?: Ref<boolean>) => Promise<Result<any>> = (
  tool_id,
  loading,
) => {
  return download(`${prefix.value}/${tool_id}/download_skill_file`, 'GET', undefined, undefined, loading)
}

/**
 * SavetoolWorkflow
 * @param tool_id
 * @param data
 * @param loading
 * @returns
 */
const putToolWorkflow: (
  tool_id: string,
  data: any,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (tool_id, data, loading) => {
  return put(`${prefix.value}/${tool_id}/workflow`, data, undefined, loading)
}

/**
 * Export the knowledge baseWorkflow
 * @param knowledge_id
 * @param knowledge_name
 * @param loading
 * @returns
 */
const exportKnowledgeWorkflow = (
  knowledge_id: string,
  knowledge_name: string,
  loading?: Ref<boolean>,
) => {
  return exportFile(
    knowledge_name + '.kbwf',
    `${prefix.value}/${knowledge_id}/workflow/export`,
    undefined,
    loading,
  )
}

/**
 * Import toolWorkflow
 */
const importToolWorkflow: (
  tool_id: string,
  data: any,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (tool_id, data, loading) => {
  return post(`${prefix.value}/${tool_id}/workflow/import`, data, undefined, loading)
}
/**
 * Get toolsWorkflow versionList
 * @param tool_id
 * @param loading
 * @returns
 */
const listToolWorkflowVersion: (tool_id: string, loading?: Ref<boolean>) => Promise<Result<any>> = (
  tool_id: string,
  loading,
) => {
  return get(`${prefix.value}/${tool_id}/tool_version`, {}, loading)
}
/**
 *
 * @param tool_id toolid
 * @param tool_version_id toolVersionid
 * @param data NumberAccording to
 * @param loading
 * @returns
 */
const updateToolWorkflowVersion: (
  tool_id: string,
  tool_version_id: string,
  data: any,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (tool_id: string, tool_version_id, data, loading) => {
  return put(`${prefix.value}/${tool_id}/tool_version/${tool_version_id}`, data, {}, loading)
}
const publish: (tool_id: string, loading?: Ref<boolean>) => Promise<Result<any>> = (
  tool_id: string,
  loading,
) => {
  return put(`${prefix.value}/${tool_id}/publish`, {}, {}, loading)
}

/**
 * DebuggingWorkflow
 * @param parameter
 * chat_id: string
 * data
 */
const debugToolWorkflow: (tool_id: string, data: any) => Promise<any> = (tool_id, data) => {
  const p = (window.MaxKB?.prefix ? window.MaxKB?.prefix : '/admin') + '/api'
  return postStream(`${p}${prefix.value}/${tool_id}/debug`, data)
}

const generateCode: (data: any) => Promise<Result<any>> = (data: any) => {
  const p = (window.MaxKB?.prefix ? window.MaxKB?.prefix : '/admin') + '/api'
  return postStream(`${p}${prefix.value}/generate_code`, data)
}
/**
 * mcp Node
 */
const getMcpTools: (
  tool_id: string,
  mcp_servers: any,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (tool_id, mcp_servers, loading) => {
  return post(`${prefix.value}/${tool_id}/mcp_tools`, { mcp_servers }, {}, loading)
}

/**
 * Batch removal tool
 * @param parameter
 * {
  "id_list": [String]
}
 */
const delMulTool: (data: any, loading?: Ref<boolean>) => Promise<Result<boolean>> = (
  data,
  loading,
) => {
  return put(`${prefix.value}/batch_delete`, { id_list: data }, undefined, loading)
}
/**
 * Batch removal tool
 * @param parameter
 * {
  "id_list": [String]
  "folder_id": string
}
 */
const putMulMoveTool: (data: any, loading?: Ref<boolean>) => Promise<Result<boolean>> = (
  data,
  loading,
) => {
  return put(`${prefix.value}/batch_move`, data, undefined, loading)
}
export default {
  getToolList,
  getAllToolList,
  getToolListPage,
  putTool,
  getToolById,
  postTool,
  postToolDebug,
  postImportTool,
  postPylint,
  exportTool,
  putToolIcon,
  delTool,
  addInternalTool,
  addStoreTool,
  updateStoreTool,
  postToolTestConnection,
  pageToolRecord,
  getToolRecordDetail,
  uploadSkillFile,
  downloadSkillFile,
  putToolWorkflow,
  importToolWorkflow,
  listToolWorkflowVersion,
  updateToolWorkflowVersion,
  publish,
  debugToolWorkflow,
  generateCode,
  getMcpTools,
  delMulTool,
  putMulMoveTool
}
