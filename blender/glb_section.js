/* ---------- MODELO DE BLENDER (GLB embebido) ---------- */
const EXPL_GROUP={tapa_balancines:'cover',culata:'head',ganchos_izado:'head',eje_balancines:'valvetrain',
  bloque:'block',camisas:'block',tapas_bancada:'block',soporte_delantero:'block',
  arbol_levas:'cam',carter:'pan',
  colector_admision:'intake',ecm:'intake',bomba_combustible:'intake',filtro_combustible:'intake',cabezal_filtro_comb:'intake',compresor_aire:'intake',tuberia_combustible:'intake',abrazaderas:'intake',
  colector_escape:'exhaust',juntas_colector:'exhaust',enfriador_aceite:'exhaust',filtros_aceite:'exhaust',tuberia_aceite_turbo:'exhaust',
  turbo:'turbo',rueda_turbina:'turbo',rueda_compresor:'turbo',codo_escape:'turbo',codo_filtro_aire:'turbo',conducto_aire:'turbo',
  carcasa_engranajes:'front',alternador:'front',cubo_ventilador:'front',tensor:'front',correa:'front',bomba_agua:'front',carcasa_termostato:'front',
  carcasa_volante:'rear',motor_arranque:'rear'};
const SHELL=new Set(['bloque','culata','tapa_balancines','carter','carcasa_engranajes','carcasa_volante','colector_admision','colector_escape','enfriador_aceite','camisas']);
const CAT='Catálogo de partes QSM11';
const INFO={
  bloque:['Bloque motor','Cylinder block','Estructura principal. Aloja los 6 cilindros, el cigüeñal, el árbol de levas, las camisas de agua y las galerías de aceite.','cat. 8 · O&M 25–39',['6 cilindros en línea, calibre 125 mm'],['Largo 946 mm (ficha técnica, sin verificar)','Forma exterior simplificada a partir del despiece']],
  camisas:['Camisas de cilindro','Cylinder liners','Superficie por la que se desliza cada pistón. Son camisas húmedas: el refrigerante las rodea por fuera.','cat. 10 · O&M 361',['Diámetro interior 125 mm','Carrera 147 mm'],['Espesor y collar superior']],
  tapas_bancada:['Tapas de bancada','Main bearing caps','Sujetan el cigüeñal al bloque en sus 7 apoyos.','cat. 12',['7 apoyos de bancada'],['Forma y tornillería']],
  culata:['Culata (una pieza)','Cylinder head','Cierra los 6 cilindros. Contiene las 24 válvulas, los conductos de admisión y escape y los inyectores.','cat. 94 · O&M 361',['Culata única para los 6 cilindros','4 válvulas por cilindro'],['Altura y forma de los puertos']],
  tapa_balancines:['Carcasa y tapa de balancines','Rocker housing and cover','Protege el tren de válvulas y retiene el aceite. Lleva el tapón de llenado de aceite y el respiradero.','O&M 25, 37',[],['Nervios y forma redondeada']],
  carcasa_engranajes:['Carcasa y tapa de engranajes delantera','Gear housing and front cover','Aloja los engranajes que sincronizan el cigüeñal con el árbol de levas (que gira a la mitad).','cat. 14, 56',[],['Contorno aproximado del despiece']],
  carcasa_volante:['Carcasa del volante SAE 2','Flywheel housing','Envuelve el volante y sirve de brida para acoplar la transmisión. Incluye el alojamiento del motor de arranque.','cat. 44, 54',['Carcasa SAE n.º 2','Motor de arranque a 243,84 mm del eje'],['Nervios y patas de apoyo']],
  carter:['Cárter de aceite','Oil pan','Depósito del aceite lubricante, con sumidero profundo y varilla de nivel.','cat. 82, 74',[],['Profundidad y posición del sumidero']],
  soporte_delantero:['Soporte delantero','Front engine support','Apoyo delantero del motor, de acero fabricado con escuadras.','cat. 36',['Apoyo a 206 mm bajo el eje del cigüeñal','A 149 mm del frente del bloque'],['Espesores']],
  ganchos_izado:['Ganchos de izado','Lifting brackets','Puntos para levantar el motor con grúa.','cat. 66',[],['Forma']],
  ciguenal:['Cigüeñal','Crankshaft','Convierte el movimiento de los pistones en giro. 7 apoyos, 6 muñequillas y 12 contrapesos. Gira en sentido horario visto desde el frente.','cat. 11 · O&M 361',['Radio de manivela 73,5 mm','Orden 1-5-3-6-2-4, giro horario'],['Diámetros de apoyos y forma de contrapesos']],
  amortiguador_polea:['Amortiguador de vibraciones y polea','Vibration damper and crank pulley','Absorbe las vibraciones de torsión del cigüeñal. La polea mueve la correa de accesorios.','cat. 26',['Polea Ø190,7 mm, poly-V de 8 canales','Correa a 140 mm del frente del bloque'],['Diámetro del amortiguador']],
  volante:['Volante de inercia','Flywheel','Suaviza el giro entre combustiones. Su corona dentada engrana con el motor de arranque.','cat. 54',['Agujero piloto Ø72 mm','Para carcasa SAE 2'],['Diámetro y número de dientes']],
  piston:['Pistón','Piston','Recibe la presión de la combustión. Tiene la cámara (bowl) en la cabeza y tres segmentos.','cat. 90 · O&M 361',['Diámetro 125 mm','Carrera 147 mm'],['Altura 120 mm y altura de compresión 80 mm','Forma del bowl']],
  biela:['Biela','Connecting rod','Une el pistón con el cigüeñal. Su tapa tiene corte diagonal, como en el despiece.','cat. 88',['Corte diagonal de la cabeza de biela'],['Longitud 260 mm (ajustable en Datos)']],
  arbol_levas:['Árbol de levas','Camshaft','Gira a la mitad de velocidad que el cigüeñal. Tiene 3 levas por cilindro: admisión, escape e inyector.','cat. 92, 18',['Árbol de levas en el bloque con seguidores'],['Perfil de levas DESCONOCIDO']],
  valvulas:['Válvulas','Valves','Abren y cierran el paso de aire (admisión) y de gases (escape). Dos de cada tipo por cilindro, unidas por una cruceta.','cat. 94 · O&M 361',['2 + 2 válvulas por cilindro'],['Diámetro 42 mm, alzada 14 mm','Apertura idealizada de 180°']],
  muelles:['Muelles de válvula','Valve springs','Cierran la válvula cuando la leva deja de empujar.','cat. 94',[],['Dimensiones']],
  balancin:['Balancín','Rocker lever','Palanca que transmite el empuje de la varilla a la válvula o al inyector.','cat. 18',[],['Geometría simplificada']],
  varilla:['Varilla de empuje','Push tube','Lleva el movimiento del seguidor de leva, en el bloque, hasta el balancín.','cat. 18',[],['Longitud']],
  eje_balancines:['Eje de balancines','Rocker shaft','Eje sobre el que pivotan los balancines.','cat. 94',[],['Diámetro']],
  inyector:['Inyector','Fuel injector','Pulveriza el combustible a alta presión al final de la compresión. Es accionado por su propia leva.','cat. 96',['Un inyector por cilindro'],['Forma simplificada']],
  colector_admision:['Colector de admisión','Air intake manifold','Reparte el aire comprimido entre los 6 cilindros. La entrada de aire va arriba.','cat. 60, 62',['Entrada de aire superior'],['Sección y posición']],
  conducto_aire:['Conducto de aire turbo → colector','Air transfer tube','Lleva el aire comprimido por el turbo hasta el colector de admisión.','cat. 58, 59, 64',['Manguera Ø102 mm'],['Recorrido']],
  abrazaderas:['Abrazaderas','Clamps','Sujetan las mangueras de aire.','cat. 59',[],[]],
  colector_escape:['Colector de escape','Exhaust manifold','Recoge los gases de los 6 cilindros y los lleva al turbo.','O&M 215–218',[],['Forma y sección']],
  juntas_colector:['Juntas del colector','Slip joints','Permiten que el colector se dilate con el calor.','—',[],['Forma']],
  turbo:['Turbocompresor con wastegate','Turbocharger','Los gases de escape giran la turbina; un eje común mueve el compresor, que comprime el aire de admisión. La wastegate limita la presión.','cat. 98–100',['Turbo con wastegate','Brida con tornillos en círculo de Ø129,06 mm'],['Tamaño de las volutas']],
  rueda_turbina:['Rueda de turbina','Turbine wheel','La mueven los gases de escape.','cat. 98',[],['Álabes simplificados; giro solo visual']],
  rueda_compresor:['Rueda del compresor','Compressor wheel','Comprime el aire de admisión.','cat. 98',[],['Álabes simplificados; giro solo visual']],
  codo_escape:['Salida de escape','Exhaust outlet','Conduce los gases desde la turbina hacia el sistema de escape.','—',[],['Recorrido']],
  codo_filtro_aire:['Codo del filtro de aire','Air cleaner elbow','Conecta el filtro de aire con la entrada del compresor.','cat. 22',[],['Recorrido']],
  ecm:['ECM (módulo de control)','Electronic Control Module','Ordenador del motor: decide cuánto combustible inyectar y cuándo. Se enfría con combustible por la placa trasera.','cat. 84',['Placa de refrigeración por combustible'],['Tamaño']],
  bomba_combustible:['Bomba de combustible','Fuel pump','Envía el combustible a presión hacia los inyectores. Sus actuadores la controla el ECM.','cat. 46–50',[],['Forma simplificada']],
  filtro_combustible:['Filtro de combustible','Fuel filter','Retiene partículas y agua del combustible.','cat. 40',[],['Posición']],
  cabezal_filtro_comb:['Cabezal del filtro de combustible','Fuel filter head','Soporte del filtro.','cat. 40',[],['Forma']],
  tuberia_combustible:['Tuberías de combustible','Fuel lines','Llevan el combustible entre filtro, bomba y culata.','cat. 52',[],['Recorrido']],
  compresor_aire:['Compresor de aire','Air compressor','Produce aire comprimido para frenos o servicios. Se lubrica con aceite del motor.','O&M 368 · cat. 24–25',['18,7 CFM: 217 × 142 × 216 mm'],['Posición']],
  motor_arranque:['Motor de arranque','Starting motor','Engrana con la corona del volante para arrancar el motor.','cat. 54',['Centro a 243,84 mm del eje del cigüeñal'],['Tamaño']],
  enfriador_aceite:['Cabezal de filtro y enfriador de aceite','Oil filter cooler head','Enfría el aceite con el refrigerante del motor y aloja los filtros.','cat. 68–72',[],['Forma y posición']],
  filtros_aceite:['Filtros de aceite','Oil filters','Limpian el aceite antes de las galerías.','cat. 72',[],['Tamaño']],
  tuberia_aceite_turbo:['Aceite del turbo','Turbo oil supply/drain','Alimenta y drena el aceite de los cojinetes del turbo.','—',[],['Recorrido']],
  alternador:['Alternador','Alternator','Genera electricidad para cargar las baterías.','cat. 31–34',['Delco Remy 22SI, largo 162 mm','Polea Ø76,2 mm'],['Posición']],
  cubo_ventilador:['Cubo y polea del ventilador','Fan hub and pulley','Mueve el ventilador del radiador (en marino se usa como polea de accionamiento).','cat. 38',['Polea Ø190 mm','Centro a 215,9 mm sobre el cigüeñal, 19 mm hacia la bomba'],[]],
  tensor:['Tensor de correa','Belt tensioner','Mantiene la correa tensa.','cat. 33',[],['Posición']],
  correa:['Correa poly-V','Drive belt','Transmite el giro del cigüeñal al ventilador y al alternador.','cat. 39',[],['Recorrido aproximado']],
  bomba_agua:['Bomba de agua','Water pump','Hace circular el refrigerante por bloque, culata y radiador o intercambiador.','O&M 164–169',[],['Posición y tamaño']],
  carcasa_termostato:['Carcasa del termostato','Thermostat housing','Regula la temperatura del motor enviando el refrigerante al radiador o de vuelta a la bomba.','cat. 30',[],['Forma']],
};
const ST={V:'ver',C:'sim',E:'est'};
function infoFor(name,ud){
  const cyl=+(name.match(/_(\d)$/)||[])[1]||0;
  let base=name.replace(/_\d$/,'').replace(/_(adm|esc|iny)$/,'');
  const kind=(name.match(/_(adm|esc|iny)_/)||[])[1];
  const d=INFO[base]||[name,'','','—',[],[]];
  let es=d[0], en=d[1];
  if(kind) es+=' de '+({adm:'admisión',esc:'escape',iny:'inyector'}[kind]);
  if(cyl){es+=' · cilindro '+cyl; en+=' · cylinder '+cyl;}
  return {es,en,sys:ud.sistema||'estructura',cyl:cyl||undefined,st:ST[ud.estado]||'est',page:d[3],fn:d[2],ver:d[4],est:d[5]};
}
const pistons={}, rods={}, gas={}, spray={}, valves=[], rockers=[], pushrods=[], springs=[], turboWheels=[];
let camShaft;
function buildFromGLB(root){
  const nodes=[...root.children];
  nodes.forEach(n=>{
    const name=n.name; const ud=n.userData||{};
    let grp=EXPL_GROUP[name];
    if(!grp){
      if(/^(piston|biela)_/.test(name)) grp='pistons';
      else if(/^(valvulas|muelles|balancin)_/.test(name)) grp='valvetrain';
      else if(/^varilla_/.test(name)) grp='push';
      else if(/^inyector_/.test(name)) grp='head';
    }
    const parent=['ciguenal','amortiguador_polea','volante'].includes(name)?crankRot:(G[grp]||G.block);
    parent.add(n);
    n.userData={partId:name,mats:{},shell:SHELL.has(name),sys:ud.sistema||'estructura'};
    parts[name]=n; PI_[name]=infoFor(name,ud);
    n.traverse(o=>{ if(!o.isMesh) return;
      const k=o.material.name||'m'; let m=n.userData.mats[k];
      if(!m){ m=o.material.clone(); m.side=T.DoubleSide; m.envMapIntensity=.55; m.userData={shell:n.userData.shell}; n.userData.mats[k]=m; allMats.push(m); }
      o.material=m; o.castShadow=true; o.receiveShadow=true; o.userData.part=n; pickables.push(o);
    });
    let mm;
    if(mm=name.match(/^piston_(\d)$/)) pistons[+mm[1]]=n;
    else if(mm=name.match(/^biela_(\d)$/)){ rods[+mm[1]]=n; }
    else if(mm=name.match(/^valvulas_(adm|esc)_(\d)$/)) valves.push({g:n,c:+mm[2],k:mm[1]==='adm'?'in':'ex',y0:n.position.y});
    else if(mm=name.match(/^balancin_(adm|esc|iny)_(\d)$/)) rockers.push({g:n,c:+mm[2],k:{adm:'in',esc:'ex',iny:'inj'}[mm[1]],arm:115});
    else if(mm=name.match(/^varilla_(adm|esc|iny)_(\d)$/)) pushrods.push({m:n,c:+mm[2],k:{adm:'in',esc:'ex',iny:'inj'}[mm[1]],y0:n.position.y});
    else if(name==='arbol_levas') camShaft=n;
    else if(/^rueda_/.test(name)) turboWheels.push(n);
  });
  // columnas de gas (ciclo) y chorro de inyección: efectos visuales
  for(let c=1;c<=6;c++){
    const gm=new T.MeshBasicMaterial({color:0x4fe3f0,transparent:true,opacity:.2,depthWrite:false,side:T.DoubleSide});
    allMats.push(gm); gm.userData={fx:true};
    const gc=new T.Mesh(cylG(61,61,1,'y',36),gm); gc.position.x=XC(c); G.pistons.add(gc); gas[c]=gc;
    const sm=new T.MeshBasicMaterial({color:0xffd27a,transparent:true,opacity:0,depthWrite:false,blending:T.AdditiveBlending});
    allMats.push(sm); sm.userData={fx:true};
    const sp=new T.Mesh(new T.ConeGeometry(42,46,24,1,true),sm); sp.position.set(XC(c),DECK-24,0); G.head.add(sp); spray[c]=sp;
  }
}
buildFromGLB(GLB_ROOT);
