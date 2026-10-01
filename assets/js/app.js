(()=>{"use strict";
const toggle=document.querySelector(".menu-toggle"),nav=document.querySelector("#primary-nav");
if(toggle&&nav){
  toggle.addEventListener("click",()=>{
    const open=toggle.getAttribute("aria-expanded")==="true";
    toggle.setAttribute("aria-expanded",String(!open));
    toggle.setAttribute("aria-label",open?"Open navigation":"Close navigation");
    nav.classList.toggle("is-open",!open)
  });
  nav.addEventListener("click",e=>{
    if(e.target.closest("a")){
      toggle.setAttribute("aria-expanded","false");
      toggle.setAttribute("aria-label","Open navigation");
      nav.classList.remove("is-open")
    }
  })
}
document.querySelectorAll("[data-year]").forEach(el=>el.textContent=String(new Date().getFullYear()));
// Histats asynchronous site analytics.
window._Hasync=window._Hasync||[];
window._Hasync.push(["Histats.start","1,5053693,4,0,0,0,00010000"]);
window._Hasync.push(["Histats.fasi","1"]);
window._Hasync.push(["Histats.track_hits",""]);
const hs=document.createElement("script");
hs.type="text/javascript";
hs.async=true;
hs.src="https://s10.histats.com/js15_as.js";
(document.head||document.body).appendChild(hs);
})();
