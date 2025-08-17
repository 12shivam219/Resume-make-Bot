
### 7. `run.py` (Application Entry Point)
```python
from app import create_app
import os

# Create application instance
app = create_app()

if __name__ == '__main__':
    # Run in development mode
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))