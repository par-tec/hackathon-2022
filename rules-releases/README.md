# Come testare il proprio snake
Il metodo più veloce per testare il tuo snake è quello di utiizzare la release ufficiale di rules (l'engine di battlesnake), a questo indirizzo trovi le release ufficiali:

https://github.com/BattlesnakeOfficial/rules/releases/tag/v1.1.21

Puoi scaricare la versione compatibile con il tuo sistema operativo o compilare direttamente dai sorgenti (fai riferimento al readme che trovi all'interno del Source Code)

Oltre l'engine per visualizzare il tuo snake hai bisogno di utilizzare una board, puoi tranquillamente usare quella di default ossia la board ufficiale del sito play.battlesnake.com. 

Ad esempio il tuo snake risponde sulla porta 8000 del tuo computer, puoi avviare l'engine con il seguente comando:
```
./battlesnake --name IL_MIO_SNAKE --url http://0.0.0.0:8000 --browser
```
 Ricordati che il nome del tuo snake è lo stesso nome che userai per la directory
