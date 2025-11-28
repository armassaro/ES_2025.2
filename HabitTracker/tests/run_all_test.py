import subprocess
import sys
import os
from datetime import datetime

def run_test_suite():
    """
    Script para executar todos os testes do HabitTracker e gerar relatórios
    """
    print("🚀 Iniciando execução completa da suíte de testes HabitTracker")
    print("=" * 80)
    
    # Configurações
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    reports_dir = "test_reports"
    
    # Criar diretório de relatórios se não existir
    os.makedirs(reports_dir, exist_ok=True)
    
    # Lista de todos os arquivos de teste
    test_files = [
        "tests/test_habit_crud.py",           # CTA-001 a CTA-004 (Arthur)
        "tests/test_habit_visualization.py",  # CTA-005 a CTA-008 (Ian)  
        "tests/test_report_generation.py"     # CTA-009 a CTA-012 (Silvino)
    ]
    
    # Resultados para o relatório final
    test_results = {}
    
    print(f"📁 Relatórios serão salvos em: {reports_dir}/")
    print(f"🕐 Timestamp: {timestamp}")
    print("-" * 80)
    
    # Executar cada arquivo de teste individualmente
    for i, test_file in enumerate(test_files, 1):
        print(f"\n📋 [{i}/{len(test_files)}] Executando: {test_file}")
        
        # Nome do arquivo de relatório
        test_name = os.path.basename(test_file).replace('.py', '')
        report_file = f"{reports_dir}/{test_name}_{timestamp}.txt"
        
        try:
            # Executar pytest com saída detalhada
            cmd = [
                sys.executable, "-m", "pytest", 
                test_file, 
                "-v", "-s", 
                "--tb=long",
                "--capture=no",
                "-W", "default"  # Mostrar todos os warnings
            ]
            
            print(f"   Comando: {' '.join(cmd)}")
            print(f"   Salvando em: {report_file}")
            
            # Executar e capturar saída
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                encoding='utf-8',
                timeout=300  # 5 minutos timeout
            )
            
            # Salvar resultado completo em arquivo
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(f"RELATÓRIO DE TESTE: {test_file}\n")
                f.write(f"Data/Hora: {datetime.now()}\n")
                f.write(f"Comando: {' '.join(cmd)}\n")
                f.write("=" * 80 + "\n\n")
                
                f.write("STDOUT:\n")
                f.write("-" * 40 + "\n")
                f.write(result.stdout)
                f.write("\n\n")
                
                f.write("STDERR:\n") 
                f.write("-" * 40 + "\n")
                f.write(result.stderr)
                f.write("\n\n")
                
                f.write(f"CÓDIGO DE SAÍDA: {result.returncode}\n")
                f.write(f"SUCESSO: {'✅ SIM' if result.returncode == 0 else '❌ NÃO'}\n")
            
            # Armazenar resultado para relatório final
            test_results[test_file] = {
                'return_code': result.returncode,
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'report_file': report_file
            }
            
            # Mostrar resumo na tela
            if result.returncode == 0:
                print(f"   ✅ SUCESSO - Sem erros críticos")
            else:
                print(f"   ❌ FALHAS DETECTADAS - Ver {report_file}")
                
            # Contar warnings
            warning_count = result.stdout.count('warning') + result.stderr.count('warning')
            if warning_count > 0:
                print(f"   ⚠️  {warning_count} warning(s) detectado(s)")
                
        except subprocess.TimeoutExpired:
            print(f"   ⏰ TIMEOUT - Teste demorou mais de 5 minutos")
            test_results[test_file] = {
                'return_code': -1,
                'success': False,
                'error': 'TIMEOUT'
            }
            
        except Exception as e:
            print(f"   💥 ERRO DE EXECUÇÃO: {e}")
            test_results[test_file] = {
                'return_code': -2,
                'success': False,
                'error': str(e)
            }
    
    # Executar TODOS os testes juntos para comparação
    print(f"\n📋 [FINAL] Executando todos os testes juntos...")
    all_tests_report = f"{reports_dir}/all_tests_combined_{timestamp}.txt"
    
    try:
        cmd_all = [
            sys.executable, "-m", "pytest", 
            "tests/", 
            "-v", "-s", 
            "--tb=short",
            "-W", "default"
        ]
        
        result_all = subprocess.run(
            cmd_all,
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=600  # 10 minutos para todos
        )
        
        with open(all_tests_report, 'w', encoding='utf-8') as f:
            f.write(f"RELATÓRIO COMBINADO - TODOS OS TESTES\n")
            f.write(f"Data/Hora: {datetime.now()}\n")
            f.write("=" * 80 + "\n\n")
            f.write(result_all.stdout)
            f.write("\n\nERROS:\n")
            f.write(result_all.stderr)
        
        test_results['ALL_COMBINED'] = {
            'return_code': result_all.returncode,
            'success': result_all.returncode == 0,
            'report_file': all_tests_report
        }
        
    except Exception as e:
        print(f"   💥 Erro ao executar todos os testes: {e}")
    
    # Gerar relatório final de resumo
    generate_summary_report(test_results, reports_dir, timestamp)
    
    print("\n" + "=" * 80)
    print("🏁 EXECUÇÃO COMPLETA!")
    print(f"📊 Ver relatório resumo em: {reports_dir}/summary_report_{timestamp}.html")
    print("=" * 80)

