# Generatorul site-ului

Paginile HTML din rădăcină sunt generate. Pentru modificări se editează fișierele din acest folder, apoi se rulează din rădăcina repository-ului:

    python3 _generator/build.py .

- `build.py`: datele firmei (nume, telefon, email, domeniu), țările, serviciile și textele paginilor
- `comanda.py`: formularul „Trimite un colet” (trimitere pe email prin FormSubmit)
- `style.css`: aspectul site-ului; se copiază în rădăcină la generare
