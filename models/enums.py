from enum import Enum

class AnimalStatus(str, Enum):
    HEALTHY = "healthy"
    SICK = "sick"
    INJURED = "injured"

class EmployeeRole(str, Enum):
    VET = "vet"
    CARETAKER = "caretaker"
    MANAGER = "manager"