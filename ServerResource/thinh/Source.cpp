#include"Header.h"
Node* createNode(int key) {
	Node* p = new Node;
	p->data = key;
	p->next = NULL;
	return p;
}
void readFile(LinkedList& l, string file_name) {
    fstream Read;
    Read.open(file_name, ios::in);
    int i;
    while (Read >> i) {
        Node* p = createNode(i);
        addTail(l, p);
    }
    Read.close();
}
void writeFile(LinkedList l, string file_name) {
    fstream Write;
    Write.open(file_name, ios::out);
    Node* temp = l.head;
    while (temp != NULL) {
        Write << temp->data << " ";
        temp = temp->next;
    }
}
void createLinkedList(LinkedList& l) {
	l.head = NULL;
	l.tail = NULL;
}
bool isEmpty(LinkedList l) {
	if (l.head == NULL)
		return true;
	return false;
}
void AddHead(LinkedList& l, Node* p) {
    if (l.head == NULL) {
        
        l.head = p;
        l.tail = p;
    }
    else {
        p->next = l.head;
        l.head = p;
    }
}
void addTail(LinkedList& l, Node* p) {
    if (l.head == NULL) {
        l.head = p;
        l.tail = p;
    }
    else {
        l.tail->next = p;
        l.tail = p;
    }
}
void addAfter(LinkedList& l, Node* prev, Node* p) {
    if (prev != NULL)
    {
        p->next = prev->next;
        prev->next = p;
        if (prev == l.tail)
            l.tail = p;

    }
    else
    {
        AddHead(l, p);
    }
}
void removeHead(LinkedList& l) {
    Node* p = new Node;
    p = l.head;
    l.head = l.head->next;
    delete p;
}
void removeTail(LinkedList& l){
    for (Node* k = l.head; k != NULL; k = k->next)
    {
        if (k->next == l.tail)
        {
            delete l.tail;
            k->next = NULL;
            l.tail = k;
        }
    }
}
//Assignment 1
void removeALLX(LinkedList& l, int key) {
    while (l.head && l.head->data == key)
        l.head = l.head->next;
    Node* curr = l.head, * prev = nullptr;
    while (curr) {
        if (curr->data == key)
            prev->next = curr->next;
        else
            prev = curr;
        curr = curr->next;
    }
}
//Assignment 2
void removeDuplicate(LinkedList& l) {
    Node* p, * k, * dup;
    p = l.head;

    while (!p && p->next != NULL) {
        k = p;
        while (k->next != NULL) {
            if (p->data == k->next->data) {
                dup = k->next;
                k->next = k->next->next;
                delete (dup);
            }
            else
                k = k->next;
        }
        p = p->next;
    }
}
//Assignment 3
void reverseLinkedList(LinkedList& l) {
    Node* cur, * temp, * prev;
    cur = l.head;
    temp = NULL;
    prev = NULL;
    while (cur!=NULL) {
        temp = cur->next;
        cur->next = prev;
        prev = cur;
        cur = temp;
    }
    l.head = prev;
}
//Assignment 4
void insertEven(LinkedList& l) {
    Node* cur, *prev;
    int i = 2;
    cur = prev =l.head;
    for (cur=l.head; cur != NULL; cur = cur->next) {
        if (cur == l.head) {
            Node* p = createNode(i);
            AddHead(l, p);
            i += 2;
        }
        else {
            Node* p = createNode(i);
            p->next = prev->next;
            prev->next = p;
            prev = prev->next->next;
            i += 2;
        }
    }
}
//Assignment 5
void sortLinkedList(LinkedList& l, Node* p) {
    Node* temp, * prev;
    temp = l.head;
    prev = NULL;
    if (p->data < temp->data)
        AddHead(l, p);
    else {
        while (temp != NULL && (temp->data < p->data)) {
            prev = temp;
            temp = temp->next;
        }
        addAfter(l, prev, p);
    }
}
//Assignment 6
LinkedList sumLinkedList(LinkedList l) {
    Node* temp = l.head;
    LinkedList sum;
    createLinkedList(sum);
    int i = 0;
    while (temp != NULL) {
        i = i + temp->data;
        Node* q = createNode(i);
        addTail(sum, q);
        temp = temp->next;
    }
    return sum;
}
//Assignment 7
void moveNode(Node*& a, Node*& b){
    if (b == NULL || a == NULL)
        return;
    if (a->next != NULL)
        a->next = a->next->next;
    if (b->next != NULL)
        b->next = b->next->next;
    moveNode(a->next, b->next);
}
void splitLinkedList(LinkedList l,LinkedList &q,LinkedList &k) {
    Node* curr = l.head;
    q.head = curr;
    k.head = curr->next;
    moveNode(q.head, k.head);
}
//Assignment 8
int lenght(LinkedList l) {
    Node* temp = l.head;
    int count = 0;
    while (temp != NULL) {
        count++;
        temp = temp->next;
    }
    return count;
}
void mergeLinkedList(LinkedList& l, LinkedList q, LinkedList k) {
    int len = lenght(q) + lenght(k);
    Node* temp1 = q.head;
    Node* temp2 = k.head;
    for (int i = 0; i <= len; i++) {
        if (i % 2 == 0&&temp1!=NULL) {
            addTail(l, temp1);
            temp1 = temp1->next;
        }
        else if(temp2!=NULL) {
            addTail(l, temp2);
            temp2 = temp2->next;
        }
    }
}
//Assignment 9
void joinLinkedList(Node*&a,Node*&b) {
    if (a != NULL && b != NULL)
    {
        if (a->next == NULL)
            a->next = b;
        else
            joinLinkedList(a->next, b);
    }
}
//Assignment 10
int LinkedListNum(LinkedList l) {
    int num = 0;
    int len = lenght(l)-1;
    Node* temp = l.head;
    while (temp != NULL) {
        num = num + temp->data * pow(10, len);
        len = len - 1;
        temp = temp->next;
    }
    return num;
}
//Assignment 11
void numLinkedList(LinkedList& l, int num) {
    Node* temp = l.head;
    int tmp = 0;
    while (num != 0) {
        tmp = num % 10;
        num = num / 10;
        Node* p = createNode(tmp);
        AddHead(l, p);
    }
}
//Assignment 12
Node* shareNode(LinkedList l, LinkedList q){
    while (q.head) {
        Node* temp = l.head;
        while (temp) {
            if (temp == q.head)
                return q.head;
            temp = temp->next;
        }
        q.head = q.head->next;
    }
    return NULL;
}
//Assignment 13
bool loopLinkedList(Node*LinkedList){
    Node* slow_p = LinkedList, * fast_p = LinkedList;

    while (slow_p && fast_p && fast_p->next) {
        slow_p = slow_p->next;
        fast_p = fast_p->next->next;
        if (slow_p == fast_p) {
            return true;
        }
    }
    return false;
}
void printLinkedList(LinkedList l) {
    Node* temp = l.head;
    while (temp != NULL) {
        cout << temp->data << " ";
        temp = temp->next;
    }
}