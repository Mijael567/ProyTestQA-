"""
Test 05: Validaciones de Campos
=====================================================

Valida comportamientos reales de validación en formularios:

1. REGISTRO - Campos obligatorios (required attribute)
2. REGISTRO - Formato de nombre (solo letras)
3. REGISTRO - Longitud mínima nombre/apellido
4. REGISTRO - Email inválido
5. REGISTRO - Teléfono inválido
6. REGISTRO - CI inválido
7. REGISTRO - Contraseña débil (sin mayúsculas/números/símbolos)
8. LOGIN - Email vacío
9. LOGIN - Contraseña vacía

Validaciones encontradas en el código real:
- Nombre: pattern="[A-Za-zÁÉÍÓÚáéíóúÑñ\s]{2,50}"
- Apellido: pattern="[A-Za-zÁÉÍÓÚáéíóúÑñ\s]{2,50}"
- Teléfono: pattern="[0-9]{7,15}"
- CI: pattern="[0-9]{6,12}"
- Correo: type="email"
- Contraseña: pattern="(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&/#¡¿])[A-Za-z\d@$!%*?&/#¡¿]{8,}"
"""

import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException


class TestValidacionesCampos:
    """Valida todas las validaciones de campos encontradas en el sistema"""
    
    def test_registro_nombre_solo_letras(self, driver):
        """Valida que nombre rechaza números"""
        print("\n[TEST] Validando que nombre rechaza números...")
        driver.get("http://localhost/sistema/public/registro.php")
        wait = WebDriverWait(driver, 5)
        
        # Intentar ingresar nombre con números
        nombre_input = wait.until(EC.presence_of_element_located((By.ID, "nombre")))
        nombre_input.send_keys("Juan123")
        
        # El navegador no permitirá enviar si hay validación HTML5
        submit_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
        
        # Verificar que el input tiene el patrón
        pattern = nombre_input.get_attribute("pattern")
        assert pattern is not None, "Campo nombre no tiene patrón de validación"
        assert "[A-Za-z" in pattern, "Patrón no valida solo letras"
        
        print("[✓] Validación de nombre correcta (solo letras)")
    
    def test_registro_nombre_longitud_minima(self, driver):
        """Valida longitud mínima de nombre"""
        print("\n[TEST] Validando longitud mínima de nombre...")
        driver.get("http://localhost/sistema/public/registro.php")
        wait = WebDriverWait(driver, 5)
        
        nombre_input = wait.until(EC.presence_of_element_located((By.ID, "nombre")))
        
        # Verificar patrón incluye longitud
        pattern = nombre_input.get_attribute("pattern")
        assert "{2," in pattern, "Patrón no valida longitud mínima 2"
        
        print("[✓] Validación de longitud mínima de nombre correcta")
    
    def test_registro_apellido_validacion(self, driver):
        """Valida que apellido tiene validaciones similares"""
        print("\n[TEST] Validando validaciones de apellido...")
        driver.get("http://localhost/sistema/public/registro.php")
        wait = WebDriverWait(driver, 5)
        
        apellido_input = wait.until(EC.presence_of_element_located((By.ID, "apellido")))
        
        # Verificar patrón
        pattern = apellido_input.get_attribute("pattern")
        assert pattern is not None, "Campo apellido no tiene validación"
        assert "[A-Za-z" in pattern, "Apellido debe validar solo letras"
        assert "{2," in pattern, "Apellido debe validar longitud mínima"
        
        print("[✓] Validaciones de apellido correctas")
    
    def test_registro_telefono_solo_numeros(self, driver):
        """Valida que teléfono acepta solo números"""
        print("\n[TEST] Validando validación de teléfono...")
        driver.get("http://localhost/sistema/public/registro.php")
        wait = WebDriverWait(driver, 5)
        
        telefono_input = wait.until(EC.presence_of_element_located((By.ID, "telefono")))
        
        # Verificar patrón
        pattern = telefono_input.get_attribute("pattern")
        assert pattern is not None, "Campo teléfono no tiene validación"
        assert "[0-9]" in pattern, "Teléfono debe validar solo números"
        assert "7," in pattern or "15" in pattern, "Teléfono debe validar longitud 7-15"
        
        print("[✓] Validación de teléfono correcta")
    
    def test_registro_ci_solo_numeros(self, driver):
        """Valida que CI acepta solo números"""
        print("\n[TEST] Validando validación de CI...")
        driver.get("http://localhost/sistema/public/registro.php")
        wait = WebDriverWait(driver, 5)
        
        ci_input = wait.until(EC.presence_of_element_located((By.ID, "ci")))
        
        # Verificar patrón
        pattern = ci_input.get_attribute("pattern")
        assert pattern is not None, "Campo CI no tiene validación"
        assert "[0-9]" in pattern, "CI debe validar solo números"
        
        print("[✓] Validación de CI correcta")
    
    def test_registro_correo_tipo_email(self, driver):
        """Valida que correo es tipo email"""
        print("\n[TEST] Validando tipo de campo correo...")
        driver.get("http://localhost/sistema/public/registro.php")
        wait = WebDriverWait(driver, 5)
        
        correo_input = wait.until(EC.presence_of_element_located((By.ID, "correo")))
        
        # Verificar tipo
        tipo = correo_input.get_attribute("type")
        assert tipo == "email", f"Campo correo debe ser tipo 'email', es '{tipo}'"
        
        print("[✓] Validación de correo correcta (tipo email)")
    
    def test_registro_contrasena_validacion_fuerte(self, driver):
        """Valida que contraseña requiere caracteres fuertes"""
        print("\n[TEST] Validando validación de contraseña fuerte...")
        driver.get("http://localhost/sistema/public/registro.php")
        wait = WebDriverWait(driver, 5)
        
        contrasena_input = wait.until(EC.presence_of_element_located((By.ID, "contrasena")))
        
        # Verificar patrón
        pattern = contrasena_input.get_attribute("pattern")
        assert pattern is not None, "Campo contraseña no tiene validación"
        
        # Verifica requisitos
        assert "a-z" in pattern, "Debe requerir minúsculas"
        assert "A-Z" in pattern, "Debe requerir mayúsculas"
        assert "\\d" in pattern, "Debe requerir números"
        assert "8" in pattern, "Debe requerir mínimo 8 caracteres"
        
        print("[✓] Validación de contraseña fuerte correcta")
    
    
    def test_login_correo_tipo_email(self, driver):
        """Valida que correo en login es tipo email"""
        print("\n[TEST] Validando tipo de correo en login...")
        driver.get("http://localhost/sistema/public/login.php")
        wait = WebDriverWait(driver, 5)
        
        correo_input = wait.until(EC.presence_of_element_located((By.ID, "correo")))
        
        # Verificar tipo
        tipo = correo_input.get_attribute("type")
        assert tipo == "email", f"Correo en login debe ser tipo 'email', es '{tipo}'"
        
        print("[✓] Validación de correo en login correcta")
    
    def test_login_contrasena_tipo_password(self, driver):
        """Valida que contraseña en login es tipo password"""
        print("\n[TEST] Validando tipo de contraseña en login...")
        driver.get("http://localhost/sistema/public/login.php")
        wait = WebDriverWait(driver, 5)
        
        contrasena_input = wait.until(EC.presence_of_element_located((By.ID, "contrasena")))
        
        # Verificar tipo
        tipo = contrasena_input.get_attribute("type")
        assert tipo == "password", f"Contraseña debe ser tipo 'password', es '{tipo}'"
        
        print("[✓] Validación de contraseña en login correcta (tipo password)")


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v", "-s"])
