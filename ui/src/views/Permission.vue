<template>
  <div>illustrate: v-hasPermission Yesusev-show Essentially ComponentsYes rendered v-if="hasPermission('xxxx')"</div>
  <div>Components will not render this way(Used forfor exampleCall interface is required when mounting Components like Components,If you don’t want Components to render)</div>
  <div>for exampleWorkspacedrop downListComponentsusev-if Example： Enterprise EditionComponents:</div>

  <button v-if="hasPermission(EditionConst.IS_CE, 'OR')">I Yes Community EditionComponents</button>

  <button v-hasPermission="EditionConst.IS_CE">I Yes Community EditionComponents</button>
  <!-- ================Yes Enterprise versionComponents================== -->
  <button v-if="hasPermission(EditionConst.IS_EE, 'OR')">Yes Enterprise versionComponents</button>
  <button v-hasPermission="EditionConst.IS_EE">Yes Enterprise versionComponents</button>

  <!-- ================Enterprise EditionComponents andYesADMINRole================== -->
  <button v-if="hasPermission([EditionConst.IS_EE, RoleConst.ADMIN], 'AND')">
    Yes Enterprise Edition andYesADMINRole
  </button>
  <button
    v-hasPermission="new ComplexPermission([RoleConst.ADMIN], [], [EditionConst.IS_EE], 'AND')"
  >
    Yes Enterprise Edition andYesADMINRole
  </button>
  <!-- ================Enterprise EditionComponents And Yescurrent worksspace manager================== -->
  <button
    v-if="hasPermission([EditionConst.IS_EE, RoleConst.WORKSPACE_MANAGE.getWorkspaceRole], 'AND')"
  >
    I Yes Enterprise and have a current jobspace managerRole
  </button>
  <button
    v-hasPermission="
      new ComplexPermission(
        [RoleConst.WORKSPACE_MANAGE.getWorkspaceRole],
        [],
        [EditionConst.IS_EE],
        'OR',
      )
    "
  >
    I Yes Enterprise and have a current jobspace managerRole
  </button>
  <!-- ================Enterprise EditionComponents （And Yescurrent worksspace manager orUsers are read-only）================== -->
  <button
    v-if="
      hasPermission(
        new ComplexPermission(
          [RoleConst.WORKSPACE_MANAGE.getWorkspaceRole],
          [PermissionConst.USER_READ],
          [EditionConst.IS_EE],
          'OR',
        ),
        'OR',
      )
    "
  >
    Yes Enterprise version （And Yescurrent worksspace manager orUsers are read-only）
  </button>
  <button
    v-hasPermission="
      new ComplexPermission(
        [RoleConst.WORKSPACE_MANAGE.getWorkspaceRole],
        [PermissionConst.USER_READ],
        [EditionConst.IS_EE],
        'OR',
      )
    "
  >
    Yes Enterprise version (and Yes current workspace manager orUsers are read-only）
  </button>
</template>
<script setup lang="ts">
import { PermissionConst, EditionConst, RoleConst } from '@/utils/permission/data'
import { hasPermission } from '@/utils/permission/index'
import { ComplexPermission } from '@/utils/permission/type'
</script>
<style lang="scss" scoped></style>
