# email_chimp

<h1 align="center">Email sending service based on Python (Django REST framework)</h1>
<p align="center">

<img src="https://img.shields.io/badge/madeBy-KD3821-lightblue" >

<p align="center">Проект в рамках выполнениня тестового задания на вакансию <b>Python-разработчик (Django, DRF)</b><br>
<strong>Тестовое Задание:</strong><p>
<b>Сервис уведомлений</b><br>
Тестовое задание – дополнительный способ для нас убедиться в вашей квалификации и понять, какого рода задачи вы выполняете эффективнее всего.<br>
Расчётное время на выполнение тестового задания: 3-4 часа, время засекается нестрого. Приступить к выполнению тестового задания можно в любое удобное для вас время.<br>
У текущего тестового задания есть только общее описание требований, конкретные детали реализации остаются на усмотрение разработчика. Решение по стеку технологий, которые необходимы для решения задачи, также принимает кандидат по своему усмотрению.<br><br>
<b>Задача</b><br>
Необходимо разработать сервис управления рассылками API администрирования и получения статистики.<br><br>
<b>Описание</b><br>
<ul>
<li>
Необходимо реализовать методы создания новой рассылки, просмотра созданных и получения статистики по выполненным рассылкам.</li>
<li>
Реализовать сам сервис отправки уведомлений на внешнее API.</li>
<li>
Опционально вы можете выбрать любое количество дополнительных пунктов описанных после основного.</li>
Для успешного принятия задания как выполненного достаточно корректной и рабочей реализации требований по основной части, но дополнительные пункты помогут вам продемонстрировать ваши навыки в смежных технологиях.</li></ul>
<b>Критерии приёмки</b><br>
<ul><li>
Выполненное задание необходимо разместить в публичном репозитории на gitlab.com</li>
<li>
Понятная документация по запуску проекта со всеми его зависимостями</li>
<li>
Документация по API для интеграции с разработанным сервисом</li>
<li>
Описание реализованных методов в формате OpenAPI</li>
<li>
Если выполнено хотя бы одно дополнительное задание - написать об этом в документации, указав на конкретные пункты из списка ниже.</li></ul>
<b>Основное задание</b><br>
Спроектировать и разработать сервис, который по заданным правилам запускает рассылку по списку клиентов.<br><br>
<b>Сущность "рассылка" имеет атрибуты:</b><br>
<ul>
<li>
уникальный id рассылки</li>
<li>
дата и время запуска рассылки</li>
<li>
текст сообщения для доставки клиенту</li>
<li>
фильтр свойств клиентов, на которых должна быть произведена рассылка (код мобильного оператора, тег)</li>
<li>
дата и время окончания рассылки: если по каким-то причинам не успели разослать все сообщения - никакие сообщения клиентам после этого времени доставляться не должны</li></ul>
<b>Сущность "клиент" имеет атрибуты:</b><br>
<ul>
<li>
уникальный id клиента</li>
<li>
номер телефона клиента в формате 7XXXXXXXXXX (X - цифра от 0 до 9)</li>
<li>
код мобильного оператора</li>
<li>
тег (произвольная метка)</li>
<li>
часовой пояс</li></ul>
<b>Сущность "сообщение" имеет атрибуты:</b><br>
<ul><li>
уникальный id сообщения</li>
<li>
дата и время создания (отправки)</li>
<li>
статус отправки</li>
<li>
id рассылки, в рамках которой было отправлено сообщение</li>
<li>
id клиента, которому отправили</li></ul><br>
<b>Спроектировать и реализовать API для:</b><br>
<ul><li>
добавления нового клиента в справочник со всеми его атрибутами</li>
<li>
обновления данных атрибутов клиента</li>
<li>
удаления клиента из справочника</li>
<li>
добавления новой рассылки со всеми её атрибутами</li>
<li>
получения общей статистики по созданным рассылкам и количеству отправленных сообщений по ним с группировкой по статусам</li>
<li>
получения детальной статистики отправленных сообщений по конкретной рассылке</li>
<li>
обновления атрибутов рассылки</li>
<li>
удаления рассылки</li>
<li>
обработки активных рассылок и отправки сообщений клиентам</li></ul>
<b>Логика рассылки</b><br>
<ul><li>
После создания новой рассылки, если текущее время больше времени начала и меньше времени окончания - должны быть выбраны из справочника все клиенты, которые подходят под значения фильтра, указанного в этой рассылке и запущена отправка для всех этих клиентов.</li>
<li>
Если создаётся рассылка с временем старта в будущем - отправка должна стартовать автоматически по наступлению этого времени без дополнительных действий со стороны пользователя системы.</li>
<li>
По ходу отправки сообщений должна собираться статистика (см. описание сущности "сообщение" выше) по каждому сообщению для последующего формирования отчётов.</li>
<li>
Внешний сервис, который принимает отправляемые сообщения, может долго обрабатывать запрос, отвечать некорректными данными, на какое-то время вообще не принимать запросы. Необходимо реализовать корректную обработку подобных ошибок. Проблемы с внешним сервисом не должны влиять на стабильность работы разрабатываемого сервиса рассылок.</li></ul>
<b>API внешнего сервиса отправки</b><br>
Для интеграции с разрабатываемым проектом в данном задании существует внешний сервис, который может принимать запросы на отправку сообщений в сторону клиентов.<br>
OpenAPI спецификация находится по адресу: https://probe.fbrq.cloud/docs<br>
В этом API предполагается аутентификация с использованием JWT. Токен доступа предоставлен вам вместе с тестовым заданием.<br><br>

