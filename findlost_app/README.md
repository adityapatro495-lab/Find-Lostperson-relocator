# FINDLOST — Lost Person Relocator Through Image Recognition

FINDLOST is a Django web app that helps reunite missing persons with their
families. Families register a missing person with a photo; volunteers
report sightings with a photo; the app automatically compares faces and
queues likely matches for an administrator to verify before anyone is
contacted.

This README explains, step by step, how to get the project running on
your own machine — no prior Django experience required.

---

## 1. What you need installed first

| Requirement | Why | Check with |
|---|---|---|
| Python 3.10 or 3.11 | Runs the app (Django 4.2 supports 3.8–3.12) | `python3 --version` |
| pip | Installs Python packages | `pip --version` |
| CMake + a C++ compiler | Needed to build `dlib`, the face-recognition engine | see below |
| Git | To clone/push this repo | `git --version` |

**About `dlib` / `face-recognition`:** these packages do the actual face
detection and are the trickiest part of setup because `dlib` compiles
native C++ code. Install the build tools *before* `pip install`:

- **Ubuntu/Debian:** `sudo apt update && sudo apt install cmake build-essential python3-dev`
- **macOS:** `xcode-select --install` then `brew install cmake`
- **Windows:** install "Desktop development with C++" via the
  [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/),
  and install [CMake](https://cmake.org/download/) and add it to your PATH.
  If `dlib` still fails to build, installing via conda
  (`conda install -c conda-forge dlib`) is usually the path of least
  resistance on Windows.

The `dlib`/`face-recognition` build can take several minutes — that's
normal, not a hang.

---

## 2. Clone and set up a virtual environment

```bash
git clone https://github.com/adityapatro495-lab/Find-Lostperson-relocator.git
cd Find-Lostperson-relocator/findlost_app

python3 -m venv venv
source venv/bin/activate        # Windows (PowerShell): venv\Scripts\Activate.ps1
```

## 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

If `dlib` fails to build, re-read the compiler notes in step 1 — this is
almost always a missing CMake/compiler issue, not a bug in this repo.

## 4. Set up the database

The repo already includes the Django migration files, so you do **not**
need to run `makemigrations` — just apply them:

```bash
python manage.py migrate
```

Then create an administrator account (this is a normal Django superuser;
FINDLOST automatically gives superusers the `ADMIN` role):

```bash
python manage.py createsuperuser
```

## 5. Run the development server

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in your browser.

## 6. Try it out

| Page | URL | Who |
|---|---|---|
| Home | `/` | everyone |
| Create account | `/accounts/register/` | everyone (choose role: Family / Volunteer / Administrator) |
| Sign in | `/login/` | everyone |
| Register a missing person | `/registry/register/` | signed-in users |
| My registered cases | `/registry/dashboard/` | signed-in users |
| Report a sighting | `/report/` | signed-in users |
| Match review dashboard | `/matching/review/` | ADMIN role only |
| Django admin | `/admin/` | superuser |

**Suggested first walkthrough:**
1. Sign up once as a **Family** user, register a missing person with a
   clear front-facing photo.
2. Sign up again (different browser tab / incognito, or log out first)
   as a **Volunteer**, and submit a sighting report using a *different
   photo of the same person* (or the same photo, for a guaranteed match).
3. Sign up a third time as an **Administrator** (or use the
   `createsuperuser` account from step 4), visit `/matching/review/`,
   and approve or reject the candidate match.
4. Approving a match sends a notification email — since the project
   ships with the console email backend, the email text is printed
   straight into the terminal running `runserver` rather than actually
   being sent.

If a photo upload says "No face could be detected," it means
`face_recognition` genuinely couldn't find a face in that image — use a
clear, front-facing, well-lit photo.

---

## Configuration

- **Email:** defaults to the console backend (prints to your terminal).
  To send real emails, edit `findlost/settings.py` and switch to the
  SMTP backend — a commented-out example is provided there.
- **Match sensitivity:** `MATCH_CONFIDENCE_THRESHOLD` in
  `findlost/settings.py` (default `0.6`) controls how close two faces'
  encodings must be to count as a candidate match. Lower = stricter.
- **Secret key:** `findlost/settings.py` ships with a placeholder
  `SECRET_KEY` so the project runs out of the box. Replace it with a
  unique value (and ideally load it from an environment variable)
  before deploying anywhere public.

## Running tests

```bash
python manage.py test
```

`tests/test_matching.py` also has a face-matching test that needs
sample images placed manually in `tests/fixtures/` before it will pass:
`person_a_1.jpg` and `person_a_2.jpg` (two photos of the same person),
`person_c_1.jpg` (a different person), and `no_face.jpg` (an image with
no face in it). These images aren't included in the repo — supply your
own test photos locally.

## Project structure

```
findlost_app/
├── accounts/     — user accounts & roles (Family / Volunteer / Admin)
├── registry/     — missing-person case registration
├── reporting/    — volunteer sighting reports
├── matching/     — face-encoding comparison engine & admin review
├── notify/       — email notifications on confirmed matches
├── findlost/     — Django project settings/URLs
├── templates/    — HTML templates (Bootstrap 5)
├── static/       — CSS
├── media/        — uploaded photos (created at runtime)
└── tests/        — automated tests
```

## Troubleshooting

- **`ModuleNotFoundError: No module named 'django'`** — your virtual
  environment isn't activated, or `pip install -r requirements.txt`
  didn't finish. Re-run step 2/3.
- **`dlib` fails to build** — you're missing CMake or a C++ compiler.
  See step 1.
- **`OperationalError: no such table`** — you skipped `python manage.py
  migrate`.
- **Static files (Bootstrap styling) don't load in production** — this
  project is configured for local development (`DEBUG=True` serves
  static/media automatically). For a real deployment you'll need
  `collectstatic` and a proper static-file server.

## Known limitations

This is an academic prototype, not a hardened production system.
Notable gaps if you intend to deploy it for real:

- No rate-limiting or abuse protection on photo uploads.
- No consent/legal review for storing biometric face encodings.
- SQLite is fine for development but should be swapped for
  PostgreSQL/MySQL for anything beyond a single-user demo.
- Face encodings are stored as raw bytes in the database; a real
  deployment should encrypt this data at rest.
