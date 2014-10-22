Mixture Models and Gibbs Sampler
======

Gibbs Sampler implementation for Mixture Models

Scope for improvements : 
 - Vectorized calculations
 - Real time plot of log likelihood
 - Most of the values of probability are in the range 1e-20 to 1e-100

![alt tag](https://github.com/prateekpg2455/GibbsSampler/blob/master/plot.jpeg)
No. of Iterations : 3000, Burnin : 1000, No. of Points = 100, No. of Clusters = 10

I got a burning phase of 1000 iterations after which change in log likelihood was of only 2.00
while the total log likelihood was around -400.0. Not going beyond the computing capacity I
took number of clusters as 10 and sampled total of 100 points. The end result indicates that it
can recognize only fewer number of clusters. It seems like when there is not much data from
each clusters it groups those clusters. This can be interpreted as hierarchy on groups. My guess
is that more number of points per cluster will result in better clustering.
 
