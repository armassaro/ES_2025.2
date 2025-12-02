import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path

def run_test_suite():
    """
    Script para executar todos os testes do HabitTracker e gerar relatórios
    """
    print("🚀 Iniciando execução completa da suíte de testes HabitTracker")
    print("=" * 80)
    
    # Detectar e ajustar diretório correto
    current_dir = Path.cwd()
    if current_dir.name == 'tests':
        # Está em tests/, subir para HabitTracker
        project_root = current_dir.parent
        os.chdir(project_root)
        print(f"📂 Detectado em tests/, mudando para: {project_root}")
    else:
        project_root = current_dir
        print(f"📂 Já está na raiz: {project_root}")
    
    print(f"📂 Diretório de trabalho atual: {os.getcwd()}")
    
    # Configurações - salvar em tests/test_reports/
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    reports_dir = "tests/test_reports"
    
    # Criar diretório de relatórios se não existir
    os.makedirs(reports_dir, exist_ok=True)
    
    # Lista de todos os arquivos de teste
    test_files = [
        "tests/test_habit_crud.py",
        "tests/test_habit_visualization.py",
        "tests/test_report_generation.py"
    ]
    
    # Verificar se os arquivos de teste existem
    print("\n🔍 Verificando arquivos de teste...")
    missing_files = []
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"   ✅ {test_file}")
        else:
            print(f"   ❌ {test_file} - ARQUIVO NÃO ENCONTRADO!")
            missing_files.append(test_file)
    
    if missing_files:
        print(f"\n⚠️  ATENÇÃO: {len(missing_files)} arquivo(s) não encontrado(s)!")
        print("   Continuando com os arquivos disponíveis...\n")
    
    print(f"\n📁 Relatórios serão salvos em: {reports_dir}/")
    print(f"🕐 Timestamp: {timestamp}")
    print("-" * 80)
    
    # Executar cada arquivo de teste individualmente
    available_tests = [f for f in test_files if os.path.exists(f)]
    
    total_passed = 0
    total_failed = 0
    
    for i, test_file in enumerate(available_tests, 1):
        print(f"\n{'='*80}")
        print(f"📋 [{i}/{len(available_tests)}] Executando: {test_file}")
        print(f"{'='*80}")
        
        # Nome do arquivo de relatório
        test_name = os.path.basename(test_file).replace('.py', '')
        report_file = f"{reports_dir}/{test_name}_{timestamp}.txt"
        
        try:
            # Executar pytest
            cmd = [
                sys.executable, "-m", "pytest", 
                test_file, 
                "-v", "-s", 
                "--tb=short",
                "--capture=no"
            ]
            
            print(f"⏱️  Iniciado em: {datetime.now().strftime('%H:%M:%S')}")
            
            # Executar e capturar saída
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                encoding='utf-8',
                errors='replace',
                timeout=300
            )
            
            # Combinar stdout e stderr
            full_output = ""
            if result.stdout:
                full_output += result.stdout
            if result.stderr:
                full_output += "\n" + result.stderr
            
            # Mostrar no console
            print(full_output)
            
            # Salvar APENAS o log real em arquivo
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(full_output)
            
            # Contar resultados
            if result.returncode == 0:
                total_passed += 1
                print(f"✅ SUCESSO")
            else:
                total_failed += 1
                print(f"❌ FALHOU")
            
            print(f"💾 Log salvo em: {report_file}")
            print(f"⏱️  Finalizado em: {datetime.now().strftime('%H:%M:%S')}")
                
        except subprocess.TimeoutExpired:
            print(f"\n⏰ TIMEOUT - Teste demorou mais de 5 minutos")
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(f"TIMEOUT ERROR - Teste demorou mais de 5 minutos\n")
            total_failed += 1
            
        except Exception as e:
            print(f"\n💥 ERRO DE EXECUÇÃO: {str(e)}")
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(f"EXECUTION ERROR: {str(e)}\n")
            total_failed += 1
    
    # Executar TODOS os testes juntos
    print(f"\n{'='*80}")
    print(f"📋 [FINAL] Executando todos os testes combinados...")
    print(f"{'='*80}")
    
    all_tests_report = f"{reports_dir}/all_tests_combined_{timestamp}.txt"
    
    try:
        cmd_all = [
            sys.executable, "-m", "pytest", 
            "tests/",
            "-v", "-s", 
            "--tb=short"
        ]
        
        print(f"⏱️  Iniciado em: {datetime.now().strftime('%H:%M:%S')}")
        
        result_all = subprocess.run(
            cmd_all,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=600
        )
        
        # Combinar saída
        full_output = ""
        if result_all.stdout:
            full_output += result_all.stdout
        if result_all.stderr:
            full_output += "\n" + result_all.stderr
        
        # Mostrar no console
        print(full_output)
        
        # Salvar em arquivo
        with open(all_tests_report, 'w', encoding='utf-8') as f:
            f.write(full_output)
        
        print(f"💾 Log combinado salvo em: {all_tests_report}")
        print(f"⏱️  Finalizado em: {datetime.now().strftime('%H:%M:%S')}")
        
    except Exception as e:
        print(f"💥 Erro ao executar todos os testes: {e}")
    
    # Resumo final simples
    print("\n" + "=" * 80)
    print("🏁 EXECUÇÃO COMPLETA!")
    print("=" * 80)
    print(f"✅ Passou: {total_passed}")
    print(f"❌ Falhou: {total_failed}")
    print(f"\n📄 Todos os logs salvos em: {reports_dir}/")
    print("=" * 80)

if __name__ == "__main__":
    run_test_suite()