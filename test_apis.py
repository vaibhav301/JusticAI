import requests
import json
import os

BASE_URL = "http://localhost:5000/api"

def test_predict_verdict():
    """Test the verdict prediction endpoint."""
    print("\nTesting /predict endpoint...")
    
    data = {
        "title": "New Contract Dispute",
        "description": """A contract dispute between two companies regarding 
        the delivery of specialized equipment. The defendant claims the equipment 
        was delivered on time, while the plaintiff argues that the specifications 
        were not met.""",
        "plaintiff": "Tech Solutions Inc",
        "defendant": "Global Equipment Ltd",
        "case_type": "Contract"
    }
    
    response = requests.post(f"{BASE_URL}/predict", json=data)
    print(f"Status Code: {response.status_code}")
    print("Response:", json.dumps(response.json(), indent=2))
    return response.json()

def test_analyze_document():
    """Test the document analysis endpoint."""
    print("\nTesting /analyze-document endpoint...")
    
    # Create a sample document
    sample_doc = """IN THE COURT OF LAW
    Case Number: DOC-2024001
    
    The plaintiff alleges that the defendant failed to maintain proper safety 
    standards in their manufacturing facility. Multiple incidents have been 
    reported, and inspection reports show several violations of safety protocols.
    
    Witness testimonies indicate that management was aware of these issues but 
    failed to take appropriate action. The defendant claims that all necessary 
    safety measures were in place and that the incidents were isolated cases."""
    
    # Save to temporary file
    with open("temp_doc.txt", "w") as f:
        f.write(sample_doc)
    
    # Send file
    with open("temp_doc.txt", "rb") as f:
        files = {"file": f}
        response = requests.post(f"{BASE_URL}/analyze-document", files=files)
    
    # Clean up
    os.remove("temp_doc.txt")
    
    print(f"Status Code: {response.status_code}")
    print("Response:", json.dumps(response.json(), indent=2))
    return response.json()

def test_get_case(case_id):
    """Test getting a specific case."""
    print(f"\nTesting /case/{case_id} endpoint...")
    
    response = requests.get(f"{BASE_URL}/case/{case_id}")
    print(f"Status Code: {response.status_code}")
    print("Response:", json.dumps(response.json(), indent=2))
    return response.json()

def test_get_history():
    """Test getting case history."""
    print("\nTesting /history endpoint...")
    
    response = requests.get(f"{BASE_URL}/history")
    print(f"Status Code: {response.status_code}")
    print("Response:", json.dumps(response.json(), indent=2))
    return response.json()

def run_all_tests():
    """Run all API tests."""
    print("Starting API tests...")
    
    # Test predict endpoint
    predict_response = test_predict_verdict()
    case_id = predict_response.get('case_id')
    
    # Test document analysis
    test_analyze_document()
    
    # Test get case
    if case_id:
        test_get_case(case_id)
    
    # Test history
    test_get_history()
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    run_all_tests() 