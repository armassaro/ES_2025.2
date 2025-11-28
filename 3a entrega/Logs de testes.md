# Logs de testes

O presente arquivo se propõe a armazenar os logs de testes da aplicação, contendo informações como a pessoa que executou os testes, informações de data da execução, escopo e ID do cenário testado.

---

## Execução de Testes - 28/11/2025

### Informações Gerais
- **Data de execução:** 28/11/2025  
- **Hora de execução:** 15:30 (horário estimado)
- **Responsável pela execução:** Equipe HabitTracker
- **Ambiente:** Windows 11, Python 3.13.9, pytest 9.0.1
- **Diretório:** HabitTracker/
- **Plugins utilizados:** json-report-1.5.0, metadata-3.1.1, mock-3.15.1

---

### 1. Testes de CRUD - test_habit_crud.py
**Responsável:** Arthur  
**Cenários testados:** CTA-001, CTA-002, CTA-003, CTA-004

#### Resultados:
- **Status:** ❌ FALHOU
- **Total de testes:** 4 cenários
- **Executados:** 1 teste
- **Falhas:** 1 teste
- **Ignorados:** 3 testes

#### Problemas principais encontrados:
1. **ModuleNotFoundError:** No module named 'model.ReportFactory'
2. **ImportError:** Falha ao importar dependências do sistema
3. **Configuração incompleta:** Métodos e classes não implementados

#### Log detalhado:
```
============================= test session starts =============================
platform win32 -- Python 3.13.9, pytest-9.0.1, pluggy-1.6.0
cachedir: .pytest_cache
rootdir: C:\Users\ianba\OneDrive\Área de Trabalho\facul\ES_2025.2\HabitTracker
plugins: json-report-1.5.0, metadata-3.1.1, mock-3.15.1

ERROR collecting tests/test_habit_crud.py
ModuleNotFoundError: No module named 'model.ReportFactory'

!!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!!
```

---

### 2. Testes de Visualização - test_habit_visualization.py  
**Responsável:** Ian  
**Cenários testados:** CTA-005, CTA-006, CTA-007, CTA-008

#### Resultados:
- **Status:** ❌ FALHOU
- **Total de testes:** 4 cenários
- **Executados:** 4 testes
- **Sucessos:** 0 testes
- **Falhas:** 1 teste  
- **Ignorados:** 3 testes
- **Warnings:** 4 warnings (PytestUnknownMarkWarning)

#### Problemas principais encontrados:
1. **UnicodeEncodeError:** 'charmap' codec can't encode characters (emoji/caracteres especiais)
2. **PytestUnknownMarkWarning:** Marca `@pytest.mark.visualization` não registrada
3. **Lógica de teste incompleta:** Testes pulados por falta de implementação

#### Log detalhado:
```
============================= test session starts =============================
platform win32 -- Python 3.13.9, pytest-9.0.1, pluggy-1.6.0
cachedir: .pytest_cache
rootdir: C:\Users\ianba\OneDrive\Área de Trabalho\facul\ES_2025.2\HabitTracker
plugins: json-report-1.5.0, metadata-3.1.1, mock-3.15.1
collecting ... collected 4 items

tests/test_habit_visualization.py::TestHabitVisualization::test_cta_005_get_active_habits_filter SKIPPED
tests/test_habit_visualization.py::TestHabitVisualization::test_cta_006_get_habit_by_id_with_history SKIPPED
tests/test_habit_visualization.py::TestHabitVisualization::test_cta_007_get_active_habits_empty_system FAILED
tests/test_habit_visualization.py::TestHabitVisualization::test_cta_008_habits_alphabetical_ordering SKIPPED

================================== FAILURES ===================================
_____ TestHabitVisualization.test_cta_007_get_active_habits_empty_system ______
tests\test_habit_visualization.py:197: in test_cta_007_get_active_habits_empty_system
    all_habits = self.habit_model.get_all_habits()
model\HabitModel.py:82: in get_all_habits
    print("\u26a0\ufe0f Nenhum usu\xe1rio logado!")
UnicodeEncodeError: 'charmap' codec can't encode characters in position 0-1: character maps to <undefined>

============================== warnings summary ===============================
tests\test_habit_visualization.py:28: PytestUnknownMarkWarning: Unknown pytest.mark.visualization
tests\test_habit_visualization.py:114: PytestUnknownMarkWarning: Unknown pytest.mark.visualization
tests\test_habit_visualization.py:187: PytestUnknownMarkWarning: Unknown pytest.mark.visualization  
tests\test_habit_visualization.py:229: PytestUnknownMarkWarning: Unknown pytest.mark.visualization

=========================== short test summary info ===========================
FAILED tests/test_habit_visualization.py::TestHabitVisualization::test_cta_007_get_active_habits_empty_system
================== 1 failed, 3 skipped, 4 warnings in 0.21s ===================
```

