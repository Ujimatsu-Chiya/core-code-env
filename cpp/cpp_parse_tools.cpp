#include "cpp_parse_tools.h"
#include <climits>
#include <deque>
#include <vector>

static TreeNode *des_tree_aux(std::vector<int> arr)
{
    int n = arr.size();
    if (n == 0 || arr[0] == INT_MIN)
    {
        return nullptr;
    }
    TreeNode **q = new TreeNode *[n];
    q[0] = new TreeNode(arr[0]);
    for (int ql = 0, qr = 1, p = 1; ql < qr; ql++)
    {
        if (p < n && arr[p] != INT_MIN)
        {
            q[qr++] = new TreeNode(arr[p]);
            q[ql]->left = q[qr - 1];
        }
        p++;
        if (p < n && arr[p] != INT_MIN)
        {
            q[qr++] = new TreeNode(arr[p]);
            q[ql]->right = q[qr - 1];
        }
        p++;
    }
    TreeNode *root = q[0];
    delete[] q;
    return root;
}

TreeNode *des_tree(const char *json_str)
{
    std::vector<int> arr = des_tree_list(json_str);
    return des_tree_aux(arr);
}

void delete_tree(TreeNode *root)
{
    if (root == nullptr)
    {
        return;
    }
    delete_tree(root->left);
    delete_tree(root->right);
    delete root;
}

static std::vector<int> ser_tree_aux(TreeNode *root)
{
    if (root == nullptr)
        return {};
    std::deque<TreeNode *> q{root};
    std::vector<int> result{root->val};
    while (!q.empty())
    {
        TreeNode *u = q.front();
        q.pop_front();
        if (u->left)
        {
            q.push_back(u->left);
            result.push_back(u->left->val);
        }
        else
        {
            result.push_back(INT_MIN);
        }
        if (u->right)
        {
            q.push_back(u->right);
            result.push_back(u->right->val);
        }
        else
        {
            result.push_back(INT_MIN);
        }
    }
    while (!result.empty() && result.back() == INT_MIN)
    {
        result.pop_back();
    }
    return result;
}

char *ser_tree(TreeNode *root)
{
    std::vector<int> result = ser_tree_aux(root);
    return ser_tree_list(result);
}

static ListNode *des_linked_list_aux(std::vector<int> arr)
{
    int n = arr.size();
    if (n == 0)
    {
        return nullptr;
    }
    ListNode *head = new ListNode(arr[0]);
    ListNode *tail = head;
    for (int i = 1; i < arr.size(); i++)
    {
        ListNode *p = new ListNode(arr[i]);
        tail->next = p;
        tail = p;
    }
    return head;
}

ListNode *des_linked_list(const char *json_str)
{
    std::vector<int> arr = des_int_list(json_str);
    return des_linked_list_aux(arr);
}

void delete_linked_list(ListNode *head)
{
    for (ListNode *p = head; p != nullptr;)
    {
        ListNode *q = p->next;
        delete p;
        p = q;
    }
}

static std::vector<int> ser_linked_list_aux(ListNode *head)
{
    std::vector<int> result;
    for (ListNode *p = head; p != nullptr; p = p->next)
    {
        result.push_back(p->val);
    }
    return result;
}

char *ser_linked_list(ListNode *head)
{
    std::vector<int> result = ser_linked_list_aux(head);
    return ser_int_list(result);
}

// g++ -shared -o libcpp_parse_tools.so -fPIC cpp_parse_tools.cpp cpp_parse_module.cpp ../rapidjson_helper.cpp 