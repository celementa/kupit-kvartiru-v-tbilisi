{
  // grow price bars when visible
  const bars=document.querySelectorAll('.bar i[data-w]');
  if(bars.length){
    const grow=()=>bars.forEach(b=>b.style.width=b.dataset.w+'%');
    if('IntersectionObserver' in window){
      const io=new IntersectionObserver(e=>{if(e.some(x=>x.isIntersecting)){grow();io.disconnect()}});
      io.observe(bars[0].closest('.rows'));
    } else grow();
  }
  // label stacked table cells for phones
  for(const t of document.querySelectorAll('table.stack')){
    const h=[...t.rows[0].cells].map(c=>c.textContent.trim());
    for(const r of [...t.rows].slice(1)) [...r.cells].forEach((c,i)=>c.dataset.l=h[i]||'');
  }
  // draft lead forms: nothing is sent yet
  for(const f of document.querySelectorAll('form[data-draft]')){
    f.addEventListener('submit',e=>{e.preventDefault();const ok=f.querySelector('.ok');if(ok)ok.style.display='block'});
  }
  // line chart for /ceny/
  const fig=document.getElementById('pricechart');
  if(fig){
    const s=fig.querySelector('svg');
    const series=JSON.parse(fig.dataset.series);
    const years=[2019,2020,2021,2022,2023,2024,2025];
    const draw=()=>{
      const W=s.clientWidth,H=s.clientHeight,narrow=W<520;
      const L=narrow?40:52,R=narrow?14:24,T=18,B=34;
      const ymin=600,ymax=2000;
      const x=y=>L+(y-years[0])/(years[years.length-1]-years[0])*(W-L-R);
      const yv=v=>T+(1-(v-ymin)/(ymax-ymin))*(H-T-B);
      let g='';
      for(let v=ymin;v<=ymax;v+=narrow?700:350){g+=`<line x1="${L}" x2="${W-R}" y1="${yv(v)}" y2="${yv(v)}" stroke="#d5e4e4"/><text x="${L-8}" y="${yv(v)+4}" text-anchor="end" font-size="12" fill="#4d6268">$${v.toLocaleString('ru-RU').replace(/ /g,' ')}</text>`}
      years.forEach((y,i)=>{if(!narrow||i%2===0)g+=`<text x="${x(y)}" y="${H-10}" text-anchor="middle" font-size="12" fill="#4d6268">${y}</text>`});
      for(const se of series){
        const pts=se.data.map(([y,v])=>`${x(y)},${yv(v)}`).join(' ');
        g+=`<polyline points="${pts}" fill="none" stroke="${se.color}" stroke-width="3" stroke-linejoin="round"/>`;
        for(const [y,v] of se.data){g+=`<circle cx="${x(y)}" cy="${yv(v)}" r="4" fill="#fff" stroke="${se.color}" stroke-width="2.5"/>`}
        const [ly,lv]=se.data[se.data.length-1];
        g+=`<text x="${x(ly)-8}" y="${yv(lv)-12}" text-anchor="end" font-size="13" font-weight="700" fill="${se.color}">$${lv.toLocaleString('ru-RU').replace(/ /g,' ')}</text>`;
      }
      s.innerHTML=g;
    };
    const ro=new ResizeObserver(draw);ro.observe(s);
  }
}
