#!/usr/bin/env python3
"""
Redis Caching Layer Agent - Google Cloud Run Version
A high-performance caching service built for Google Cloud Run with Memorystore Redis
"""

import os
import json
import time
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import logging

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import redis.asyncio as redis
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="Redis Caching Layer Agent",
    description="High-performance caching service for Google Cloud Run",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis connection
redis_client: Optional[redis.Redis] = None

# In-memory cache fallback for testing
in_memory_cache: Dict[str, Any] = {}
cache_ttl: Dict[str, float] = {}

# Pydantic models
class CacheItem(BaseModel):
    key: str = Field(..., description="Cache key")
    value: Any = Field(..., description="Cache value")
    ttl: Optional[int] = Field(None, description="Time to live in seconds")

class CacheSetRequest(BaseModel):
    key: str = Field(..., description="Cache key")
    value: Any = Field(..., description="Cache value")
    ttl: Optional[int] = Field(None, description="Time to live in seconds")

class CacheInvalidateRequest(BaseModel):
    pattern: str = Field(..., description="Pattern to match keys for invalidation")

class CacheStats(BaseModel):
    total_keys: int
    memory_usage: str
    connected_clients: int
    uptime_seconds: int
    total_commands_processed: int
    keyspace_hits: int
    keyspace_misses: int
    hit_rate: float

# Health check model
class HealthResponse(BaseModel):
    status: str
    timestamp: str
    redis_connected: bool
    version: str
    uptime_seconds: int

# Metrics model
class MetricsResponse(BaseModel):
    cache_operations: Dict[str, int]
    response_times: Dict[str, float]
    error_count: int
    uptime_seconds: int

# Global variables for metrics
start_time = time.time()
operation_counts = {
    "set": 0,
    "get": 0,
    "delete": 0,
    "invalidate": 0,
    "stats": 0
}
response_times = {
    "set": 0.0,
    "get": 0.0,
    "delete": 0.0,
    "invalidate": 0.0,
    "stats": 0.0
}
error_count = 0

def is_cache_expired(key: str) -> bool:
    """Check if a cache key has expired"""
    if key not in cache_ttl:
        return False
    return time.time() > cache_ttl[key]

def set_in_memory_cache(key: str, value: Any, ttl: Optional[int] = None):
    """Set value in in-memory cache"""
    in_memory_cache[key] = value
    if ttl:
        cache_ttl[key] = time.time() + ttl
    else:
        cache_ttl[key] = float('inf')

def get_in_memory_cache(key: str) -> Optional[Any]:
    """Get value from in-memory cache"""
    if key in in_memory_cache and not is_cache_expired(key):
        return in_memory_cache[key]
    return None

def delete_in_memory_cache(key: str) -> bool:
    """Delete value from in-memory cache"""
    if key in in_memory_cache:
        del in_memory_cache[key]
        if key in cache_ttl:
            del cache_ttl[key]
        return True
    return False

def invalidate_in_memory_cache(pattern: str) -> int:
    """Invalidate keys matching pattern in in-memory cache"""
    import re
    count = 0
    keys_to_delete = []
    
    for key in in_memory_cache.keys():
        if re.match(pattern.replace('*', '.*'), key):
            keys_to_delete.append(key)
    
    for key in keys_to_delete:
        delete_in_memory_cache(key)
        count += 1
    
    return count

async def get_redis_client() -> redis.Redis:
    """Get Redis client with connection pooling"""
    global redis_client
    
    if redis_client is None:
        # Get Redis configuration from environment
        redis_host = os.getenv("REDIS_HOST", "10.1.93.195")
        redis_port = int(os.getenv("REDIS_PORT", "6379"))
        redis_url = os.getenv("REDIS_URL", f"redis://{redis_host}:{redis_port}")
        
        # Try to connect to Redis - VPC connector should now be available
        logger.info(f"Attempting to connect to Redis at {redis_host}:{redis_port}")
        
        try:
            # Create Redis connection with connection pooling
            redis_client = redis.from_url(
                redis_url,
                encoding="utf-8",
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True,
                health_check_interval=30
            )
            
            # Test connection
            await redis_client.ping()
            logger.info(f"✅ Connected to Redis at {redis_host}:{redis_port}")
            
        except Exception as e:
            logger.error(f"❌ Failed to connect to Redis: {e}")
            raise HTTPException(status_code=503, detail="Redis connection failed")
    
    return redis_client

