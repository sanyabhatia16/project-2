async function analyzeText(){

const text=document.getElementById("text").value.trim();

if(text===""){

alert("Please enter some text.");

return;

}

document.getElementById("loading").style.display="block";

document.getElementById("results").innerHTML="";

try{

const response=await fetch("https://aitext-api-f3efhxarf8cndhaw.centralindia-01.azurewebsites.net/analyze",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({text})

});

const data=await response.json();

document.getElementById("loading").style.display="none";

let sentiment="neutral";

if(data.sentiment.label==="positive") sentiment="positive";

if(data.sentiment.label==="negative") sentiment="negative";

document.getElementById("results").innerHTML=`

<div class="card">
<h2>🌍 Language</h2>
<p><strong>${data.language.name}</strong></p>
<p>Confidence : ${(data.language.confidence*100).toFixed(1)}%</p>
</div>

<div class="card">
<h2>😊 Sentiment</h2>
<span class="badge ${sentiment}">
${data.sentiment.label.toUpperCase()}
</span>

<br><br>

<p>🟢 ${(data.sentiment.confidence.positive*100).toFixed(1)}%</p>

<p>⚪ ${(data.sentiment.confidence.neutral*100).toFixed(1)}%</p>

<p>🔴 ${(data.sentiment.confidence.negative*100).toFixed(1)}%</p>

</div>

<div class="card">

<h2>🔑 Key Phrases</h2>

${data.key_phrases.map(k=>`<span class="chip">${k}</span>`).join("")}

</div>

<div class="card">

<h2>👤 Named Entities</h2>

${data.entities.map(e=>`

<div class="item">

<strong>${e.text}</strong>

<br>

${e.category}

</div>

`).join("")}

</div>

<div class="card">

<h2>🔒 PII Detected</h2>

${data.pii.length>0?

data.pii.map(p=>`

<div class="item">

<strong>${p.text}</strong>

<br>

${p.category}

</div>

`).join("")

:"<p>No PII Found ✅</p>"}

</div>

<div class="card">

<h2>🛡️ Redacted Text</h2>

<pre>${data.redacted_text}</pre>

</div>

<div class="card summary">

<h2>📄 AI Summary</h2>

<pre>${data.summary??"Summary unavailable."}</pre>

</div>

`;

}

catch(err){

document.getElementById("loading").style.display="none";

document.getElementById("results").innerHTML=`

<div class="card">

<h2>❌ Error</h2>

<p>${err}</p>

</div>

`;

}

}

function clearText(){

document.getElementById("text").value="";

document.getElementById("results").innerHTML="";

}