# Mastermind játék

### A Mastermind egy színkeresős játék, amelyben négy elrejtett színt kell sorrendhelyesen kitalálni adott számú tippeléssel.
## A játék szabályai és használata
- Összesen 6 szín van (magenta, zöld, kék, sárga, fehér és fekete), amiből 4 lesz a játék kezdetekor elrejtve.
- A játéktér egyes soraiban, felülről lefelé haladva kell tippelni a színeket. Ezt a körökre való bal egérgombbal való kattintással lehet megtenni. Minden egyes kattintásra új színre vált a kör. Ha végére ért a színsorozatnak, akkor előröl kezdődnek újra a színek.
- Ha ilyen módon mind a négy pozícióban megvan a tippünk, akkor a *Tipp Ellenőrzése* gombot megnyomva a sor jobb szélén levő négyzetben visszajelzést kapunk, hogy van-e találatunk. A fekete körök azt jelentik, hogy annyi színt eltaláltunk, ahány fekete van, és ráadásul azok helyes pozícióban is vannak. A fehér körök pedig azt mutatják, hogy azok számának megfelelő számú színt eltalálatunk, de ezek még nincsenek jó helyen.
- A kiértékelést követően módosítani már nem lehet a tippet, hanem a következő sorban tippelhetünk újra.
- Ha egy adott sorban levő tippünkben szereplő minden színt eltaláltuk és helyes pozícióban is vannak, akkor a játék sikerrel zárul, amiről egy üzenetablak tájékoztat.
- Ha viszont az utolsó sorban levő tippünk sem helyes, akkor egy üzenetablak jön fel, ami a játék sikertelen végéről tájékoztat.

A *Tipp Ellenőrzése* gomb alatt látható részben lehet a játék megkezdése előtt beállítani egy 1 és 12 közötti számmal, hogy hány sor áll rendelkezésre a tippekhez, valamint azt, hogy az elrejtett színekben lehet-e ismétlődés és szerepelhet-e elrejtettként az üres pozíció. Alapesetben a sorok száma nyolc és egyik opció sincs megengedve.
Ha az alapértékektől eltérünk, akkor az *Új játék* gomb megnyomásával kell indítani indítani a játékot, ami már az 
aktuális beállításoknak megfelelően fog megjelenni és működni.

A játék indítása után megjelenő felület képernyőképét mutatja az alábbi ábra bal oldala. Középen egy sikeres megfejtéssel végződő játék képe látható. Ennek alsó részén megfigyelhető, hogy a választógombok nincsenek bekapcsolt állapotban, ami azt jelenti, hogy az elrejtett színek csak egyszer fordulhatnak elő, és az üres pozíció nem szerepelhet közöttük.  Ezzel szemben, az ábra jobb oldali képernyőképe egy olyan játékmenet sikertelen végét mutatja, ahol a rejtett színek között lehet ismétlődés és az üres pozíció is szerepelhet.

<img src="https://github.com/pythontudasepites/mastermind_game/blob/main/mastermind_screenshot_1.jpg" width="623" height="420">

A következő ábra bal oldala egy csökkentett tippsorokkal indított játékot mutat, a jobb oldal pedig azt a hibaüzenetet, amikor a sorok száma a megengedett tartományon kívüli értékre lett megadva.

<img src="https://github.com/pythontudasepites/mastermind_game/blob/main/mastermind_screenshot_2.jpg" width="420" height="354">
