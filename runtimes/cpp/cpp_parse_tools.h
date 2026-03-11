#ifndef CPP_PARSE_TOOLS_H
#define CPP_PARSE_TOOLS_H

#include "cpp_node_type.h"
#include "cpp_parse_module.h"

// Tree conversion helpers (JSON <-> TreeNode).
TreeNode *des_tree(const std::string &json_str);
std::string ser_tree(TreeNode *root);
void delete_tree(TreeNode *root);

// Linked-list conversion helpers (JSON <-> ListNode).
ListNode *des_linked_list(const std::string &json_str);
std::string ser_linked_list(ListNode *head);
void delete_linked_list(ListNode *head);

#endif // CPP_PARSE_TOOLS_H
