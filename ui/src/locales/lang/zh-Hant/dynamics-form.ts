export default {
  input_type_list: {
    TextInput: 'text box',
    PasswordInput: 'Secret text box',
    Slider: 'Slider',
    SwitchInput: 'switch',
    SingleSelect: 'radio button',
    MultiSelect: 'checkbox',
    DatePicker: 'date picker',
    JsonInput: 'JSONtext box',
    RadioCard: 'tab',
    RadioRow: 'Single row tab',
    UploadInput: 'File upload',
    TextareaInput: 'Multiline text box',
    MultiRow: 'Single row multiple choice cards',
    Model: 'Model',
    Knowledge: 'knowledge base',
  },
  default: {
    label: 'Default value',
    placeholder: 'Please enter default value',
    requiredMessage: 'is a required attribute',
    show: 'Show default value',
  },
  tip: {
    requiredMessage: 'cannot be empty',
    jsonMessage: 'JSON Incorrect format',
  },
  paramForm: {
    field: {
      label: 'parameters',
      placeholder: 'Please enter parameters',
      requiredMessage: 'parameters is a required attribute',
      requiredMessage2: 'Only letters can be entered、Numbers and the bottom line',
    },
    name: {
      label: 'display name',
      placeholder: 'Please enter a display name',
      requiredMessage: 'display name is a required attribute',
    },
    tooltip: {
      label: 'Parameter prompt description',
      placeholder: 'Please enter parameter prompt description',
    },
    required: {
      label: 'Is it required?',
      requiredMessage: 'Is it required? is a required attribute',
    },
    input_type: {
      label: 'Component type',
      placeholder: 'Please select component type',
      requiredMessage: 'Component type is a required attribute',
    },
    desc: {
      label: 'describe',
      placeholder: 'Please enter a description',
    },
  },
  TreeSelect: {
    label: 'tree selector',
    select: 'Options',
    selectRequired: 'Option required',
    allowMultipleSelections: 'Allow multiple selections',
    addDialog: {
      addFirstOption: 'Added first level options',
      addSubOptions: 'Add new sub-option',
      require: 'Please fill in at least one complete information',
      nodeNotFound: 'Parent node not found',
      tagRequire: 'Label and option values ​​cannot be empty',
    },
  },
  DatePicker: {
    placeholder: 'Select date',
    year: 'Year',
    month: 'moon',
    date: 'date',
    datetime: 'date time',
    dataType: {
      label: 'time type',
      placeholder: 'Please select time type',
    },
    format: {
      label: 'Format',
      placeholder: 'Please select format',
    },
  },
  Select: {
    label: 'option value',
    placeholder: 'Please enter option value',
  },
  tag: {
    label: 'label',
    placeholder: 'Please enter option tag',
  },
  Slider: {
    showInput: {
      label: 'Whether to have input box',
    },
    valueRange: {
      label: 'Value range',
      minRequired: 'Minimum value required',
      maxRequired: 'Maximum value required',
    },
    step: {
      label: 'step value',
      requiredMessage1: 'Step value is required',
      requiredMessage2: 'The step size cannot be0',
    },
  },
  TextInput: {
    length: {
      label: 'text length',
      minRequired: 'Minimum length required',
      maxRequired: 'Maximum length required',
      requiredMessage1: 'The length is',
      requiredMessage2: 'arrive',
      requiredMessage3: 'characters',
      requiredMessage4: 'Text length is a required parameter',
    },
  },
  UploadInput: {
    limit: {
      label: 'Maximum number of files uploaded at a time',
      required: 'The maximum number of files uploaded at a time is required',
    },
    max_file_size: {
      label: 'Max per file(MB)',
      required: 'Maximum required for each file',
    },
    accept: {
      label: 'File type',
      required: 'File type required',
    },
    errorTip: {
      sizeError: 'Size exceeds limit',
      networkError: 'Network failure',
    },
    reUpload: 'Try again',
    uploadStatus: 'Completed {success} / {total} files',
    failedStatus: 'Fail {count} files',
    uploading: 'Uploading',
    allSuccess: 'All successful',
  },
  AssignmentMethod: {
    label: 'Assignment method',
    ref_variables: {
      label: 'reference variable',
      popover: 'The value of the variable must match',
      json_format: 'JSON Format',
      popover_label: 'label',
      popover_value: 'value',
      popover_default: 'Is it the default value?',
    },
  },
  ModelConstructor: {
    optionalModel: 'Select model',
    defaultModel: 'Default model',
    modelPlaceholder: 'Please enter model name',
  },
}
