# Introduction
Data tools to increase productivity in your workflow

# How to setup
Install with pip:
```
pip install core_graph
```


# Metrics in community finding:
## 1. Modularity

Modularity measures the strength of division of a network into communities. 
It compares the density of connections inside communities to the density of connections between communities.

Modularity values typically range from -1 to 1:
- Positive values indicate more edges within communities than would be expected by random chance.
- Negative values indicate fewer edges within communities than expected by random chance.

In practice, modularity values for real networks with good community structure often fall in the range of 0.3 to 0.7.

Using Modularity for Comparison:
- Higher modularity generally indicates a better community structure.
- You can compare the modularity scores of different community detection algorithms on the same network.
- The algorithm that produces the highest modularity score is often considered to have found the best community 
structure.

## 2. Codelength

Codelength is a central concept in Infomap's approach to community detection. 

It's based on the principle of data compression and information theory:
- Codelength represents the average number of bits needed to describe a random walk on the network.
- A lower codelength indicates a better partition of the network into communities.
- Infomap aims to minimize this codelength, which corresponds to finding the best community structure.

The codelength consists of two parts:
- The description length of movements between modules
- The description length of movements within modules
