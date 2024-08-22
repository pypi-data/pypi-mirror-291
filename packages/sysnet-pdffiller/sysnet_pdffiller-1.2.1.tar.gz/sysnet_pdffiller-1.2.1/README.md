# PDF Filler

Knihovna pro plnění připravených PDF šablon daty.


## Verze

### 1.1.0

Přesun z PyPDF3 v1.0.6 na pypdf v3.15.5. 

### 1.2.0

Konfigurační soubor přejmenován ze **settings.py** na **init.py**


## Použití

Instalace:

    pip install pip install sysnet-pdffiller


V programu

    from sysnet_pdf.pdf_utils import parse_template_type
    ...
    ...
    template_type = parse_template_type(template.template_first)
