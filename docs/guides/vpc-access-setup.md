# VPC Access Setup Guide

## 🌉 What is VPC Access?

VPC Access is Google Cloud's solution for connecting Cloud Run services to resources in your Virtual Private Cloud (VPC) network. It creates a secure "bridge" between Cloud Run's managed environment and your private VPC resources like Redis, databases, and other internal services.

## 🔧 Why Do We Need VPC Access?

### **The Problem**
- **Cloud Run Services** = Public internet-facing services
- **Google Cloud Memorystore (Redis)** = Private internal network service
- **Default State**: They can't communicate due to network isolation

### **The Solution**
VPC Access creates a secure connector that allows Cloud Run to access VPC resources without exposing them to the public internet.

## 🚀 Step-by-Step Setup

### **Prerequisites**
- Google Cloud project with billing enabled
- Cloud Run service deployed
- Redis instance in VPC (Google Cloud Memorystore)
- `gcloud` CLI configured with appropriate permissions

### **Step 1: Enable VPC Access API**
```bash
gcloud services enable vpcaccess.googleapis.com --project=YOUR_PROJECT_ID
```

### **Step 2: Create VPC Connector Subnet**
VPC connectors require a subnet with a /28 netmask (16 IP addresses).

```bash
gcloud compute networks subnets create vpc-connector-subnet \
    --region=us-central1 \
    --network=default \
    --range=10.2.0.0/28 \
    --project=YOUR_PROJECT_ID
```

### **Step 3: Create VPC Connector**
```bash
gcloud compute networks vpc-access connectors create redis-connector \
    --region=us-central1 \
    --subnet=vpc-connector-subnet \
    --subnet-project=YOUR_PROJECT_ID \
    --min-instances=2 \
    --max-instances=3
```

### **Step 4: Connect Cloud Run to VPC**
```bash
gcloud run services update YOUR_SERVICE_NAME \
    --vpc-connector=redis-connector \
    --region=us-central1 \
    --project=YOUR_PROJECT_ID
```

## 🔍 Verification

### **Check VPC Connector Status**
```bash
gcloud compute networks vpc-access connectors describe redis-connector \
    --region=us-central1 \
    --project=YOUR_PROJECT_ID
```

Look for `state: READY` in the output.

### **Verify Cloud Run Configuration**
```bash
gcloud run services describe YOUR_SERVICE_NAME \
    --region=us-central1 \
    --project=YOUR_PROJECT_ID \
    --format="value(spec.template.metadata.annotations)"
```

Look for `run.googleapis.com/vpc-access-connector=redis-connector`.

### **Test Redis Connection**
```bash
curl -s "https://YOUR_SERVICE_URL/health" | jq '.redis_connected'
```

Should return `true`.

## 📊 Configuration Details

### **VPC Connector Specifications**
- **Machine Type**: e2-micro (default)
- **Min Instances**: 2 (recommended for availability)
- **Max Instances**: 3 (cost optimization)
- **Min Throughput**: 200 Mbps
- **Max Throughput**: 300 Mbps

### **Network Architecture**
```
┌─────────────────┐    VPC Connector    ┌─────────────────┐
│   Cloud Run     │ ←─────────────────→ │   VPC Network   │
│   (Public)      │                     │   (Private)     │
└─────────────────┘                     └─────────────────┘
                                               │
                                               ▼
                                        ┌─────────────────┐
                                        │   Redis         │
                                        │   (Memorystore) │
                                        └─────────────────┘
```

## 💰 Cost Considerations

### **VPC Connector Costs**
- **Fixed Cost**: ~$0.36/hour per connector
- **Variable Cost**: Based on throughput usage
- **Min Instances**: Always running (2 instances = ~$0.72/hour)

### **Cost Optimization Tips**
1. **Right-size instances**: Use min/max instances appropriately
2. **Monitor usage**: Check Cloud Console for actual throughput
3. **Consider alternatives**: For simple use cases, public Redis might be cheaper

## 🔒 Security Benefits

### **Network Isolation**
- Redis remains private and not accessible from the internet
- Only Cloud Run services with VPC connector can access Redis
- No need to expose Redis with public IPs or firewall rules

### **Encryption**
- All traffic between Cloud Run and VPC is encrypted
- Redis connections can use TLS for additional security
- No data traverses the public internet

## 🚨 Troubleshooting

### **Common Issues**

#### **1. Subnet Netmask Error**
```
ERROR: Subnets used for VPC connectors must have a netmask of 28.
```
**Solution**: Create a dedicated subnet with /28 netmask (16 IP addresses).

#### **2. Connector in ERROR State**
```bash
gcloud compute networks vpc-access connectors list --region=us-central1
```
**Solution**: Delete and recreate the connector with proper subnet.

#### **3. Redis Connection Timeout**
**Check**: VPC connector is in READY state
**Check**: Cloud Run service has VPC connector annotation
**Check**: Redis instance is in the same VPC network

### **Debug Commands**
```bash
# Check connector status
gcloud compute networks vpc-access connectors list --region=us-central1

# Check Cloud Run VPC configuration
gcloud run services describe SERVICE_NAME --region=us-central1 \
    --format="value(spec.template.metadata.annotations)"

# Test Redis connectivity
curl -s "https://SERVICE_URL/health" | jq '.'
```

## 📚 Additional Resources

- [Google Cloud VPC Access Documentation](https://cloud.google.com/vpc/docs/configure-serverless-vpc-access)
- [Cloud Run VPC Integration](https://cloud.google.com/run/docs/configuring/vpc)
- [Memorystore for Redis](https://cloud.google.com/memorystore/docs/redis)

## ✅ Success Checklist

- [ ] VPC Access API enabled
- [ ] VPC connector subnet created (/28 netmask)
- [ ] VPC connector created and in READY state
- [ ] Cloud Run service updated with VPC connector
- [ ] Redis connection verified in health check
- [ ] Cache operations tested and working
- [ ] Performance metrics within expected ranges
