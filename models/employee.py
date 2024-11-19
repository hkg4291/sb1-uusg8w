from typing import List, Optional
from .base import BaseDocument
from .enums import EmployeeRole
from pydantic import Field
from cryptography.fernet import Fernet
from config import settings

cipher_suite = Fernet(settings.ENCRYPTION_KEY.encode())

class Employee(BaseDocument):
    role: EmployeeRole
    tasks: List[str] = Field(default_factory=list)
    _encrypted_first_name: Optional[bytes] = None
    _encrypted_last_name: Optional[bytes] = None
    _encrypted_email: Optional[bytes] = None
    _encrypted_phone: Optional[bytes] = None

    @property
    def first_name(self) -> str:
        return cipher_suite.decrypt(self._encrypted_first_name).decode()

    @first_name.setter
    def first_name(self, value: str):
        self._encrypted_first_name = cipher_suite.encrypt(value.encode())

    # Similar getters and setters for last_name, email, and phone
    
    class Settings:
        name = "employees"
        indexes = [
            "role"
        ]