<b>Дополнительные задания</b><br>
Опциональные пункты, выполнение любого количества из приведённого списка повышают ваши шансы на положительное решение о приёме<br>
<ol>
<li>
организовать тестирование написанного кода</li>
<li>
обеспечить автоматическую сборку/тестирование с помощью GitLab CI</li>
<li>
подготовить docker-compose для запуска всех сервисов проекта одной командой</li>
<li>
написать конфигурационные файлы (deployment, ingress, …) для запуска проекта в kubernetes и описать как их применить к работающему кластеру</li>
<li>
сделать так, чтобы по адресу /docs/ открывалась страница со Swagger UI и в нём отображалось описание разработанного API. Пример: https://petstore.swagger.io</li>
<li>
реализовать администраторский Web UI для управления рассылками и получения статистики по отправленным сообщениям</li>
<li>
обеспечить интеграцию с внешним OAuth2 сервисом авторизации для административного интерфейса. Пример: https://auth0.com</li>
<li>
реализовать дополнительный сервис, который раз в сутки отправляет статистику по обработанным рассылкам на email</li>
<li>
удаленный сервис может быть недоступен, долго отвечать на запросы или выдавать некорректные ответы. Необходимо организовать обработку ошибок и откладывание запросов при неуспехе для последующей повторной отправки. Задержки в работе внешнего сервиса никак не должны оказывать влияние на работу сервиса рассылок</li>
<li>
реализовать отдачу метрик в формате prometheus и задокументировать эндпоинты и экспортируемые метрики</li>
<li>
реализовать дополнительную бизнес-логику: добавить в сущность "рассылка" поле "временной интервал", в котором можно задать промежуток времени, в котором клиентам можно отправлять сообщения с учётом их локального времени. Не отправлять клиенту сообщение, если его локальное время не входит в указанный интервал</li>
<li>
обеспечить подробное логирование на всех этапах обработки запросов, чтобы при эксплуатации была возможность найти в логах всю информацию по
<ul><li>
id рассылки - все логи по конкретной рассылке (и запросы на api и внешние запросы на отправку конкретных сообщений)</li>
<li>
id сообщения - по конкретному сообщению (все запросы и ответы от внешнего сервиса, вся обработка конкретного сообщения)</li>
<li>
id клиента - любые операции, которые связаны с конкретным клиентом (добавление/редактирование/отправка сообщения/…)</li></ul></li>
</ul>
<h2>Краткая документация по работе сервиса управления email рассылками</h2>
Стэк:
<ul>
  <li>Django и Django REST framework.</li>
  <li>БД - SQLite</li>
  <li>Celery ( запустить командой: python -m celery -A emails worker -l info )</li>
  <li>RabbitMQ ( запустить в docker контейнере: docker run -d -p 5672:5672 rabbitmq )</li>
