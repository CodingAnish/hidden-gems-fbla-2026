# Deployment Guide

Complete guide for deploying Hidden Gems to Render.com's free tier.

## Platform: Render.com (Recommended)

Render offers free Python deployments with automatic GitHub integration. Perfect for Flask applications.

### Prerequisites

- GitHub account
- Render account (free): https://render.com
- Project pushed to a GitHub repository

## Step-by-Step Deployment

### 1. Prepare Your Repository

Ensure these files are in your repo:
- `requirements.txt` (Python dependencies)
- `render.yaml` (Render configuration)
- `.gitignore` (excludes `.env`, `config.py`, etc.)

**Important**: Never commit `.env` or `config.py` files containing API keys!

### 2. Create Render Account

1. Visit https://render.com
2. Sign up with GitHub
3. Authorize Render to access your repositories

### 3. Create New Web Service

1. Click **New +** → **Web Service**
2. Connect your GitHub repository (may need to grant access)
3. Select `hidden-gems-fbla-2026` repository

### 4. Configure Service Settings

| Setting           | Value                              |
|-------------------|-------------------------------------|
| **Name**          | hidden-gems-fbla-2026             |
| **Environment**   | Python 3                           |
| **Region**        | Oregon (US West) - free tier       |
| **Branch**        | main                               |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python -m web.app`               |

### 5. Set Environment Variables

In the Render dashboard, go to **Environment** tab and add:

```
SECRET_KEY=generate-using-secrets-module-see-below
GROQ_API_KEY=gsk_your-groq-api-key
SENDGRID_API_KEY=SG.your-sendgrid-api-key
FROM_EMAIL=your-verified-sender@domain.com
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
YELP_API_KEY=your-yelp-api-key
HUGGINGFACE_API_KEY=your-hf-api-key
```

**Generate SECRET_KEY**:
```python
from secrets import token_urlsafe
print(token_urlsafe(32))
```

**Optional Variables**: GROQ_API_KEY is highly recommended for chatbot. Others optional.

### 6. Deploy

1. Click **Create Web Service**
2. Watch the deployment logs
3. Wait for "Your service is live 🎉" message (1-2 minutes)

Your app will be live at: `https://your-service-name.onrender.com`

## API Keys Setup

### Groq API (Free - Required for Chatbot)
1. Visit https://console.groq.com
2. Create account (no credit card needed)
3. Go to **API Keys** section
4. Generate new key
5. Copy key starting with `gsk_`
6. Add to Render environment variables

### SendGrid (Free - Required for Email)
1. Visit https://sendgrid.com
2. Create free account (100 emails/day)
3. Verify your sender email address
4. Go to **Settings** → **API Keys**
5. Create new API key
6. Copy key starting with `SG.`
7. Add to Render environment variables

### Google Maps (Free Tier)
1. Visit https://cloud.google.com/maps-platform
2. Create project
3. Enable **Maps JavaScript API** and **Geocoding API**
4. Create API key
5. (Optional) Restrict key to your domain
6. Add to Render environment variables

## Post-Deployment

### Verify Deployment

1. Visit your Render URL
2. Test user registration
3. Check email verification (should show code or send email)
4. Try logging in
5. Test chatbot functionality
6. Browse businesses and submit a review

### Monitor logs

- Go to Render dashboard → **Logs** tab
- Watch for errors or warnings
- Check `[DEBUG]` messages from chatbot
- Monitor performance and response times

### Auto-Deployment

Render automatically redeploys when you push to GitHub:

```bash
git add .
git commit -m "Update feature"
git push origin main
```

Render detects the push and redeploys (~1-2 minutes).

## Troubleshooting

### Build Fails

**Check:**
- `requirements.txt` has all dependencies
- No syntax errors in Python files
- Render has access to your repository

**Solution:**
- Review build logs in Render dashboard
- Ensure Python 3.10+ compatibility
- Check for missing dependencies

### App Doesn't Start

**Check:**
- Start command is `python -m web.app`
- Port binding (Render injects PORT variable)
- Database file permissions

**Solution:**
- Verify WSGI is correct in logs
- Check that Flask app runs locally first
- Review startup logs for errors

### Environment Variables Not Loading

**Check:**
- Variables set in Render Environment tab
- No typos in variable names
- Correct capitalization (case-sensitive)

**Solution:**
- Restart service after adding variables
- Verify variable names match code
- Check logs for "API Keys available" debug messages

### Chatbot Returns Generic Responses

**Check:**
- `GROQ_API_KEY` is set correctly
- API key is active on groq.com
- Check logs for "Groq API error" messages

**Solution:**
- Verify API key hasn't expired
- Test API key locally first
- Check internet connectivity from Render

### Email Not Sending

**Check:**
- `SENDGRID_API_KEY` is set
- `FROM_EMAIL` matches verified sender in SendGrid
- SendGrid account is active

**Solution:**
- Verify sender email in SendGrid dashboard
- Check SendGrid API key permissions
- Review email logs in SendGrid

### Performance Issues

**Symptoms:**
- Slow response times
- Timeouts
- High latency

**Solutions:**
- Optimize database queries
- Reduce chatbot context size
- Add caching for static content
- Consider paid Render tier for more resources

## Limiting Rate Limits (Future)

For production, consider adding:
- API rate limiting per user
- Request throttling
- Caching for frequently accessed data
- CDN for static assets (if scaling)

## Database Persistence

Render's free tier includes:
- Persistent disk storage
- SQLite database survives redeploys
- Automatic backups (manual download only)

**Backup locally**:
```bash
# Download database from Render
# Use Render Shell or SFTP
```

## Scaling

Free tier limitations:
- 512 MB RAM
- Shared CPU
- Sleeps after 15 minutes of inactivity
- Cold starts (~30 seconds to wake)

**Upgrade needed if:**
- High traffic (>1000 monthly users)
- Need 24/7 uptime
- Require dedicated resources

## Security Checklist

Before going live:

- [ ] Unique `SECRET_KEY` generated
- [ ] All API keys in environment variables (not code)
- [ ] `.env` and `config.py` in `.gitignore`
- [ ] HTTPS enabled (automatic on Render)
- [ ] Email sender verified
- [ ] Tested all features in production env
- [ ] Reviewed logs for sensitive data leaks
- [ ] Password reset functionality works
- [ ] CAPTCHA working on reviews

## Maintenance

### Regular Tasks

- Monitor logs weekly
- Check error rates
- Review SendGrid email usage
- Test features after updates
- Update dependencies quarterly

### Updating Dependencies

```bash
# Locally
pip list --outdated
pip install --upgrade package-name
pip freeze > requirements.txt

# Push to GitHub
git add requirements.txt
git commit -m "Update dependencies"
git push origin main
```

Render automatically redeploys with new dependencies.

## Environment-Specific Configurations

### Development (.env local)
```env
FLASK_DEBUG=True
SECRET_KEY=dev-secret-key
```

### Production (Render)
```env
FLASK_DEBUG=False
SECRET_KEY=strong-random-key
```

## Support

### Render Resources
- Documentation: https://render.com/docs
- Status page: https://status.render.com
- Community: https://community.render.com

### Hidden Gems Support
- GitHub Issues: [Your repo issues page]
- Documentation: `/docs` folder
- Email: [Your contact email]

---

**Deployment Complete!** Your Hidden Gems app should now be live and accessible worldwide.

Last Updated: February 2026
