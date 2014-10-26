1. makeCorpus.py and twaggregate.py are used for preprocess data for both methods.

2. dictnostops.txt lightly changed than the former edition (delete http...)

3. dacongress.py lightly changed: 
   adjust the parameters batchsize, D, K and tau_0 for aggregated data)
   change the input

4. sample_results included the results got : by gensim
					     by Vowpal Wabbit
					     by Vowpal Wabbit with aggregated data

5. 2 set of output lambda are also included