Given the lists with suppliers' production, consumers' demand, and the matrix of supplier-to-consumer transportation costs, calculate the minimum cost of the products transportation which satisfied all the demand.

Notes
Costs-matrix legend: costs[i][j] is the cost of transporting 1 unit of produce from suppliers[i] to consumers[j]

The produce is identical - multiple suppliers can be the source for one consumer, and multiple consumers can be the target of one supplier

The produce is not important - it can be anything and have any price, we're only interested in transporting it efficiently

Total supply will always equal total demand

Your solution should pass 12 cases with matrices of size 150x150 as a performance test (the reference solution itself takes ~8500 ms to do so)

For all tests, 0 <= costs[i][j] <= 100

In performance tests, 1 <= suppliers[i], consumers[j] <= 10000

Disabled modules are scipy and sklearn

Disabled built-in functions are open, exec, eval, globals, locals and exit

Example
Given these inputs:

suppliers = [10, 20, 20]

consumers = [5, 25, 10, 10]

costs = 
    [2  5  3  0]
    [3  4  1  4]
    [2  6  5  2]
The shipments can be arranged the following way:

[            10]  | 10
[    10  10    ]  | 20
[ 5  15        ]  | 20
------------------+---
  5  25  10  10   |
By multiplying each element of this matrix by the corresponding element of the costs matrix, we get the result:

[             0]
[    40  10    ]  =>  0 + 40 + 10 + 10 + 90 = 150
[10  90        ]