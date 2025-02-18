import base64
import logging
from config import ENCRYPTION_KEY

logger = logging.getLogger(__name__)


class EncryptorDecryptor:
    @staticmethod
    def encrypt(data: str) -> str:
        """מצפין מידע באמצעות XOR cipher ומחזיר מחרוזת base64."""
        try:
            data_bytes = data.encode('utf-8')
            encrypted = bytes(
                [(data_bytes[i] ^ ENCRYPTION_KEY[i % len(ENCRYPTION_KEY)]) for i in range(len(data_bytes))])
            return base64.b64encode(encrypted).decode('utf-8')
        except Exception as e:
            logger.error(f"Encryption error: {e}")
            raise

    @staticmethod
    def decrypt(encrypted_b64: str) -> str:
        """מפענח מחרוזת מוצפנת ב-base64."""
        try:
            encrypted_data = base64.b64decode(encrypted_b64)
            decrypted = bytes(
                [(encrypted_data[i] ^ ENCRYPTION_KEY[i % len(ENCRYPTION_KEY)]) for i in range(len(encrypted_data))])
            return decrypted.decode('utf-8')
        except Exception as e:
            logger.error(f"Decryption error: {e}")
            return ""
