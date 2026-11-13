(function(){
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
const bg=$('#burger'),menu=$('#menu');
if(bg)bg.onclick=()=>{const o=menu.classList.toggle('open');bg.setAttribute('aria-expanded',o)};
$$('#menu a').forEach(a=>a.addEventListener('click',()=>{menu.classList.remove('open');bg&&bg.setAttribute('aria-expanded',false)}));
const bar=$('#bar');addEventListener('scroll',()=>{const h=document.documentElement;if(bar)bar.style.width=scrollY/(h.scrollHeight-innerHeight||1)*100+'%'},{passive:true});
if('IntersectionObserver'in window){const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('on');io.unobserve(e.target)}}),{threshold:.12});$$('.rv').forEach(e=>io.observe(e))}else $$('.rv').forEach(e=>e.classList.add('on'));
$$('.tc').forEach(b=>b.onclick=()=>{const o=b.getAttribute('aria-expanded')==='true';b.setAttribute('aria-expanded',!o)});
const ort=$('#ort'),sv=$('#ortsvar');
if(ort)ort.onchange=()=>{const v=ort.value,n=ort.selectedOptions[0].textContent;sv.className='svar';
 if(!v){sv.textContent='Välj din ort så ser du direkt om den finns bland Mias besöksorter.';return}
 if(v==='annan'){sv.classList.add('no');sv.innerHTML='Orten finns inte i listan, men hör av dig ändå så svarar Mia om det går att ordna. <a href="kontakt.html">Skriv till Mia</a>';return}
 sv.classList.add('ok');sv.innerHTML='Ja, Mia gör hembesök i '+n+'. <a href="fotvard-'+v+'.html">Läs mer om fotvård i '+n+'</a> eller <a href="kontakt.html">fråga om en tid</a>.'};
const fc=$$('.fc'),q=$('#q'),list=$('#list');
function filt(){if(!list)return;const c=($('.fc.on')||{}).dataset?.c||'Alla',t=(q.value||'').toLowerCase();let n=0;$$('.story',list).forEach(s=>{const ok=(c==='Alla'||s.dataset.cat===c)&&s.dataset.t.includes(t);s.hidden=!ok;if(ok)n++});$('#none').hidden=n>0}
fc.forEach(b=>b.onclick=()=>{fc.forEach(x=>x.classList.remove('on'));b.classList.add('on');filt()});if(q)q.oninput=filt;
const toc=$('#toc');if(toc){const hs=$$('.prose h2');hs.forEach(h=>{const li=document.createElement('li'),a=document.createElement('a');a.href='#'+h.id;a.textContent=h.textContent;li.append(a);toc.append(li)});
 addEventListener('scroll',()=>{let cur=null;hs.forEach(h=>{if(h.getBoundingClientRect().top<160)cur=h.id});$$('a',toc).forEach(a=>a.classList.toggle('on',a.getAttribute('href')==='#'+cur))},{passive:true})}
const f=$('#req');if(f)f.onsubmit=e=>{e.preventDefault();const g=i=>$('#'+i).value.trim(),m=$('#fmsg');
 if(!g('f-n')||!g('f-o')){m.textContent='Fyll i namn och ort så vet Mia vad det gäller.';return}
 const body='Hej Mia!\n\nJag heter '+g('f-n')+' och bor i '+g('f-o')+'.\nJag vill ha hjälp med: '+g('f-b')+'.\n'+($('#f-c').checked?'Jag bokar åt en närstående.\n':'')+(g('f-m')?'\n'+g('f-m')+'\n':'')+'\nVad kostar ett besök och vilka tider finns?\n\nHälsningar,\n'+g('f-n');
 m.textContent='Öppnar ett färdigt mejl i din mejlapp. Inget skickas förrän du trycker på skicka.';
 location.href='mailto:miaalineus.fotvard@gmail.com?subject='+encodeURIComponent('Fråga om hembesök i '+g('f-o'))+'&body='+encodeURIComponent(body)};
})();
