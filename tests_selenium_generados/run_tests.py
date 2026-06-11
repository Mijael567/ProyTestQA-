#!/usr/bin/env python
"""
run_tests.py - Script para ejecutar la suite de tests

Uso:
    python run_tests.py                    # Ejecuta todos los tests
    python run_tests.py --test 01          # Ejecuta test 01
    python run_tests.py --html             # Genera reporte HTML
    python run_tests.py --verbose          # Modo verbose
"""

import subprocess
import sys
import argparse
import os

def run_tests(test_num=None, html=False, verbose=True):
    """Ejecuta los tests con pytest"""
    
    cmd = [sys.executable, "-m", "pytest"]
    
    if test_num:
        # Test específico
        test_file = f"test_0{test_num}_*.py"
        cmd.append(test_file)
        print(f"Ejecutando test 0{test_num}...")
    else:
        # Todos los tests
        cmd.append("tests_selenium_generados/")
        print("Ejecutando TODOS los tests...")
    
    if verbose:
        cmd.append("-v")
        cmd.append("-s")
    
    if html:
        cmd.append("--html=report.html")
        cmd.append("--self-contained-html")
        print("Generando reporte HTML...")
    
    cmd.append("--tb=short")
    
    # Ejecutar
    print(f"\nComando: {' '.join(cmd)}\n")
    result = subprocess.run(cmd, cwd=os.path.dirname(__file__) or ".")
    
    return result.returncode

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ejecutor de tests Selenium - Pollos Express")
    parser.add_argument("--test", type=int, help="Número de test específico (1-5)")
    parser.add_argument("--html", action="store_true", help="Generar reporte HTML")
    parser.add_argument("--verbose", action="store_true", default=True, help="Modo verbose")
    
    args = parser.parse_args()
    
    exit_code = run_tests(test_num=args.test, html=args.html, verbose=args.verbose)
    sys.exit(exit_code)
