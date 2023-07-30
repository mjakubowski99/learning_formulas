# Biblioteka wspomagająca uczenie formuł logicznych 

## Struktury danych 
Definicje wszystkich wykorzystywanych struktur danych znajdują się w pliku types.hpp.


### Formuła logiczna
Formuła logiczna jest zdefiniowana jako wektor klauzul. Natomiast klauzula jest zdefiniowana jako
wektor literałów.

Definicja formuły logicznej 
```
typedef vector<Clause> Formula;
```

Definicja klauzuli
```
typedef vector<Literal> Clause;
```

Literał jest strukturą posiadającą 2 pola. Pozycja odpowiadającego mu bitu(atrybutu) oraz informacja
mówiąca o tym czy literał jest zanegowany czy nie.
```
struct Literal {
    int bitPosition;
    bool positive;

    Literal();
    Literal(int bitPositon, bool positive);
};
```

### Przechowywanie formuły oraz wyniku
Wykorzystywana jest również struktura danych, która pozwala przechowywać formułę razem z jej wynikiem
na danych treningowych.
```
struct FormulaWithScore
{
    float score;
    Formula formula;
};
```  
Oraz struktura pozwalająca przechowywać tablicę wyżej wspomnianych struktur.
```
struct FormulaWithScoreArray
{
    FormulaWithScore * formulas;
    int size=0;

    FormulaWithScoreArray(){};

    FormulaWithScoreArray(int size)
    {
        this->formulas = new FormulaWithScore[size];
        this->size = size;
    }

    void sortByScore();
};
```

### Struktura przechowująca dane

Struktura przechowuje oprócz danych, wartości takie jak ilość rekordów oraz ilość atrybutów. Udostępnia również operacje, które pozwalają na pobranie wartości atrybutu.
```c++
struct Data {
    int rows_count;
    int attributes_count;
    bool ** data;
    Data();
    Data(int rows_count, int attributes_count);
    void init(int rows);
    void insert(int i, int j, bool value);
    bool get(int i, int j);
};
```

### Podział na klasy decyzyjne
Formuły opisujące klasę decyzyjną są definiowane jako tablica struktury FormulaWithScoreArray, gdzie każdy indeks tablicy odpowiada klasie decyzyjnej. Natomiast pod indeksem kryje się lista formuł, które mają ją opisywać.

## Generator formuł logicznych

Generator formuł logicznych(klasa FormulaGenerator) Jest odpowiedzialny za losowe wygenerowanie formuł logicznych dla podanej klasy decyzyjnej  według następujących zasad. Generowane są formuły dwóch rodzajów.

1. Pozytywne, czyli takie, których celem jest spełnialność dla jak największej liczby
wierszy z danej klasy decyzyjnej.

Generowane polega na wylosowaniu wiersza i kolumny w danych treningowych unikając powtórzeń zarówno wiersza jak i kolumny w obrębie klauzuli. Jeśli wartość bitu jest pozytywana to literał również zapisuje się jako pozytywny, w przypadku wartości negatywnej literał jest odpowiednio negatywny.

2. Negatywne, czyli takie, których celem jest bycie niespełnianą dla innej klasy decyzjnej.
Losowanie przebiega podobobnie, z tym, że w przypadku wylosowania bitu pozytywnego, tworzymy literał negatywny. Dodatkowo losowanie stara się unikać tylko powtarzania kolumny w obrębie jednej klauzuli.

## Ewaluator formuł logicznych(FormulaEvaluator)

Udostępnia takie metody jak zdefiniowane poniżej.
```c++
class FormulaEvaluator {
    float numericScore(
        Formula formula, 
        Data * data, 
        int classes_count, 
        int goal
    );

    bool formulaSatisfied(
        Formula formula, 
        Data data, 
        int row, 
        int attributes_count
    );
};
```
Pierwsza z nich zwraca wynik formuły dla podanych danych. Druga natomiast udostępnia metodę pozwalającą na sprawdzenie spełnialności formuły.







