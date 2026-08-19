import { PermissionConst, EditionConst, RoleConst } from '@/utils/permission/data'
const ModelRouter = {
  path: '/knowledge',
  name: 'knowledge',
  meta: {
    title: 'views.knowledge.title',
    menu: true,
    permission: [
      RoleConst.ADMIN,
      RoleConst.EXTENDS_ADMIN,
      RoleConst.USER.getWorkspaceRole,
      RoleConst.WORKSPACE_MANAGE.getWorkspaceRole,
      PermissionConst.KNOWLEDGE_READ.getWorkspacePermission,
      PermissionConst.KNOWLEDGE_READ.getWorkspacePermissionWorkspaceManageRole,
    ],
    icon: 'app-knowledge',
    iconActive: 'app-knowledge-active',
    group: 'workspace',
    order: 3,
  },
  redirect: '/knowledge',
  component: () => import('@/layout/layout-template/SimpleLayout.vue'),
  children: [
    {
      path: '/knowledge',
      name: 'knowledge-index',
      meta: { title: 'knowledge baseHome page', activeMenu: '/knowledge', sameRoute: 'knowledge' },
      component: () => import('@/views/knowledge/index.vue'),
    },

    // UploadDocumentation
    {
      path: '/knowledge/document/upload/:folderId/:type',
      name: 'UploadDocument',
      meta: { activeMenu: '/knowledge' },
      component: () => import('@/views/document/UploadDocument.vue'),
      hidden: true,
    },
    // UploadDocumentation - FeishuDocumentation
    {
      path: '/knowledge/import/lark/:folderId',
      name: 'ImportLarkDocument',
      meta: { activeMenu: '/knowledge' },
      component: () => import('@/views/document/ImportLarkDocument.vue'),
      hidden: true,
    },
    // UploadDocumentation - Workflow
    {
      path: '/knowledge/import/workflow/:folderId',
      name: 'ImportWorkflowDocument',
      meta: { activeMenu: '/knowledge' },
      component: () => import('@/views/document/ImportWorkflowDocument.vue'),
      hidden: true,
    },
  ],
}

export default ModelRouter
