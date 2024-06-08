# AutomTest 3.0
Article on AutomTest's First version: 
Towards a Test Case Generation Tool Based on Functional Requirements <https://dl.acm.org/doi/10.1145/3439961.3440002>

## Requisitos:
PySimpleGUI

## Para atualizar:
pyinstaller app.spec

## Endpoints:
- Recebe uma história de usuário e seu idioma
- Retorna uma coleção de métodos

### Para executar:
python3 main.py
  1. ```pip3 install spacy``` (Spacy)
  2. ```python3 -m spacy download pt_core_news_md```
  3. ```pip install Unidecode```

### Para executar no Linux:
python3 main.py

## Remarks

#### 1. Specification of some variable types

  - String

    - predefined sets:

    ```
    sign/signs
    alphanumeric/alphanumerics
    any/all
    number/numbers
    letter/letters	
    ```

    - substrings (example)
    
    ```
    [all][letter][alphanumeric]
    ```

    - size (example)
    ```
    [1~4][1][2~6]
    ```

  - Date:
    ```
    YYYY/MM/DD or YYYY-MM-DD
    ```

#### 2. Possible error in package version ***requests***

If you get this error:

> /usr/lib/python3/dist-packages/requests/__init__.py:89: RequestsDependencyWarning: urllib3 (1.26.8) or chardet (3.0.4) doesn't match a supported version!
> warnings.warn("urllib3 ({}) or chardet ({}) doesn't match a supported "
> Traceback (most recent call last):  File "main.py", line 158, in \<module\>
> if ( p.telaInicialConjTesteCorreta(vals2[1],vals2[2]) and p.entradaTipoCorreta(MUT.output_type,vals2[3],vals2[4],vals2[5])): KeyError: 1

Run the command:

```
pip3 install --upgrade requests
```

Reference: <https://stackoverflow.com/questions/56155627/requestsdependencywarning-urllib3-1-25-2-or-chardet-3-0-4-doesnt-match-a-s>
