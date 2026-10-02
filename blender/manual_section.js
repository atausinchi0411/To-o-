/* ================= VISOR DE PÁGINAS DEL MANUAL ================= */
function pageSrc(n){ return (window.MANUAL_PAGES&&MANUAL_PAGES[n]) || ('manual/'+n+'.png'); }
function hasPage(n){ return !window.MANUAL_PAGES || !!MANUAL_PAGES[n]; }
let MV={list:[],i:0,z:1};
function openManual(pdfPages,i=0){
  const list=pdfPages.filter(n=>n&&hasPage(n)); if(!list.length) return;
  MV={list,i:Math.min(i,list.length-1),z:1}; $('#mview').hidden=false; drawManual();
}
const printedOf=n=>{ for(const [s,b] of [['TS',300],['V',360],['A',156],['7',144],['6',132],['5',124],['4',110],['3',96],['2',88],['1',42],['E',24]]){ if(s==='A'&&n>=190&&n<=192) return 'A-'+(n-158); if(n>b&&n-b<=60&&!(s==='TS'&&n<303)) return s+'-'+(n-b);} return ''; };
function drawManual(){
  const n=MV.list[MV.i];
  $('#mvimg').src=pageSrc(n); $('#mvimg').style.width=(MV.z*100)+'%';
  $('#mvlab').textContent=`Manual O&M · pág. ${printedOf(n)} · PDF ${n}  (${MV.i+1}/${MV.list.length})`;
  $('#mvprev').disabled=MV.i===0; $('#mvnext').disabled=MV.i===MV.list.length-1;
  $('#mvbody').scrollTop=0;
}
function rangePages(a,b){ const pa=mpage(a), pb=mpage(b||a); if(!pa) return []; const r=[]; for(let n=pa;n<=(pb||pa);n++) r.push(n); return r; }
// Convierte referencias del texto en botones que abren la página del manual
function linkify(txt){
  return String(txt)
   .replace(/(procedimientos?|Procedimiento)\s+(\d{3}-\d{3})/g,(m,w,num)=>PROCMAP[num]?`${w} <button class="mlink" data-mp="${mpage(PROCMAP[num])}">📖 ${num}</button>`:m)
   .replace(/págs?\.\s+((?:TS|[1-7AEV])-\d+)(?:\s*(?:a|y|–|-)\s*((?:TS|[1-7AEV])-\d+))?/g,(m,a,b)=>{const pp=rangePages(a,b); return pp.length?`<button class="mlink" data-mp="${pp.join(',')}">📖 ${m}</button>`:m;});
}
function bindManualLinks(el){ el.querySelectorAll('.mlink').forEach(b=>b.onclick=ev=>{ev.stopPropagation(); openManual(b.dataset.mp.split(',').map(Number));}); }
