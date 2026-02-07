try:
    print("Importing app.main...")
    from app.main import app
    print("Success!")
    
    print("Creating TestClient...")
    from fastapi.testclient import TestClient
    client = TestClient(app)
    print("Client created!")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
