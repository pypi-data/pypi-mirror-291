# Batocera Manager

## Initialize

```python
from batocera_manager import BatoceraManager

manager = BatoceraManager("192.168.0.123")

await manager.async_update_state(raise_errors=True)
```