---

### 3. Testes de Relatórios - test_report_generation.py
**Responsável:** Silvino  
**Cenários testados:** CTA-009, CTA-010, CTA-011, CTA-012

#### Resultados:
- **Status:** ⚠️ TODOS IGNORADOS
- **Total de testes:** 4 cenários
- **Executados:** 4 testes  
- **Sucessos:** 0 testes
- **Falhas:** 0 testes
- **Ignorados:** 4 testes
- **Warnings:** 4 warnings (PytestUnknownMarkWarning)

#### Problemas principais encontrados:
1. **Testes não executados:** Todos os 4 testes foram marcados como SKIPPED
2. **PytestUnknownMarkWarning:** Marca `@pytest.mark.reports` não registrada
3. **Dependências ausentes:** Testes pulados por falta de implementações necessárias

#### Log detalhado:
```
============================= test session starts =============================
platform win32 -- Python 3.13.9, pytest-9.0.1, pluggy-1.6.0
cachedir: .pytest_cache
rootdir: C:\Users\ianba\OneDrive\Área de Trabalho\facul\ES_2025.2\HabitTracker
plugins: json-report-1.5.0, metadata-3.1.1, mock-3.15.1
collecting ... collected 4 items

tests/test_report_generation.py::TestReportGeneration::test_cta_009_daily_report_with_mixed_completion SKIPPED
tests/test_report_generation.py::TestReportGeneration::test_cta_010_weekly_report_with_completion_history SKIPPED
tests/test_report_generation.py::TestReportGeneration::test_cta_011_monthly_report_with_varied_patterns SKIPPED
tests/test_report_generation.py::TestReportGeneration::test_cta_012_reports_with_empty_history SKIPPED

============================== warnings summary ===============================
tests\test_report_generation.py:41: PytestUnknownMarkWarning: Unknown pytest.mark.reports
tests\test_report_generation.py:167: PytestUnknownMarkWarning: Unknown pytest.mark.reports
tests\test_report_generation.py:313: PytestUnknownMarkWarning: Unknown pytest.mark.reports
tests\test_report_generation.py:494: PytestUnknownMarkWarning: Unknown pytest.mark.reports

======================= 4 skipped, 4 warnings in 0.09s ========================
```

---

### 4. Execução Combinada - Resumo Geral

#### Resultados Consolidados:
- **Total de arquivos de teste:** 3
- **Total de cenários de teste:** 12 (CTA-001 a CTA-012)
- **Testes executados:** 5
- **Sucessos:** 0 ❌
- **Falhas:** 2 ❌ 
- **Ignorados:** 7 ⏭️
- **Erros de coleta:** 1 💥
- **Warnings:** 8 ⚠️
- **Taxa de sucesso:** 0% ❌

#### Distribuição por Responsável:
| Responsável | Cenários | Executados | Sucessos | Falhas | Ignorados | Status |
|-------------|----------|------------|----------|---------|-----------|---------|
| Arthur      | CTA-001 a CTA-004 | 0 | 0 | 0 | 4 | ❌ Erro de coleta |
| Ian         | CTA-005 a CTA-008 | 4 | 0 | 1 | 3 | ❌ Falha crítica |
| Silvino     | CTA-009 a CTA-012 | 4 | 0 | 0 | 4 | ⏭️ Todos ignorados |

#### Problemas Comuns Identificados:
1. **Dependências ausentes:** `model.ReportFactory` não implementado
2. **Codificação de caracteres:** Problemas com emojis e caracteres especiais no Windows
3. **Marcas de teste não registradas:** `@pytest.mark.visualization` e `@pytest.mark.reports`
4. **Implementações incompletas:** Métodos abstratos não implementados
5. **Fixtures ausentes:** `clean_json_files`, `mock_datetime` não implementadas

