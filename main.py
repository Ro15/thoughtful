from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get('/health')
def health() -> dict:
    """Health check endpoint"""
    return {'status': 'ok'}

@app.post('/trigger')
def trigger() -> dict:
    """Trigger action endpoint"""
    return {'message': 'triggered'}

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)
