export default {
  title: 'knowledge base',
  relatedApplications: 'associated agents',
  document_count: 'Number of documents',
  relatedApp_count: 'associated agents',
  setting: {
    vectorization: 'vectorization',
    sync: 'synchronous',
    tokenize: 'index',
  },
  tip: {
    professionalMessage: 'The social version supports the most 50 knowledge base，For more knowledge base，Please upgrade to professional version。',
    syncSuccess: 'Synchronization task sent successfully',
    updateModeMessage: 'After modifying the knowledge base vector model，Need to vectorize the knowledge base，Do you want to continue saving?？',
  },
  delete: {
    confirmTitle: 'Whether to delete the knowledge base：',
    confirmTitle2: 'knowledge base?',
    confirmMessage1: 'This knowledge base is associated with',
    confirmMessage2: 'agent，Unable to recover after deletion，Please operate with caution。',
    resourceCountMessage: 'This knowledge base is associated with {count} resources，Unable to use after deletion，Please operate with caution。',
  },
  knowledgeType: {
    label: 'Knowledge base type',
    generalKnowledge: 'Common knowledge base',
    webKnowledge: 'Web knowledge base',
    larkKnowledge: 'Feishu Knowledge Base',
    workflowKnowledge: 'Workflow knowledge base',
    yuqueKnowledge: 'Yuque knowledge base',
    generalInfo: 'Upload local file',
    webInfo: 'synchronous Web Website text data',
    larkInfo: 'Build a knowledge base through Feishu documents',
    yuqueInfo: 'Build a knowledge base through Yuque documents',
    createWorkflowKnowledge: 'Build a workflow knowledge base',
    workflowInfo: 'Build a knowledge base with custom workflow pipelines',
  },
  form: {
    knowledgeName: {
      label: 'Knowledge base name',
      placeholder: 'Please enter the knowledge base name',
      requiredMessage: 'Please enter the knowledge base name',
    },
    knowledgeDescription: {
      label: 'Knowledge base description',
      placeholder:
        'Describe the content of the knowledge base，A thorough description will helpAIHave an in-depth understanding of the content of this knowledge base，Content can be retrieved more accurately，Improve the hit rate of the knowledge base。',
      requiredMessage: 'Please enter a knowledge base description',
    },
    EmbeddingModel: {
      label: 'vector model',
      placeholder: 'Please select a vector model',
      requiredMessage: 'Please select a vector model',
    },

    source_url: {
      label: 'Web root address',
      placeholder: 'Please enter Web root address',
      requiredMessage: 'Please enter Web root address',
    },
    selector: {
      label: 'selector',
      placeholder: 'Default is body，Can be input .classname/#idname/tagname',
    },
    file_count_limit: {
      label: 'Maximum number of files uploaded at a time',
    },
    file_size_limit: {
      label: 'Maximum size of each file uploaded(MB)',
      placeholder: 'It is recommended to adjust according to the server configuration，Otherwise it will cause service downtime',
    },
    appTemplate: {
      blank: {
        title: 'Create blank',
      },
      basic: {
        title: 'Basic template',
        description: 'Support local files、Feishu Documents、Web Basic workflow template for site data sources',
      },
    },
  },

  ResultSuccess: {
    title: 'Knowledge base established successfully',
    paragraph: 'paragraph',
    paragraph_count: 'paragraphs',
    documentList: 'file list',
    loading: 'Importing',
    buttons: {
      toKnowledge: 'Return to knowledge base list',
      toDocument: 'Go to file',
    },
  },
  syncWeb: {
    title: 'Sync knowledge base',
    syncMethod: 'sync mode',
    replace: 'replace sync',
    replaceText: 'reacquire Web site files，Overwrite and replace files in the local knowledge base',
    complete: 'full sync',
    completeText: 'First delete all files in the local knowledge base，reacquire Web site files',
    tip: 'Notice：All syncs delete existing data and re-fetch new data，Please operate with caution。',
  },
  transform: {
    button: 'Convert',
    title: 'Convert to workflow knowledge base',
    message1:
      'You can now convert an existing knowledge base into a workflow knowledge base——This is a more open、A more flexible knowledge base，Autonomously orchestrate the entire process from different data sources to knowledge base writing by dragging and dropping nodes.，Meet the personalized knowledge management needs of enterprises。Access to data sources and tools from our tools。',
    message2: 'The new processing method will be applied to all subsequent imported files。',
    tip: 'Notice：Irreversible after conversion。',
    comfirm: 'Confirm conversion to workflow knowledge base？Cannot go back after conversion，Please operate with caution。',
  },
  customSegmentation: {
    title: 'Custom word segmentation',
    tip: 'Avoid jargon being broken up，Improve the precision and recall rate of full-text search',
    create: 'create words',
    quickCreate: 'Create words quickly',
    word: 'words',
    wordplaceholder: 'Please enter the professional terms that need to be retained/Exclusive vocabulary，One per line',
    wordRequiredMessage: 'Please enter the word',
    wordIndexing: 'index',
  },
}
