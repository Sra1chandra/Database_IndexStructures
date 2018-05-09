import re
import sys
class Node(object):
    """docstring for Node."""
    def __init__(self,NodeCapacity):
        self.NodeCapacity = NodeCapacity;
        self.NodeData=[None]*self.NodeCapacity;
        self.OverflowBlock=None;

    def isNodeFull(self):
        if(self.NodeData[self.NodeCapacity-1]==None):
            return False;
        else:
            return True;

    def bisect(self,Data):
        i=0;
        while(i<self.NodeCapacity):
            if(self.NodeData[i]==None):
                self.NodeData[i]=Data;
                return True;
            if(self.NodeData[i]==Data):
                return False;
            i=i+1;
        if(self.OverflowBlock==None):
            self.OverflowBlock=Node(self.NodeCapacity);
            self.OverflowBlock.NodeData[0]=Data;
            return True;
        else:
            return self.OverflowBlock.bisect(Data);

class LinearHasing(object):
    """docstring for LinearHasing."""
    def __init__(self, NodeCapacity):
        self.NodeCapacity=NodeCapacity;
        self.HashTable=[Node(self.NodeCapacity),Node(self.NodeCapacity)];
        self.N=2;
        self.Next=0;
        self.Level=0;
        self.HashMod=2;
        self.HashTableLength=2;
        self.No_of_Records=0;


    def SwapElements(self,node,compare):
        Node1=Node(self.NodeCapacity)
        Node2=Node(self.NodeCapacity)
        i=0;
        data=node.NodeData[0]
        while(data!=None):
            # print data,compare,data&compare
            if(data&compare):
                Node2.bisect(data);
            else:
                Node1.bisect(data);

            i=i+1;
            if(i==node.NodeCapacity):
                i=0;
                if(node.OverflowBlock!=None):
                    node=node.OverflowBlock;
                else:
                    break;
            data=node.NodeData[i];

        return Node1,Node2

    def AddNode(self):
        if(self.Next==0):
            self.Level=self.Level+1;
            self.HashMod=self.HashMod*2;
            self.N *=2;
        Node1,Node2=self.SwapElements(self.HashTable[self.Next],self.HashMod/2);
        self.HashTable[self.Next]=Node1;
        self.HashTable.append(Node2);
        self.Next=(self.Next+1)%self.N;
        self.HashTableLength=self.HashTableLength+1;


    def InsertRecord(self,Value):
        HashValue=Value%self.HashMod;
        if(HashValue>=self.HashTableLength):
            HashValue=Value%(self.HashMod/2);

        # print self.HashMod
        if(self.HashTable[HashValue].bisect(Value)):
            print Value
        self.No_of_Records=self.No_of_Records+1;
        if((self.No_of_Records*1.0)/(self.HashTableLength*self.NodeCapacity)>=0.75):
            self.AddNode()

    def Traverse(self):
        for node in self.HashTable:
            while(1):
                print node.NodeData
                if(node.OverflowBlock!=None):
                    node=node.OverflowBlock;
                else:
                    break;
            print

if __name__ == '__main__':
    LINEARHASHING=LinearHasing(4);

    if len(sys.argv)==4:
        file_name=sys.argv[1];
    else:
        print 'Command Format python B+trees.py #file_name #M #B'
        sys.exit()
    f = open(file_name,"r") #opens file with name of "test.txt"
    for command in f:
            LINEARHASHING.InsertRecord(int(command));


    # while(1):
    #     command=raw_input();
    #     if(command=='traverse'):
    #         LINEARHASHING.Traverse();
    #         continue;
    #     LINEARHASHING.InsertRecord(int(command));
