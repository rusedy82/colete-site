# Secțiunea „Trimite un colet”: formular cu trimitere automată pe email prin FormSubmit.
def comanda_section(C, TARI, icon):
    tari = ["România"] + sorted(t["tara"] for t in TARI)
    def opts(sel):
        return "".join(f'<option{" selected" if x == sel else ""}>{x}</option>' for x in tari)
    def adresa(prefix, titlu, tara_def, ic):
        return f'''<fieldset class="fs">
    <legend><span class="n">{icon(ic, 20, "#fff")}</span>{titlu}</legend>
    <div class="row2">
      <label>Nume și prenume<input name="{prefix} - nume" required autocomplete="name"></label>
      <label>Telefon<input name="{prefix} - telefon" type="tel" required autocomplete="tel" placeholder="+40 7xx xxx xxx"></label>
    </div>
    <div class="row3">
      <label>Țara<select name="{prefix} - țara" required>{opts(tara_def)}</select></label>
      <label>Oraș / localitate<input name="{prefix} - oraș" required></label>
      <label>Cod poștal<input name="{prefix} - cod poștal" required inputmode="numeric" autocomplete="postal-code"></label>
    </div>
    <div class="row2">
      <label>Județ / regiune<input name="{prefix} - județ"></label>
      <label>Stradă și număr<input name="{prefix} - stradă și număr" required autocomplete="street-address"></label>
    </div>
    <label>Bloc, scară, etaj, apartament <small>(opțional)</small><input name="{prefix} - detalii adresă"></label>
  </fieldset>'''
    return f'''
<section id="comanda" class="order-sec"><div class="wrap">
  <div class="head"><span class="eyebrow pill">Trimite un colet</span><h2 style="margin-top:14px">Comandă transportul coletului</h2>
  <p>Completează datele de mai jos și apasă „Trimite comanda”. Te sunăm noi să confirmăm ziua ridicării și prețul final.</p></div>
  <form id="order-form" class="order" novalidate>
  <fieldset class="fs">
    <legend><span class="n">{icon("box", 20, "#fff")}</span>Coletul</legend>
    <div class="row3">
      <label>Greutate (kg)<input name="Colet - greutate (kg)" id="f-kg" type="number" min="0.1" step="0.1" required inputmode="decimal"></label>
      <label>Număr de colete<input name="Colet - număr colete" type="number" min="1" step="1" value="1" required></label>
      <label>Data preferată de ridicare<input name="Colet - data ridicare" type="date"></label>
    </div>
    <p class="hint">Dimensiuni (cm)</p>
    <div class="row3">
      <label>Lungime<input name="Colet - lungime (cm)" type="number" min="1" required inputmode="numeric"></label>
      <label>Lățime<input name="Colet - lățime (cm)" type="number" min="1" required inputmode="numeric"></label>
      <label>Înălțime<input name="Colet - înălțime (cm)" type="number" min="1" required inputmode="numeric"></label>
    </div>
    <label>Ce conține coletul<input name="Colet - conținut" required placeholder="de ex. haine, încălțăminte, cadouri"></label>
    <div class="estimate" id="estimate" aria-live="polite">Introdu greutatea ca să vezi prețul estimat.</div>
  </fieldset>
  {adresa("Ridicare", "Adresa de ridicare", "România", "home")}
  {adresa("Livrare", "Adresa de livrare", "Germania", "pin")}
  <fieldset class="fs">
    <legend><span class="n">{icon("msg", 20, "#fff")}</span>Datele tale de contact</legend>
    <div class="row2">
      <label>Emailul tău <small>(opțional)</small><input name="email" type="email" autocomplete="email"></label>
      <label>Observații <small>(opțional)</small><input name="Observații"></label>
    </div>
  </fieldset>
  <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
  <label class="agree"><input type="checkbox" required> Sunt de acord ca datele mele să fie folosite pentru preluarea și livrarea coletului.</label>
  <button class="btn" type="submit" id="order-submit">Trimite comanda</button>
  <div id="order-msg" class="order-msg" role="status" aria-live="polite" hidden></div>
  </form>
</div></section>
<script>
(function(){{
  var f=document.getElementById("order-form"); if(!f) return;
  var kg=document.getElementById("f-kg"), est=document.getElementById("estimate"),
      btn=document.getElementById("order-submit"), msg=document.getElementById("order-msg");
  function pret(k){{ return k<=20 ? 30 : Math.round(k*1.70*100)/100; }}
  function fmt(x){{ return x.toFixed(2).replace(".00","").replace(".",",")+" €"; }}
  function upd(){{ var k=parseFloat((kg.value||"").replace(",","."));
    est.innerHTML = k>0 ? "Preț estimat: <b>"+fmt(pret(k))+"</b> <span>(30 € până la 20 kg, 1,70 €/kg peste 20 kg; prețul final se confirmă la cântărire)</span>" : "Introdu greutatea ca să vezi prețul estimat."; }}
  kg.addEventListener("input",upd);
  function show(ok,t){{ msg.hidden=false; msg.className="order-msg "+(ok?"ok":"err"); msg.innerHTML=t; msg.scrollIntoView({{block:"center",behavior:"smooth"}}); }}
  f.addEventListener("submit",function(e){{
    e.preventDefault();
    if(!f.checkValidity()){{ f.reportValidity(); return; }}
    var d={{}}; new FormData(f).forEach(function(v,k){{ d[k]=v; }});
    var k=parseFloat(String(d["Colet - greutate (kg)"]).replace(",","."));
    d["Preț estimat"]=fmt(pret(k));
    d["_subject"]="Comandă colet nouă: "+d["Ridicare - oraș"]+" ("+d["Ridicare - țara"]+") → "+d["Livrare - oraș"]+" ("+d["Livrare - țara"]+"), "+k+" kg";
    d["_template"]="table"; d["_captcha"]="false";
    if(!d.email) delete d.email;
    btn.disabled=true; btn.textContent="Se trimite...";
    fetch("https://formsubmit.co/ajax/{C["email"]}",{{method:"POST",headers:{{"Content-Type":"application/json","Accept":"application/json"}},body:JSON.stringify(d)}})
      .then(function(r){{ return r.json().then(function(j){{ if(!r.ok||String(j.success)!=="true") throw new Error(j.message||"eroare"); }}); }})
      .then(function(){{ f.reset(); upd(); show(true,"<b>Comanda a fost trimisă.</b> Te sunăm în curând să confirmăm ridicarea. Pentru urgențe: <a href=\\"tel:{C["tel_link"]}\\">{C["tel_afisat"]}</a>"); }})
      .catch(function(){{ show(false,"Comanda nu a putut fi trimisă. Te rugăm să ne suni la <a href=\\"tel:{C["tel_link"]}\\">{C["tel_afisat"]}</a>."); }})
      .finally(function(){{ btn.disabled=false; btn.textContent="Trimite comanda"; }});
  }});
}})();
</script>
'''
