interface ChatProfile {
  // Whether to openCertification
  authentication: boolean
  // icon
  icon?: string
  // Application name
  application_name?: string
  // Background image
  bg_icon?: string
  // Authentication type
  authentication_type?: 'password' | 'login'
  // LoginType
  login_value?: Array<string>
  max_attempts?: number
  rsaKey?: string
}

interface ChatUserProfile {
  email: string
  id: string
  nick_name: string
  username: string
  source: string
}
export { type ChatProfile, type ChatUserProfile }
