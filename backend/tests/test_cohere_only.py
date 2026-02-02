#!/usr/bin/env python3
"""
Test script to verify the Cohere-only implementation
"""

import sys
import os
from pathlib import Path

# Add the backend src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test that all imports work correctly"""
    print("Testing imports...")

    try:
        from src.agent.core import get_agent
        print("[PASS] Core module imported successfully")

        # Test that the Cohere client is properly configured
        agent_data = get_agent("test_user")
        print(f"[PASS] Agent created with model: {agent_data.get('model')}")

        client = agent_data["client"]
        print(f"[PASS] Cohere client type: {type(client)}")

        return True

    except ImportError as e:
        print(f"[FAIL] Import error: {e}")
        return False
    except Exception as e:
        print(f"[FAIL] Error creating agent: {e}")
        return False


def test_core_logic():
    """Test the core logic without making actual API calls"""
    print("\nTesting core logic...")

    try:
        from src.agent.core import bind_tools_to_user
        from src.mcp.tools import all_tools

        # Test tool binding
        user_tools = bind_tools_to_user(all_tools, "test_user_123")
        print(f"[PASS] Bound {len(user_tools)} tools to user")

        # Test agent creation
        from src.agent.core import get_agent
        agent_data = get_agent("test_user_123")

        if "client" in agent_data and "tools" in agent_data:
            print("[PASS] Agent data contains required keys")
        else:
            print("[FAIL] Agent data missing required keys")
            return False

        return True

    except Exception as e:
        print(f"[FAIL] Error in core logic: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("=" * 60)
    print("Cohere-Only Implementation Test")
    print("=" * 60)

    success_count = 0
    total_tests = 2

    if test_imports():
        success_count += 1

    if test_core_logic():
        success_count += 1

    print("\n" + "=" * 60)
    print(f"Results: {success_count}/{total_tests} tests passed")

    if success_count == total_tests:
        print("[SUCCESS] ALL TESTS PASSED! Cohere-only implementation is ready.")
    else:
        print("[WARNING] Some tests failed. Please check the implementation.")

    print("=" * 60)
    return success_count == total_tests


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)