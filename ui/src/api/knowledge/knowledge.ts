import { Result } from '@/request/Result'
import { get, post, del, put, exportFile, exportExcel } from '@/request/index'
import { type Ref } from 'vue'
import type { Dict, pageRequest } from '@/api/type/common'
import type { knowledgeData } from '@/api/type/knowledge'

import useStore from '@/stores'
const prefix: any = { _value: '/workspace/' }
Object.defineProperty(prefix, 'value', {
  get: function () {
    const { user } = useStore()
    return this._value + user.getWorkspaceId() + '/knowledge'
  },
})

/**
 * Knowledge base list（No pagination）
 * @param parameter
 * param  {
    folder_id: "string",
    name: "string",
    tool_type: "string",
    desc: string,
  }
 */
const getKnowledgeList: (param?: any, loading?: Ref<boolean>) => Promise<Result<any>> = (
  param,
  loading,
) => {
  return get(`${prefix.value}`, param, loading)
}

/**
 * knowledge basePaginated list
 * @param parameter
 * param  {
 "folder_id": "string",
 "name": "string",
 "tool_type": "string",
 desc: string,
 }
 */
const getKnowledgeListPage: (
  page: pageRequest,
  param?: any,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (page, param, loading) => {
  return get(`${prefix.value}/${page.current_page}/${page.page_size}`, param, loading)
}

/**
 * knowledge baseDetails
 * @param parameter knowledge_id
 */
const getKnowledgeDetail: (knowledge_id: string, loading?: Ref<boolean>) => Promise<Result<any>> = (
  knowledge_id,
  loading,
) => {
  return get(`${prefix.value}/${knowledge_id}`, undefined, loading)
}

/**
 * Modify knowledge base information
 * @param parameter
 * knowledge_id
 * {
 "name": "string",
 "desc": true
 }
 */
const putKnowledge: (
  knowledge_id: string,
  data: any,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (knowledge_id, data, loading) => {
  return put(`${prefix.value}/${knowledge_id}`, data, undefined, loading)
}

/**
 * Delete knowledge base
 * @param parameter knowledge_id
 */
const delKnowledge: (knowledge_id: string, loading?: Ref<boolean>) => Promise<Result<boolean>> = (
  knowledge_id,
  loading,
) => {
  return del(`${prefix.value}/${knowledge_id}`, undefined, {}, loading)
}

/**
 * vectorizationknowledge base
 * @param parameter knowledge_id
 */
const putReEmbeddingKnowledge: (
  knowledge_id: string,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (knowledge_id, loading) => {
  return put(`${prefix.value}/${knowledge_id}/embedding`, undefined, undefined, loading)
}

/**
 * Export the knowledge base
 * @param knowledge_name Knowledge base name
 * @param knowledge_id   knowledge baseid
 * @returns
 */
const exportKnowledge: (
  knowledge_name: string,
  knowledge_id: string,
  loading?: Ref<boolean>,
) => Promise<any> = (knowledge_name, knowledge_id, loading) => {
  return exportExcel(
    knowledge_name + '.xlsx',
    `${prefix.value}/${knowledge_id}/export`,
    undefined,
    loading,
  )
}
/**
 *Export Zip Knowledge Base
 * @param knowledge_name Knowledge base name
 * @param knowledge_id   knowledge baseid
 * @param loading      loader
 * @returns
 */
const exportZipKnowledge: (
  knowledge_name: string,
  knowledge_id: string,
  loading?: Ref<boolean>,
) => Promise<any> = (knowledge_name, knowledge_id, loading) => {
  return exportFile(
    knowledge_name + '.zip',
    `${prefix.value}/${knowledge_id}/export_zip`,
    undefined,
    loading,
  )
}

/**
 * generateRelated questions
 * @param knowledge_id knowledge baseid
 * @param data
 * @param loading
 * @returns
 */
const putGenerateRelated: (
  knowledge_id: string,
  data: any,
  loading?: Ref<boolean>,
) => Promise<Result<Array<any>>> = (knowledge_id, data, loading) => {
  return put(`${prefix.value}/${knowledge_id}/generate_related`, data, null, loading)
}

/**
 * hit test list
 * @param knowledge_id
 * @param loading
 * @query  { query_text: string, top_number: number, similarity: number }
 * @returns
 */
const putKnowledgeHitTest: (
  knowledge_id: string,
  data: any,
  loading?: Ref<boolean>,
) => Promise<Result<Array<any>>> = (knowledge_id, data, loading) => {
  return post(`${prefix.value}/${knowledge_id}/hit_test`, data, undefined, loading)
}

/**
 * synchronousknowledge base
 * @param parameter knowledge_id
 * @query parameter sync_type // Sync type->replace:Replacementsynchronous,complete:full sync
 */
const putSyncWebKnowledge: (
  knowledge_id: string,
  sync_type: string,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (knowledge_id, sync_type, loading) => {
  return put(`${prefix.value}/${knowledge_id}/sync`, undefined, { sync_type }, loading)
}

/**
 * Create knowledge base
 * @param parameter
 * {
 "name": "string",
 "folder_id": "string",
 "desc": "string",
 "embedding": "string"
 }
 */
const postKnowledge: (data: knowledgeData, loading?: Ref<boolean>) => Promise<Result<any>> = (
  data,
  loading,
) => {
  return post(`${prefix.value}/base`, data, undefined, loading, 1000 * 60 * 5)
}

/**
 * createWorkflowknowledge base
 * @param data
 * @param loading
 * @returns
 */
const createWorkflowKnowledge: (data: any, loading?: Ref<boolean>) => Promise<Result<any>> = (
  data,
  loading,
) => {
  return post(`${prefix.value}/workflow`, data, undefined, loading)
}
/**
 * getcurrentUsersAvailablevectorizationModelList (Uselessarrive)
 * @param application_id
 * @param loading
 * @query  { query_text: string, top_number: number, similarity: number }
 * @returns
 */
const getKnowledgeEmdeddingModel: (
  knowledge_id: string,
  loading?: Ref<boolean>,
) => Promise<Result<Array<any>>> = (knowledge_id, loading) => {
  return get(`${prefix.value}/${knowledge_id}/emdedding_model`, loading)
}

/**
 * getcurrentUsersAvailableModelList
 * @param
 * @param loading
 * @returns
 */
const getKnowledgeModel: (loading?: Ref<boolean>) => Promise<Result<Array<any>>> = (loading) => {
  return get(`${prefix.value}/model`, loading)
}

/**
 * createWebknowledge base
 * @param parameter
 * {
 "name": "string",
 "folder_id": "string",
 "desc": "string",
 "embedding": "string",
 "source_url": "string",
 "selector": "string"
 }
 */
const postWebKnowledge: (data: any, loading?: Ref<boolean>) => Promise<Result<any>> = (
  data,
  loading,
) => {
  return post(`${prefix.value}/web`, data, undefined, loading)
}

// createFeishuknowledge base
const postLarkKnowledge: (data: any, loading?: Ref<boolean>) => Promise<Result<Array<any>>> = (
  data,
  loading,
) => {
  return post(`${prefix.value}/lark/save`, data, null, loading)
}

const putLarkKnowledge: (
  knowledge_id: string,
  data: any,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (knowledge_id, data, loading) => {
  return put(`${prefix.value}/lark/${knowledge_id}`, data, undefined, loading)
}

const getAllTags: (params: any, loading?: Ref<boolean>) => Promise<Result<any>> = (
  params,
  loading,
) => {
  return get(`${prefix.value}/tags`, params, loading)
}

const getTags: (
  knowledge_id: string,
  params: any,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (knowledge_id, params, loading) => {
  return get(`${prefix.value}/${knowledge_id}/tags`, params, loading)
}

const postTags: (
  knowledge_id: string,
  tags: any,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (knowledge_id, tags, loading) => {
  return post(`${prefix.value}/${knowledge_id}/tags`, tags, null, loading)
}

const putTag: (
  knowledge_id: string,
  tag_id: string,
  tag: any,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (knowledge_id, tag_id, tag, loading) => {
  return put(`${prefix.value}/${knowledge_id}/tags/${tag_id}`, tag, null, loading)
}

const delTag: (
  knowledge_id: string,
  tag_id: string,
  type: string,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (knowledge_id, tag_id, type, loading) => {
  return del(`${prefix.value}/${knowledge_id}/tags/${tag_id}/${type}`, null, loading)
}

const delMulTag: (
  knowledge_id: string,
  tags: any,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (knowledge_id, tags, loading) => {
  return put(`${prefix.value}/${knowledge_id}/tags/batch_delete`, tags, null, loading)
}
const getKnowledgeWorkflowFormList: (
  knowledge_id: string,
  type: 'local' | 'tool',
  id: string,
  node: any,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (
  knowledge_id: string,
  type: 'local' | 'tool',
  id: string,
  node,
  loading,
) => {
  return post(
    `${prefix.value}/${knowledge_id}/datasource/${type}/${id}/form_list`,
    { node },
    {},
    loading,
  )
}
const getKnowledgeWorkflowDatasourceDetails: (
  knowledge_id: string,
  type: 'local' | 'tool',
  id: string,
  params: any,
  function_name: string,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (
  knowledge_id: string,
  type: 'local' | 'tool',
  id: string,
  params,
  function_name,
  loading,
) => {
  return post(
    `${prefix.value}/${knowledge_id}/datasource/${type}/${id}/${function_name}`,
    params,
    {},
    loading,
  )
}
const workflowAction: (
  knowledge_id: string,
  instance: Dict<any>,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (knowledge_id: string, instance, loading) => {
  return post(`${prefix.value}/${knowledge_id}/debug`, instance, {}, loading)
}

const workflowUpload: (
  knowledge_id: string,
  instance: Dict<any>,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (knowledge_id: string, instance, loading) => {
  return post(`${prefix.value}/${knowledge_id}/upload_document`, instance, {}, loading)
}

const publish: (knowledge_id: string, loading?: Ref<boolean>) => Promise<Result<any>> = (
  knowledge_id: string,
  loading,
) => {
  return put(`${prefix.value}/${knowledge_id}/publish`, {}, {}, loading)
}

/**
 * Saveknowledge baseWorkflow
 * @param knowledge_id
 * @param data
 * @param loading
 * @returns
 */
const putKnowledgeWorkflow: (
  knowledge_id: string,
  data: any,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (knowledge_id, data, loading) => {
  return put(`${prefix.value}/${knowledge_id}/workflow`, data, undefined, loading)
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
 * Import knowledge baseWorkflow
 */
const importKnowledgeWorkflow: (
  knowledge_id: string,
  data: any,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (knowledge_id, data, loading) => {
  return post(`${prefix.value}/${knowledge_id}/workflow/import`, data, undefined, loading)
}

const listKnowledgeVersion: (
  knowledge_id: string,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (knowledge_id: string, loading) => {
  return get(`${prefix.value}/${knowledge_id}/knowledge_version`, {}, loading)
}
const updateKnowledgeVersion: (
  knowledge_id: string,
  knowledge_version_id: string,
  data: any,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (knowledge_id: string, knowledge_version_id, data, loading) => {
  return put(
    `${prefix.value}/${knowledge_id}/knowledge_version/${knowledge_version_id}`,
    data,
    {},
    loading,
  )
}
const getWorkflowActionPage: (
  knowledge_id: string,
  page: pageRequest,
  query: any,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (knowledge_id: string, page, query, loading) => {
  return get(
    `${prefix.value}/${knowledge_id}/action/${page.current_page}/${page.page_size}`,
    query,
    loading,
  )
}
const getWorkflowAction: (
  knowledge_id: string,
  knowledge_action_id: string,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (knowledge_id: string, knowledge_action_id, loading) => {
  return get(`${prefix.value}/${knowledge_id}/action/${knowledge_action_id}`, {}, loading)
}
const cancelWorkflowAction: (
  knowledge_id: string,
  knowledge_action_id: string,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (knowledge_id: string, knowledge_action_id, loading) => {
  return post(
    `${prefix.value}/${knowledge_id}/action/${knowledge_action_id}/cancel`,
    {},
    undefined,
    loading,
  )
}
/**
 * mcp Node
 */
const getMcpTools: (
  knowledge_id: string,
  mcp_servers: any,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (knowledge_id, mcp_servers, loading) => {
  return post(`${prefix.value}/${knowledge_id}/mcp_tools`, { mcp_servers }, {}, loading)
}

const postTransformWorkflow: (
  knowledge_id: string,
  data: any,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (knowledge_id, data, loading) => {
  return post(`${prefix.value}/${knowledge_id}/transform_workflow`, data, undefined, loading)
}

/**
 * Export the knowledge base
 * @param knowledge_name
 * @param knowledge_id
 * @param loading
 * @returns
 */
const exportKnowledgeBundle: (
  knowledge_name: string,
  knowledge_id: string,
  with_source_file: boolean,
  loading?: Ref<boolean>
) => Promise<any> = (knowledge_name, knowledge_id, with_source_file, loading) => {
  return exportFile(
    knowledge_name + '.zip',
    `${prefix.value}/${knowledge_id}/export_knowledge`, {with_source_file: with_source_file}, loading
  )
}

/**
 * Import knowledge base
 * @param data
 * @param loading
 * @returns
 */
const importKnowledgeBundle: (
  data: any,
  loading: Ref<boolean>
) => Promise<Result<any>> = (data, loading) => {
  return post(`${prefix.value}/import_knowledge`, data, undefined, loading)
}

/**
 * Delete knowledge base in batches
 * @param parameter
 * {
  "id_list": [String]
}
 */
const delMulKnowledge: (data: any, loading?: Ref<boolean>) => Promise<Result<boolean>> = (
  data,
  loading,
) => {
  return put(`${prefix.value}/batch_delete`, { id_list: data }, undefined, loading)
}
/**
 * Batch transferknowledge base
 * @param parameter
 * {
  "id_list": [String]
  "folder_id": string
}
 */
const putMulMoveKnowledge: (data: any, loading?: Ref<boolean>) => Promise<Result<boolean>> = (
  data,
  loading,
) => {
  return put(`${prefix.value}/batch_move`, data, undefined, loading)
}


export default {
  getKnowledgeList,
  getKnowledgeListPage,
  getKnowledgeDetail,
  putKnowledge,
  delKnowledge,
  putReEmbeddingKnowledge,
  exportKnowledge,
  exportZipKnowledge,
  putGenerateRelated,
  putKnowledgeHitTest,
  putSyncWebKnowledge,
  postKnowledge,
  getKnowledgeModel,
  postWebKnowledge,
  postLarkKnowledge,
  putLarkKnowledge,
  getAllTags,
  getTags,
  postTags,
  putTag,
  delTag,
  delMulTag,
  createWorkflowKnowledge,
  getKnowledgeWorkflowFormList,
  workflowAction,
  getWorkflowAction,
  getKnowledgeWorkflowDatasourceDetails,
  getMcpTools,
  listKnowledgeVersion,
  updateKnowledgeVersion,
  publish,
  putKnowledgeWorkflow,
  workflowUpload,
  getWorkflowActionPage,
  cancelWorkflowAction,
  exportKnowledgeWorkflow,
  importKnowledgeWorkflow,
  postTransformWorkflow,
  exportKnowledgeBundle,
  importKnowledgeBundle,
  delMulKnowledge,
  putMulMoveKnowledge,
}
