# 🐾 AdoptPets — Migración Java → Python/Django

## Equivalencias Spring Boot → Django

| Java / Spring Boot              | Python / Django                        |
|---------------------------------|----------------------------------------|
| `@SpringBootApplication`        | `manage.py` + `settings.py`            |
| `@Entity` + JPA                 | `models.py` (Django ORM)               |
| `@Repository` (JpaRepository)   | `Model.objects` (QuerySet API)         |
| `@Service`                      | Funciones en `services/`               |
| `@Controller` + `@GetMapping`   | `views.py` + `urls.py`                 |
| `Model` (addAttribute)          | `context` dict en `render()`           |
| Thymeleaf templates             | Django templates (`{% %}`, `{{ }}`)    |
| Spring Security                 | Django Auth + decoradores de rol       |
| `BCryptPasswordEncoder`         | `BCryptSHA256PasswordHasher`           |
| `@PreAuthorize("hasRole(...)")` | `@rol_requerido('ADMIN')`              |
| `RedirectAttributes` (flash)    | `messages.success/error(request, ...)` |
| `CommandLineRunner`             | `manage.py init_data`                  |
| `application.properties`       | `settings.py`                          |
| `pom.xml`                       | `requirements.txt`                     |
| OpenPDF                         | ReportLab                              |
| Apache POI                      | openpyxl                               |

---

## 🚀 Instalación y ejecución

### 1. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate       # Linux/Mac
venv\Scripts\activate          # Windows
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar base de datos
Edita `settings.py` con tus credenciales MySQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'adoptpets',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 4. Crear las tablas (equivalente a `spring.jpa.hibernate.ddl-auto=create`)
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Inicializar datos (equivalente a `DataInitializer.java`)
```bash
python manage.py init_data
```

### 6. Correr el servidor (equivalente a `mvn spring-boot:run`)
```bash
python manage.py runserver
```

El proyecto queda disponible en: **http://localhost:8000**

---

## 📁 Estructura del proyecto

```
adoptpets_project/          ← Proyecto Django (equivale al root de Spring)
│
├── adoptpets/              ← App principal
│   ├── models.py           ← Entidades JPA → modelos Django
│   ├── views.py            ← Controllers → Views
│   ├── urls.py             ← @RequestMapping → urlpatterns
│   ├── services/
│   │   └── reporte_service.py  ← ReporteService.java
│   └── management/
│       └── commands/
│           └── init_data.py    ← DataInitializer.java
│
├── templates/              ← Templates HTML (reemplaza Thymeleaf)
├── static/                 ← CSS, JS, imágenes
├── settings.py             ← application.properties
└── requirements.txt        ← pom.xml
```

---

## 🔐 Credenciales por defecto

| Campo    | Valor                  |
|----------|------------------------|
| Email    | admin@adoptpets.com    |
| Password | admin123               |

---

## 📝 Notas importantes

- Los **templates Thymeleaf** (`th:each`, `th:if`, `th:text`) deben convertirse a sintaxis Django (`{% for %}`, `{% if %}`, `{{ variable }}`).
- Las **rutas** cambian de `/admin/mascotas` a `{% url 'admin_mascotas' %}` en templates.
- El **CSRF** es manejado automáticamente por Django — agrega `{% csrf_token %}` en todos los formularios POST.