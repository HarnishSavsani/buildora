<template>
  <el-dialog
    align-center
    :title="$t('views.application.generateDialog.generatePrompt')"
    v-model="dialogVisible"
    style="width: 600px"
    append-to-body
    :close-on-click-modal="true"
    :close-on-press-escape="true"
    :before-close="handleDialogClose"
  >
    <div class="generate-prompt-dialog-bg border-r-8">
      <div class="scrollbar-height">
        <!-- generatecontent -->
        <div class="p-16 pb-0 lighter">
          <el-scrollbar ref="scrollDiv">
            <div
              ref="dialogScrollbar"
              v-if="answer"
              class="pre-wrap lighter"
              style="max-height: calc(100vh - 400px)"
            >
              {{ answer }}
            </div>
            <p v-else-if="loading" shadow="always" style="margin: 0.5rem 0">
              <el-icon class="is-loading color-primary mr-4"><Loading /></el-icon>
              {{ $t('views.application.generateDialog.loading') }}
              <span class="dotting"></span>
            </p>
            <p v-else class="flex align-center">
              <AppIcon iconName="app-generate-star" class="color-primary mr-4"></AppIcon>
              {{ $t('views.application.generateDialog.title') }}
            </p>
          </el-scrollbar>

          <div v-if="answer && !loading && !isStreaming && !showContinueButton" class="mt-8">
            <el-button type="primary" @click="() => emit('replace', answer)">
              {{ $t('views.application.generateDialog.replace') }}
            </el-button>
            <el-button @click="copyClick(answer)">
              {{ $t('common.copy') }}
            </el-button>
            <el-button @click="reAnswerClick" :disabled="!answer || loading" :loading="loading">
              {{ $t('views.application.generateDialog.remake') }}
            </el-button>
          </div>
          <div class="mt-8" v-else>
            <el-button type="primary" v-if="showContinueButton" @click="continueStreaming" link>
              {{ $t('views.application.generateDialog.continue') }}
            </el-button>
          </div>
        </div>

        <!-- textInput box -->

        <div class="generate-prompt-operate p-16">
          <div v-if="showStopButton" class="text-center mb-8">
            <el-button class="border-primary video-stop-button" @click="pauseStreaming">
              <app-icon iconName="app-video-stop" class="mr-8"></app-icon>
              {{ $t('views.application.generateDialog.stop') }}
            </el-button>
          </div>

          <div class="operate-textarea">
            <el-input
              ref="quickInputRef"
              v-model="inputValue"
              :autosize="{ minRows: 1, maxRows: 10 }"
              type="textarea"
              :placeholder="$t('views.application.generateDialog.placeholder')"
              :maxlength="100000"
              class="chat-operate-textarea"
              @keydown.enter="handleSubmit($event)"
            />

            <div class="operate">
              <div class="text-right">
                <el-button
                  text
                  class="sent-button"
                  :disabled="!inputValue.trim() || loading || isStreaming"
                  @click="handleSubmit"
                >
                  <img
                    v-show="!inputValue.trim() || loading || isStreaming"
                    src="@/assets/chat/icon_send.svg"
                    alt=""
                  />
                  <SendIcon v-show="inputValue.trim() && !loading && !isStreaming" />
                </el-button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </el-dialog>
</template>

<script setup lang="ts">
import { computed, onUnmounted, reactive, ref, nextTick, watch } from 'vue'
import { useRoute } from 'vue-router'
import { MsgConfirm } from '@/utils/message'
import { t } from '@/locales'
import systemGeneratePromptAPI from '@/api/system-resource-management/application'
import generatePromptAPI from '@/api/application/application'
import useStore from '@/stores'
import { copyClick } from '@/utils/clipboard'
const emit = defineEmits(['replace'])
const { user } = useStore()
const route = useRoute()

const chatMessages = ref<Array<any>>([])

const apiType = computed(() => {
  if (route.path.includes('resource-management')) {
    return 'systemManage'
  } else {
    return 'workspace'
  }
})
// original input
const originalUserInput = ref<string>('')
const modelID = ref('')
const applicationID = ref('')
const dialogVisible = ref(false)
const inputValue = ref<string>('')
const loading = ref<boolean>(false)

