import{d as i,r as _,a as p,b as m,e as s,f as g,i as f,u as y,z as o,J as h,K as x,o as k,M as b}from"./index-bBROF-nZ.js";const w={class:"about"},M=i({__name:"AboutView",setup(v){const r=async()=>{try{const e=await o.post("/api/rs/check_update"),a=e.latest_version,n=e.msg,l=e.latest_url,u=`${n}：${a} 
 ${l||""}`;x.alert(u,"info",{confirmButtonText:"确认",callback:d=>{h({type:"info",message:`action: ${d}`})}})}catch{return[]}},t=_("# 加载中"),c=async()=>{try{const e=await o.post("/api/rs/get_readme");t.value=e}catch{return[]}};return p(()=>{c()}),(e,a)=>(k(),m("div",w,[s("h1",{id:"-center-pywxdump-center-",style:{"text-align":"center"}},[g(" PyWxDump"),s("a",{onClick:r,target:"_blank",style:{float:"right","margin-right":"30px"}},"检查更新")]),f(y(b),{source:t.value,style:{"background-color":"#d2d2fa"}},null,8,["source"])]))}});export{M as default};
