# coding=utf-8
"""
@project: MaxKB
@Author：TigerTiger
@file： login.py
@date：2025/4/14 11:08
@desc:
"""

import base64
import json

from captcha.image import ImageCaptcha
from django.core import signing
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from application.models import ApplicationAccessToken
from common.auth.common import FileToken
from common.constants.authentication_type import AuthenticationType
from common.constants.cache_version import Cache_Version
from common.database_model_manage.database_model_manage import DatabaseModelManage
from common.exception.app_exception import AppApiException
from common.utils.common import password_encrypt, password_verify, needs_password_upgrade, get_random_chars
from common.utils.rsa_util import decrypt
from maxkb.const import CONFIG
from users.models import User
from common.utils.logger import maxkb_logger


class LoginRequest(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=64, help_text=_("Username"), label=_("Username"))
    password = serializers.CharField(required=True, max_length=128, label=_("Password"))
    captcha = serializers.CharField(
        required=False, max_length=64, label=_("captcha"), allow_null=True, allow_blank=True
    )
    encryptedData = serializers.CharField(required=False, label=_("encryptedData"), allow_null=True, allow_blank=True)


system_version, system_get_key = Cache_Version.SYSTEM.value


class LoginResponse(serializers.Serializer):
    """
    Loginresponse object
    """

    token = serializers.CharField(required=True, label=_("token"))


def record_login_fail(username: str, expire: int = 600):
    """RecordLogin failedNumber (atomic) ReturncurrentFailed of InPage2Number"""
    if not username:
        return 0
    fail_key = system_get_key(f"system_{username}")
    try:
        fail_count = cache.incr(fail_key, 1, version=system_version)
    except ValueError:
        # key Does not exist，Initialize and Settings expire
        cache.set(fail_key, 1, timeout=expire, version=system_version)
        fail_count = 1
    return fail_count


def record_login_fail_lock(username: str, expire: int = 10):
    """
    use cache.incr Guaranteed atomic increment, andInDoes not existWhen initializing the Number counter andReturncurrentvalue。
    The counter here is used to determine whether Yes should enter"Lock"Branch，Avoid relying on non-atomic get -> set combination。
    """
    if not username:
        return 0
    fail_key = system_get_key(f"system_{username}_lock_count")
    try:
        fail_count = cache.incr(fail_key, 1, version=system_version)
    except ValueError:
        # key Does not exist，Initialization and Settings expire (minutes to seconds)）
        cache.set(fail_key, 1, timeout=expire * 60, version=system_version)
        fail_count = 1
    return fail_count


