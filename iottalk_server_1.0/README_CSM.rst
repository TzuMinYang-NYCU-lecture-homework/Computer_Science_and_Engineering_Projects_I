
前題
====

- 所有 API function 成功的話會回 200 OK。

- 錯誤的 request (e.g., json 個式不對/沒給必要的參數/參數型態不對) 會回傳 4xx，
  並且在 response body 會有簡易說明。

- 若拿到回傳值 5xx，這是 bug，請回報。

- csmapi 相容於 Python2, 3，需要安裝第三方套件 requests，可透過 pip 安裝。
  官網: `<http://docs.python-requests.org/en/latest/>`_

- csmapi 在參教有給錯/使用錯誤時，會丟 Exception，錯誤訊息會在 Exception 裡。

- 網路版 CSM 的 endpoint 一樣在 ``http://openmtc.darkgerm.com:9999`` ，
  在遠端使用 csmapi 時記得先去改檔首的 ENDPOINT 設定。


list_all
========

- debug 用，用瀏覽器看: `<http://openmtc.darkgerm.com:9999/list_all>`_

- 這不是 API 的一部份，請不要在程式裡呼叫。


create API function
===================

- HTTP message example::

    POST /C860008BD249 HTTP/1.1
    Content-Type: application/json
    Content-Length: 193

    {"profile": { "d_name": "D1",
                  "dm_name": "MorSensor",
                  "u_name": "yb",
                  "is_sim": false,
                  "df_list": ["Acceleration", "Temperature"]}}

- csmapi example::

    csmapi.create('C860008BD249', {
        'd_name': 'D1',
        'dm_name': 'MorSensor',
        'u_name': 'yb',
        'is_sim': False,
        'df_list': ['Acceleration', 'Temperature'],
    })

- profile dictionary 必要欄位:
    - d_name: device name (與以前一樣)。
    - dm_name: device model name (與以前一樣)。
    - u_name: user name (與以前一樣，simulator 可以填 null)。
    - is_sim: 是否為 simulator，一般 device 要設成 false。
    - df_list: 一個 list 裡面列出 device 擁有的 feature name (以前叫 features)。


push API function
=================

- HTTP message example::

    PUT /C860008BD249/Acceleration HTTP/1.1
    Content-Type: application/json
    Content-Length: 21

    {"data": [0, 0, 9.8]}

- csmapi example::

    csmapi.push('C860008BD249', 'Acceleration', [0, 0, 9.8])

- profile 不可被修改。


pull API function
=================

- HTTP message example::

    GET /C860008BD249/Acceleration HTTP/1.1

- HTTP response body::

    {"samples": [["2015-10-16 21:07:17.005919", [0, 0, 9.8]], ["2015-10-16 21:04:39.997805", [0, 0, 9.8]]]}

- csmapi example::

    csmapi.pull('C860008BD249', 'Acceleration')

- return value::

    [['2015-10-16 21:07:44.794336', [0, 0, 9.8]], ['2015-10-16 21:07:17.005919', [0, 0, 9.8]]]

- ``[<timestamp>, <data>]`` 稱為一個 sample。

- 現在只會回傳兩筆 sample，前面的比較新。
    - 沒資料時回傳空 list, e.g., ``{"samples": []}`` 。
    - 只有一筆資料時回傳 1-elem list,
      e.g., ``{"samples": [['2015-10-16 21:07:44.794336', [0, 0, 9.8]]]}`` 。

- 一樣可以 pull profile，內容會與 create 時傳的一樣，並且會多一欄 min_max
  (Simulator 使用)。


delete API function
===================

- HTTP message example::

    DELETE /C860008BD249 HTTP/1.1

- csmapi example::

    csmapi.delete('C860008BD249')

- 除了 HTTP method 改用 DELETE 外其他與以前一樣。


tree API function
=================

- HTTP message example::

    GET /tree HTTP/1.1

- HTTP response body::

    {"C860008BD249": ["Temperature", "Acceleration", "profile"]}

- csmapi example::

    csmapi.tree()

- return value::

    {'C860008BD249': ['Temperature', 'Acceleration', 'profile']}

- 與以前一樣。應該只有 Simulator 需要使用。

