# QSM11 en Inventor: plan de detalle

Objetivo: pasar del modelo de cajas del visor a piezas con forma fiel a las ilustraciones del manual (Bulletin 3666).
Las imágenes de referencia están en `inventor/referencias/` (páginas 25 y 29–39 a 150 dpi).

**Límite:** las ilustraciones no tienen cotas. Solo son exactas estas medidas: calibre 125, carrera 147, orden de encendido y compresor de aire 217 × 142 × 216 mm. El resto se mide **por proporción** sobre las imágenes, tomando como referencia el paso entre cilindros (≈150 mm, estimado).

## 1. Correcciones de posición vistas en el manual (versión marina)

| # | Qué cambia | Visor actual | Lo que muestra el manual | Página |
|---|---|---|---|---|
| 1 | **Aftercooler** | Caja lateral, lado admisión | Carcasa **nervada encima del motor**, a lo largo de la culata | 32, 33, 37 |
| 2 | **Depósito de expansión + intercambiador** | Cilindro y caja arriba, al frente | **Gran carcasa redondeada** en el extremo del turbo, lado estribor (a confirmar con la pág. 31, que marca el intercambiador al frente) | 31, 32 |
| 3 | **Filtro de aire** | Pequeño, detrás del turbo | **Cilindro grande** al lado del turbo, visible desde atrás | 36, 37 |
| 4 | **Codo de escape** | Tubo recto | Codo curvo de gran diámetro que sale hacia abajo y atrás | 37 |
| 5 | **Amortiguador de vibraciones** | Disco liso | Disco con **tapa ranurada** (ventilada) | 31 |
| 6 | **Enfriador de aceite de reductora** | No existe | Cilindro en el extremo posterior, con ánodo de zinc | 32 |
| 7 | **Soportes delanteros** | Bloques | Escuadras con patas a ambos lados del frente | 31, 32 |
| 8 | **Ánodos de zinc** | No existen | Tapones en el intercambiador, el aftercooler y los enfriadores | 31, 32 |

## 2. Detalle por pieza (orden de construcción)

Nivel A = forma fiel (prioridad). Nivel B = detalle fino (opcional).

| Orden | Pieza | Cómo modelarla en Inventor | Nivel A | Nivel B |
|---|---|---|---|---|
| 1 | Bloque | Extrusión del perfil frontal (sección en "Y" con faldón) y vaciado | Faldón inferior, nervios verticales laterales, tapones de agua, caras de montaje para filtros y bomba | Galerías y camisas de agua internas |
| 2 | Culata | Extrusión + 6 cortes de puertos por lado (patrón rectangular) | Puertos de admisión y escape, asientos de tornillos | Conductos internos curvos |
| 3 | Tapa de balancines | Barrido de perfil redondeado + empalmes | Nervios superiores y tornillos perimetrales | Respiradero |
| 4 | Aftercooler (encima) | Caja con empalmes y patrón de nervios | Aletas superiores visibles (pág. 37), tapas extremas | Ánodos |
| 5 | Turbo | Revolución de la voluta (espiral) + bridas | Voluta de turbina y de compresor, brida en V | Álabes |
| 6 | Codo de escape | Barrido sobre trayectoria 3D | Codo con camisa de agua y brida | — |
| 7 | Depósito de expansión + intercambiador | Caja con empalmes grandes + cilindro interno | Forma redondeada, tapón de llenado | Haz tubular |
| 8 | Cárter | Extrusión con desmoldeo (forma de bandeja) | Fondo inclinado, tapón de vaciado, varilla | — |
| 9 | Volante + carcasa | Revolución | Patrón de 8 tornillos, corona dentada (patrón circular) | Marcas de sincronismo |
| 10 | Amortiguador | Revolución + patrón de ranuras | Tapa ranurada | — |
| 11 | Accesorios (alternador, arranque, bombas, filtros) | Revolución + extrusiones | Carcasas con aletas, poleas acanaladas | Cableado |
| 12 | Internos (pistón, biela, cigüeñal) | Revolución (pistón), extrusión de perfil en I (biela), revoluciones + extrusiones (cigüeñal) | Bowl del pistón, sección en I, contrapesos | Segmentos, taladros de aceite |

## 3. Flujo de trabajo en casa (Claude Code en tu PC)

1. Ejecutar `inventor/test_conexion.ps1` y confirmar "OK".
2. Pedir a Claude Code una pieza a la vez, en el orden de la tabla, guardando cada `.ipt` en `inventor/piezas/`.
3. Revisar cada pieza en Inventor contra su imagen de referencia antes de pasar a la siguiente.
4. Al final, crear el ensamblaje `QSM11.iam` con restricciones (el cigüeñal puede girar para impulsar el mecanismo).
5. Subir los archivos a GitHub para no perderlos.
