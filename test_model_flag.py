#!/usr/bin/env python3
"""
Test script for the model flag parsing functionality in the Poe o3 MCP server.
"""

import sys
from poe_o3_mcp_server import parse_model_flag

def test_parse_model_flag():
    """Test the parse_model_flag function with various inputs."""
    test_cases = [
        # Test case: No flag
        {
            "input": "What is the capital of France?",
            "expected_message": "What is the capital of France?",
            "expected_model": "o3"
        },
        # Test case: Flag at the beginning
        {
            "input": "--Claude-3.5-Sonnet What is the capital of France?",
            "expected_message": "What is the capital of France?",
            "expected_model": "Claude-3.5-Sonnet"
        },
        # Test case: Flag in the middle
        {
            "input": "Please tell me --Claude-3.5-Sonnet what is the capital of France?",
            "expected_message": "Please tell me what is the capital of France?",
            "expected_model": "Claude-3.5-Sonnet"
        },
        # Test case: Flag at the end
        {
            "input": "What is the capital of France? --Claude-3.5-Sonnet",
            "expected_message": "What is the capital of France?",
            "expected_model": "Claude-3.5-Sonnet"
        },
        # Test case: Multiple words in flag
        {
            "input": "What is the capital of France? --Claude-3.5-Sonnet",
            "expected_message": "What is the capital of France?",
            "expected_model": "Claude-3.5-Sonnet"
        },
        # Test case: Different model
        {
            "input": "What is the capital of France? --GPT-4",
            "expected_message": "What is the capital of France?",
            "expected_model": "GPT-4"
        }
    ]

    for i, test_case in enumerate(test_cases):
        input_msg = test_case["input"]
        expected_msg = test_case["expected_message"]
        expected_model = test_case["expected_model"]
        
        actual_msg, actual_model = parse_model_flag(input_msg)
        
        if actual_msg == expected_msg and actual_model == expected_model:
            print(f"Test case {i+1}: PASSED")
        else:
            print(f"Test case {i+1}: FAILED")
            print(f"  Input: '{input_msg}'")
            print(f"  Expected message: '{expected_msg}'")
            print(f"  Actual message: '{actual_msg}'")
            print(f"  Expected model: '{expected_model}'")
            print(f"  Actual model: '{actual_model}'")

if __name__ == "__main__":
    print("Testing parse_model_flag function...")
    test_parse_model_flag()
    print("Testing complete.")