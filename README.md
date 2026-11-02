# Sistema Distribuido de Gestión de Correos Internos
**Proyecto Integrador - Tercer Nivel**  
*Ingeniería en Sistemas de Información - Universidad Internacional del Ecuador (UIDE)*

## Descripción del Proyecto
Plataforma de correo interno para dos sedes (A y B) interconectadas, sin depender de SMTP externo. La aplicación cliente-servidor está desarrollada en **Go** y se integra con un servicio de autenticación en **FastAPI**, sobre una red segmentada con VLANs y enrutamiento **OSPF**.

## Arquitectura y Tecnologías
- **Aplicación principal:** Go, cliente-servidor mediante TCP.
- **Autenticación:** FastAPI (Python). Emite y valida las sesiones; la sesión caduca tras 30 minutos de inactividad.
- **Red:** OpenWrt (Raspberry Pi), OSPF, VLANs, EtherChannel, RSTP y VLSM.
- **Análisis estadístico:** latencia, tiempos de respuesta y volumen de mensajería a partir del registro de actividad.

## Estructura del Repositorio
- `/docs`: Documentos de la Fase 1 y 2 (PDFs) y Diagrama UML.
- `/app-go`: Código fuente del sistema de correo interno en Go.
- `/auth-service`: Servicio API REST para registro e inicio de sesión en FastAPI.
- `/network`: Plan de direccionamiento IP, topologías y configuraciones de red.
- `/research`: Datos, encuestas y análisis estadístico.

## Integrantes del Equipo y Roles
- **Paula Doménica Cevallos Vacacela** – Desarrolladora Lead Go / POO y Coordinación Técnica
- **Odalis Jamel Anangonó Sevillano** – Especialista en Infraestructura, Redes y Seguridad
- **Keyla Antonella Imba Untuña** – Analista Estadístico y Socio-Tecnológico

## Vídeo explicativo acerca de roles
https://youtu.be/6H8S9G2ZL00?si=Lrfr2mipz3l5Dy1w

## Licencia
Proyecto distribuido bajo la Licencia **MIT**. Ver [LICENSE](./LICENSE).

## Declaración de Integridad Académica y Uso de IA
Declaramos que el presente trabajo ha sido elaborado íntegramente por las tres integrantes del equipo, quienes asumieron la responsabilidad de su desarrollo y validación final.Si bien se recurrió a la herramienta de inteligencia artificial Claude (Anthropic) con un carácter exclusivamente de apoyo, limitando su función a la revisión de la coherencia interna entre los apartados del documento, todas las correcciones propuestas fueron sometidas a una estricta evaluación por parte de los miembros del grupo antes de su aplicación.En consecuencia, la autoría y la responsabilidad última sobre el contenido corresponden en su totalidad al equipo.
