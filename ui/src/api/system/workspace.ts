import { Result } from '@/request/Result'
import type { Ref } from 'vue'
import { get, post, del } from '@/request/index'
import type { WorkspaceItem, CreateWorkspaceMemberParamsItem, WorkspaceMemberItem } from '@/api/type/workspace'
import type { pageRequest, PageList } from '@/api/type/common'

const prefix = '/system/workspace'

/**
 * getfront pageWorkspace drop-downList
 */
const getWorkspaceListByUser: (loading?: Ref<boolean>) => Promise<Result<WorkspaceItem[]>> = (loading) => {
  return get('/workspace/by_user', undefined, loading)
}

/**
 * getAdd memberWorkspace drop-downList
 */
const getWorkspaceList: (loading?: Ref<boolean>) => Promise<Result<Record<string, any>[]>> = (loading) => {
  return get('/workspace/current_user', undefined, loading)
}

/**
 * Get a list of workspaces
 */
const getSystemWorkspaceList: (loading?: Ref<boolean>) => Promise<Result<WorkspaceItem[]>> = (loading) => {
  return get(`${prefix}`, undefined, loading)
}

/**
 * NeworrenewWorkspace
 */
const CreateOrUpdateWorkspace: (
  data: WorkspaceItem,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (data, loading) => {
  return post(`${prefix}`, data, undefined, loading)
}

/**
 * Delete workspaceformer schoolVerification
 */
const deleteWorkspaceCheck: (workspace_id: string, loading?: Ref<boolean>) => Promise<Result<any>> = (
  workspace_id,
  loading,
) => {
  return get(`${prefix}/${workspace_id}/check`, undefined, loading)
}

/**
 * Delete workspace
 */
const deleteWorkspace: (workspace_id: string, loading?: Ref<boolean>) => Promise<Result<boolean>> = (
  workspace_id,
  loading,
) => {
  return del(`${prefix}/${workspace_id}`, undefined, {}, loading)
}

/**
 * Get workspace member list
 */
const getWorkspaceMemberList: (
  workspace_id: string,
  page: pageRequest,
  param: any,
  loading?: Ref<boolean>,
) => Promise<Result<PageList<WorkspaceMemberItem[]>>> = (workspace_id, page, param, loading) => {
  return get(
    `${prefix}/${workspace_id}/user_list/${page.current_page}/${page.page_size}`,
    param,
    loading,
  )
}

/**
 * Create a new Workspace member
 */
const CreateWorkspaceMember: (
  workspace_id: string,
  data: CreateWorkspaceMemberParamsItem[],
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (workspace_id, data, loading) => {
  return post(`${prefix}/${workspace_id}/add_member`, data, undefined, loading)
}

/**
 * Delete workspacemember
 */
const deleteWorkspaceMember: (workspace_id: string, user_relation_id: string, loading?: Ref<boolean>) => Promise<Result<any>> = (
  workspace_id,
  user_relation_id,
  loading,
) => {
  return post(`${prefix}/${workspace_id}/remove_member/${user_relation_id}`, undefined, {}, loading)
}

/**
 * getAdd memberRole drop-downList
 */
const getWorkspaceRoleList: (loading?: Ref<boolean>) => Promise<Result<Record<string, any>[]>> = (loading) => {
  return get('/role_list/current_user', undefined, loading)
}

export default {
  getWorkspaceList,
  getSystemWorkspaceList,
  CreateOrUpdateWorkspace,
  deleteWorkspace,
  getWorkspaceMemberList,
  CreateWorkspaceMember,
  deleteWorkspaceMember,
  getWorkspaceRoleList,
  getWorkspaceListByUser,
  deleteWorkspaceCheck
}
