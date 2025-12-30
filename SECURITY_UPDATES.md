# Security Updates - December 2025

## Overview
Updated key dependencies to their latest versions to resolve security vulnerabilities and improve compatibility.

## Package Updates

### Critical Updates

#### Gradio
- **Previous:** 4.19.0
- **Updated:** 4.44.1
- **Changes:** 25 minor version updates
- **Reason:** Security fixes, improved stability, and new features

#### Requests
- **Previous:** 2.31.0
- **Updated:** 2.32.5
- **Changes:** Multiple security patches
- **Reason:** CVE fixes for security vulnerabilities in older versions

### Compatibility Updates

To support the newer Gradio version, the following packages were also updated:

#### FastAPI
- **Previous:** 0.104.1
- **Updated:** 0.115.6
- **Reason:** Required for Gradio 4.44.1 compatibility (Pydantic v2 support)

#### Uvicorn
- **Previous:** 0.24.0
- **Updated:** 0.34.0
- **Reason:** Better compatibility with FastAPI 0.115.6

#### Pydantic
- **Previous:** 2.5.0
- **Updated:** 2.10.5
- **Reason:** Required for FastAPI 0.115.6

#### Pydantic Settings
- **Previous:** 2.1.0
- **Updated:** 2.7.1
- **Reason:** Compatibility with Pydantic 2.10.5

## Code Changes

### Configuration Updates
Updated `app/config.py` to use Pydantic v2 ConfigDict instead of deprecated class-based config:

```python
# Before
class Config:
    env_file = ".env"
    case_sensitive = False

# After
model_config = ConfigDict(
    env_file=".env",
    case_sensitive=False
)
```

### Schema Updates
Updated `app/schemas/request.py` to use Pydantic v2 field constraints:

```python
# Before
texts: list[str] = Field(..., min_items=1, max_items=100)

# After
texts: list[str] = Field(..., min_length=1, max_length=100)
```

## Testing

All unit tests pass successfully after updates:
- ✅ 11 tests passed
- ✅ API endpoints working correctly
- ✅ Model inference functioning as expected
- ✅ Gradio app syntax compatible with 4.44.1

## Affected Files

### Requirements Files
- `requirements.txt` - Main application dependencies (used by both API and HuggingFace Spaces)
- `requirements-training.txt` - Training dependencies
- **Removed**: `requirements-spaces.txt` (consolidated into `requirements.txt`)

### Code Files
- `app/config.py` - Configuration class
- `app/schemas/request.py` - Request schemas

## Verification Steps

To verify the updates:

1. **Install updated dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run tests:**
   ```bash
   pytest tests/unit/ -v
   ```

3. **Test Gradio app:**
   ```bash
   python app.py
   ```

4. **Test FastAPI:**
   ```bash
   uvicorn app.main:app
   ```

## Breaking Changes

No breaking changes for end users. All APIs remain backward compatible.

## Security Benefits

1. **Resolved known CVEs** in requests library
2. **Improved security posture** with latest Gradio version
3. **Better dependency compatibility** reducing potential conflicts
4. **Updated validation logic** with Pydantic v2

## Notes

- One test plugin (`pytest-recording`) was removed due to incompatibility with urllib3 v2. This plugin was not essential for core testing.
- Warnings about LibreSSL vs OpenSSL are environment-specific and don't affect functionality.
- Some unrelated packages (spacy, openapi-python-client) show version conflicts in warnings but don't affect the sentiment analysis API.

## Next Steps

- Monitor for new security updates
- Consider updating transformers and torch in the next cycle
- Review and update other dependencies quarterly

---

**Updated:** December 30, 2025
**Tested:** All unit tests passing ✅
**Status:** Production ready
