export default {
  title: 'knowledge base',
  document_count: 'DocumentationNumber',
  relatedApp_count: 'associationAgent',
  setting: {
    vectorization: 'vectorization',
    sync: 'synchronous',
    tokenize: 'index',
  },

  tip: {
    professionalMessage: 'Community Editionmostsupport 50 piecesknowledge base，likeneed to have moreknowledge base，pleaseUpgrade toProfessional version。',
    syncSuccess: 'synchronousTask sendingsuccess',
    updateModeMessage: 'Modify knowledge basevector modelFinally, it is necessary toKnowledge base vectorChange, Yes to continue saving？',
  },
  delete: {
    confirmTitle: 'YesnoDelete knowledge base：',
    confirmTitle2: 'piecesknowledge base?',
    confirmMessage1: 'Thisknowledge baseassociation',
    confirmMessage2: 'piecesAgent，Deletecannot be restored, please be carefuloperate。',
    resourceCountMessage: 'Thisknowledge baseassociation {count} piecesresource，Deletecannot be used after, please be carefuloperate。',
  },
  knowledgeType: {
    label: 'knowledge baseType',
    generalKnowledge: 'Universalknowledge base',
    webKnowledge: 'Web knowledge base',
    larkKnowledge: 'Feishuknowledge base',
    workflowKnowledge: 'Workflowknowledge base',
    yuqueKnowledge: 'Yuqueknowledge base',
    generalInfo: 'passUpload fileorManual entry buildknowledge base',
    webInfo: 'Build via website linksknowledge base',
    larkInfo: 'Built by FeishuDocumentationknowledge base',
    yuqueInfo: 'Built through Yuque Documentationknowledge base',
    createGeneralKnowledge: 'createUniversalknowledge base',
    createWebKnowledge: 'create Web knowledge base',
    createLarkKnowledge: 'createFeishuknowledge base',
    createYuqueKnowledge: 'createYuqueknowledge base',
    createWorkflowKnowledge: 'createWorkflowknowledge base',
    workflowInfo: 'Construct through CustomizeWorkflowknowledge base',
  },
  form: {
    knowledgeName: {
      label: 'Knowledge base name',
      placeholder: 'Please enterKnowledge base name',
      requiredMessage: 'Please enterKnowledge base name',
    },
    knowledgeDescription: {
      label: 'Knowledge base description',
      placeholder:
        'describeknowledge basecontent, detailed describeWillHelp helps AI understand the content in depthknowledge basecontent can more accurately retrieve arrivecontent, improve theknowledge baseHit Medium rate。',
      requiredMessage: 'Please enterKnowledge base description',
    },
    EmbeddingModel: {
      label: 'vector model',
      placeholder: 'Please selectvector model',
      requiredMessage: 'Please selectvector model',
    },

    source_url: {
      label: 'Web Root address',
      placeholder: 'Please enter Web Root address',
      requiredMessage: ' Please enter Web Root address',
    },
    user_id: {
      requiredMessage: 'Please enter User ID',
    },
    token: {
      requiredMessage: 'Please enter Token',
    },
    selector: {
      label: 'Selector',
      placeholder: 'Default is body，Can be input .classname/#idname/tagname',
    },
    file_count_limit: {
      label: 'every uploadmostdocumentNumber',
    },
    file_size_limit: {
      label: 'Maximum uploaded piecesDocumentation per(MB)',
      placeholder: 'It is recommended to adjust according to the server configuration，Otherwise it may cause service downtime',
    },
    appTemplate: {
      blank: {
        title: 'blankcreate',
      },
      basic: {
        title: 'Basetemplate',
        description: 'Support local files、FeishuDocumentation、Web siteNumberAccording tosource baseWorkflowtemplate',
      },
    },
  },

  ResultSuccess: {
    title: 'knowledge basecreatesuccess',
    paragraph: 'segmentation',
    paragraph_count: 'piecessegmentation',
    documentList: 'Document list',
    loading: 'importMedium',
    buttons: {
      toKnowledge: 'ReturnKnowledge base list',
      toDocument: 'Go toDocumentation',
    },
  },
  syncWeb: {
    title: 'synchronousknowledge base',
    syncMethod: 'sync mode',
    replace: 'Replacementsynchronous',
    replaceText: 'againget Web Site Documentation, overwrite and replace localknowledge baseMediumofDocumentation',
    complete: 'overallsynchronous',
    completeText: 'Delete local firstknowledge baseallDocumentation，againget Web siteDocumentation',
    tip: 'Notice：allsynchronousMetro Delete already existsNumberAccording toto get newNumberAccording to，Please be carefuloperate。',
  },

  transform: {
    button: 'Convert',
    title: 'Convert toWorkflowknowledge base',
    message1:
      'You can now Will existing onesknowledge baseConvert toWorkflowknowledge base ——This isA more open and flexibleknowledge base，Autonomous arrangement by dragging and dropping Nodal from differentNumberAccording tosourcearriveknowledge baseThe entire writing process meets the personalized knowledge management needs of enterprise pieces. You can use our toolMediumNumberAccording tosourceandtool。',
    message2: 'New Processing method Willapplicationarrive subsequent importallDocumentation。',
    tip: 'Notice：Irreversible after conversion。',
    comfirm: 'ConfirmConvert toWorkflowknowledge base？There is no way to go back after conversion, please be careful.operate。',
  },
  customSegmentation: {
    title: 'Customizeparticiple',
    tip: 'Avoid professional terms being split and improve the accuracy and recall rate of full-text retrieval.',
    create: 'createwords',
    quickCreate: 'Quickly create words',
    word: 'words',
    wordplaceholder: 'Please enterProfessional terms that need to be retained/Exclusive vocabulary，One per line',
    wordRequiredMessage: 'Please enter the word',
    wordIndexing: 'index',
  },
}
