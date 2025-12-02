#!/usr/bin/env python3
import os
import sys
import platform
import subprocess

def main():
    # Detectar sistema operacional
    sistema = platform.system()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    os.chdir(project_root)
    
    print(f"[Diretório]: {os.getcwd()}")
    
    # Definir comandos baseado no SO
    if sistema == "Windows":
        python_cmd = "python3"
    else:  # Linux, macOS, etc.
        python_cmd = "python"
    
    # Lista de comandos a executar
    comandos = [
        f"{python_cmd} tests/test_habit_crud.py",
        f"{python_cmd} tests/test_habit_visualization.py -v -s",
        f"{python_cmd} tests/test_report_generation.py -v -s"
    ]
    
    # Executar cada comando em sequência
    resultados = []
    
    for i, comando in enumerate(comandos, 1):
        print(f"\n")
        print(f"[{i}/{len(comandos)}] Executando: {comando}")
        
        try:
            # Executar comando
            resultado = subprocess.run(
                comando,
                shell=True,
                cwd=project_root,
                capture_output=False,  # Mostrar output em tempo real
                text=True
            )
            
            # Armazenar código de saída
            resultados.append({
                'comando': comando,
                'sucesso': resultado.returncode == 0,
                'codigo': resultado.returncode
            })
            
            if resultado.returncode == 0:
                print(f"\n✅ Teste {i} concluído com SUCESSO")
            else:
                print(f"\n❌ Teste {i} FALHOU (código: {resultado.returncode})")
                
        except Exception as e:
            print(f"\n💥 ERRO ao executar comando: {e}")
            resultados.append({
                'comando': comando,
                'sucesso': False,
                'codigo': -1
            })
    
    # Resumo final
    print("\n")
    print("[RESUMO DA EXECUÇÃO]")
    
    total = len(resultados)
    sucessos = sum(1 for r in resultados if r['sucesso'])
    falhas = total - sucessos
    
    for i, resultado in enumerate(resultados, 1):
        icone = "✅" if resultado['sucesso'] else "❌"
        status = "PASSOU" if resultado['sucesso'] else "FALHOU"
        print(f"{icone} Teste {i}: {status}")
        print(f"   Comando: {resultado['comando']}")
        print(f"   Código: {resultado['codigo']}")
        print()
    
    print("-"*80)
    print(f"📊 Total: {total} | ✅ Sucessos: {sucessos} | ❌ Falhas: {falhas}")
    print("="*80)
    
    # Código de saída
    return 0 if falhas == 0 else 1


if __name__ == "__main__":
    try:
        codigo_saida = main()
        sys.exit(codigo_saida)
    except Exception as e:
        print(f"\n\n[ERRO INESPERADO]: {e}")
        sys.exit(1)