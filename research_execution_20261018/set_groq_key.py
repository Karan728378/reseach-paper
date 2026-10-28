import sys
import winreg

def main():
    print("=" * 60)
    print("GROQ API KEY SECURE CONFIGURATOR")
    print("Saves GROQ_API_KEY into Windows User Environment registry.")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        key = sys.argv[1].strip()
    else:
        try:
            key = input("Paste your Groq API key (starts with gsk_): ").strip()
        except EOFError:
            print("ERROR: No input received.")
            sys.exit(1)
            
    if not key:
        print("ERROR: Provided key was empty. Nothing saved.")
        sys.exit(1)
        
    from pathlib import Path
    key_file = Path(__file__).resolve().parent / "groq_key.txt"
    try:
        key_file.write_text(key, encoding="utf-8")
        print(f"SUCCESS: GROQ_API_KEY saved to gitignored file: {key_file.name}")
    except Exception as e:
        print(f"WARNING: Could not write to {key_file.name}: {e}")

    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_SET_VALUE) as reg_key:
            winreg.SetValueEx(reg_key, "GROQ_API_KEY", 0, winreg.REG_SZ, key)
        print("SUCCESS: GROQ_API_KEY successfully saved to HKCU\\Environment.")
        print("=" * 60)
    except Exception as e:
        print(f"WARNING: Failed to save to registry: {e}")

if __name__ == "__main__":
    main()
