import {Result} from '@/request/Result'
import {get, post} from '@/request/index'
import type {User, ResetPasswordRequest, CheckCodeRequest} from '@/api/type/user'
import type {Ref} from 'vue'

/**
 * getUsersBasicinformation
 * @param loading interface loader
 * @returns UsersBasicinformation
 */
const getUserProfile: (loading?: Ref<boolean>) => Promise<Result<User>> = (loading) => {
  return get('/user/profile', undefined, loading)
}

/**
 * getprofile
 */
const getProfile: (loading?: Ref<boolean>) => Promise<Result<any>> = (loading) => {
  return get('/profile', undefined, loading)
}
/**
 * getallUsers
 */
const getUserList: (arg?: any, loading?: Ref<boolean>) => Promise<Result<Record<string, any>[]>> = (
  arg,
  loading,
) => {
  return get('/user/list', arg, loading)
}

/**
 * getallUsers
 */
const getAllMemberList: (arg: any, loading?: Ref<boolean>) => Promise<Result<Record<string, any>[]>> = (
  arg,
  loading,
) => {
  return get('/user/list', arg, loading)
}

/**
 * CalibrationVerificationVerification code
 * @param request request object
 * @param loading interface loader
 * @returns
 */
const checkCode: (request: CheckCodeRequest, loading?: Ref<boolean>) => Promise<Result<boolean>> = (
  request,
  loading,
) => {
  return post('/user/check_code', request, undefined, loading)
}

/**
 * Send email
 * @param email  Emailaddress
 * @param loading interface loader
 * @returns
 */
const sendEmit: (
  email: string,
  type: 'register' | 'reset_password',
  loading?: Ref<boolean>,
) => Promise<Result<boolean>> = (email, type, loading) => {
  return post('/user/send_email', {email, type}, undefined, loading)
}

/**
 * resetPassword
 * @param request Reset Password requestparameter
 * @param loading interface loader
 * @returns
 */
const postResetPassword: (
  request: ResetPasswordRequest,
  loading?: Ref<boolean>,
) => Promise<Result<boolean>> = (request, loading) => {
  return post('/user/re_password', request, undefined, loading)
}

/**
 * resetPassword
 * @param data Reset Password requestparameter
 * @param loading interface loader
 * @returns
 */
const resetCurrentPassword: (
  data: any,
  loading?: Ref<boolean>,
) => Promise<Result<boolean>> = (data, loading) => {
  return post('/user/current/reset_password', data, undefined, loading)
}

export default {
  getUserProfile,
  getProfile,
  getUserList,
  getAllMemberList,
  postResetPassword,
  checkCode,
  sendEmit,
  resetCurrentPassword,
}