@app.on_event("startup")
async def startup_event():
    """Initialize Redis connection on startup"""
    try:
        await get_redis_client()
        logger.info("🚀 Redis Caching Agent started successfully")
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Close Redis connection on shutdown"""
    global redis_client
    if redis_client:
        await redis_client.close()
        logger.info("🔌 Redis connection closed")

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint"""
    return {
        "message": "Redis Caching Layer Agent - Google Cloud Run",
        "version": "2.0.0",
        "status": "operational",
        "docs": "/docs"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        redis_client = await get_redis_client()
        await redis_client.ping()
        redis_connected = True
    except Exception:
        redis_connected = False
    
    uptime = int(time.time() - start_time)
    
    return HealthResponse(
        status="healthy" if redis_connected else "unhealthy",
        timestamp=datetime.utcnow().isoformat(),
        redis_connected=redis_connected,
        version="2.0.0",
        uptime_seconds=uptime
    )

@app.post("/cache", response_model=Dict[str, Any])
async def set_cache(request: CacheSetRequest):
    """Set a cache value with optional TTL"""
    start_time_op = time.time()
    global operation_counts, response_times, error_count
    
    try:
        redis_client = await get_redis_client()
        
        if redis_client is None:
            # Use in-memory cache
            set_in_memory_cache(request.key, request.value, request.ttl)
            operation_counts["set"] += 1
            response_times["set"] = (time.time() - start_time_op) * 1000
            
            return {
                "success": True,
                "key": request.key,
                "message": f"Value cached in memory with TTL: {request.ttl or 'no expiration'}"
            }
        
        # Serialize value to JSON
        value_str = json.dumps(request.value)
        
        # Set with TTL if provided
        if request.ttl:
            await redis_client.setex(request.key, request.ttl, value_str)
        else:
            await redis_client.set(request.key, value_str)
        
        operation_counts["set"] += 1
        response_times["set"] = (time.time() - start_time_op) * 1000
        
        return {
            "success": True,
            "key": request.key,
            "message": f"Value cached successfully with TTL: {request.ttl or 'no expiration'}"
        }
        
    except Exception as e:
        error_count += 1
        logger.error(f"Error setting cache: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to set cache: {str(e)}")

@app.get("/cache/stats", response_model=CacheStats)
async def get_cache_stats():
    """Get comprehensive cache statistics"""
    start_time_op = time.time()
    global operation_counts, response_times, error_count
    
    try:
        redis_client = await get_redis_client()
        
        if redis_client is None:
            # Use in-memory cache stats
            total_keys = len(in_memory_cache)
            memory_usage = f"{len(str(in_memory_cache))} bytes"
            uptime_seconds = int(time.time() - start_time)
            
            operation_counts["stats"] += 1
            response_times["stats"] = (time.time() - start_time_op) * 1000
            
            return CacheStats(
                total_keys=total_keys,
                memory_usage=memory_usage,
                connected_clients=1,
                uptime_seconds=uptime_seconds,
                total_commands_processed=sum(operation_counts.values()),
                keyspace_hits=operation_counts.get("get", 0),
                keyspace_misses=0,
                hit_rate=100.0 if operation_counts.get("get", 0) > 0 else 0.0
            )
        
        # Get Redis info
        info = await redis_client.info()
        
        # Calculate hit rate
        hits = int(info.get('keyspace_hits', 0))
        misses = int(info.get('keyspace_misses', 0))
        total_requests = hits + misses
        hit_rate = (hits / total_requests * 100) if total_requests > 0 else 0
        
        operation_counts["stats"] += 1
        response_times["stats"] = (time.time() - start_time_op) * 1000
        
        return CacheStats(
            total_keys=info.get('db0', {}).get('keys', 0) if 'db0' in info else 0,
            memory_usage=info.get('used_memory_human', '0B'),
            connected_clients=info.get('connected_clients', 0),
            uptime_seconds=info.get('uptime_in_seconds', 0),
            total_commands_processed=info.get('total_commands_processed', 0),
            keyspace_hits=hits,
            keyspace_misses=misses,
            hit_rate=round(hit_rate, 2)
        )
        
    except Exception as e:
        error_count += 1
        logger.error(f"Error getting cache stats: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get cache stats: {str(e)}")

@app.get("/cache/{key}", response_model=Dict[str, Any])
async def get_cache(key: str):
    """Get a cache value"""
    start_time_op = time.time()
    global operation_counts, response_times, error_count
    
    try:
        redis_client = await get_redis_client()
        
        if redis_client is None:
            # Use in-memory cache
            value = get_in_memory_cache(key)
            
            if value is None:
                operation_counts["get"] += 1
                response_times["get"] = (time.time() - start_time_op) * 1000
                raise HTTPException(status_code=404, detail="Key not found")
            
            operation_counts["get"] += 1
            response_times["get"] = (time.time() - start_time_op) * 1000
            
            return {
                "success": True,
                "key": key,
                "value": value
            }
        
        value_str = await redis_client.get(key)
        
        if value_str is None:
            operation_counts["get"] += 1
            response_times["get"] = (time.time() - start_time_op) * 1000
            raise HTTPException(status_code=404, detail="Key not found")
        
        # Deserialize from JSON
        value = json.loads(value_str)
        
        operation_counts["get"] += 1
        response_times["get"] = (time.time() - start_time_op) * 1000
        
        return {
            "success": True,
            "key": key,
            "value": value
        }
        
    except HTTPException:
        raise
    except Exception as e:
        error_count += 1
        logger.error(f"Error getting cache: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get cache: {str(e)}")

@app.delete("/cache/{key}", response_model=Dict[str, Any])
async def delete_cache(key: str):
    """Delete a cache value"""
    start_time_op = time.time()
    global operation_counts, response_times, error_count
    
    try:
        redis_client = await get_redis_client()
        
        if redis_client is None:
            # Use in-memory cache
            result = delete_in_memory_cache(key)
            
            operation_counts["delete"] += 1
            response_times["delete"] = (time.time() - start_time_op) * 1000
            
            if not result:
                raise HTTPException(status_code=404, detail="Key not found")
            
            return {
                "success": True,
                "key": key,
                "message": "Key deleted successfully from memory"
            }
        
        result = await redis_client.delete(key)
        
        operation_counts["delete"] += 1
        response_times["delete"] = (time.time() - start_time_op) * 1000
        
        if result == 0:
            raise HTTPException(status_code=404, detail="Key not found")
        
        return {
            "success": True,
            "key": key,
            "message": "Key deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        error_count += 1
        logger.error(f"Error deleting cache: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete cache: {str(e)}")

@app.post("/cache/invalidate", response_model=Dict[str, Any])
async def invalidate_cache(request: CacheInvalidateRequest):
    """Invalidate cache keys matching a pattern"""
    start_time_op = time.time()
    global operation_counts, response_times, error_count
    
    try:
        redis_client = await get_redis_client()
        
        if redis_client is None:
            # Use in-memory cache
            deleted_count = invalidate_in_memory_cache(request.pattern)
            
            operation_counts["invalidate"] += 1
            response_times["invalidate"] = (time.time() - start_time_op) * 1000
            
            return {
                "success": True,
                "pattern": request.pattern,
                "keys_deleted": deleted_count,
                "message": f"Invalidated {deleted_count} keys matching pattern in memory"
            }
        
        # Find keys matching pattern
        keys = await redis_client.keys(request.pattern)
        
        if keys:
            deleted_count = await redis_client.delete(*keys)
        else:
            deleted_count = 0
        
        operation_counts["invalidate"] += 1
        response_times["invalidate"] = (time.time() - start_time_op) * 1000
        
        return {
            "success": True,
            "pattern": request.pattern,
            "keys_deleted": deleted_count,
            "message": f"Invalidated {deleted_count} keys matching pattern"
        }
        
    except Exception as e:
        error_count += 1
        logger.error(f"Error invalidating cache: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to invalidate cache: {str(e)}")


@app.get("/metrics", response_model=MetricsResponse)
async def get_metrics():
    """Get Prometheus-style metrics"""
    uptime = int(time.time() - start_time)
    
    return MetricsResponse(
        cache_operations=operation_counts.copy(),
        response_times=response_times.copy(),
        error_count=error_count,
        uptime_seconds=uptime
    )

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time header to responses"""
    start_time_req = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time_req
    response.headers["X-Process-Time"] = str(process_time)
    return response

if __name__ == "__main__":
    # Get port from environment (Google Cloud Run sets PORT)
    port = int(os.getenv("PORT", 8080))
    
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        log_level="info",
        access_log=True
    )
