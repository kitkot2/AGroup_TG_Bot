
<a name="readme-top"></a>

<br />
<div align="center">
  <a href="https://github.com/kitkot2/AGroup_TG_Bot">
  </a>

<h3 align="center">Group messages tg-bot</h3>

  <p align="center">
    Телеграм бот для отправки сообщений в вузах и школах.
    <br />
    <a href="https://github.com/kitkot2/AGroup_TG_Bot"><strong>Посмотреть файлы »</strong></a>
    <br />
    <br />
    <a href="https://github.com/kitkot2/AGroup_TG_Bot/issues">Сообщить об ошибке</a>
    ·
    <a href="https://github.com/kitkot2/AGroup_TG_Bot/issues">Предложить команду</a>
  </p>
</div>


<details>
  <summary>Оглавление</summary>
  <ol>
    <li>
      <a href="#о-проекте">О проекте</a>
      <ul>
        <li><a href="#Использованные библиотеки">Использованные библиотеки</a></li>
      </ul>
    </li>
    <li><a href="#Запуск бота">Запуск бота</a></li>
    <li><a href="#Команды">Команды</a></li>
    <li><a href="#Контакты">Контакты</a></li>
  </ol>
</details>


## О проекте

Данный бот позволяет учителям совершать рассылку организационной информации и домашнего задания по классам, в которых они преподают.

При этом, пользователям достаточно только зарегистрироваться в боте. Такой подход позволяет избежать возникновения информационных чатов для каждого предмета. 

Также, благодаря тому, что для отправки сообщений нужно указать только класс, это позволяет существенно улучшить конфиденциальность. Доступ к телеграм ID пользователей есть только у администратора, а такие данные как телефон и почта не требуются для регистрации.

<p align="right">(<a href="#readme-top">к началу</a>)</p>



### Использованные библиотеки

* aiogram
* pandas
* numpy

<p align="right">(<a href="#readme-top">к началу</a>)</p>


## Запуск бота

1. Получите токен написв BotFather
2. Скопируйте репозиторий
   ```sh
   git clone https://github.com/kitkot2/AGroup_TG_Bot.git
   ```
   Или скачайте его в виде .zip файла
3. Убедитесь, что у вас установлен python и pip
3. Установите библиотеки командой:
   ```sh
   pip install -r requirements.txt
   ```
4. Создайте файл token.txt в основной директории и вставьте туда свой токен
5. Бот запускается с помощью команды:
   ```sh
   python tg_bot.py
   ```
6. При правильном запуске в открывшейся командной строке должно быть написано: "Бот онлайн".

<p align="right">(<a href="#readme-top">к началу</a>)</p>


## Команды

Поддерживаемые команды:

* /start - начало работы с ботом
* /register - регистрация или обновление данных пользователя
* /send - отправка набранного сообщения указанному классу (только для учителей)
* /show - показать зарегистрированных учеников указанного класса (только для учителей)
* /cancel - отмена действия

Информация о пользователях сохраняется в .csv файл после прохождения регистрации. 

<p align="right">(<a href="#readme-top">к началу</a>)</p>


## Контакты

Котенко Никита - kotenko.na@phystech.edu

Кравцов Артем - kravtsov.aa@phystech.edu

Project Link: [https://github.com/kitkot2/AGroup_TG_Bot](https://github.com/kitkot2/AGroup_TG_Bot)

<p align="right">(<a href="#readme-top">к началу</a>)</p>


[contributors-shield]: https://img.shields.io/github/contributors/kitkot2/AGroup_TG_Bot.svg?style=for-the-badge
[contributors-url]: https://github.com/kitkot2/AGroup_TG_Bot/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/kitkot2/AGroup_TG_Bot.svg?style=for-the-badge
[forks-url]: https://github.com/kitkot2/AGroup_TG_Bot/network/members
[stars-shield]: https://img.shields.io/github/stars/kitkot2/AGroup_TG_Bot.svg?style=for-the-badge
[stars-url]: https://github.com/kitkot2/AGroup_TG_Bot/stargazers
[issues-shield]: https://img.shields.io/github/issues/kitkot2/AGroup_TG_Bot.svg?style=for-the-badge
[issues-url]: https://github.com/kitkot2/AGroup_TG_Bot/issues
