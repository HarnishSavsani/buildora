import type { Dict } from './common'
interface modelRequest {
  name: string
  model_type: string
  model_name: string
}

interface Provider {
  /**
   * suppliercode name
   */
  provider: string
  /**
   * supplierName
   */
  name: string
  /**
   * suppliericon
   */
  icon: string
}

interface ListModelRequest {
  /**
   * Model name
   */
  name?: string
  /**
   * Model type
   */
  model_type?: string
  /**
   * base modelName
   */
  model_name?: string
  /**
   * supplier
   */
  provider?: string

  workspace_id?: string
}

interface Model {
  /**
   * Primary keyid
   */
  id: string
  /**
   * ModelName
   */
  name: string
  /**
   * Model type
   */
  model_type: string
  user_id: string
  username: string
  nick_name: string
  /**
   * base model
   */
  model_name: string
  /**
   * Authentication information
   */
  credential: any
  /**
   * supplier
   */
  provider: string
  /**
   * state
   */
  status: 'SUCCESS' | 'DOWNLOAD' | 'ERROR' | 'PAUSE_DOWNLOAD'
  /**
   * Metadata
   */
  meta: Dict<any>
  /**
   * ModelParameter configuration
   */
  model_params_form: Dict<any>[]
  resource_count: number
  create_time?: any
}
interface CreateModelRequest {
  /**
   * ModelName
   */
  name: string
  /**
   * Model type
   */
  model_type: string
  /**
   * base model
   */
  model_name: string
  /**
   * Authentication information
   */
  credential: any
  /**
   * supplier
   */
  provider: string
}

interface EditModelRequest {
  /**
   * ModelName
   */
  name: string
  /**
   * Model type
   */
  model_type: string
  /**
   * base model
   */
  model_name: string
  /**
   * Authentication information
   */
  credential: any
}

interface BaseModel {
  /**
   * base modelName
   */
  name: string
  /**
   * base modeldescribe
   */
  desc: string
  /**
   * base modelType
   */
  model_type: string
}
export type {
  modelRequest,
  Provider,
  ListModelRequest,
  Model,
  BaseModel,
  CreateModelRequest,
  EditModelRequest
}
