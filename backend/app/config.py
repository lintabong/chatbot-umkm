import os

class Config:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/lintang')
    MODEL_CONTEXT = '''Kamu adalah asisten AI untuk bisnis UMKM, kamu membantu tentang marketing, bisnis,
            legalitas, hukum di indonesia, dll'''