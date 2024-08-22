from xia_module_terraform_gcs.gcs import GcsState
from xia_module_terraform_gcs.foundation_gcs import FoundationGcsState
from xia_module_terraform_gcs.application_gcs import ApplicationGcsState

modules = {
    "module-state-gcs": "GcsState",
    "module-foundation-state-gcs": "FoundationGcsState",
    "module-application-state-gcs": "ApplicationGcsState",
}

__all__ = [
    "GcsState",
    "FoundationGcsState",
    "ApplicationGcsState"
]

__version__ = "0.0.5"
