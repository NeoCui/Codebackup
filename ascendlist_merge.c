#include <stdio.h>
#include <stdlib.h>
#include <malloc.h>

// List structure definition
typedef struct _listnode{
    int val;
    struct _listnode* next;
}ListNode;

// List create
ListNode* ascendlist_Create(){
    int len, val;
    ListNode* p = (ListNode*)malloc(sizeof(ListNode));
    p->val = 0;
    p->next = NULL;
    ListNode* ret = p;

    printf("Please input list length: ");
    scanf("%d", &len);
    
    if(len>0){
        while(len--){
            ListNode* tmp = (ListNode*)malloc(sizeof(ListNode));
	    printf("Please input the list node value: ");
	    scanf("%d", &val);
	    tmp->val = val;
	    tmp->next = NULL;
	    p->next = tmp;
	    p = p->next;
	}
	return ret->next;
    }else{
	printf("List length should be bigger than 0.\n");
	return NULL;
    }
}

// List merge
ListNode* ascendlist_Merge(ListNode* l1, ListNode* l2){
    if(l1==NULL || l2==NULL)
	return l1 ? l1:l2;

    ListNode* p = (ListNode*)malloc(sizeof(ListNode));
    p->val = 0;
    p->next = NULL;
    ListNode* ret = p;

    while(l1 && l2){
	if(l1->val < l2->val){
	    p->next = l1;
	    p = l1;
	    l1 = l1->next;
	}else{
	    p->next = l2;
	    p = l2;
	    l2 = l2->next;
	}
    }

    p->next = l1 ? l1:l2;
    return ret->next;
}

// Print list
static int ascendlist_Print(ListNode* list){
    if(!list){
	printf("%s failed! List is null!\n", __func__);
	return -1;
    }
    printf("List information: ");
    while(list){
	printf("%d->", list->val);
	list = list->next;
    }
    printf("End\n");
    return 0;
}

// main function
int main()
{
    ListNode* l1 = ascendlist_Create();
    ascendlist_Print(l1);
    ListNode* l2 = ascendlist_Create();
    ascendlist_Print(l2);

    printf("Merged result:\n");
    ListNode* ret = ascendlist_Merge(l1, l2);
    ascendlist_Print(ret);

    return 0;
}
