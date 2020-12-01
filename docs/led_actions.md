# Led Tweens \<WIP\>
define actions that can be performed on the LEDs for pehrty lites

Goals:
* Run actions in an event loop (not necessarily async, but maybe)
* Each action encapsulated in an object with an update method

Encapsulation gives:
* Ability to easily alter action behaviour at runtime via params / methods
* Ability to easily stop actions without them interfering

TODO: continue searching for good python tween library, or partial impl myself 
TODO:  convert brightness pingpong to use delta/tween (how does DOTween handle it?)

Resources
https://easings.net
\[?\] http://robertpenner.com/easing/penner_chapter7_tweening.pdf
http://dotween.demigiant.com/


