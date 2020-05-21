## J.A.R.V.I.S

![](https://img.shields.io/badge/Python3-red)
![](https://img.shields.io/badge/ElasticSearch-green)
![](https://img.shields.io/badge/AI-blue)

This is a prototype to understand and learn on AI - Deep Learning, Neural Networks and NLP


### What he do?
I programed it to respond to me while working on my Mac book. Now Jarvis has following capabilities,

1) Greet me
2) Open any application running in my Mac - Eg: by saying "jarvis open outlook"
3) Ask me back if I am sitting idle, with out talking to Jarvis
4) If I tell Jarvis to sleep, it will greet me back for the day and go to infinite sleep till I woke him up

More proficiencies and code optimizations will be done in coming days

```
$ ./jarvis.py 
Listening to you...
hello Jarvis
Listening to you...
GET http://localhost:9200/voice_assistant/text/_search [status:400 request:0.005s]
Listening to you...
Jarvis open Outlook
Listening to you...
GET http://localhost:9200/voice_assistant/text/_search [status:400 request:0.004s]
Listening to you...
Jarvis open Outlook
Listening to you...
GET http://localhost:9200/voice_assistant/text/_search [status:400 request:0.003s]
Listening to you...
```
