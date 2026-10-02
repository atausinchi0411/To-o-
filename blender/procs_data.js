/* ================= PROCEDIMIENTOS (manual O&M, Bulletin 3666) ================= */
// Página impresa del manual ("4-3", "A-27", "V-19", "TS-11") → página del PDF
function mpage(ref){
  const m=String(ref).match(/^(TS|[1-7]|[AEV])-(\d+)$/i); if(!m) return null;
  const s=m[1].toUpperCase(), n=+m[2];
  const base={'1':42,'2':88,'3':96,'4':110,'5':124,'6':132,'7':144,'E':24,'V':360,'TS':300}[s];
  if(s==='A') return n<=31?156+n:158+n;
  return base==null?null:base+n;
}
const PROCMAP={'101-007':'1-8','018-002':'V-10','006-015':'4-1','010-059':'3-7','010-024':'6-2','101-015':'1-5','003-004':'5-1','007-043':'3-3','007-002':'4-3','007-013':'4-4',
 '001-052':'7-1','018-020':'V-6','010-033':'A-27','010-028':'3-7','008-086':'3-4','008-066':'3-3','008-002':'A-1','103-002':'3-5','008-046':'4-9','101-004':'1-4','102-002':'2-3',
 '003-018':'3-6','018-009':'V-20','008-040':'3-4','008-036':'A-24','101-014':'1-2','012-015':'7-9','013-007':'6-4','018-003':'V-11','008-018':'7-2','008-006':'4-6','018-005':'V-18','019-016':'V-2','003-011':'5-5'};
