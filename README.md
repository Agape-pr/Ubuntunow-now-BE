# Ubuntunow-now-BE
Ubuntunow backend dev repo.

## Deploy to Render

### Render Blueprint (recommended)
- **Add a Postgres database** in Render, then connect it to the web service so `DATABASE_URL` is available.
- In Render, create a new service and select **Blueprint**, pointing to this repo. Render will pick up `render.yaml`.

### Required environment variables
Render will set `PORT` and (if you add a Render Postgres instance) `DATABASE_URL`.

You must set/provide:
- `DJANGO_SETTINGS_MODULE=config.settings.prod`
- `DJANGO_SECRET_KEY` (Render can generate this)
- `DJANGO_ALLOWED_HOSTS` (comma-separated). You can set it to your Render hostname, e.g. `ubuntunow-api.onrender.com`

Optional:
- **CORS**: set `CORS_ALLOWED_ORIGINS` (comma-separated) to your frontend origin(s), e.g. `https://your-frontend.com,http://localhost:3000`
- **SendGrid (OTP email)**:
  - `SENDGRID_API_KEY`
  - `SENDGRID_FROM_EMAIL`
  - `SENDGRID_FROM_NAME`
  - `SENDGRID_TEMPLATE_OTP_ID`

### Commands Render will run
- **Build**: installs deps + `collectstatic`
- **Start**: runs `migrate` then starts `gunicorn`

