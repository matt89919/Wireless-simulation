# wireless-simulation

best-effort algorithm's problem:
  the frequency of the base station is different, and the frequecy is the main cause of path loss, so when there is no enough cars, the switch time will be very low (also, cars always tend to connect to those base staitons who have low frequency)

min_threshold algorithm's problem:
  the switch time is decided by the threshold value(this value has a very little range because the signal strenth is too weak (and the number of bs is too small) )

entropy algorithm's problem:
  just like the min_threshold method, the range is small, if the entropy value is too large, the switch time will be very little (cannot be larger than 70 because the maximum signal stenth is 70)