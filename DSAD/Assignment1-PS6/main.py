import os
from csv import reader

class bookNode:
    def __init__(self, bkID=None, availCount=None):
        self.left = None
        self.right = None
        self.bookID = bkID
        self.avCntr = availCount
        self.chkOutCntr = 0    
    
    def _readBookList(self,bkID,availCount):
        if self.bookID:
            if bkID < self.bookID:
                if self.left is None:
                    self.left = bookNode(bkID,availCount)
                else:
                    self.left._readBookList(bkID,availCount)
            elif bkID > self.bookID:
                if self.right is None:
                    self.right = bookNode(bkID,availCount)
                else:
                    self.right._readBookList(bkID,availCount)
        else:
            self.bookID = bkID
            self.avCntr = availCount
    
    def _chkInChkOut(self,bkID,inOut):
        self.updateData(bkID,inOut,self)        
        
    def updateData(self,bkID,inOut,root):
        if root:
            if root.bookID==bkID:
                if inOut=='checkOut':
                    root.avCntr-=1
                    root.chkOutCntr+=1
                if inOut=='checkIn':
                    root.avCntr+=1
                return                
            self.updateData(bkID,inOut,root.left)            
            self.updateData(bkID,inOut,root.right)
        return
    
      
    def getAllData(self,root):
        res = []
        if root:
            res.append((root.bookID,root.chkOutCntr,root.avCntr))
            if root.left:
                res = res+self.getAllData(root.left)
            if root.right:
                res = res+self.getAllData(root.right)
        else:
            return
        return res
            
    def _getTopBooks(self):        
        lt = self.getAllData(self)
        lt.sort(key=lambda x:x[1],reverse=True)
        file = open(dir+'\outputPS6.txt','a')
        string = ''
        for i,x in enumerate(lt[:3]):
            string=string+'Top Books '+str(i+1)+': '+str(x[0])+', '+str(x[1])+'\n'  
        string = string +'\n'
        print(string)
        file.write(string)
        file.close()
    
    def printBooks(self):
        lt = self.getAllData(self)
        file = open(dir+'\outputPS6.txt','a')
        string = 'There are a total of '+str(len(lt))+' book titles in the library.\n'
        for i,x in enumerate(sorted(lt)):
            string = string + str(x[0])+', '+str(x[2])+'\n'
        string = string +'\n'
        print(string)
        file.write(string)
        file.close()
        
    def _findBook(self, bkID):
        string = self.searchInventory(bkID,self)
        if string=='':
            string = 'Book id '+str(bkID)+' does not exist.\n\n'
        print(string)
        file = open(dir+'\outputPS6.txt','a')
        file.write(string)
        file.close()            
        
        
    def searchInventory(self, bkID, root):
        string=''
        if root:
            if root.bookID==bkID:
                if root.avCntr>0:
                    string = 'Book id '+str(bkID)+' is available for checkout\n\n'
                elif root.avCntr==0:
                    string = 'All copies of book id '+str(bkID)+' have been checked out\n\n'
                return string               
            string = string + self.searchInventory(bkID,root.left)            
            string = string + self.searchInventory(bkID,root.right)
        return string
        
if __name__=='__main__':
    obj = bookNode()
    dir = os.path.dirname(__file__)
    if os.path.exists(dir+'\outputPS6.txt'):
        os.remove(dir+'\outputPS6.txt')
    with open(dir+'\inputPS6.txt', 'r') as read_obj:        
        csv_reader = reader(read_obj)
        for row in csv_reader:
            obj._readBookList(int(row[0].strip()),int(row[1].strip()))
            
    with open(dir+'\promptsPS6.txt', 'r') as read_obj:
        csv_reader = reader(read_obj)
        for row in csv_reader:
            #print(row)
            if len(row)>0:
                if ':' in row[0]:
                    if 'check' in row[0]:
                        inOut,bkID  = row[0].split(':')
                        obj._chkInChkOut(int(bkID.strip()),inOut)
                        continue
                    if 'find' in row[0]:
                        inOut,bkID  = row[0].split(':')
                        obj._findBook(int(bkID.strip()))
                if 'ListTopBooks' in row[0]:
                    obj._getTopBooks()
                    continue
                if 'printInventory' in row[0]:
                    obj.printBooks()
                    continue


# In[ ]:





# In[ ]:




