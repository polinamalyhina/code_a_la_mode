# code_a_la_mode

I've passed the Wood 3 and Wood 2 League with the modified code represented in Starter Kit (https://github.com/csj/code-a-la-mode/blob/master/src/test/starterkit/starterAI.py) There are many if...else constructions that keep tracking the state of the player.
When croissant appeared in recipes of Wood 1 league, I ran into a problem in which the input and output states in the loop are the same, so the code loops.
After much thought and unsuccessful insertion of an additional counter, I decided to reformat the code: start taking into account the specifics of orders (before, my chef did not make ORDERS, but simply the SAME DISH), track the availability of ready-made products, etc.
I believe that the implemented logic is correct and in general it should work, but unfortunately it does not.( At this stage, I can't find the error myself. I have used all my time and now I need an advice to get through this league. (I can provide the solution code for the previous steps upon request)
In this code, there is no talk about optimization yet; the primary task is to make it work in the form in which it already exists.
In the future, there is a plan to deal with the orders queue in more details, so that my chef starts making a FREE order, and NOT THE FIRST one in line, which the second chef has already taken.
