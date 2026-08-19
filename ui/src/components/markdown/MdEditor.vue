<template>
  <MdEditor :language="language" noIconfont noPrettier v-bind="$attrs">
    <template #defFooters>
      <slot name="defFooters"> </slot>
    </template>
  </MdEditor>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { MdEditor, config } from 'md-editor-v3'
import { getBrowserLang } from '@/locales/index'
import './assets/markdown-iconfont.js'
// Introducing the public common library MediumlanguageConfiguration
import ZH_TW from '@vavt/cm-extension/dist/locale/zh-TW'
defineOptions({ name: 'MdEditor' })
const language = computed(() => localStorage.getItem('MaxKB-locale') || getBrowserLang() || '')
config({
  editorConfig: {
    languageUserDefined: {
      'zh-Hant': ZH_TW,
    },
  },
})
</script>
