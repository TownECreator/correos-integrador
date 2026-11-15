"""
generar_prototipo.py
Proyecto Integrador Fase 3 - Grupo 8 - Sistema de correos internos

Genera las imágenes del prototipo visual del cliente de consola (una por pantalla).

Cómo usarlo:
    1. Instalar Pillow:        pip install pillow
    2. Ejecutar:               python generar_prototipo.py
    3. Salida: carpeta "prototipo_salida" con prototipo_pantalla_1.png ... _7.png

Cómo editarlo:
    - Cambiar textos: modificar la lista PANTALLAS (más abajo).
    - Cada línea es una tupla (texto, color). Colores disponibles:
        "titulo" verde en negrita, "menu" azul en negrita, "normal" blanco,
        "tenue" gris, "resalte" amarillo, "ok" verde, "error" rojo.
    - Cambiar tamaño de letra: variable TAM_LETRA.
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- configuración
CARPETA_SALIDA = "prototipo_salida"
TAM_LETRA = 22
ALTO_LINEA = 34
RELLENO = 26          # espacio interno de la ventana
ALTO_BARRA = 52       # barra de título de la ventana
MARGEN = 40           # margen alrededor de la ventana
ANCHO_MINIMO = 1000   # ancho mínimo de la imagen

# Fuentes monoespaciadas (se usa la primera que exista en el equipo)
FUENTES_NORMAL = [
    "C:/Windows/Fonts/consola.ttf",
    "/System/Library/Fonts/Menlo.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
]
FUENTES_NEGRITA = [
    "C:/Windows/Fonts/consolab.ttf",
    "/System/Library/Fonts/Menlo.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf",
]

FONDO_IMAGEN = (22, 27, 34)
FONDO_VENTANA = (13, 17, 23)
FONDO_BARRA = (48, 54, 61)
TEXTO_BARRA = (230, 237, 243)

COLORES = {
    "titulo":  ((126, 231, 135), True),    # (color, negrita)
    "menu":    ((121, 192, 255), True),
    "normal":  ((230, 237, 243), False),
    "tenue":   ((139, 148, 158), False),
    "resalte": ((255, 211, 105), False),
    "ok":      ((126, 231, 135), False),
    "error":   ((255, 123, 114), False),
}

VERDE = (63, 185, 80)
AZUL = (88, 166, 255)
ROJO = (248, 81, 73)

# ---------------------------------------------------------------- contenido
# (nombre de archivo, título de la ventana, color del borde, líneas)
PANTALLAS = [
    ("prototipo_pantalla_1", "PANTALLA 1 · Inicio de sesión", VERDE, [
        ("================ CORREO INTERNO ================", "titulo"),
        ("Usuario: usuario1", "normal"),
        ("Contraseña: ********", "normal"),
        ("------------------------------------------------", "tenue"),
        ("Iniciando sesión...", "resalte"),
    ]),
    ("prototipo_pantalla_2", "PANTALLA 2 · Menú principal", AZUL, [
        ("=========== MENÚ PRINCIPAL (usuario1) ==========", "menu"),
        ("1. Redactar mensaje", "normal"),
        ("2. Bandeja de entrada", "normal"),
        ("3. Mensajes enviados", "normal"),
        ("4. Cerrar sesión", "normal"),
        ("Elija una opción (1-4): _", "resalte"),
    ]),
    ("prototipo_pantalla_3", "PANTALLA 3 · Bandeja de entrada", VERDE, [
        ("============== BANDEJA DE ENTRADA ==============", "titulo"),
        (" ID  Estado    De        Asunto          Fecha", "tenue"),
        (" 12  [NUEVO]   usuario2  Reunión lunes   14/11 09:30", "resalte"),
        (" 10  [LEÍDO]   usuario3  Informe         13/11 16:05", "normal"),
        ("------------------------------------------------", "tenue"),
        ("Ingrese el ID para leer, o 0 para volver: _", "resalte"),
        ("(Si no hay mensajes se muestra: Sin mensajes)", "tenue"),
    ]),
    ("prototipo_pantalla_4", "PANTALLA 4 · Leer y eliminar mensaje", VERDE, [
        ("================= LEER MENSAJE =================", "titulo"),
        ("De:      usuario2", "normal"),
        ("Asunto:  Reunión lunes", "normal"),
        ("Fecha:   14/11/2026 09:30", "normal"),
        ("------------------------------------------------", "tenue"),
        ("Recuerden traer el informe impreso.", "normal"),
        ("------------------------------------------------", "tenue"),
        ("1. Eliminar   2. Volver", "normal"),
        ("Opción: 1", "resalte"),
        ("¿Eliminar este mensaje? (s/n): s", "resalte"),
        ("Mensaje eliminado.", "ok"),
    ]),
    ("prototipo_pantalla_5", "PANTALLA 5 · Redactar mensaje", VERDE, [
        ("================ REDACTAR MENSAJE ==============", "titulo"),
        ("Para:    usuario2", "normal"),
        ("Asunto:  Informe", "normal"),
        ("Mensaje: Adjunto el resumen de la semana.", "normal"),
        ("¿Enviar? (s/n): s", "resalte"),
        ("Mensaje enviado.", "ok"),
    ]),
    ("prototipo_pantalla_6", "PANTALLA 6 · Mensajes enviados", VERDE, [
        ("============== MENSAJES ENVIADOS ===============", "titulo"),
        (" ID  Para      Asunto     Fecha", "tenue"),
        (" 15  usuario2  Informe    14/11 12:40", "normal"),
        ("------------------------------------------------", "tenue"),
        ("0. Volver", "resalte"),
        ("(Si no hay envíos se muestra: Sin mensajes enviados)", "tenue"),
    ]),
    ("prototipo_pantalla_7", "PANTALLA 7 · Mensajes de error", ROJO, [
        ("[ERROR] Credenciales inválidas. Revise su usuario y contraseña e intente de nuevo.", "error"),
        ("[ERROR] Servicio de autenticación no disponible. Intente más tarde.", "error"),
        ("[ERROR] Su sesión venció. Inicie sesión de nuevo.", "error"),
        ("[ERROR] No se pudo conectar con el servidor. Verifique la red e intente de nuevo.", "error"),
        ("[ERROR] El destinatario no existe. El mensaje no fue enviado.", "error"),
        ("[ERROR] Hay campos vacíos. Complételos para enviar el mensaje.", "error"),
        ("[ERROR] Mensaje no encontrado.", "error"),
    ]),
]


# ---------------------------------------------------------------- código
def cargar_fuente(rutas, tamano):
    for ruta in rutas:
        if os.path.exists(ruta):
            return ImageFont.truetype(ruta, tamano)
    print("Aviso: no se encontró una fuente monoespaciada; se usa la predeterminada.")
    return ImageFont.load_default()


def dibujar_pantalla(nombre, titulo, borde, lineas, f_normal, f_negrita, carpeta):
    # Ancho según la línea más larga
    medidor = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    ancho_texto = max(
        medidor.textlength(t, font=f_negrita if COLORES[c][1] else f_normal)
        for t, c in lineas
    )
    ancho_ventana = int(max(ANCHO_MINIMO - 2 * MARGEN, ancho_texto + 2 * RELLENO))
    alto_ventana = ALTO_BARRA + 2 * RELLENO + len(lineas) * ALTO_LINEA

    ancho = ancho_ventana + 2 * MARGEN
    alto = alto_ventana + 2 * MARGEN
    img = Image.new("RGB", (ancho, alto), FONDO_IMAGEN)
    d = ImageDraw.Draw(img)

    x0, y0 = MARGEN, MARGEN
    x1, y1 = x0 + ancho_ventana, y0 + alto_ventana

    # Ventana y barra de título
    d.rounded_rectangle((x0, y0, x1, y1), radius=16, fill=FONDO_VENTANA, outline=borde, width=3)
    d.rounded_rectangle((x0, y0, x1, y0 + ALTO_BARRA), radius=16, fill=FONDO_BARRA)
    d.rectangle((x0 + 2, y0 + ALTO_BARRA - 16, x1 - 2, y0 + ALTO_BARRA), fill=FONDO_BARRA)
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        cx = x0 + 28 + i * 30
        d.ellipse((cx, y0 + 18, cx + 16, y0 + 34), fill=c)
    d.text((x0 + 120, y0 + 13), titulo, font=f_negrita, fill=TEXTO_BARRA)
    # Reafirma el borde por encima de la barra para que no queden residuos
    d.rounded_rectangle((x0, y0, x1, y1), radius=16, outline=borde, width=3)

    # Líneas de texto
    y = y0 + ALTO_BARRA + RELLENO
    for texto, clave in lineas:
        color, negrita = COLORES[clave]
        d.text((x0 + RELLENO, y), texto, font=f_negrita if negrita else f_normal, fill=color)
        y += ALTO_LINEA

    ruta = os.path.join(carpeta, nombre + ".png")
    img.save(ruta)
    return ruta, img.size


def main():
    carpeta = sys.argv[1] if len(sys.argv) > 1 else CARPETA_SALIDA
    os.makedirs(carpeta, exist_ok=True)
    f_normal = cargar_fuente(FUENTES_NORMAL, TAM_LETRA)
    f_negrita = cargar_fuente(FUENTES_NEGRITA, TAM_LETRA)
    for nombre, titulo, borde, lineas in PANTALLAS:
        ruta, tam = dibujar_pantalla(nombre, titulo, borde, lineas, f_normal, f_negrita, carpeta)
        print(f"Generada: {ruta} {tam[0]}x{tam[1]}")


if __name__ == "__main__":
    main()
