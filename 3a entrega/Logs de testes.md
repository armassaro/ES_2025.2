# Logs de testes

O presente arquivo se propõe a armazenar os logs de testes da aplicação, contendo informações como a pessoa que executou os testes, informações de data da execução, escopo e ID do cenário testado.

## Execuções - 28/11/2025

### Teste #01

> **Data de execução**: 28/11/2025  
> **ID do cenário**: CTA-001, CTA-002, CTA-003, CTA-004  
> **Membro**: Arthur  
> **Foram apontados erros?**: True

#### Descrição do teste
Durante a execução dos testes de CRUD (test_habit_crud.py), ocorreu um erro crítico que impediu completamente a coleta e execução dos 4 cenários de teste. O pytest retornou o seguinte erro:

```
ModuleNotFoundError: No module named 'model.ReportFactory'
ERROR collecting tests/test_habit_crud.py
!!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!!
```

O ambiente de teste estava configurado corretamente (Windows 11, Python 3.13.9, pytest 9.0.1), porém a ausência do módulo `ReportFactory` bloqueou completamente a execução.

Nenhum dos testes de CRUD pôde ser executado devido a esta dependência faltante.

#### Ações a serem tomadas para correção do erro
- Criar o arquivo `model/ReportFactory.py` com a classe ReportFactory e métodos básicos
- Implementar as classes e métodos necessários para o sistema de geração de relatórios
- Garantir que todas as importações estejam corretas nos arquivos de teste
- Re-executar os testes após implementação do módulo

#### Ações tomadas para correção do erro
- Documentação do erro crítico que impede a execução dos testes
- Priorização da implementação do módulo `ReportFactory` como tarefa crítica
- Planejamento da estrutura básica do módulo de relatórios

---

### Teste #02

> **Data de execução**: 28/11/2025  
> **ID do cenário**: CTA-005, CTA-006, CTA-007, CTA-008  
> **Membro**: Ian  
> **Foram apontados erros?**: True

#### Descrição do teste
Durante a execução dos testes de Visualização (test_habit_visualization.py), foram encontrados múltiplos problemas. Do total de 4 cenários testados:
- **CTA-005 (filtro de hábitos ativos):** SKIPPED - teste ignorado por implementação incompleta
- **CTA-006 (busca por ID com histórico):** SKIPPED - teste ignorado por implementação incompleta  
- **CTA-007 (sistema vazio):** FAILED - falha crítica com UnicodeEncodeError
- **CTA-008 (ordenação alfabética):** SKIPPED - teste ignorado por implementação incompleta

O erro crítico ocorreu no CTA-007:

```
tests\test_habit_visualization.py:197: in test_cta_007_get_active_habits_empty_system
    all_habits = self.habit_model.get_all_habits()
model\HabitModel.py:82: in get_all_habits
    print("\u26a0\ufe0f Nenhum usuário logado!")
UnicodeEncodeError: 'charmap' codec can't encode characters in position 0-1: character maps to <undefined>
```

Adicionalmente, foram detectados 4 warnings do tipo `PytestUnknownMarkWarning` indicando que a marca `@pytest.mark.visualization` não está registrada no arquivo de configuração `pytest.ini`.

#### Ações a serem tomadas para correção do erro
- Substituir emojis por texto simples no arquivo `HabitModel.py:82` (ex: "[AVISO] Nenhum usuário logado!")
- Registrar a marca customizada `@pytest.mark.visualization` no arquivo `pytest.ini`
- Implementar os métodos de filtragem, busca por ID e ordenação alfabética
- Completar as implementações dos métodos do HabitModel
- Re-executar os testes após as correções

#### Ações tomadas para correção do erro
- Identificação do erro de encoding causado por emojis no código
- Documentação dos testes ignorados por falta de implementação
- Registro dos warnings de marcas não configuradas
- Priorização da correção de encoding como tarefa crítica

---

### Teste #03

> **Data de execução**: 28/11/2025  
> **ID do cenário**: CTA-009, CTA-010, CTA-011, CTA-012  
> **Membro**: Silvino  
> **Foram apontados erros?**: True

