export default {
  node: 'node',
  nodeName: 'Node name',
  baseComponent: 'Basic components',
  nodeSetting: 'Node settings',
  workflow: 'Workflow',
  knowledgeWorkflow: 'Knowledge base workflow',
  info: {
    previewVersion: 'preview version：',
    saveTime: 'save time：',
  },
  operation: {
    toImportDoc: 'Go to import document',
    importWorkflow: 'Import workflow',
    exportWorkflow: 'Export workflow',
  },
  setting: {
    restoreVersion: 'recovery version',
    restoreCurrentVersion: 'Restore this version',
    addComponent: 'Add component',
    releaseHistory: 'Release history',
    autoSave: 'Auto save',
    latestRelease: 'Recently published',
    copyParam: 'Copy parameters',
    exit: 'Exit directly',
    exitSave: 'Save and exit',
    templateCenter: 'Template Center',
  },
  tip: {
    noData: 'No relevant results found',
    nameMessage: 'name cannot be empty！',
    onlyRight: 'Only allow connections from the right anchor point',
    notRecyclable: 'Not loopable',
    onlyLeft: 'Only the left anchor point is allowed to be connected',
    applicationNodeError: 'The agent is not available',
    toolNodeError: 'This function is not available',
    repeatedNodeError: 'Node name already exists！',
    cannotCopy: 'cannot be copied',
    copyError: 'Node copied',
    paramErrorMessage: 'Parameter already exists: ',
    saveMessage: 'The current modification is not saved，Whether to save and exit？',
    searchPlaceholder: 'Please enter the node name',
    disabled: 'The node has been disabled',
  },
  delete: {
    confirmTitle: 'Confirm to delete this node？',
    deleteMessage: 'Nodes are not allowed to be deleted',
  },
  control: {
    zoomOut: 'zoom out',
    zoomIn: 'enlarge',
    fitView: 'Adapt',
    retract: 'Collapse all nodes',
    extend: 'Expand all nodes',
    beautify: 'Beautify with one click',
  },
  variable: {
    global: 'global variables',
    chat: 'session variables',
    Referencing: 'reference variable',
    ReferencingRequired: 'Reference variable required',
    ReferencingError: 'Reference variable error',
    NoReferencing: 'non-existent reference variable',
    placeholder_key: 'Please enter key name',
    placeholder: 'Please select a variable',
    inputPlaceholder: 'Please enter variables',
    loop: 'loop variable',
  },
  condition: {
    title: 'Execution conditions',
    front: 'prefix',
    AND: 'all',
    OR: 'any',
    text: 'The connection node is executed，Execute current node',
  },
  validate: {
    startNodeRequired: 'Start node required',
    startNodeOnly: 'There can only be one start node',
    baseNodeRequired: 'Basic information node is required',
    baseNodeOnly: 'There can only be one basic information node',
    notInWorkFlowNode: 'Nodes not in the process',
    noNextNode: 'The next node does not exist',
    nodeUnavailable: 'Node is unavailable',
    needConnect1: 'Nodal',
    needConnect2: 'Branches need to be connected',
    cannotEndNode: 'Node cannot be used as an end node',
    loopNodeBreakNodeRequired: 'Infinite loop must exist Break node',
  },
  nodes: {
    toolWorlflowNode: {
      label: 'Workflow tools',
      text: 'Workflow tools',
    },
    knowledgeWriteNode: {
      label: 'Knowledge base writing',
      text: 'Write the input segmented list to the current knowledge base，and complete the vectorization process',
    },
    dataSourceWebNode: {
      label: 'Web website',
      text: 'Enter the root address to automatically crawlWebdata（Single link corresponds to single document），Output a document list with content',
      field_label: 'file list',
    },
    dataSourceLocalNode: {
      label: 'local file',
      text: 'Upload local files，Output file list（Dont parse content，Need to cooperate “Document content extraction” Node parsing）',
      fileList: 'file list',
      fileFormat: {
        label: 'Supported file formats',
        requiredMessage: 'Please select file format',
      },
      maxFileNumber: {
        label: 'Maximum number of files uploaded per time',
      },
      maxFileCountNumber: {
        label: 'Each document uploaded has a maximum(MB)',
      },
    },
    classify: {
      aiCapability: 'AI ability',
      businessLogic: 'business logic',
      dataProcessing: 'Data processing',
    },
    startNode: {
      label: 'Start',
      question: 'User issues',
      currentTime: 'current time',
    },
    baseNode: {
      visibilitySetting: {
        label: 'Visibility setting',
        showCondition‌: 'display conditions',
        hideCondition‌: 'Hidden conditions',
      },
      fileUpload: {
        label: 'File upload',
        tooltip: 'After opening，The Q&A page will display a button to upload files。',
      },
      FileUploadSetting: {
        title: 'File upload settings',
        maxFiles: 'Maximum number of files uploaded at a time',
        fileLimit: 'Max per file（MB）',
        fileUploadType: {
          label: 'Uploaded file type',
          documentText: 'Need to use「Document content extraction」Node parses document content',
          imageText: 'Need to use「Picture understanding」Node parses image content',
          videoText: 'Need to use「video understanding」Node parses video content',
          audioText: 'Need to use「speech to text」Node parses audio content',
          uploadMethod: 'Upload method',
        },
      },
    },
    KnowledgeBaseNode: {
      DocumentSetting: 'Document processing settings',
    },
    aiChatNode: {
      label: 'AI dialogue',
      text: 'and AI Large model for conversation',
      answer: 'AI Answer content',
      vision: {
        label: 'Vision',
      },
      returnContent: {
        label: 'Return content',
        tooltip: `After closing, the content of the node will not be output to the user.。
                  If you want the user to see the output of this node，Please turn on the switch。`,
      },
      defaultPrompt: 'known information',
      think: 'thought process',
      historyMessage: 'Chat history',
    },
    searchKnowledgeNode: {
      label: 'Knowledge base search',
      text: 'Related knowledge base，Find segments related to your question',
      paragraph_list: 'Segmented list of search results',
      is_hit_handling_method_list: 'Segmented list that satisfies direct answer',
      result: 'Search results',
      directly_return: 'Paragraph content that satisfies direct answers',
      searchParam: 'Retrieval parameters',
      showKnowledge: {
        label: 'Results are displayed in the knowledge source',
        requiredMessage: 'Please set parameters',
      },
      searchQuestion: {
        label: 'Search questions',
        placeholder: 'Please select a search question',
        requiredMessage: 'Please select a search question',
      },
    },
    searchDocumentNode: {
      label: 'Document tag retrieval',
      text: 'From the set search range，Retrieve documents that meet the conditions based on document tags',
      selectKnowledge: 'Search scope',
      searchSetting: 'Search settings',
      custom: 'Manual',
      customTooltip: 'Manually set label filters',
      auto: 'automatic',
      autoTooltip: 'Automatically match document tags based on search questions',
      documentList: 'Document list',
      knowledgeList: 'Knowledge base list',
      result: 'Search results',
      searchParam: 'Retrieval parameters',
      select_variable: 'Select variables',
      valueMessage: `value or variable`,

      searchQuestion: {
        label: 'Search questions',
        placeholder: 'Please select a search question',
        requiredMessage: 'Please select a search question',
      },
    },
    questionNode: {
      label: 'Problem optimization',
      text: 'Optimize and improve current issues based on historical chat records，More conducive to matching knowledge base segments',
      result: 'Problem optimization results',
      systemDefault: `# Role
You are a problem optimization master，Good at accurately guessing user intentions based on context，and optimize issues raised by users。

## Skill
### Skill 1: optimization problem
2. Problems receiving user input。
3. Carefully analyze the meaning of the question based on the context。
4. Output optimized problems。

## limit:
- Return only optimized questions，No additional explanation or explanation。
- Ensure that the optimized problem accurately reflects the original problem intent，Do not change your original intention。`,
    },
    conditionNode: {
      label: 'Judger',
      text: 'Execute different nodes based on different conditions',
      branch_name: 'branch name',
      conditions: {
        label: 'condition',
        info: 'Meet the following',
        requiredMessage: 'Please select conditions',
      },
      valueMessage: 'Please enter a value',
      addCondition: 'Add conditions',
      addBranch: 'add branch',
    },
    replyNode: {
      label: 'Specify reply',
      text: 'Specify reply content，Reference variables will be converted to strings for output',
      replyContent: 'Reply content',
    },
    rerankerNode: {
      label: 'Multiple recall',
      text: 'Use the rearrangement model to perform secondary recall of search results from multiple knowledge bases',
      result_list: 'Reorder result list',
      result: 'Rearrange results',
      rerankerContent: {
        label: 'Rearrange content',
        requiredMessage: 'Please select content to rearrange',
      },
      higher: 'higher than',
      ScoreTooltip: 'Score The higher the correlation, the stronger the correlation。',
      max_paragraph_char_number: 'Maximum number of quoted characters',
      reranker_model: {
        label: 'rearrange model',
        placeholder: 'Please select a rearrangement model',
      },
    },
    formNode: {
      label: 'Form collection',
      text: 'Used to collect user information during the question and answer process，Subsequent processes can be executed based on the collected form data.',
      form_content_format1: 'Hello，Please fill in the form below first：',
      form_content_format2: 'After filling in, please click【submit】button to submit。',
      form_data: 'All contents of the form',
      formContent: {
        label: 'Form output content',
        requiredMessage: 'Please enter the form content',
        tooltip: 'Set the content output by executing the node，{ form } placeholder for the form。',
      },
      formAllContent: 'All contents of the form',
      formSetting: 'Form configuration',
    },
    documentExtractNode: {
      label: 'Document content extraction',
      text: 'Parse input document，Output structured document content',
      content: 'Document content',
    },
    documentSplitNode: {
      label: 'Document splitting',
      text: 'Split input document content by segmentation strategy，Output segmented text list',
      paragraphList: 'Segmented list',
      splitStrategy: {
        label: 'Staging strategy',
        placeholder: 'Please select a segmentation strategy',
        requiredMessage: 'Please select a segmentation strategy',
      },
      chunk_length: {
        label: 'Sub-block length',
        tooltip1: 'The core goal is to balance retrieval precision and recall efficiency',
        tooltip2:
          'Avoid splits that are too short：Monoblock＜50 Words easily lead to semantic fragmentation，The query intent may not be matched due to lack of context during retrieval.',
        tooltip3:
          'Avoid long splits：Monoblock＞500 words will add redundant information，Reduce search accuracy，and takes up more storage and computing resources',
      },
      title1: 'Section title is set to the associated question of the section',
      title2: 'Document name is set to segmented association issues',
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
    imageUnderstandNode: {
      label: 'Picture understanding',
      text: 'Identify objects in pictures、Scenarios and other information to answer user questions',
      answer: 'AI Answer content',
      model: {
        label: 'visual model',
        requiredMessage: 'Please select a visual model',
      },
      image: {
        label: 'Select picture',
        requiredMessage: 'Please select a picture',
      },
    },
    variableAssignNode: {
      label: 'variable assignment',
      text: 'Update the value of a global variable',
      assign: 'Assignment',
    },
    variableAggregationNode: {
      label: 'variable aggregation',
      text: 'Aggregate variables for each group by aggregation strategy',
      Strategy: 'aggregation strategy',
      placeholder: 'Returns the first non-null value of each group',
      placeholder1: 'Returns an array for each set of variables（Array）',
      placeholder2: 'Returns a dictionary for each set of variables（Dict）',
      group: {
        noneError: 'Name cannot be empty',
        dupError: 'Name cannot be repeated',
      },
      addGroup: 'Add group',
      editGroup: 'Edit group',
    },
    mcpNode: {
      label: 'MCP call',
      text: 'pass through SSE/Streamable HTTP method execution MCP Tools in service',
      getToolsSuccess: 'Obtain tool successfully',
      getTool: 'Get tools',
      toolParam: 'Tool parameters',
      mcpServerTip: 'Please enter JSON Formatted MCP Server configuration',
      mcpToolTip: 'Please select a tool',
      configLabel: 'MCP Server Config (Only supportsSSE/Streamable HTTP Calling method)',
      reference: 'QuoteMCP',
    },
    imageGenerateNode: {
      label: 'Image generation',
      text: 'Generate images based on provided text content',
      answer: 'AI Answer content',
      model: {
        label: 'Image generation model',
        requiredMessage: 'Please select an image generation model',
      },
      prompt: {
        label: 'prompt word(forward)',
        tooltip: 'positive cue words，Used to describe the elements and visual characteristics expected to be included in the generated image',
      },
      negative_prompt: {
        label: 'prompt word(Negative)',
        tooltip: 'reverse prompt word，Used to describe content you do not want to see in the screen，Screens can be restricted。',
        placeholder: 'Please describe the image content you do not want to generate，for example：color、Gory content',
      },
    },
    textToVideoGenerate: {
      label: 'Vincent Video',
      text: 'Generate a video based on the provided text content',
      answer: 'AI Answer content',
      model: {
        label: 'Vincent film model',
        requiredMessage: 'Please select Vincent video model',
      },
      prompt: {
        label: 'prompt word(forward)',
        tooltip: 'positive cue words，Used to describe the elements and visual characteristics expected to be included in the generated video',
      },
      negative_prompt: {
        label: 'prompt word(Negative)',
        tooltip: 'reverse prompt word，Used to describe content you dont want to see in a video，Videos can be restricted。',
        placeholder: 'Please describe the video content you do not want generated，For example：color、Gory content',
      },
    },
    imageToVideoGenerate: {
      label: 'Tusheng videos',
      text: 'Generate a video from the provided image',
      answer: 'AI Answer content',
      model: {
        label: 'Tusheng video model',
        requiredMessage: 'Please select Tusheng video model',
      },
      prompt: {
        label: 'prompt word(forward)',
        tooltip: 'positive cue words，Used to describe the elements and visual characteristics expected to be included in the generated video',
      },
      negative_prompt: {
        label: 'prompt word(Negative)',
        tooltip: 'reverse prompt word，Used to describe content you dont want to see in a video，Videos can be restricted。',
        placeholder: 'Please describe the video content you do not want generated，For example：color、Gory content',
      },
      first_frame: {
        label: 'First frame picture',
        requiredMessage: 'Please select the first frame picture',
      },
      last_frame: {
        label: 'Last frame picture',
        requiredMessage: 'Please select the last frame picture',
      },
    },
    speechToTextNode: {
      label: 'speech to text',
      text: 'Convert audio to text via speech recognition model',
      stt_model: {
        label: 'speech recognition model',
      },
      audio: {
        label: 'Select voice file',
        placeholder: 'Please select a voice file',
      },
    },
    textToSpeechNode: {
      label: 'text to speech',
      text: 'Convert text to audio using a speech synthesis model',
      tts_model: {
        label: 'speech synthesis model',
      },
      content: {
        label: 'Select text content',
      },
    },
    toolNode: {
      label: 'Custom tools',
      text: 'By executing a custom script，Implement data processing',
    },
    intentNode: {
      label: 'Intent recognition',
      text: 'Match user questions to user preset intent categories',
      error2: 'Intent to repeat',
      placeholder: 'Please select a category item',
      classify: {
        label: 'Intent classification',
      },
      input: {
        label: 'input',
      },
    },
    applicationNode: {
      label: 'agent node',
    },
    loopNode: {
      label: 'loop node',
      text: 'By setting the number of loops and logic，Repeat a series of tasks',
      loopType: {
        label: 'Loop type',
        requiredMessage: 'Please select cycle type',
        arrayLoop: 'array loop',
        numberLoop: 'Loop a specified number of times',
        infiniteLoop: 'infinite loop',
      },
      loopNumber: {
        label: 'Number of cycles',
        requiredMessage: 'Please fill in the number of cycles',
      },
      loopArray: {
        label: 'loop array',
        requiredMessage: 'Loop array required',
        placeholder: 'Please select loop array',
      },
      loopSetting: 'Cycle settings',
      loopDetail: 'Loop details',
    },
    loopStartNode: {
      label: 'Loop starts',
      loopIndex: 'subscript',
      loopItem: 'loop element',
    },
    loopBodyNode: { label: 'loop body', text: 'loop body' },
    loopContinueNode: {
      label: 'Continue',
      text: 'Used to terminate the current loop，Execute next cycle',
      isContinue: 'Continue',
    },
    loopBreakNode: { label: 'Break', text: 'Terminate current loop，Jump out of the loop', isBreak: 'Break' },
    variableSplittingNode: {
      label: 'variable splitting',
      text: 'via configuration JSON Path expression，for input JSON Format variables are parsed and split',
      result: 'result',
      splitVariables: 'split variable',
      inputVariables: 'input variables',
      addVariables: 'Add variables',
      editVariables: 'Edit variables',
      variableListPlaceholder: 'Please add folding variables',
      expression: {
        label: 'expression',
        placeholder: 'Please enter an expression',
        tooltip:
          'Please use JSON Path expression split variable，For example：$.store.book <a href="https://pypi.org/project/jsonpath-ng/1.8.0/" target="_blank" class="expression_tip">Click to view details ➜ pypi.org</a>',
      },
    },
    parameterExtractionNode: {
      label: 'Parameter extraction',
      text: 'use AI Model extracts structured parameters',
      extractParameters: {
        label: 'Extract parameters',
        variableListPlaceholder: 'Please add selection parameters',
        parameterType: 'Parameter type',
      },
    },
  },
  compare: {
    is_null: 'is empty',
    is_not_null: 'Not empty',
    contain: 'Include',
    not_contain: 'Not included',
    eq: 'equal to',
    not_eq: 'not equal to',
    ge: 'Greater than or equal to',
    gt: 'greater than',
    le: 'less than or equal to',
    lt: 'less than',
    len_eq: 'The length is equal to',
    len_ge: 'length greater than or equal to',
    len_gt: 'length greater than',
    len_le: 'length less than or equal to',
    len_lt: 'length less than',
    is_true: 'is true',
    is_not_true: 'not true',
    regex: 'Regular match',
    wildcard: 'wildcard matching',
  },
  SystemPromptPlaceholder: 'System prompt word，You can reference variables in the system：like',
  UserPromptPlaceholder: 'User prompt words，You can reference variables in the system：like',
  initiator: 'initiator',
  abnormalInformation: 'Exception information',
}
