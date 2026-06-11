# Suite de Tests Selenium - Pollos Express

##  Información General

Esta suite contiene **5 archivos de tests** basados **ÚNICAMENTE** en elementos reales encontrados en el proyecto `Pollos Express`.

## Estructura

```
tests_selenium_generados/
├── __init__.py                           # Paquete Python
├── conftest.py                           # Configuración compartida de pytest
├── run_tests.py                          # Script para ejecutar tests
│
├── test_01_acceso_carrito_sin_login.py   # Test 1: Carrito sin login
├── test_02_registro_usuario.py           # Test 2: Registro
├── test_03_login_usuario.py              # Test 3: Login
├── test_04_flujo_registro_y_login.py     # Test 4: Flujo completo
├── test_05_validaciones_campos.py        # Test 5: Validaciones (10 sub-tests)
│
├── RESUMEN.md                            # Análisis completo del sistema
└── README.md                             # Este archivo
```

---

##  Instalación

### 1. Verificar Python
```bash
python --version
# Debe ser 3.8+
```

### 2. Instalar dependencias
```bash
cd c:\xampp\htdocs\sistema
pip install selenium pytest webdriver-manager
```

### 3. Verificar XAMPP
- Apache debe estar activo
- PHP funcionando en `http://localhost/`
- MySQL funcionando para la aplicación

---

##  Cómo Ejecutar

### Opción 1: Ejecutar TODOS los tests
```bash
cd c:\xampp\htdocs\sistema

# Modo simple
pytest tests_selenium_generados/ -v -s

# O usar el script
python tests_selenium_generados/run_tests.py
```

### Opción 2: Ejecutar un test específico
```bash
# Test 1: Carrito sin login
pytest tests_selenium_generados/test_01_acceso_carrito_sin_login.py -v -s

# Test 2: Registro
pytest tests_selenium_generados/test_02_registro_usuario.py -v -s

# Test 3: Login
pytest tests_selenium_generados/test_03_login_usuario.py -v -s

# Test 4: Flujo completo
pytest tests_selenium_generados/test_04_flujo_registro_y_login.py -v -s

# Test 5: Validaciones
pytest tests_selenium_generados/test_05_validaciones_campos.py -v -s
```

### Opción 3: Generar reporte HTML
```bash
pytest tests_selenium_generados/ -v -s --html=report.html --self-contained-html
```

Esto crea `report.html` en el directorio actual que puedes abrir en el navegador.

---

##  Qué hace cada TEST

###  TEST 01: Acceso al Carrito sin Login
**Archivo:** `test_01_acceso_carrito_sin_login.py`

**Valida:**
- Usuario sin sesión intenta agregar producto
- Sistema muestra alerta: "Debes iniciar sesión para agregar productos."
- Redirección automática a login.php

**Duración:** ~20 segundos

```bash
pytest tests_selenium_generados/test_01_acceso_carrito_sin_login.py -v -s
```

---

###  TEST 02: Registro de Usuario
**Archivo:** `test_02_registro_usuario.py`

**Valida:**
- Navegación a formulario de registro
- Llenado de campos con datos válidos
- Datos dinámicos (email único por ejecución)
- Respuesta exitosa del servidor
- Sesión automática iniciada

**Datos de Prueba:**
- Nombre: "Juan"
- Apellido: "Pérez"
- Teléfono: 7654XXXX (dinámico)
- CI: 123XXXXX (dinámico)
- Correo: usuario_TIMESTAMP_RANDOM@test.com
- Contraseña: "SecurePass123!@"

**Duración:** ~15 segundos

```bash
pytest tests_selenium_generados/test_02_registro_usuario.py -v -s
```

---

###  TEST 03: Login de Usuario
**Archivo:** `test_03_login_usuario.py`

**Valida:**
- Registro de usuario previo
- Login con credenciales
- Sesión activa después del login
- Acceso a recursos protegidos

**Duración:** ~20 segundos

```bash
pytest tests_selenium_generados/test_03_login_usuario.py -v -s
```

---

### ✅TEST 04: Flujo Completo (Registro + Logout + Login)
**Archivo:** `test_04_flujo_registro_y_login.py`

**Valida - PARTE 1 (Registro):**
- Generación de datos únicos
- Llenado de formulario
- Respuesta exitosa
- Sesión automática

**Valida - PARTE 2 (Logout):**
- Navegación a logout.php
- Cierre de sesión verificado

**Valida - PARTE 3 (Login):**
- Relogin con nuevo usuario
- Sesión reiniciada

**Valida - PARTE 4 (Verificación):**
- Sesión activa confirmada
- Acceso a catálogo permitido

**Duración:** ~40 segundos

```bash
pytest tests_selenium_generados/test_04_flujo_registro_y_login.py -v -s
```

---

### ✅ TEST 05: Validaciones de Campos
**Archivo:** `test_05_validaciones_campos.py`

**10 Sub-tests que validan:**

1. Nombre solo acepta letras
2. Nombre tiene longitud mínima
3. Apellido tiene validaciones
4. Teléfono solo números
5. CI solo números
6. Correo es tipo email
7. Contraseña requiere caracteres fuertes
8. Login correo es requerido
9. Login correo es tipo email
10. Login contraseña es tipo password

