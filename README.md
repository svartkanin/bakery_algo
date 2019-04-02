
# Required packages

python3-pytest
python3.7


# Run the code 

python3 app/app.py


# Run the tests 

pytest-3

There are currently 3 test cases:

- Test the correct workflow of the algorithm, meaning test the correct result of the packaging
- Test error when packaging is not possible
- Test error on wrong code


# Workflow

After running the program the current product list is printed; the user can now enter an order in the command line and get the total amount, as well as the breakdown of which packages have been used.
Currently only orders that are able to be packaged without any rest are processed, otherwise a message will be printed indicated that the order could not be processed. 

E.g. 

$ python3 app/app.py
...
Please enter an order: 11 CF
'11 CF' total: $21.85
               1 x 5 $9.95
               2 x 3 $5.95

Please enter an order: 7 CF
Packaging not possible for this order: Order '7 CF'

Please enter an order: 11 AA
No product with that code could be found: Order '11 AA'


# Packging algo

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
