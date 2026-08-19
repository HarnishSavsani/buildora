interface LoginRequest {
  /**
   * username
   */
  username: string
  /**
   * Password
   */
  password: string
  /**
   * Verification code
   */
  captcha: string
  /**
   * encryptionNumberAccording to
   */
  encryptedData?: string
}
export type { LoginRequest }
