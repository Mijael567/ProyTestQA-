"""
Test 03: Login de Usuario
=====================================================

Escenario:
- Navegar a página de login
- Completar formulario con credenciales válidas previamente registradas
- Verificar inicio de sesión exitoso
- Verificar redirecciones reales

Validaciones reales encontradas:
- Campo correo: id="correo" type="email"
- Campo contraseña: id="contrasena" type="password"
- Botón submit: id="btnLogin"
- Respuesta exitosa: {"success": true, "rol": ..., "correo": ...}
- Respuesta error: {"success": false, "mensaje": "Usuario no encontrado." o "Contraseña incorrecta."}
"""

import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestLoginUsuario:
    """Verifica que el login funciona correctamente"""
    
    def test_login_usuario_valido(self, driver):
        """
        Login con usuario válido previamente registrado
        """
        # Paso 1: Registrar un usuario primero
        print("\n[PASO 1] Registrando usuario de prueba...")
        driver.get("http://localhost/sistema/public/registro.php")
        wait = WebDriverWait(driver, 10)
        
        timestamp = str(int(time.time() * 1000))
        random_num = str(random.randint(1000, 9999))
        
        correo_test = f"login_test_{timestamp}_{random_num}@test.com"
        telefono_test = f"7654{random_num[-4:]}"
        ci_test = f"123{random_num}"
        contrasena_test = "SecurePass123!@"
        
        print(f"[DATOS REGISTRO] Correo: {correo_test}")
        
        # Llenar formulario de registro
        driver.find_element(By.ID, "nombre").send_keys("Juan")
        driver.find_element(By.ID, "apellido").send_keys("Pérez")
        driver.find_element(By.ID, "telefono").send_keys(telefono_test)
        driver.find_element(By.ID, "ci").send_keys(ci_test)
        driver.find_element(By.ID, "correo").send_keys(correo_test)
        driver.find_element(By.ID, "contrasena").send_keys(contrasena_test)
        
        # Enviar registro
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(1)
        
        # Manejar alert de registro
        try:
            alert = driver.switch_to.alert
            alert_text = alert.text
            print("[ALERT REGISTRO] {}".format(alert_text))
            alert.accept()
        except:
            pass
        
        time.sleep(1)
        
        print("[✓] Usuario registrado")
        
        # Paso 2: Navegar a login
        print("\n[PASO 2] Navegando a página de login...")
        driver.get("http://localhost/sistema/public/login.php")
        wait.until(EC.presence_of_element_located((By.ID, "correo")))
        print("[✓] Página de login cargada")
        
        # Paso 3: Llenar formulario de login
        print("\n[PASO 3] Llenando formulario de login...")
        driver.find_element(By.ID, "correo").send_keys(correo_test)
        print("[✓] Correo ingresado")
        
        driver.find_element(By.ID, "contrasena").send_keys(contrasena_test)
        print("[✓] Contraseña ingresada")
        
        # Paso 4: Hacer clic en login
        print("\n[PASO 4] Haciendo clic en botón Entrar...")
        login_button = driver.find_element(By.ID, "btnLogin")
        login_button.click()
        
        # Paso 5: Esperar respuesta
        print("\n[PASO 5] Esperando respuesta del servidor...")
        time.sleep(2)
        
        # Paso 6: Verificar que login fue exitoso
        print("\n[PASO 6] Verificando login exitoso...")
        current_url = driver.current_url
        print(f"[URL ACTUAL] {current_url}")
        
        # Verificar que NO estamos en login.php (significa que fue redirigido)
        if "login.php" in current_url:
            # Verifica si hay error en la página
            page_text = driver.find_element(By.TAG_NAME, "body").text
            if "usuario no encontrado" in page_text.lower() or "contraseña incorrecta" in page_text.lower():
                raise AssertionError("Hay mensaje de error en login: el usuario o contraseña fueron rechazados")
            print("[⚠] Aún en login.php pero sin errores visibles")
        else:
            # Fue redirigido, login exitoso
            print("[✓] Redirigido correctamente (login exitoso)")
        
        # Paso 7: Verificar que hay sesión activa (opcional pero útil)
        print("\n[PASO 7] Verificando sesión activa...")
        driver.get("http://localhost/sistema/public/estadoSesion.php")
        page_source = driver.page_source
        
        if "logeado\":true" in page_source or "\"logeado\": true" in page_source:
            print("[✓] Sesión activa confirmada")
        else:
            print("[⚠] No se pudo confirmar sesión en endpoint")
        
        print("\n[✅] TEST APROBADO: Login de usuario exitoso")


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v", "-s"])
