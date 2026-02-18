# Deployment Guide - Hidden Gems FBLA 2026

This guide explains how to deploy the Hidden Gems website to a live hosting platform.

## Quick Deploy to Render (Free Hosting)

### Prerequisites
- GitHub account with your code pushed
- Free Render account ([render.com](https://render.com))
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Step 1: Sign Up for Render
1. Go to [render.com](https://render.com)
2. Click "Get Started" and sign up with your GitHub account
3. Authorize Render to access your GitHub repositories

### Step 2: Create a New Web Service
1. From your Render dashboard, click "New +"
2. Select "Web Service"
3. Connect your GitHub repository: `CodingAnish/hidden-gems-fbla-2026`
4. Render will auto-detect the `render.yaml` configuration file

### Step 3: Configure Environment Variables
In the Render dashboard, add these environment variables:

**Required:**
- `SECRET_KEY`: Generate a random string (e.g., use a password generator)
- `GROQ_API_KEY`: Your Groq API key from console.groq.com
- `FLASK_ENV`: Set to `production`
- `FLASK_DEBUG`: Set to `false`

**Optional (for email verification):**
- `SMTP_HOST`: Your email provider's SMTP server (e.g., `smtp.gmail.com`)
- `SMTP_PORT`: SMTP port (usually `587`)
- `SMTP_USER`: Your email address
- `SMTP_PASSWORD`: Your email app password

### Step 4: Deploy
1. Click "Create Web Service"
2. Render will automatically:
   - Install dependencies from `requirements.txt`
   - Initialize the database
   - Start the Flask application
3. Wait 2-5 minutes for the first build
4. Your site will be live at: `https://hidden-gems-fbla.onrender.com`

### Step 5: Test Your Live Site
1. Visit your Render URL
2. Test user registration and login
3. Browse businesses in the directory
4. Try the AI chatbot recommendations
5. Test favorites and reviews

## Alternative Hosting Options

### Deploy to Railway
1. Visit [railway.app](https://railway.app)
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Add environment variables
6. Deploy!

### Deploy to Vercel
1. Visit [vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Configure as a Python project
4. Add environment variables
5. Deploy!

## Environment Variables Explained

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `SECRET_KEY` | Flask session encryption key | Yes | `r4nd0m-s3cr3t-k3y-h3r3` |
| `GROQ_API_KEY` | AI chatbot API key | Yes | `gsk_abc123...` |
| `FLASK_ENV` | Environment mode | Yes | `production` |
| `FLASK_DEBUG` | Debug mode (false for production) | Yes | `false` |
| `SMTP_HOST` | Email server hostname | No | `smtp.gmail.com` |
| `SMTP_PORT` | Email server port | No | `587` |
| `SMTP_USER` | Email sending account | No | `yourapp@gmail.com` |
| `SMTP_PASSWORD` | Email app password | No | `apppassword123` |
| `PORT` | Web server port (auto-set by host) | No | `10000` |

## Getting API Keys

### Groq API (Required for Chatbot)
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Navigate to "API Keys"
4. Click "Create API Key"
5. Copy the key (starts with `gsk_`)

### Email Configuration (Optional)
For Gmail:
1. Enable 2-Factor Authentication
2. Go to Google Account > Security > App Passwords
3. Create an app password for "Mail"
4. Use this password (not your regular Gmail password)

## Troubleshooting

### Build Failed
- Check that `requirements.txt` has all dependencies
- Verify Python version compatibility (3.8+)
- Check build logs for specific error messages

### Site Won't Load
- Verify all required environment variables are set
- Check that `PORT` environment variable is correctly read
- Review application logs in Render dashboard

### Database Issues
- SQLite database is created automatically on first run
- Database persists on Render's free tier disk storage
- Database resets if service restarts (upgrade to paid for persistence)

### Chatbot Not Working
- Verify `GROQ_API_KEY` is correctly set
- Check API key hasn't exceeded usage limits
- Review chatbot error logs

## Custom Domain (Optional)

To use your own domain:
1. In Render dashboard, go to Settings > Custom Domain
2. Add your domain name
3. Update DNS records as instructed
4. Wait for DNS propagation (up to 48 hours)

## Continuous Deployment

With Render's auto-deploy enabled:
1. Push changes to GitHub main branch
2. Render automatically detects changes
3. Rebuilds and redeploys your site
4. Updates are live in 2-5 minutes

## Support

For issues:
- Check [Render documentation](https://render.com/docs)
- Review application logs in dashboard
- Contact FBLA advisor or team members
