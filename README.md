webconsole
==========
[[UNCOMPLETED]]
Просброс запуска консольных приложений в веб.

Задача:
Уметь запускать консольные приложения (например, скрипты диагностики) из веба, получать их вывод, 
интерактивно с ними работать

Данный демон будет конфигурироваться набором ini файлов для приложений, для каждой будут свои ссылки с параметрами
Если параметров будет недоставать - вернет html код с формой их ввода
Если хватит - вернет html с полем ввода и консолью, соедененной через websocket с демоном, который будет проксировать 
данные из stdin/out/err в веб и обратно

Также возможно реализовать список всех запущенных приложений, работа с 1 приложением из нескольких сессий браузера 
(вы можете запустить bash и использовать его вдвоем)

Пока что реализовано только тестовое окно с запуском bash.
