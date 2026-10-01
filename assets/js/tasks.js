(()=>{"use strict";
const names={ID:"Indonesia",MY:"Malaysia",PH:"Philippines"};
const rewardNames={cash:"Cash",voucher:"Voucher",discount:"Discount",points:"Points",other:"Other"};
const list=document.querySelector("#offer-list"),featured=document.querySelector("#featured-offers");
const countryFilter=document.querySelector("#country-filter"),rewardFilter=document.querySelector("#reward-filter");
const count=document.querySelector("#offer-count"),empty=document.querySelector("#empty-state");
if(!list&&!featured)return;
const target=list||featured;
function esc(v){return String(v??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]))}
function rewardFor(o){
 const r=o.reward;
 if(!r||typeof r!=="object")return {label:String(r||"Reward details pending"),type:"other",verified:false};
 let label=r.label;
 if(!label&&r.amount!==null&&r.amount!==undefined){
   const symbols={USD:"$",IDR:"Rp",MYR:"RM",PHP:"₱"};
   label=(symbols[r.currency]||r.currency+" ")+r.amount+(r.unit?" / "+r.unit:"");
 }
 return {label:label||"Reward details pending",type:r.type||"other",verified:Boolean(r.verified&&r.termsUrl)};
}
function card(o){
 const href="/tasks/"+encodeURIComponent(o.slug)+"/",reward=rewardFor(o);
 return '<article class="offer-card"><div class="offer-card-top"><span class="offer-category"><i class="category-dot"></i>'+esc(o.category||"Remote task")+'</span><span class="country-tag">'+esc((o.countries||[]).map(c=>names[c]||c).join(", "))+'</span></div><h3>'+esc(o.title)+'</h3><p>'+esc(o.description)+'</p><div class="reward-row"><span class="reward-chip"><span aria-hidden="true">✦</span>'+esc(reward.label)+'</span><span class="reward-kind">'+esc(rewardNames[reward.type]||"Other")+(reward.verified?" · provider terms linked":" · demo")+'</span></div><span class="offer-badge">Demo listing · Provider terms apply</span><div class="offer-card-bottom"><span class="offer-type">'+esc(o.type||"Remote task")+'</span><a class="card-link" href="'+href+'">View details <span aria-hidden="true">→</span></a></div></article>'
}
fetch("/data/offers.json",{headers:{"Accept":"application/json"}}).then(r=>{if(!r.ok)throw new Error("Offer data unavailable");return r.json()}).then(data=>{
 const offers=Array.isArray(data.offers)?data.offers:[];
 if(rewardFilter){const selected=rewardFilter.value;rewardFilter.innerHTML='<option value="all">All reward types</option>'+((data.rewardTypes||["cash","voucher","discount","points","other"]).map(type=>'<option value="'+esc(type)+'">'+esc(rewardNames[type]||type)+'</option>').join(""));rewardFilter.value=selected}
 function render(){
  const country=countryFilter?countryFilter.value:"all",rewardType=rewardFilter?rewardFilter.value:"all";
  const available=offers.filter(o=>o.status==="active"&&(country==="all"||(o.countries||[]).includes(country))&&(rewardType==="all"||rewardFor(o).type===rewardType));
  target.innerHTML=available.length?available.map(card).join(""):'<p class="notice">No offers match these filters right now.</p>';
  if(count)count.textContent=available.length+" "+(available.length===1?"offer":"offers")+" available";
  if(empty)empty.hidden=available.length>0
 }
 if(countryFilter)countryFilter.addEventListener("change",render);
 if(rewardFilter)rewardFilter.addEventListener("change",render);
 render()
}).catch(()=>{target.innerHTML='<p class="notice">Offers could not be loaded. Please try again later.</p>';if(count)count.textContent="";if(empty)empty.hidden=true})
})();
