import useStore from '@/stores'
import { useRoute } from 'vue-router'
export type PF = () => Role | string | Permission | ComplexPermission
export type CRF = () => Role | string
export type CPF = () => Permission | string
/**
 * Roleobject
 */
export class Role {
  role: string

  constructor(role: string) {
    this.role = role
  }

  getWorkspaceRole = () => {
    const { user } = useStore()
    return new Role(`${this.role}:/WORKSPACE/${user.getWorkspaceId()}`)
  }
  getWorkspaceRoleString = () => {
    const { user } = useStore()
    return `${this.role}:/WORKSPACE/${user.getWorkspaceId()}`
  }
  toString() {
    return this.role
  }
}
/**
 * Permissionsobject
 */
export class Permission {
  permission: string

  constructor(permission: string) {
    this.permission = permission
  }
  /**
   * WorkspacePermissions
   * @param workspace_id Workspaceid
   * @returns WorkspacePermissions
   */
  getWorkspacePermission = () => {
    const { user } = useStore()
    return `${this.permission}:/WORKSPACE/${user.getWorkspaceId()}`
  }
  /**
   * CustomizeWorkspace managerPermissions
   * @returns
   */
  getWorkspacePermissionWorkspaceManageRole = () => {
    const { user } = useStore()
    return `${this.permission}:/WORKSPACE/${user.getWorkspaceId()}:ROLE/WORKSPACE_MANAGE`
  }
  /**
   * WorkspaceresourcePermissions
   * @param workspace_id Workspaceid
   * @param resource     resource
   * @param resource_id  resourceid
   * @returns  WorkspaceresourcePermissions
   */
  getWorkspaceResourcePermission = (resource: string, resource_id: string) => {
    const { user } = useStore()
    return `${this.permission}:/WORKSPACE/${user.getWorkspaceId()}/${resource}/${resource_id}`
  }
  /**
   *
   * @param resource_id resourceid
   * @returns WorkspaceDownKnowledge base resourcesPermissions
   */
  getKnowledgeWorkspaceResourcePermission = (resource_id: string) => {
    return this.getWorkspaceResourcePermission('KNOWLEDGE', resource_id)
  }
  getTest=()=>{
    const route=useRoute()
    debugger
    console.log(route)
    return ""
  }
  /**
   *
   * @param resource_id  resourceid
   * @returns WorkspaceDownapplicationresourcePermissions
   */
  getApplicationWorkspaceResourcePermission = (resource_id: string) => {
    return this.getWorkspaceResourcePermission('APPLICATION', resource_id)
  }
  /**
   * 
   * @param resource_id resourceid
   * @returns WorkspaceDownModel resourcesPermissions
   */
  getModelWorkspaceResourcePermission = (resource_id: string) => {
    return this.getWorkspaceResourcePermission('MODEL', resource_id)
  }
  /**
   * 
   * @param resource_id 
   * @returns WorkspaceDownTools and resourcesPermissions
   */
  getToolWorkspaceResourcePermission = (resource_id: string) => {
    return this.getWorkspaceResourcePermission('TOOL', resource_id)
  }

  toString() {
    return this.permission
  }
}

/**
 * Complex Permissions object
 */
export class ComplexPermission {
  roleList: Array<string | Role | CRF>

  permissionList: Array<string | Permission | CPF>

  editionList: Array<string | Edition>

  compare: 'OR' | 'AND'

  constructor(
    roleList: Array<string | Role | CRF>,
    permissionList: Array<string | Permission | CPF>,
    editionList: Array<string | Edition>,
    compare: 'OR' | 'AND',
  ) {
    this.roleList = roleList
    this.permissionList = permissionList
    this.editionList = editionList
    this.compare = compare
  }
}
/**
 * Version
 */
export class Edition {
  edition: string
  constructor(edition: string) {
    this.edition = edition
  }
  toString() {
    return this.edition
  }
}
