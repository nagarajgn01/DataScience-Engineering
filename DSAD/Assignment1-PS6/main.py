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
        if self.bookID:
            if self.bookID==bkID:
                if inOut=='checkOut':
                    self.avCntr-=1
                    self.chkOutCntr+=1
                if inOut=='checkIn':
                    self.avCntr+=1
            elif bkID<self.bookID:
                if self.left is not None:
                    self.left._chkInChkOut(bkID,inOut)
            else:
                if self.right is not None:
                    self.right._chkInChkOut(bkID,inOut)    

    def getBookList(self,bkNode):
        res = []
        if bkNode:
            res = self.getBookList(bkNode.left)
            res.append((bkNode.bookID,bkNode.chkOutCntr,bkNode.avCntr))            
            res = res + self.getBookList(bkNode.right)
        return res

    def _getTopBooks(self,bkNode):
        res = self.getBookList(bkNode)
        res.sort(key=lambda x:x[1],reverse=True)
        file = open(dir+'\outputPS6.txt','a')
        string = ''
        for i,x in enumerate(res[:3]):
            string=string+'Top Books '+str(i+1)+': '+str(x[0])+', '+str(x[1])+'\n'  
        string = string +'\n'
        file.write(string)
        file.close()
        
    def searchInventory(self,eNode, bkID):
        string=''
        if eNode.bookID:
            if eNode.bookID==bkID:
                if eNode.avCntr>0:
                    string = 'Book id '+str(bkID)+' is available for checkout\n\n'
                elif eNode.avCntr==0:
                    string = 'All copies of book id '+str(bkID)+' have been checked out\n\n'
                return string
            elif bkID<eNode.bookID:  
                if eNode.left is not None:
                    string = string + self.searchInventory(eNode.left,bkID) 
            else:           
                if eNode.right is not None: 
                    string = string + self.searchInventory(eNode.right,bkID)
        return string   

    def _findBook(self, eNode, bkID):
        string = self.searchInventory(eNode, bkID)
        if string=='':
            string = 'Book id '+str(bkID)+' does not exist.\n\n'
        file = open(dir+'\outputPS6.txt','a')
        file.write(string)
        file.close()     

    def printBooks(self,bkNode):
        lt = self.getBookList(bkNode)
        file = open(dir+'\outputPS6.txt','a')
        string = 'There are a total of '+str(len(lt))+' book titles in the library.\n'
        for i,x in enumerate(lt):
            string = string + str(x[0])+', '+str(x[2])+'\n'
        string = string +'\n'
        file.write(string)
        file.close()       

        
if __name__=='__main__':
    obj = bookNode()
    dir = os.path.dirname(__file__)
    if os.path.exists(dir+'\outputPS6.txt'):
        os.remove(dir+'\outputPS6.txt')
    with open(dir+'\inputPS6.txt', 'r') as read_obj:        
        csv_reader = reader(read_obj)
        for row in csv_reader:
            obj._readBookList(int(row[0].strip()),int(row[1].strip()))
            
    with open(dir+'\promptsPS6_test.txt', 'r') as read_obj:
        csv_reader = reader(read_obj)
        for row in csv_reader:
            if len(row)>0:
                #print(row)
                if ':' in row[0]:
                    if 'check' in row[0]:
                        inOut,bkID  = row[0].split(':')
                        obj._chkInChkOut(int(bkID.strip()),inOut)
                        continue
                    if 'find' in row[0]:
                        inOut,bkID  = row[0].split(':')
                        obj._findBook(obj,int(bkID.strip()))
                if 'ListTopBooks' in row[0]:
                    obj._getTopBooks(obj)
                    continue
                if 'printInventory' in row[0]:
                    obj.printBooks(obj)
                    continue