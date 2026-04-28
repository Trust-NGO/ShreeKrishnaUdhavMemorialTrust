# Validation Fix TODO

## Steps
- [x] Step 1: Fix `schemas.py` — Define `TeamMemberBase` properly and remove misplaced fields from `AuditLog`
- [x] Step 2: Fix `financial_transparency.html` — Add missing closing `</div>` tags in Fund Utilization grid
- [x] Step 3: Fix `admin_routes.py` — Enforce `MAX_FILE_SIZE` in `validate_file_upload()`
- [x] Step 4: Fix `donation_routes.py` — Use `Optional` types in `PaymentVerificationData` and validate amount
- [x] Step 5: Fix `api_routes.py` — Add Pydantic schema for `create_order` with amount bounds
- [x] Step 6: Fix `page_routes.py` — Use `EmailStr` for volunteer email
- [x] Step 7: Run syntax check on modified Python files

