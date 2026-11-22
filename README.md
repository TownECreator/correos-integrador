# Sistema Distribuido de Gestión de Correos Internos
**Proyecto Integrador - Tercer Nivel**  
*Ingeniería en Sistemas de Información - Universidad Internacional del Ecuador (UIDE)*  
**Grupo 8**

## Descripción del Proyecto
Plataforma de correo interno para dos sedes (A y B) interconectadas, sin depender de SMTP externo. La aplicación cliente-servidor está desarrollada en **Go** y se integra con un servicio de autenticación en **FastAPI**, sobre una red segmentada con VLANs y enrutamiento **OSPF**.

## Arquitectura y Tecnologías
- **Aplicación principal:** Go, arquitectura cliente-servidor mediante HTTP con intercambio de datos en formato JSON (tiempo de espera de 5 segundos en cliente).
- **Autenticación:** FastAPI (Python). Emite y valida los tokens de sesión; la sesión caduca tras 30 minutos de inactividad. La aplicación Go no almacena contraseñas.
- **Red:** OpenWrt (Raspberry Pi), OSPF, VLANs, EtherChannel, RSTP y VLSM.
- **Análisis estadístico:** Latencia, tiempos de respuesta y volumen de mensajería a partir del registro de actividad (`ActivityLog`).

## Configuración y Puertos (RNF-04)
- **Servidor Go (`MailServer`):** Ejecutado en Sede A, escucha peticiones HTTP en el puerto `8080`.
- **Servicio de Autenticación (`FastAPI`):** Ejecutado en Sede A, responde peticiones REST en el puerto `8000`.
- **Cliente Go (`MailClient`):** Ejecutado en Sede B mediante interfaz de consola (`ConsoleUI`), conectándose a la dirección IP del servidor en Sede A.

## Estructura del Repositorio
- `/docs`: Documentación del proyecto y archivos editables de los diagramas UML.
- `/app-go`: Código fuente del sistema de correo interno en Go (`cmd/client`, `cmd/server`, `internal/cliente`, `internal/servidor`, `internal/modelos`).
- `/auth-service`: Servicio API REST para registro e inicio de sesión en FastAPI.
- `/network`: Plan de direccionamiento IP, topologías y configuraciones de red.
- `/research`: Datos, encuestas y análisis estadístico.

## Entregables por Fase

### Fase 2: Análisis y Requisitos
- **Documento de análisis y requisitos:** [Ver Fase 2 (PDF)]([./docs/Proyecto_integrador_fase_2.pdf](https://github.com/TownECreator/correos-integrador/blob/main/docs/Proyecto%20integrador%20fase%202.pdf)) 
- **Contenido:** Definición de actores, alcance, requisitos funcionales (`RF-SW-01` a `RF-INT-01`), requisitos no funcionales (`RNF-01` a `RNF-07`), diagrama de casos de uso, fichas y matriz de trazabilidad inicial.

### Fase 3: Diseño de la Solución
- **Documento de diseño de arquitectura y clases:** [Ver Fase3_POO_Grupo8.pdf](./docs/Fase3_POO_Grupo8.pdf)
- **Contenido:** Arquitectura cliente-servidor entre Sede A y Sede B, diagramas UML (componentes, clases en Go con interfaces y composición, y secuencia de autenticación), estructura de paquetes, matriz de trazabilidad completa (`RNF-01` a `RNF-08`), plan de pruebas (`CP-01` a `CP-28`) y prototipo visual de consola.

## Integrantes del Equipo y Roles
- **Paula Doménica Cevallos Vacacela** – Desarrolladora Lead Go / POO y Coordinación Técnica
- **Odalis Jamel Anangonó Sevillano** – Especialista en Infraestructura, Redes y Seguridad
- **Keyla Antonella Imba Untuña** – Analista Estadístico y Socio-Tecnológico

## Vídeo explicativo acerca de roles
https://youtu.be/6H8S9G2ZL00?si=Lrfr2mipz3l5Dy1w

## Licencia
Proyecto distribuido bajo la Licencia **MIT**. Ver [LICENSE](./LICENSE).

## Declaración de Integridad Académica y Uso de IA
Declaramos que el presente trabajo ha sido elaborado íntegramente por las tres integrantes del equipo, quienes asumieron la responsabilidad de su desarrollo y validación final. Se contó con la asistencia de herramientas de inteligencia artificial (Claude Sonnet 5.5 y Gemini) exclusivamente como apoyo para la revisión de coherencia interna, generación de borradores iniciales de matrices, pruebas y prototipos visuales. Todas las propuestas fueron sometidas a una estricta evaluación, corrección y validación por parte de las miembros del grupo antes de su inclusión, asumiendo la autoría y responsabilidad total sobre el contenido.
