# Sistema Distribuido de Gestión de Correos Internos
**Proyecto Integrador - Tercer Nivel**  
*Ingeniería en Sistemas de Información - Universidad Internacional del Ecuador (UIDE)*

## Descripción del Proyecto
Plataforma de correo interno para dos sedes (A y B) interconectadas, sin depender de SMTP externo. La aplicación cliente-servidor está desarrollada en **Go** y se integra con un servicio de autenticación en **FastAPI**, sobre una red segmentada con VLANs y enrutamiento **OSPF**.

Operaciones: iniciar sesión, enviar mensajes de texto, consultar bandeja de entrada y enviados, leer y eliminar mensajes.

## Arquitectura y Tecnologías
- **Aplicación principal:** Go, cliente-servidor mediante TCP.
- **Autenticación:** FastAPI (Python). Emite y valida las sesiones; la sesión caduca tras 30 minutos de inactividad.
- **Red:** OpenWrt (Raspberry Pi), OSPF, VLANs, EtherChannel, RSTP y VLSM.
- **Análisis estadístico:** latencia, tiempos de respuesta y volumen de mensajería a partir del registro de actividad.

## Estructura del Repositorio
- `docs/`: documentos de las Fases 1 y 2 y diagramas UML.
- `app-go/`: código en Go, dividido en paquetes `cliente`, `servidor` y `modelos`. 
- `auth-service/`: servicio de autenticación en FastAPI.
- `network/`: direccionamiento IP, topologías y configuraciones de red.
- `research/`: datos y análisis estadístico.

## Configuración
| Componente | Sede | IP | Puerto |
|---|---|---|---|
| MailServer (Go) | A | [COMPLETAR] | [COMPLETAR] |
| FastAPI | A | [COMPLETAR] | [COMPLETAR] |
| MailClient (Go) | B | [COMPLETAR] | no aplica |

## Cómo ejecutar
1. **FastAPI** (Sede A):
   `cd auth-service && uvicorn [COMPLETAR] --host 0.0.0.0 --port [PUERTO]`
2. **MailServer** (Sede A):
   `cd app-go && go run ./servidor`
3. **MailClient** (Sede B):
   `cd app-go && go run ./cliente`

## Documentación
- Fase 1: `docs/Proyecto integrador fase 1.pdf`
- Fase 2: `docs/Proyecto integrador fase 2.pdf`
- Diagrama de clases actualizado: `docs/DIAGRAMA_2.jpg`

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
