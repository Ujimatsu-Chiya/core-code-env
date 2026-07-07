"""Language-specific commented node definitions for generated templates."""

from typing import Iterable

from code_gen.utils import ClassDef, MethodDef, TypeEnum


NODE_COMMENT_TEMPLATES = {
    "c": {
        TypeEnum.LISTNODE: "\n".join(
            [
                "/*",
                " * Definition for singly-linked list.",
                " * struct ListNode {",
                " *     int val;",
                " *     struct ListNode *next;",
                " * };",
                " */",
            ]
        ),
        TypeEnum.TREENODE: "\n".join(
            [
                "/*",
                " * Definition for a binary tree node.",
                " * struct TreeNode {",
                " *     int val;",
                " *     struct TreeNode *left;",
                " *     struct TreeNode *right;",
                " * };",
                " */",
            ]
        ),
    },
    "cpp": {
        TypeEnum.LISTNODE: "\n".join(
            [
                "// Definition for singly-linked list.",
                "// struct ListNode {",
                "//     int val;",
                "//     ListNode *next;",
                "//     ListNode() : val(0), next(nullptr) {}",
                "//     ListNode(int x) : val(x), next(nullptr) {}",
                "// };",
            ]
        ),
        TypeEnum.TREENODE: "\n".join(
            [
                "// Definition for a binary tree node.",
                "// struct TreeNode {",
                "//     int val;",
                "//     TreeNode *left;",
                "//     TreeNode *right;",
                "//     TreeNode() : val(0), left(nullptr), right(nullptr) {}",
                "//     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}",
                "//     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}",
                "// };",
            ]
        ),
    },
    "java": {
        TypeEnum.LISTNODE: "\n".join(
            [
                "// Definition for singly-linked list.",
                "// class ListNode {",
                "//     int val;",
                "//     ListNode next;",
                "//     ListNode() { this.val = 0; this.next = null; }",
                "//     ListNode(int val) { this.val = val; this.next = null; }",
                "//     ListNode(int val, ListNode next) { this.val = val; this.next = next; }",
                "// }",
            ]
        ),
        TypeEnum.TREENODE: "\n".join(
            [
                "// Definition for a binary tree node.",
                "// class TreeNode {",
                "//     int val;",
                "//     TreeNode left;",
                "//     TreeNode right;",
                "//     TreeNode() { this.val = 0; this.left = null; this.right = null; }",
                "//     TreeNode(int val) { this.val = val; this.left = null; this.right = null; }",
                "//     TreeNode(int val, TreeNode left, TreeNode right) { this.val = val; this.left = left; this.right = right; }",
                "// }",
            ]
        ),
    },
    "py": {
        TypeEnum.LISTNODE: "\n".join(
            [
                "# Definition for singly-linked list.",
                "# class ListNode:",
                "#     def __init__(self, val=0, next=None):",
                "#         self.val = val",
                "#         self.next = next",
            ]
        ),
        TypeEnum.TREENODE: "\n".join(
            [
                "# Definition for a binary tree node.",
                "# class TreeNode:",
                "#     def __init__(self, val=0, left=None, right=None):",
                "#         self.val = val",
                "#         self.left = left",
                "#         self.right = right",
            ]
        ),
    },
    "ts": {
        TypeEnum.LISTNODE: "\n".join(
            [
                "// Definition for singly-linked list.",
                "// class ListNode {",
                "//     val: number;",
                "//     next: ListNode | null;",
                "//     constructor(val?: number, next?: ListNode | null) {",
                "//         this.val = (val === undefined ? 0 : val);",
                "//         this.next = (next === undefined ? null : next);",
                "//     }",
                "// }",
            ]
        ),
        TypeEnum.TREENODE: "\n".join(
            [
                "// Definition for a binary tree node.",
                "// class TreeNode {",
                "//     val: number;",
                "//     left: TreeNode | null;",
                "//     right: TreeNode | null;",
                "//     constructor(val?: number, left?: TreeNode | null, right?: TreeNode | null) {",
                "//         this.val = (val === undefined ? 0 : val);",
                "//         this.left = (left === undefined ? null : left);",
                "//         this.right = (right === undefined ? null : right);",
                "//     }",
                "// }",
            ]
        ),
    },
    "js": {
        TypeEnum.LISTNODE: "\n".join(
            [
                "// Definition for singly-linked list.",
                "// class ListNode {",
                "//     constructor(val, next) {",
                "//         this.val = (val === undefined ? 0 : val);",
                "//         this.next = (next === undefined ? null : next);",
                "//     }",
                "// }",
            ]
        ),
        TypeEnum.TREENODE: "\n".join(
            [
                "// Definition for a binary tree node.",
                "// class TreeNode {",
                "//     constructor(val, left, right) {",
                "//         this.val = (val === undefined ? 0 : val);",
                "//         this.left = (left === undefined ? null : left);",
                "//         this.right = (right === undefined ? null : right);",
                "//     }",
                "// }",
            ]
        ),
    },
    "go": {
        TypeEnum.LISTNODE: "\n".join(
            [
                "// Definition for singly-linked list.",
                "// type ListNode struct {",
                "//     Val  int",
                "//     Next *ListNode",
                "// }",
            ]
        ),
        TypeEnum.TREENODE: "\n".join(
            [
                "// Definition for a binary tree node.",
                "// type TreeNode struct {",
                "//     Val   int",
                "//     Left  *TreeNode",
                "//     Right *TreeNode",
                "// }",
            ]
        ),
    },
}


def method_node_types(method_def: MethodDef) -> set[TypeEnum]:
    types = set(method_def.params_type)
    types.add(method_def.return_type)
    return {t for t in types if t in (TypeEnum.LISTNODE, TypeEnum.TREENODE)}


def class_node_types(class_def: ClassDef) -> set[TypeEnum]:
    types = set(class_def.constructor.params_type)
    for method in class_def.methods:
        types.update(method_node_types(method))
    return {t for t in types if t in (TypeEnum.LISTNODE, TypeEnum.TREENODE)}


def build_node_definition_comments(lang: str, node_types: Iterable[TypeEnum]) -> str:
    templates = NODE_COMMENT_TEMPLATES[lang]
    ordered_types = [TypeEnum.LISTNODE, TypeEnum.TREENODE]
    comments = [templates[node_type] for node_type in ordered_types if node_type in node_types]
    return "\n\n".join(comments)


def prepend_node_definition_comments(code: str, lang: str, node_types: Iterable[TypeEnum]) -> str:
    comments = build_node_definition_comments(lang, node_types)
    if not comments:
        return code
    return f"{comments}\n\n{code}"
