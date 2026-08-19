export default {
  title: 'User management',
  createUser: 'EstablishUser',
  editUser: 'EditUser',
  roleSetting: 'RoleSettings',
  addRole: 'Add toRole',
  setting: {
    updatePwd: 'ReviseUserpassword',
  },
  tip: {
    professionalMessage: 'The social version supports the most 2 PieceUsers，likeneed to have moreUsers，Please upgrade to professional version。',
    updatePwdSuccess: 'UserspasswordModification successful',
  },
  delete: {
    confirmTitle: 'Whether to deleteTheUser？',
    confirmMessage:
      'deleteAfter the User, the UsersEstablishallResources（Agent in、knowledge base、Model）Neither will bedelete，Please operate with caution。',
  },
  userForm: {
    nick_name: {
      label: 'Name',
      placeholder: 'Please enterName',
      lengthMessage: 'The length must be between 2 arrive 20 between characters',
    },

    phone: {
      label: 'mobile phonenumber',
      placeholder: 'Please entermobile phonenumber',
      invalidMessage: 'mobile phonenumberIncorrect format',
    },
  },
  source: {
    label: 'UserSource',
    local: 'SystemUser',
    localCreate: 'localEstablish',
    wecom: 'Enterprise WeChat',
    lark: 'Feishu',
    dingtalk: 'DingTalk',
  },
  settingRole: 'SettingsRole',
  defaultPassword: 'Defaultpassword',
}
