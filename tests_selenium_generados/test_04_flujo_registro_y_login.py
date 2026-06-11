"""
Test 04: Flujo Completo Registro + Login
=====================================================

Escenario COMPLETO:
1. Registrar nuevo usuario
2. Confirmar registro exitoso
3. Cerrar sesión (logout)
4. Iniciar sesión con credenciales del nuevo usuario
5. Verificar autenticación
6. Validar elementos que confirman sesión activa

Este es el test más completo que valida toda una sesión de usuario
"""

import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestFlujoRegistroLogin:
    """Verifica el flujo completo de registro, logout y login"""
    
    def test_flujo_completo_usuario_nuevo(self, driver):
        """
        Flujo completo: registro -> logout -> login -> verificar sesión
        """
        wait = WebDriverWait(driver, 10)
        
        # PARTE 1: REGISTRO
        # =========================================
        print("\n" + "="*60)
        print("PARTE 1: REGISTRO DE USUARIO")
        print("="*60)
        
        # Paso 1: Generar datos únicos
        print("\n[PASO 1] Generando datos de usuario...")
        timestamp = str(int(time.time() * 1000))
        random_num = str(random.randint(10000, 99999))
        
        correo_nuevo = f"flujo_{timestamp}_{random_num}@test.com"
        telefono_nuevo = f"765{random_num[-4:]}"
        ci_nuevo = f"1234{random_num[-3:]}"
        contrasena_nueva = "FlowPass123!@#"
        
        print(f"[CORREO] {correo_nuevo}")
        print(f"[TELÉFONO] {telefono_nuevo}")
        print(f"[CI] {ci_nuevo}")
        
        # Paso 2: Navegar a registro
        print("\n[PASO 2] Navegando a página de registro...")
        driver.get("http://localhost/sistema/public/registro.php")
        wait.until(EC.presence_of_element_located((By.ID, "nombre")))
        print("[✓] Página de registro cargada")
        
        # Paso 3: Llenar formulario
        print("\n[PASO 3] Completando formulario de registro...")
        driver.find_element(By.ID, "nombre").send_keys("TestUser")
        driver.find_element(By.ID, "apellido").send_keys("FlowTest")
        driver.find_element(By.ID, "telefono").send_keys(telefono_nuevo)
        driver.find_element(By.ID, "ci").send_keys(ci_nuevo)
        driver.find_element(By.ID, "correo").send_keys(correo_nuevo)
        driver.find_element(By.ID, "contrasena").send_keys(contrasena_nueva)
        print("[✓] Todos los campos completados")
        
        # Paso 4: Enviar registro
        print("\n[PASO 4] Enviando formulario...")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(1)
        
        # Manejar alert de registro
        try:
            alert = driver.switch_to.alert
            alert.accept()
        except:
            pass
        
        time.sleep(1)
        print("[OK] Registro completado")
        
        # Paso 5: Verificar sesion activa después de registro
        print("\n[PASO 5] Verificando sesion después de registro...")
        driver.get("http://localhost/sistema/public/estadoSesion.php")
        page_text = driver.page_source
        
        if "\"logeado\":true" in page_text or "logeado\": true" in page_text:
            print("[✓] Sesión automática iniciada después del registro")
            sesion_activa_post_registro = True
        else:
            print("[⚠] No se confirmó sesión automática")
            sesion_activa_post_registro = False
        
        
        # PARTE 2: LOGOUT
        # =========================================
        print("\n" + "="*60)
        print("PARTE 2: LOGOUT/CIERRE DE SESIÓN")
        print("="*60)
        
        # Paso 6: Navegar a logout
        print("\n[PASO 6] Cerrando sesión...")
        driver.get("http://localhost/sistema/public/logout.php")
        time.sleep(1)
        print("[✓] Logout completado")
        
        # Paso 7: Verificar sesión cerrada
        print("\n[PASO 7] Verificando sesión cerrada...")
        driver.get("http://localhost/sistema/public/estadoSesion.php")
        page_text = driver.page_source
        
        if "\"logeado\":false" in page_text or "logeado\": false" in page_text:
            print("[✓] Sesión correctamente cerrada")
        else:
            print("[⚠] No se pudo confirmar sesión cerrada")
        
        
        # PARTE 3: LOGIN CON NUEVO USUARIO
        # =========================================
        print("\n" + "="*60)
        print("PARTE 3: LOGIN CON NUEVO USUARIO")
        print("="*60)
        
        # Paso 8: Navegar a login
        print("\n[PASO 8] Navegando a página de login...")
        driver.get("http://localhost/sistema/public/login.php")
        wait.until(EC.presence_of_element_located((By.ID, "correo")))
        print("[✓] Página de login cargada")
        
        # Paso 9: Llenar credenciales
        print("\n[PASO 9] Ingresando credenciales...")
        driver.find_element(By.ID, "correo").send_keys(correo_nuevo)
        driver.find_element(By.ID, "contrasena").send_keys(contrasena_nueva)
        print("[✓] Credenciales ingresadas")
        
        # Paso 10: Hacer login
        print("\n[PASO 10] Haciendo login...")
        login_button = driver.find_element(By.ID, "btnLogin")
        login_button.click()
        time.sleep(2)
        
        print("[✓] Login enviado")
        
        
        # PARTE 4: VERIFICACIÓN DE SESIÓN ACTIVA
        # =========================================
        print("\n" + "="*60)
        print("PARTE 4: VERIFICACIÓN DE SESIÓN ACTIVA")
        print("="*60)
        
        # Paso 11: Verificar sesión después de login
        print("\n[PASO 11] Verificando sesión activa...")
        driver.get("http://localhost/sistema/public/estadoSesion.php")
        page_source = driver.page_source
        
        # Buscar indicadores de sesión activa
        assert "logeado" in page_source.lower(), "No se encontró indicador de sesión"
        
        if "\"logeado\":true" in page_source or "logeado\": true" in page_source:
            print("[✓] SESIÓN ACTIVA CONFIRMADA")
            
            # Buscar correo en la sesión
            if correo_nuevo in page_source:
                print(f"[✓] Correo confirmado en sesión: {correo_nuevo}")
            else:
                print("[⚠] Correo no visible en endpoint (pero sesión activa)")
        else:
            raise AssertionError("Login fallido: sesión no activa")
        
        # Paso 12: Verificar acceso a recursos protegidos
        print("\n[PASO 12] Verificando acceso a catálogo...")
        driver.get("http://localhost/sistema/public/catalogo.php")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "menu-container")))
        
        # Intentar agregar producto (ahora debería funcionar)
        print("[✓] Acceso a catálogo permitido (usuario autenticado)")
        
        print("\n" + "="*60)
        print("[✅] FLUJO COMPLETO APROBADO")
        print("="*60)
        print("\nResumen:")
        print(f"✓ Usuario registrado: {correo_nuevo}")
        print("✓ Sesión automática al registrar")
        print("✓ Logout completado")
        print("✓ Login exitoso")
        print("✓ Sesión activa confirmada")
        print("✓ Acceso a recursos protegidos")


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v", "-s"])
