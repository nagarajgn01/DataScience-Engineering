import os
from csv import reader
import time

class bookNode:
    # The basic structure of the book node in Binary Tree
    def __init__(self,bkID=None,availCount=None):
        self.left = None
        self.right = None
        self.bookID = bkID
        self.avCntr = availCount
        self.chkOutCntr = 0    
    
    # This function reads the book ids and the number of copies available from the inputPS6.txt file placed in current directory
    # bkID : bookID, availCount: Count of books available 
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
            # Root Node
            self.bookID = bkID
            self.avCntr = availCount
    

    # Function updates the check in / check out status of a book based on the book id. 
    # bkID : bookID, inOut: either checkOut or checkIn
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

    # Function to get list of books with Inorder tree traversal
    def getBookList(self,bkNode):
        res = []
        if bkNode:
            res = self.getBookList(bkNode.left)
            res.append((bkNode.bookID,bkNode.chkOutCntr,bkNode.avCntr))            
            res = res + self.getBookList(bkNode.right)
        return res

    # Function searches through the list of books and the checkout counter and determines which are the top three books that have been checked out the most and lists those books and the number of times they have been checked out 
    def _getTopBooks(self,bkNode):
        res = self.getBookList(bkNode)
        res.sort(key=lambda x:x[1],reverse=True)
        # Appending top three books to Output file
        file = open(dir+'\outputPS6.txt','a')
        string = ''
        for i,x in enumerate(res[:3]):
            string=string+'Top Books '+str(i+1)+': '+str(x[0])+', '+str(x[1])+'\n'  
        string = string +'\n'
        file.write(string)
        file.close()

    # Trigger recursive from binnary tree root node  
    def searchInventory(self,eNode,bkID):
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

    # Get the book id that needs to be searched for availability in the system
    def _findBook(self,eNode,bkID):
        string = self.searchInventory(eNode, bkID)
        if string=='':
            string = 'Book id '+str(bkID)+' does not exist.\n\n'
        file = open(dir+'\outputPS6.txt','a')
        file.write(string)
        file.close()     

    #function prints the list of book ids and the available number of copies in the output file
    def printBooks(self,bkNode):
        lt = self.getBookList(bkNode)
        file = open(dir+'\outputPS6.txt','a')
        string = 'There are a total of '+str(len(lt))+' book titles in the library.\n'
        for i,x in enumerate(sorted(lt)):
            string = string + str(x[0])+', '+str(x[2])+'\n'
        string = string +'\n'
        file.write(string)
        file.close()

    # Triggers function to delete node in binary tree
    def removeNode(self,bkID):
        if self == None :
            return None
        if self.left == None and self.right == None:
            if self.key == bkID:
                return None
            else:
                return self
        key_node = None
        q = []
        q.append(self)
        while(len(q)):
            temp = q.pop(0)
            if temp.bookID == bkID:
                key_node = temp
            if temp.left:
                q.append(temp.left)
            if temp.right:
                q.append(temp.right)

        if key_node :
            x,y,z = temp.bookID,temp.avCntr,temp.chkOutCntr
            self.deleteDeepest(temp)
            key_node.bookID = x
            key_node.avCntr = y
            key_node.chkOutCntr = z

        return self

    # function to delete the given deepest node (d_node) in binary tree
    def deleteDeepest(self,d_node):
        q = []
        q.append(self)
        while(len(q)):
            temp = q.pop(0)
            if temp is d_node:
                temp = None
                return
            if temp.right:
                if temp.right is d_node:
                    temp.right = None
                    return
                else:
                    q.append(temp.right)
            if temp.left:
                if temp.left is d_node:
                    temp.left = None
                    return
                else:
                    q.append(temp.left)

    def _notIssued(self,bkNode):
        lt = self.getBookList(bkNode)
        lt = [x for x in lt if x[1]==0]
        string = 'List of books not issued:\n'
        for x in lt:
            string = string + str(x[0])+'\n'
            self.removeNode(x[0])
        string = string +'\n'
        file = open(dir+'\outputPS6.txt','a')
        file.write(string)
        file.close()

# Driver code    
if __name__=='__main__':
    obj = bookNode()
    # Get current Directory to read input file
    dir = os.path.dirname(__file__)

    # Delete output file if already exists
    if os.path.exists(dir+'\outputPS6.txt'):
        os.remove(dir+'\outputPS6.txt')
    
    # With help of reader object, read each line of input file
    with open(dir+'\inputPS6.txt', 'r') as read_obj:        
        csv_reader = reader(read_obj)
        for row in csv_reader:
            obj._readBookList(int(row[0].strip()),int(row[1].strip()))

    # Start timer to calculate processing time
    start = time.time()        

    # Read Prompts file for execution
    with open(dir+'\promptsPS6.txt', 'r') as read_obj:
        csv_reader = reader(read_obj)
        for row in csv_reader:
            if len(row)>0:
                if ':' in row[0]:
                    if 'check' in row[0]:
                        inOut,bkID  = row[0].split(':')
                        obj._chkInChkOut(int(bkID.strip()),inOut)
                        continue
                    if 'find' in row[0]:
                        inOut,bkID  = row[0].split(':')
                        obj._findBook(obj,int(bkID.strip()))
                        continue
                if 'ListTopBooks' in row[0]:
                    obj._getTopBooks(obj)
                    continue
                if 'printInventory' in row[0]:
                    obj.printBooks(obj)
                    continue
                if 'BooksNotIssued' in row[0]:
                    obj._notIssued(obj)
                    continue
    
    # Print processing time to execute all prompts
    print(f"Runtime of the program is {round(time.time() - start,5)} sec")