#!/usr/bin/env python3
"""
Test the updated agent runner to see if the Cohere 405 error is handled
"""

import os
import sys
from pathlib import Path

# Add the backend src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "backend/src"))

from agent.runner import run_agent_sync

def test_agent_runner():
    """Test the agent runner with the updated fallback mechanism"""
    print("Testing Agent Runner with Fallback Mechanism...")

    try:
        # Try to run a simple test - this will attempt to call Cohere API
        result = run_agent_sync(
            user_id="test_user_123",
            message_text="Hello, can you help me add a task?",
            conversation_id=None
        )

        print(f"[OK] Agent runner executed successfully")
        print(f"Response: {result.get('response', 'No response')}")
        print(f"Tool calls made: {len(result.get('tool_calls', []))}")

        return True

    except Exception as e:
        print(f"[ERROR] Agent runner failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Testing Updated Agent Runner")
    print("=" * 60)

    success = test_agent_runner()

    print("\n" + "=" * 60)
    if success:
        print("SUCCESS: Agent runner is working with fallback mechanism!")
    else:
        print("FAILURE: Agent runner still has issues.")
    print("=" * 60)