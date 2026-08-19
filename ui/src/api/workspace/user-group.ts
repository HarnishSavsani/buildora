import {Result} from '@/request/Result'
import {get, post, del} from '@/request/index'
import type {Ref} from 'vue'
import type {ChatUserGroupUserItem,} from '@/api/type/systemChatUser'
import type {pageRequest, PageList, ListItem} from '@/api/type/common'

const prefix = '/workspace/group'

/**
 * Get list of user groups
 */
const getUserGroup: (loading?: Ref<boolean>) => Promise<Result<ListItem[]>> = () => {
  return get(`${prefix}`)
}

/**
 * Create usersGroup
 * @param parameter
 * {
 "id": "string",
 "name": "string"
 }
 */
const postUserGroup: (data: ListItem, loading?: Ref<boolean>) => Promise<Result<boolean>> = (
  data,
  loading,
) => {
  return post(`${prefix}`, data, undefined, loading)
}

/**
 * Delete user group
 * @param parameter user_group_id
 */
const delUserGroup: (user_group_id: string, loading?: Ref<boolean>) => Promise<Result<boolean>> = (
  user_group_id,
  loading,
) => {
  return del(`${prefix}/${user_group_id}`, undefined, {}, loading)
}

/**
 * GiveUser groupAdd user
 */
const postAddMember: (
  user_group_id: string,
  body: any,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (user_group_id, body, loading) => {
  return post(`${prefix}/${user_group_id}/add_member`, body, {}, loading)
}

/**
 * FromUser groupDelete user
 */
const postRemoveMember: (
  user_group_id: string,
  body: any,
  loading?: Ref<boolean>,
) => Promise<Result<any>> = (user_group_id, body, loading) => {
  return post(`${prefix}/${user_group_id}/remove_member`, body, {}, loading)
}

/**
 * getUser groupmembers ofList
 */
const getUserListByGroup: (
  user_group_id: string,
  page: pageRequest,
  params ?: any,
  loading?: Ref<boolean>,
) => Promise<Result<PageList<ChatUserGroupUserItem[]>>> = (user_group_id, page, params, loading) => {
  return get(
    `${prefix}/${user_group_id}/user_list/${page.current_page}/${page.page_size}`,
    params ? params : undefined,
    loading,
  )
}
export default {
  getUserGroup,
  postUserGroup,
  delUserGroup,
  postAddMember,
  postRemoveMember,
  getUserListByGroup
}