---

### Análise Técnica Detalhada

#### Erros Críticos (Impedem execução):
1. **ModuleNotFoundError: No module named 'model.ReportFactory'**
   - **Impacto:** Impede execução completa dos testes de CRUD
   - **Causa:** Classe `ReportFactory` não foi implementada
   - **Arquivos afetados:** `test_habit_crud.py`

2. **UnicodeEncodeError: 'charmap' codec can't encode characters**
   - **Impacto:** Falha na execução de testes de visualização
   - **Causa:** Uso de emojis em `print()` no código `HabitModel.py:82`
   - **Arquivos afetados:** `test_habit_visualization.py`

#### Warnings (Não críticos mas devem ser corrigidos):
1. **PytestUnknownMarkWarning** (8 ocorrências)
   - **Causa:** Marcas customizadas não registradas no `pytest.ini`
   - **Solução:** Registrar marcas ou remover decoradores

#### Implementações Pendentes:
1. **model/ReportFactory.py** - Completamente ausente
2. **Métodos do HabitModel** - Implementações incompletas
3. **Fixtures de teste** - `clean_json_files`, `mock_datetime`
4. **Tratamento de encoding** - Substituir emojis por texto simples

---

### Ações Recomendadas

#### Prioridade CRÍTICA (Impede execução):
1. **Implementar `model/ReportFactory.py`** com classe e métodos básicos
2. **Corrigir encoding no HabitModel.py:82** - substituir emoji por texto
3. **Implementar fixtures ausentes** em `conftest.py`

#### Prioridade ALTA (Melhora qualidade):
4. **Registrar marcas de teste** no arquivo `pytest.ini`
5. **Completar métodos abstratos** no `HabitModel`
6. **Implementar `ReportController`** básico

#### Prioridade MÉDIA (Organização):
7. **Padronizar estrutura de dados** de hábitos
8. **Adicionar documentação** nos métodos
9. **Implementar tratamento de erros** robusto

#### Prioridade BAIXA (Refinamento):
10. **Otimizar performance** dos testes
11. **Adicionar testes unitários** granulares
12. **Melhorar cobertura de código**

---

### Próximos Passos

#### Fase 1 - Correções Críticas (Prazo: Imediato)
- [ ] Criar arquivo `model/ReportFactory.py` com implementação mínima
- [ ] Corrigir problema de encoding no `HabitModel.py`
- [ ] Implementar fixtures básicas em `conftest.py`
- [ ] Testar execução básica sem erros de coleta

#### Fase 2 - Implementações Core (Prazo: 1-2 dias)  
- [ ] Implementar métodos `add_habit`, `get_all_habits`, `get_habit_by_id`
- [ ] Criar `ReportController` básico
- [ ] Registrar marcas de teste adequadamente
- [ ] Executar e validar testes individuais

#### Fase 3 - Refinamento (Prazo: Final do projeto)
- [ ] Completar todos os cenários de teste
- [ ] Atingir taxa de sucesso > 80%
- [ ] Documentar funcionalidades implementadas
- [ ] Preparar apresentação final

---

### Conclusões

O sistema **HabitTracker** está em fase inicial de implementação com **infraestrutura de testes bem estruturada** mas **implementações de core faltantes**. Os 12 cenários de teste (CTA-001 a CTA-012) estão bem definidos e aguardam apenas as implementações correspondentes.

**Pontos Positivos:**
✅ Estrutura de testes bem organizada  
✅ Cenários de teste abrangentes e detalhados  
✅ Padrão MVC bem definido  
✅ Configuração de ambiente adequada  

**Pontos de Atenção:**
❌ 0% de taxa de sucesso nos testes  
❌ Dependências críticas ausentes  
❌ Problemas de encoding no ambiente Windows  
❌ Implementações de métodos incompletas  

A **prioridade imediata** deve ser resolver os erros críticos para permitir a execução básica dos testes, seguida pela implementação gradual das funcionalidades core do sistema.

---

**Última atualização:** 28/11/2025  
**Próxima revisão:** Após implementação das correções críticas