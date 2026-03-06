# Logging Improvements - User Failure Tracking

## Summary

All exception handlers and error paths now log failures with `user_id` using structured logging via `log_event()`. This enables you to answer questions like **"Why did user 482 get a failure at 3:04pm?"**

## Changes Made

### 1. Created Middleware for User ID Extraction

**`app/middleware/request_logging.py`**
- Extracts `user_id` from JWT token in Authorization header
- Stores `user_id` in `request.state` for use throughout request lifecycle
- Works even when authentication fails (extracts from token without DB lookup)

**`app/middleware/request_id.py`**
- Generates unique request ID for each request
- Stores in `request.state.request_id`
- Adds to response headers

### 2. Created Request Utilities

**`app/core/request_utils.py`**
- Helper functions to safely extract `user_id` and `request_id` from requests
- Used by exception handlers

### 3. Updated Exception Handlers

All exception handlers in `app/main.py` now use `log_event()` with `user_id`:

- **HTTPException handler** - Logs 400, 401, 403, 404 errors with user_id
- **RequestValidationError handler** - Logs 422 validation errors with user_id  
- **General Exception handler** - Logs 500 unhandled exceptions with user_id

Each log entry includes:
- `user_id` (if available)
- `request_id` (for correlation)
- `timestamp` (UTC)
- `event` name
- `level` (warning/error)
- `extra` metadata (status_code, method, path, error details, etc.)

### 4. Fixed Duplicate Functions

Cleaned up duplicate `get_current_user_from_query` functions in `app/auth.py`.

## How to Query Failures in Better Stack

### Example Query: "Why did user 482 get a failure at 3:04pm?"

In Better Stack, search for:
```
user_id:482 AND level:error AND timestamp:"2024-12-20T15:04"
```

Or more broadly:
```
user_id:482 AND (event:http_exception OR event:validation_error OR event:unhandled_exception)
```

### Available Event Types

- `http_exception` - HTTP 400, 401, 403, 404, 500 errors
- `validation_error` - Request validation failures (422)
- `unhandled_exception` - Unexpected exceptions (500)
- `llm_failure` - LLM service failures (already existed)
- `stt_failure` - Speech-to-text failures (already existed)
- `tts_failure` - Text-to-speech failures (already existed)

### Log Entry Structure

All failure logs now include:
```json
{
  "timestamp": "2024-12-20T15:04:23.123Z",
  "level": "error",
  "event": "http_exception",
  "message": "HTTPException 404 on GET /v1/situations/invalid_id: Situation not found",
  "request_id": "abc-123-def",
  "user_id": "482",
  "status_code": 404,
  "method": "GET",
  "path": "/v1/situations/invalid_id",
  "detail": "Situation not found"
}
```

## Testing

To verify logging works:

1. **Test HTTPException** (404):
   ```bash
   curl -H "Authorization: Bearer <token>" http://localhost:8000/v1/situations/invalid_id
   ```
   Should log: `event:http_exception` with `user_id` and `status_code:404`

2. **Test ValidationError** (422):
   ```bash
   curl -X POST http://localhost:8000/v1/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email":"test","password":"short"}'
   ```
   Should log: `event:validation_error` with validation errors

3. **Test Unhandled Exception**:
   Trigger an internal server error (if possible in test environment)
   Should log: `event:unhandled_exception` with full traceback

## Benefits

✅ **All failures now include user_id** - Can track failures per user  
✅ **Structured JSON logging** - Easy to query and filter in Better Stack  
✅ **Request correlation** - `request_id` links related logs  
✅ **Rich metadata** - Status codes, paths, error messages, tracebacks  
✅ **Backward compatible** - Still logs to Python logger for existing tools  

## Next Steps

Consider adding:
- User journey tracking (PostHog/Mixpanel) for product analytics
- Alerting on high error rates per user
- Dashboard for error trends by user_id


