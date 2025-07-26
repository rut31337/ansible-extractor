# Usage Examples

This document provides practical examples of how to use the Ansible Vault Extractor.

## Basic Examples

### 1. Extract and Display Variables
```bash
python extract_vault_values.py --yaml-file secrets.yml --vault-password-file .vault_pass
```

Output:
```
database_host: "localhost"
database_port: 5432
database_name: "myapp"
database_user: "dbuser"
database_password: "secret_password"
api_key: "sk-1234567890abcdef"
api_endpoint: "https://api.example.com"
api_timeout: 30
redis_host: "redis.example.com"
redis_port: 6379
redis_password: "redis_secret"
app_config_debug: false
app_config_log_level: "info"
app_config_features_cache_enabled: true
app_config_features_rate_limiting: true
```

### 2. Export as Environment Variables
```bash
python extract_vault_values.py --yaml-file secrets.yml --vault-password-file .vault_pass --env
```

Output:
```
export DATABASE_HOST="localhost"
export DATABASE_PORT=5432
export DATABASE_NAME="myapp"
export DATABASE_USER="dbuser"
export DATABASE_PASSWORD="secret_password"
export API_KEY="sk-1234567890abcdef"
export API_ENDPOINT="https://api.example.com"
export API_TIMEOUT=30
export REDIS_HOST="redis.example.com"
export REDIS_PORT=6379
export REDIS_PASSWORD="redis_secret"
export APP_CONFIG_DEBUG=false
export APP_CONFIG_LOG_LEVEL="info"
export APP_CONFIG_FEATURES_CACHE_ENABLED=true
export APP_CONFIG_FEATURES_RATE_LIMITING=true
```

### 3. Source Variables into Current Shell
```bash
source <(python extract_vault_values.py --yaml-file secrets.yml --vault-password-file .vault_pass --env)
```

Then use the variables:
```bash
echo $DATABASE_HOST
echo $API_KEY
```

### 4. Debug Mode (View Raw Ansible Output)
```bash
python extract_vault_values.py --yaml-file secrets.yml --vault-password-file .vault_pass --debug
```

## Advanced Examples

### 5. Use in Scripts
```bash
#!/bin/bash
# Load secrets and start application

# Extract database credentials
eval $(python extract_vault_values.py --yaml-file secrets.yml --vault-password-file .vault_pass --env | grep DATABASE)

# Start database connection
echo "Connecting to database: $DATABASE_HOST:$DATABASE_PORT/$DATABASE_NAME"
```

### 6. Docker Integration
```dockerfile
# In your Dockerfile
COPY extract_vault_values.py /usr/local/bin/
RUN chmod +x /usr/local/bin/extract_vault_values.py

# In your entrypoint script
#!/bin/bash
source <(python /usr/local/bin/extract_vault_values.py --yaml-file /secrets/secrets.yml --vault-password-file /secrets/.vault_pass --env)
exec "$@"
```

### 7. CI/CD Pipeline Integration
```yaml
# GitHub Actions example
- name: Load secrets
  run: |
    source <(python extract_vault_values.py --yaml-file secrets.yml --vault-password-file .vault_pass --env)
    echo "API_KEY=$API_KEY" >> $GITHUB_ENV
```

## Troubleshooting

### Common Issues

1. **Permission Denied**
   ```bash
   chmod +x extract_vault_values.py
   ```

2. **Ansible Not Found**
   ```bash
   # Install Ansible
   pip install ansible
   # or
   sudo apt-get install ansible  # Ubuntu/Debian
   ```

3. **Vault Password File Not Found**
   ```bash
   # Create vault password file
   echo "your_vault_password" > .vault_pass
   chmod 600 .vault_pass
   ```

4. **Invalid Vault Password**
   - Verify the password in your vault password file
   - Check if the YAML file is actually encrypted with Ansible vault 