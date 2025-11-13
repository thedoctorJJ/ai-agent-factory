#!/usr/bin/env python3
"""
Generate OpenAPI specification from FastAPI application.
This script exports the OpenAPI schema for use as a contract between backend and frontend.
"""

import sys
import json
import requests
from pathlib import Path
from typing import Dict, Any

def fetch_openapi_from_api(api_url: str) -> Dict[str, Any]:
    """Fetch OpenAPI spec from live API."""
    try:
        response = requests.get(f"{api_url}/openapi.json", timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Failed to fetch from API: {e}")
        return None

def generate_openapi_spec_from_app():
    """Generate OpenAPI specification from FastAPI app (requires dependencies)."""
    try:
        # Add backend to path
        backend_dir = Path(__file__).parent.parent.parent / "backend"
        sys.path.insert(0, str(backend_dir))
        
        from fastapi_app.main import app
        return app.openapi()
    except ImportError as e:
        print(f"⚠️  Cannot import FastAPI app (missing dependencies): {e}")
        return None

def enhance_openapi_spec(spec: Dict[str, Any]) -> Dict[str, Any]:
    """Enhance OpenAPI spec with additional metadata."""
    if not spec:
        return None
    
    # Enhance the schema with additional metadata
    spec["info"]["contact"] = {
        "name": "AI Agent Factory",
        "url": "https://github.com/thedoctorJJ/ai-agent-factory"
    }
    
    spec["info"]["license"] = {
        "name": "MIT",
        "identifier": "MIT"
    }
    
    # Add servers if not present
    if "servers" not in spec:
        spec["servers"] = []
    
    # Ensure production server is listed
    production_server = {
        "url": "https://ai-agent-factory-backend-952475323593.us-central1.run.app",
        "description": "Production server"
    }
    
    development_server = {
        "url": "http://localhost:8000",
        "description": "Local development server"
    }
    
    # Add servers if not already present
    server_urls = [s.get("url") for s in spec["servers"]]
    if production_server["url"] not in server_urls:
        spec["servers"].insert(0, production_server)
    if development_server["url"] not in server_urls:
        spec["servers"].append(development_server)
    
    # Add security schemes if needed
    if "components" not in spec:
        spec["components"] = {}
    
    if "securitySchemes" not in spec["components"]:
        spec["components"]["securitySchemes"] = {}
    
    return spec

def generate_openapi_spec():
    """Generate OpenAPI specification from FastAPI app."""
    
    # Try to fetch from production API first
    print("🔍 Attempting to fetch OpenAPI spec from production API...")
    spec = fetch_openapi_from_api("https://ai-agent-factory-backend-952475323593.us-central1.run.app")
    
    if spec:
        print("✅ Fetched from production API")
        return enhance_openapi_spec(spec)
    
    # Fallback: Try to generate from app (requires dependencies)
    print("🔍 Attempting to generate from FastAPI app...")
    spec = generate_openapi_spec_from_app()
    
    if spec:
        print("✅ Generated from FastAPI app")
        return enhance_openapi_spec(spec)
    
    print("❌ Could not generate OpenAPI spec")
    return None

def save_openapi_spec(output_path: Path, format: str = "json"):
    """Save OpenAPI specification to file."""
    
    spec = generate_openapi_spec()
    
    if format == "json":
        with open(output_path, 'w') as f:
            json.dump(spec, f, indent=2)
        print(f"✅ OpenAPI JSON specification saved to: {output_path}")
    elif format == "yaml":
        try:
            import yaml
            with open(output_path, 'w') as f:
                yaml.dump(spec, f, default_flow_style=False, sort_keys=False)
            print(f"✅ OpenAPI YAML specification saved to: {output_path}")
        except ImportError:
            print("❌ PyYAML not installed. Install with: pip install pyyaml")
            print(f"   Saving as JSON instead: {output_path.with_suffix('.json')}")
            save_openapi_spec(output_path.with_suffix('.json'), "json")
    else:
        raise ValueError(f"Unsupported format: {format}")

def main():
    """Main function."""
    project_root = Path(__file__).parent.parent.parent
    
    # Create API spec directory
    spec_dir = project_root / "api-spec"
    spec_dir.mkdir(exist_ok=True)
    
    # Generate and save OpenAPI spec
    json_path = spec_dir / "openapi.json"
    yaml_path = spec_dir / "openapi.yaml"
    
    print("🚀 Generating OpenAPI specification...")
    print("=" * 50)
    print()
    
    spec = generate_openapi_spec()
    
    if not spec:
        print("❌ Failed to generate OpenAPI specification")
        sys.exit(1)
    
    save_openapi_spec(json_path, "json")
    save_openapi_spec(yaml_path, "yaml")
    
    print()
    print("📊 Specification Summary:")
    print(f"   - Paths: {len(spec.get('paths', {}))}")
    print(f"   - Schemas: {len(spec.get('components', {}).get('schemas', {}))}")
    print(f"   - Version: {spec.get('info', {}).get('version', 'N/A')}")
    print()
    print("📝 Next steps:")
    print("   1. Review the spec at: api-spec/openapi.json")
    print("   2. Generate TypeScript types: npm run generate:types")
    print("   3. Validate API against spec: npm run validate:api")

if __name__ == "__main__":
    main()

