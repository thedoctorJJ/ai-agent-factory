#!/usr/bin/env python3
"""
Test script for comprehensive PRD parsing
Tests the new PRD parser with sample PRD content
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend', 'fastapi_app'))

from services.prd_parser import PRDParser

def test_comprehensive_prd_parsing():
    """Test the comprehensive PRD parser with sample content"""
    
    # Sample PRD content based on the template
    sample_prd_content = """# **Title**

**Customer Support AI Agent**

---

## **Description**

An intelligent AI agent designed to handle customer support inquiries automatically, providing 24/7 assistance and reducing response times.

---

## **Problem Statement**

Our customer support team is overwhelmed with repetitive inquiries, leading to long response times and decreased customer satisfaction. We need an automated solution to handle common questions and escalate complex issues to human agents.

---

## **Target Users**

* **Primary Users**
  - Customer Service Representatives
  - End Customers
* **Secondary Users**
  - Support Managers
  - Product Team

---

## **User Stories**

* As a **customer**, I want to get instant answers to common questions so that I don't have to wait for human support
* As a **support agent**, I want the AI to handle routine inquiries so that I can focus on complex issues
* As a **manager**, I want to track AI performance so that I can optimize the system

---

## **Requirements**

### **Functional Requirements**
1. Handle common customer inquiries automatically
2. Escalate complex issues to human agents
3. Provide multi-language support
4. Integrate with existing CRM system
5. Generate support tickets when needed

### **Non-Functional Requirements**
1. Response time under 2 seconds
2. 99.9% uptime availability
3. Support for 1000+ concurrent users
4. GDPR compliant data handling

---

## **Acceptance Criteria**

* [ ] AI responds to 80% of common inquiries correctly
* [ ] Response time is consistently under 2 seconds
* [ ] Integration with CRM system works seamlessly
* [ ] Multi-language support for English, Spanish, and French
* [ ] Escalation to human agents works within 30 seconds

---

## **Technical Requirements**

* **Backend:** FastAPI with Python 3.9+
* **AI/ML:** OpenAI GPT-4 or similar LLM
* **Database:** PostgreSQL for conversation history
* **Infrastructure:** Docker containers on AWS
* **Security:** End-to-end encryption for customer data
* **Integration:** REST API for CRM integration

---

## **Performance Requirements**

* **Response Time:** Under 2 seconds for 95% of requests
* **Throughput:** Handle 1000+ concurrent conversations
* **Availability:** 99.9% uptime
* **Scalability:** Auto-scale based on demand

---

## **Security Requirements**

* End-to-end encryption for all customer communications
* GDPR compliant data processing and storage
* Regular security audits and penetration testing
* Secure API authentication and authorization

---

## **Success Metrics**

* 80% reduction in support ticket volume
* 90% customer satisfaction score
* 50% reduction in average response time
* 95% AI accuracy rate

---

## **Timeline**

* **Start Date:** 2024-02-01
* **Target Completion:** 2024-04-30
* **Key Milestones:**
  - Week 2: AI model training and testing
  - Week 6: CRM integration development
  - Week 10: Multi-language support implementation
  - Week 12: Production deployment and testing

---

## **Dependencies**

* OpenAI API access and credits
* CRM system API documentation
* Customer support team training
* Legal review for GDPR compliance

---

## **Risks**

* AI model accuracy may not meet expectations
* Integration with legacy CRM system could be complex
* Customer adoption may be slower than anticipated
* Regulatory compliance requirements may change

---

## **Assumptions**

