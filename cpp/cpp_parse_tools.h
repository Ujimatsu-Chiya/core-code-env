#ifndef CPP_PARSE_TOOLS_H
#define CPP_PARSE_TOOLS_H

#include "cpp_node_type.h"
#include "cpp_parse_module.h"

TreeNode *des_tree(char *json_str);
char *ser_tree(TreeNode *root);
void delete_tree(TreeNode *root);
ListNode *des_linked_list(const char *json_str);
char *ser_linked_list(ListNode *head);
void delete_linked_list(ListNode *head);

#endif // CPP_PARSE_TOOLS_H