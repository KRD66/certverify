# CertVerify — Build Order (Simplest → Complex)

Stack: Python, Django, DRF, SQLite, Cloudinary, Render, TokenAuthentication
Each numbered block is roughly one sitting. Tick items off as you go.

---

## 1. Project & App Setup
*Difficulty: Easy*

- [ ] Create Django project `certverify`
- [ ] Create app `certificates`
- [ ] Add `certificates`, `rest_framework`, `rest_framework.authtoken` to `INSTALLED_APPS`
- [ ] Basic `settings.py` sanity check (nothing fancy yet)
- [ ] `.gitignore` in place before first commit (venv/, db.sqlite3, __pycache__/, .env, media/)

---

## 2. Certificate Model
*Difficulty: Easy*

- [ ] Build the `Certificate` model with all fields (UUID PK, recipient info, course info, dates, status, remarks, timestamps)
- [ ] Decide: `is_valid` as a computed property that checks `expiry_date` live, vs. a stored flag that needs a scheduled task to flip — pick the computed property unless you have a specific reason not to (simpler, no cron job needed)
- [ ] Run migrations
- [ ] **Test:** open a shell (`python manage.py shell`), create a certificate manually, confirm fields and computed status behave as expected

---

## 3. Basic Admin Registration
*Difficulty: Easy*

- [ ] Register `Certificate` in `admin.py` (plain `register`, no customization)
- [ ] Manually add a test certificate through `/admin/` to confirm the model works

---

## 4. Serializers
*Difficulty: Easy–Medium*

- [ ] Build `CertificateSerializer` covering all fields, for use in the admin/API side
- [ ] Decide if a separate slim serializer is needed for public JSON verification (optional)

---

## 5. Public Views (HTML, no auth)
*Difficulty: Medium*

- [ ] Home view (`/`) — landing page with search bar
- [ ] Search view (`/search/`) — search by **full name or full/near-complete certificate ID only** (avoid partial-name matching — it lets anyone probe for who holds a certificate; require enough specificity that a search returns a small, intentional result)
- [ ] Verify view (`/verify/<uuid>/`) — show valid/revoked/expired + certificate details
- [ ] Public URL routing for the above
- [ ] **Test:** hit each view manually with a valid UUID, an invalid UUID, and a revoked cert's UUID — confirm each renders the right state

---

## 6. Templates
*Difficulty: Medium*

- [ ] `base.html` — shared layout
- [ ] `home.html`
- [ ] `search.html`
- [ ] `verify.html`

---

## 7. Authentication Setup
*Difficulty: Medium*

- [ ] Confirm `rest_framework.authtoken` migrations are applied
- [ ] Set up a way to obtain a token (Django admin token creation, or a simple obtain-token endpoint)
- [ ] Configure `TokenAuthentication` + `IsAuthenticated` as defaults for the admin/API views

---

## 8. Admin / API Views (DRF)
*Difficulty: Medium–Hard*

- [ ] List certificates (GET) — staff only
- [ ] Retrieve single certificate (GET) — staff only
- [ ] Create/issue certificate (POST) — staff only
- [ ] Update certificate (PATCH/PUT) — staff only
- [ ] Revoke certificate (custom action or PATCH toggling `is_valid`) — staff only
- [ ] API URL routing (`/api/...`)
- [ ] Add DRF throttle classes to the admin API (even a basic `UserRateThrottle`) so authenticated abuse is still bounded
- [ ] **Test:** curl every endpoint with a valid token, then without one, confirming 401/403 behave correctly

---

## 9. QR Code Generation
*Difficulty: Hard (new library)*

- [ ] Build a utility function that takes a certificate UUID, builds the verification URL, and generates a QR image
- [ ] Hook it into certificate creation (signal or overridden `save()`) so QR auto-generates
- [ ] Confirm QR image displays correctly (locally first, before Cloudinary)
- [ ] **Test:** scan a generated QR with a phone, confirm it lands on the correct verify page

---

## 10. PDF Certificate Generation
*Difficulty: Hard (new library)*

- [ ] Build a PDF generator in `utils.py` using ReportLab (recipient name, course, dates, cert ID, issuer, QR code)
- [ ] Build the download view (`/download/<uuid>/`) that streams the PDF

---

## 11. Cloudinary Integration
*Difficulty: Hard (new service)*

- [ ] Install and configure `django-cloudinary-storage`
- [ ] Set Cloudinary env vars
- [ ] Confirm QR images upload to Cloudinary instead of local disk
- [ ] Confirm images persist correctly through the model's `qr_code` field

---

## 12. Deployment
*Difficulty: Medium (mostly config, not code)*

- [ ] `requirements.txt`
- [ ] `Procfile` (`gunicorn certverify.wsgi`)
- [ ] `.env.example`
- [ ] Add basic rate limiting to the public search/verify views before going live (reuse the Redis fixed-window pattern from the URL Shortener, or a lighter Django-only version if Redis feels like overkill for this project's scope)
- [ ] README — honest pass on what's actually implemented vs. planned, same discipline as ITS/SecureNet
- [ ] Push to GitHub
- [ ] Create Render Web Service, connect repo
- [ ] Set build/start commands + environment variables
- [ ] Deploy and confirm live `.onrender.com` URL works end-to-end (issue → QR → verify → download)

---

## Suggested Pacing
Lighter sessions (models, serializers, admin registration) pair well with weekday after-hours slots.
Heavier sessions (QR, PDF, Cloudinary) are better saved for Sundays when you have more uninterrupted time.
