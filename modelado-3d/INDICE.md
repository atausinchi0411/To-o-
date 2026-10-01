# Cummins QSM11: páginas útiles para modelado 3D

Fuente: *Cummins QSM-11 Operation and Maintenance Manual* (Bulletin 3666, 412 páginas).
Seleccionadas: **75 páginas** (18 %). Descartadas: 337.

## Archivos

| Archivo | Páginas | Para qué |
|---|---|---|
| `QSM11_modelado3D_esencial.pdf` | 16 | Vistas generales del motor y medidas. Con esto se modela el volumen general. |
| `QSM11_modelado3D_completo.pdf` | 75 | Lo anterior más el ruteo de tuberías y el detalle de los componentes externos. |

Los dos PDF tienen **marcadores** (panel lateral del lector de PDF) que indican la página original de cada bloque.

## Orden de trabajo sugerido

| Fase | Bloque | Páginas originales | Qué obtienes |
|---|---|---|---|
| 1 | Datos dimensionales | 361, 126, 366, 368 | Escala y proporciones del motor |
| 2 | Vistas generales | 25, 29–39 | Silueta y ubicación de los componentes |
| 3 | Diagramas de sistemas | 196–220 | Ruteo de tuberías, múltiples y turbo |
| 4 | Detalle de componentes | 158–191 | Forma de bomba de agua, termostato, turbo, arranque, poleas |

## Datos clave (página 361)

| Dato | Valor |
|---|---|
| Configuración | 6 cilindros en línea, 4 válvulas por cilindro, 4 tiempos |
| Calibre × carrera | 125 mm × 147 mm |
| Cilindrada | 10,8 L |
| Orden de encendido | 1-5-3-6-2-4 |
| Rotación del cigüeñal | Horaria, vista desde el frente |
| Peso | 940 kg (industrial) / 1124 kg (marino) |

**Cómo escalar:** el motor no trae cotas exteriores en este manual. Calibre la escala con la distancia entre cilindros. Mida en una vista lateral (páginas 32 o 33) el largo del bloque de cilindros y ajústelo a una proporción coherente con un calibre de 125 mm. Como referencia práctica, el paso entre cilindros es aproximadamente 1,1 a 1,2 veces el calibre. Ese valor es una estimación, no un dato del manual.

## Detalle por bloque

### 1. Vistas generales (geometría base)
| Pág. | Contenido |
|---|---|
| 25 | Vista isométrica del motor marino y ubicación del dataplate |
| 29 | Industrial / generador: lado del escape, con la ubicación de 25 componentes |
| 30 | Industrial / generador: lado de la bomba de combustible |
| 31 | Marino: vista frontal (amortiguador, alternador, soportes) |
| 32 | Marino: vista de estribor |
| 33–34 | Marino: estribor y babor |
| 35–37 | Marino: vistas superior, posterior y laterales adicionales |
| 38–39 | Marino: isométricas con intercambiador de calor y con keel cooler |

### 2. Datos dimensionales
| Pág. | Contenido |
|---|---|
| 361 | Especificaciones generales |
| 126 | Numeración de cilindros (1 al frente) y orden de encendido |
| 366 | Diámetro interior del tubo de escape |
| 368 | Compresor de aire: alto, ancho y largo (217 × 142 × 216 mm y 306 × 142 × 287 mm) |

### 3. Diagramas de sistemas
| Pág. | Sistema |
|---|---|
| 196–198 | Combustible |
| 199–200 | Aceite lubricante |
| 201–212 | Refrigeración (agua de mar, intercambiador, keel cooler, termostato) |
| 213–214 | Admisión de aire y aftercooler |
| 215–218 | Escape, turbo y EGR |
| 219–220 | Compresor de aire |

### 4. Detalle de componentes externos
| Pág. | Componente |
|---|---|
| 158–163 | Correas, tensores y ruteo de poleas |
| 164–169 | Bomba de agua |
| 170–174 | Bomba de agua de mar, con despiece |
| 175–178 | Carcasa del termostato |
| 179–183 | Polea loca y cubo del ventilador |
| 184–185 | Turbocompresor |
| 186–188 | Compresor de refrigerante |
| 189–191 | Motor de arranque |

## Qué se descartó y por qué
- **Garantía, distribuidores y literatura** (pp. 221–298, 383–412): no tienen información técnica.
- **Troubleshooting** (pp. 299–358): son tablas de síntomas sin geometría.
- **Operación electrónica** (pp. 41–86): describe el panel, los códigos de falla y el ECM.
- **Mantenimiento periódico** (pp. 87–154): son fotos de filtros y niveles. Solo se conservó la página 126.
- **Especificaciones de fluidos y torques** (pp. 362–381, salvo las elegidas): son presiones, capacidades y aceites.

## Limitación importante
Este es un manual de **operación y mantenimiento**, no de taller. **No tiene** medidas interiores (pistón, biela, cigüeñal, culata) ni cotas exteriores del motor completo. Para un modelo de nivel ingeniería se necesitaría:
- **Cummins QSM11 Service Manual / Shop Manual** (manual de taller; consulte el número de boletín con un distribuidor Cummins), que trae medidas de pistón, cigüeñal y válvulas.
- **Installation Drawing / General Arrangement drawing** del QSM11, que trae las cotas exteriores, soportes y bridas. Suele estar disponible a través de un distribuidor Cummins o de QuickServe Online.