* Customers will be willing to interact with AI agents
* Existing CRM system has stable APIs
* Support team will provide adequate training data
* Legal requirements remain stable during development
"""

    print("🧪 Testing Comprehensive PRD Parsing")
    print("=" * 50)
    
    # Initialize parser
    parser = PRDParser()
    
    # Parse the sample PRD
    print("📝 Parsing sample PRD content...")
    parsed_data = parser.parse_prd_content(sample_prd_content, "customer-support-agent.md")
    
    # Display results
    print("\n✅ Parsing Results:")
    print("-" * 30)
    
    # Core fields
    print(f"Title: {parsed_data['title']}")
    print(f"PRD Type: {parsed_data['prd_type']}")
    print(f"Description: {parsed_data['description'][:100]}...")
    print(f"Problem Statement: {parsed_data['problem_statement'][:100]}...")
    
    # Lists
    print(f"\nTarget Users ({len(parsed_data['target_users'])}):")
    for user in parsed_data['target_users'][:3]:
        print(f"  • {user}")
    
    print(f"\nUser Stories ({len(parsed_data['user_stories'])}):")
    for story in parsed_data['user_stories'][:2]:
        print(f"  • {story[:80]}...")
    
    print(f"\nFunctional Requirements ({len(parsed_data['functional_requirements'])}):")
    for req in parsed_data['functional_requirements'][:3]:
        print(f"  • {req}")
    
    print(f"\nNon-Functional Requirements ({len(parsed_data['non_functional_requirements'])}):")
    for req in parsed_data['non_functional_requirements'][:3]:
        print(f"  • {req}")
    
    print(f"\nAcceptance Criteria ({len(parsed_data['acceptance_criteria'])}):")
    for criteria in parsed_data['acceptance_criteria'][:3]:
        print(f"  • {criteria}")
    
    print(f"\nTechnical Requirements ({len(parsed_data['technical_requirements'])}):")
    for req in parsed_data['technical_requirements'][:3]:
        print(f"  • {req}")
    
    print(f"\nPerformance Requirements:")
    for key, value in parsed_data['performance_requirements'].items():
        print(f"  • {key}: {value}")
    
    print(f"\nSecurity Requirements ({len(parsed_data['security_requirements'])}):")
    for req in parsed_data['security_requirements'][:3]:
        print(f"  • {req}")
    
    print(f"\nSuccess Metrics ({len(parsed_data['success_metrics'])}):")
    for metric in parsed_data['success_metrics'][:3]:
        print(f"  • {metric}")
    
    print(f"\nTimeline: {parsed_data['timeline'][:100]}...")
    print(f"Start Date: {parsed_data['start_date']}")
    print(f"Target Completion: {parsed_data['target_completion_date']}")
    print(f"Key Milestones ({len(parsed_data['key_milestones'])}):")
    for milestone in parsed_data['key_milestones'][:3]:
        print(f"  • {milestone}")
    
    print(f"\nDependencies ({len(parsed_data['dependencies'])}):")
    for dep in parsed_data['dependencies'][:3]:
        print(f"  • {dep}")
    
    print(f"\nRisks ({len(parsed_data['risks'])}):")
    for risk in parsed_data['risks'][:3]:
        print(f"  • {risk}")
    
    print(f"\nAssumptions ({len(parsed_data['assumptions'])}):")
    for assumption in parsed_data['assumptions'][:3]:
        print(f"  • {assumption}")
    
    # Validation results
    if 'validation' in parsed_data:
        validation = parsed_data['validation']
        print(f"\n📊 Validation Results:")
        print(f"  Valid: {validation['is_valid']}")
        print(f"  Completeness Score: {validation['completeness_score']:.1f}%")
        if validation['errors']:
            print(f"  Errors: {len(validation['errors'])}")
            for error in validation['errors']:
                print(f"    • {error}")
        if validation['warnings']:
            print(f"  Warnings: {len(validation['warnings'])}")
            for warning in validation['warnings']:
                print(f"    • {warning}")
    
    print(f"\n🎉 Comprehensive PRD Parsing Test Complete!")
    print(f"   Extracted {len([k for k, v in parsed_data.items() if v and k != 'validation'])} fields")
    
    return parsed_data

if __name__ == "__main__":
    test_comprehensive_prd_parsing()
