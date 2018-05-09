import re
import sys;
import math
class Node(object):
    """docstring for Node."""
    def __init__(self,NodeCapacity):
        self.NodeCapacity = NodeCapacity;
        self.NodeData=[None]*self.NodeCapacity;
        self.ChildPointers=[None]*(self.NodeCapacity+1);
        self.isLeafNode=True;
        self.isRootNode=False;

    def isNodeFull(self):
        if(self.NodeData[self.NodeCapacity-1]==None):
            return False;
        else:
            return True;

    def bisect(self,Data,ChildPointer):
        i=self.NodeCapacity-1;

        while(i>=0):
            if(self.NodeData[i]==None):
                i=i-1;
            else:
                break;
        # print 'fsafds' , i
        while(i>=0):
            if(self.NodeData[i]>Data):
                self.NodeData[i+1]=self.NodeData[i];
                if(not self.isLeafNode):
                    self.ChildPointers[i+2]=self.ChildPointers[i+1];
                i=i-1;
            else:
                break;
        self.NodeData[i+1]=Data;
        if(not self.isLeafNode):
            self.ChildPointers[i+2]=ChildPointer;

class BTree(object):
    """docstring for BTree."""
    def __init__(self,NodeCapacity):
        self.NodeCapacity=NodeCapacity;
        self.root=Node(self.NodeCapacity);
        self.root.isRootNode=True;
        self.splitNode=[None,None,None];


    def InsertRecord(self,Value):
        # print self.root
        self.Insert(self.root,Value)
        if(self.splitNode[0]!=None):
            if(self.splitNode[0].isLeafNode):
                data,left,right=self.splitLeafNode(self.splitNode[0],self.splitNode[1]);
            else:
                data,left,right=self.splitNonLeafNode(self.splitNode[0],self.splitNode[1],self.splitNode[2]);

            self.splitNode=[None,None,None];
            self.root=Node(self.NodeCapacity);
            self.root.NodeData[0]=data;
            self.root.ChildPointers[0]=left;
            self.root.ChildPointers[1]=right;
            self.root.isLeafNode=False;

    def Insert(self,node,Value):
        # print node
        if(node.isLeafNode):
            if(not node.isNodeFull()):
                node.bisect(Value,None);
            else:
                self.splitNode[0]=node;
                self.splitNode[1]=Value;
                return;
        else:
            i=0;
            while(i<self.NodeCapacity and node.NodeData[i]!=None):
                if(node.NodeData[i]<Value):
                    i=i+1;
                else:
                    break;
            # if(i<self.NodeCapacity and node.NodeData[i]==None):
            #     i=i-1;
            # print 'sraca',i,self.NodeCapacity,node.NodeData,node.ChildPointers
            self.Insert(node.ChildPointers[i],Value);

        if(self.splitNode[0]!=None):
            if(self.splitNode[0].isLeafNode):
                data,left,right=self.splitLeafNode(self.splitNode[0],self.splitNode[1]);
                # print 'sldnsfjnkjfsan',data,left,right
            else:
                data,left,right=self.splitNonLeafNode(self.splitNode[0],self.splitNode[1],self.splitNode[2]);

            self.splitNode=[None,None,None];
            if(not node.isNodeFull()):
                node.bisect(data,right);
                return ;
            else:
                self.splitNode[0]=node;
                self.splitNode[1]=data;
                self.splitNode[2]=right;
                return ;


    def splitLeafNode(self,Left,Value):
        Right=Node(self.NodeCapacity);
        No_of_Records=len(Left.NodeData);
        i=(No_of_Records//2);
        while(i<No_of_Records):
            Right.NodeData[i-(No_of_Records//2)]=Left.NodeData[i];
            Left.NodeData[i]=None;
            i=i+1;
        if(Value<Right.NodeData[0]):
            Left.bisect(Value,None);
        else:
            Right.bisect(Value,None);
        Right.ChildPointers[self.NodeCapacity]=Left.ChildPointers[self.NodeCapacity];
        Left.ChildPointers[self.NodeCapacity]=Right;
        # print 'split Leaf ',Left.NodeData,Left.ChildPointers,Right.NodeData,Right.ChildPointers
        return Right.NodeData[0],Left,Right

    def splitNonLeafNode(self,temp,Value,ChildPointer):
        Left=temp;
        Right=Node(self.NodeCapacity);
        Right.isLeafNode=False;
        No_of_Records=len(Left.NodeData);
        i=(No_of_Records//2);
        return_data=Left.NodeData[i];
        Left.NodeData[i]=None;
        Right.ChildPointers[0]=Left.ChildPointers[i+1];
        Left.ChildPointers[i+1]=None;
        # Left.ChildPointers[i]=None;
        i=i+1;
        while(i<No_of_Records):
            # print i
            # if(Value == 196000):
                # print Left.NodeData,Left.ChildPointers
                # print Left.NodeData,Left.ChildPointers

            Right.NodeData[i-(No_of_Records//2)-1]=Left.NodeData[i];
            Right.ChildPointers[i-(No_of_Records//2)]=Left.ChildPointers[i+1];
            Left.NodeData[i]=None;
            Left.ChildPointers[i+1]=None;
            i=i+1;
        # Right.ChildPointers[i-(No_of_Records//2)]
        if(ChildPointer==None):
            sys.exit()
        if(Value<Right.NodeData[0]):
            Left.bisect(Value,ChildPointer);
        else:
            Right.bisect(Value,ChildPointer);

        # if(Left == None or Right == None):
        #     sys.exit();
        # if(return_data=196000):
        #     print 'Debug',Left,Right

        return return_data,Left,Right

    def FindRecord(self,node,Value):
        # print node.NodeData,node.isLeafNode
        i=0;
        recordFound=False
        while(i<self.NodeCapacity and node.NodeData[i]!=None):
            if(node.NodeData[i]<Value):
                i=i+1;
            else:
                if(node.NodeData[i]==Value):
                    recordFound=True
                break;
        if(recordFound):
            return True;
        elif(node.isLeafNode and not recordFound):
            return False;
        else:
            return self.FindRecord(node.ChildPointers[i],Value);

    def FindRange(self,node,Value1,Value2):
        # print Value1,Value2
        # print node.NodeData,node.isLeafNode
        count=0;
        i=0;
        recordFound=False
        while(i<self.NodeCapacity and node.NodeData[i]!=None):
            if(node.NodeData[i]<Value1):
                i=i+1;
            else:
                break;
        if(i==self.NodeCapacity):
            return 0;
        if(node.isLeafNode):
            while(1):
                # i=i%self.NodeCapacity
                if(node==None):
                    break;
                if node.NodeData[i]>Value2:
                    break;
                if(node.NodeData[i]!=None):
                    count+=1;
                # print node.NodeData[i];
                i=i+1
                if(i==self.NodeCapacity):
                    node=node.ChildPointers[i];
                    i=0;
            return count;
        else:
            return self.FindRange(node.ChildPointers[i],Value1,Value2);

    def Traverse(self,node):
        # if( not node.isLeafNode):
        #     print node.NodeData,sum(x is None for x in node.NodeData),sum(x is  None for x in node.ChildPointers)
            # if(sum(x is None for x in node.NodeData)!=sum(x is  None for x in node.ChildPointers)):
            #     sys.exit();
        i=0;
        # print(node.NodeData,node.ChildPointers);
        while(i<=self.NodeCapacity):
            if(node.ChildPointers[i]!=None):
                self.Traverse(node.ChildPointers[i]);
            else:
                break;
            i=i+1;

if __name__ == '__main__':
    find_command=re.compile('^find$', re.IGNORECASE);
    insert_command=re.compile('^insert$', re.IGNORECASE);
    count_command=re.compile('^count$', re.IGNORECASE);
    range_command=re.compile('^range$', re.IGNORECASE);

    if len(sys.argv)==4:
        file_name=sys.argv[1];
    else:
        print 'Command Format python B+trees.py #file_name #M #B'
        sys.exit()
    # print int(math.floor(int(sys.argv[3])/4))
    BTREE=BTree(int(math.floor(int(sys.argv[3])/4)));
    f = open(file_name,"r") #opens file with name of "test.txt"
    for command in f:
        # print command
    #     myList.append(line)
        # print command
    # while(1):
        # command=raw_input();
        parse=command.split();
        if(len(parse)<=1):
            continue;

        isFindCommand=find_command.search(parse[0]);
        if(isFindCommand and len(parse)==2):
            if(BTREE.FindRecord(BTREE.root,int(parse[1]))):
                print "YES";
            else:
                print "NO"
            continue;

        isRangeCommand=range_command.search(parse[0]);
        if(isRangeCommand and len(parse)==3):
            print BTREE.FindRange(BTREE.root,int(parse[1]),int(parse[2]));
            continue;

        isInsertCommand=insert_command.search(parse[0]);
        if(isInsertCommand and len(parse)==2):
            # if(int(parse[1])==196000):
            # BTREE.Traverse(BTREE.root)
            BTREE.InsertRecord(int(parse[1]))
            # if(int(parse[1])==7000):
            #     BTREE.Traverse(BTREE.root);
            #     sys.exit()


        isCountCommand=count_command.search(parse[0]);
        if(isCountCommand and len(parse)==2):
            print BTREE.FindRange(BTREE.root,int(parse[1]),int(parse[1]));
