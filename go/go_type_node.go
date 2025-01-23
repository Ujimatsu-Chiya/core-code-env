package main

type TreeNode struct {
    Val   int
    Left  *TreeNode
    Right *TreeNode
}

type ListNode struct {
    Val  int
    Next *ListNode
}

func CreateTreeNode(val int) *TreeNode {
    return &TreeNode{Val: val}
}

func CreateListNode(val int) *ListNode {
    return &ListNode{Val: val}
}