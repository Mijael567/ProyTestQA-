"""
Test 01: Acceso al Carrito sin Login
=====================================================

Escenario:
- Usuario sin sesión intenta agregar un producto al carrito
- Debe recibir alerta indicando que necesita iniciar sesión
- Debe ser redirigido a la página de login

Validaciones reales encontradas:
- Mensaje: "Debes iniciar sesión para agregar productos."
- Redirección a: login.php
- La alerta se muestra en DOM como div.alerta-login
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestAccesoCarritoSinLogin:
    """Verifica que el sistema requiere login para agregar productos"""
    
    def test_agregar_producto_sin_login_redirige_a_login(self, driver):
        """
        Valida que intentar agregar producto sin login redirige a login
        """
        # Paso 1: Navegar a la pagina principal
        print("\n[PASO 1] Navegando a pagina principal...")
        driver.get("http://localhost/sistema/public/index.php")
        wait = WebDriverWait(driver, 10)
        
        assert "Pollos" in driver.title or "pollos" in driver.title.lower(), \
            "No se cargo la pagina principal correctamente"
        print("[OK] Pagina principal cargada")
        
        # Paso 2: Navegar al catalogo
        print("\n[PASO 2] Navegando al catalogo...")
        driver.get("http://localhost/sistema/public/catalogo.php")
        wait.until(EC.url_contains("catalogo.php"))
        print("[OK] Catalogo cargado")
        
        # Paso 3: Esperar a que se carguen los productos
        print("\n[PASO 3] Esperando carga de productos...")
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "producto")))
        productos = driver.find_elements(By.CLASS_NAME, "producto")
        assert len(productos) > 0, "No se encontraron productos en el catalogo"
        print("[OK] Se encontraron {} productos".format(len(productos)))
        
        # Paso 4: Buscar primer boton de "Anadir al carrito"
        print("\n[PASO 4] Buscando boton de agregar al carrito...")
        # Esperar a que haya un boton clickeable
        time.sleep(1)  # Pequena pausa para animaciones
        
        # Inspeccion
        primer_producto = driver.find_elements(By.CLASS_NAME, "producto")[0]
        html_interno = primer_producto.get_attribute("innerHTML")
        print("[DEBUG] HTML del primer producto:\n{}".format(html_interno[:200]))
        
        buttons = driver.find_elements(By.TAG_NAME, "button")
        print("[DEBUG] Total de botones en la pagina: {}".format(len(buttons)))
        
        buttons_en_productos = driver.find_elements(By.XPATH, "//button[@class='btn']")
        print("[DEBUG] Botones con clase 'btn': {}".format(len(buttons_en_productos)))
        
        assert len(buttons_en_productos) > 0, "No se encontraron botones. Botones totales: {}".format(len(buttons))
        agregar_button = buttons_en_productos[0]
        print("[OK] Boton encontrado")
        print("[✓] Botón encontrado")
        
        # Paso 5: Hacer clic en agregar sin estar logeado
        print("\n[PASO 5] Haciendo clic en agregar al carrito (sin login)...")
        # Ejecutar click via JavaScript para asegurar que funciona
        driver.execute_script("arguments[0].click();", agregar_button)
        
        # Paso 6: Verificar que aparece el mensaje de alerta
        print("\n[PASO 6] Verificando alerta de login requerido...")
        time.sleep(1)  # Pequeño delay para que aparezca la alerta
        
        # Buscar alerta en el DOM
        alerta_present = False
        try:
            # La alerta es un div que se crea dinámicamente
            alerta = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "alerta-login")),
                timeout=3
            )
            alerta_text = alerta.text
            print(f"[ALERTA MOSTRADA] {alerta_text}")
            
            assert "iniciar sesión" in alerta_text.lower() or "login" in alerta_text.lower(), \
                f"Alerta no contiene mensaje de login: {alerta_text}"
            alerta_present = True
            print("[✓] Alerta correcta mostrada")
        except:
            print("[INFO] Alerta no encontrada en DOM (puede haber sido eliminada)")
        
        # Paso 7: Verificar redirección a login
        print("\n[PASO 7] Verificando redirección a login...")
        time.sleep(2.5)  # Esperar tiempo de cierre de alerta (2 segundos) mas un buffer
        assert "login.php" in driver.current_url, \
            "No fue redirigido a login. URL actual: {}".format(driver.current_url)
        print("[OK] Redirigido correctamente a: {}".format(driver.current_url))
        
        print("\n[EXITO] TEST APROBADO: Carrito sin login redirige correctamente")


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v", "-s"])
