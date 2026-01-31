# MES Examples

Example scripts demonstrating the Factory MES system.

## Storage Demo

```bash
python examples/storage_demo.py
```

Demonstrates database operations.

## API Usage

Start the server:
```bash
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

Then use curl or any HTTP client:
```bash
curl http://localhost:8000/api/status/health
curl http://localhost:8000/api/status
curl http://localhost:8000/api/devices
curl http://localhost:8000/api/data/realtime
```
