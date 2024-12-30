public class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;

    // 构造方法，只有值
    public TreeNode(int val) {
        this.val = val;
        this.left = null;
        this.right = null;
    }

    // 构造方法，带值和左右子节点
    public TreeNode(int val, TreeNode left, TreeNode right) {
        this.val = val;
        this.left = left;
        this.right = right;
    }
}
