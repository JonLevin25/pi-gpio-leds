# Led Tweens \<WIP\>
define actions that can be performed on the LEDs for pehrty lites

Goals:
* Run actions in an event loop (not necessarily async, but maybe)
* Each action encapsulated in an object with an update method
* Actions composable/blendable to create cooler emergent behaviour

# TODO
0. NeoPixelRange: Support writing to temp buffer instead of pixels
0. NeoPixelTween:
    * Finish basic impl
    * Support Loop (type: only hardcoded `yoyo` for now)
    * `OnComplete` callback on each loop iteration completion
0. NeoPixelAnimator: Create Prototype. Req:
    * Support multi-layers of NeoPixelRanges (temp buffers)
    * Blending - only hardcoded "override" for now
    * `None` pixel on layer should not override layer underneath (or actual pixel if its the bottom layer)
0. `ColorCycle` / `BrightnessPingPong`: rewrite to use `NeoPixelTween`
0. `Chase` anim: group of pixels moving to the right / left, no wraparound (since that has overlap, more complex)
0. Animator PoC: 2 layers: `BrightnessYoyo + random deep colors`, `Chase` above it (stays active even when bottom layer turns lights off)

# Architecture:
## Considerations
Spent a while debating if I should tween statefully (_increment_ color/brightness etc. each frame, according to **last value** & anim duration)
or statelessly (_set_ color/bright/etc each frame, only according to time since last frame)

Since composing animations is important to me I leaned towards using deltas (stateful), but that creates a problem
in cases where you want to override a certain subset of pixels (i.e. sending a "pulse" of light through otherwise animated pixels)
or just control the weight of any animation layer. <br />
The solution I settled on for now is _blending_.

## Blending
 if I have more than one layer of animation,
I could blend them using weights + a `combine(aPixels, bPixels, aWeight, bWeight)` function.
With this solution, I can also use **stateless** animation, which is easier/more reliable.

* **This means the tween should _not_ set pixels directly, rather hold buffer array that may be blended before dumping to the pixel buffer. <br/>**

* **the temporary buffer should be able to hold `None` values to denote "ignore while blending"**

## Looping
Pingpong/Yoyo could be solved more generically using a "looping" construct similar to DOTween/other tweening libs.
in this case a full cycle would be 2 "loop iterations"


# Resources
* https://easings.net
* \[?\] http://robertpenner.com/easing/penner_chapter7_tweening.pdf
* http://dotween.demigiant.com/