const promptTemplates = {
  INIT_TEMPLATE: `
Please rootAccording toUsersdescribegeneratea piece completeAIRolePersonalitytemplate:

Usersneed：{userInput}

Important note：
1. RoleThe setting must serve"{userInput}"contentSet the core functions of the application
2. Allow Users to adjust and optimize the specific content set by Role
3. likeIf UsersRequirementsRevise a certain piecesSkillor part, make corresponding adjustments while maintaining the applicationTheme

pleaseaccording toBelowFormatgenerate：

Must strictly follow the Below rules：
1. **It is strictly prohibited to output explanations, prefaces, and additional explanations**. Only the final results are output.。
2. **Strict useBelowFormat**, no missing Title, no moreotherparagraph。
3. **likeIf certain pieces set by UsersRequirementsReviseRole, make adjustments while maintaining the core functions of the application**。
4. **likeIf Users’ needs have nothing to do with Role setting generate (like chatting, other topics), then it mainly depends onAccording toapplicationinformationgeneratestandardRoleSettings, but do not completely ignore Users input, can extract valuable auxiliary information (like field background, tone, Style, etc.) from Medium for secondary reference.**。

# Role:
RoleOverviewandA sentence of main responsibilitiesdescribe

## Target：
Roles job goals,If there are multiple goals, you can list them in points,But it is recommended to focus on 1-2 goals

## core skills：
### Skill 1: [Skill name, such as work recommendation/information inquiry/professional analysis, etc.]
1. [Execution steps1 - Describe the first specific operation step of the skill, including conditional judgment and processing methods]
2. [Execution steps2 - Describe the second specific action step of the skill, including how to obtain or process information]
3. [Execution steps3 - Describe the final output steps of the skill, explaining how the results are presented]

===Reply example===
- 📋 [Identifier]: <Specific content format description>
- 🎯 [Identifier]: <Specific content format description>
- 💡 [Identifier]: <Specific content format description>
===End of example===

### Skill 2: [Skill name]
1. [Execution steps1 - Describe trigger conditions and initial processing]
2. [Execution steps2 - Describe specific methods for obtaining and deepening information]
3. [Execution steps3 - Describe the specific requirements and format of the final output]

### Skill 3: [Skill name]
- [Core competency description - Describe the primary purpose and knowledge base of this skill]
- [Application method - Describe how to use this skill to provide services to users, including specific implementation methods]

## Workflow：
1. Describe the first step in the role workflow
2. Describe the second step of the role workflow
3. The third step of describing the role workflow

## Output format：
If you have specific requirements for the output format of the role, you can emphasize and give examples here to illustrate the desired output format


## limit：
1. **Strictly limit the scope of answers**: only answer questions related to character setting。
   - If the user asks a question that is not related to the role, the following fixed format must be used to reply：
     “Sorry, I can only answer questions related to [Character Setting]. Your question is not within the scope of the service.。”
   - Do not provide any answers unrelated to role settings。
2. Describe the constraints that characters need to follow during interactions2
3. Describe the constraints that characters need to follow during interactions3

The output must not contain any explanations or additional notes, and can only return content that conforms to the above format.。
  `,
}

const isStreaming = ref<boolean>(false) // YesNoInStreaming output
const isPaused = ref<boolean>(false) // YesNo pause
const fullContent = ref<string>('') // Full content cache
const currentDisplayIndex = ref<number>(0) // currentDisplay the character position of arrival
let streamTimer: number | null = null // timerQuote
const isOutputComplete = ref<boolean>(false)

// simulationStreaming outputtimer functionNumber
const startStreamingOutput = () => {
  if (streamTimer) {
    clearInterval(streamTimer)
  }

  isStreaming.value = true
  isPaused.value = false

  streamTimer = setInterval(() => {
    if (isApiComplete.value && !isPaused.value) {
      // renewshowcontent
      const currentAnswer = chatMessages.value[chatMessages.value.length - 1]
      if (currentAnswer && currentAnswer.role === 'ai') {
        currentAnswer.content = fullContent.value
      }
      stopStreaming()
      return
    }
    if (!isPaused.value && currentDisplayIndex.value < fullContent.value.length) {
      // Output 1-3characters each time, simulate realStreaming output
      const step = Math.min(3, fullContent.value.length - currentDisplayIndex.value)
      currentDisplayIndex.value += step

      // renewshowcontent
      const currentAnswer = chatMessages.value[chatMessages.value.length - 1]
      if (currentAnswer && currentAnswer.role === 'ai') {
        currentAnswer.content = fullContent.value.substring(0, currentDisplayIndex.value)
      }
    } else if (loading.value === false && currentDisplayIndex.value >= fullContent.value.length) {
      stopStreaming()
    }
  }, 50) as any
}

// stopStreaming output
const stopStreaming = () => {
  if (streamTimer) {
    clearInterval(streamTimer)
    streamTimer = null
  }
  isStreaming.value = false
  isPaused.value = false
  loading.value = false
  isOutputComplete.value = true
}

const showStopButton = computed(() => {
  return isStreaming.value
})

// pauseStreaming output
const pauseStreaming = () => {
  isPaused.value = true
  isStreaming.value = false
}