const PROCS=[
 // ---------- Operación (Sección 1)
 {id:'arranque',sec:'Operación',t:'Arranque normal',part:'motor_arranque',pages:['1-2','1-3'],steps:[
  'El motor debe mostrar presión de aceite antes de 15 segundos. Si no la muestra o la lámpara de presión baja sigue encendida, apagarlo de inmediato y revisar el nivel de aceite.',
  'Dejar en ralentí 3 a 5 minutos antes de aplicar carga.',
  'Subir las rpm lentamente para que la presión de aceite se estabilice y lubrique los cojinetes.',
  'No dejarlo en ralentí más de 10 minutos: la cámara se enfría, el combustible no se quema completo, se forma carbón en inyectores y segmentos y las válvulas pueden pegarse.'],
  warn:['No operar un motor diésel donde haya o pueda haber vapores combustibles: el motor puede aspirarlos y acelerarse sin control (pág. 1-1).']},
 {id:'frio',sec:'Operación',t:'Arranque con baterías auxiliares y en frío',part:'motor_arranque',pages:['1-4','1-5','1-6'],steps:[
  'Ventilar el compartimiento de baterías antes de trabajar.',
  'Con cables de puente, conectar en paralelo: positivo (+) con positivo (+) y negativo (−) con negativo (−).',
  'Si se usa una fuente eléctrica externa, poner el interruptor de desconexión en OFF y retirar la llave antes de conectar los cables.',
  'Seguir el arranque normal. En frío el motor queda en ralentí hasta que el ECM detecta la presión mínima de aceite.',
  'Bajo 0 °C usar refrigerante 50/50; en frío extremo (−32 a −54 °C), 60 % glicol y 40 % agua. El combustible debe tener puntos de nube y fluidez 6 °C bajo la temperatura ambiente.'],
  warn:['Las baterías emiten gases explosivos. Desconectar primero el cable negativo y conectarlo al final.']},
 {id:'operacion',sec:'Operación',t:'Operación y apagado del motor',part:'ecm',pages:['1-5','1-6','1-7'],steps:[
  'Vigilar con frecuencia la presión de aceite y la temperatura del refrigerante (límites en la Sección V). Apagar si están fuera de especificación.',
  'Si empieza a sobrecalentar, reducir la carga hasta que la temperatura vuelva a lo normal. Si no baja, reducir más la velocidad y contactar a un taller autorizado.',
  'No operar a plena aceleración por debajo de las rpm de par máximo durante más de 30 segundos.',
  'No superar la velocidad máxima del motor.',
  'Antes de apagar tras trabajo a plena carga: 3 a 5 minutos de ralentí. Con colector y turbo blindados, 10 a 12 minutos.'],warn:[]},
 {id:'codigos',sec:'Operación',t:'Leer códigos de falla con las lámparas',part:'ecm',pages:['1-8','1-9','1-10','1-11','1-12'],steps:[
  'Al dar contacto, las lámparas STOP, CHECK y MAINT se encienden unos 2 segundos y se apagan en secuencia (autoprueba).',
  'STOP (roja): apagar el motor en cuanto sea seguro. CHECK (ámbar): falla no crítica, se puede seguir pero hay que corregirla pronto. MAINT: mantenimiento requerido.',
  'Para ver los códigos: motor apagado, llave en ON e interruptor de diagnóstico (ENG DIAG) en ON.',
  'Si no hay códigos, CHECK y STOP quedan encendidas fijas. Si hay códigos, CHECK parpadea una vez y luego STOP parpadea los tres dígitos del código; CHECK parpadea entre cada dígito.',
  'El código se repite hasta corregir la falla o apagar el interruptor. Con el interruptor rpm + se pasa al código siguiente o al anterior.',
  'Los códigos inactivos solo se leen con la herramienta electrónica INSITE.'],warn:['Los nombres y colores de las lámparas pueden variar según el fabricante del equipo.']},
 // ---------- Diario (Sección 3)
 {id:'separador',sec:'Diario',t:'Drenar el separador de agua y combustible',part:'filtro_combustible',pages:['3-2'],steps:[
  'Apagar el motor y poner un recipiente bajo el drenaje.',
  'Tipo cartucho: subir la palanca de drenaje hasta que salga líquido y drenar hasta que salga combustible limpio.',
  'Tipo spin-on: abrir la válvula a mano girando en sentido antihorario hasta que baje y empiece a drenar. Drenar hasta ver combustible limpio.',
  'Cerrar la válvula girando en sentido horario, apretada solo a mano. Apretarla de más daña la rosca.'],warn:['Desechar el líquido drenado según las normas ambientales.']},
 {id:'nivel_aceite',sec:'Diario',t:'Revisar el nivel de aceite',part:'carter',pages:['3-3'],steps:[
  'Motor nivelado y apagado.',
  'Esperar al menos 15 minutos después de apagar para que el aceite baje al cárter.',
  'Leer la varilla. Nunca operar con el nivel bajo la marca L ni sobre la marca H.'],warn:[]},
 {id:'nivel_refrig',sec:'Diario',t:'Revisar y completar el refrigerante',part:'carcasa_termostato',pages:['3-3','3-4'],steps:[
  'No quitar la tapa de presión con el motor caliente: esperar a que el refrigerante baje de 50 °C.',
  'Revisar el nivel a diario. Las fugas y la falta de refrigerante causan sobrecalentamiento.',
  'El refrigerante que se agregue debe estar mezclado con las proporciones correctas de anticongelante, aditivo (SCA) y agua.',
  'Llenar hasta el fondo del cuello de llenado del radiador o del depósito. Algunos radiadores tienen dos cuellos y hay que llenar ambos.'],warn:['No agregar refrigerante frío a un motor caliente: las fundiciones pueden dañarse.']},
 {id:'mangueras',sec:'Diario',t:'Inspeccionar mangueras de refrigerante',part:'bomba_agua',pages:['3-4'],steps:[
  'Revisar mangueras y conexiones buscando fugas o deterioro.',
  'Los trozos de manguera deteriorada pueden tapar pasajes pequeños (enfriador de aceite, intercambiador) y reducir la circulación. Cambiar las que estén dañadas.'],warn:[]},
 {id:'ventilador',sec:'Diario',t:'Inspeccionar el ventilador',part:'ventilador',pages:['3-4','3-5'],steps:[
  'No girar el motor tirando del ventilador: usar la herramienta de giro en el eje de accesorios.',
  'Buscar grietas, remaches flojos y aspas dobladas o sueltas. Verificar que esté bien montado y apretar los tornillos si es necesario.',
  'No enderezar un aspa doblada ni seguir usando un ventilador dañado: puede romperse en marcha. Cambiarlo por uno del mismo número de parte.'],warn:['Un aspa dañada puede desprenderse y causar lesiones graves.']},
 {id:'correas_insp',sec:'Diario',t:'Inspeccionar y medir la tensión de correas',part:'correa',pages:['3-5','3-6'],steps:[
  'Poly-V: las grietas transversales son aceptables; las longitudinales que se cruzan con transversales no. Cambiar si está deshilachada o le faltan trozos.',
  'Una superficie vidriada o brillante indica que patina: ajustar la tensión.',
  'Medir la tensión en el centro del tramo entre poleas con el medidor indicado en la tabla de la pág. V-18.',
  'Método alternativo en correas en V: aplicar 110 N entre poleas. Si la deflexión supera un espesor de correa por cada pie de distancia entre centros, ajustar.',
  'Correas dentadas: poner la pata central del medidor sobre la cresta de un diente.',
  'Causas de daño: tensión o tamaño incorrectos, poleas desalineadas, mala instalación, ambiente severo o aceite en la correa.'],warn:['Las correas con tensor automático no se ajustan (ver procedimiento del tensor).']},
 {id:'respiradero',sec:'Diario',t:'Revisar el tubo respiradero del cárter',part:'tapa_balancines',pages:['3-6'],steps:[
  'Inspeccionar si hay lodo, suciedad o hielo en el tubo.','Con temperaturas bajo cero, revisarlo con más frecuencia.'],warn:[]},
 {id:'restriccion',sec:'Diario',t:'Restricción del filtro de aire, tanques de aire y tubería de aire de carga',part:'codo_filtro_aire',pages:['3-7','6-2'],steps:[
  'Indicador mecánico: la bandera roja sube a medida que el filtro se ensucia. Tras cambiar el cartucho, reiniciarlo con el botón. No quitar la arandela de fieltro: absorbe humedad.',
  'El indicador debe ir lo más cerca posible de la entrada del turbo para medir la restricción real. Límites: Sección V, pág. V-5.',
  'Tanques de aire: si hay purga automática, verificar que funcione; si no, abrir el drenaje del tanque húmedo. Si sale aceite, revisar el compresor con un taller autorizado.',
  'Tubería de aire de carga: buscar fugas, agujeros, grietas o conexiones sueltas y apretar las abrazaderas.'],warn:[]},
 // ---------- 250 h (Sección 4)
 {id:'filtro_comb',sec:'250 h / 6 meses',t:'Cambiar el filtro de combustible (spin-on)',part:'filtro_combustible',pages:['4-1','4-2'],steps:[
  'Limpiar alrededor del filtro y del cabezal.',
  'Retirar el filtro con la llave de filtros (n.º 3376807 o equivalente) y retirar el anillo de sello del adaptador.',
  'Limpiar la superficie de la junta del cabezal con un paño sin pelusa.',
  'Lubricar la junta del filtro nuevo con aceite de motor limpio y llenar el filtro con diésel limpio.',
  'Instalar el anillo de sello nuevo que viene con el filtro.',
  'Girar el filtro hasta que la junta toque el cabezal y apretar a mano entre ½ y ¾ de vuelta más, o según el fabricante del filtro.'],warn:['No usar un filtro abollado o rayado: puede romperse.','No apretar con herramienta: deforma la rosca y daña el sello.']},
 {id:'aceite',sec:'250 h / 6 meses',t:'Cambiar el aceite',part:'carter',pages:['4-3','4-4'],steps:[
  'Operar el motor hasta que el refrigerante llegue a 60 °C y apagarlo.',
  'Quitar el tapón de drenaje del fondo del cárter. No usar los tapones laterales: no drenan por completo.',
  'Revisar la arandela del tapón e instalarlo (88 N·m).',
  'Llenar con aceite limpio hasta la marca H de la varilla (capacidades en la Sección V).',
  'Operar en ralentí y buscar fugas en el filtro y el tapón.',
  'Apagar, esperar unos 10 minutos y completar hasta la marca H.'],warn:['El aceite usado es tóxico: evitar contacto con la piel y desecharlo según las normas ambientales.']},
 {id:'filtro_aceite',sec:'250 h / 6 meses',t:'Cambiar el filtro de aceite',part:'filtros_aceite',pages:['4-4','4-5','4-6'],steps:[
  'El filtro es combinado: la parte superior es de flujo total y la inferior de derivación (bypass).',
  'Limpiar alrededor del cabezal y retirar el filtro con la llave de filtros.',
  'Limpiar la superficie del cabezal y asegurarse de retirar el o-ring viejo, que puede quedar pegado.',
  'Llenar el filtro nuevo con aceite limpio y aplicar una película de aceite en la junta.',
  'Apretar hasta que la junta toque el cabezal y luego según las indicaciones del filtro.',
  'Arrancar: la presión de aceite debe aparecer antes de 15 segundos; si no, apagar. Dejar 3 minutos en ralentí y revisar fugas.'],warn:['No reemplazar el filtro LF9001 por el LF9000 más largo sin verificar el espacio libre con la suspensión o el chasis.','No apretar de más: daña la rosca o el sello.']},
 {id:'filtro_refrig',sec:'250 h / 6 meses',t:'Cambiar el filtro de refrigerante',part:'bomba_agua',pages:['4-6','4-7','4-8'],steps:[
  'Se cambia en cada cambio de aceite, salvo que el SCA esté sobre 3 unidades. El SCA se mide cada 6 meses.',
  'Esperar a que el refrigerante baje de 50 °C y quitar la tapa de presión.',
  'Poner la válvula del cabezal del filtro en OFF y retirar el filtro.',
  'Limpiar el cabezal y aplicar una película de aceite limpio en la junta del filtro nuevo.',
  'Apretar hasta que la junta toque y luego ½ a ¾ de vuelta más, o según el fabricante.',
  'Poner la válvula en ON e instalar la tapa. Operar el motor, revisar fugas y, después de purgar el aire, revisar el nivel.'],warn:['Con la válvula en OFF igual puede salir un poco de refrigerante caliente.']},
 {id:'sca',sec:'250 h / 6 meses',t:'Revisar SCA y anticongelante',part:'carcasa_termostato',pages:['4-9'],steps:[
  'Medir la concentración de SCA al menos dos veces al año, en cada cambio de aceite si está sobre 3 unidades y cada vez que se agregue refrigerante entre cambios de filtro. Usar el kit de prueba.',
  'Medir la concentración de anticongelante. Una mezcla 50/50 de agua y glicol protege hasta −32 °C. El refractómetro da la lectura más confiable.',
  'El exceso de anticongelante o el anticongelante con alto silicato dañan el motor.'],warn:[]},
 {id:'cableado',sec:'250 h / 6 meses',t:'Revisar el cableado del motor',part:'mazo_cables',pages:['4-11'],steps:['Inspeccionar conexiones y arneses buscando daños. Un cableado defectuoso causa mal funcionamiento y bajo rendimiento.'],warn:['Nunca tocar conexiones con la llave en ON.']},
 // ---------- Sección 5
 {id:'overhead',sec:'Ajuste de válvulas',t:'Ajuste de válvulas e inyectores (overhead set)',part:'tapa_balancines',pages:['5-1','5-2','5-3','5-4','5-5'],steps:[
  'Medir con el motor frío y la temperatura del refrigerante estabilizada.',
  'Retirar la tapa de balancines.',
  'Las marcas A, B y C están en la polea de accesorios y se alinean con el puntero de la caja de engranajes. Girar el motor con el eje de accesorios, en sentido horario visto desde el frente.',
  'Cada cilindro tiene tres balancines: el largo es de escape, el central del inyector y el corto de admisión. El cilindro 1 está al frente.',
  'Secuencia: marca A → cilindro 1; B → 5; C → 3; A → 6; B → 2; C → 4.',
  'Con la marca A alineada, las válvulas del cilindro 1 deben estar cerradas y el émbolo del inyector abajo. Si no, es el turno del cilindro 6. Los balancines deben tener juego al moverlos a mano.',
  'Válvulas: medir con galgas entre la cruceta y la nariz del balancín. Admisión 0,10–0,41 mm; escape 0,46–0,76 mm. Fuera de rango, ajustar.',
  'Inyector: montar el reloj comparador sobre el balancín del inyector, encima de la rótula. Accionar el émbolo 3 o 4 veces, poner el reloj en cero con el émbolo abajo, soltar despacio y leer: 0,51–2,03 mm.',
  'Contratuerca del tornillo de ajuste: 61 N·m.',
  'Si tiene freno motor, revisar también la holgura del pistón esclavo (procedimiento 020-001; contratuerca 50 N·m).',
  'Instalar la tapa de balancines.'],warn:['El émbolo del inyector está bajo tensión de resorte: no dejar que la herramienta resbale.','No girar el motor desde el ventilador: puede dañar las aspas.']},
 // ---------- Sección 6
 {id:'filtro_aire',sec:'Sección 6',t:'Inspeccionar y cambiar el filtro de aire',part:'codo_filtro_aire',pages:['6-1','6-2'],steps:[
  'Agujeros, sellos sueltos o superficies de sello abolladas inutilizan el filtro: cambiarlo de inmediato.',
  'Los elementos limpiados varias veces terminan tapándose. Después de limpiarlo, medir la restricción y cambiarlo si es necesario.',
  'Soltar los seguros de la tapa y sacar tapa y elemento en línea recta para no dañarlo.',
  'Revisar el o-ring de la tapa y cambiarlo si está dañado.',
  'Instalar el elemento y verificar que el o-ring asiente bien.'],warn:[]},
 {id:'fugas',sec:'Sección 6',t:'Revisar fugas de admisión y escape',part:'colector_escape',pages:['6-2','6-3','6-4'],steps:[
  'Revisar la tubería de admisión una vez por semana: mangueras agrietadas, daños o abrazaderas sueltas.',
  'Revisar la corrosión bajo abrazaderas y mangueras: deja pasar suciedad al motor.',
  'Un ruido puede venir de fugas en: unión turbo–codo de descarga; junta turbo–colector de escape; superficie de la carcasa de turbina (apretar tornillos o abrazadera V); superficie de la carcasa del compresor (apretar la abrazadera V).',
  'Si entró refrigerante, aceite, exceso de combustible o humo negro al escape, revisar el sistema de postratamiento.'],warn:[]},
 {id:'baterias',sec:'Sección 6',t:'Revisar baterías',part:'motor_arranque',pages:['6-4','6-5'],steps:[
  'Baterías libres de mantenimiento: probar el estado de carga con un analizador de carga y arranque. Cargar si está bajo; cambiar si no carga o no mantiene la carga.',
  'Baterías convencionales: revisar el nivel de electrolito y completar con agua.',
  'Medir la densidad de cada celda con densímetro: bajo 1.200 hay que cargar. No medir justo después de agregar agua.'],warn:['Ventilar el compartimiento. Quitar primero el cable negativo y conectarlo al final.']},
 {id:'soportes',sec:'Sección 6',t:'Soportes del motor, mangueras y limpieza',part:'soporte_delantero',pages:['6-5'],steps:[
  'Revisar el apriete de tuercas y pernos de los soportes (torque según el fabricante del equipo).',
  'Revisar si la goma está deteriorada o endurecida. Reponer pernos rotos o perdidos.',
  'Arrancar y revisar mangueras y conexiones.',
  'Limpieza: el vapor es el mejor método; si no hay, usar solvente. Proteger los componentes eléctricos, aberturas y cableado del chorro directo.'],warn:['Usar protección facial y ropa protectora con vapor.']},
 {id:'persianas',sec:'Sección 6',t:'Persianas del radiador',part:'ventilador',pages:['6-6'],steps:[
  'Revisar persianas y ventilador termostático cada 1500 horas.','Con las persianas cerradas, verificar que cierren por completo.','Verificar que abran por completo a la temperatura ajustada, en el mismo rango que el termostato del motor.'],warn:[]},
 {id:'turbo_rev',sec:'Sección 6',t:'Revisar el turbocompresor',part:'turbo',pages:['6-9','6-10','7-2'],steps:[
  'Apretar las tuercas de montaje del turbo (68 N·m).',
  'Revisar fugas de escape en la superficie de la carcasa de turbina; si hay, apretar la tuerca de la abrazadera V.',
  'Revisar fugas en la superficie de la carcasa del compresor; si hay, apretar la tuerca de la abrazadera V.',
  'Si una falla metió refrigerante, aceite, exceso de combustible o humo negro al escape, inspeccionar el postratamiento.'],warn:[]},
 {id:'bomba_rev',sec:'Sección 6',t:'Revisar la bomba de agua',part:'bomba_agua',pages:['6-10'],steps:[
  'Revisar el agujero de drenaje (weep hole) de la bomba.',
  'Una mancha o depósito químico en el agujero no justifica cambiar la bomba.',
  'Un goteo o flujo constante de refrigerante o aceite sí: cambiar por una bomba nueva o reconstruida.',
  'Verificar que el agujero esté despejado (se puede limpiar con un destornillador pequeño).'],warn:[]},
 // ---------- Sección 7
 {id:'amortiguador',sec:'Sección 7',t:'Revisar el amortiguador viscoso',part:'amortiguador_polea',pages:['7-1'],steps:[
  'Con el tiempo el fluido de silicona se solidifica y el amortiguador deja de funcionar, lo que puede causar fallas graves del motor o la transmisión.',
  'Buscar pérdida de fluido, abolladuras, bamboleo y deformación del espesor o tapa levantada.',
  'Si aparece alguna de estas condiciones, cambiarlo en un taller autorizado. Su vida es limitada (Sección V).'],warn:[]},
 {id:'refrig_lavado',sec:'Sección 7',t:'Limpiar, lavar y llenar el sistema de refrigeración',part:'carcasa_termostato',pages:['7-2','7-3','7-4','7-5','7-6','7-7','7-8'],steps:[
  'Esperar a que el refrigerante baje de 50 °C y quitar la tapa del radiador.',
  'Drenar el sistema. No quitar el filtro de refrigerante.',
  'Agregar 3,8 L de limpiador Fleetguard Restore (o equivalente) por cada 38 a 57 L de capacidad y llenar con agua.',
  'Poner la calefacción de cabina al máximo para que circule por el calefactor.',
  'Operar a temperatura normal el tiempo indicado en el manual, apagar y drenar.',
  'Llenar con agua limpia, operar 5 minutos en ralentí alto, apagar y drenar. Repetir hasta que el agua salga limpia.',
  'Llenar con refrigerante totalmente formulado o mezcla 50/50 de anticongelante formulado y agua de buena calidad. Usar un filtro de servicio para dejar el SCA correcto.',
  'Llenar hasta el fondo del cuello (algunos radiadores tienen dos). Instalar la tapa.',
  'Operar hasta 82 °C, revisar fugas, dejar enfriar y revisar el nivel.'],warn:['El limpiador no contiene anticongelante: no dejar que el sistema se congele durante la limpieza.','No llenar un motor caliente con refrigerante frío.','El refrigerante es tóxico: desecharlo según las normas.']},
 {id:'descarga_comp',sec:'Sección 7',t:'Revisar las líneas de descarga del compresor de aire',part:'compresor_aire',pages:['7-9','7-10'],steps:[
  'Apagar el motor y abrir el drenaje del tanque húmedo para liberar la presión.',
  'Retirar la línea de descarga del compresor y medir el espesor total de carbón en su interior.',
  'Si supera la especificación, revisar culata, válvulas y línea del compresor, y cambiar lo necesario con un taller autorizado.',
  'Seguir revisando las conexiones hasta el primer tanque hasta que el carbón sea menor a 2 mm; limpiar o cambiar lo que exceda.',
  'Revisar secadores, válvulas divisoras, de alivio e inyectores de alcohol, y buscar fugas de aire.'],warn:['Usar protección ocular con aire comprimido.']},
 // ---------- Sección A: reparación y reemplazo
 {id:'corte_volt',sec:'Reparación (Sección A)',t:'Probar el voltaje de la válvula de corte',part:'valvula_corte',pages:['A-1'],steps:[
  'Conectar un solo cable al solenoide de corte: más de uno puede dañar el ECM.',
  'El voltaje y el número de parte de la bobina están grabados en el extremo del terminal.',
  'Llave en ON y medir el voltaje en la bobina con un multímetro: debe ser igual al voltaje de batería.',
  'Llave en OFF.'],warn:[]},
 {id:'correa_vent',sec:'Reparación (Sección A)',t:'Ajustar o cambiar la correa del ventilador',part:'correa',pages:['A-1','A-2','A-3'],steps:[
  'Aflojar la contratuerca del eje de la polea tensora.',
  'Para sacarla: girar el tornillo de ajuste en sentido antihorario y acercar al máximo los centros de la polea tensora y la del ventilador. No hacer rodar la correa sobre la polea ni hacer palanca.',
  'Instalar la correa y ajustar la tensión con el tornillo, midiéndola con el medidor (tabla de la pág. V-18). No llevar la tensión al valor total solo con el tornillo: al apretar la contratuerca sube.',
  'Apretar la contratuerca (165–190 N·m) y medir otra vez.',
  'Una correa con 10 minutos de uso se considera usada: si su tensión está bajo el mínimo, tensarla al máximo de usada. Cambiarla si no mantiene la tensión.',
  'La desalineación entre poleas no debe superar 6 mm.'],warn:[]},
 {id:'correa_alt',sec:'Reparación (Sección A)',t:'Ajustar o cambiar la correa del alternador',part:'alternador',pages:['A-3','A-4','A-5'],steps:[
  'Tipo con eslabón de ajuste: aflojar la contratuerca del tornillo de ajuste, el tornillo de bloqueo del eslabón y el perno de pivote.',
  'Instalar la correa en las poleas de la bomba de agua y del alternador sin hacerla rodar ni hacer palanca.',
  'Girar el tornillo de ajuste en sentido horario para tensar y medir con el medidor (tabla de la pág. V-18).',
  'Apretar la contratuerca contra el soporte y el tornillo de bloqueo del eslabón.'],warn:['Si el motor tiene un segundo alternador, seguir el procedimiento del fabricante del equipo.']},
 {id:'tensor',sec:'Reparación (Sección A)',t:'Tensor automático: revisar y cambiar',part:'tensor',pages:['A-5','A-6','A-7'],steps:[
  'Las correas con tensor automático no se ajustan y el medidor no da una lectura válida: solo se inspecciona el tensor.',
  'Si el brazo golpea los topes en operación, revisar los soportes y el largo de la correa (soportes sueltos, alternador movido o correa incorrecta).',
  'Para cambiar la correa: sostener el tensor con una barra de ⅜" o ¾", girarlo hasta el tope, sacar la correa, instalar la nueva y soltar el tensor.',
  'Para cambiar el tensor: sacar la correa, retirar los tornillos de montaje y el tensor, instalar el nuevo y apretar los tornillos.'],warn:['Cuidar la correa al pasarla por las poleas con pestaña.']},
 {id:'bomba_agua',sec:'Reparación (Sección A)',t:'Cambiar la bomba de agua',part:'bomba_agua',pages:['A-7','A-8','A-9','A-10','A-11','A-12','A-13','A-14','A-15','A-16'],steps:[
  'Con el motor frío, quitar la tapa de presión y drenar el refrigerante (procedimiento 008-018).',
  'Quitar la correa del alternador, el tornillo de la polea de la bomba y la polea (extractor ST-647 o equivalente). Retirar el alternador si estorba.',
  'Aflojar las abrazaderas de la manguera de derivación, quitar la manguera superior y los 4 tornillos de la carcasa del termostato.',
  'Quitar los 2 tornillos de la conexión de transferencia de agua y los 3 tornillos de montaje de la bomba.',
  'Sacar la bomba girándola hacia afuera desde arriba e inclinando la parte trasera hacia abajo para pasar el soporte del termostato.',
  'Instalar con o-rings nuevos. Lubricarlos con refrigerante limpio, agua jabonosa o aceite vegetal, no con aceite de motor.',
  'Retén de aceite: labio y eje limpios y secos, sin lubricar, con el labio amarillo hacia afuera. Usar la camisa de instalación que trae el retén.',
  'Si hay enfriador del convertidor de torque, colocar el disco (orificio) en la manguera de derivación antes de montar la carcasa del termostato.',
  'Montar el termostato con sello nuevo, las mangueras, la polea, el alternador y la correa.',
  'Llenar el sistema, operar hasta 71 °C y revisar fugas.'],warn:['No quitar la tapa de presión con el motor caliente.']},
 {id:'termostato',sec:'Reparación (Sección A)',t:'Cambiar el termostato',part:'carcasa_termostato',pages:['A-20','A-21','A-22'],steps:[
  'Con el motor frío, quitar la tapa de presión.',
  'Drenar: abrir el grifo del radiador y quitar la manguera inferior.',
  'Quitar la manguera superior de la carcasa del termostato y aflojar las abrazaderas de la manguera de derivación (en algunos modelos lleva un disco del enfriador del convertidor).',
  'Quitar los 4 tornillos, la carcasa y el termostato.',
  'Instalar el termostato y un o-ring nuevo en la ranura de la carcasa.',
  'Montar la manguera de derivación, la carcasa con sus 4 tornillos y la manguera superior.',
  'Cerrar el grifo, instalar la manguera inferior, llenar (procedimiento 008-018) y revisar fugas.'],warn:[]},
 {id:'polea_tensora',sec:'Reparación (Sección A)',t:'Cambiar la polea tensora del ventilador',part:'tensor',pages:['A-23','A-24'],steps:[
  'Aflojar la contratuerca del eje, soltar el ajuste, acercar las poleas y sacar la correa.',
  'Quitar el pasador y la arandela del tornillo de ajuste, la contratuerca y arandela traseras y el tornillo de ajuste.',
  'Retirar la polea tensora del soporte del cubo del ventilador.',
  'Instalar la polea nueva con arandela y contratuerca, sin apretar todavía.',
  'Instalar el tornillo de ajuste, la arandela y el pasador.',
  'Instalar y tensar la correa, apretar la contratuerca y volver a medir la tensión.'],warn:[]},
 {id:'cubo_vent',sec:'Reparación (Sección A)',t:'Cambiar el cubo del ventilador',part:'cubo_ventilador',pages:['A-24','A-25','A-26','A-27'],steps:[
  'Aflojar la contratuerca de la polea tensora, acercar las poleas y sacar la correa.',
  'Retirar el conjunto de ventilador y embrague, la polea del ventilador y los 4 tornillos del cubo.',
  'Instalar el cubo nuevo con sus 4 tornillos, la polea y el conjunto de ventilador y embrague.',
  'Instalar y tensar la correa, apretar la contratuerca y volver a medir la tensión.'],warn:[]},
 {id:'turbo',sec:'Reparación (Sección A)',t:'Verificar y cambiar el turbocompresor',part:'turbo',pages:['A-27','A-28','A-29','A-30'],steps:[
  'Comparar el número de conjunto de la placa del turbo con el que indica la lista de partes de control (CPL) del motor. Si no corresponde, instalar el correcto.',
  'Usar grúa o ayuda para levantarlo. El ojo de izado se usa solo para el turbo, con su hombro asentado contra la carcasa de cojinetes.',
  'No usar el actuador como punto de apoyo y no girar la carcasa de turbina.',
  'Cuidar el sensor de temperatura del aire de entrada, el de velocidad del turbo y las líneas de refrigerante del actuador.',
  'Quitar las 4 tuercas de montaje (si no sueltan, partirlas para no romper los espárragos). Retirar el turbo y desechar las juntas.',
  'Aplicar compuesto antiagarrotante, instalar con junta nueva y apretar las 4 tuercas (68 N·m).',
  'Si el turbo es nuevo, instalar la entrada de refrigerante y la alimentación de aceite.'],warn:['Pieza pesada: usar grúa o ayuda.']},
 {id:'arranque_aire',sec:'Reparación (Sección A)',t:'Motor de arranque neumático',part:'motor_arranque',pages:['A-30'],steps:[
  'No operarlo con una presión de aire menor a 480 kPa (70 psi).',
  'Mantener el compresor según este manual y verificar que mangueras, tubos y líneas no tengan fugas.',
  'Tanques, líneas y válvulas los diseña el fabricante del equipo: consultar su manual.'],warn:[]},
 {id:'arrancador',sec:'Reparación (Sección A)',t:'Cambiar el motor de arranque eléctrico',part:'motor_arranque',pages:['A-32','A-33'],steps:[
  'Ventilar el compartimiento de baterías y desconectar las baterías (negativo primero).',
  'Etiquetar y desconectar los cables del motor de arranque.',
  'Quitar los 3 tornillos y el motor de arranque. Pueden ser métricos o en pulgadas: usar los mismos.',
  'Verificar el tamaño y grado de los tornillos, instalar el motor y apretar.',
  'Conectar los cables del motor de arranque y luego las baterías (negativo al final).'],warn:['Las baterías emiten gases explosivos.']},
 {id:'almacenaje',sec:'Reparación (Sección A)',t:'Almacenamiento prolongado',part:'bloque',pages:['A-33','A-34'],steps:['Si el motor va a estar fuera de servicio más de 6 meses, hay que tomar precauciones contra el óxido. Consultar el procedimiento con un taller autorizado Cummins.'],warn:[]},
];
