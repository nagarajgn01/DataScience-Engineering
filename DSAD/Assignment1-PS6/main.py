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
def _readBookList(temp,bkID,availCount): 
    if not temp:
        root = bookNode(bkID,availCount)
        return
    q = []
    q.append(temp)

    # Do level order traversal until we find
    # an empty place.
    while (len(q)):
        temp = q[0]
        q.pop(0)

        if (not temp.left):
            temp.left = bookNode(bkID,availCount)
            break
        else:
            q.append(temp.left)

        if (not temp.right):
            temp.right = bookNode(bkID,availCount)
            break
        else:
            q.append(temp.right)


# Function to get list of books with preorder tree traversal
def getBookList(temp):
    res = []
    if temp: 
        res.append((temp.bookID,temp.chkOutCntr,temp.avCntr))
        res = res + getBookList(temp.left)    
        res = res + getBookList(temp.right)
    return res


# Function prints the list of book ids and 
# the available number of copies in the output file
def printBooks(temp):
    lt = getBookList(temp)
    string = 'There are a total of '+str(len(lt))+' book titles in the library.\n'
    for i,x in enumerate(sorted(lt)):
        string = string + str(x[0])+', '+str(x[2])+'\n'
    string = string +'\n'    
    file = open(dir+'\outputPS6.txt','a')
    file.write(string)
    file.close()

# function to delete the given deepest node (d_node) in binary tree
def deleteDeepest(root,d_node):
    q = []
    q.append(root)
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
  
# function to delete element in binary tree
def deletion(root, bkID):
    if root == None :
        return None
    if root.left == None and root.right == None:
        if root.bookID == bkID :
            return None
        else :
            return root
    key_node = None
    q = []
    q.append(root)
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
        deleteDeepest(root,temp)
        key_node.bookID = x
        key_node.avCntr = y
        key_node.chkOutCntr = z
    return root

# Function to traverse the tree in preorder
# and check if the given node exists in it
def _findBook(temp,bkID):
    if (temp == None):
        return '' 
    if (temp.bookID == bkID):
        if temp.avCntr>0:
            string = 'Book id '+str(bkID)+' is available for checkout\n\n'
        elif temp.avCntr==0:
            string = 'All copies of book id '+str(bkID)+' have been checked out\n\n'
        return string 
    """ then recur on left sutree """
    res1 = _findBook(temp.left, bkID)
    # node found, no need to look further
    if res1:
        return '' 
    """ node is not found in left,
    so recur on right subtree """
    res2 = _findBook(temp.right, bkID) 
    return res2

# Function to traverse the tree in preorder
# Function updates the check in / check out status of a book based on the book id. 
# bkID : bookID, inOut: either checkOut or checkIn
def _chkInChkOut(temp,bkID,inOut):
    if (temp == None):
        return False 
    if (temp.bookID == bkID):
        if inOut=='checkOut':
            temp.avCntr-=1
            temp.chkOutCntr+=1
        if inOut=='checkIn':
            temp.avCntr+=1
        return True 
    """ then recur on left sutree """
    res1 = _chkInChkOut(temp.left, bkID, inOut)
    # node found, no need to look further
    if res1:
        return True 
    """ node is not found in left,
    so recur on right subtree """
    res2 = _chkInChkOut(temp.right, bkID, inOut) 
    return res2

def _notIssued(temp):
    lt = getBookList(temp)
    lt = [x for x in lt if x[1]==0]
    string = 'List of books not issued:\n'
    for x in lt:
        string = string + str(x[0])+'\n'
        deletion(temp,x[0])
    string = string +'\n'
    file = open(dir+'\outputPS6.txt','a')
    file.write(string)
    file.close()   

# Function searches through the list of books and the checkout counter and 
# determines which are the top three books that have been checked out the most 
# and lists those books and the number of times they have been checked out 
def _getTopBooks(temp):
    lt = getBookList(temp)    
    if len(res)<1:
        print('No Books Available')
        return
    lt.sort(key=lambda x:x[1],reverse=True)    
    # Appending top three books to Output file
    file = open(dir+'\outputPS6.txt','a')
    string = ''
    for i,x in enumerate(lt[:3]):
        string=string+'Top Books '+str(i+1)+': '+str(x[0])+', '+str(x[1])+'\n'  
    string = string +'\n'
    file.write(string)
    file.close() 

# Driver code    
if __name__=='__main__':
    # Get current Directory to read input file
    dir = os.path.dirname(__file__)

    # Delete output file if already exists
    if os.path.exists(dir+'\outputPS6.txt'):
        os.remove(dir+'\outputPS6.txt')
    
    # With help of reader object, read each line of input file
    root = None
    with open(dir+'\inputPS6.txt', 'r') as read_obj:        
        csv_reader = reader(read_obj)
        for row in csv_reader:
            if root:
                _readBookList(root,int(row[0].strip()),int(row[1].strip()))
            else:
                root = bookNode(int(row[0].strip()),int(row[1].strip()))
    
    # Read Prompts file for execution
    with open(dir+'\promptsPS6.txt', 'r') as read_obj:
        csv_reader = reader(read_obj)
        for row in csv_reader:
            if len(row)>0:
                if ':' in row[0]:
                    # Check-In/Check-Out Transaction
                    if 'check' in row[0]:
                        inOut,bkID  = row[0].split(':')
                        _chkInChkOut(root,int(bkID.strip()),inOut)
                        continue
                    # Find Book Transaction
                    if 'find' in row[0]:
                        inOut,bkID  = row[0].split(':')
                        res = _findBook(root,int(bkID.strip()))
                        if res=='':
                            res = 'Book id '+str(bkID)+' does not exist.\n\n'
                        file = open(dir+'\outputPS6.txt','a')
                        file.write(res)
                        file.close()
                        continue
                # Get Top 3 books based on check-out
                if 'ListTopBooks' in row[0]:
                    _getTopBooks(root)
                    continue
                # Get all books in inventory sorted by bookID
                if 'printInventory' in row[0]:
                    printBooks(root)
                    continue
                # Check books which are not checked-Out and Delete/rearrange Tree
                if 'BooksNotIssued' in row[0]:
                    _notIssued(root)
                    continue
    
    
        
    
    
    