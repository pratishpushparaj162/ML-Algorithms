// ConsoleApplication1.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>
using namespace std;
#define INF 9999
//struct Node{
//    int data;
//    struct Node* next = NULL;
//};

//struct Graph{
//    int V;
//    struct Node** adjlist;
//    Graph(int v)
//    {
//        V = v;
//        adjlist = new struct Node*[V];
//        for (int i = 0; i < V; i++)
//            adjlist[i] = NULL;
//    }
//};
struct Node{
    int dest;
    int wt;
    struct Node* next = NULL;
};

struct adjarray{
    int data;
    struct Node* head = NULL;
};

struct Graph
{
    int V;
    struct adjarray** ar;
    Graph(int v)
    {
        V = v;
        ar = new struct adjarray*[V];
        for (int i = 0; i < V; i++)
            ar[i] = NULL;
    }
};

struct queue{
    int front;
    int back;
    int* list;
    queue(int V)
    {
        front = -1;
        back = 0;
        list = new int[V];
    }
};

void enqueue(int data, struct queue* q)
{
    q->list[q->back++] = data;
    if (q->front == -1)
        q->front = 0;
}

int dequeue(struct queue* q)
{
    return q->list[q->front++];
}

bool isempty(struct queue* q)
{
    if (q->front == -1 || q->front == q->back)
        return 1;
    else
        return 0;
}

struct tupl{
    int value;
    int key;
};

struct priority_queue{
    int heapsize=0;
    struct tupl* heap;
    priority_queue(int s)
    {
        heapsize = s;
        heap = new struct tupl[heapsize];
    }
};

void push_q(struct priority_queue* pq, int data, int key)
{
    struct tupl* t = new tupl();
    t->value = data;
    t->key = key;
    pq->heap[pq->heapsize] = *t;
    int current = pq->heapsize;
    while (current > 0 && pq->heap[current].key < pq->heap[(current-1)/2].key)
    {
        swap(pq->heap[current], pq->heap[(current - 1) / 2]);
        current = (current - 1) / 2;
    }
    pq->heapsize++;
}

struct tupl pop_q(struct priority_queue* pq)
{
    struct tupl t = pq->heap[0];
    pq->heapsize--;
    pq->heap[0] = pq->heap[pq->heapsize];
    int current = 0;
    while (2 * current + 1 < pq->heapsize)
    {
        int child;
        if (current * 2 + 2 == pq->heapsize)
            child = current * 2 + 1;
        else
            child = pq->heap[current * 2 + 1].key < pq->heap[current * 2 + 2].key ? current * 2 + 1 : current * 2 + 2;
        if (pq->heap[current].key < pq->heap[child].key)
            break;
        swap(pq->heap[current], pq->heap[child]);
        current = child;
    }
    return t;
}

//void bfs(struct Graph* G, int start)
//{
//    int *visited = new int[G->V];
//    for (int i = 0; i < G->V; i++)
//        visited[i] = false;
//    struct queue* q = new queue(G->V);
//    enqueue(start, q);
//    visited[start] = true;
//    while (!isempty(q))
//    {
//        int temp = dequeue(q);
//        cout << temp << " ";
//        struct Node* t = G->adjlist[temp];
//        while (t)
//        {
//            if (!visited[t->data])
//            {
//                enqueue(t->data, q);
//                visited[t->data] = true;
//            }
//            t = t->next;
//        }
//    }
//}

struct stack{
    int top = -1;
    int *list;
    stack(int v)
    {
        list = new int[v];
    }
};

void push(struct stack* s, int data)
{
    s->top++;
    s->list[s->top] = data;
}

int pop(struct stack* s)
{
    return  s->list[s->top--];
}

//void dfs(struct Graph* G, int start)
//{
//    int *visited = new int[G->V];
//    for (int i = 0; i < G->V; i++)
//        visited[i] = false;
//    struct stack* s = new stack(G->V);
//    push(s, start);
//    visited[start] = true;
//    while (s->top != -1)
//    {
//        int temp = pop(s);
//        cout << temp << " ";
//        struct Node* t = G->adjlist[temp];
//        while (t)
//        {
//            if (!visited[t->data])
//            {
//                push(s, t->data);
//                visited[t->data] = true;
//            }
//            t = t->next;
//        }
//    }
//}

//void add_edge(struct Graph* G, int start, int en)
//{
//    struct Node* temp = new Node();
//    temp->data = en;
//    temp->next = G->adjlist[start];
//    G->adjlist[start] = temp;
//}

void add_edge(struct Graph* G, int start, int en, int wt)
{
    struct Node* temp = new Node();
    temp->dest = en;
    temp->wt = wt;
    temp->next = G->ar[start]->head;
    G->ar[start]->head = temp;
}

void prim(struct Graph* G, int start)
{
    struct priority_queue* pq = new priority_queue();
    push_q(pq, start, 0);
    for (int i = 0; i < G->V; i++)
        if (i != start)
            push_q(pq, i, INF);
    int weight = 0;
    while (pq->heapsize != 0)
    {
        struct tupl temp = pop_q(pq);
        weight += temp.key;
        struct Node* t = G->ar[temp.value]->head;
        while (t)
        {
            if (pq->heap[])
        }
    }
}

int _tmain(int argc, _TCHAR* argv[])
{
    int V;
    cin >> V;
    struct Graph* G = new Graph(V);
    int start, en, wt;
    for (int i = 0; i < V; i++)
    {
        cin >> start >> en >> wt;
        add_edge(G, start, en, wt);
    }
    prim(G, 0);
    /*bfs(G, 0);
    dfs(G, 0);*/
    return 0;
}
