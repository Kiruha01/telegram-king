# Telegram King
Телеграм-бот для подсчёта очков в игре [Кинг](https://ru.wikipedia.org/wiki/Кинг_(игра))

[Рабочий бот](https://t.me/gameofking_bot) `@gameofking_bot` 

## Правила

Цель игры — набрать наибольшее количество очков, стараясь брать или не брать взятки.

### Раздача карт

В игре участвуют 32 карты (от семёрки до туза), если играют вчетвером, 30 карт (исключают
две чёрные семерки), если играют втроём и 16 карт(набор из валетов, дам, королей и тузов), если играют вдвоём.

### Ход игры

Во время каждого хода игрок должен скинуть одну из своих карт на стол той же масти, с которой 
начали ход. Если у игрока нет карты этой масти, ему разрешается бросить любую карту (если она 
допустима во время текущего кона). Игрок, бросивший самую высокую карту подходящей масти, берёт
взятку и кладёт возле себя. После каждого кона происходит подсчет очков.

### Подсчет очков

Очки начисляются по-разному в зависимости от кона. Данные для каждого кона представленные в 
таблице.

|                 Кон             |     Особенность кона   |                Для 2/3 игроков               | Для 4 игроков                                |
| :-----------------------------: | ---------------------- | -------------------------------------------- | -------------------------------------------- |
|        **Не брать взятки**      |         -              |          `-4` очка за каждую взятку          |          `-2` очка за каждую взятку          |
|         **Не брать черви**      | С червей ходить нельзя |       `-5` очков за каждую червовую карту    |      `-2` очка за каждую червовую карту      |
|       **Не брать мальчиков**    |         -              |        `-10` очков за каждого валета         |          `-4` очка за каждого валета         |
|        **Не брать девочек**     |         -              |          `-10` очков за каждую даму          |          `-4` очка за каждую даму            |
|        **Не брать "Кинга"**     | С червей ходить нельзя. Необходимо сбросить кинга при отсутствии подходящей карты | `-40` очков за Кинга | `-16` очков за Кинга |
| **Не брать 2 последние взятки** |         -              |     `-20` очков за каждую последнюю взятку   |     `-8` очков за каждую последнюю взятку    |
|      **Отрицательный Ералаш**   |  Учитываются все коны  | Очки начисляются, как за все предыдущие коны | Очки начисляются, как за все предыдущие коны |
|||||
|           **Брать взятки**      |         -              |          `+4` очка за каждую взятку          |           `+2` очка за каждую взятку         |
|            **Брать черви**      | С червей ходить нельзя |     `+5` очков за каждую червовую карту      |       `+2` очка за каждую червовую карту     |
|          **Брать мальчиков**    |         -              |        `+10` очков за каждого валета         |           `+4` очка за каждого валета        |
|           **Брать девочек**     |         -              |         `+10` очков за каждую даму           |           `+4` очка за каждую даму           |
|           **Брать "Кинга"**     | С червей ходить нельзя. Необходимо сбросить кинга при отсутствии подходящей карты | `+40` очков за Кинга | `+16` очков за Кинга |
|    **Брать 2 последние взятки** |         -              |    `+20` очков за каждую последнюю взятку    |      `+8` очков за каждую последнюю взятку   |
|      **Положительный Ералаш**   |  Учитываются все коны  | Очки начисляются, как за все предыдущие коны | Очки начисляются, как за все предыдущие коны |




## Типы состояний пользователя

* `start` - Состояние регистрации в игре 

* `names` - Состояние ввода имён игроков

* `negative_bribes` - кон "не брать взятки"
* `negative_hearts` - кон "не брать черви"
* `negative_boys` - кон "не брать мальчиков"
* `negative_girls` - кон "не брать девочек"
* `negative_king` - кон "не брать кинга"
* `negative_patchwork` - кон "отрицательный ералаш"


* `positive_bribes` - кон "брать взятки"
* `positive_hearts` - кон "брать черви"
* `positive_boys` - кон "брать мальчиков"
* `positive_girls` - кон "брать девочек"
* `positive_king` - кон "брать кинга"
* `positive_patchwork` - кон "положительный ералаш"

* `final` - Состояние результатов
