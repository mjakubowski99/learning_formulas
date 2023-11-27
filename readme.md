## Uruchomienie interfejsu użytkownika
Wymagania:
    - cmake
    - python3
    - biblioteki zdefiniowane w requirements.txt

Uprzednio należy zbudować kod C++, można tego dokonać poprzez wykonanie:
```
./build.sh
```

W celu instalacji bibliotek można użyć polecenia:
```
pip install -r requirements.txt
```

Do działania aplikacji niezbędę jest zbudowanie kodu C++ w przypadku systemów Linux
można skorzystać z polecenia ./build.sh

Uruchomienie interfejsu użytkownika:
```
python main.py
```
Interfejs użytkownika pozwala na uruchomienie modułu uczącego formuły zarówno z użyciem dockera jak i bez niego.
Opcja bez dockera wymaga posiadania dystrybucji Linuxa bądź jego emulatora. Sterowanie tym czy interfejs ma korzystać
z dockera czy nie wykonujemy poprzez ustawienie zmiennej w pliku main.py. Domyślnie uczenie jest uruchamiane bez dockera.


## Uruchomienie core w c++

### Z dockerem
Wymagany docker oraz docker-compose 
```
docker-compose up -d
```

### Bez dockera
W celu zbudowaniu kodu C++ należy uruchomić skrypt bash:
```
./build.sh
```
Wymagane gcc oraz cmake. Można uruchomić poprzez wykonaniu w terminalu:
```
./run.sh
```
Skrypt wykorzystuje zmienne zdefiniowane w pliku .env, należy pamiętać, że zmienne odpowiadające
za ścieżki do plików bądź katalogów są relatywne.



### Uwagi
1. Przetworzone przez interfejs pliki z ciągami danych binarnych zakodowane przez interfejs. Znajdują się w katalogu
core/data/, które są wykorzystywane przez moduł uczący jako źródło danych.
2. Wynikowe formuły wraz z wynikami zapisują się w katalogu core/result/
3. Interfejs podczas kodowania danych zapisuje plik konfiguracyjny, w katalogu wczytanego pliku csv. Przechowuje on
wszystkie informacje, które są wykorzystywane w celu zapamiętania konfiguracji parametrów kodowania binarnego. Dane z tych
plików są również wykorzystywane w celu przetworzenia danych przesłanych do predykcji.
4. Predykcji na podstawie formuł możemy dokonać tylko gdy w kataglu core/result/ znajduje się plik result.txt z formułami.
Należy pamiętać, że plik z danymi do predykcji musi zawierać wszystkie kolumny jakie zawierały dane csv, które służyły do
celów treningowych. Istnieje tu, też pewne ograniczenie. Jako, że ilość bitów w każdym wierszu danych binarnych musi być stała to
w przypadku jeśli taki plik csv będzie zawierał większe wartości niż znane w zbiorze treningowym. To zostaną one ograniczone do maksymalnych wartości znanych temu zbiorowi podczas kodowania na dane binarne.
5. Po każdym ukończeniu uczenia zapisywany jest plik z raportem, który zawiera zapis parametrów algorytmu oraz wynik na danych
testowych(plik result/report.csv)
