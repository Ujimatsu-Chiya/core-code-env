from py_node_type import *
from py_parse_module import *
from collections import deque

INT_MIN = -2 ** 31

def _des_tree_aux(arr):
    n = len(arr)
    if n == 0 or arr[0] == INT_MIN:
        return None
    root = TreeNode(arr[0])
    q = deque([root])
    p = 1
    while p < n:
        node = q.popleft()
        if p < n and arr[p] != INT_MIN:
            node.left = TreeNode(arr[p])
            q.append(node.left)
        p += 1
        if p < n and arr[p] != INT_MIN:
            node.right = TreeNode(arr[p])
            q.append(node.right)
        p += 1
    return root

def des_tree(json_str):
    return _des_tree_aux(des_tree_list(json_str))


def _ser_tree_aux(root):
    if root is None:
        return []
    print(type(root))
    q = deque([root])
    result = [root.val]
    while q:
        u = q.popleft()
        if u.left:
            q.append(u.left)
            result.append(u.left.val)
        else:
            result.append(INT_MIN)
        if u.right:
            q.append(u.right)
            result.append(u.right.val)
        else:
            result.append(INT_MIN)
    while result and result[-1] == INT_MIN:
        result.pop()
    return result


def ser_tree(root:TreeNode):
    return ser_tree_list(_ser_tree_aux(root))

def _des_linked_list_aux(arr):
    n = len(arr)
    if n == 0:
        return None
    head = ListNode(arr[0])
    tail = head
    for i in range(1, n):
        p = ListNode(arr[i])
        tail.next = p
        tail = p
    return head


def des_linked_list(json_str:str):
    return _des_linked_list_aux(des_int_list(json_str))


def _ser_linked_list_aux(head):
    result = []
    p = head
    while p:
        result.append(p.val)
        p = p.next
    return result

def ser_linked_list(head:ListNode):
    return ser_int_list(_ser_linked_list_aux(head))
