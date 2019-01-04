# regex4ocr

A simple library to plug regular expression models to parse your favorite OCR
output and extract important fields and info from it.

## Document Regexp Model (DRM)

The DRM are yml files which describres the desired documents with many regular expressions. Those are used to extract the document data in order to transform the OCR results into well formatted JSON.

### OCR and DRM example:

Given the following DRM:

```yml
identifiers:
  - cupom fiscal
fields:
  cnpj: 'cnpj:\s*(\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2})'
  coo: 'coo:\s*(\d{6})'
  date: '\d{2}\/\d{2}\/\d{4}\s*\d{2}:\d{2}:\d{2}'
options:
  lowercase: true
  remove_whitespace: false
  force_ascii: true
  replace:
    - ['c00', 'coo']
    - ['c10', 'coo']
table:
  header: (item|iten)\s+codigo.*vl.*(?=\n)
  line_start: \n\d*.+\d+
  footer: total\s*r\$
```

One can extract the following JSON based given the following OCR results (Google Vision of a receipt note):

```
(...)
cnpj: 11.123.456/0001-99
ie:111.111.111. 111
im: 123456-7
2570972078 17:54: ttccf 3045759 **** coo:047621
cupom fiscal
iten codigo descricao qid un vl unit r$ ) st vl item(r$)
17273 breit grossa -7mts" bunx373 ft 288 026
2 $17 pedra 1 (ht) 2unx84 694 f1
169 38g
003 515 cimento votoran todas as obras 50 kg
cred)
boun x 26.489 f1
794,676
total r$
1.247.07
cheque
1.247.09
troco r$
0.02
(...)
```


The OCR result is finally parsed into the following JSON based on the DRM yml regular expressions:

```javascript
{
    'cnpj': '11.123.456/0001-99',
    'coo': '047621',
    'table': '\n17273 breit grossa -7mts" bunx373 ft 288 026\n2 $17 pedra 1 (ht) 2unx84 694 f1\n169 38g\n003 515 cimento votoran todas as obras 50 kg\ncred)\nboun x 26.489 f1\n794,676\n',
    'rows': [
        '17273 breit grossa -7mts" bunx373 ft 288 026', '2 $17 pedra 1 (ht) 2unx84 694 f1', 
        '169 38g', 
        '003 515 cimento votoran todas as obras 50 kgcred)', 'boun x 26.489 f1', '794,676'
    ]
}
```