#include "c_parse_tools.h"
#include <limits.h>
#include <stdlib.h>

static struct TreeNode* des_tree_aux(int* arr, int n) {
    if (n == 0 || arr[0] == INT_MIN) {
        return NULL;
    }
    struct TreeNode **q = (struct TreeNode**)malloc(n * sizeof(struct TreeNode*));
    q[0] = (struct TreeNode*)malloc(sizeof(struct TreeNode));
    q[0]->val = arr[0];
    q[0]->left = q[0]->right = NULL;

    int ql = 0, qr = 1, p = 1;
    while (ql < qr) {
        if (p < n && arr[p] != INT_MIN) {
            q[qr] = (struct TreeNode*)malloc(sizeof(struct TreeNode));
            q[qr]->val = arr[p];
            q[qr]->left = q[qr]->right = NULL;
            q[ql]->left = q[qr];
            qr++;
        }
        p++;
        if (p < n && arr[p] != INT_MIN) {
            q[qr] = (struct TreeNode*)malloc(sizeof(struct TreeNode));
            q[qr]->val = arr[p];
            q[qr]->left = q[qr]->right = NULL;
            q[ql]->right = q[qr];
            qr++;
        }
        p++;
        ql++;
    }
    struct TreeNode *root = q[0];
    free(q);
    return root;
}

struct TreeNode* des_tree(char* json_str) {
    size_t n;
    int* arr = des_tree_list(json_str, &n);
    return des_tree_aux(arr, n);
}

void delete_tree(struct TreeNode* root) {
    if (root == NULL) {
        return;
    }
    delete_tree(root->left);
    delete_tree(root->right);
    free(root);
}

static int count_tree_nodes(struct TreeNode *root) {
    if (root == NULL) {
        return 0;
    }
    return 1 + count_tree_nodes(root->left) + count_tree_nodes(root->right);
}

static int* ser_tree_aux(struct TreeNode* root, int* result, int* size) {
    if (root == NULL) {
        return result;
    }
    result[*size] = root->val;
    (*size)++;

    if (root->left) {
        result = ser_tree_aux(root->left, result, size);
    } else {
        result[*size] = INT_MIN;
        (*size)++;
    }
    
    if (root->right) {
        result = ser_tree_aux(root->right, result, size);
    } else {
        result[*size] = INT_MIN;
        (*size)++;
    }

    return result;
}

char* ser_tree(struct TreeNode* root) {
    int size = 0;
    int cnt = count_tree_nodes(root);
    int* result = (int*)malloc((2 * cnt + 2) * sizeof(int));
    result = ser_tree_aux(root, result, &size);
    char* json_str = ser_tree_list(result, size);
    free(result);
    return json_str;
}

static struct ListNode* des_linked_list_aux(int* arr, int n) {
    if (n == 0) {
        return NULL;
    }

    struct ListNode* head = (struct ListNode*)malloc(sizeof(struct ListNode));
    head->val = arr[0];
    head->next = NULL;
    struct ListNode* tail = head;

    for (int i = 1; i < n; i++) {
        struct ListNode* p = (struct ListNode*)malloc(sizeof(struct ListNode));
        p->val = arr[i];
        p->next = NULL;
        tail->next = p;
        tail = p;
    }

    return head;
}

struct ListNode* des_linked_list(char* json_str) {
    size_t n;
    int* arr = des_int_list(json_str, &n);
    return des_linked_list_aux(arr, n);
}

void delete_linked_list(struct ListNode* head) {
    while (head != NULL) {
        struct ListNode* temp = head;
        head = head->next;
        free(temp);
    }
}

static int count_linked_list_nodes(struct ListNode *head) {
    int count = 0;
    struct ListNode *current = head;
    while (current != NULL) {
        count++;
        current = current->next;
    }
    return count;
}

static int* ser_linked_list_aux(struct ListNode* head, int* result, int* size) {
    struct ListNode* p = head;
    while (p != NULL) {
        result[*size] = p->val;
        (*size)++;
        p = p->next;
    }
    return result;
}

char* ser_linked_list(struct ListNode* head) {
    int size = 0;
    int cnt = count_linked_list_nodes(head);
    int* result = (int*)malloc(cnt * sizeof(int));
    result = ser_linked_list_aux(head, result, &size);
    
    char* json_str = ser_int_list(result, size);
    
    free(result);
    return json_str;
}

