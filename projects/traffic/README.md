Approach 1:

First time trying my hand at neural networks. I've decided to start with the same structure that was used in the lecture for handwriting classification

Convolution layer - 32 filters, 3x3 kernal
Pool layer - Max pooling, 2x2
Flatten
Hidden layer - 128 neurons, relu, 50% dropout
Output - NUM_CATEGORIES neurons, softmax

The training accuracy capped at 88.9%. The testing accuracy however was a much better 96.6%.

---

Approach 2:

Keeping everything else constant, I dooubled the colvolution filters to compare the effect of this parameter on the training

As it's training I can feel my pc slowing down and having some trouble keeping up with chrome and other things. Potato pc problems, but goes to show the resource cost of all the calculus going on in there.

Even this time, the testing accuracy (97.2%) is significantly better than the training accuracy (87.4%). Wonder why that is; this wasn't the case with the lecture's network.

---

Approach 3:

I increased the number of convulution layers, as well as the filters in each layer. Also doubled the hidden layers and increased the number of neurons significantly. This seems like a very overkill network

Convolution layer - 128 filters, 5x5 kernal
Pool layer - Max pooling, 2x2
Convolution layer - 64 filters, 3x3 kernal
Pool layer - Max pooling, 2x2
Flatten
Hidden layer - 600 neurons, relu, 50% dropout
Hidden layer - 64 neurons, relu, 50% dropout
Output - NUM_CATEGORIES neurons, softmax

For this overkill network, the epoch-wise increase in accuracy was the most dramatic. It was, however, resourcefully very slow

---

Approach 4:

After some experimentation mainly with the number of neurons in the two hidden layer, I have settled on this model.

Convolution layer - 32 filters, 5x5 kernal
Pool layer - Max pooling, 2x2
Convolution layer - 64 filters, 3x3 kernal
Pool layer - Max pooling, 2x2
Flatten
Hidden layer - 400 neurons, relu, 50% dropout
Hidden layer -175 neurons, relu
Output - NUM_CATEGORIES neurons, softmax

This model is still relatively large, but gets a very good accuracy score, which is what I was prioritizing.
Training accuracy: 98.3%
Testing accuracy: 98.8%
