#!/bin/bash

echo "⏳ Esperando o banco de dados iniciar..."
sleep 5  # pode ajustar se o banco for mais lento

echo "✅ Criando tabelas (se necessário)..."
python -c "from database.base import Base; from database.engine import engine; import models.filament; Base.metadata.create_all(bind=engine)"

echo "📦 Populando dados iniciais..."
python database/populate.py

echo "🚀 Iniciando o servidor FastAPI..."
exec uvicorn main:app --host 0.0.0.0 --port 8000