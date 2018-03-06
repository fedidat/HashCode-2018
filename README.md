# HashCode-2018

This is our submission to Google's HashCode on March 1 2018.

![We scored 
18,482,501 point out of 50,000,000](score.png)

The basic algorithm goes this way:

1. Simulate step 0 by calculating the best ride for each vehicle to take, and keep its next_time_free in a list. Note that, since all vehicles start at (0, 0), we need not make a difference between vehicles.

2. Then, as long as there are undispatched rides, we fetch the next vehicle that goes free and dispatch it to the best ride.

What we mean by best ride is given by a generic score function. In this instance:

* we measure the feasibility of the ride, 

* we add some score for its distance from the vehicle's stopping coordinates. The lower distance the better, so we don't send vehicles to the end of the world.

* we add the ride's bonus.

At current time, some optimization bug prevents all rides from being dispatched at the higher levels.