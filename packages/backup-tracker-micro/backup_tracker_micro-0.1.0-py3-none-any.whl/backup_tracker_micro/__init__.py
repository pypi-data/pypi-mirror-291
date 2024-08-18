"""
Transmit your backup events

```python
from backup_tracker_micro import BackupTracker, BackupEvent

b = BackupTracker("localhost", "documents", "http://localhost:5000/")
b.backup_event(BackupEvent.STARTED)
// Size of backup in KB
b.backup_status(100_347)
b.backup_event(BackupEvent.FINISHED)

res = b.get_backup_events()
print(res)
```
"""

from .backup import BackupTracker, BackupEvent

VERSION = (0, 1, 0)

VERSION_STRING = '.'.join(map(str, VERSION))

BackupTracker
BackupEvent
