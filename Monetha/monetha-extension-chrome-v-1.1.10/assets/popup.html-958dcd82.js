import{r as o,u as h,b as c,j as t,S as g,B as u,d as w,M as v,F as k,A as z,c as y,i as L,f as N}from"./inject-93900a55.js";import{s as x,w as j,d as C,o as d,x as b,A as M,y as E,z as q}from"./constants-0ac025b2.js";(function(){const r=document.createElement("link").relList;if(r&&r.supports&&r.supports("modulepreload"))return;for(const s of document.querySelectorAll('link[rel="modulepreload"]'))a(s);new MutationObserver(s=>{for(const n of s)if(n.type==="childList")for(const l of n.addedNodes)l.tagName==="LINK"&&l.rel==="modulepreload"&&a(l)}).observe(document,{childList:!0,subtree:!0});function i(s){const n={};return s.integrity&&(n.integrity=s.integrity),s.referrerPolicy&&(n.referrerPolicy=s.referrerPolicy),s.crossOrigin==="use-credentials"?n.credentials="include":s.crossOrigin==="anonymous"?n.credentials="omit":n.credentials="same-origin",n}function a(s){if(s.ep)return;s.ep=!0;const n=i(s);fetch(s.href,n)}})();const S=e=>o.createElement("svg",{width:16,height:16,viewBox:"0 0 16 16",fill:"none",xmlns:"http://www.w3.org/2000/svg",...e},o.createElement("path",{d:"M6.66667 14.6667H3.33333C2.59695 14.6667 2 14.0698 2 13.3334V2.66671C2 1.93033 2.59695 1.33337 3.33333 1.33337H6.66667",stroke:"#1F2025",strokeWidth:1.5,strokeLinecap:"round",strokeLinejoin:"round"}),o.createElement("path",{d:"M11.333 10.6667L13.9997 8.00004L11.333 5.33337",stroke:"#1F2025",strokeWidth:1.5,strokeLinecap:"round",strokeLinejoin:"round"}),o.createElement("path",{d:"M14 8H6",stroke:"#1F2025",strokeWidth:1.5,strokeLinecap:"round",strokeLinejoin:"round"})),A=()=>{const[e]=h("user",x);return o.useEffect(()=>{j()},[]),[e]},B=({showLogout:e})=>{var l,m,p,f;const[r]=A(),i=()=>{C()?b():d(M)},a=()=>{d("https://www.monetha.io/account/wallet")},s=()=>{d("https://www.monetha.io/")},n=()=>d("https://www.monetha.io/account/boost-level");return c("div",{className:"ex-h1tqi ex-hlz9g ex-clx8j ex-lhnj4 ex-mfxwf ex-dlcew ex-puydv ex-otw6a ex-e8btz ex-htgio ex-vdv43",children:[t(g,{className:"ex-pqzfh ex-ehrfd",onClick:s}),!r&&t(u,{onClick:i,variant:"small",children:"Login"}),r&&typeof r!="string"&&c("div",{className:"ex-mfxwf ex-zsz2e",children:[((l=r.balance)==null?void 0:l.approvedTokens)!==void 0?c("div",{className:"ex-gjyki ex-mfxwf ex-pqzfh ex-zsz2e",onClick:a,children:[t("div",{className:" ex-mj0yl ex-gw7gf ex-xwhf0 ex-zwtf3",children:(m=r.balance)==null?void 0:m.approvedTokens}),t(w,{className:"ex-letj4 ex-tfl3x"})]}):null,t("div",{className:"ex-mj0yl ex-pqzfh",onClick:n,children:(p=r.progress)==null?void 0:p.level.name}),((f=r.progress)==null?void 0:f.level.icon)&&t("img",{className:"ex-netqn ex-z8w7y ex-pqzfh",src:r.progress.level.icon,alt:"level",onClick:a}),t(S,{className:"ex-qwhqx ex-pqzfh",onClick:e})]})]})},H=e=>o.createElement("svg",{width:24,height:24,viewBox:"0 0 24 24",fill:"none",xmlns:"http://www.w3.org/2000/svg",...e},o.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z",stroke:"white",strokeWidth:2,strokeLinecap:"round",strokeLinejoin:"round"}),o.createElement("path",{d:"M15 9L9 15",stroke:"white",strokeWidth:2,strokeLinecap:"round",strokeLinejoin:"round"}),o.createElement("path",{d:"M9 9L15 15",stroke:"white",strokeWidth:2,strokeLinecap:"round",strokeLinejoin:"round"})),P=()=>c("div",{className:"ex-t4oc1 ex-clx8j ex-lhnj4 ex-mfxwf ex-zsz2e ex-dysg1 ex-lytsa ex-f8tzc ex-vdv43",children:[t(H,{className:"ex-yzjn4 ex-z8w7y"}),t("span",{className:"ex-tqm3d ex-cdzzv ex-tsx51",children:"No rewards on this website"})]}),W=()=>{const[e]=h("topMerchants",x),[r]=h("user",x),i=()=>{d("https://www.monetha.io/shops?utm_source=monetha&utm_medium=extension")};return e!=null&&e.length?c("div",{className:"ex-rs64g ex-sothe",children:[t("div",{className:"ex-gw7gf ex-xwhf0 ex-z3ep2",children:"Top deals"}),t("div",{className:" ex-gvryz ex-x584t ex-a9kxl ex-kaw8o",children:e.map(a=>t(v,{merchant:a,user:r},a.id))}),t("button",{className:"ml-[calc(50%-58px)] ex-gvryz ex-jta75 ex-gwkeo ex-dtlp0 ex-otw6a ex-knsj6 ex-kxcd4 ex-m6i8z ex-s8ddp ex-bn33m",onClick:i,children:"See more shops"})]}):null},I=()=>{const[e,r]=o.useState(),[i]=h("activationData",x),a=o.useMemo(()=>{if(!(!i||!i.length||!e))return i.find(n=>n.merchantId===e.id)},[i,e]),s=async()=>{const n=await E();if(!n)return;const{actualMerchant:l}=n;r(l)};return o.useEffect(()=>{s()},[]),c(k,{children:[e?t(z,{merchant:e,className:"ex-kvdqb",isActivated:!!(a!=null&&a.activated),fromPopup:!0}):t(P,{}),t(W,{})]})},O="/assets/background_cropped-f508cc6f.png",R=({showMain:e})=>t("div",{className:" ex-mfxwf ex-dysg1 ex-i2gw4 ex-s07mq",children:c("div",{className:"ex-sx9c9 ex-mfxwf ex-eu84z ex-dysg1 ex-jocbz ex-yt66b ex-cccc0 ex-t041t ex-sji4v ex-x7glj ex-soqxu ex-vdv43",children:[t(y,{className:"ex-xjzol ex-bkn6d ex-xseut ex-pqzfh",onClick:e}),t("h1",{className:"ex-ml33o ex-bsjak",children:"Are you sure you want to log out?"}),t(u,{className:"ex-tep8s",onClick:e,children:"Stay logged in"}),t(u,{className:"ex-gvryz",color:"transparent",onClick:()=>{e(),q()},children:"Log me out"})]})}),T=e=>o.createElement("svg",{viewBox:"0 0 24 24",fill:"none",xmlns:"http://www.w3.org/2000/svg",...e},o.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M10.2908 4.85996L1.82075 19C1.46539 19.6154 1.46327 20.3731 1.81518 20.9905C2.16709 21.6079 2.82017 21.9922 3.53075 22H20.4708C21.1813 21.9922 21.8344 21.6079 22.1863 20.9905C22.5382 20.3731 22.5361 19.6154 22.1808 19L13.7108 4.85996C13.3482 4.26224 12.6998 3.89722 12.0008 3.89722C11.3017 3.89722 10.6533 4.26224 10.2908 4.85996Z",stroke:"white",strokeWidth:2,strokeLinecap:"round",strokeLinejoin:"round"}),o.createElement("path",{d:"M12 10V14",stroke:"white",strokeWidth:2,strokeLinecap:"round",strokeLinejoin:"round"}),o.createElement("ellipse",{cx:12,cy:18,rx:1,ry:1,fill:"white"})),F=e=>o.createElement("svg",{viewBox:"0 0 24 24",fill:"none",xmlns:"http://www.w3.org/2000/svg",...e},o.createElement("path",{d:"M18 6L6 18",stroke:"white",strokeLinecap:"round",strokeLinejoin:"round"}),o.createElement("path",{d:"M6 6L18 18",stroke:"white",strokeLinecap:"round",strokeLinejoin:"round"})),V=e=>o.createElement("svg",{viewBox:"0 0 16 16",fill:"none",xmlns:"http://www.w3.org/2000/svg",...e},o.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M6 8C6 6.89543 6.89543 6 8 6H12.6667C13.7712 6 14.6667 6.89543 14.6667 8V12.6667C14.6667 13.7712 13.7712 14.6667 12.6667 14.6667H8C6.89543 14.6667 6 13.7712 6 12.6667V8Z",stroke:"white",strokeLinecap:"round",strokeLinejoin:"round"}),o.createElement("path",{d:"M3.33301 10H2.66634C1.92996 10 1.33301 9.40309 1.33301 8.66671V2.66671C1.33301 1.93033 1.92996 1.33337 2.66634 1.33337H8.66634C9.40272 1.33337 9.99967 1.93033 9.99967 2.66671V3.33337",stroke:"white",strokeLinecap:"round",strokeLinejoin:"round"})),_=()=>{const[e,r]=h("HttpError",x),i=n=>{navigator.clipboard.writeText(n)},a=()=>{r("")},s=o.useMemo(()=>{if(!e)return null;try{return JSON.parse(e)}catch(n){console.log("error parsing message",n)}},[e]);return s?c("div",{className:"ex-h1tqi ex-gi2fs ex-nnhmw ex-r5v16 ex-sn63c ex-jocbz ex-tsx51 ex-soqxu ex-vdv43",children:[t(F,{className:"ex-xjzol ex-bkn6d ex-bu6ew ex-z8w7y ex-pqzfh",onClick:a}),c("div",{className:"ex-mfxwf ex-zsz2e ex-j15w4 ex-cccc0 ex-f8tzc",children:[t(T,{className:"ex-yzjn4 ex-z8w7y"}),t("span",{className:"ex-gw7gf ex-xwhf0",children:s.title})]}),c("div",{className:"ex-p3gna ex-cccc0 ex-f8tzc ex-zu1yt ex-cdzzv",children:[c("p",{children:["Share this with"," ",t("a",{className:"ex-v5fo6",href:"mailto:support@monetha.io",children:"support@monetha.io"}),":"]}),t("p",{className:"ex-w37ak ex-h6mnw",children:s.body})]}),c("div",{className:"ex-xjzol ex-el1p9 ex-e7rd0 ex-mfxwf ex-pqzfh ex-zsz2e",onClick:()=>i(s.body),children:[t("span",{className:"ex-mj0yl ex-zu1yt ex-cdzzv",children:"Copy"}),t(V,{className:" ex-dvt50"})]})]}):null},U=()=>{const[e,r]=o.useState(!0);return c("div",{className:"ex-sx9c9 ex-bb33z ex-b2ipl  ex-sn63c",children:[t(B,{showLogout:()=>r(!1)}),c("div",{className:"ex-opyet ex-rw1nd ex-rf5tb",children:[t(_,{}),t("img",{src:O,alt:"",className:"ex-h1tqi ex-deob8 ex-clx8j -z-10 ex-twv35"}),e?t(I,{}):t(R,{showMain:()=>r(!0)})]})]})};async function D(){L(),await x.init(),N.createRoot(document.getElementById("monetha-popup-root")).render(t(U,{}))}D().then().catch(e=>console.log(e));
