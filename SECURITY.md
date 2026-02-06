# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of Occamy Field Operations System seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### Please Do Not:
- Open a public GitHub issue
- Discuss the vulnerability publicly
- Exploit the vulnerability

### Please Do:
1. **Email us**: Send details to security@occamy.com
2. **Include**:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)
3. **Wait**: We'll acknowledge within 48 hours

### What to Expect:
- **48 hours**: Initial response acknowledging receipt
- **7 days**: Preliminary assessment and action plan
- **30 days**: Fix developed and tested
- **90 days**: Coordinated disclosure (if agreed)

## Security Best Practices

### For Deployment

#### 1. Environment Variables
Never commit sensitive data to the repository:

```bash
# .env (NEVER commit this file)
SECRET_KEY=your-random-secret-key-here
DATABASE_URL=postgresql://user:pass@localhost/db
```

#### 2. HTTPS Only
Always use HTTPS in production:

```python
# config.py
class ProductionConfig(Config):
    SESSION_COOKIE_SECURE = True
    PREFERRED_URL_SCHEME = 'https'
```

#### 3. Database Security
- Use strong passwords
- Limit database user permissions
- Enable SSL for database connections
- Regular backups
- Keep database software updated

```bash
# PostgreSQL example
CREATE USER occamy_user WITH PASSWORD 'strong-password-here';
GRANT CONNECT ON DATABASE occamy_db TO occamy_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO occamy_user;
```

#### 4. Session Security
Configure secure session handling:

```python
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
```

#### 5. Rate Limiting
Implement rate limiting to prevent abuse:

```bash
# nginx.conf already includes rate limiting
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
```

#### 6. Input Validation
Always validate and sanitize user input:

```python
from wtforms import StringField, validators

class MeetingForm(FlaskForm):
    person_name = StringField('Name', [validators.Length(min=2, max=100)])
    contact = StringField('Contact', [validators.Regexp(r'^\d{10}$')])
```

#### 7. SQL Injection Prevention
Use SQLAlchemy ORM (already implemented):

```python
# GOOD - Parameterized query
User.query.filter_by(username=username).first()

# BAD - String concatenation (don't do this!)
# db.execute(f"SELECT * FROM user WHERE username='{username}'")
```

#### 8. XSS Prevention
Jinja2 auto-escapes by default (already enabled):

```html
<!-- Safe - auto-escaped -->
<p>{{ user.name }}</p>

<!-- Unsafe - only if you explicitly use |safe -->
<!-- <p>{{ user.name | safe }}</p> -->
```

### For Development

#### 1. Dependencies
Keep dependencies updated:

```bash
pip list --outdated
pip install --upgrade package-name
```

#### 2. Secret Key
Generate strong secret keys:

```python
import secrets
print(secrets.token_hex(32))
```

#### 3. Password Policy
Enforce strong passwords:

```python
def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain uppercase"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain lowercase"
    if not re.search(r"\d", password):
        return False, "Password must contain number"
    return True, "Password is valid"
```

#### 4. CORS Configuration
Be specific with CORS if needed:

```python
from flask_cors import CORS

# Be specific, don't use '*'
CORS(app, origins=['https://yourdomain.com'])
```

## Known Security Considerations

### Current Implementation

1. **Default Admin Account**: 
   - Username: `admin`, Password: `admin123`
   - **MUST** be changed immediately after first login
   - Use strong password

2. **SQLite Database**:
   - Default for development
   - Single file, no user authentication
   - **Migrate to PostgreSQL** for production

3. **Session Management**:
   - Uses Flask-Login with sessions
   - Sessions stored in cookies
   - Configured for HTTP in development
   - **Enable HTTPS** in production

4. **No Email Verification**:
   - Email addresses not verified
   - Consider adding verification for production

5. **No 2FA**:
   - Two-factor authentication not implemented
   - Consider adding for admin accounts

## Security Checklist

Before deploying to production:

### Infrastructure
- [ ] Use HTTPS (SSL/TLS certificate)
- [ ] Enable firewall
- [ ] Close unnecessary ports
- [ ] Use secure hosting provider
- [ ] Enable DDoS protection

### Application
- [ ] Change default admin password
- [ ] Set strong SECRET_KEY
- [ ] Use PostgreSQL (not SQLite)
- [ ] Enable secure session cookies
- [ ] Implement rate limiting
- [ ] Add CSRF protection
- [ ] Configure CORS properly
- [ ] Set up logging and monitoring

### Database
- [ ] Use strong database password
- [ ] Limit database user permissions
- [ ] Enable SSL connections
- [ ] Regular backups
- [ ] Encrypt sensitive data

### Code
- [ ] Update all dependencies
- [ ] Remove debug mode
- [ ] Validate all inputs
- [ ] Sanitize outputs
- [ ] Remove unused code
- [ ] Review third-party libraries

### Monitoring
- [ ] Set up error logging (Sentry)
- [ ] Monitor access logs
- [ ] Track failed login attempts
- [ ] Alert on suspicious activity
- [ ] Regular security audits

## Secure Deployment Example

```bash
# 1. Set environment variables
export SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
export DATABASE_URL='postgresql://secure_user:strong_password@localhost/occamy_db'
export FLASK_ENV='production'

# 2. Use production config
python app.py

# 3. Run behind nginx with SSL
# Configure nginx with SSL certificate (Let's Encrypt)
sudo certbot --nginx -d yourdomain.com

# 4. Set up firewall
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# 5. Monitor logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

## Security Updates

We regularly review and update security measures. Subscribe to:
- GitHub Security Advisories
- Dependency alerts
- Security mailing list: security-updates@occamy.com

## Third-Party Security

This application uses:
- **Flask**: Web framework - regularly updated
- **SQLAlchemy**: ORM - prevents SQL injection
- **Werkzeug**: WSGI utilities - secure password hashing
- **Flask-Login**: User session management

Keep all dependencies updated:
```bash
pip install --upgrade -r requirements.txt
```

## Incident Response

If a security incident occurs:

1. **Contain**: Isolate affected systems
2. **Assess**: Determine scope and impact
3. **Notify**: Inform affected users (if applicable)
4. **Fix**: Deploy security patches
5. **Review**: Post-mortem and improvements

## Contact

- **Security issues**: security@occamy.com
- **General support**: support@occamy.com
- **GitHub issues**: For non-security bugs only

## Acknowledgments

We appreciate responsible disclosure and will acknowledge security researchers who report vulnerabilities responsibly.

---

**Last Updated**: February 6, 2024
**Version**: 1.0.0
