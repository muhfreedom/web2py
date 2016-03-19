# -*- coding: utf-8 -*-
# try something like
import random 
def histogram():
    dataset = [(random.randint(1,6) + random.randint(1,6)) for i in range(100)]
    return dict(dataset=dataset, title='D3.js Histogram')
