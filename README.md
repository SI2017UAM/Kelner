# Kelner

### Folder TopDown/PNG zawiera zestaw spriteów które użyłem, oczywiście można w przyszłości użyć czegokolwiek
### Folder imgs zawiera używane sprite'y
### Folder maps na razie nas nie interesuje, nie zrobilem powiązania z tym folderem przy wczytywaniu mapy tylko korzystam z pliku map1.txt


**settings.py** znajdują się główne stałe gry, zdefiniowane są kolory, wielkość okna gry w px, max FPS (czyli co jaki czas aktualizujemy obiekty na ekranie), rozmiar bloku, wymiary mapy (w blokach), ustawienia gracza, ustawienia mobów i innych obiektów.

**main.py** znajduje się klasa gry , przy tworzeniu gry (na samym dole **g=Game()**) inicjujemy w niej podstawowe parametry (__init__) oraz wczytujemy dane, w tym mapę (**load_data**)

Poniżej znajduje się główna pętla gry (**na samym dole w while true**), w funkcji **new** grupujemy sprite'y tworząc kategorie (wszystkie sprite'y, ściany, itp, dzięki czemu możemy potem robić np. zbiorczy update na obiektach) oraz korzystamy z wczytanej mapy (z **load_data**) i odpowiednio tworzymy obiekty w grze. 

w funkcji **run** sprawdzamy FPS (ponieważ od tego uzależniamy ruch obiektów), zbieramy eventy (czyli nacisniecia klawiszy, myszki itp),
następnie robimy update na obiektach gry, które mogły zmienić swój stan po eventach, na koniec rysujemy wszystkie sprite'y na ekranie.

resztę funkcji - cost, find_neighbours, passable, in_bounds, wall_existence_check być może będziemy używać później, do wyszukiwania ścieżek.

**sprites.py** opisane są poszczególne obiekty poprzez **funkcję inicjującą**, w której przekazujemy kopię gry, oraz pozycję na mapie, przypisujemy obiekt do grupy, przypisujemy sprite'a z **settings.py** do obiektu, pobieramy prostokątny wymiar obrazku (**image.get_rect()**), oraz ustalamy inne **początkowe** parametry obiektu

w funkcji **update**  uaktualniamy parametry obiektu, np w zależności od naciśniętych przycisków (klasa Player i funkcja **get_keys**), obiekt Mob 'śledzi' gracza - **to taki typ zachowania wykorzystamy do imitacji kelnera**.

**tilemap.py** w klasie Map zdefiniowana jest funkcja dzięki któej możemy wczytać z pliku tekstowego mapę, oraz klasa Camera, która umożliwia śledzenie obiektu (w tym przypadku gracza)


# Źródło ->  https://www.youtube.com/watch?v=3UxnelT9aCo #
