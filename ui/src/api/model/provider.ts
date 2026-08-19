import {Result} from '@/request/Result'
import {get, post} from '@/request/index'
import type {Ref} from 'vue'
import type {Provider, BaseModel} from '@/api/type/model'
import type {FormField} from '@/components/dynamics-form/type'
import type {KeyValue} from '../type/common'

const prefix_provider = '/provider'
/**
 * getsupplierList
 */
const getProvider: (loading?: Ref<boolean>) => Promise<Result<Array<Provider>>> = (loading) => {
  return get(`${prefix_provider}`, {}, loading)
}

/**
 * getsupplierList
 */
const getProviderByModelType: (
  model_type: string,
  loading?: Ref<boolean>,
) => Promise<Result<Array<Provider>>> = (model_type, loading) => {
  return get(`${prefix_provider}`, {model_type}, loading)
}

/**
 * Get model creation form
 * @param provider
 * @param model_type
 * @param model_name
 * @param loading
 * @returns
 */
const getModelCreateForm: (
  provider: string,
  model_type: string,
  model_name: string,
  loading?: Ref<boolean>,
) => Promise<Result<Array<FormField>>> = (provider, model_type, model_name, loading) => {
  return get(`${prefix_provider}/model_form`, {provider, model_type, model_name}, loading)
}

/**
 * Get a list of model types
 * @param provider supplier
 * @param loading  loader
 * @returns Model typeList
 */
const listModelType: (
  provider: string,
  loading?: Ref<boolean>,
) => Promise<Result<Array<KeyValue<string, string>>>> = (provider, loading?: Ref<boolean>) => {
  return get(`${prefix_provider}/model_type_list`, {provider}, loading)
}

/**
 * getbase modelList
 * @param provider
 * @param model_type
 * @param loading
 * @returns
 */
const listBaseModel: (
  provider: string,
  model_type: string,
  loading?: Ref<boolean>,
) => Promise<Result<Array<BaseModel>>> = (provider, model_type, loading) => {
  return get(`${prefix_provider}/model_list`, {provider, model_type}, loading)
}

const listBaseModelParamsForm: (
  provider: string,
  model_type: string,
  model_name: string,
  loading?: Ref<boolean>,
) => Promise<Result<Array<BaseModel>>> = (provider, model_type, model_name, loading) => {
  return get(`${prefix_provider}/model_params_form`, {provider, model_type, model_name}, loading)
}
export default {
  getProvider,
  getModelCreateForm,
  getProviderByModelType,
  listModelType,
  listBaseModel,
  listBaseModelParamsForm,
}
