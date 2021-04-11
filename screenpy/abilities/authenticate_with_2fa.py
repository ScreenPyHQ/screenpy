"""
Enable the Actor to get a generated code for two-factor authentication.
"""

from datetime import datetime
from time import sleep

import pyotp


class AuthenticateWith2FA:
    """Use PyOTP to enable retrieval of tokens from a two-factor authenticator.

    Examples::

        Perry = AnActor.named("Perry")who_can(
            AuthenticateWith2FA.using_secret(2FA_SECRET)
        )

        Perry = AnActor.named("Perry").who_can(
            AuthenticateWith2FA.using(pyotp_instance)
        )
    """

    @staticmethod
    def using_secret(secret: str) -> "AuthenticateWith2FA":
        """Create a TOTP instance with the given secret.

        Args:
            secret: the secret given by the 2FA service. You may need to
                decode a QR code to get this secret.
        """
        totp = pyotp.TOTP(secret)
        return AuthenticateWith2FA.using(totp)

    @staticmethod
    def using(otp: pyotp.TOTP) -> "AuthenticateWith2FA":
        """Specify an already-created TOTP instance to provide tokens."""
        return AuthenticateWith2FA(otp)

    def to_get_token(self) -> str:
        """Get the current two-factor token to use as a one-time password."""
        if 30 - (datetime.now().second % 30) <= 1:
            # token would expire before it can be entered, wait a bit.
            sleep(2)
        return self.otp.now()

    def forget(self) -> None:
        """Clean up the pyotp instance stored in this Ability."""
        del self.otp

    def __repr__(self) -> str:
        return "Authenticate with 2-Factor"

    __str__ = __repr__

    def __init__(self, otp: pyotp.TOTP) -> None:
        self.otp = otp
