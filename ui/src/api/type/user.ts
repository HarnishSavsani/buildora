interface User {
  /**
   * Usersid
   */
  id: string
  /**
   * username
   */
  username: string
  nick_name: string
  /**
   * Mail
   */
  email: string
  /**
   * UsersRole
   */
  role: Array<string>
  /**
   * User permissions
   */
  permissions: Array<string>
  /**
   * YesNo needChange password
   */
  is_edit_password?: boolean
  IS_XPACK?: boolean
  XPACK_LICENSE_IS_VALID?: boolean
  language?: string
  workspace_list?: Array<any>
  role_name?: Array<any>
  source?: string
}

interface LoginRequest {
  /**
   * username
   */
  username: string
  /**
   * Password
   */
  password: string
}

interface RegisterRequest {
  /**
   * username
   */
  username: string
  /**
   * Password
   */
  password: string
  /**
   * ConfirmPassword
   */
  re_password: string
  /**
   * Mail
   */
  email: string
  /**
   * Verification code
   */
  code: string
}

interface CheckCodeRequest {
  /**
   * Mail
   */
  email: string
  /**
   *Verification code
   */
  code: string
  /**
   * Type
   */
  type: 'register' | 'reset_password'
}

interface ResetCurrentUserPasswordRequest {
  /**
   * Verification code
   */
  code?: string
  /**
   *Password
   */
  password: string
  /**
   * Confirm Password
   */
  re_password: string
}

interface ResetPasswordRequest {
  /**
   * Mail
   */
  email?: string
  /**
   * Verification code
   */
  code?: string
  /**
   * Password
   */
  password: string
  /**
   * Confirm Password
   */
  re_password: string
  encrypted?: boolean
}

export type {
  LoginRequest,
  RegisterRequest,
  CheckCodeRequest,
  ResetPasswordRequest,
  User,
  ResetCurrentUserPasswordRequest,
}