class LoginSerializer(serializers.Serializer):
    @staticmethod
    def get_auth_setting():
        """getCertificationSettings"""
        auth_setting_model = DatabaseModelManage.get_model("auth_setting")
        auth_setting = {}
        if auth_setting_model:
            setting_obj = auth_setting_model.objects.filter(param_key="auth_setting").first()
            if setting_obj:
                try:
                    auth_setting = json.loads(setting_obj.param_value) or {}
                except Exception:
                    auth_setting = {}
        return auth_setting

    @staticmethod
    def login(instance):
        # DecryptNumberAccording to
        username = instance.get("username", "")
        encrypted_data = instance.get("encryptedData", "")

        if encrypted_data:
            try:
                decrypted_raw = decrypt(encrypted_data)
                # decrypt Maybe Return is not JSON characterString, guard parsing different normal
                decrypted_data = json.loads(decrypted_raw) if decrypted_raw else {}
                if isinstance(decrypted_data, dict):
                    instance.update(decrypted_data)
            except Exception as e:
                maxkb_logger.exception("Failed to decrypt/parse encryptedData for user %s: %s", username, e)
                raise AppApiException(500, _("Invalid encrypted data"))

        try:
            LoginRequest(data=instance).is_valid(raise_exception=True)
        except serializers.ValidationError:
            raise
        except Exception as e:
            raise AppApiException(500, str(e))

        password = instance.get("password")
        captcha = instance.get("captcha", "")

        # Get certification configuration
        auth_setting = LoginSerializer.get_auth_setting()
        max_attempts = auth_setting.get("max_attempts", 1)
        failed_attempts = auth_setting.get("failed_attempts", 5)
        lock_time = auth_setting.get("lock_time", 10)

        # Check license validity
        license_validator = DatabaseModelManage.get_model("license_is_valid") or (lambda: False)
        is_license_valid = license_validator() if license_validator() is not None else False

        if is_license_valid:
            # Check whether the account Yes is locked
            if LoginSerializer._is_account_locked(username, failed_attempts):
                raise AppApiException(
                    1005, _("This account has been locked for %s minutes, please try again later") % lock_time
                )

            # VerificationVerification code
        if LoginSerializer._need_captcha(username, max_attempts):
            LoginSerializer._validate_captcha(username, captcha)

        # VerificationUsersByAccording to：Firstaccording tousernameFind and use password_verify VerificationPassword
        user = User.objects.filter(username=username).first()

        if not user or not password_verify(password, user.password):
            LoginSerializer._handle_failed_login(username, is_license_valid, failed_attempts, lock_time)
            raise AppApiException(500, _("The username or password is incorrect"))

        # Transparently upgrade legacy MD5 hash to PBKDF2
        if needs_password_upgrade(user.password):
            user.password = password_encrypt(password)
            user.save(update_fields=["password"])

        if not user.is_active:
            raise AppApiException(1005, _("The user has been disabled, please contact the administrator!"))

        # ClearFailedCount Number and mergegeneratetoken
        cache.delete(system_get_key(f"system_{username}"), version=system_version)
        cache.delete(system_get_key(f"system_{username}_lock"), version=system_version)
        token = signing.dumps(
            {
                "username": user.username,
                "id": str(user.id),
                "email": user.email,
                "type": AuthenticationType.SYSTEM_USER.value,
            }
        )

        version, get_key = Cache_Version.TOKEN.value
        timeout = CONFIG.get_session_timeout()
        cache.set(get_key(token), user, timeout=timeout, version=version)

        return {"token": token}, FileToken(str(user.id), AuthenticationType.SYSTEM_USER.value).to_token()

    @staticmethod
    def _is_account_locked(username: str, failed_attempts: int) -> bool:
        """Check whether the account Yes is locked"""
        if failed_attempts == -1:
            return False
        lock_cache = cache.get(system_get_key(f"system_{username}_lock"), version=system_version)
        return bool(lock_cache)

    @staticmethod
    def _need_captcha(username: str, max_attempts: int) -> bool:
        """Determine whether Yes is neededVerification code"""
        if max_attempts == -1:
            return False
        elif max_attempts > 0:
            fail_count = cache.get(system_get_key(f"system_{username}"), version=system_version) or 0
            return fail_count >= max_attempts
        return True

    @staticmethod
    def _validate_captcha(username: str, captcha: str) -> None:
        """VerificationVerification code"""
        if not captcha:
            raise AppApiException(1005, _("Captcha is required"))

        captcha_cache = cache.get(
            Cache_Version.CAPTCHA.get_key(captcha=f"system_{username}"), version=Cache_Version.CAPTCHA.get_version()
        )

        if captcha_cache is None or captcha.lower() != captcha_cache:
            raise AppApiException(1005, _("Captcha code error or expiration"))

    @staticmethod
    def _handle_failed_login(username: str, is_license_valid: bool, failed_attempts: int, lock_time: int) -> None:
        """ProcessingLogin failed

        Repair points：
        - use record_login_fail / record_login_fail_lock Two pieces atoms incr to recordFailed；
        - No more reliance on precision etc. 0 comparison to trigger the lock, while Yes is based on the atomic countNumber >= Threshold value to decide to enter the lockBranch；
        - use cache.add Atomic create lock key，cache.add Guaranteed that only the first piecessuccesscreate can write to the key；
          otherIf concurrently arrived requests are found that the Count Number has arrived and reached the threshold value, they should alsoReturn"Locked"Respond to avoid bypasses。
        """
        # Record common Failed statisticsNumber（forVerification codetriggeruse）
        try:
            record_login_fail(username)
        except Exception:
            maxkb_logger.exception("Failed to record login fail for user %s", username)

        # Record the Failed count used for lock judgmentNumber（according to lock_time For initialization expiration minutes）
        lock_fail_count = 0
        try:
            lock_fail_count = record_login_fail_lock(username, lock_time)
        except Exception:
            maxkb_logger.exception("Failed to record lock fail count for user %s", username)

        # likeIf not Yes Enterprise Edition or disable the locking function, return directly (but the Number has been recorded）
        if not is_license_valid or failed_attempts <= 0:
            return

        # When the count Number is less than the threshold value, notify the remaining attempts.Number
        if lock_fail_count < failed_attempts:
            remain_attempts = failed_attempts - lock_fail_count
            raise AppApiException(
                1005,
                _("Login failed %s times, account will be locked, you have %s more chances !")
                % (failed_attempts, remain_attempts),
            )

        # When the count reaches arrival or exceeds the threshold value, try to create the lock key atomically; regardless of cache.add Return True/False，Return the locked response，
        # Because iffor False Description other concurrent request has Will account marked for locked, row for should be consistent。
        try:
            locked = cache.add(
                system_get_key(f"system_{username}_lock"), 1, timeout=lock_time * 60, version=system_version
            )
            if locked:
                maxkb_logger.info("Account %s locked by setting cache key", username)
            else:
                maxkb_logger.info("Account %s lock key already present (another request set it)", username)
        except Exception:
            maxkb_logger.exception("Failed to set lock key for user %s", username)

        raise AppApiException(
            1005, _("This account has been locked for %s minutes, please try again later") % lock_time
        )


