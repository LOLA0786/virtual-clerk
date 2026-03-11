#!/bin/bash
echo "Starting Virtual Clerk API..."
uvicorn litigation_api:app --host 0.0.0.0 --port 8000
