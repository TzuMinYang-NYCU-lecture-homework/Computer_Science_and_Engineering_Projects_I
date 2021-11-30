# IoTtalk-CHT
Connect IoTtalk and CHT.

## TODO
- [ ] 是否值得實作 semaphore 去應付 extreme case 對同一筆資料，還沒確定前一個操作執行完畢後下一筆操作就來了
- [ ] CHT reply timeout

## CHT side TODO
- [ ] 各 sensor 補充 range 欄位
- [ ] sensorname 待討論
- [ ] timestamp 到小數點下三位

## Question list
- 下指令給冷氣沒有聲音 feedback
- 沒試成功的
    - 空氣清淨機的 Lock、Mode
    - 智慧電扇的 Nature
    - 冷氣的 Clean
- 電扇的 Timer 是收到 3 時設定為 4 小時關機
- Spec 中冷氣的 Fuzzy 的 1 有太冷、太熱兩個意思
- 當 write 非預期值時，是否可在 writeValueReply 提醒
- ManagedSlaveList 變動時可否寄通知
- OnValueChanged 的 last 只要不一樣，必定差 500ms 以上