#### Descrição do teste
Durante a execução dos testes de Geração de Relatórios (test_report_generation.py), todos os 4 cenários foram marcados como SKIPPED (ignorados):
- **CTA-009 (relatório diário):** SKIPPED - dependências ausentes
- **CTA-010 (relatório semanal):** SKIPPED - dependências ausentes
- **CTA-011 (relatório mensal):** SKIPPED - dependências ausentes
- **CTA-012 (relatórios com histórico vazio):** SKIPPED - dependências ausentes

Log da execução:
```
tests/test_report_generation.py::TestReportGeneration::test_cta_009_daily_report_with_mixed_completion SKIPPED
tests/test_report_generation.py::TestReportGeneration::test_cta_010_weekly_report_with_completion_history SKIPPED
tests/test_report_generation.py::TestReportGeneration::test_cta_011_monthly_report_with_varied_patterns SKIPPED
tests/test_report_generation.py::TestReportGeneration::test_cta_012_reports_with_empty_history SKIPPED
```

Foram detectados 4 warnings do tipo `PytestUnknownMarkWarning` indicando que a marca `@pytest.mark.reports` não está registrada no arquivo `pytest.ini`. Todos os testes foram pulados por falta de implementações necessárias no `ReportController` e dependências relacionadas.

#### Ações a serem tomadas para correção do erro
- Implementar a classe `ReportController` com métodos básicos de geração de relatórios
- Criar métodos para geração de relatórios diários, semanais e mensais
- Implementar tratamento para casos de histórico vazio
- Registrar a marca customizada `@pytest.mark.reports` no arquivo `pytest.ini`
- Implementar as fixtures ausentes (`clean_json_files`, `mock_datetime`)
- Re-executar os testes após implementação das funcionalidades

#### Ações tomadas para correção do erro
- Documentação de todos os cenários ignorados por falta de implementação
- Identificação da necessidade de criar o ReportController completo
- Registro dos warnings de marcas não configuradas
- Planejamento da implementação do sistema de geração de relatórios

---

### Resumo Geral da Execução - 28/11/2025

### Estatísticas Consolidadas:
- **Total de arquivos de teste:** 3
- **Total de cenários de teste:** 12 (CTA-001 a CTA-012)
- **Testes coletados:** 8
- **Testes executados:** 5
- **Sucessos:** 0 ❌
- **Falhas:** 1 ❌
- **Ignorados:** 7 ⏭️
- **Erros de coleta:** 1 💥
- **Warnings:** 8 ⚠️
- **Taxa de sucesso:** 0%

### Distribuição por Responsável:
| Responsável | Cenários | Executados | Sucessos | Falhas | Ignorados | Status |
|-------------|----------|------------|----------|---------|-----------|---------|
| Arthur      | CTA-001 a CTA-004 | 0 | 0 | 0 | 4 | ❌ Erro de coleta |
| Ian         | CTA-005 a CTA-008 | 4 | 0 | 1 | 3 | ❌ Falha crítica |
| Silvino     | CTA-009 a CTA-012 | 4 | 0 | 0 | 4 | ⏭️ Todos ignorados |

### Problemas Críticos Identificados:
1. **ModuleNotFoundError:** `model.ReportFactory` não implementado (bloqueia CTA-001 a CTA-004)
2. **UnicodeEncodeError:** Emoji no `HabitModel.py:82` (falha CTA-007)
3. **PytestUnknownMarkWarning:** Marcas não registradas (8 ocorrências)
4. **Implementações incompletas:** Métodos e funcionalidades pendentes (CTA-005, CTA-006, CTA-008, CTA-009 a CTA-012)
5. **Fixtures ausentes:** `clean_json_files`, `mock_datetime` não implementadas

### Próximas Ações Prioritárias:

#### Prioridade CRÍTICA (Impedem execução):
- Criar arquivo `model/ReportFactory.py` com implementação mínima
- Corrigir encoding no `HabitModel.py:82` - substituir emoji por texto simples
- Implementar fixtures ausentes em `conftest.py`

#### Prioridade ALTA (Melhoram qualidade):
- Registrar marcas de teste (`visualization`, `reports`) no arquivo `pytest.ini`
- Completar métodos abstratos no `HabitModel`
- Implementar `ReportController` básico

#### Prioridade MÉDIA (Organização):
- Padronizar estrutura de dados de hábitos
- Adicionar documentação nos métodos
- Implementar tratamento de erros robusto