// ContinueStreaming output
const continueStreaming = () => {
  if (currentDisplayIndex.value < fullContent.value.length) {
    startStreamingOutput()
  }
}

/**
 * getOne piece recursive functionNumber,ProcessingstreamingNumberAccording to
 * @param chat    Each itemConversation record
 * @param reader  StreamNumberAccording to
 * @param stream  YesNo Yes StreamingNumberAccording to
 */
const getWrite = (reader: any) => {
  let tempResult = ''
  const middleAnswer = reactive({ content: '', role: 'ai' })
  chatMessages.value.push(middleAnswer)

  // Initialize state and
  fullContent.value = ''
  currentDisplayIndex.value = 0
  isOutputComplete.value = false

  let streamingStarted = false

  /**
   *
   * @param done  YesnoFinish
   * @param value value
   */
  const write_stream = ({ done, value }: { done: boolean; value: any }) => {
    try {
      if (done) {
        // StreamNumberAccording toThe reception is completed, but the timer continues to run until arrival is displayed.allcontent
        loading.value = false
        isApiComplete.value = true
        return
      }
      const decoder = new TextDecoder('utf-8')
      let str = decoder.decode(value, { stream: true })
      // Explain here start causeforNumberAccording toThe stream Return stream does notYesaccording toAccording toBackendchunkReturn We hope to arrivechunkYesdata:{xxx}\n\n But Yes it is possible to getarriveYes data:{ -> xxx}\n\n All in all,Yes fetchThere is no guarantee that every pieceschunk is said to bedata:Start \n\nFinish
      tempResult += str
      const split = tempResult.match(/data:.*}\n\n/g)
      if (split) {
        str = split.join('')
        tempResult = tempResult.replace(str, '')
      } else {
        return reader.read().then(write_stream)
      }
      // Explain here end
      if (str && str.startsWith('data:')) {
        if (split) {
          for (const index in split) {
            const chunk = JSON?.parse(split[index].replace('data:', ''))
            if (chunk.error) {
              loading.value = false
              stopStreaming()
              middleAnswer.content = chunk.error
              return Promise.reject(new Error(chunk.error))
            }
            if (!chunk.is_end) {
              // Real-time Will newly receivedcontentAdd toarrivewholecontentMedium
              fullContent.value += chunk.content
              if (!streamingStarted) {
                streamingStarted = true
                startStreamingOutput()
              }
            }
            if (chunk.is_end) {
              return Promise.resolve()
            }
          }
        }
      }
    } catch (e) {
      loading.value = false
      stopStreaming()
      return Promise.reject(e)
    }
    return reader.read().then(write_stream)
  }

  return write_stream
}
const isApiComplete = ref<boolean>(false)
const answer = computed(() => {
  const result = chatMessages.value[chatMessages.value.length - 1]

  if (result && result.role == 'ai') {
    return result.content
  }
  return ''
})

// according toButton state calculation
const showContinueButton = computed(() => {
  return (
    !isStreaming.value && isPaused.value && currentDisplayIndex.value < fullContent.value.length
  )
})

function generatePrompt(inputValue: any) {
  isApiComplete.value = false
  loading.value = true
  const workspaceId = user.getWorkspaceId() || 'default'
  chatMessages.value.push({ content: inputValue, role: 'user' })
  const requestData = {
    messages: chatMessages.value,
    prompt: promptTemplates.INIT_TEMPLATE,
  }
  if (apiType.value === 'workspace') {
    generatePromptAPI
      .generate_prompt(workspaceId, modelID.value, applicationID.value, requestData)
      .then((response) => {
        nextTick(() => {
          if (dialogScrollbar.value) {
            // WillThe scroll bar scrolls to the bottom of arrival
            scrollDiv.value.setScrollTop(getMaxHeight())
          }
        })
        const reader = response.body.getReader()
        reader.read().then(getWrite(reader))
      })
  } else if (apiType.value === 'systemManage') {
    systemGeneratePromptAPI
      .generate_prompt(applicationID.value, modelID.value, requestData)
      .then((response) => {
        nextTick(() => {
          if (dialogScrollbar.value) {
            // WillThe scroll bar scrolls to the bottom of arrival
            scrollDiv.value.setScrollTop(getMaxHeight())
          }
        })
        const reader = response.body.getReader()
        reader.read().then(getWrite(reader))
      })
  }
}

// Regenerate click
const reAnswerClick = () => {
  if (originalUserInput.value) {
    generatePrompt(
      `The last answer was not satisfactory. Please target the originalProblem"${originalUserInput.value}"and combineConversation record，Strictaccording toRe-according to Format specificationsgenerate。`,
    )
  }
}

