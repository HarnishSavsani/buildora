export default {
  node: 'Node',
  nodeName: 'NodeName',
  baseComponent: 'BaseComponents',
  nodeSetting: 'NodeSettings',
  workflow: 'Workflow',
  knowledgeWorkflow: 'knowledge baseWorkflow',
  info: {
    previewVersion: 'PreviewVersion：',
    saveTime: 'save time：',
  },
  operation: {
    toImportDoc: 'goimportDocumentation',
    importWorkflow: 'importWorkflow',
    exportWorkflow: 'ExportWorkflow',
  },
  setting: {
    restoreVersion: 'RecoveryVersion',
    restoreCurrentVersion: 'restore thisVersion',
    addComponent: 'Add toComponents',
    releaseHistory: 'Publishhistory',
    autoSave: 'Auto save',
    latestRelease: 'recentPublish',
    copyParam: 'Copyparameter',
    exit: 'Exit directly',
    exitSave: 'Save and exit',
    templateCenter: 'Template Center',
  },
  tip: {
    noData: 'No results found related to arrival',
    nameMessage: 'NameCharactercannot be empty！',
    onlyRight: 'Only allow connections from the right anchor point',
    notRecyclable: 'Not loopable',
    onlyLeft: 'Only the anchor point on the left side of connect is allowed',
    applicationNodeError: 'ShouldAgentNot available',
    toolNodeError: 'ShouldtoolNot available',
    repeatedNodeError: 'NodeNameAlready exists！',
    cannotCopy: 'cannot beCopy',
    copyError: 'alreadyCopyNode',
    paramErrorMessage: 'parameterAlready exists: ',
    saveMessage: 'currentThe changes have not been saved, Yes or No to save and exit.?',
    searchPlaceholder: 'Please enterNodeName',
    disabled: 'The node has been disabled',
  },
  delete: {
    confirmTitle: 'Confirm that Delete shouldNode？',
    deleteMessage: 'NodeNot allowedDelete',
  },
  control: {
    zoomOut: 'zoom out',
    zoomIn: 'enlarge',
    fitView: 'adapt',
    retract: 'closeallNode',
    extend: 'ExpandallNode',
    beautify: 'Beautify with one click',
  },
  variable: {
    global: 'global variables',
    chat: 'session variables',
    Referencing: 'Quotevariable',
    ReferencingRequired: 'QuotevariableRequired',
    ReferencingError: 'QuotevariableError',
    NoReferencing: 'Does not existQuotevariable',
    placeholder_key: 'Please enterKey name',
    placeholder: 'Please select variables',
    inputPlaceholder: 'Please entervariable',
    loop: 'Loop variable',
  },
  condition: {
    title: 'implementcondition',
    front: 'prefix',
    AND: 'all',
    OR: 'any',
    text: 'After the connection Node is executed, executecurrentNode',
  },
  validate: {
    startNodeRequired: 'StartNodeRequired',
    startNodeOnly: 'StartNodeThere can only be onepieces',
    baseNodeRequired: 'BasicinformationNodeRequired',
    baseNodeOnly: 'There can only be one basic informationNodepieces',
    notInWorkFlowNode: 'Not In Process MediumNode',
    noNextNode: 'Does not existNextpiecesNode',
    nodeUnavailable: 'NodeNot available',
    needConnect1: 'Nodal',
    needConnect2: 'BranchNeed to connect',
    cannotEndNode: 'Nodecannot be used as aFinishNode',
    loopNodeBreakNodeRequired: 'Infinite loop Must saveIn Break Node',
  },
  nodes: {
    toolWorlflowNode: {
      label: 'Workflow tools',
      text: 'Workflow tools',
    },
    knowledgeWriteNode: {
      label: 'knowledge basewrite',
      text: 'WillinputSegmented listwriteCurrent knowledge base，and completevectorizationProcessing',
    },
    dataSourceWebNode: {
      label: 'Web site',
      text: 'enterRoot addressAutomatic capture Web NumberAccording to（SingleThe link corresponds to SingleDocumentation), and the output contains contentDocument list',
      field_label: 'Document list',
    },
    dataSourceLocalNode: {
      label: 'local file',
      text: 'Upload local Documentation, outputDocument list（Not parsedcontent，Need to cooperate “Documentationcontentextract” Nodeparse）',
      fileList: 'file list',
      fileFormat: {
        label: 'Supported file formats',
        requiredMessage: 'Please selectFile format',
      },
      maxFileNumber: {
        label: 'Maximum upload per timedocumentNumber',
      },
      maxFileCountNumber: {
        label: 'Maximum uploaded piecesDocumentation per(MB)',
      },
    },
    classify: {
      aiCapability: 'AI ability',
      businessLogic: 'business logic',
      dataProcessing: 'NumberAccording toProcessing',
    },
    startNode: {
      label: 'Start',
      question: 'User Questions',
      currentTime: 'currentTime',
    },
    baseNode: {
      visibilitySetting: {
        label: 'Show and hideSettings',
        showCondition: 'showcondition',
        hideCondition: 'hidecondition',
      },
      fileUpload: {
        label: 'documentUpload',
        tooltip: 'After turning it on, the Q&A page will displayUpload fileofaccording tobutton。',
      },
      FileUploadSetting: {
        title: 'documentUploadSettings',
        maxFiles: 'SingleuploadedmostdocumentNumber',
        fileLimit: 'maximum per piecesdocument（MB）',
        fileUploadType: {
          label: 'UploadeddocumentType',
          documentText: 'Need to use“DocumentationcontentExtract "Node parsingDocumentationcontent',
          imageText: 'Need to use“Picture"Understanding" Node parsingPicturecontent',
          audioText: 'Need to use“Voice to text "Node analysisAudiocontent',
          videoText: 'Need to use“video understanding”NodeParse videocontent',
          otherText: 'Need to parse this by yourselfTypedocument',
          uploadMethod: 'Upload methods',
        },
      },
    },
    KnowledgeBaseNode: {
      DocumentSetting: 'DocumentationProcessingSettings',
    },
    aiChatNode: {
      label: 'AI Conversation',
      text: 'and AI Large ModelConversation',
      answer: 'AI Answer content',
      vision: {
        label: 'Vision',
      },
      returnContent: {
        label: 'Returncontent',
        tooltip: `After closing, the Nodalcontent will not be output toUsers。
                  likeIf you want Users to see the Nodal output content, please Open the switch.。`,
      },
      defaultPrompt: 'known information',
      think: 'Thinkingprocess',
      historyMessage: 'Chat history',
    },
    searchKnowledgeNode: {
      label: 'knowledge baseSearch',
      text: 'associationknowledge base，Find related to Problemsegmentation',
      paragraph_list: 'The search resultSegmented list',
      is_hit_handling_method_list: 'satisfydirect answerofSegmented list',
      result: 'Search results',
      directly_return: 'satisfydirect answerofsegmentationcontent',
      searchParam: 'Searchparameter',
      showKnowledge: {
        label: 'The results show In knowledgesourceMedium',
        requiredMessage: 'pleaseSettingsparameter',
      },
      searchQuestion: {
        label: 'SearchProblem',
        placeholder: 'Please select searchProblem',
        requiredMessage: 'Please select searchProblem',
      },
    },
    searchDocumentNode: {
      label: 'DocumentationTagsSearch',
      text: 'Retrieve RangeMedium from the setting, rootAccording toDocumentationTagsRetrieve those that satisfy conditionDocumentation',
      selectKnowledge: 'SearchRange',
      searchSetting: 'SearchSettings',
      custom: 'Manual',
      customTooltip: 'Manual SettingsTags filteringcondition',
      auto: 'automatic',
      autoTooltip: 'RootAccording toRetrieve Problem automaticallymatchDocumentationTags',
      documentList: 'Document list',
      knowledgeList: 'Knowledge base list',
      result: 'Search results',
      searchParam: 'Searchparameter',
      select_variable: 'Select variable',
      valueMessage: `valueorvariable`,
      searchQuestion: {
        label: 'SearchProblem',
        placeholder: 'Please select searchProblem',
        requiredMessage: 'Please select searchProblem',
      },
    },
    questionNode: {
      label: 'Problemoptimization',
      text: 'RootAccording toChat historyOptimize and improve currentProblem, which is more conducive tomatchknowledge basesegmentation',
      result: 'ProblemOptimization results',
      systemDefault: `# Role
You are a Problem optimization master, good at rootAccording tocontextAccurately guess Users’ intentions and optimize the Problems raised by Users。

## Skill
### Skill 1: optimizationProblem
2. Receive input from UsersProblem。
3. According toAccording tocontextCarefully analyze the meaning of Problem。
4. outputProblems after optimization。

## limit:
- onlyReturnProblems after optimization，No additional explanation or explanation。
- make sureProblems after optimizationAccurately reflect the original Problem intent and must not change the original intent.。`,
    },
    conditionNode: {
      label: 'Judger',
      text: 'RootAccording toDifferent conditions execute differentNode',
      branch_name: 'BranchName',
      conditions: {
        label: 'condition',
        info: 'Meet the following',
        requiredMessage: 'Please selectcondition',
      },
      valueMessage: 'Please entervalue',
      addCondition: 'Add tocondition',
      addBranch: 'add branch',
    },
    replyNode: {
      label: 'Specifyreply',
      text: 'Specify replycontent, Quote variable willConvert to stringperform output',
      replyContent: 'replycontent',
    },
    rerankerNode: {
      label: 'Multiple recall',
      text: 'userearrange modelTo manypiecesknowledge baseSearch results for secondary recall',
      result_list: 'Rearrange resultsList',
      result: 'Rearrange results',
      rerankerContent: {
        label: 'rearrangecontent',
        requiredMessage: 'Please select reordercontent',
      },
      higher: 'higher than',
      ScoreTooltip: 'Score The higher the correlation, the stronger。',
      max_paragraph_char_number: 'maximumQuotecharacterNumber',
      reranker_model: {
        label: 'rearrange model',
        placeholder: 'Please selectrearrange model',
      },
    },
    formNode: {
      label: 'TableSingleCollection',
      text: 'InThe question and answer process Medium is used to collect Users information, which can beAccording toCollectarriveForm dataExecute subsequent processes',
      form_content_format1: 'Hello，Please fill in the form below firstSinglecontent：',
      form_content_format2: 'Please click after filling in【submit】according tobutton to proceedsubmit。',
      form_data: 'surfaceSingleallcontent',
      formContent: {
        label: 'Form output content',
        requiredMessage: 'pleaseForm output content',
        tooltip: 'SettingsExecute the Node outputcontent，{ form } forPlaceholder for table Single。',
      },
      formAllContent: 'surfaceSingleallcontent',
      formSetting: 'Form configuration',
    },
    documentExtractNode: {
      label: 'Documentationcontentextract',
      text: 'Parse the input Documentation and output a structuredDocumentationcontent',
      content: 'Documentationcontent',
    },
    documentSplitNode: {
      label: 'Documentationsegmentation',
      text: 'according toStaging strategySplit input Documentationcontent, outputsegmentationtextList',
      paragraphList: 'Segmented list',
      splitStrategy: {
        label: 'Staging strategy',
        placeholder: 'Please selectStaging strategy',
        requiredMessage: 'Please selectStaging strategy',
      },
      chunk_length: {
        label: 'Sub-block length',
        tooltip1: 'Core TargetYes balances retrieval precision and recall efficiency',
        tooltip2:
          'Avoid too short splits: Single block＜50 CharacterIt can easily lead to semantic fragmentation, and the Query intent may not be matched due to lack of context during retrieval.',
        tooltip3:
          'Avoid overly long splits: Single block＞500 CharacterIt will increase redundant information, reduce retrieval accuracy, and occupy more storage and calculations.resource',
      },
      title1: 'Section titleSettingsforsegmentationofRelated questions',
      title2: 'Document nameSettingsforsegmentationofRelated questions',
    },
    imageUnderstandNode: {
      label: 'Pictureunderstand',
      text: 'Recognize the PictureMedium object、Scenarios and other information to answer user questions',
      answer: 'AI Answer content',
      model: {
        label: 'visual model',
        requiredMessage: 'Please select a visual model',
      },
      image: {
        label: 'choosePicture',
        requiredMessage: 'Please selectPicture',
      },
    },
    variableAggregationNode: {
      label: 'variable aggregation',
      text: 'according toaggregation strategyAggregate variables of each group',
      Strategy: 'aggregation strategy',
      placeholder: 'ReturnThe first pieces of each group are not emptyvalue',
      placeholder1: 'ReturnNumber group of each group of variables（Array）',
      placeholder2: 'ReturnCharacter dictionary for each group of variables（Dict）',
      group: {
        noneError: 'Namecannot be empty',
        dupError: 'The name cannot be repeated',
      },
      addGroup: 'Add toGroup',
      editGroup: 'editGroup',
    },
    variableAssignNode: {
      label: 'variable assignmentvalue',
      text: 'renewglobal variablesvalue',
      assign: 'Assignmentvalue',
    },
    mcpNode: {
      label: 'MCP Call',
      text: 'pass SSE/Streamable HTTP Ways to execute MCP service Mediumtool',
      getToolsSuccess: 'Get toolssuccess',
      getTool: 'Get tools',
      toolParam: 'Tool parameters',
      mcpServerTip: 'Please enter JSON FormattedMCPserverConfiguration',
      mcpToolTip: 'Please selecttool',
      configLabel: 'MCP Server Config (onlysupport SSE/Streamable HTTP CallWay)',
      reference: 'QuoteMCP',
    },
    imageGenerateNode: {
      label: 'Image generation',
      text: 'RootAccording tomention fortext contentgeneratePicture',
      answer: 'AI Answer content',
      model: {
        label: 'Image generationModel',
        requiredMessage: 'Please selectImage generationModel',
      },
      prompt: {
        label: 'Prompt words(forward)',
        tooltip: 'forwardPrompt words，Used to describegenerate image Medium expected Elements and visual characteristics of Include',
      },
      negative_prompt: {
        label: 'Prompt words(Negative)',
        tooltip: 'reversePrompt words，Used to describe the content that you don\'t want In Screen Medium to see the arrival, you can modify the screenlimit。',
        placeholder: 'Please describe if you don’t want to generatePicturecontent，for example：color、bloodycontent',
      },
    },
    textToVideoGenerate: {
      label: 'Vincent Video',
      text: 'RootAccording tomention fortext contentgeneratevideo',
      answer: 'AI Answer content',
      model: {
        label: 'Vincent VideoModel',
        requiredMessage: 'Please selectVincent VideoModel',
      },
      prompt: {
        label: 'Prompt words(forward)',
        tooltip: 'forwardPrompt words，Used to describegenerate the elements and visual characteristics of the video Medium expects to include',
      },
      negative_prompt: {
        label: 'Prompt words(Negative)',
        tooltip: 'reversePrompt words，Used to describe the content that you do not want In Video Medium to see the arrival, you can perform the videolimit。',
        placeholder: 'Please describe the video that you do not want to generatecontent，for example：color、bloodycontent',
      },
    },
    videoUnderstandNode: {
      label: 'video understanding',
      text: 'Identify objects in videos、Scenarios and other information to answer user questions',
      answer: 'AI Answer content',
      model: {
        label: 'visual model',
        requiredMessage: 'Please select a visual model',
      },
      video: {
        label: 'Select video',
        requiredMessage: 'Please select a video',
      },
    },
    imageToVideoGenerate: {
      label: 'Tusheng video',
      text: 'RootAccording tomention forImage generationvideo',
      answer: 'AI Answer content',
      model: {
        label: 'Tusheng videoModel',
        requiredMessage: 'Please selectTusheng videoModel',
      },
      prompt: {
        label: 'Prompt words(forward)',
        tooltip: 'forwardPrompt words，Used to describegenerate the elements and visual characteristics of the video Medium expects to include',
      },
      negative_prompt: {
        label: 'Prompt words(Negative)',
        tooltip: 'reversePrompt words，Used to describe the content that you do not want In Video Medium to see the arrival, you can perform the videolimit。',
        placeholder: 'Please describe the video that you do not want to generatecontent，for example：color、bloodycontent',
      },
      first_frame: {
        label: 'First framePicture',
        requiredMessage: 'Please select the first framePicture',
      },
      last_frame: {
        label: 'last framePicture',
        requiredMessage: 'Please select the last framePicture',
      },
    },
    speechToTextNode: {
      label: 'voice to speechtext',
      text: 'WillAudiopassspeech recognition modelConvert totext',
      stt_model: {
        label: 'speech recognition model',
      },
      audio: {
        label: 'Select voicedocument',
        placeholder: 'Please select voicedocument',
      },
    },
    textToSpeechNode: {
      label: 'textConvert to voice',
      text: 'Willtextpassspeech synthesisModelConvert toAudio',
      tts_model: {
        label: 'speech synthesisModel',
      },
      content: {
        label: 'choosetext content',
      },
    },
    toolNode: {
      label: 'Customizetool',
      text: 'By executing the Customize script, achieveNumberAccording toProcessing',
    },
    intentNode: {
      label: 'Intent recognition',
      text: 'WillUser QuestionsPerform with Users\' default intent classificationmatch',
      error2: 'Intent to repeat',
      placeholder: 'Please select a category item',
      classify: {
        label: 'Intent classification',
      },
      input: {
        label: 'enter',
      },
    },
    applicationNode: {
      label: 'AgentNode',
    },
    loopNode: {
      label: 'cycleNode',
      text: 'Loop Numberand logic through Settings to repeatedly perform a series of tasks.',
      loopType: {
        label: 'cycleType',
        requiredMessage: 'Please select cycleType',
        arrayLoop: 'Numbergroup loop',
        numberLoop: 'Specify Number times to loop',
        infiniteLoop: 'Infinite loop',
      },
      loopNumber: {
        label: 'Loop timesNumber',
        requiredMessage: 'Loop timesNumberRequired',
      },
      loopArray: {
        label: 'Loop Number group',
        requiredMessage: 'Loop Number groupRequired',
        placeholder: 'Please select the loop Number group',
      },
      loopSetting: 'cycleSettings',
      loopDetail: 'cycleDetails',
    },
    loopStartNode: {
      label: 'cycleStart',
      loopIndex: 'subscript',
      loopItem: 'Loop element',
    },
    loopBodyNode: {
      label: 'loop body',
      text: 'loop body',
    },
    loopContinueNode: {
      label: 'Continue',
      text: 'Used to terminate the current loop and execute the next loop',
      isContinue: 'Continue',
    },
    loopBreakNode: {
      label: 'Break',
      text: 'Terminate the current loop and jump out of the loop body',
      isBreak: 'Break',
    },
    variableSplittingNode: {
      label: 'variable splitting',
      text: 'passConfigurationJSON Path expression, for input JSON FormatVariables are parsed and split',
      splitVariables: 'Split variables',
      inputVariables: 'input variables',
      addVariables: 'Add tovariable',
      editVariables: 'editvariable',
      variableListPlaceholder: 'pleaseAdd toSplit variables',
      expression: {
        label: 'Expression',
        placeholder: 'Please enterExpression',
        tooltip:
          'pleaseuse JSON Path Expression split variable，For example：$.store.book <a href="https://pypi.org/project/jsonpath-ng/1.8.0/" target="_blank" class="expression_tip">ClickViewDetails ➜ pypi.org</a>',
      },
    },
    parameterExtractionNode: {
      label: 'parameterextract',
      text: 'use AI ModelExtract structuredparameter',
      extractParameters: {
        label: 'extractparameter',
        variableListPlaceholder: 'pleaseAdd toextractparameter',
        parameterType: 'parameterType',
      },
    },
  },
  compare: {
    is_null: 'fornull',
    is_not_null: 'Not for empty',
    contain: 'Include',
    not_contain: 'Not included',
    eq: 'etc.At',
    not_eq: 'Not etc.',
    ge: 'Greater than etc. in',
    gt: 'Greater than',
    le: 'Less than etc. Yu',
    lt: 'less than',
    len_eq: 'Length etc. Yu',
    len_ge: 'length is greater than etc. in',
    len_gt: 'length greater than',
    len_le: 'The length is less than etc.',
    len_lt: 'length less than',
    is_true: 'forreal',
    is_not_true: 'Not true',
    regex: 'Regularmatch',
    wildcard: 'wildcard matching',
  },
  SystemPromptPlaceholder: 'systemPrompt words，Variables that can QuotesystemMedium：like',
  UserPromptPlaceholder: 'UsersPrompt words，Variables that can QuotesystemMedium：like',
  initiator: 'initiatepeople',
  abnormalInformation: 'differentofteninformation',
}
