import random as rnd
import statistics as stc
import math as math


# pypi-AgEIcHlwaS5vcmcCJGYyMmUyMzM2LTNiMzUtNDY3NC1hYmU5LTc4YjhiMGRmZTA2NQACKlszLCIzY2IyNWRlZC1hMjZiLTQ4MjYtYWRiYS1hN2UyYjllNzUzMzIiXQAABiAeVHoGOuJH_k8SOapUmMPAJIeOtpBSGG9NkaA5hVCc1Q

class Gbemisola_Math_General:

    def __init__(self, length=0, breath=0, base=0, height=0, square_number=0, random_range=0, square_root=0, square=0, mode=[], mean=[]):

        self.length =length
        self.breath =breath
        self.base =base
        self.height = height
        self.square_number =square_number
        self.random_range =random_range
        self.square_root =square_root
        self.square =square
        self.mode =mode
        self.mean =mean

        """
        Function to output the characteristics of Gbemisola_Math_General

        Args: 
            length(int), 
            breath(int), 
            base(int), 
            height(int), 
            square_number(int), 
            random_range(int), 
            square_root(int), 
            square(int), 
            mode(array), 
            mean(array)

        Attributes:
            length: length of a rectangle, 
            breath: breath of a rectangle, 
            base: base of a triangle, 
            heigh: height of a rectangle, 
            square_number: squart number, 
            random_range: randome Range Number, 
            square_root: square root number, 
            square: square number of a square, 
            mode: array of numbers to get the mode, 
            mean: array of numbers to get the mean
        """

    def set_area_triangle(self, base, height):
        self.base =base
        self.height =height
        return self.base, self.height

    def get_area_triangle(self):
        result =0.5*(self.base*self.height)
        return result


    def set_area_rectangle(self, length, breath):
        self.length =length
        self.breath =breath
        return self.length, self.breath
    
    def get_area_rectangle(self):
        result =self.length*self.breath
        return result

    
    def set_area_square(self, square):
        self.square =square
        return self.square

    def get_area_square(self):
        result =self.square*self.square
        return result

    def generate_random_range(self, random_range):
        result =rnd.random()* random_range
        return result

    def  set_square_root(self, square_root):
        self.square_root=square_root
        return self.square_root
        
    
    def set_square(self, square_number):
        self.square_number=square_number
        return self.square_root

    def  get_square_root(self):
         result =math.sqrt(self.square_root)
         return result
    
    def get_square(self):
        result =self.square_number*self.square_number
        return result

    def set_mean(self, mean):
        self.mean =mean
        return self.mean

    def get_mean(self):
        result = stc.mean(self.mean)
        return result

    def set_mode(self, mode):
        self.mode =mode
        return self.mode

    def get_mode(self):
        result = stc.mode(self.mode)
        return result


obj = Gbemisola_Math_General()
