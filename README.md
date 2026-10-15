# Sistema Distribuido de Gestión de Correos Internos
**Proyecto Integrador - Tercer Nivel**  
*Ingeniería en Sistemas de Información - Universidad Internacional del Ecuador (UIDE)*

## Descripción del Proyecto
Plataforma empresarial distribuida para la gestión de correo electrónico interno entre dos sedes operativas interconectadas. La aplicación cliente-servidor está desarrollada en **Go (Golang)** e integrada con un servicio de autenticación segura en **FastAPI**, sobre una infraestructura de red segmentada con VLANs y enrutamiento dinámico **OSPF**.

## Arquitectura y Tecnologías
- **Aplicación Principal:** Go (Golang) - Cliente-Servidor mediante TCP/Sockets.
- **Autenticación y Seguridad:** FastAPI (Python), hashing de contraseñas y tokens.
- **Infraestructura de Red:** OpenWrt (Raspberry Pi), OSPF, VLANs, EtherChannel, RSTP y VLSM.
- **Análisis Estadístico:** Medición de latencia de red, tiempos de respuesta y volumen de mensajería.

## Estructura del Repositorio
- `/docs`: Documentos de la Fase 1 (PDFs) y Diagrama UML.
- `/app-go`: Código fuente del sistema de correo interno en Go.
- `/auth-service`: Servicio API REST para registro e inicio de sesión en FastAPI.
- `/network`: Plan de direccionamiento IP, topologías y configuraciones de red.
- `/research`: Datos, encuestas y análisis estadístico.

## Integrantes del Equipo y Roles
- **Paula Doménica Cevallos Vacacela** – *Desarrolladora Lead Go / POO & Coordinación Técnica*
- **Odalis Jamel Anangonó Sevillano** – *Especialista en Infraestructura, Redes & Seguridad*
- **Keyla Antonella Imba Untuña** – *Analista Estadístico & Socio-Tecnológico*

## Licencia
Este proyecto se distribuye bajo los términos de la Licencia **MIT**. Para más detalles, consulta el archivo [LICENSE](./LICENSE).

## Vídeo explicativo acerca de roles
https://youtu.be/6H8S9G2ZL00?si=Lrfr2mipz3l5Dy1w

## Declaración de Integridad Académica y Uso de IA
Declaramos que el presente trabajo ha sido desarrollado colaborativamente por el equipo. Se han utilizado herramientas de Inteligencia Artificial (ej. ChatGPT, Gemini) de forma ética y complementaria como apoyo para la redacción de documentación, diseño estructural de código y depuración. La autoría y validación final corresponden íntegramente a las integrantes del grupo.
