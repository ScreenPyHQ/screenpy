"""
An ability that will allow the actor to get a generated code for two-factor
authentication. Grant your actor the ability to authenticate with 2FA in one
of these ways:

    # during instantiation
    the_actor = AnActor.who_can(AuthenticateWith2FA.using_secret(2FA_SECRET))
    the_actor = AnActor.who_can(AuthenticateWith2FA.using(pyotp_instance))

    # after instantiation
    the_actor.can(AuthenticateWith2FA.using_secret(2FA_SECRET))

    # use in new actions
    the_actor.uses_ability_to(AuthenticateWith2FA).to_get_token()
"""


from datetime import datetime
from time import sleep

import pyotp


class AuthenticateWith2FA:
    """
    The ability to retrieve a one-time password from a two-factor
    authenticator. This ability is meant to be instantiated with its
    |AuthenticateWith2FA.using_secret| method, which will take in the 2FA
    secret, or its |AuthenticateWith2FA.using| static method, which takes in
    an instantiated PyOTP instance. A typical invocation looks like:

        AuthenticateWith2FA.using_secret("KEEPITSECRETKEEPITSAFE")

        AuthenticateWith2FA.using(pyotp_instance)

    This will create the ability that can be passed in to an actor's
    |Actor.who_can| method.
    """

    @staticmethod
    def using_secret(secret: str) -> "AuthenticateWith2FA":
        """
        Create a TOTP instance with the given secret.

        Args:
            secret: the secret given by the 2FA service. You may need to
                decode a QR code to get this secret.

        Returns:
            |AuthenticateWith2FA|
        """
        totp = pyotp.TOTP(secret)
        return AuthenticateWith2FA.using(totp)

    @staticmethod
    def using(otp: pyotp.TOTP) -> "AuthenticateWith2FA":
        """
        Specify an already-created TOTP instance to provide tokens.

        Args:
            otp (pyotp.TOTP): an instance of a TOTP object.

        Returns:
            |AuthenticateWith2FA|
        """
        return AuthenticateWith2FA(otp)

    def to_get_token(self) -> str:
        """
        Get the current two-factor token to use as a one-time password.

        Returns:
            str
        """
        if 30 - (datetime.now().second % 30) <= 1:
            # token would expire before it can be entered, wait a second.
            sleep(2)
        return self.otp.now()

    def forget(self) -> None:
        """Clean up the pyotp instance stored in this ability."""
        del self.otp

    def __repr__(self) -> str:
        return "Authenticate with 2-Factor"

    def __init__(self, otp: pyotp.TOTP) -> None:
        self.otp = otp
