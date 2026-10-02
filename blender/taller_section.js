/* ================= TALLER: MANTENIMIENTO, SENSORES, FRENO MOTOR, COMBUSTIBLE ================= */
const B=(x,y,z)=>new T.Vector3(x,z,-y);          // coordenadas de Blender → visor
const INT={d:{n:'Diario',c:'#4fe3f0'},h250:{n:'250 h / 6 meses',c:'#9fe0b8'},h600:{n:'600 h / 1 año',c:'#f2d23c'},h1500:{n:'1500 h / 1 año',c:'#ffb347'},h6000:{n:'6000 h / 2 años',c:'#ff7a6e'}};
const MAINT=[
 {i:'d',t:'Drenar el separador de agua y combustible',en:'Fuel-water separator — drain',part:'filtro_combustible',b:[-20,270,-125],pg:'Sección 3',how:'Abrir la válvula de drenaje del filtro hasta que salga combustible limpio, sin agua. El agua en el combustible daña la bomba y los inyectores.'},
 {i:'d',t:'Revisar el nivel de aceite',en:'Lubricating oil level — check',part:'carter',b:[-290,232,412],pg:'Sección 3',how:'Con el motor detenido y nivelado, leer la varilla. Mantener el nivel entre las marcas de mínimo y máximo.'},
 {i:'d',t:'Revisar el nivel de refrigerante',en:'Coolant level — check',part:'carcasa_termostato',pg:'Sección 3',how:'Se revisa en el depósito del radiador del camión, con el motor frío. No abrir el tapón con el motor caliente: el sistema está a presión.'},
 {i:'d',t:'Inspeccionar la correa',en:'Drive belt — inspect',part:'correa',pg:'Sección 3',how:'Buscar grietas transversales, deshilachado o vidriado. Las grietas que cruzan las costillas a lo ancho indican reemplazo.'},
 {i:'d',t:'Revisar la restricción del filtro de aire',en:'Air cleaner restriction — check',part:'codo_filtro_aire',pg:'Sección 3',how:'Leer el indicador de restricción. Si marca rojo, dar servicio al filtro. Clave en minería por el polvo.'},
 {i:'d',t:'Revisar el tubo respiradero del cárter',en:'Crankcase breather tube — check',part:'tapa_balancines',b:[-353,-60,690],pg:'Sección 3',how:'Verificar que no esté obstruido ni doblado. Un respiradero tapado aumenta la presión del cárter y provoca fugas de aceite.'},
 {i:'d',t:'Inspeccionar el ventilador',en:'Cooling fan — inspect',part:'ventilador',pg:'Sección 3',how:'Buscar aspas dobladas, rotas o flojas. Un aspa dañada puede soltarse y desbalancea el ventilador.'},
 {i:'d',t:'Revisar las tuberías del aire de carga',en:'Charge air piping — check',part:'conducto_aire',pg:'Sección 3',how:'Revisar mangueras y abrazaderas entre el turbo, el enfriador de aire y el colector. Una fuga hace perder potencia.'},
 {i:'d',t:'Drenar los tanques de aire',en:'Air tanks and reservoirs — drain',part:'compresor_aire',pg:'Sección 3',how:'Los tanques están en el camión, no en el motor. Purgarlos elimina el agua que condensa el compresor.'},
 {i:'h250',t:'Cambiar aceite y filtros de aceite',en:'Lubricating oil and filters — change',part:'filtros_aceite',pg:'Sección 4 · pág. 2-4',how:'El intervalo industrial depende del ciclo de trabajo y del aceite (tabla de la pág. 2-4): por ejemplo, con aceite CH-4 entre 300 h (severo) y 600 h (ligero). Máximo 250 h si el 40 % del tiempo se trabaja a más de 38 °C. Reducir 50 % si el azufre del combustible supera 0,5 %.'},
 {i:'h250',t:'Vaciar el cárter (tapón de drenaje)',en:'Oil pan drain plug',part:'carter',b:[-78,0,-378],pg:'Sección 4',how:'Drenar con el aceite tibio para que arrastre los sedimentos. Revisar la arandela del tapón.'},
 {i:'h250',t:'Reemplazar el filtro de combustible',en:'Fuel filter — replace',part:'filtro_combustible',pg:'Sección 4',how:'Llenar el filtro nuevo con combustible limpio antes de instalarlo y apretar a mano según indique el filtro.'},
 {i:'h250',t:'Cambiar el filtro de refrigerante',en:'Coolant filter — change',part:'bomba_agua',pg:'Sección 4',how:'No cambiarlo si la concentración de SCA supera 3 unidades (nota de la pág. 2-3). Su ubicación exacta depende de la instalación.'},
 {i:'h250',t:'Revisar SCA y anticongelante',en:'SCA and antifreeze concentration — check',part:'carcasa_termostato',pg:'Sección 4',how:'Medir la concentración del aditivo (SCA) y del anticongelante con el kit de prueba. Protegen las camisas húmedas contra la corrosión.'},
 {i:'h250',t:'Revisar el cableado del motor',en:'Engine wiring — check',part:'mazo_cables',pg:'Sección 4',how:'Buscar roces, conectores flojos o corroídos, sobre todo en el ECM y los sensores.'},
 {i:'h600',t:'Ajustar válvulas e inyectores (overhead set)',en:'Overhead set — adjust',part:'tapa_balancines',pg:'Sección 5 · págs. 5-1 a 5-4',how:'Holgura de válvulas (límites de recomprobación): admisión 0,10–0,41 mm, escape 0,46–0,76 mm. Holgura del inyector: 0,51–2,03 mm (0,020–0,080 in). Secuencia girando el motor: marca A → cil. 1, B → 5, C → 3, A → 6, B → 2, C → 4. Si tiene freno motor, revisar también la holgura del pistón esclavo (procedimiento 020-001).',warn:'El manual indica este ajuste a 600 h / 1 año en la tabla de la pág. 2-3, pero la Sección 5 lo titula "1500 horas". Confírmalo con tu programa de mantenimiento.'},
 {i:'h1500',t:'Revisar la bomba de agua',en:'Water pump — check',part:'bomba_agua',pg:'Sección 6',how:'Buscar fugas por el orificio de drenaje y juego en el eje.'},
 {i:'h1500',t:'Revisar el turbocompresor',en:'Turbocharger — check',part:'turbo',pg:'Sección 6',how:'Revisar fugas de aceite, montaje y juego del eje. Rozamiento de la rueda contra la carcasa indica cojinetes gastados.'},
 {i:'h1500',t:'Revisar los pernos de los soportes',en:'Engine mounting bolts — check',part:'soporte_delantero',pg:'Sección 6',how:'Apretar al par especificado y revisar los aisladores de goma.'},
 {i:'h1500',t:'Revisar fugas de admisión y escape',en:'Air leaks, intake and exhaust — check',part:'colector_escape',pg:'Sección 6',how:'Buscar hollín en juntas del colector de escape y fugas de aire en el colector de admisión.'},
 {i:'h1500',t:'Revisar el conjunto del filtro de aire',en:'Air cleaner assembly — check',part:'codo_filtro_aire',pg:'Sección 6',how:'Revisar abrazaderas, juntas y que no entre aire sin filtrar. En minería es una de las causas principales de desgaste prematuro.'},
 {i:'h1500',t:'Revisar las mangueras del refrigerante',en:'Cooling system hoses — check',part:'carcasa_termostato',pg:'Sección 6',how:'Buscar grietas, ablandamiento o abrazaderas flojas.'},
 {i:'h1500',t:'Limpiar el motor',en:'Engine — clean',part:'bloque',pg:'Sección 6',how:'Lavar con vapor o agua a presión, protegiendo el ECM, los conectores y el alternador.'},
 {i:'h6000',t:'Limpiar, lavar y rellenar el sistema de refrigeración',en:'Cooling system — clean, flush, fill',part:'carcasa_termostato',pg:'Sección 7',how:'Drenar, lavar con limpiador, enjuagar y rellenar con mezcla 50/50 de anticongelante y agua de calidad.'},
 {i:'h6000',t:'Revisar el amortiguador de vibraciones',en:'Vibration damper — check',part:'amortiguador_polea',pg:'Sección 7',how:'Buscar abolladuras, fugas de fluido (viscoso) o deformación. Un amortiguador dañado puede romper el cigüeñal.'},
 {i:'h6000',t:'Revisar la polea tensora',en:'Fan drive idler pulley — check',part:'tensor',pg:'Sección 7',how:'Girar a mano: no debe tener ruido ni juego.'},
 {i:'h6000',t:'Revisar el cubo del ventilador',en:'Fan hub, belt driven — check',part:'cubo_ventilador',pg:'Sección 7',how:'Revisar juego del rodamiento y fugas de grasa.'},
 {i:'h6000',t:'Revisar el compresor de aire',en:'Air compressor — check',part:'compresor_aire',pg:'Sección 7',how:'Revisar la línea de descarga: el carbón acumulado indica paso de aceite.'},
];
const SENS=[
 {part:'sensor_presion_admision',t:'Presión del colector de admisión (boost)',en:'Intake manifold pressure sensor',pg:'O&M págs. 29 (n.º 4) y 59',mide:'La presión del aire que entrega el turbo al colector.',ecm:'El ECM la usa para saber cuánto aire entra y dosificar el combustible.'},
 {part:'sensor_temp_admision',t:'Temperatura del colector de admisión',en:'Intake manifold temperature sensor',pg:'O&M págs. 29 y 59',mide:'La temperatura del aire después del enfriador de aire de carga.',ecm:'Si es alta, se enciende la lámpara de alta temperatura de admisión y el sistema de protección reduce potencia (pág. 58).'},
 {part:'sensor_temp_refrigerante',t:'Temperatura del refrigerante',en:'Coolant temperature sensor',pg:'O&M pág. 59 (n.º 13)',mide:'La temperatura del refrigerante, en el soporte del termostato.',ecm:'Si es alta, se enciende la lámpara de alta temperatura de refrigerante y se reduce potencia (pág. 58).'},
 {part:'sensor_aceite',t:'Presión y temperatura de aceite',en:'Oil pressure and temperature sensor',pg:'O&M págs. 30 (n.º 17), 57–59',mide:'La presión y la temperatura del aceite en la galería del bloque.',ecm:'Presión baja: lámpara y reducción de potencia (pág. 57). Temperatura alta: lámpara de alta temperatura de aceite (pág. 58).'},
 {part:'sensor_posicion_motor',t:'Sensor de posición del motor (EPS)',en:'Engine position sensor',pg:'O&M págs. 30 (n.º 18) y 59',mide:'La posición y la velocidad del motor.',ecm:'Es la referencia de tiempo para decidir cuándo inyectar en cada cilindro.'},
 {part:'sensor_velocidad_volante',t:'Velocidad de la corona del volante',en:'Flywheel ring gear speed sensor',pg:'O&M pág. 30 (n.º 10)',mide:'Las rpm del motor, contando los dientes de la corona.',ecm:'Lectura de velocidad del motor.'},
 {part:'sensor_presion_ambiente',t:'Presión ambiente',en:'Ambient air pressure sensor',pg:'O&M págs. 30 (n.º 5) y 59',mide:'La presión atmosférica.',ecm:'Permite al ECM ajustar el combustible según la altitud. Muy relevante en minas de altura, donde el aire tiene menos oxígeno.'},
 {part:'sensor_presion_riel',t:'Presión de combustible (riel)',en:'Rail pressure',pg:'O&M pág. 30 (n.º 15)',mide:'La presión del combustible que la bomba envía a los inyectores.',ecm:'El ECM regula esa presión con los actuadores de la bomba.'},
 {part:'sensor_agua_combustible',t:'Agua en el combustible (opcional)',en:'Water-in-fuel sensor',pg:'O&M pág. 58',mide:'Agua acumulada en el filtro primario de combustible.',ecm:'Enciende la lámpara de agua en el combustible: hay que drenar el separador.'},
 {part:'sensor_ventilador',t:'Sensor del ventilador',en:'Fan sensor',pg:'O&M pág. 29 (n.º 9)',mide:'Aparece en la vista del lado de escape del motor industrial.',ecm:'Su función exacta depende de la instalación del ventilador en el camión.'},
 {part:'valvula_corte',t:'Válvula de corte de combustible',en:'Fuel shutoff valve',pg:'O&M pág. 59 (n.º 1)',mide:'Es un actuador, no un sensor.',ecm:'Abre el paso de combustible al girar la llave y lo cierra para apagar el motor.'},
 {part:'ecm',t:'ECM (módulo de control electrónico)',en:'Electronic Control Module',pg:'O&M págs. 30 y 59',mide:'Recibe todas las señales de los sensores.',ecm:'Decide cuánto combustible inyectar y cuándo, gestiona la protección del motor y guarda los códigos de falla.'},
];
const FUEL=[
 {part:null,b:[300,560,-80],t:'1. Tanque de combustible',d:'El combustible sale del tanque del camión (pág. 197, n.º 1).'},
 {part:'ecm',t:'2. Placa de refrigeración del ECM',d:'El combustible pasa por la placa trasera del ECM y lo enfría (n.º 7).'},
 {part:'filtro_combustible',t:'3. Filtro y separador de agua',d:'Retiene partículas y agua (n.º 3). Aquí está el sensor opcional de agua en el combustible.'},
 {part:'bomba_combustible',t:'4. Bomba de engranajes y actuadores',d:'La bomba de engranajes aspira y presuriza el combustible. Los actuadores, controlados por el ECM, regulan la presión hacia los inyectores (n.º 2).'},
 {part:'valvula_corte',t:'5. Válvula de corte',d:'Abre el paso con la llave en ON y lo cierra para apagar el motor.'},
 {part:'culata',t:'6. Galería de la culata',d:'El combustible recorre una perforación interna de la culata hasta los 6 inyectores (n.º 6).'},
 {part:'inyector_1',t:'7. Inyectores accionados por leva',d:'La tercera leva de cada cilindro empuja, a través de su varilla y balancín, el émbolo del inyector. El émbolo baja y pulveriza el combustible a alta presión cerca del punto muerto superior (n.º 4).'},
 {part:'culata',t:'8. Drenaje y retorno',d:'El combustible sobrante sale por el drenaje de los inyectores (n.º 5) y vuelve al tanque, llevándose calor.'},
];
let T_mode='mant', T_int='d', T_sel=-1, T_items=[];
const hotEls=[];
function partCenter(id){const p=parts[id]; if(!p)return null; return new T.Box3().setFromObject(p).getCenter(new T.Vector3());}
function itemPos(it){ if(it.b) return B(...it.b).add(it.part&&parts[it.part]?parts[it.part].parent.position.clone().sub(parts[it.part].parent.userData.base||new T.Vector3()):new T.Vector3()); return partCenter(it.part)||new T.Vector3(); }
function setHot(list){
  T_items=list; T_sel=-1;
  hotEls.forEach(e=>e.remove()); hotEls.length=0;
  list.forEach((it,k)=>{const e=document.createElement('button'); e.className='hot'; e.textContent=k+1; e.style.setProperty('--hc',it.col||'var(--accent)');
    e.onclick=ev=>{ev.stopPropagation(); pickItem(k);}; $('#labels').appendChild(e); hotEls.push(e);});
}
function updateHot(w,h){
  T_items.forEach((it,k)=>{const e=hotEls[k]; const p=itemPos(it); tmpV.copy(p).project(camera);
    if(tmpV.z>1||$('#tab-taller').hidden&&!S.tallerPins){e.style.display='none';return;}
    e.style.display='flex'; e.style.left=((tmpV.x+1)/2*w)+'px'; e.style.top=((1-tmpV.y)/2*h)+'px'; e.classList.toggle('on',k===T_sel);});
}
function pickItem(k){
  T_sel=k; const it=T_items[k]; renderTaller();
  if(it.part&&parts[it.part]){ if(!S.sys[PI_[it.part].sys]){S.sys[PI_[it.part].sys]=true;syncSys();applyVisibility();} select(it.part,true); }
  const p=itemPos(it), dir=camera.position.clone().sub(controls.target).normalize();
  flyTo(p.clone().addScaledVector(dir,950),p);
  const el=document.getElementById('titem'+k); if(el) el.scrollIntoView({block:'nearest'});
}
function brakeLift(c,th){ if(!S.brake) return 0; const a=phaseOf(c,th).a; const d=a>360?a-720:a; return (d>-25&&d<35)?3.5*Math.sin((d+25)/60*Math.PI):0; }
function renderTaller(){
  const el=$('#tab-taller');
  const modes=[['mant','Mantenimiento'],['sens','Sensores'],['freno','Freno motor'],['comb','Combustible']];
  let h=`<div class="grid2" style="margin-bottom:10px">${modes.map(([k,n])=>`<button class="btn ${T_mode===k?'on':''}" data-tm="${k}">${n}</button>`).join('')}</div>`;
  if(T_mode==='mant'){
    h+=`<h2>Mapa de mantenimiento</h2><p class="small">Tabla de la pág. 2-3 del manual (aplicaciones marinas e industriales). Haz cada tarea en el intervalo que ocurra primero, horas o meses, y en cada intervalo repite también las tareas de los anteriores.</p>
    <div class="row" style="margin:8px 0">${Object.entries(INT).map(([k,v])=>`<button class="btn ${T_int===k?'on':''}" data-ti="${k}" style="border-color:${v.c}">${v.n}</button>`).join('')}</div>
    <button class="btn primary" id="tRoutine">Rutina guiada: ${INT[T_int].n}</button>`;
  } else if(T_mode==='sens'){
    h+=`<h2>Sensores y diagnóstico</h2><p class="small">Ubicaciones según las vistas del motor industrial (págs. 29–30) y la lista del sistema de combustible electrónico (pág. 59). El sensor de nivel de refrigerante (opcional) va en el depósito de expansión del camión, por eso no aparece en el modelo.</p>
    <div class="note">Sistema de protección (pág. 57): cuando una presión o temperatura sale de rango, el ECM registra la falla, enciende una lámpara en cabina y reduce gradualmente potencia y velocidad. Solo apaga el motor si la función de apagado por protección está activada. Las fallas se leen con la herramienta de servicio electrónica (INSITE).</div>`;
  } else if(T_mode==='freno'){
    h+=`<h2>Freno motor de compresión</h2>
    <label class="sw"><input type="checkbox" id="brakeOn" ${S.brake?'checked':''}> <b>Freno motor activado</b></label>
    <ol class="small" style="padding-left:18px;line-height:1.55">
     <li>El conductor activa el freno en cabina. El ECM energiza los solenoides del freno (pág. 50) y corta la inyección de combustible.</li>
     <li>En la carrera de compresión, el pistón comprime aire. Comprimir cuesta energía: la toma de las ruedas del camión, a través de la transmisión.</li>
     <li>Cerca del punto muerto superior, un pistón esclavo hidráulico (pieza roja) empuja y abre la válvula de escape.</li>
     <li>El aire comprimido escapa sin devolver su energía al pistón en la bajada. El resultado es una fuerza de frenado en cada cilindro, cada 720°.</li>
    </ol>
    <div class="note">En minería permite bajar rampas cargado sin recalentar los frenos de servicio. Con el freno activado, observa en rayos X la válvula de escape abriéndose al final de la compresión y la ausencia de chorro de combustible.</div>
    <div class="note warn">Funcionamiento general de un freno de compresión. El manual O&M no detalla los tiempos ni la hidráulica del freno del QSM11; la apertura mostrada es ilustrativa. Si el motor tiene freno, al ajustar las válvulas hay que revisar la holgura del pistón esclavo (pág. 5-4, procedimiento 020-001).</div>`;
  } else {
    h+=`<h2>Sistema de combustible</h2><p class="small">Recorrido según el diagrama de flujo del motor industrial (pág. 197) y los componentes de la pág. 59. Activa Rayos X para ver las partículas.</p>`;
  }
  const list=T_mode==='mant'?MAINT.filter(m=>m.i===T_int).map(m=>({...m,col:INT[m.i].c})):T_mode==='sens'?SENS:T_mode==='comb'?FUEL:[{part:'freno_motor',t:'Carcasas del freno motor',d:'Una por cada dos cilindros, debajo de la tapa de balancines (catálogo pág. 29).'},{part:'solenoides_freno',t:'Solenoides',d:'Los activa el ECM. Dejan pasar aceite a presión hacia los pistones esclavos.'},{part:'esclavo_freno_1',t:'Pistón esclavo (cilindro 1)',d:'Empuja la cruceta de escape para abrir las válvulas cerca del punto muerto superior.'}];
  if(JSON.stringify(list.map(x=>x.t))!==JSON.stringify(T_items.map(x=>x.t))) setHot(list);
  h+=`<div class="partlist" style="margin-top:10px">${list.map((it,k)=>`<div id="titem${k}" class="titem ${k===T_sel?'sel':''}">
    <button data-tk="${k}"><span class="hnum" style="--hc:${it.col||'var(--accent)'}">${k+1}</span> ${it.t}${it.en?` <span class="en small">${it.en}</span>`:''}</button>
    ${k===T_sel?`<div class="tdet">${it.how?`<p>${it.how}</p>`:''}${it.mide?`<p><b>Mide:</b> ${it.mide}</p><p><b>Uso en el ECM:</b> ${it.ecm}</p>`:''}${it.d?`<p>${it.d}</p>`:''}${it.warn?`<div class="note warn">${it.warn}</div>`:''}${it.pg?`<div class="small">Fuente: manual O&M, ${it.pg}</div>`:''}</div>`:''}</div>`).join('')}</div>`;
  el.innerHTML=h;
  el.querySelectorAll('[data-tm]').forEach(b=>b.onclick=()=>enterMode(b.dataset.tm));
  el.querySelectorAll('[data-ti]').forEach(b=>b.onclick=()=>{T_int=b.dataset.ti; renderTaller();});
  el.querySelectorAll('[data-tk]').forEach(b=>b.onclick=()=>pickItem(+b.dataset.tk));
  const r=$('#tRoutine'); if(r) r.onclick=()=>{pickItem(0); S.routine=true;};
  const bo=$('#brakeOn'); if(bo) bo.onchange=()=>{S.brake=bo.checked; renderTaller();};
}
function enterMode(m){
  T_mode=m; S.routine=false;
  if(m==='freno'){ setSys(['estructura','distribucion','freno','moviles','cigueñal','combustible']); S.xray=true; S.brake=true; flyTo(V(900,1050,1300),V(0,560,0)); }
  else if(m==='comb'){ setSys(['estructura','combustible','electronica','distribucion']); S.xray=true; S.brake=false; flyTo(V(700,900,-2300),V(-50,300,-100)); }
  else if(m==='sens'){ setSys(Object.keys(SYS)); S.xray=false; S.brake=false; }
  else { setSys(Object.keys(SYS)); S.xray=false; S.brake=false; }
  $('#xray').checked=S.xray; applyMaterials(); applyVisibility(); syncQuick(); T_items=[]; renderTaller();
}
