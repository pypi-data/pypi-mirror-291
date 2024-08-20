import os
from enum import Enum
from resemble.settings import (
    ENVVAR_KUBERNETES_SERVICE_HOST,
    ENVVAR_NODEJS_CONSENSUS,
    ENVVAR_RSM_DEV,
    ENVVAR_RSM_SERVE,
)


class RunEnvironment(Enum):
    """Known run environments."""
    RSM_DEV = 1
    RSM_SERVE = 2
    KUBERNETES = 3
    NODEJS_CONSENSUS = 4


class InvalidRunEnvironment(RuntimeError):
    """Exception for when run environment cannot be determined."""
    pass


def _detect_run_environment() -> RunEnvironment:
    """Internal helper to determine what run environment we are in."""
    # NOTE: ordering matters here as we may have multiple environment
    # variables set but some take precedence to others.
    if os.environ.get(ENVVAR_NODEJS_CONSENSUS, 'false').lower() == 'true':
        return RunEnvironment.NODEJS_CONSENSUS
    elif os.environ.get(ENVVAR_RSM_DEV, 'false').lower() == 'true':
        return RunEnvironment.RSM_DEV
    elif os.environ.get(ENVVAR_RSM_SERVE, 'false').lower() == 'true':
        return RunEnvironment.RSM_SERVE
    elif os.environ.get(ENVVAR_KUBERNETES_SERVICE_HOST) is not None:
        return RunEnvironment.KUBERNETES

    raise InvalidRunEnvironment()


def on_kubernetes() -> bool:
    """Helper for checking if we are running in a Kubernetes
    cluster."""
    try:
        return _detect_run_environment() == RunEnvironment.KUBERNETES
    except InvalidRunEnvironment:
        return False


def running_rsm_dev() -> bool:
    """Helper for checking if we are running in a local development
    environment."""
    try:
        return _detect_run_environment() == RunEnvironment.RSM_DEV
    except InvalidRunEnvironment:
        return False
