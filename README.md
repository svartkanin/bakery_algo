# What is it
This is a demonstration of the knapsack problem in form of a bakery order distribution application. It processed an order and distributes given packaging sizes to cover the order by using the minimum cost and packaging required.


## Installing packages
To run the application the following packages must be installed

- python3-pytest
- python3.7


### Run the code 

```python3 app/app.py```


### Run the tests 

```pytest-3```

There are currently 3 test cases:

- Test the correct workflow of the algorithm, meaning test the correct result of the packaging
- Test error when packaging is not possible
- Test error on wrong code



## Packging algorithm (Derived form of the knapsack problem)

The algorithm builds the final result from the bottom up. 
It will calculate the packaging for each order [0, actual_order], whereas the currently calculated order is build on the previously calculated orders. 
Walkthrough for `11 CF` with packaging [9,5,3]:

1. Order 0 -> nothing to do, set to [0,0,0]
2. Order 1 -> Cannot be build with from any packaging number since all are bigger; set to -1
3. Order 2 -> Cannot be build with from any packaging number since all are bigger; set to -1
4. Order 3 -> Only packaging 3 works, check (order-3) which is [0,0,0] and either use previous packaging or add 1; result is [0,0,1]
5. Order 4 -> Only packaing 3 works, however (order-3) is set to -1 (couldn't be build), therefore we can't build this one either; set to -1
6. Order 5 -> Only packaging 3 works, however (order-3) is set to -1 (couldn't be build), therefore we can't build this one either; set to -1
7. Order 6 -> Packaging 5 works, however order 1 is -1 so no; packaging 3 works, so look at (order-3) which was [0,0,1] and we add +1 for the packaging 3; result is [0,0,2]
8. Order 7...; result set to -1
9. Order 8...; result set to [0,1,1]
10. Order 9...; result set to [1,0,0]
11. Order 10...; result set to [0,2,0]
11. Order 11...; result set to [0,2,1]
