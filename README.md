# email_chimp

<h2>Краткая документация по работе сервиса управления email рассылками</h2>
Стэк:
<ul>
  <li>Django и Django REST framework.</li>
  <li>БД - SQLite</li>
  <li>Celery</li>
  <li>RabbitMQ (docker)</li>
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
