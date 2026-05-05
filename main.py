# main.py
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "ui":
            print("Starting Streamlit UI...")
            import subprocess
            subprocess.run(["streamlit", "run", "ui/app.py"])
        elif command == "test":
            print("Testing agent...")
            from agent.symptom_agent import get_agent_response
            user_input = input("Enter symptoms: ")
            response = get_agent_response(user_input)
            print("\nAgent Response:", response)
        else:
            print("Usage: python main.py [ui|test]")
    else:
        print("Symptom Checker Agent")
        print("Usage: python main.py [ui|test]")
        print("  ui   - Launch web UI")
        print("  test - Test agent in terminal")

if __name__ == "__main__":
    main()