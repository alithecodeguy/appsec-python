from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from examples.ch27.export_crypto import Keyring


def dummy_keyrings():
    # Disposable, independent keys; never persisted, printed, or used outside synthetic runs.
    return {workspace:Keyring({f"export-w{workspace}-demo":AESGCM.generate_key(bit_length=256)},
                             f"export-w{workspace}-demo") for workspace in (1,2)}
