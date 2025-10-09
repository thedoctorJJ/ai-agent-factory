#!/usr/bin/env python3
"""
Test script for Devin AI integration
"""

import requests
import json

# Test the Devin AI integration endpoints
BASE_URL = "http://localhost:8000/api/v1"

def test_devin_integration():
    print("🤖 Testing Devin AI Integration")
    print("=" * 50)
    
    # Test data
    test_task = {
        "prd_id": "test-prd-123",
        "title": "Email Marketing Agent",
        "description": "An AI agent that creates and sends personalized email marketing campaigns",
        "requirements": [
            "Connect to email service providers (SendGrid, Mailchimp)",
            "Generate personalized email content based on user data",
            "Schedule and send campaigns automatically",
            "Track open rates and click-through rates",
            "A/B test different email variations",
            "Integrate with CRM systems"
        ]
    }
    
    try:
        # Test creating a Devin task
        print("1. Creating Devin AI task...")
        response = requests.post(f"{BASE_URL}/devin/tasks", json=test_task)
        
        if response.status_code == 200:
            task = response.json()
            print(f"✅ Task created: {task['id']}")
            print(f"   Title: {task['title']}")
            print(f"   Status: {task['status']}")
            
            # Test getting the Devin prompt
            print("\n2. Getting Devin AI prompt...")
            prompt_response = requests.get(f"{BASE_URL}/devin/tasks/{task['id']}/prompt")
            
            if prompt_response.status_code == 200:
                prompt_data = prompt_response.json()
                print("✅ Prompt generated successfully")
                print(f"   Prompt length: {len(prompt_data['prompt'])} characters")
                print("\n📋 Sample prompt (first 200 chars):")
                print(prompt_data['prompt'][:200] + "...")
                
                # Test getting all tasks
                print("\n3. Getting all Devin tasks...")
                tasks_response = requests.get(f"{BASE_URL}/devin/tasks")
                
                if tasks_response.status_code == 200:
                    tasks = tasks_response.json()
                    print(f"✅ Found {len(tasks)} tasks")
                    
                    # Test completing a task
                    print("\n4. Testing task completion...")
                    mock_agent_code = """
# Email Marketing Agent
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailMarketingAgent:
    def __init__(self, api_key):
        self.api_key = api_key
    
    def create_campaign(self, subject, content, recipients):
        # Implementation here
        pass
    
    def send_campaign(self, campaign_id):
        # Implementation here
        pass
"""
                    
                    complete_response = requests.put(
                        f"{BASE_URL}/devin/tasks/{task['id']}/complete",
                        json={"agent_code": mock_agent_code}
                    )
                    
                    if complete_response.status_code == 200:
                        completed_task = complete_response.json()
                        print("✅ Task completed successfully")
                        print(f"   Status: {completed_task['status']}")
                        print(f"   Code length: {len(completed_task['agent_code'])} characters")
                    else:
                        print(f"❌ Failed to complete task: {complete_response.status_code}")
                else:
                    print(f"❌ Failed to get tasks: {tasks_response.status_code}")
            else:
                print(f"❌ Failed to get prompt: {prompt_response.status_code}")
        else:
            print(f"❌ Failed to create task: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Make sure the FastAPI server is running")
        print("   Run: cd backend && uvicorn fastapi_app.main:app --reload")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_devin_integration()
