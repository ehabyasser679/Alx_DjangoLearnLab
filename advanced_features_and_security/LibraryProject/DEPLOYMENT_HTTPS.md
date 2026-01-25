# HTTPS Deployment Configuration Guide

This guide provides step-by-step instructions for configuring HTTPS/SSL for the Library Project Django application in production environments.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [SSL/TLS Certificate Setup](#ssltls-certificate-setup)
3. [Nginx Configuration](#nginx-configuration)
4. [Apache Configuration](#apache-configuration)
5. [Django Settings Configuration](#django-settings-configuration)
6. [Testing HTTPS Configuration](#testing-https-configuration)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

- Django application deployed and running
- Domain name configured and pointing to your server
- Root or sudo access to the server
- Web server (Nginx or Apache) installed

## SSL/TLS Certificate Setup

### Option 1: Let's Encrypt (Recommended - Free)

Let's Encrypt provides free SSL certificates that are automatically renewed.

#### Installation

```bash
# Install Certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx  # For Nginx
# OR
sudo apt-get install certbot python3-certbot-apache  # For Apache
```

#### Obtain Certificate

```bash
# For Nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# For Apache
sudo certbot --apache -d yourdomain.com -d www.yourdomain.com

# Standalone (if web server is not running)
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com
```

#### Auto-Renewal

Certbot automatically sets up renewal. Test with:

```bash
sudo certbot renew --dry-run
```

### Option 2: Commercial SSL Certificate

If using a commercial certificate provider:

1. Purchase SSL certificate
2. Generate Certificate Signing Request (CSR)
3. Submit CSR to certificate authority
4. Install certificate files on server

## Nginx Configuration

### Basic HTTPS Configuration

Create or edit `/etc/nginx/sites-available/libraryproject`:

```nginx
# HTTP to HTTPS redirect
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect all HTTP traffic to HTTPS
    return 301 https://$server_name$request_uri;
}

# HTTPS server block
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL Certificate paths (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # SSL Configuration - Strong security settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Client body size (adjust as needed)
    client_max_body_size 10M;
    
    # Static files
    location /static/ {
        alias /path/to/your/project/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Media files (if applicable)
    location /media/ {
        alias /path/to/your/project/media/;
        expires 30d;
        add_header Cache-Control "public";
    }
    
    # Proxy to Django application
    location / {
        proxy_pass http://127.0.0.1:8000;  # Adjust port if using different port
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $server_name;
        
        # WebSocket support (if needed)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### Enable Site

```bash
# Create symbolic link
sudo ln -s /etc/nginx/sites-available/libraryproject /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

## Apache Configuration

### Basic HTTPS Configuration

Create or edit `/etc/apache2/sites-available/libraryproject-ssl.conf`:

```apache
# HTTP to HTTPS redirect
<VirtualHost *:80>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com
    
    # Redirect all HTTP traffic to HTTPS
    Redirect permanent / https://yourdomain.com/
</VirtualHost>

# HTTPS server block
<VirtualHost *:443>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com
    
    # SSL Configuration
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/yourdomain.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/yourdomain.com/privkey.pem
    
    # SSL Protocol Configuration
    SSLProtocol all -SSLv3 -TLSv1 -TLSv1.1
    SSLCipherSuite ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384
    SSLHonorCipherOrder on
    
    # Security Headers
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
    Header always set X-Frame-Options "DENY"
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-XSS-Protection "1; mode=block"
    Header always set Referrer-Policy "strict-origin-when-cross-origin"
    
    # Static files
    Alias /static /path/to/your/project/staticfiles
    <Directory /path/to/your/project/staticfiles>
        Require all granted
    </Directory>
    
    # Media files (if applicable)
    Alias /media /path/to/your/project/media
    <Directory /path/to/your/project/media>
        Require all granted
    </Directory>
    
    # WSGI Configuration
    WSGIDaemonProcess libraryproject python-home=/path/to/venv python-path=/path/to/project
    WSGIProcessGroup libraryproject
    WSGIScriptAlias / /path/to/project/LibraryProject/wsgi.py
    
    <Directory /path/to/project/LibraryProject>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>
    
    # Proxy headers for Django
    RequestHeader set X-Forwarded-Proto "https"
    RequestHeader set X-Forwarded-Host "yourdomain.com"
</VirtualHost>
```

### Enable Modules and Site

```bash
# Enable required modules
sudo a2enmod ssl
sudo a2enmod headers
sudo a2enmod rewrite

# Enable site
sudo a2ensite libraryproject-ssl.conf

# Test configuration
sudo apache2ctl configtest

# Restart Apache
sudo systemctl restart apache2
```

## Django Settings Configuration

### Production Settings

Update `settings.py` for production:

```python
# HTTPS Configuration
SECURE_SSL_REDIRECT = True  # Redirect HTTP to HTTPS
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Secure Cookies
SESSION_COOKIE_SECURE = True  # Only send over HTTPS
CSRF_COOKIE_SECURE = True  # Only send over HTTPS
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'

# Security Headers
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# Allowed Hosts
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Debug Mode
DEBUG = False

# Secret Key (must be changed from default)
SECRET_KEY = 'your-production-secret-key-here'  # Generate a new secret key!
```

### Proxy Configuration

If using a reverse proxy (Nginx/Apache), ensure Django knows about HTTPS:

```python
# Trust proxy headers
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Or use middleware (if needed)
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True
```

## Testing HTTPS Configuration

### 1. Test SSL Certificate

```bash
# Check certificate validity
openssl ssl_client -connect yourdomain.com:443 -showcerts

# Test with SSL Labs
# Visit: https://www.ssllabs.com/ssltest/analyze.html?d=yourdomain.com
```

### 2. Test HTTP to HTTPS Redirect

```bash
# Should redirect to HTTPS
curl -I http://yourdomain.com

# Should return 301 or 302 redirect
```

### 3. Test Security Headers

```bash
# Check headers
curl -I https://yourdomain.com

# Should include:
# - Strict-Transport-Security
# - X-Frame-Options: DENY
# - X-Content-Type-Options: nosniff
```

### 4. Test HSTS

1. Visit `https://yourdomain.com` in browser
2. Check browser developer tools → Network → Headers
3. Verify `Strict-Transport-Security` header is present

### 5. Test Cookie Security

1. Log in to the application
2. Open browser developer tools → Application → Cookies
3. Verify cookies have `Secure` flag set
4. Verify cookies are only sent over HTTPS

## Troubleshooting

### Issue: Redirect Loop

**Symptoms**: Site continuously redirects, page never loads

**Causes**:
- `SECURE_SSL_REDIRECT = True` but HTTPS not configured
- Proxy not forwarding `X-Forwarded-Proto` header

**Solutions**:
1. Ensure HTTPS is properly configured in web server
2. Set `SECURE_SSL_REDIRECT = False` temporarily to test
3. Configure proxy headers correctly

### Issue: Cookies Not Working

**Symptoms**: Users can't log in, sessions don't persist

**Causes**:
- `SESSION_COOKIE_SECURE = True` but site accessed via HTTP
- Cookie domain mismatch

**Solutions**:
1. Ensure all access is via HTTPS
2. Check cookie domain settings
3. Verify `SESSION_COOKIE_SAMESITE` setting

### Issue: Mixed Content Warnings

**Symptoms**: Browser shows "Mixed Content" warnings

**Causes**:
- Loading HTTP resources on HTTPS page
- External resources not using HTTPS

**Solutions**:
1. Ensure all static files served over HTTPS
2. Update external resource URLs to HTTPS
3. Use relative URLs where possible

### Issue: HSTS Not Working

**Symptoms**: HSTS header not present or not being respected

**Causes**:
- Header not set correctly
- Browser hasn't seen header yet

**Solutions**:
1. Verify header in response: `curl -I https://yourdomain.com`
2. Clear browser cache and cookies
3. Ensure `SECURE_HSTS_SECONDS` is set correctly

## Security Checklist

Before going live, verify:

- [ ] SSL certificate is valid and not expired
- [ ] HTTP to HTTPS redirect works
- [ ] All cookies have `Secure` flag
- [ ] HSTS header is present
- [ ] Security headers are configured
- [ ] `DEBUG = False` in production
- [ ] `SECRET_KEY` is changed from default
- [ ] `ALLOWED_HOSTS` is configured
- [ ] No mixed content warnings
- [ ] SSL Labs test shows A or A+ rating

## Additional Resources

- [Django Security Documentation](https://docs.djangoproject.com/en/stable/topics/security/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
- [SSL Labs SSL Test](https://www.ssllabs.com/ssltest/)

## Notes

- **Development**: Keep HTTPS settings disabled (`SECURE_SSL_REDIRECT = False`) when developing locally
- **Production**: Always enable HTTPS settings before deploying to production
- **Testing**: Test HTTPS configuration in staging environment first
- **Monitoring**: Set up certificate expiration alerts (Let's Encrypt auto-renews, but monitor anyway)

