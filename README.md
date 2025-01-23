# Setup
## For Docker
- docker compose up --build
If you add new python package then you might need to run build command again
else just run without --build flag
- docker compose up

## No Docker ? Run directly in python
- python3 -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt
- uvicorn app.main:app --reload --port 8888

## Start venv in Windows
- Command Prompt: `venv\Scripts\activate`
- Powershell: `.\venv\Scripts\Activate`

