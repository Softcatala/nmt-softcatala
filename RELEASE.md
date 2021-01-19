# Build translate web service

Build serving/translate-service/docker

## English to Catalan

### Upper case

HELLO MY FRIENDS
Hello my friends
WHICH DAY IS TODAY?

### Test tags processing

Both the <emphasis>Color Picker</emphasis> and the <emphasis>Sample Points</emphasis> dialog now display pixel values in CIE LAB and CIE LCH at your preference.

"You can use <u id='3521'><br id='p2'/></u> and <u id='3522'><br id='p1'/></u>, available under <u id='3523'>Apps</u>, to enable or disable these new capabilities for specific users."

## Performance benchmark

Using serving/perf-tests 

On Softcatalà production hardware:

Production:
** Catalan - English (10 req, 1 at the time)
  95%    290
** Catalan - English (50 req, 5 at the time)
  95%    650
** English - Catalan (10 req, 1 at the time)
  95%    329
** English - Catalan (50 req, 5 at the time)
  95%    542

## Check versions in production

https://www.softcatala.org/sc/v2/api/nmt-engcat/version/




