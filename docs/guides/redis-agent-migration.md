# Redis Agent Migration Guide: Fly.io to Google Cloud Run

## 📋 Overview

This guide walks you through migrating the Redis Caching Layer Agent from Fly.io to Google Cloud Run, leveraging the existing Google Cloud infrastructure and Redis Memorystore instance.

## 🎯 Migration Goals

- **Platform Consistency**: Move all agents to Google Cloud Run for unified management
- **Cost Optimization**: Leverage existing Google Cloud resources and billing
- **Performance**: Utilize Google Cloud's global infrastructure
- **Integration**: Better integration with the AI Agent Factory platform

## 🏗️ Architecture Changes

### Before (Fly.io)
```
Redis Agent (Fly.io) → Upstash Redis → External Service
```

### After (Google Cloud Run)
```
Redis Agent (Cloud Run) → Google Memorystore Redis → AI Agent Factory Platform
```

## 📦 Prerequisites

- Google Cloud CLI installed and authenticated
- Access to the `agent-factory-474201` project
- Existing Redis Memorystore instance (10.1.93.195:6379)
- AI Agent Factory platform running

## 🚀 Migration Steps

### Step 1: Deploy Redis Agent to Google Cloud Run

```bash
# Navigate to the project root
cd /Users/jason/Repositories/ai-agent-factory

# Run the deployment script
./scripts/deploy-redis-agent-to-gcp.sh
```

This script will:
- Build the Docker image
- Push to Google Container Registry
- Deploy to Cloud Run
- Test all endpoints
- Provide the new service URL

### Step 2: Update Agent Registration

```bash
# Update the agent registration in the platform
python scripts/update-redis-agent-registration.py <new-service-url>
```

Example:
```bash
python scripts/update-redis-agent-registration.py https://redis-caching-agent-952475323593.us-central1.run.app
```

### Step 3: Verify Migration

1. **Check AI Agent Factory Dashboard**
   - Navigate to the Agents tab
   - Verify the Redis agent shows the new Google Cloud Run URL
   - Confirm health status is "healthy"

2. **Test All Endpoints**
   - Health check: `GET /health`
   - Cache operations: `POST /cache`, `GET /cache/{key}`
   - Cache management: `DELETE /cache/{key}`, `POST /cache/invalidate`
   - Statistics: `GET /cache/stats`
   - Metrics: `GET /metrics`

3. **Performance Testing**
   - Test response times (should be < 50ms)
   - Verify Redis connectivity
   - Check auto-scaling behavior

## 🔧 Technical Details

### Redis Agent Features

The migrated Redis agent includes:

- **High Performance**: Sub-50ms response times
- **Connection Pooling**: Efficient Redis connection management
- **Health Monitoring**: Comprehensive health checks
- **Metrics**: Prometheus-style metrics endpoint
- **Auto-scaling**: 1-10 instances based on demand
- **Error Handling**: Robust error handling and logging

### Environment Configuration

```yaml
REDIS_HOST: 10.1.93.195
REDIS_PORT: 6379
REDIS_URL: redis://10.1.93.195:6379
ENVIRONMENT: production
PORT: 8080
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root endpoint with service info |
| `/health` | GET | Health check with Redis status |
| `/cache` | POST | Set cache value with TTL |
| `/cache/{key}` | GET | Get cache value |
| `/cache/{key}` | DELETE | Delete cache value |
| `/cache/invalidate` | POST | Invalidate keys by pattern |
| `/cache/stats` | GET | Comprehensive cache statistics |
| `/metrics` | GET | Prometheus-style metrics |

## 📊 Performance Comparison

| Metric | Fly.io | Google Cloud Run |
|--------|--------|------------------|
| Response Time | 24-47ms | < 50ms |
| Auto-scaling | 0-10 instances | 1-10 instances |
| Memory | 1GB | 2GB |
| CPU | 1 vCPU | 2 vCPU |
| Redis Backend | Upstash | Google Memorystore |
| Platform Integration | External | Native |

## 🔍 Monitoring and Observability

### Health Checks
- **Endpoint**: `/health`
- **Checks**: Redis connectivity, service status
- **Response**: JSON with detailed status

### Metrics
- **Endpoint**: `/metrics`
- **Data**: Operation counts, response times, error rates
- **Format**: JSON (Prometheus-compatible)

### Logging
- **Platform**: Google Cloud Logging
- **Level**: INFO with error details
- **Access**: Google Cloud Console

## 🛠️ Troubleshooting

### Common Issues

1. **Redis Connection Failed**
   ```bash
   # Check Redis instance status
   gcloud redis instances describe ai-agent-factory-redis --region=us-central1
   ```

2. **Service Not Responding**
   ```bash
   # Check Cloud Run service status
   gcloud run services describe redis-caching-agent --region=us-central1
   ```

3. **High Response Times**
   - Check Redis instance performance
   - Verify network connectivity
   - Monitor Cloud Run metrics

### Debug Commands

```bash
# Check service logs
gcloud run services logs read redis-caching-agent --region=us-central1

# Test Redis connectivity
gcloud redis instances describe ai-agent-factory-redis --region=us-central1

# Check service configuration
gcloud run services describe redis-caching-agent --region=us-central1 --format=yaml
```

## 🔄 Rollback Plan

If issues arise, you can rollback by:

1. **Revert Agent Registration**
   ```bash
   # Update back to Fly.io URL
   python scripts/update-redis-agent-registration.py https://redis-caching-layer-upstash.fly.dev/
   ```

2. **Keep Fly.io Service Running**
   - Don't decommission Fly.io until migration is confirmed
   - Monitor both services during transition

3. **Gradual Migration**
   - Test thoroughly before full cutover
   - Use feature flags if available

## 📈 Benefits of Migration

### Technical Benefits
- **Unified Platform**: All services on Google Cloud
- **Better Integration**: Native integration with AI Agent Factory
- **Improved Monitoring**: Google Cloud monitoring and logging
- **Enhanced Security**: Google Cloud security features

### Operational Benefits
- **Simplified Management**: Single platform for all services
- **Cost Optimization**: Consolidated billing and resource usage
- **Better Support**: Google Cloud support and documentation
- **Scalability**: Google Cloud's global infrastructure

## 🎉 Success Criteria

Migration is successful when:

- ✅ Redis agent deployed to Google Cloud Run
- ✅ All API endpoints responding correctly
- ✅ Response times < 50ms
- ✅ Agent registered in AI Agent Factory platform
- ✅ Health checks passing
- ✅ Cache operations working correctly
- ✅ Metrics and monitoring functional

## 📞 Support

For issues or questions:

1. Check the troubleshooting section above
2. Review Google Cloud Run documentation
3. Check AI Agent Factory platform logs
4. Contact the development team

---

**Migration completed successfully!** 🚀

The Redis Caching Layer Agent is now running on Google Cloud Run with improved performance, better integration, and unified platform management.