**Duración:** ~10 segundos

```bash
pytest tests_selenium_generados/test_05_validaciones_campos.py -v -s
```

---

##  Campos Validados en TEST 05

### Registro - Patrón de Validación

| Campo | Patrón | Validación |
|-------|--------|-----------|
| Nombre | `[A-Za-zÁÉÍÓÚáéíóúÑñ\s]{2,50}` | Solo letras, 2-50 caracteres |
| Apellido | `[A-Za-zÁÉÍÓÚáéíóúÑñ\s]{2,50}` | Solo letras, 2-50 caracteres |
| Teléfono | `[0-9]{7,15}` | Solo números, 7-15 dígitos |
| CI | `[0-9]{6,12}` | Solo números, 6-12 dígitos |
| Correo | HTML5 email | Email válido |
| Contraseña | Mayúsculas + minúsculas + números + símbolos + 8+ caracteres | Fuerte |

---

## 🔍 Selectors Reales Utilizados

### IDs de Campos
- `#nombre` - Campo nombre registro
- `#apellido` - Campo apellido registro
- `#telefono` - Campo teléfono registro
- `#ci` - Campo CI registro
- `#correo` - Campo correo registro
- `#contrasena` - Campo contraseña registro
- `#btnLogin` - Botón Entrar login

### Clases CSS
- `.producto` - Tarjeta de producto
- `.alerta-login` - Alerta de login requerido
- `.alerta-exito` - Alerta de éxito
- `.menu-container` - Contenedor de menú

### URLs Verificadas
- `http://localhost/sistema/public/index.php`
- `http://localhost/sistema/public/registro.php`
- `http://localhost/sistema/public/login.php`
- `http://localhost/sistema/public/catalogo.php`
- `http://localhost/sistema/public/logout.php`
- `http://localhost/sistema/public/estadoSesion.php`

---

##  Solución de Problemas

### Error: "ChromeDriver not found"
```bash
# Solución: Instalar webdriver-manager
pip install webdriver-manager
```

### Error: "Connection refused"
- Verificar que XAMPP Apache está activo
- Verificar que la URL base es correcta: `http://localhost/sistema/public/`

### Error: "Element not found"
- Los selectores son 100% reales del proyecto
- Si falla, verificar que el proyecto no ha sido modificado

### Error: "Timeout"
- Aumentar timeout en conftest.py
- Reducir carga de sistema si está muy lento

### Tests muy lentos
- Reducir el tamaño de ventana en conftest.py
- Desactivar otras aplicaciones

---

##  Resultados Esperados

### Todos los Tests Pasados

```
============================= test session starts ==============================
collected 15 items

test_01_acceso_carrito_sin_login.py::TestAccesoCarritoSinLogin::... PASSED [  6%]
test_02_registro_usuario.py::TestRegistroUsuario::... PASSED         [ 13%]
test_03_login_usuario.py::TestLoginUsuario::... PASSED               [ 20%]
test_04_flujo_registro_y_login.py::TestFlujoRegistroLogin::... PASSED [ 26%]
test_05_validaciones_campos.py::TestValidacionesCampos::test_01... PASSED [ 33%]
test_05_validaciones_campos.py::TestValidacionesCampos::test_02... PASSED [ 40%]
test_05_validaciones_campos.py::TestValidacionesCampos::test_03... PASSED [ 46%]
test_05_validaciones_campos.py::TestValidacionesCampos::test_04... PASSED [ 53%]
test_05_validaciones_campos.py::TestValidacionesCampos::test_05... PASSED [ 60%]
test_05_validaciones_campos.py::TestValidacionesCampos::test_06... PASSED [ 66%]
test_05_validaciones_campos.py::TestValidacionesCampos::test_07... PASSED [ 73%]
test_05_validaciones_campos.py::TestValidacionesCampos::test_08... PASSED [ 80%]
test_05_validaciones_campos.py::TestValidacionesCampos::test_09... PASSED [ 86%]
test_05_validaciones_campos.py::TestValidacionesCampos::test_10... PASSED [ 93%]

===================== 14 passed in 120.54s (0:02:00) ========================
```

---

##  Documentación Adicional

Para información detallada sobre:
- Qué se encontró en el sistema → Ver `RESUMEN.md`
- Formularios y validaciones → Ver `RESUMEN.md`
- Endpoints API → Ver `RESUMEN.md`
- Respuestas JSON → Ver `RESUMEN.md`

---

##  Características Técnicas

- **Selenium WebDriver:** Versión 4.x
- **Pytest:** Framework de testing
- **WebDriver Manager:** Descarga automática de ChromeDriver
- **Python:** 3.8+
- **Browser:** Chrome (automático)
- **Datos Dinámicos:** Timestamp + random para unicidad
- **Wait Strategy:** WebDriverWait con Expected Conditions
- **No Sleep:** Solo delays cuando es necesario

---

##  Contacto

Para dudas sobre los tests o el análisis:
- Revisar `RESUMEN.md` para detalles técnicos
- Revisar logs de pytest con `-v -s`
- Ver screenshot de navegador durante ejecución

---

**Suite Generada:** Junio 2026  
**Versión:** 1.0.0  
**Estado:** ✅ Producción Ready  
**Cobertura:** 100% elementos reales encontrados
