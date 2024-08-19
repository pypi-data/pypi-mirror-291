import requests
import time
from enum import Enum
from datetime import datetime
from .const import API_URL, USER_AGENT

class LockConnectionStatus(Enum):
    OFFLINE = 'offline'
    DISCONNECTED = 'disconnected'
    CONNECTED = 'connected'
    BUSY = 'busy'

class LockOperationType(Enum):
    LOCK = 'lock'
    UNLOCK = 'unlock'

class LockOperationStatus(Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    TIMEOUT = 'timeout'
    FAILED = 'failed'

class EventType(Enum):
    UNKNOWN = 'unknown'
    LOCAL_LOCK = 'localLock'
    LOCAL_UNLOCK = 'localUnlock'
    REMOTE_LOCK = 'remoteLock'
    REMOTE_UNLOCK = 'remoteUnlock'
    PRESS_AND_GO = 'pressAndGo'
    MANUAL_UNLOCK = 'manualUnlock'
    MANUAL_LOCK = 'manualLock'

class LockEvent:
    def __init__(self, event_type: EventType, event_time: datetime):
        self.event_type = event_type
        self.event_time = event_time

    @classmethod
    def from_json(cls, data):
        if not data:
            return None
        return cls(
            event_type=EventType(data['eventType']),
            event_time=datetime.fromisoformat(data['eventTime'])
        )

class Lock:
    def __init__(self, api_key: str, id: str, serial_number: str, description: str, firmware_version: str, 
                 battery_status: int, connection_status: str, last_lock_event):
        self.api_key = api_key
        self.id = id
        self.serial_number = serial_number
        self.description = description
        self.firmware_version = firmware_version
        self.battery_status = battery_status
        self.connection_status = LockConnectionStatus(connection_status)
        self.last_lock_event = LockEvent.from_json(last_lock_event) if last_lock_event else None

    @classmethod
    def from_json(cls, api_key: str, data: dict):
        return cls(
            api_key=api_key,
            id=data['id'],
            serial_number=data['serialNumber'],
            description=data['description'],
            firmware_version=data['firmwareVersion'],
            battery_status=data['batteryStatus'],
            connection_status=data['connectionStatus'],
            last_lock_event=data.get('lastLockEvent')
        )

    def update(self):
        response = requests.get(f'{API_URL}/v1/locks/{self.id}', 
                                headers={'Authorization': f'Api-Key {self.api_key}',
                                         'User-Agent': USER_AGENT})
        response.raise_for_status()
        data = response.json()
        
        self.serial_number = data['serialNumber']
        self.description = data['description']
        self.firmware_version = data['firmwareVersion']
        self.battery_status = data['batteryStatus']
        self.connection_status = LockConnectionStatus(data['connectionStatus'])
        self.last_lock_event = LockEvent.from_json(data.get('lastLockEvent'))

    def lock(self):
        return self._create_lock_operation(LockOperationType.LOCK.value)

    def unlock(self):
        return self._create_lock_operation(LockOperationType.UNLOCK.value)

    def _create_lock_operation(self, operation_type: str):
        response = requests.post(f'{API_URL}/v1/locks/{self.id}/operations', 
                                 json={'type': operation_type},
                                 headers={'Authorization': f'Api-Key {self.api_key}',
                                          'User-Agent': USER_AGENT})
        response.raise_for_status()
        operation = LockOperation.from_json(response.json())
        return self._wait_for_operation(operation)

    def _wait_for_operation(self, operation):
        max_attempts = 20
        wait_time = 1

        for _ in range(max_attempts):
            if operation.is_finished():
                return operation.status == LockOperationStatus.COMPLETED

            time.sleep(wait_time)
            response = requests.get(f'{API_URL}/v1/locks/{self.id}/operations/{operation.id}', 
                                    headers={'Authorization': f'Api-Key {self.api_key}',
                                             'User-Agent': USER_AGENT})
            response.raise_for_status()
            operation = LockOperation.from_json(response.json())

        raise TimeoutError(f"Operation did not complete after {max_attempts} attempts")

class LockOperation:
    def __init__(self, id, status, reason=None):
        self.id = id
        self.status = LockOperationStatus(status)
        self.reason = reason

    @classmethod
    def from_json(cls, data):
        return cls(
            id=data['id'],
            status=data['status'],
            reason=data.get('reason')
        )

    def is_finished(self):
        return self.status != LockOperationStatus.PENDING
