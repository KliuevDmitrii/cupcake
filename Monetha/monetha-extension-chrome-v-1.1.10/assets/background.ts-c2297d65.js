var E=Object.defineProperty;var p=(s,e,t)=>e in s?E(s,e,{enumerable:!0,configurable:!0,writable:!0,value:t}):s[e]=t;var o=(s,e,t)=>(p(s,typeof e!="symbol"?e+"":e,t),t);import{s as n,H as T,e as I,f as U,d as v,A as y,I as D,j as k,k as L,m as N,n as R,p as P,q as H,r as O,t as C,u as S,v as w}from"./constants-0ac025b2.js";import{c as M,g as b}from"./getInterstitialUrl-dcf73a8a.js";var g=(s=>(s.TOP_MERCHANTS="merchants/high-rewards",s.LOGIN="login",s.GET_MERCHANTS_BY_URL="merchant/lookup",s.ALL_MERCHANTS="merchants",s.USER_PROGRESS="user/progress",s.USER_BALANCE="wallet/balance",s.VERIFY_TOKEN="user/v1/token/verify",s.REFRESH_TOKEN="user/v1/token/refresh",s))(g||{});const B=(s,e,t)=>{const a=new URL(e),r={400:{title:"An error has occurred",body:`Malformed request for ${a.pathname}${a.search}`},401:{title:"An error has occurred",body:`Unauthorized to access ${a.pathname}${a.search}`},403:{title:"An error has occurred",body:`Forbidden to access ${a.pathname}${a.search}`},404:{title:"An error has occurred",body:`Resource ${a.pathname}${a.search} not found`},500:{title:"Unexpected error has occurred",body:t}};return r[s]?r[s]:{title:"Unexpected error has occurred",body:t}};class ${constructor(e){this.baseUrl=e}setHeaders(e,t){e||(e={}),e.headers||(e.headers={}),Object.assign(e.headers,t)}async fetchWithRetries(e,t="GET",a=!1,r,c){let h=0,f=c;const i=n.get("tokens");for(i!=null&&i.access_token&&this.setHeaders(f,{"X-User-Authorization":`Bearer ${i.access_token}`});h<r;){try{const l=await fetch(e,{method:t,headers:{"Content-Type":"application/json"},...f});if(l.ok)return await l.json();if(l.status>=400&&l.status<500){const d=await this.verifyTokens();if(!d)return Promise.reject();this.setHeaders(f,{"X-User-Authorization":`Bearer ${d}`})}else{const d=await l.text(),A=JSON.parse(d).message,_=B(l.status,l.url,A);throw n.set("HttpError",JSON.stringify(_)),new Error(`HTTP error ${l.status}: ${d}`)}}catch(l){console.error(`Fetch error (retry ${h+1}): ${l}`)}h++}throw new Error(`Failed to fetch ${e} after ${r} retries`)}validate(e){if(e.status===200)return e.response;throw new Error(`Internal API error: ${e}`)}async refreshTokens(e){const t=`${T}/${g.REFRESH_TOKEN}`,a={};a.body=JSON.stringify({refresh_token:e}),a.headers={"Content-Type":"application/json"};try{const r=await fetch(t,{method:"POST",headers:{"Content-Type":"application/json"},...a});if(r.ok){const c=await r.json();return n.set("tokens",{access_token:c.new_access_token,refresh_token:c.new_refresh_token}),c.new_access_token}else return}catch(r){console.log("fail refresh token: ",r)}}async verifyTokens(){const e=n.get("tokens"),t=`${T}/${g.VERIFY_TOKEN}`;if(!(e!=null&&e.access_token)||!(e!=null&&e.refresh_token))return;const a={};a.headers={"Content-Type":"application/json"},a.body=JSON.stringify({access_token:e.access_token});try{const r=await fetch(t,{method:"POST",...a});if(r.ok){const c=await r.json();return c&&n.set("userId",c.user_id),e.access_token}else return this.refreshTokens(e.refresh_token)}catch(r){console.log("fail verify token: ",r);return}}async fetch(e,t="GET",a,r=!1,c=1,h={}){let f=`${this.baseUrl}/${e}`;const i=!a||a&&!Object.keys(a).length;if(t==="GET"&&!i){const l=new URLSearchParams(Object.entries(a).map(([d,A])=>[d,A.toString()])).toString();f+=`?${l}`}return t==="POST"&&!i&&(h.body=JSON.stringify(a)),h.headers={"Content-Type":"application/json"},this.fetchWithRetries(f,t,r,r?2:c,h)}}class G extends ${constructor(e){super(e)}getTopMerchants(){return this.fetch(g.TOP_MERCHANTS,"GET",{source:"web"})}getAllMerchants(){return this.fetch(g.ALL_MERCHANTS,"GET",{limit:1e4})}getMerchantByUrl(e){return this.fetch(g.GET_MERCHANTS_BY_URL,"GET",{domain:e})}getUserProgress(){return this.fetch(g.USER_PROGRESS,"GET",{},!0)}getUserBalance(){return this.fetch(g.USER_BALANCE,"GET",{},!0)}}var u=(s=>(s.FETCH_TOP_MERCHANTS="fetch_top_merchants",s.FETCH_ALL_MERCHANTS="fetch_all_merchants",s.UPDATE_ACTIVATION_DATA="update_activation_data",s.UPDATE_USER_DATA="update_user_data",s))(u||{});const F=s=>JSON.stringify(s),j=s=>JSON.parse(s.name),m=async(s,e)=>{const t=F(s);await new Promise(r=>chrome.alarms.get(t,c=>r(c)))||chrome.alarms.create(t,e)},x=s=>function(e){const t=j(e);s(t)};class V{get topMerchants(){const e=n.get("topMerchants");return e||[]}set topMerchants(e){n.set("topMerchants",e)}get allMerchants(){const e=n.get("allMerchants");return e||[]}set allMerchants(e){n.set("allMerchants",e)}getActualMerchant(){return n.get("actualMerchant")}setActualMerchant(e){n.set("actualMerchant",e)}getActivationData(){return n.get("activationData")||[]}getActivationDataById(e){return(n.get("activationData")||[]).find(a=>a.merchantId===e)}setActivationData(e){const t=n.get("activationData");if(!t||!t.length)n.set("activationData",[e]);else{const a=t.findIndex(r=>r.merchantId===e.merchantId);a<0?t.push(e):t[a]=e,n.set("activationData",t)}}setNewActivationData(e){n.set("activationData",e)}clearActivationData(){n.set("activationData",[])}}class J{constructor(e){o(this,"merchants",new V);o(this,"currentHost","");this.api=e,this.getAllMerchants(),this.getTopMerchants()}async getTopMerchants(){let e=this.merchants.topMerchants;return e.length||(e=await this.fetchTopMerchants()),e}async fetchTopMerchants(){const e=await this.api.getTopMerchants();return this.merchants.topMerchants=e,e}async getAllMerchants(){let e=this.merchants.allMerchants;return e.length||(e=await this.fetchAllMerchants()),e}async fetchAllMerchants(){const e=await this.api.getAllMerchants();return this.merchants.allMerchants=e,e}async getMerchantByUrl(e){const{host:t}=new URL(e),a=t.replace("www.","");if(this.currentHost===a||!a)return;this.currentHost=a;let r=this.merchants.getActualMerchant();return(!r||r.website!==a)&&(r=await this.fetchMerchantByUrl(a)),r}async fetchMerchantByUrl(e){const t=await this.api.getMerchantByUrl(e);if(t!=null&&t.merchant)return this.merchants.setActualMerchant(t.merchant),t.merchant}async getActualMerchantByDomain(e){const t=this.merchants.getActualMerchant();if(t&&M(t==null?void 0:t.website,e))return t}addInterstitialVisitForMerchant(e){const t={merchantId:e.id,ttl:Date.now(),activated:!1,isInterstitial:!0};this.merchants.setActivationData(t)}createActivationData(e){const t={merchantId:e.id,ttl:Date.now(),activated:!0};this.merchants.setActivationData(t)}getActivationDataByMerchantId(e){return this.merchants.getActivationDataById(e)}updateSliderViewData(e){const t=this.merchants.getActivationDataById(e.id);t?(t.isHide=!0,t.ttl=Date.now(),this.merchants.setActivationData(t)):this.merchants.setActivationData({merchantId:e.id,ttl:Date.now(),activated:!1,isHide:!0})}checkActualActivationData(){const e=this.merchants.getActivationData();if(!e.length)return;let t=[];for(const a of e)Date.now()-a.ttl>I||t.push(a);this.merchants.setNewActivationData(t)}async clearActivationData(){this.merchants.clearActivationData()}async getMerchantById(e){return(await this.getAllMerchants()).find(a=>a.id===Number(e))}async getMerchantByDomain(e){return(await this.getAllMerchants()).find(a=>M(a.website,e))}}class K{getUser(){return n.get("user")}setUser(e){return n.set("user",e)}setTokens(e){n.set("tokens",e)}clearTokens(){chrome.storage.local.remove("tokens")}setUserId(e){n.set("userId",e)}}class Y{constructor(e,t){o(this,"userStorage",new K);this.api=e,this.gaService=t,this.getUserInfo()}async getUserInfo(){const e=this.userStorage.getUser();return e||await this.fetchUserData()}async fetchUserProgress(){try{return await this.api.getUserProgress()}catch(e){console.log("error fetch user Progress",e);return}}async fetchUserBalance(){try{return await this.api.getUserBalance()}catch(e){console.log("error fetch user Balance",e);return}}async fetchUserData(){try{const e=await this.fetchUserProgress(),t=await this.fetchUserBalance();if(!e&&!t)return;const a={progress:e,balance:t};return this.userStorage.setUser(a),a}catch(e){console.log("🚀 ~ UserService ~ fetchUserData ~ error:",e);return}}async saveTokens(e){this.userStorage.setTokens(e),await this.api.verifyTokens(),await this.fetchUserData()}async clearUserData(){this.userStorage.setUser(""),this.userStorage.clearTokens(),this.userStorage.setUserId(0)}safariLogin(){const e=chrome.runtime.connectNative("");e.postMessage({action:"startAuthentication"}),e.onMessage.addListener(async t=>{t!=null&&t.accessToken&&(t!=null&&t.refreshToken)&&(console.log("Token:",t),await this.saveTokens({access_token:t.accessToken,refresh_token:t.refreshToken}),await this.gaService.signInEvent(),e.disconnect())}),e.onDisconnect.addListener(()=>{chrome.runtime.lastError&&console.error("Error:",chrome.runtime.lastError.message)})}}class q{constructor(){o(this,"GA_ENDPOINT","https://www.google-analytics.com/mp/collect");o(this,"GA_DEBUG_ENDPOINT","https://www.google-analytics.com/debug/mp/collect");o(this,"MEASUREMENT_ID","G-SH0PLD2Y3X");o(this,"API_SECRET","sJXc_KmARGG4hhTt8o33SQ")}async signInEvent(){const e=n.get("userId");e&&e>0&&this.sendEvent(e,"signup",{user_id:e})}async logoutEvent(){const e=n.get("userId");e&&e>0&&this.sendEvent(e,"logout",{user_id:e})}async GoToShopEvent(e){const t=n.get("userId");t&&t>0&&this.sendEvent(t,"go_to_shop",{merchant_id:e})}async sendEvent(e,t,a){try{fetch(`${this.GA_ENDPOINT}?measurement_id=${this.MEASUREMENT_ID}&api_secret=${this.API_SECRET}`,{method:"POST",body:JSON.stringify({client_id:String(e),events:[{name:t,params:a}]})})}catch(r){console.log("GA send error",r)}}}const z=(s,e)=>{if(!s||!e)return!1;const t=new URL(s),a=new URL(e);return t.hostname===a.hostname},X=s=>{chrome.tabs.get(s,e=>{chrome.runtime.lastError?console.log("Tab does not exist."):chrome.tabs.remove(s)})};class W{constructor(){o(this,"api",new G(U));o(this,"gaService",new q);o(this,"userService",new Y(this.api,this.gaService));o(this,"merchantService",new J(this.api));o(this,"creating");o(this,"deepLink",null);o(this,"checkInstall",e=>{e.reason==="install"&&!v()&&this.redirectTo(y)});this.setMessageHandlers(),this.checkAlarmState()}redirectTo(e){chrome.tabs.create({url:e})}async toggleLoader(e){n.set("isActivationProcess",e)}setMessageHandlers(){chrome.alarms.onAlarm.addListener(x(this.alarmHandle.bind(this))),chrome.runtime.onInstalled.addListener(this.checkInstall),chrome.tabs.onUpdated.addListener(async(e,t,a)=>{const r=a.id&&this.deepLink?this.deepLink[String(a.id)]:!1;if(a.url&&r&&this.deepLink&&z(this.deepLink[String(a.id)],a.url)){chrome.tabs.update(a.id,{url:this.deepLink[String(a.id)]}),delete this.deepLink[String(a.id)];return}this.getActualMerchant(a)}),chrome.webNavigation.onBeforeNavigate.addListener(async e=>{if(e.frameId===0&&e.url.includes(D)){const a=new URL(e.url).searchParams.get("m_id");if(!a)return;const r=await this.merchantService.getMerchantById(a);if(!r)return;this.merchantService.addInterstitialVisitForMerchant(r)}}),chrome.webNavigation.onCommitted.addListener(async e=>{if(e.frameId===0){const t=await this.merchantService.getMerchantByUrl(e.url);if(!t)return;const a=this.merchantService.getActivationDataByMerchantId(t.id);a&&a.isInterstitial&&(this.merchantService.createActivationData(t),await this.toggleLoader(""))}}),chrome.tabs.onActivated.addListener(async e=>{const t=await chrome.tabs.get(e.tabId);this.getActualMerchant(t)}),k(async(e,t,a)=>{var c;await this.userService.saveTokens(e.data),await this.gaService.signInEvent(),a(null);const r=(c=t.tab)==null?void 0:c.id;r&&X(r)}),L(async(e,t,a)=>{await this.userService.fetchUserData(),a(null)}),N(async(e,t,a)=>{chrome.tabs.query({active:!0},async r=>{const c=r[0];if(c.url&&c.active&&!c.url.includes("chrome://")){const h=await this.merchantService.getActualMerchantByDomain(c.url);a({actualMerchant:h})}else a(null)})}),R(async(e,t,a)=>{await this.gaService.logoutEvent(),await this.userService.clearUserData(),await this.merchantService.clearActivationData(),await this.toggleLoader(""),a(null)}),P(async(e,t,a)=>{this.userService.safariLogin(),a(null)}),H(async(e,t,a)=>{const{merchant:r,fromPopup:c}=e;if(!r)return a(null),null;const h=this.merchantService.getActivationDataByMerchantId(r.id);if(h&&h.activated)return this.redirectTo(r.website),a(null),null;if(!await this.userService.getUserInfo())return v()?this.userService.safariLogin():this.redirectTo(y),null;const i=await O();i&&i.id&&i.url&&(this.deepLink={[String(i.id)]:i.url}),await this.toggleLoader(String(r.id)),await this.gaService.GoToShopEvent(r.id),this.redirectTo(r.interstitialURL?b(r.interstitialURL):r.website),!c&&(i!=null&&i.id)&&chrome.tabs.remove(i.id,()=>{chrome.runtime.lastError&&console.log(chrome.runtime.lastError)}),a(null)}),C(async(e,t,a)=>{this.merchantService.updateSliderViewData(e.merchant),a(null)})}async alarmHandle(e){switch(e.type){case u.FETCH_TOP_MERCHANTS:{this.merchantService.fetchTopMerchants();break}case u.FETCH_ALL_MERCHANTS:{this.merchantService.fetchAllMerchants();break}case u.UPDATE_ACTIVATION_DATA:{this.merchantService.checkActualActivationData();break}case u.UPDATE_USER_DATA:{this.userService.fetchUserData();break}}}async checkAlarmState(){await m({type:u.FETCH_TOP_MERCHANTS,data:void 0},{periodInMinutes:S}),await m({type:u.FETCH_ALL_MERCHANTS,data:void 0},{periodInMinutes:S}),await m({type:u.UPDATE_ACTIVATION_DATA,data:void 0},{periodInMinutes:w}),await m({type:u.UPDATE_USER_DATA,data:void 0},{periodInMinutes:w})}async getActualMerchant(e){if(e.url&&(e==null?void 0:e.status)==="complete"&&e.active&&!e.url.includes("chrome://"))return await this.merchantService.getMerchantByUrl(e.url)}}async function Q(){return await n.init(),new W}Q();export{W as Background};
