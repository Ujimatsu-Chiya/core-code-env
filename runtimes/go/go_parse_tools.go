package main

import (
	"encoding/json"
	"fmt"
	"math"
	"os"
	"container/list"
)

func DesIntList(jsonStr string) []int {
	var arr []int
	err := json.Unmarshal([]byte(jsonStr), &arr)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error during Deserialization: %v\n", err)
		os.Exit(1)
	}
	return arr
}

func DesBool(jsonStr string) bool {
	var b bool
	err := json.Unmarshal([]byte(jsonStr), &b)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error during Deserialization: %v\n", err)
		os.Exit(1)
	}
	return b
}

func DesInt(jsonStr string) int {
	var i int
	err := json.Unmarshal([]byte(jsonStr), &i)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error during Deserialization: %v\n", err)
		os.Exit(1)
	}
	return i
}

func DesLong(jsonStr string) int64 {
	var l int64
	err := json.Unmarshal([]byte(jsonStr), &l)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error during Deserialization: %v\n", err)
		os.Exit(1)
	}
	return l
}

func DesDouble(jsonStr string) float64 {
	var d float64
	err := json.Unmarshal([]byte(jsonStr), &d)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error during Deserialization: %v\n", err)
		os.Exit(1)
	}
	return d
}

func DesString(jsonStr string) string {
	var s string
	err := json.Unmarshal([]byte(jsonStr), &s)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error during Deserialization: %v\n", err)
		os.Exit(1)
	}
	return s
}

func DesIntListList(jsonStr string) [][]int {
	var arr [][]int
	err := json.Unmarshal([]byte(jsonStr), &arr)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error during Deserialization: %v\n", err)
		os.Exit(1)
	}
	return arr
}

func DesDoubleList(jsonStr string) []float64 {
	var arr []float64
	err := json.Unmarshal([]byte(jsonStr), &arr)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error during Deserialization: %v\n", err)
		os.Exit(1)
	}
	return arr
}

func DesStringList(jsonStr string) []string {
	var arr []string
	err := json.Unmarshal([]byte(jsonStr), &arr)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error during Deserialization: %v\n", err)
		os.Exit(1)
	}
	return arr
}

func DesBoolList(jsonStr string) []bool {
	var arr []bool
	err := json.Unmarshal([]byte(jsonStr), &arr)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error during Deserialization: %v\n", err)
		os.Exit(1)
	}
	return arr
}

func DesLongList(jsonStr string) []int64 {
	var arr []int64
	err := json.Unmarshal([]byte(jsonStr), &arr)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error during Deserialization: %v\n", err)
		os.Exit(1)
	}
	return arr
}

func DesTreeList(jsonStr string) []int {
	var arr []interface{}
	err := json.Unmarshal([]byte(jsonStr), &arr)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error during Deserialization: %v\n", err)
		os.Exit(1)
	}

	var result []int
	for _, v := range arr {
		if v == nil {
			result = append(result, math.MinInt32)
		} else {
			if val, ok := v.(float64); ok {
				result = append(result, int(val))
			} else {
				fmt.Fprintf(os.Stderr, "Error: expected integer or null, got %T\n", v)
				os.Exit(1)
			}
		}
	}

	return result
}

func _DesTreeAux(arr []int) *TreeNode {
	n := len(arr)
	if n == 0 || arr[0] == math.MinInt32 {
		return nil
	}
	root := &TreeNode{Val: arr[0]}
	q := list.New()
	q.PushBack(root)
	p := 1
	for p < n {
		node := q.Front().Value.(*TreeNode)
		q.Remove(q.Front())

		if p < n && arr[p] != math.MinInt32 {
			node.Left = &TreeNode{Val: arr[p]}
			q.PushBack(node.Left)
		}
		p++

		if p < n && arr[p] != math.MinInt32 {
			node.Right = &TreeNode{Val: arr[p]}
			q.PushBack(node.Right)
		}
		p++
	}
	return root
}

