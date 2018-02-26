def a_function(data,list=[]):
    list.append(data)
    return list
class var():
    id=None
    name=None
    def __str__(self):
        return self.name
        

var1=var() 
var1.id=44
var1.name="Leon"

a=a_function(var1)
var1.id=23
var1.name="Jack"
b=a_function(var1)
print(b)

