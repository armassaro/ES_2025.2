import pytest
import os
import json
import sys
from unittest.mock import patch
from datetime import datetime

# Adicionar o diretório pai ao path para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def clean_json_files():
    """Limpa os arquivos JSON antes de cada teste"""
    test_files = ['usuarios.json', 'habitos_registros.json']
    
    # Backup dos arquivos originais
    backups = {}
    for file in test_files:
        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as f:
                backups[file] = f.read()
    
    # Limpa os arquivos para teste
    for file in test_files:
        with open(file, 'w', encoding='utf-8') as f:
            json.dump({} if 'usuarios' in file else [], f)
    
    yield
    
    # Restaura os arquivos originais
    for file, content in backups.items():
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)

@pytest.fixture
def sample_habit_data():
    """Dados de exemplo para testes"""
    return {
        "name": "Beber água",
        "description": "Beber 2L por dia",
        "frequency": "daily"
    }

@pytest.fixture
def mock_datetime():
    """Mock para data fixa nos testes"""
    with patch('datetime.datetime') as mock_dt:
        mock_dt.now.return_value = datetime(2025, 11, 14, 14, 30, 0)
        mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw)
        yield mock_dt