
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;

public class JavaParseTools extends JavaParseModule{
    public static TreeNode desTree(String jsonStr) {
        return desTreeAux(desTreeList(jsonStr));
    }

    private static TreeNode desTreeAux(int[] arr) {
        int n = arr.length;
        if (n == 0 || arr[0] == Integer.MIN_VALUE) {
            return null;
        }

        TreeNode root = new TreeNode(arr[0]);
        Queue<TreeNode> q = new LinkedList<>();
        q.add(root);
        int p = 1;

        while (p < n) {
            TreeNode node = q.poll();

            if (p < n && arr[p] != Integer.MIN_VALUE) {
                node.left = new TreeNode(arr[p]);
                q.add(node.left);
            }
            p++;

            if (p < n && arr[p] != Integer.MIN_VALUE) {
                node.right = new TreeNode(arr[p]);
                q.add(node.right);
            }
            p++;
        }
        return root;
    }

    public static String serTree(TreeNode root) {
        return serTreeList(serTreeAux(root));
    }

    private static int[] serTreeAux(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) {
            return new int[0];
        }

        Queue<TreeNode> q = new LinkedList<>();
        q.add(root);
        result.add(root.val);

        while (!q.isEmpty()) {
            TreeNode u = q.poll();
            if (u.left != null) {
                q.add(u.left);
                result.add(u.left.val);
            } else {
                result.add(Integer.MIN_VALUE);
            }

            if (u.right != null) {
                q.add(u.right);
                result.add(u.right.val);
            } else {
                result.add(Integer.MIN_VALUE);
            }
        }

        while (!result.isEmpty() && result.get(result.size() - 1) == Integer.MIN_VALUE) {
            result.remove(result.size() - 1);
        }

        int[] arr = new int[result.size()];
        for (int i = 0; i < result.size(); i++) {
            arr[i] = result.get(i);
        }

        return arr;
    }

    public static ListNode desLinkedList(String jsonStr) {
        return desLinkedListAux(desIntList(jsonStr));
    }
    
    private static ListNode desLinkedListAux(int[] arr) {
        int n = arr.length;
        if (n == 0) {
            return null;
        }
        ListNode head = new ListNode(arr[0]);
        ListNode tail = head;
        for (int i = 1; i < n; i++) {
            ListNode p = new ListNode(arr[i]);
            tail.next = p;
            tail = p;
        }
        return head;
    }
    
    public static String serLinkedList(ListNode head) {
        return serIntList(serLinkedListAux(head));
    }
    
    private static int[] serLinkedListAux(ListNode head) {
        List<Integer> result = new ArrayList<>();
        ListNode p = head;
        while (p != null) {
            result.add(p.val);
            p = p.next;
        }

        int[] arr = new int[result.size()];
        for (int i = 0; i < result.size(); i++) {
            arr[i] = result.get(i);
        }
    
        return arr;
    }
}
