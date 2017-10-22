HackMD Changed Notify
=====================

This is a HackMD Change Notifier, it use to nofity
if the student changed there work on HackMD.

Currently, you should following the format of the works to
use this notifier.

For the format of works, please see this [example](https://hackmd.io/s/HyxQTaZj-)

Prerequirements
---------------

* `Python 3`
* `python3 -m pip install -r requirements.txt`


How to use
----------

### First time user

If you first time use `hackmd-changed-notify`, please make sure you
create the database via command line:

```
$ python hackmd-notify.py -d
2017-10-22 17:11:53 INFO  [hackmd-notify:202] Init database
```

### Import works from HackMD

* Please make sure you are using publish page! *

```
$ python hackmd-notify.py -i https://hackmd.io/s/HyxQTaZj-
2017-10-22 17:12:53 INFO  [hackmd-notify:206] Start parsing HackMD
2017-10-22 17:12:57 WARNI [hackmd-notify:138] parse-hackmd: "LinRiver    ", work: "phonebook" Can not get words
2017-10-22 17:12:57 WARNI [hackmd-notify:142]    - HackMD URL is not in publish mode! Please change it.
2017-10-22 17:12:57 WARNI [hackmd-notify:143]    - LinRiver - phonebook: https://hackmd.io/JwVgjMBsAcCmBMBaADGWZEBYyU4ghiPgMyLDKTxgBm0I8lyQA===#
2017-10-22 17:12:59 WARNI [hackmd-notify:116] works: "maskashura" gave a bad format of "開發紀錄(phonebook"
2017-10-22 17:13:01 WARNI [hackmd-notify:138] parse-hackmd: "yuan922     ", work: "ternary" Can not get words
2017-10-22 17:13:01 WARNI [hackmd-notify:142]    - HackMD URL is not in publish mode! Please change it.
2017-10-22 17:13:01 WARNI [hackmd-notify:143]    - yuan922 - ternary: https://hackmd.io/BwMwbArAJjDMC0B2ADBE8AsGCcj4CNgAmDeAY0QwEMjLgyiwMg
2017-10-22 17:13:01 WARNI [hackmd-notify:138] parse-hackmd: "yuan922     ", work: "phonebook" Can not get words
2017-10-22 17:13:01 WARNI [hackmd-notify:142]    - HackMD URL is not in publish mode! Please change it.
2017-10-22 17:13:01 WARNI [hackmd-notify:143]    - yuan922 - phonebook: https://hackmd.io/EYJgZgLArAJgHAdgLQgVAjEiBjHSCG2w+SAbMFAnAJxhRjZzZA
2017-10-22 17:13:01 WARNI [hackmd-notify:116] works: "ZixinYang" gave a bad format of "開發紀錄（clz）"
2017-10-22 17:13:02 WARNI [hackmd-notify:138] parse-hackmd: "tina0405    ", work: "ternary" Can not get words
2017-10-22 17:13:02 WARNI [hackmd-notify:142]    - HackMD URL is not in publish mode! Please change it.
2017-10-22 17:13:02 WARNI [hackmd-notify:143]    - tina0405 - ternary: https://hackmd.io/GYBg7GCGyQLAtAZgJwFNL1gEwEYGN4AOLAJhHgDYSBGFXAVkjFqA?view
2017-10-22 17:13:06 WARNI [hackmd-notify:138] parse-hackmd: "as23041248  ", work: "phonebook" Can not get words
2017-10-22 17:13:06 WARNI [hackmd-notify:142]    - HackMD URL is not in publish mode! Please change it.
2017-10-22 17:13:06 WARNI [hackmd-notify:143]    - as23041248 - phonebook: https://hackmd.io/KYJgDArARgHMCGBaM8YGNEBYBs2KPgmwwHYBONKTTMgZhADNN4g=?both
2017-10-22 17:13:06 WARNI [hackmd-notify:138] parse-hackmd: "as23041248  ", work: "clz" Can not get words
2017-10-22 17:13:06 WARNI [hackmd-notify:142]    - HackMD URL is not in publish mode! Please change it.
2017-10-22 17:13:06 WARNI [hackmd-notify:143]    - as23041248 - clz: https://hackmd.io/AwNgZgxg7FAcwFpjAKYBMEBZgFZGzWACMs0QBDctI4MKATkyA===?view
2017-10-22 17:13:08 WARNI [hackmd-notify:138] parse-hackmd: "williamchangTW", work: "ternary" Can not get words
2017-10-22 17:13:08 WARNI [hackmd-notify:142]    - HackMD URL is not in publish mode! Please change it.
2017-10-22 17:13:08 WARNI [hackmd-notify:143]    - williamchangTW - ternary: https://hackmd.io/IwIwHAJgnA7AxiAtAQwEwmYgLMArMFYANgDNEAGIiEOMKAUxOBKiA===#
2017-10-22 17:13:09 WARNI [hackmd-notify:138] parse-hackmd: "yang196569  ", work: "phonebook" Can not get words
2017-10-22 17:13:09 WARNI [hackmd-notify:142]    - HackMD URL is not in publish mode! Please change it.
2017-10-22 17:13:09 WARNI [hackmd-notify:143]    - yang196569 - phonebook: https://hackmd.io/IwDgzA7CBmBM0FowggQwQFmmhKwBNcBjAViKIAZhhUBTfEIA?view
2017-10-22 17:13:16 INFO  [hackmd-notify:208] Done, save the result to database
```

Please note that, if the page add some new people, or someone add a
new report on HackMD, you still can use this function to import new
works on HackMD, and the old data won't be override.

### Check if there is any update

After import the works, you can check if there is any update.

```
$ python hackmd-notify.py -c
2017-10-22 17:16:25 INFO  [hackmd-notify:211] Start to check all works in database
2017-10-22 17:16:26 CRITI [hackmd-notify:86] Bang, please check: ian910297 - ternary: https://hackmd.io/s/S1syEHzi-
2017-10-22 17:16:30 INFO  [hackmd-notify:215] Done, save the update result to database
```

You can also change the threshold of the words and minutes, default
words diff is 300, and minutes diff is 20.

```
$ python hackmd-notify.py -c --words 200 --minutes 10
$ python hackmd-notify.py -c --words 200 --minutes 100
$ python hackmd-notify.py -c --words 200
$ python hackmd-notify.py -c --minutes 13
```
