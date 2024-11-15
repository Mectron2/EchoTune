# EchoTune 🎵

**EchoTune** — это игра, созданная на Python с использованием Pygame, где игроки проверяют свои навыки по воспроизведению текста песен и получают результаты с оценками в конце. Игра позволяет легко создавать свои карты и выбирать их скорость. Код писался давно, еще неопытным мной, и он, конечно, далеко не совершенен, но все же мне нравится этот проект. Возможно понравится и вам.

## Особенности игры

- 🎶 **Режим воспроизведения песен**: Выберите песню из меню и следуйте за текстом, чтобы повторить его максимально точно.
- ✨ **Шейдеры**: В игре используются небольшие шейдеры, которые, к сожалению, сильно бьют по производительности в виду неторопливости Python :( Однако, на хорошем железе все будет работать нормально, хотя, в любом случае, их можно отключить одной кнопкой.
- 📝 **Подсчет очков и оценка**: Получите процент совпадения и оценку за ваш результат после каждой песни.
- 📋 **Возможность создавать свобственные карты**: Вы можете легко создать свою карту и слушать то, что вам действительно нравится! О создании карт чуть позже.
- 🐋 **Выбор скорости**: Не успеваете за текстом? Или же слишком легко? Не проблема, вы всегда можете ускорить или замедлить игру.

## Запуск

- Склонируйте репозиторий
```
git clone https://github.com/Mectron2/EchoTune.git
```
- Перейдите в директорию приложения
```
cd EchoTune/compiled
```
- Запустите игру, открыв **EchoTune.exe**

И, конечно, вы можете запустить игру из исходного кода, но тот, кому это надо, думаю, разберется сам

## О создании карт

В директории **compiled** присутсвует папка **maps**, куда мы и будем помещать наши будущие карты. Как вы можете видеть – здесь уже есть 2 карты, но я предлагаю создать свою.

1. В директории ```compiled/maps``` создайте папку с названием вашей песни или карты (в меню игры будет отображаться именно название папки).
2. Создайте файл ```lyrics.json``` и заполните его таким образом: (Файл должен называться ```lyrics.json```. Это важно!)
```
{
    "song": "<Название песни>",
    "artist": "<Исполнитель>",
    "lyrics": [
        {
            "line": "<Первая строка песни>",
            "start": "<Время начала строки в формате СС:CC, например 00:01>",
            "end": "<Время конца строки в формате СС:CC, например 00:07>",
        },
        {
            "line": "<Вторая строка песни>",
            "start": "<Время начала строки в формате СС:CC, например 00:08>",
            "end": "<Время конца строки в формате СС:CC, например 00:14>",
        },
        ...
        {
            "line": "<Последняя строка песни>",
            "start": "<Время начала строки в формате СС:CC, например 01:15>",
            "end": "<Время конца строки в формате СС:CC, например 01:27>",
        }
    ]
}
```
3. Поместите в созданную папку песню в формате ```.wav```. Файл должен называться ```musuc.wav```. (Важно!)
4. Готово, запускайте игру и наслаждайтесь вашей любимой песней.

Игра создаст дополнительные строчки ```"font_size": {размер шрифта}``` в вашем файле ```lyrics.json``` и может создать дополнительные файлы ```lyrics_{скорость}.json``` и ```pitched.wav```. Это нормально и нужно для правильной синхронизации текста с песней.

## Спасибо за уделенное время и удачи (´▽`ʃ♡ƪ)
