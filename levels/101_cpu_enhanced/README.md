# Level 101: CPU Enhanced monitoring
In the previous level, we wrote a simple program to evaluate how much CPU the container was using over a 60 second duration. While averages may be ok for some applications, you may be surprised to find how much CPU you may actually be utilizing.

## Relevant Documentation
* [cgroup v2 Documentation](https://www.kernel.org/doc/Documentation/cgroup-v2.txt)
* [Percentiles](https://en.wikipedia.org/wiki/Percentile)

## Exercises
* Write code that provides the 90th, 95th and 100th(Max) percentile CPU usage of the container over a minute duration

## How to run the excercise

## How to check your work
Look at the output of your program and you should see a 95th percentile CPU usage of 80-90%
