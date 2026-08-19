import { useLocalStorage } from '@vueuse/core'
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { i18n, langCode, localeConfigKey } from '@/locales/index'

export function useLocale() {
  const { locale } = useI18n({ useScope: 'global' })
  function changeLocale(lang: string) {
    // likeIf the switched language does not correspond to the language documentDefault isSimplifiedindian
    if (!langCode.includes(lang)) {
      lang = 'en-US'
    }

    locale.value = lang
    useLocalStorage(localeConfigKey, 'en-US').value = lang
  }

  const getComponentsLocale = computed(() => {
    const localeMessage = i18n.global.getLocaleMessage(locale.value) as Record<string, any>
    return localeMessage.componentsLocale
  })

  return {
    changeLocale,
    getComponentsLocale,
    locale,
  }
}
