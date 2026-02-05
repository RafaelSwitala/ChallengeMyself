#!/usr/bin/env python
"""
Flask Server Runner - Einfach und zuverlässig
"""
import sys
import time
import os

# Add the backend directory to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    print("🚀 Loading Flask app...")
    from app import app
    
    print("✅ App loaded successfully")
    print("⏳ Starting server on http://127.0.0.1:5000/")
    print("   Press CTRL+C to stop\n")
    
    # Run without debug and without reloader
    app.run(
        debug=False, 
        host='127.0.0.1', 
        port=5000, 
        use_reloader=False, 
        threaded=True,
        use_debugger=False
    )
    
except KeyboardInterrupt:
    print("\n\n🛑 Server stopped by user")
    sys.exit(0)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