func DesTree(jsonStr string) *TreeNode {
	treeList := DesTreeList(jsonStr)
	return _DesTreeAux(treeList)
}

func _DesLinkedListAux(arr []int) *ListNode {
	n := len(arr)
	if n == 0 {
		return nil
	}

	head := &ListNode{Val: arr[0]}
	tail := head

	for i := 1; i < n; i++ {
		node := &ListNode{Val: arr[i]}
		tail.Next = node
		tail = node
	}
	return head
}

func DesLinkedList(jsonStr string) *ListNode {
	arr := DesIntList(jsonStr)
	return _DesLinkedListAux(arr)
}

func SerBool(value bool) string {
	jsonStr, err := json.Marshal(value)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error during Serialization: %v\n", err)
		os.Exit(1)
	}
	return string(jsonStr)
}

func SerInt(value int) string {
	jsonStr, err := json.Marshal(value)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error during Serialization: %v\n", err)
		os.Exit(1)
	}
	return string(jsonStr)
}

func SerLong(value int64) string {
	jsonStr, err := json.Marshal(value)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error during Serialization: %v\n", err)
		os.Exit(1)
	}
	return string(jsonStr)
}

func SerDouble(value float64) string {
	jsonStr, err := json.Marshal(value)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error during Serialization: %v\n", err)
		os.Exit(1)
	}
	return string(jsonStr)
}

func SerString(value string) string {
	jsonStr, err := json.Marshal(value)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error during Serialization: %v\n", err)
		os.Exit(1)
	}
	return string(jsonStr)
}

func SerIntList(values []int) string {
	jsonStr, err := json.Marshal(values)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error during Serialization: %v\n", err)
		os.Exit(1)
	}
	return string(jsonStr)
}

func SerIntListList(values [][]int) string {
	jsonStr, err := json.Marshal(values)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error during Serialization: %v\n", err)
		os.Exit(1)
	}
	return string(jsonStr)
}

func SerDoubleList(values []float64) string {
	jsonStr, err := json.Marshal(values)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error during Serialization: %v\n", err)
		os.Exit(1)
	}
	return string(jsonStr)
}

func SerStringList(values []string) string {
	jsonStr, err := json.Marshal(values)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error during Serialization: %v\n", err)
		os.Exit(1)
	}
	return string(jsonStr)
}

func SerBoolList(values []bool) string {
	jsonStr, err := json.Marshal(values)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error during Serialization: %v\n", err)
		os.Exit(1)
	}
	return string(jsonStr)
}

func SerLongList(values []int64) string {
	jsonStr, err := json.Marshal(values)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error during Serialization: %v\n", err)
		os.Exit(1)
	}
	return string(jsonStr)
}

func _SerTreeAux(root *TreeNode) []interface{} {
	if root == nil {
		return []interface{}{}
	}

	queue := []*TreeNode{root}
	result := []interface{}{}
	for len(queue) > 0 {
		node := queue[0]
		queue = queue[1:]

		if node != nil {
			result = append(result, node.Val)
			queue = append(queue, node.Left, node.Right)
		} else {
			result = append(result, nil)
		}
	}

	for len(result) > 0 && result[len(result)-1] == nil {
		result = result[:len(result)-1]
	}
	return result
}

func SerTree(root *TreeNode) string {
	arr := _SerTreeAux(root)
	jsonStr, err := json.Marshal(arr)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error during Serialization: %v\n", err)
		return ""
	}
	return string(jsonStr)
}

func _SerLinkedListAux(head *ListNode) []int {
	result := []int{}
	for p := head; p != nil; p = p.Next {
		result = append(result, p.Val)
	}
	return result
}

func SerLinkedList(head *ListNode) string {
	arr := _SerLinkedListAux(head)
	jsonStr, err := json.Marshal(arr)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error during Serialization: %v\n", err)
		os.Exit(1)
	}
	return string(jsonStr)
}