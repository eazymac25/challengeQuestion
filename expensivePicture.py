'''
Created on Oct 1, 2016

@author: kmacneneyjr
'''
import numpy as np
import random
import math
import pandas as pd
import matplotlib.pyplot as plt



class picture(object):
    def __init__(self,low,high,mean = 10000.0, stdev = 1000.0, name="picture",dist = 'default'):
        self.dist = dist
        if dist =='default':
            self.price = random.randint(low,high)
        elif dist == 'normal':
            self.price = np.random.normal(mean,stdev)
        elif dist == 'uniform':
            self.price = np.random.uniform(low,high)
        else:
            raise ValueError('dist = {0} is not an accepted distribution'.format(dist))
        self.name = name
        
    def __str__(self):
        return "Picture named {0} worth ${1}".format(self.name,str(self.price))
        
class room(object):
    
    def __init__(self,low,high,total=100,mean = 0, stdev = 1.0,dist='default'):
        self.low = low
        self.high = high
        self.itotal = total
        self. ctotal = total
        
        self.imax,self.imin,self.mean,self.stdev,self.m2 = 0,0,0.0,0.0,0.0
        self.pictures = []
        
        if total > 0:
            self.pictures = [picture(low,high,mean = mean, stdev=stdev,name="picture " +str(x),dist=dist) for x in range(total)]
            self.imax, self.imin = self.pictures[0].price,self.pictures[0].price
            t = 0.0
            for p in self.pictures:
                if p.price > self.imax:
                    self.imax = p.price
                if p.price < self.imin:
                    self.imin = p.price
                t += p.price
                self.m2 += (p.price)**2
            self.mean = t/self.ctotal
            self.stdev = math.sqrt(((self.m2 - float(self.ctotal)*(self.mean)**2))/(float(self.ctotal)-1.))
                
        self.cmax = self.imax
        self.cmin = self.imin
    
    def remove(self):
        if len(self.pictures) > 0:
            pic = self.pictures.pop()
            self.recalculateMeanStDev(pic,sign=-1)
            self.updateMinMax(pic.price)
            self.ctotal -= 1
            return pic
        return None
    
    def add(self,pic):
        if (pic.price <= self.high and pic.price >= self.low) or pic.dist!= 'default':
            self.pictures += [pic]
            self.updateMinMax(pic.price)
            self.recalculateMeanStDev(pic)
            self.ctotal += 1
        else: 
            raise ValueError("Picture doesn't belong in this room")
        
    def updateMinMax(self,price):
        if price > self.cmax:
            self.cmax = price
        if price< self.cmin:
            self.cmin = price
    
    def recalculateMeanStDev(self,newPic,sign=1):
        price = newPic.price if sign >= 1 else newPic.price*-1.0
        total = self.ctotal if sign >= 1 else self.ctotal - 1
        
        self.mean = (self.mean*total + price)/(total+1)
        self.m2 += (float(price))**2
        self.stdev = math.sqrt((self.m2-((total*1. + 1)*(self.mean)**2))/float(total)) if total else 1
            
        
class picker(object):
    def __init__(self,minprice = 100, maxprice = 100000,mean=100000.0,stdev=100000.0, total = 100,dist ='default'):
        self.fR = room(minprice,maxprice,total=total,mean=mean,stdev=stdev,dist=dist)
        self.discard = room(minprice,maxprice,total=0)
        self.winner = None
        self.payOff = 0
        
    
    def strat(self,threshold,minSize):
        
        for p in range(len(self.fR.pictures)):
            std = self.discard.stdev
            m = self.discard.mean
            ptemp = self.fR.remove()
            
            z = (ptemp.price*1. - m*1.)/std if std else 0
            #print len(self.fR.pictures)
            
            if len(self.fR.pictures) < 1:
                self.setWinner(ptemp)
                self.payOff = (1.*self.winner.price)/(1.*self.fR.imax)
                return self.payOff
            elif z>=threshold and self.discard.ctotal >= minSize:
                self.setWinner(ptemp)
                self.payOff = (1.*self.winner.price)/(1.*self.fR.imax)
                return self.payOff
            self.discard.add(ptemp)
            #print ptemp.price
            
        return None      
            
        
    def setWinner(self,painting):
        self.winner = painting
        
    



if __name__ == '__main__':
    
    
    dist = 'default'
    dist = 'normal'
    ntrials = 1000
    data = pd.DataFrame()
     
    def drange(start,stop,step):
        m = start
        while m < stop:
            yield m
            m+= step
             
    for t in drange(-3.0,3.0,0.1):
        pay = []
        for n in range(ntrials):
            pick = picker(dist=dist)
            result = pick.strat(t,20)
            pay += [result]
        temp = pd.Series(pay)
        data[str(t)] = temp
    #print data.head(5)
    print data.describe()
    newdata = data.mean(axis=0)
    plt.figure()
    newdata.plot.bar()
    plt.show()

#     data = pd.DataFrame({'a':[1,2,3,4]})
#     print data.mean(axis=0)
    
    
        
        
    
    