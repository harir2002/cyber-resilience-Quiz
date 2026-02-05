
import sys
import os
from pathlib import Path

# Add current dir to path
sys.path.append(os.getcwd())

print("Importing app from main...")
try:
    from main import app
    print("App imported successfully.")
    
    print("Registered Routes:")
    found_config = False
    for route in app.routes:
        if hasattr(route, "path"):
            methods = ','.join(route.methods)
            print(f"  - {route.path} [{methods}]")
            if route.path == "/api/config":
                found_config = True
                
    if found_config:
        print("\nSUCCESS: /api/config route is present in the app object.")
    else:
        print("\nFAILURE: /api/config route is MISSING from the app object.")
        
except Exception as e:
    print(f"Error importing app: {e}")
    import traceback
    traceback.print_exc()
