# wireless-simulation

best-effort algorithm's problem:
  the frequency of the base station is different, and the frequecy is the main cause of path loss, so when there is no enough cars, the switch time will be very low (also, cars always tend to connect to those base staitons who have low frequency)

min_threshold algorithm's problem:
  the switch time is decided by the threshold value(this value has a very little range because the signal strength is too weak (and the number of bs is too small) )

entropy algorithm's problem:
  just like the min_threshold method, the range is small, if the entropy value is too large, the switch time will be very little (cannot be larger than 70 because the maximum signal stength is 70)

my algorithm:
  combine minimum threshold and entropy, the threshold of my algo is 50, and entropy is 10 in my design.
  when the signal strength is larger than threshold value, there will be no switch.
  when is less than, the algo will find the largest signal strength base station and compare with the current one.
    if the difference is larger than entropy, switch. else, no switch happens.

  pros of my algo: less switch time than the two algo with the same parameter.  (0.055-0.08 times/car in my simulation)
                   compare to min_threshold method, we can have a higher threshold to ensure signal strength
                   compare to entropy, when the signal strength is enough, switch is not neccesery
  