const quickInputRef = ref()

const handleSubmit = (event?: any) => {
  if (!event?.ctrlKey && !event?.shiftKey && !event?.altKey && !event?.metaKey) {
    // likeIf notaccording toIf you press the key combination, the default event will be blocked.
    event?.preventDefault()
    if (!inputValue.value.trim() || loading.value || isStreaming.value) {
      return
    }
    if (!originalUserInput.value) {
      originalUserInput.value = inputValue.value
    }
    if (isPaused.value || isStreaming.value) {
      return
    }
    if (inputValue.value) {
      generatePrompt(inputValue.value)
      inputValue.value = ''
    }
  } else {
    // likefruit at the same timeaccording toDownctrl/shift/cmd/opt +enter，will wrap
    insertNewlineAtCursor(event)
  }
}
const insertNewlineAtCursor = (event?: any) => {
  const textarea = quickInputRef.value.$el.querySelector(
    '.el-textarea__inner',
  ) as HTMLTextAreaElement
  const startPos = textarea.selectionStart
  const endPos = textarea.selectionEnd
  // Block the default line for (avoid extra line breaks）
  event.preventDefault()
  // InInsert newline character at cursor
  inputValue.value = inputValue.value.slice(0, startPos) + '\n' + inputValue.value.slice(endPos)
  nextTick(() => {
    textarea.setSelectionRange(startPos + 1, startPos + 1) // Cursor position after arrival line break
  })
}

const open = (modelId: string, applicationId: string) => {
  modelID.value = modelId
  applicationID.value = applicationId
  dialogVisible.value = true
  originalUserInput.value = ''
  chatMessages.value = []
}

const scrollDiv = ref()
const dialogScrollbar = ref()

const getMaxHeight = () => {
  return dialogScrollbar.value!.scrollHeight
}

/**
 * Processingfollow scroll bar
 */
const handleScroll = () => {
  if (scrollDiv.value) {
    // The inner height is less than the outer height It requires a scroll bar
    if (scrollDiv.value.wrapRef.offsetHeight < dialogScrollbar.value?.scrollHeight) {
      // likeIf the distance between the current scroll bar and the bottomIn Specify the distance The scroll bar will follow
      scrollDiv.value.setScrollTop(getMaxHeight())
    }
  }
}

const handleDialogClose = (done: () => void) => {
  if (answer.value) {
    // pop up Messages
    MsgConfirm(t('common.tip'), t('views.application.generateDialog.exit'), {
      confirmButtonText: t('common.confirm'),
      cancelButtonText: t('common.cancel'),
      distinguishCancelAndClose: true,
    })
      .then(() => {
        // Click to confirm，Clearstate
        stopStreaming()
        chatMessages.value = []
        fullContent.value = ''
        currentDisplayIndex.value = 0
        isOutputComplete.value = false
        done() // Real close
      })
      .catch(() => {
        // ClickCancel
      })
  } else {
    done()
  }
}

// ComponentsClean up timer when uninstalling
onUnmounted(() => {
  stopStreaming()
})

watch(
  answer,
  () => {
    handleScroll()
  },
  { deep: true, immediate: true },
)

defineExpose({
  open,
})
</script>

<style lang="scss" scoped>
.generate-prompt-dialog-bg {
  background: var(--dialog-bg-gradient-color);
  overflow: hidden;
  box-sizing: border-box;
}

.generate-prompt-operate {
  position: relative;
  width: 100%;
  box-sizing: border-box;
  z-index: 10;

  :deep(.operate-textarea) {
    box-shadow: 0px 6px 24px 0px rgba(var(--el-text-color-primary-rgb), 0.08);
    background-color: #ffffff;
    border-radius: var(--app-border-radius-large);
    border: 1px solid #ffffff;
    box-sizing: border-box;

    &:has(.el-textarea__inner:focus) {
      border: 1px solid var(--el-color-primary);
    }

    .el-textarea__inner {
      border-radius: var(--app-border-radius-large) !important;
      box-shadow: none;
      resize: none;
      padding: 13px 16px;
      box-sizing: border-box;
      min-height: 47px !important;
      height: 0;
    }

    .operate {
      padding: 6px 10px;

      .el-icon {
        font-size: 20px;
      }

      .sent-button {
        max-height: none;

        .el-icon {
          font-size: 24px;
        }
      }

      .el-loading-spinner {
        margin-top: -15px;

        .circular {
          width: 31px;
          height: 31px;
        }
      }
    }
  }
  .video-stop-button {
    box-shadow: 0px 6px 24px 0px rgba(var(--el-text-color-primary-rgb), 0.08);

    &:hover {
      background: #ffffff;
    }
  }
}
</style>
