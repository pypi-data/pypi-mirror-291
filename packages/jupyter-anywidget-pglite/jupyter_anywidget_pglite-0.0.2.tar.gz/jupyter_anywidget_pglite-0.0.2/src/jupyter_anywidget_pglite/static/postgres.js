var l=`<div class="pglite-app-container">

    <h1><tt>pglite</tt></h1>

    <div>Executed commands:</div>
    <div class="code-editor" title="code-editor"></div>
    <div id="pglite-timestamp"></div>
    <hr>
    <div>Result:</div>
    <div title="results"></div>
    <hr>
    <div>Raw Output:</div>
    <div title="output"></div>
</div>`;function c(){return"xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g,function(t){let e=Math.random()*16|0;return(t==="x"?e:e&3|8).toString(16)})}import{PGlite as m}from"https://cdn.jsdelivr.net/npm/@electric-sql/pglite/dist/index.js";var M=`
-- Optionally select statements to execute.

CREATE TABLE IF NOT EXISTS test  (
        id serial primary key,
        title varchar not null
      );

INSERT INTO test (title) values ('dummy');

`.trim();function u(t){let e=document.createElement("table"),r=e.insertRow();return t.fields.forEach(o=>{let n=document.createElement("th");n.textContent=o.name,r.appendChild(n)}),e}function g(t,e){t.rows.forEach(r=>{let o=e.insertRow();t.fields.forEach(n=>{let i=o.insertCell();i.textContent=String(r[n.name])})})}function f({model:t,el:e}){let r=new m,o=t.get("headless");if(!o){let n=document.createElement("div");n.innerHTML=l;let i=c();n.id=i,e.appendChild(n)}t.on("change:code_content",async()=>{let n=t.get("code_content"),i=await r.query(n);if(t.set("response",i),!o){let a=e.querySelector('div[title="code-editor"]'),p=e.querySelector('div[title="output"]'),s=e.querySelector('div[title="results"]');a.innerHTML=a.innerHTML+"<br>"+t.get("code_content"),p.innerHTML=JSON.stringify(i);let d=u(i);g(i,d),s.innerHTML="",s.append(d)}t.save_changes()})}var R={render:f};export{R as default};
