"""
Test script for AutoPFTReport System.

This script tests the basic functionality of all agents and the API endpoints.
"""

import asyncio
import json
import requests
import time
from typing import Dict, Any

# Test data
SAMPLE_PFT_DATA = {
    "patient_demographics": {
        "patient_id": "TEST001",
        "age": 45,
        "gender": "Male",
        "height": 175,
        "weight": 80,
        "ethnicity": "Caucasian",
        "smoking_status": "Former"
    },
    "raw_data": {
        "fvc": 3.2,
        "fev1": 2.1,
        "fev1_fvc_ratio": 65.6,
        "pef": 4.5,
        "fef25_75": 1.8,
        "dlco": 18.5,
        "tlc": 5.8,
        "rv": 2.6,
        "post_bd_fvc": 3.3,
        "post_bd_fev1": 2.3
    },
    "predicted_values": {
        "fvc": 4.2,
        "fev1": 3.4,
        "dlco": 25.0,
        "tlc": 6.5
    },
    "percent_predicted": {
        "fvc_percent": 76.2,
        "fev1_percent": 61.8,
        "dlco_percent": 74.0,
        "tlc_percent": 89.2
    }
}

SAMPLE_FILE_CONTENT = """
PULMONARY FUNCTION TEST REPORT
Patient: TEST001
Date: 2024-01-15

SPIROMETRY RESULTS:
FVC: 3.2 L (76% predicted)
FEV1: 2.1 L (62% predicted)
FEV1/FVC: 65.6%
PEF: 4.5 L/s
FEF25-75: 1.8 L/s

POST-BRONCHODILATOR:
FVC: 3.3 L
FEV1: 2.3 L

LUNG VOLUMES:
TLC: 5.8 L (89% predicted)
RV: 2.6 L

DIFFUSION CAPACITY:
DLCO: 18.5 mL/min/mmHg (74% predicted)
"""


def test_agent_imports():
    """Test that all agents can be imported successfully."""
    print("Testing agent imports...")
    
    try:
        from agent.data_specialist import DataSpecialistAgent
        from agent.interpreter import InterpreterAgent
        from agent.report_writer import ReportWriterAgent
        from agent.triage_specialist import TriageSpecialistAgent
        from agent.medical_chatbot import MedicalChatbotAgent
        from agent.learning_assistant import LearningAssistantAgent
        
        print("✓ All agents imported successfully")
        return True
    except Exception as e:
        print(f"✗ Agent import failed: {e}")
        return False


def test_agent_initialization():
    """Test that all agents can be initialized."""
    print("Testing agent initialization...")
    
    try:
        from agent.data_specialist import DataSpecialistAgent
        from agent.interpreter import InterpreterAgent
        from agent.report_writer import ReportWriterAgent
        from agent.triage_specialist import TriageSpecialistAgent
        from agent.medical_chatbot import MedicalChatbotAgent
        from agent.learning_assistant import LearningAssistantAgent
        
        # Initialize agents
        data_specialist = DataSpecialistAgent()
        interpreter = InterpreterAgent()
        report_writer = ReportWriterAgent()
        triage_specialist = TriageSpecialistAgent()
        medical_chatbot = MedicalChatbotAgent()
        learning_assistant = LearningAssistantAgent()
        
        print("✓ All agents initialized successfully")
        return True
    except Exception as e:
        print(f"✗ Agent initialization failed: {e}")
        return False


def test_data_specialist():
    """Test the Data Specialist agent."""
    print("Testing Data Specialist agent...")
    
    try:
        from agent.data_specialist import DataSpecialistAgent
        
        agent = DataSpecialistAgent()
        
        # Test file processing
        result = agent.process_file(SAMPLE_FILE_CONTENT, "txt")
        
        if result and "raw_data" in result:
            print("✓ Data Specialist agent working")
            return True
        else:
            print("✗ Data Specialist agent returned invalid result")
            return False
            
    except Exception as e:
        print(f"✗ Data Specialist agent failed: {e}")
        return False


def test_interpreter():
    """Test the Interpreter agent."""
    print("Testing Interpreter agent...")
    
    try:
        from agent.interpreter import InterpreterAgent
        
        agent = InterpreterAgent()
        
        # Test interpretation
        result = agent.interpret_pft_results(
            raw_data=SAMPLE_PFT_DATA["raw_data"],
            predicted_values=SAMPLE_PFT_DATA["predicted_values"],
            percent_predicted=SAMPLE_PFT_DATA["percent_predicted"],
            patient_demographics=SAMPLE_PFT_DATA["patient_demographics"]
        )
        
        if result and "pattern" in result:
            print("✓ Interpreter agent working")
            return True
        else:
            print("✗ Interpreter agent returned invalid result")
            return False
            
    except Exception as e:
        print(f"✗ Interpreter agent failed: {e}")
        return False


def test_api_endpoints():
    """Test API endpoints."""
    print("Testing API endpoints...")
    
    base_url = "http://localhost:8000"
    
    try:
        # Test health endpoint
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✓ Health endpoint working")
        else:
            print(f"✗ Health endpoint failed: {response.status_code}")
            return False
        
        # Test root endpoint
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("✓ Root endpoint working")
        else:
            print(f"✗ Root endpoint failed: {response.status_code}")
            return False
        
        # Test direct interpretation endpoint
        interpretation_data = {
            "raw_data": SAMPLE_PFT_DATA["raw_data"],
            "patient_demographics": SAMPLE_PFT_DATA["patient_demographics"],
            "predicted_values": SAMPLE_PFT_DATA["predicted_values"]
        }
        
        response = requests.post(
            f"{base_url}/pft/interpret",
            json=interpretation_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if "interpretation" in result and "triage" in result:
                print("✓ Direct interpretation endpoint working")
            else:
                print("✗ Direct interpretation endpoint returned invalid result")
                return False
        else:
            print(f"✗ Direct interpretation endpoint failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to API server. Make sure it's running on localhost:8000")
        return False
    except Exception as e:
        print(f"✗ API endpoint test failed: {e}")
        return False


def run_all_tests():
    """Run all tests."""
    print("=" * 50)
    print("AutoPFTReport System Test Suite")
    print("=" * 50)
    
    tests = [
        ("Agent Imports", test_agent_imports),
        ("Agent Initialization", test_agent_initialization),
        ("Data Specialist", test_data_specialist),
        ("Interpreter", test_interpreter),
        ("API Endpoints", test_api_endpoints)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 30)
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)

