## Izziv večvrstična enovrstičnica

V programskem jeziku Python je podan program enostavnega igralnega avtomata, ki naključno izbira trojčke simbolov iz podanega nabora simbolov `SYMBOLS`. V kolikor so vsi trije simboli enaki `7`, je dosežen _Jackpot_! V tem primeru program zaključi izvajanje in izpiše vzpodbudno sporočilo. V nasprotnem primeru program nadaljuje izvajanje največ `TRIES` korakov. V kolikor po `TRIES` korakih še vedno ni dobljenega _Jackpot_-a, program uporabnika pozove k ponovnemu igranju.

```py
import random as rnd

TRIES = 1000
SYMBOLS = '♣♠♦♥♪♫◄☼☽xyz7'

def random(symbols):
  return symbols[rnd.randint(0, len(symbols) - 1)]

for i in range(TRIES):
  s1 = random(SYMBOLS)
  s2 = random(SYMBOLS)
  s3 = random(SYMBOLS)

  print('{0:d}. {1:s}|{2:s}|{3:s}'.format(i + 1, s1, s2, s3))

  if s1 == '7' and s2 == '7' and s3 == '7':
    print('Jackpot in {0:d} tries :) Well done!'.format(i + 1))
    break

  if i == TRIES - 1:
    print('No jackpot :( Better luck next time!')
```

V programskem jeziku Python sestavite program z enako funkcionalnostjo v **zgolj eni vrstici**. (_Posamezne stavke programa lahko zapišete v eni vrstici v kolikor jih ločite s podpičjem `;`._)