</ul>
Сущности проекта:
<ul>
  <li>Tag - тег</li>
  <li>Carrier - сотовой оператор</li>
  <li>Filter - фильтр свойств клиента</li>
  <li>Customer - клиент</li>
  <li>Campaign - рассылка</li>
  <li>Email - сообщение</li>
</ul>

<pre>
_Carrier_    ___Customer__             
    \____\__/____/  |      \____Email____    
          \/        |                     \_Campaign_
_Tag______/\______Slug____________________ email_filter
    \___________/                         
</pre>

<p>
    В первую очередь создаем Тэги и Сотовых операторов, далее их комбинации объединяем в Фильтры.</br>
    Затем создаем Клиентов. В момент создания Рассылки (POST http://127.0.0.1:8000/api/campaigns/) запускается процесс создания и отправки Сообщений с помощью Celery и RabbitMQ:<br> - если в БД есть Клиенты, подходящие по Фильтру, и время запуска рассылки уже наступило - запускается task для Celery c таймером остановки в тот момент, когда наступит время остановки рассылки, уазанное в параметрах при создании рассылки (также перед отправкой запроса на API - каждый раз сверяется текущее время и время остановки рассылки).<br> - Если время не настуипило - тогда запускается такой же task для Celery, но дополнительным параметром передается таймер времени запуска рассылки.
</p>
<h3>Таблица ендпоинтов</h3>

<table>
<thead>
<tr>
  <th>HTTP Verb</th>
  <th>Scope</th>
  <th>Semantics</th>
  <th>URL</th>
</tr>
</thead>
<tbody>
<tr>
  <td>GET</td>
  <td>Reports</td>
  <td>Report All Campaigns</td>
  <td>http://127.0.0.1:8000/api/report_all/</td>
</tr>
<tr>
  <td>GET</td>
  <td>Reports</td>
  <td>Report All Emails of Campaign</td>
  <td>http://127.0.0.1:8000/api/emails/?campaign_id__id={id}</td>
</tr>
<tr>
  <td>GET</td>
  <td>Tags</td>
  <td>List Tags</td>
  <td>http://127.0.0.1:8000/api/tags/</td>
</tr>
<tr>
  <td>POST</td>
  <td>Tags</td>
  <td>Create Tag</td>
  <td>http://127.0.0.1:8000/api/tags/</td>
</tr>
<tr>
  <td>GET</td>
  <td>Tags</td>
  <td>Retrieve Tag</td>
  <td>http://127.0.0.1:8000/api/tags/{id}/</td>
</tr>
<tr>
  <td>PATCH</td>
  <td>Tags</td>
  <td>Update Tag</td>
  <td>http://127.0.0.1:8000/api/tags/{id}/</td>
</tr>
<tr>
  <td>DELETE</td>
  <td>Tags</td>
  <td>Delete Tag</td>
  <td>http://127.0.0.1:8000/api/tags/{id}/</td>
</tr>
<tr>
  <td>GET</td>
  <td>Carriers</td>
  <td>List Carriers</td>
  <td>http://127.0.0.1:8000/api/carriers/</td>
  </tr>
<tr>
  <td>POST</td>
  <td>Carriers</td>
  <td>Create Carrier</td>
  <td>http://127.0.0.1:8000/api/carriers/</td>
</tr>
<tr>
  <td>GET</td>
  <td>Carriers</td>
  <td>Retrieve Carrier</td>
  <td>http://127.0.0.1:8000/api/carriers/{id}/</td>
</tr>
<tr>
  <td>PATCH</td>
  <td>Carriers</td>
  <td>Update Carrier</td>
  <td>http://127.0.0.1:8000/api/carriers/{id}/</td>
</tr>
<tr>
  <td>DELETE</td>
  <td>Carriers</td>
  <td>Delete Carrier</td>
  <td>http://127.0.0.1:8000/api/carriers/{id}/</td>
</tr>
<tr>
  <td>GET</td>
  <td>Filters</td>
  <td>List Filters</td>
  <td>http://127.0.0.1:8000/api/filters/</td>
  </tr>
<tr>
  <td>POST</td>
  <td>Filters</td>
  <td>Create Filter</td>
  <td>http://127.0.0.1:8000/api/filters/</td>
</tr>
<tr>
  <td>GET</td>
  <td>Filters</td>
  <td>Retrieve Filter</td>
  <td>http://127.0.0.1:8000/api/filters/{id}/</td>
</tr>
<tr>
  <td>PATCH</td>
  <td>Filters</td>
  <td>Update Filter</td>
  <td>http://127.0.0.1:8000/api/filters/{id}/</td>
</tr>
<tr>
  <td>DELETE</td>
  <td>Filters</td>
  <td>Delete Filters</td>
  <td>http://127.0.0.1:8000/api/filters/{id}/</td>
</tr>
<tr>
  <td>GET</td>
  <td>Customers</td>
  <td>List Customers</td>
  <td>http://127.0.0.1:8000/api/customers/</td>
  </tr>
<tr>
  <td>POST</td>
  <td>Customers</td>
  <td>Create Customer</td>
  <td>http://127.0.0.1:8000/api/customers/</td>
</tr>
<tr>
  <td>GET</td>
  <td>Customers</td>
  <td>Retrieve Customer</td>
  <td>http://127.0.0.1:8000/api/customers/{id}/</td>
</tr>
<tr>
  <td>PATCH</td>
  <td>Customers</td>
  <td>Update Customer</td>
  <td>http://127.0.0.1:8000/api/customers/{id}/</td>
</tr>
<tr>
  <td>DELETE</td>
  <td>Customers</td>
  <td>Delete Customer</td>
  <td>http://127.0.0.1:8000/api/customers/{id}/</td>
</tr>
<tr>
  <td>GET</td>
  <td>Campaigns</td>
  <td>List Campaigns</td>
  <td>http://127.0.0.1:8000/api/campaigns/</td>
  </tr>
<tr>
  <td>POST</td>
  <td>Campaigns</td>
  <td>Create Campaign</td>
  <td>http://127.0.0.1:8000/api/campaigns/</td>
</tr>
<tr>
  <td>GET</td>
  <td>Campaigns</td>
  <td>Retrieve Campaign</td>
  <td>http://127.0.0.1:8000/api/campaigns/{id}/</td>
</tr>
<tr>
  <td>PATCH</td>
  <td>Campaigns</td>
  <td>Update Campaign</td>
  <td>http://127.0.0.1:8000/api/campaigns/{id}/</td>
</tr>
<tr>
  <td>DELETE</td>
  <td>Campaigns</td>
  <td>Delete Campaign</td>
  <td>http://127.0.0.1:8000/api/campaigns/{id}/</td>
</tr>
<tr>
  <td>GET</td>
  <td>Emails</td>
  <td>List Emails</td>
  <td>http://127.0.0.1:8000/api/emails/</td>
  </tr>
<tr>
  <td>POST</td>
  <td>Emails</td>
  <td>Create Email</td>
  <td>http://127.0.0.1:8000/api/emails/</td>
</tr>
<tr>
  <td>GET</td>
  <td>Emails</td>
  <td>Retrieve Email</td>
  <td>http://127.0.0.1:8000/api/emails/{id}/</td>
</tr>
<tr>
  <td>PATCH</td>
  <td>Emails</td>
  <td>Update Email</td>
  <td>http://127.0.0.1:8000/api/emails/{id}/</td>
</tr>
<tr>
  <td>DELETE</td>
  <td>Emails</td>
  <td>Delete Email</td>
  <td>http://127.0.0.1:8000/api/emails/{id}/</td>
</tr>
</tbody>
</table>
