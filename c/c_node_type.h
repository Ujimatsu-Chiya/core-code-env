#ifndef C_NODE_TYPE_H
#define C_NODE_TYPE_H

struct TreeNode {
    int val;
    struct TreeNode *left;
    struct TreeNode *right;
};

struct ListNode {
    int val;
    struct ListNode *next;
};

#endif // C_NODE_TYPE_H