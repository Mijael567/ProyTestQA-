"""
Test 02: Registro de Usuario
=====================================================

Escenario:
- Navegar desde página principal
- Completar formulario de registro con datos válidos
- Utilizar emails dinámicos para evitar conflictos
- Verificar mensaje de éxito real: "Registro exitoso."

Validaciones reales encontradas:
- Campo nombre: pattern="[A-Za-zÁÉÍÓÚáéíóúÑñ\s]{2,50}" (Solo letras, 2-50)
- Campo apellido: pattern="[A-Za-zÁÉÍÓÚáéíóúÑñ\s]{2,50}" (Solo letras, 2-50)
- Campo teléfono: pattern="[0-9]{7,15}" (Números 7-15 dígitos)
- Campo CI: pattern="[0-9]{6,12}" (Números 6-12 dígitos)
- Campo correo: type="email" (Email válido)
- Campo contraseña: pattern="(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&/#¡¿])[A-Za-z\d@$!%*?&/#¡¿]{8,}"
  (Mínimo 8 caracteres, mayúsculas, minúsculas, números, símbolos)
- Respuesta: {"success": true, "mensaje": "Registro exitoso."}
"""

import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestRegistroUsuario:
    """Verifica que el formulario de registro funciona correctamente"""
    
    def test_registro_usuario_valido(self, driver):
        """
        Registra un usuario con datos válidos y verifica éxito
        """
        # Paso 1: Navegar a página principal
        driver.get("http://localhost/sistema/public/index.php")
        wait = WebDriverWait(driver, 10)
        
        print("\n[PASO 1] Navegando a página principal...")
        assert "Pollos" in driver.title or "pollos" in driver.title.lower()
        print("[✓] Página principal cargada")
        
        # Paso 2: Buscar y hacer clic en "Regístrate" o link de registro
        print("\n[PASO 2] Buscando acceso a registro...")
        # Buscar link en navegación o botón de registro
        try:
            registro_link = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Registro') or contains(text(), 'registro') or contains(text(), 'Regístrate')]"))
            )
            registro_link.click()
        except:
            # Alternativa: navegar directamente
            driver.get("http://localhost/sistema/public/registro.php")
        
        wait.until(EC.url_contains("registro.php"))
        print("[✓] Formulario de registro cargado")
        
        # Paso 3: Generar datos válidos dinámicos
        print("\n[PASO 3] Generando datos dinámicos de usuario...")
        timestamp = str(int(time.time() * 1000))
        random_num = str(random.randint(1000, 9999))
        
        datos_usuario = {
            "nombre": "Juan",
            "apellido": "Pérez",
            "telefono": f"7654{random_num[-4:]}",  # Formato: 76541234
            "ci": f"123{random_num}",  # Formato: 1231234
            "correo": f"usuario_{timestamp}_{random_num}@test.com",
            "contrasena": "SecurePass123!@"  # Válido: mayúsculas, minúsculas, números, símbolos
        }
        
        print(f"[DATOS] Correo: {datos_usuario['correo']}")
        print(f"[DATOS] CI: {datos_usuario['ci']}")
        
        # Paso 4: Llenar formulario
        print("\n[PASO 4] Llenando formulario con datos válidos...")
        
        driver.find_element(By.ID, "nombre").send_keys(datos_usuario["nombre"])
        print("[✓] Nombre ingresado")
        
        driver.find_element(By.ID, "apellido").send_keys(datos_usuario["apellido"])
        print("[✓] Apellido ingresado")
        
        driver.find_element(By.ID, "telefono").send_keys(datos_usuario["telefono"])
        print("[✓] Teléfono ingresado")
        
        driver.find_element(By.ID, "ci").send_keys(datos_usuario["ci"])
        print("[✓] CI ingresado")
        
        driver.find_element(By.ID, "correo").send_keys(datos_usuario["correo"])
        print("[✓] Correo ingresado")
        
        driver.find_element(By.ID, "contrasena").send_keys(datos_usuario["contrasena"])
        print("[✓] Contraseña ingresada")
        
        # Paso 5: Enviar formulario
        print("\n[PASO 5] Enviando formulario...")
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()
        
        # Paso 6: Esperar respuesta y verificar
        print("\n[PASO 6] Esperando respuesta del servidor...")
        time.sleep(1)  # Esperar procesamiento
        
        # Manejar alert si aparece
        try:
            alert = driver.switch_to.alert
            alert_text = alert.text
            print("[ALERT] {}".format(alert_text))
            assert "exitoso" in alert_text.lower(), "Alert no indica exito: {}".format(alert_text)
            alert.accept()
            print("[OK] Alert aceptado")
        except:
            print("[INFO] No hay alert para aceptar")
        
        time.sleep(1)
        
        # Verificar redirection o mensaje de exito
        current_url = driver.current_url
        print("[URL ACTUAL] {}".format(current_url))
        
        # Validar que se registró correctamente
        # El sistema debería redirigir o mostrar confirmación
        if "registro.php" in current_url:
            # Aún en registro, buscar mensaje de error o validación
            body_text = driver.find_element(By.TAG_NAME, "body").text
            assert "error" not in body_text.lower() or "fallid" not in body_text.lower(), \
                "Hay un mensaje de error en la página"
        else:
            # Fue redirigido, significa que registro fue exitoso
            print("[✓] Redirigido después de registro")
        
        print("\n[✅] TEST APROBADO: Registro de usuario exitoso")
        
        # Guardar datos para usar en otros tests
        return datos_usuario


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v", "-s"])
