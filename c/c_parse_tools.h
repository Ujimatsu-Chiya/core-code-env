#ifndef C_PARSE_TOOLS_H
#define C_PARSE_TOOLS_H

#include "c_node_type.h"
#include "c_parse_module.h"

#ifdef __cplusplus
extern "C" {
#endif


struct TreeNode* des_tree(const char* json_str);
char *ser_tree(struct TreeNode *root);
struct ListNode *des_linked_list(const char *json_str);
char *ser_linked_list(struct ListNode *head);

#ifdef __cplusplus
}
#endif

#endif // C_PARSE_TOOLS_H