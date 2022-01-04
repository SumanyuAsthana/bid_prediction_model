# bid_prediction_model
Created a reinforcement learning model based on Knapsack and random forest classifier that can accurately predict bids on items to make maximum profit.
The basic idea is the following:
We are given data with various parameters including the following budget for a certain day,costs of all items for that day and the profit for all these items.
I had to build a neural network that could learn to place bids on those items that yielded maximum profit at the end of the day.
To do so the following was the training process:
Run the knapsack algo to distribute the daily budget across the items that yielded max profit.
Train a random forest to predict 0 or 1 for not placing bid vs placing bid.
