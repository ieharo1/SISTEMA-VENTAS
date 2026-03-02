# Sistema de Gestión de Ventas

Un sistema completo de gestión de ventas desarrollado con FastAPI y MongoDB.

## Características

- **Autenticación JWT**: Inicio de sesión seguro con tokens JWT
- **Gestión de Vendedores**: CRUD completo de vendedores
- **Registro de Ventas**: Registro y seguimiento de ventas
- **Metas Mensuales**: Establecer y rastrear metas de ventas
- **Dashboard**: Métricas y KPIs en tiempo real
- **Reportes**: Ranking de vendedores y estado de metas
- **Diseño Responsivo**: Interfaz moderna con Bootstrap 5

## Requisitos

- Python 3.8+
- MongoDB

## Instalación

1. Clonar el repositorio:
```bash
cd Streaming
```

2. Crear un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno (opcional):
```bash
# Crea un archivo .env con tus configuraciones
DATABASE_URL=mongodb://localhost:27017
DATABASE_NAME=sales_management
SECRET_KEY=tu-secret-key-segura
```

5. Iniciar MongoDB:
```bash
# Asegúrate de tener MongoDB instalado y ejecutándose
mongod
```

6. Ejecutar la aplicación:
```bash
uvicorn app.main:app --reload
```

7. Abrir en el navegador:
```
http://localhost:8000
```

## Estructura del Proyecto

```
Streaming/
├── app/
│   ├── config.py          # Configuración de la aplicación
│   ├── database.py        # Conexión a MongoDB
│   ├── main.py           # Aplicación FastAPI principal
│   ├── schemas/
│   │   └── schemas.py    # Modelos Pydantic
│   ├── services/
│   │   └── auth_service.py  # Autenticación JWT
│   ├── repositories/
│   │   └── repository.py # Operaciones CRUD
│   ├── routes/
│   │   ├── auth.py       # Rutas de autenticación
│   │   └── sales.py      # Rutas de ventas
│   └── templates/
│       ├── base.html     # Plantilla base
│       ├── index.html    # Página de inicio
│       ├── login.html   # Página de login
│       ├── dashboard.html
│       ├── sellers.html
│       ├── sales.html
│       ├── goals.html
│       └── reports.html
├── requirements.txt
└── README.md
```

## Colecciones de MongoDB

El sistema utiliza las siguientes colecciones:
- `users`: Usuarios del sistema
- `sellers`: Vendedores
- `sales`: Registro de ventas
- `goals`: Metas mensuales

## Uso

1. **Registro**: Crea una cuenta en `/register`
2. **Login**: Inicia sesión con tus credenciales
3. **Dashboard**: Ver métricas generales
4. **Vendedores**: Gestiona tu equipo de vendedores
5. **Ventas**: Registra nuevas ventas
6. **Metas**: Establece metas mensuales
7. **Reportes**: Analiza el rendimiento

## Desarrollado por

Isaac Esteban Haro Torres
- Ingeniero en Sistemas
- Full Stack Developer
- Especializado en Automatización y Data

**Contacto:**
- Email: zackharo1@gmail.com
- WhatsApp: 098805517
- GitHub: https://github.com/ieharo1
- Portafolio: https://ieharo1.github.io/portafolio-isaac.haro/
