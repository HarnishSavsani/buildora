export default {
  input_type_list: {
    TextInput: 'textBox',
    PasswordInput: 'PasswordBox',
    Slider: 'slider',
    SwitchInput: 'switch',
    SingleSelect: 'Singleselection box',
    MultiSelect: 'checkbox',
    DatePicker: 'date',
    JsonInput: 'JSON textBox',
    RadioCard: 'Tab',
    RadioRow: 'Singlerow tab',
    UploadInput: 'documentUpload',
    TextareaInput: 'multi-line text box',
    MultiRow: 'Singlerow multi-select card',
    Model: 'Model',
    Knowledge: 'knowledge base',
  },
  default: {
    label: 'default value',
    placeholder: 'Please enterdefault value',
    requiredMessage: 'is a required attribute',
    show: 'showdefault value',
  },
  tip: {
    requiredMessage: 'cannot be empty',
    jsonMessage: 'JSON FormatIncorrect',
  },
  paramForm: {
    field: {
      label: 'parameter',
      placeholder: 'Please enterparameter',
      requiredMessage: 'parameter is a required attribute',
      requiredMessage2: 'Only Character, Number, Character and underscore can be entered.',
    },
    name: {
      label: 'Display name',
      placeholder: 'Please enterDisplay name',
      requiredMessage: 'Display name is a required attribute',
    },
    tooltip: {
      label: 'parameterhintillustrate',
      placeholder: 'Please enterparameterhintillustrate',
    },
    required: {
      label: 'Is it required?',
      requiredMessage: 'Is it required? is a required attribute',
    },
    input_type: {
      label: 'ComponentsType',
      placeholder: 'Please selectComponentsType',
      requiredMessage: 'EstablishType is a required attribute',
    },
    desc: {
      label: 'describe',
      placeholder: 'Please enterdescribe',
    },
  },
  TreeSelect: {
    label: 'tree shapeSelector',
    select: 'Options',
    selectRequired: 'OptionsRequired',
    allowMultipleSelections: 'Allow multiple selections',
    addDialog: {
      addFirstOption: 'Add toFirst level option',
      addSubOptions: 'Add tosub-options',
      require: 'Please fill in at least one completeNumberAccording to',
      nodeNotFound: 'The arrival parent has not been foundNode',
      tagRequire: 'TagsandOptionsvaluecannot be empty',
    },
  },
  DatePicker: {
    placeholder: 'choosedate',
    year: 'Year',
    month: 'moon',
    date: 'date',
    datetime: 'dateTime',
    dataType: {
      label: 'TimeType',
      placeholder: 'Please select a timeType',
    },
    format: {
      label: 'Format',
      placeholder: 'Please selectFormat',
    },
  },
  Select: {
    label: 'Optionsvalue',
    placeholder: 'Please enterOptionsvalue',
  },
  tag: {
    label: 'Tags',
    placeholder: 'Please enterOptionsTags',
  },
  Slider: {
    showInput: {
      label: 'YesNo input box',
    },
    valueRange: {
      label: 'PickvalueRange',
      minRequired: 'Minimum value required',
      maxRequired: 'Maximum value required',
    },
    step: {
      label: 'step sizevalue',
      requiredMessage1: 'step sizevalueRequired',
      requiredMessage2: 'Step size cannotfor 0',
    },
  },
  TextInput: {
    length: {
      label: 'textlength',
      minRequired: 'minimum lengthRequired',
      maxRequired: 'Maximum lengthRequired',
      requiredMessage1: 'Length in',
      requiredMessage2: 'arrive',
      requiredMessage3: 'characters',
      requiredMessage4: 'textlengthforRequiredparameter',
    },
  },
  UploadInput: {
    limit: {
      label: 'SingleuploadedmostdocumentNumber',
      required: 'SingleuploadedmostdocumentNumberRequired',
    },
    max_file_size: {
      label: 'maximum per piecesdocument(MB)',
      required: 'maximum per piecesdocument(MB)Required',
    },
    accept: {
      label: 'documentType',
      required: 'documentTypeRequired',
    },
    errorTip: {
      sizeError: 'Size exceeds limit',
      networkError: 'networkFailed',
    },
    reUpload: 'Try again',
    uploadStatus: 'Completed {success} / {total} piecesdocument',
    failedStatus: 'Failed {count} piecesdocument',
    uploading: 'UploadMedium',
    allSuccess: 'All successful',
  },
  AssignmentMethod: {
    label: 'Assign value method',
    ref_variables: {
      popover: 'The variable value must conform to',
      json_format: 'JSON Format',
      popover_label: 'Tags',
      popover_value: 'value',
      popover_default: 'Yesnofordefault value',
    },
  },
  ModelConstructor: {
    optionalModel: 'OptionalModel',
    defaultModel: 'defaultModel',
    modelPlaceholder: 'Please selectModel',
  },
  KnowledgeConstructor: {
    optionalKnowledge: 'Optionalknowledge base',
    optionalKnowledgePlaceholder: 'Please select optionalknowledge base',
    defaultKnowledge: 'defaultknowledge base',
  },
}
