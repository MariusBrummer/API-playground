"""Check util."""
import inspect
import logging
from typing import List

log = logging.getLogger(__name__)


class Check:
    """Simple object that is used for delayed checks in tests."""

    def __init__(self):
        self._errors = []

    def __call__(self, success: bool, message: str):
        """Add a check result.

        All check results are collected and if there are failed checks, the
        test that produced this failed checks is marked as failed.

        Args:
            success: Result of check.
            message: Message that describes check. If check was un-successful,
                this message is added as error.
        """
        if success:
            log.info("[PASS] %s", message)
        else:
            log.warning("[FAIL] %s", message)
            frame = inspect.currentframe()
            try:
                local_vars = "\n".join(
                    [
                        f"\t {key}={value}"
                        for key, value in frame.f_back.f_locals.items()
                    ]
                )
                self._errors.append(f"{message} \n{local_vars} \n")
            finally:
                del frame

    def consume_errors(self) -> List[str]:
        """Consume all errors collected so far."""
        errors = self._errors
        self._errors = []
        return errors
