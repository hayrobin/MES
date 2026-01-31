# Setup Guide

This guide provides detailed instructions for installing, configuring, and deploying the Factory MES system.

## System Requirements

### Hardware Requirements
- CPU: 2+ cores recommended
- RAM: 4GB minimum, 8GB+ recommended for production
- Storage: 10GB+ for application and data

### Software Requirements
- Python 3.10 or higher
- Docker and Docker Compose (for containerized deployment)
- PostgreSQL 12+ (for production deployment)

## Installation Methods

### Method 1: Local Development Setup

#### Step 1: Clone Repository
```bash
git clone https://github.com/hayrobin/MES.git
cd MES
```

#### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Configure Database
For development, SQLite is used by default. No additional setup required.

For production with PostgreSQL:
1. Install PostgreSQL
2. Create database:
```sql
CREATE DATABASE mes_db;
CREATE USER mes_user WITH PASSWORD 'mes_password';
GRANT ALL PRIVILEGES ON DATABASE mes_db TO mes_user;
```

3. Update configuration in `.env` file:
```bash
MES_DATABASE__TYPE=postgresql
MES_DATABASE__HOST=localhost
MES_DATABASE__PORT=5432
MES_DATABASE__DATABASE=mes_db
MES_DATABASE__USERNAME=mes_user
MES_DATABASE__PASSWORD=mes_password
```

#### Step 5: Configure Protocols

Edit configuration files in `config/` directory:

**OPC UA Server** (`config/opcua_server.yaml`):
- Define data points to expose
- Set endpoint URL and security settings
- Configure initial values

**OPC UA Clients** (`config/opcua_clients.yaml`):
- Add client connections to PLCs/SCADA
- Configure subscriptions
- Set reconnection parameters

**Modbus Devices** (`config/modbus_devices.yaml`):
- Add Modbus TCP devices
- Map registers to data points
- Configure polling intervals

#### Step 6: Run Application
```bash
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

The application will start on http://localhost:8000

### Method 2: Docker Deployment

#### Step 1: Clone Repository
```bash
git clone https://github.com/hayrobin/MES.git
cd MES
```

#### Step 2: Configure Environment
Edit `config/` files as needed for your environment.

#### Step 3: Build and Run
```bash
cd docker
docker-compose up -d
```

This will start:
- MES application on port 8000
- PostgreSQL database on port 5432
- pgAdmin on port 5050 (optional)

#### Step 4: Check Status
```bash
docker-compose ps
docker-compose logs -f mes
```

#### Step 5: Access Services
- MES API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- pgAdmin: http://localhost:5050 (admin@factory.com / admin)

### Method 3: Production Deployment

#### Prerequisites
- Linux server (Ubuntu 20.04+ or similar)
- Nginx (reverse proxy)
- Systemd (process management)
- PostgreSQL

#### Step 1: System User
```bash
sudo useradd -m -s /bin/bash mes
sudo su - mes
```

#### Step 2: Install Application
```bash
cd /home/mes
git clone https://github.com/hayrobin/MES.git
cd MES
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Step 3: Configure Application
```bash
cp config/mes_config.yaml .env
# Edit .env with production settings
```

#### Step 4: Create Systemd Service
Create `/etc/systemd/system/mes.service`:
```ini
[Unit]
Description=Factory MES System
After=network.target postgresql.service

[Service]
Type=simple
User=mes
WorkingDirectory=/home/mes/MES
Environment="PATH=/home/mes/MES/venv/bin"
ExecStart=/home/mes/MES/venv/bin/uvicorn src.api.main:app --host 127.0.0.1 --port 8000 --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable mes
sudo systemctl start mes
sudo systemctl status mes
```

#### Step 5: Configure Nginx
Create `/etc/nginx/sites-available/mes`:
```nginx
server {
    listen 80;
    server_name mes.factory.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /ws {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/mes /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Configuration Details

### Environment Variables

All settings can be configured via environment variables with `MES_` prefix:

```bash
# Application
MES_APP_NAME="Factory MES"
MES_DEBUG=false

# Logging
MES_LOG_LEVEL=INFO
MES_JSON_LOGGING=true

# Database
MES_DATABASE__TYPE=postgresql
MES_DATABASE__HOST=localhost
MES_DATABASE__PORT=5432
MES_DATABASE__DATABASE=mes_db
MES_DATABASE__USERNAME=mes_user
MES_DATABASE__PASSWORD=mes_password