class CaptchaResponse(serializers.Serializer):
    """
    Loginresponse object
    """

    captcha = serializers.CharField(required=True, label=_("captcha"))


class CaptchaSerializer(serializers.Serializer):
    @staticmethod
    def generate(username: str, type: str = "system"):
        auth_setting = LoginSerializer.get_auth_setting()
        max_attempts = auth_setting.get("max_attempts", 1)

        need_captcha = True
        if max_attempts == -1:
            need_captcha = False
        elif max_attempts > 0:
            fail_count = cache.get(system_get_key(f"system_{username}"), version=system_version) or 0
            need_captcha = fail_count >= max_attempts

        return CaptchaSerializer._generate_captcha_if_needed(username, type, need_captcha)

    @staticmethod
    def chat_generate(username: str, type: str = "chat", access_token: str = ""):
        application_access_token = ApplicationAccessToken.objects.filter(access_token=access_token).first()

        if not application_access_token:
            raise AppApiException(1005, _("Invalid access token"))

        auth_setting = application_access_token.authentication_value
        max_attempts = auth_setting.get("max_attempts", 1)

        need_captcha = True
        if max_attempts == -1:
            need_captcha = False
        elif max_attempts > 0:
            fail_count = cache.get(system_get_key(f"{type}_{username}"), version=system_version) or 0
            need_captcha = fail_count >= max_attempts

        return CaptchaSerializer._generate_captcha_if_needed(username, type, need_captcha)

    @staticmethod
    def _generate_captcha_if_needed(username: str, type: str, need_captcha: bool):
        """
        Extracted publiccommonVerification codegeneratemethods
        """
        if need_captcha:
            chars = get_random_chars()
            image = ImageCaptcha()
            data = image.generate(chars)
            captcha = base64.b64encode(data.getbuffer())
            cache.set(
                Cache_Version.CAPTCHA.get_key(captcha=f"{type}_{username}"),
                chars.lower(),
                timeout=300,
                version=Cache_Version.CAPTCHA.get_version(),
            )
            return {"captcha": "data:image/png;base64," + captcha.decode()}
        return {"captcha": ""}
