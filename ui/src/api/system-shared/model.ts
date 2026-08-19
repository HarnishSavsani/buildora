import { Result } from '@/request/Result'
import { get, post, del, put } from '@/request/index'
import { type Ref } from 'vue'
import type {
  ListModelRequest,
  Model,
  CreateModelRequest,
  EditModelRequest,
} from '@/api/type/model'
import type { FormField } from '@/components/dynamics-form/type'

const prefix = '/system/shared/model'

/**
 * getModelList
 * @params parameter name, model_type, model_name
 */
const getModelList: (
  request?: ListModelRequest,
  loading?: Ref<boolean>,
) => Promise<Result<Array<Model>>> = (data, loading) => {
  return get(`${prefix}`, data, loading)
}

/**
 * Get drop-down selection boxModelList
 * @params parameter name, model_type, model_name
 */
const getSelectModelList: (
  data?: ListModelRequest,
  loading?: Ref<boolean>,
) => Promise<Result<Array<Model>>> = (data, loading) => {
  return get(`${prefix}`, data, loading)
}

/**
 * Get model parameter form
 * @param model_id Modelid
 * @param loading
 * @returns
 */
const getModelParamsForm: (
  model_id: string,
  loading?: Ref<boolean>,
) => Promise<Result<Array<FormField>>> = (model_id, loading) => {
  return get(`${prefix}/${model_id}/model_params_form`, {}, loading)
}

/**
 * Create model
 * @param request request object
 * @param loading loader
 * @returns
 */
const createModel: (
  request: CreateModelRequest,
  loading?: Ref<boolean>,
) => Promise<Result<Model>> = (request, loading) => {
  return post(`${prefix}`, request, {}, loading)
}

/**
 * ReviseModel
 * @param request request object
 * @param loading loader
 * @returns
 */
const updateModel: (
  model_id: string,
  request: EditModelRequest,
  loading?: Ref<boolean>,
) => Promise<Result<Model>> = (model_id, request, loading) => {
  return put(`${prefix}/${model_id}`, request, {}, loading)
}

/**
 * ReviseModelParameter configuration
 * @param request request object
 * @param loading loader
 * @returns
 */
const updateModelParamsForm: (
  model_id: string,
  request: any[],
  loading?: Ref<boolean>,
) => Promise<Result<Model>> = (model_id, request, loading) => {
  return put(`${prefix}/${model_id}/model_params_form`, request, {}, loading)
}

/**
 * getModelDetailsRootAccording toModelid includeAuthentication information
 * @param model_id Modelid
 * @param loading  loader
 * @returns
 */
const getModelById: (model_id: string, loading?: Ref<boolean>) => Promise<Result<Model>> = (
  model_id,
  loading,
) => {
  return get(`${prefix}/${model_id}`, {}, loading)
}
/**
 * getModelinformationExcludesAuthentication informationRootAccording toModelid
 * @param model_id Modelid
 * @param loading  loader
 * @returns
 */
const getModelMetaById: (model_id: string, loading?: Ref<boolean>) => Promise<Result<Model>> = (
  model_id,
  loading,
) => {
  return get(`${prefix}/${model_id}/meta`, {}, loading)
}
/**
 * pausedownload
 * @param model_id Modelid
 * @param loading loader
 * @returns
 */
const pauseDownload: (model_id: string, loading?: Ref<boolean>) => Promise<Result<boolean>> = (
  model_id,
  loading,
) => {
  return put(`${prefix}/${model_id}/pause_download`, undefined, {}, loading)
}
const deleteModel: (model_id: string, loading?: Ref<boolean>) => Promise<Result<boolean>> = (
  model_id,
  loading,
) => {
  return del(`${prefix}/${model_id}`, undefined, {}, loading)
}

export default {
  getModelList,
  createModel,
  updateModel,
  deleteModel,
  getModelById,
  getModelMetaById,
  pauseDownload,
  getModelParamsForm,
  updateModelParamsForm,
  getSelectModelList,
}
