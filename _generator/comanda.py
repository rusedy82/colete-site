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
    <legend><span class="n">{icon("phone", 20, "#fff")}</span>Datele tale</legend>
    <p class="hint-sm">Te sunăm la acest număr ca să confirmăm comanda.</p>
    <div class="row2">
      <label>Numele tău <em>*</em><input name="Client - nume" id="f-nume" required autocomplete="name"></label>
      <label>Telefonul tău <em>*</em><input name="Client - telefon" id="f-tel" type="tel" required autocomplete="tel" placeholder="+40 7xx xxx xxx"><span class="err-txt" id="tel-err" hidden>Scrie un număr de telefon valid, ca să te putem suna.</span></label>
    </div>
    <div class="row2">
      <label>Emailul tău <small>(opțional)</small><input name="email" type="email" autocomplete="email"></label>
      <label>Observații <small>(opțional)</small><input name="Observații"></label>
    </div>
  </fieldset>
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
  <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
  <label class="agree"><input type="checkbox" required> Sunt de acord ca datele mele să fie folosite pentru preluarea și livrarea coletului.</label>
  <button class="btn" type="submit" id="order-submit">Trimite comanda</button>
  <div id="order-msg" class="order-msg err" role="alert" hidden></div>
  </form>
  <div id="order-ok" class="order-ok" tabindex="-1" hidden>
    <div class="ok-ic"><svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></div>
    <h3>Comanda ta s-a trimis!</h3>
    <p class="ok-thanks">Vă mulțumim că ați ales {C["nume"]}.</p>
    <div class="ok-sum" id="ok-sum"></div>
    <p class="ok-next">Te sunăm în cel mai scurt timp la <b id="ok-tel"></b> ca să confirmăm ziua ridicării și prețul final.</p>
    <p class="ok-urgent">Pentru urgențe: <a href="tel:{C["tel_link"]}">{C["tel_afisat"]}</a></p>
    <button type="button" class="btn ghost" id="ok-again">Trimite alt colet</button>
  </div>
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
  document.getElementById("f-tel").addEventListener("input",function(){{ this.setCustomValidity(""); document.getElementById("tel-err").hidden=true; }});
  document.getElementById("ok-again").addEventListener("click",function(){{
    document.getElementById("order-ok").hidden=true; f.hidden=false;
    f.scrollIntoView({{block:"start",behavior:"smooth"}});
  }});
  function show(ok,t){{ msg.hidden=false; msg.className="order-msg "+(ok?"ok":"err"); msg.innerHTML=t; msg.scrollIntoView({{block:"center",behavior:"smooth"}}); }}
  f.addEventListener("submit",function(e){{
    e.preventDefault();
    var tel=document.getElementById("f-tel"), cifre=(tel.value.match(/\\d/g)||[]).length;
    tel.setCustomValidity(cifre>=9 && cifre<=15 ? "" : "Scrie un număr de telefon valid.");
    document.getElementById("tel-err").hidden = tel.validity.valid;
    if(!f.checkValidity()){{ f.reportValidity(); return; }}
    var d={{}}; new FormData(f).forEach(function(v,k){{ d[k]=v; }});
    var k=parseFloat(String(d["Colet - greutate (kg)"]).replace(",","."));
    d["Preț estimat"]=fmt(pret(k));
    d["_subject"]="Comandă colet nouă de la "+d["Client - nume"]+" ("+d["Client - telefon"]+"): "+d["Ridicare - oraș"]+" ("+d["Ridicare - țara"]+") → "+d["Livrare - oraș"]+" ("+d["Livrare - țara"]+"), "+k+" kg";
    d["_template"]="table"; d["_captcha"]="false";
    if(!d.email) delete d.email;
    btn.disabled=true; btn.textContent="Se trimite...";
    fetch("https://formsubmit.co/ajax/{C["email"]}",{{method:"POST",headers:{{"Content-Type":"application/json","Accept":"application/json"}},body:JSON.stringify(d)}})
      .then(function(r){{ return r.json().then(function(j){{ if(!r.ok||String(j.success)!=="true") throw new Error(j.message||"eroare"); }}); }})
      .then(function(){{
        var esc=function(x){{ return String(x).replace(/[&<>"]/g,function(c){{ return {{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}}[c]; }}); }};
        document.getElementById("ok-sum").innerHTML =
          "<div><span>Traseu</span><b>"+esc(d["Ridicare - oraș"])+", "+esc(d["Ridicare - țara"])+" → "+esc(d["Livrare - oraș"])+", "+esc(d["Livrare - țara"])+"</b></div>"+
          "<div><span>Greutate</span><b>"+esc(k)+" kg</b></div>"+
          "<div><span>Preț estimat</span><b>"+esc(d["Preț estimat"])+"</b></div>";
        document.getElementById("ok-tel").textContent=d["Client - telefon"];
        f.reset(); upd(); msg.hidden=true; f.hidden=true;
        var ok=document.getElementById("order-ok"); ok.hidden=false;
        ok.scrollIntoView({{block:"center",behavior:"smooth"}}); ok.focus({{preventScroll:true}});
      }})
      .catch(function(){{ show(false,"Comanda nu a putut fi trimisă. Te rugăm să ne suni la <a href=\\"tel:{C["tel_link"]}\\">{C["tel_afisat"]}</a>."); }})
      .finally(function(){{ btn.disabled=false; btn.textContent="Trimite comanda"; }});
  }});
}})();
</script>
'''