def generate_summary_report(results, reports_dir, timestamp):
    """Gerar relatório HTML de resumo"""
    
    summary_file = f"{reports_dir}/summary_report_{timestamp}.html"
    
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Relatório de Testes - HabitTracker</title>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .success {{ color: green; }}
        .failure {{ color: red; }}
        .warning {{ color: orange; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .details {{ margin: 10px 0; padding: 10px; background-color: #f9f9f9; }}
    </style>
</head>
<body>
    <h1>📋 Relatório de Testes - HabitTracker</h1>
    <p><strong>Data/Hora:</strong> {datetime.now()}</p>
    <p><strong>Timestamp:</strong> {timestamp}</p>
    
    <h2>📊 Resumo Geral</h2>
    <table>
        <tr>
            <th>Arquivo de Teste</th>
            <th>Status</th>
            <th>Código de Saída</th>
            <th>Relatório Detalhado</th>
        </tr>
    """
    
    for test_file, result in results.items():
        status = "✅ SUCESSO" if result.get('success', False) else "❌ FALHA"
        status_class = "success" if result.get('success', False) else "failure"
        
        report_link = ""
        if 'report_file' in result:
            report_name = os.path.basename(result['report_file'])
            report_link = f'<a href="{report_name}">{report_name}</a>'
        
        html_content += f"""
        <tr>
            <td><strong>{test_file}</strong></td>
            <td class="{status_class}">{status}</td>
            <td>{result.get('return_code', 'N/A')}</td>
            <td>{report_link}</td>
        </tr>
        """
    
    html_content += """
    </table>
    
    <h2>🔍 Análise de Problemas Detectados</h2>
    <div class="details">
    """
    
    # Analisar problemas comuns
    common_issues = analyze_common_issues(results)
    
    for issue_type, issues in common_issues.items():
        if issues:
            html_content += f"<h3>⚠️ {issue_type}</h3><ul>"
            for issue in issues:
                html_content += f"<li>{issue}</li>"
            html_content += "</ul>"
    
    html_content += """
    </div>
    
    <h2>📝 Recomendações para Refatoração</h2>
    <div class="details">
        <h3>🔧 Ações Prioritárias:</h3>
        <ol>
            <li><strong>Implementar métodos ausentes:</strong> add_habit, get_active_habits, etc.</li>
            <li><strong>Corrigir imports:</strong> ReportFactory, ReportController</li>
            <li><strong>Implementar fixtures:</strong> clean_json_files, mock_datetime</li>
            <li><strong>Completar HabitModel:</strong> Métodos abstratos e concertos</li>
            <li><strong>Estrutura de dados:</strong> Padronizar formato de hábitos</li>
        </ol>
        
        <h3>📋 Próximos Passos:</h3>
        <ul>
            <li>Revisar arquivos de log detalhados para cada erro específico</li>
            <li>Implementar métodos faltantes um por vez</li>
            <li>Executar testes individuais após cada correção</li>
            <li>Implementar testes de integração após correções básicas</li>
        </ul>
    </div>
    
    <footer>
        <hr>
        <p><small>Relatório gerado automaticamente em {datetime.now()}</small></p>
    </footer>
</body>
</html>
    """
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

def analyze_common_issues(results):
    """Analisar problemas comuns nos testes"""
    issues = {
        'Import Errors': [],
        'Method Not Found': [],
        'Fixture Errors': [],
        'Syntax Errors': [],
        'Warnings': []
    }
    
    for test_file, result in results.items():
        if 'stdout' in result and 'stderr' in result:
            output = result['stdout'] + result['stderr']
            
            if 'ModuleNotFoundError' in output or 'ImportError' in output:
                issues['Import Errors'].append(f"{test_file}: Problemas de import detectados")
            
            if 'AttributeError' in output:
                issues['Method Not Found'].append(f"{test_file}: Métodos/atributos não encontrados")
            
            if 'fixture' in output.lower() and 'error' in output.lower():
                issues['Fixture Errors'].append(f"{test_file}: Problemas com fixtures")
            
            if 'SyntaxError' in output:
                issues['Syntax Errors'].append(f"{test_file}: Erros de sintaxe")
            
            if 'warning' in output.lower():
                warning_count = output.lower().count('warning')
                issues['Warnings'].append(f"{test_file}: {warning_count} warning(s)")
    
    return issues

if __name__ == "__main__":
    run_test_suite()