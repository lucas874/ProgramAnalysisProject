## DSJAKLDJALK 

Weird things with the if thing. Issue is this: if we have for instance [l1, h1] < [l2, h2] then we either have
* h1 < l2, in which case we jump to target 
* or l1 >= h2 in which case we carry on and increment pc by 1
* or neither of these two scenarios. Then we should continue with two paths: taking the jump and continuing incrementing pc by one. 
	* But if the compared values where loaded from locals we should somehow change them in the locals array? Force ordering, get the state implied by comparison in corresponding branch
	* We can do this, because we track variables loaded from locals when we load them to stack. 
	* But i think it does not really make sense when we compare two variables where both are non constants loaded from locals... 
	* It seems weird to force on or the other to be smaller/larger etc. how could we do that in a meaning full way, without making up stuff, how do we know where in the intervals to 'cut'?
	* We can do it when one of the compared values is a constant not loaded from the locals though i think? 
	* So suggestion is to check for this condition and make appropriate changes in the locals for that branch. copy of locals for that branch. 
	* e.g. [0, 5] < [2, 2]. Where [0, 5] has been loaded from locals at index 1 and [2,2] is a constant not loaded from locals. In if branch put [0, 1] at locals[1]. in else branch put [3, 5] at locals[1].
* ???
