# Interim-Report-Prediction
Detta är ett enkelt projekt för att titta på om NLP kan förutse aktiers rörelse baserat på vilken rapport företaget släpper.

Scripts:
Här finns en scraper för att hämta samtliga kvartalsrapporter på Nasdaq OMX Nordics Hemsida. Scrapern hämtar alla "Interimsrapporter" under 2019 och sparar ner dessa i csv-format. Bolag, Tidpunkt och hela releasen hämtas. Se bill "Eolus" för exempel.
Scrapern använder python-bilioteket "selenium" för att hämta samtliga rapporter. 

Data:
Här finns de hämtade Rapporterna och historiska priser för samtliga bolag dessa hör till. 

Jupyter:
Här processas all data för att kunna bli presenterat för ett neuralt nätverk. Python-biblioteket Keras används med Tensorflow som Backend. 




