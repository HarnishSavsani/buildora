<template>
  <component :is="column.property" v-bind="attrs" :column="column" :row="row"></component>
</template>
<script setup lang="ts">
import { computed, ref } from 'vue'
import _ from 'lodash'
const props = defineProps<{
  /**
   *TableSingle renderingItem column
   */
  column: any
  /**
   * This lineNumberAccording to
   */
  row: any
}>()

const attrs = computed(() => {
  return props.column.attrs ? props.column.attrs : {}
})
</script>
<style lang="scss" scoped></style>