# API
MES_API__HOST=0.0.0.0
MES_API__PORT=8000
MES_API__WORKERS=4
```

### OPC UA Configuration

**Server Configuration** (`opcua_server.yaml`):
```yaml
endpoint: "opc.tcp://0.0.0.0:4840/freeopcua/server/"
server_name: "Factory MES OPC UA Server"
namespace: "http://factory.mes"
security_enabled: false
nodes:
  - node_id: "Temperature1"
    browse_name: "Temperature1"
    display_name: "Zone 1 Temperature"
    data_type: "float"
    initial_value: 25.0
    writable: false
```

**Client Configuration** (`opcua_clients.yaml`):
```yaml
clients:
  - name: "PLC1"
    endpoint: "opc.tcp://192.168.1.100:4840"
    namespace_index: 2
    reconnect_interval: 5
    timeout: 10
    subscriptions:
      - node_id: "ns=2;s=Temperature"
        publishing_interval: 1000
```

### Modbus Configuration

```yaml
devices:
  - name: "TempSensor1"
    host: "192.168.1.50"
    port: 502
    unit_id: 1
    polling_interval: 2
    timeout: 5
    registers:
      - name: "Temperature"
        register_type: "input_register"
        address: 0
        count: 2
        data_type: "float32"
        scale: 1.0
        offset: 0.0
        unit: "°C"
```

## Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connection
psql -h localhost -U mes_user -d mes_db

# View logs
sudo journalctl -u postgresql
```

### OPC UA Connection Issues
- Verify endpoint URL is correct
- Check firewall rules (port 4840)
- Verify server is running
- Check security settings match

### Modbus Connection Issues
- Verify IP address and port
- Check network connectivity: `ping 192.168.1.50`
- Verify Modbus device is responding
- Check unit ID matches device configuration

### Application Logs
```bash
# Docker deployment
docker-compose logs -f mes

# Systemd deployment
sudo journalctl -u mes -f

# Check application health
curl http://localhost:8000/api/status/health
```

## Security Considerations

### Production Checklist
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable OPC UA security (certificates)
- [ ] Use strong database passwords
- [ ] Configure firewall rules
- [ ] Enable HTTPS with SSL certificate
- [ ] Implement authentication for API
- [ ] Regular database backups
- [ ] Keep dependencies updated
- [ ] Monitor system logs
- [ ] Implement rate limiting

### Firewall Configuration
```bash
# Allow API port
sudo ufw allow 8000/tcp

# Allow OPC UA server port
sudo ufw allow 4840/tcp

# Allow PostgreSQL (if remote access needed)
sudo ufw allow from 192.168.1.0/24 to any port 5432
```

## Backup and Recovery

### Database Backup
```bash
# PostgreSQL backup
pg_dump -h localhost -U mes_user mes_db > mes_backup.sql

# Restore
psql -h localhost -U mes_user mes_db < mes_backup.sql
```

### Configuration Backup
```bash
# Backup configuration files
tar -czf mes_config_backup.tar.gz config/
```

## Monitoring

### Health Check Endpoint
```bash
curl http://localhost:8000/api/status/health
```

### System Status
```bash
curl http://localhost:8000/api/status
```

### Database Size
```sql
SELECT pg_size_pretty(pg_database_size('mes_db'));
```

## Upgrading

### Application Upgrade
```bash
cd /home/mes/MES
git pull
source venv/bin/activate
pip install -r requirements.txt --upgrade
sudo systemctl restart mes
```

### Database Migration
Future versions will include Alembic migrations. For now, database schema is automatically created on startup.

## Performance Tuning

### Database Optimization
```sql
-- Create indexes for better query performance
CREATE INDEX CONCURRENTLY idx_historical_timestamp 
ON historical_data (timestamp DESC);

-- Analyze tables
ANALYZE historical_data;
```

### Application Settings
- Increase workers for high load: `MES_API__WORKERS=8`
- Adjust database pool size: `MES_DATABASE__POOL_SIZE=20`
- Optimize polling intervals in Modbus configuration
- Use batch operations where possible

## Next Steps

After installation:
1. Review [API Documentation](API.md)
2. Configure your devices in `config/` files
3. Test connections using API endpoints
4. Set up monitoring and alerting
5. Configure data retention policies
6. Implement backup procedures
