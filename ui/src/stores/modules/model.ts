import { defineStore } from 'pinia'
import { type Ref } from 'vue'
import ProviderApi from '@/api/model/provider'
import ModelApi from '@/api/model/model'
import type { ListModelRequest } from '@/api/type/model'

const useModelStore = defineStore('model', {
  state: () => ({}),
  actions: {
    // Only available for Inapplication drop-down Listuse, not commonresource
    async asyncGetSelectModel(data?: ListModelRequest, loading?: Ref<boolean>) {
      return new Promise((resolve, reject) => {
        ModelApi.getSelectModelList(data, loading)
          .then((res: any) => {
            resolve(res)
          })
          .catch((error: any) => {
            reject(error)
          })
      })
    },
    async asyncGetProvider(loading?: Ref<boolean>) {
      return new Promise((resolve, reject) => {
        ProviderApi.getProvider(loading)
          .then((res) => {
            resolve(res)
          })
          .catch((error) => {
            reject(error)
          })
      })
    },
  },
})

export default useModelStore
