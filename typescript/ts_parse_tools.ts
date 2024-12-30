import { TreeNode, ListNode } from './ts_type_node';

export function desIntList(jsonStr: string): number[] {
    const parsed = JSON.parse(jsonStr);

    if (!Array.isArray(parsed)) {
        throw new TypeError("Input is not a valid JSON array");
    }

    return parsed.map(item => {
        if (typeof item !== "number") {
            throw new TypeError("Array contains non-number elements");
        }
        return item;
    });
}

export function desInt(jsonStr: string): number {
    const parsed = JSON.parse(jsonStr);
    if (typeof parsed !== "number") {
        throw new TypeError("Input is not a valid number");
    }
    return parsed;
}

export function desBool(jsonStr: string): boolean {
    const parsed = JSON.parse(jsonStr);
    if (typeof parsed !== "boolean") {
        throw new TypeError("Input is not a valid boolean");
    }
    return parsed;
}

export function desString(jsonStr: string): string {
    const parsed = JSON.parse(jsonStr);
    if (typeof parsed !== "string") {
        throw new TypeError("Input is not a valid string");
    }
    return parsed;
}

export function desIntListList(jsonStr: string): (number[] | null)[] {
    const parsed = JSON.parse(jsonStr);
    if (!Array.isArray(parsed)) {
        throw new TypeError("Input is not a valid JSON array");
    }

    return parsed.map(row => {
        if (row === null) return null;
        if (!Array.isArray(row)) {
            throw new TypeError("Row is not a valid array");
        }
        return row.map(item => {
            if (typeof item !== "number") {
                throw new TypeError("Array contains non-number elements");
            }
            return item;
        });
    });
}

export function desStringList(jsonStr: string): string[] {
    const parsed = JSON.parse(jsonStr);
    if (!Array.isArray(parsed)) {
        throw new TypeError("Input is not a valid JSON array");
    }
    return parsed.map(item => {
        if (typeof item !== "string") {
            throw new TypeError("Array contains non-string elements");
        }
        return item;
    });
}

export function desBoolList(jsonStr: string): boolean[] {
    const parsed = JSON.parse(jsonStr);
    if (!Array.isArray(parsed)) {
        throw new TypeError("Input is not a valid JSON array");
    }
    return parsed.map(item => {
        if (typeof item !== "boolean") {
            throw new TypeError("Array contains non-boolean elements");
        }
        return item;
    });
}

export function desTreeList(jsonStr: string): (number | null)[] {
    const parsed = JSON.parse(jsonStr);
    if (!Array.isArray(parsed)) {
        throw new TypeError("Input is not a valid JSON array");
    }
    return parsed.map(item => {
        if (item !== null && typeof item !== "number") {
            throw new TypeError("Array contains non-number and non-null elements");
        }
        return item;
    });
}

export function serInt(value: number): string {
    return JSON.stringify(value);
}

export function serBool(value: boolean): string {
    return JSON.stringify(value);
}

export function serString(value: string): string {
    return JSON.stringify(value);
}

export function serIntList(values: number[]): string {
    return JSON.stringify(values);
}

export function serIntListList(values: number[][]): string {
    return JSON.stringify(values);
}

export function serStringList(values: string[]): string {
    return JSON.stringify(values);
}

export function serBoolList(values: boolean[]): string {
    return JSON.stringify(values);
}

export function serTreeList(values: (number | null)[]): string {
    return JSON.stringify(values);
}

function desTreeAux(arr: number[]): TreeNode | null {
    const n = arr.length;
    if (n === 0 || arr[0] === null) {
        return null;
    }

    const root = new TreeNode(arr[0]);
    const q: TreeNode[] = [root];
    let p = 1;

    while (p < n) {
        const node = q.shift()!;

        if (p < n && arr[p] !== null) {
            node.left = new TreeNode(arr[p]);
            q.push(node.left);
        }
        p++;

        if (p < n && arr[p] !== null) {
            node.right = new TreeNode(arr[p]);
            q.push(node.right);
        }
        p++;
    }
    return root;
}

export function desTree(jsonStr: string): TreeNode | null {
    return desTreeAux(desTreeList(jsonStr));
}

function serTreeAux(root: TreeNode | null): number[] {
    const result: number[] = [];
    if (root === null) {
        return [];
    }

    const q: TreeNode[] = [root];
    result.push(root.val);

    while (q.length > 0) {
        const u = q.shift()!;
        if (u.left !== null) {
            q.push(u.left);
            result.push(u.left.val);
        } else {
            result.push(null);
        }

        if (u.right !== null) {
            q.push(u.right);
            result.push(u.right.val);
        } else {
            result.push(null);
        }
    }
    while (result.length > 0 && result[result.length - 1] === null) {
        result.pop();
    }

    return result;
}

export function serTree(root: TreeNode | null): string {
    return serTreeList(serTreeAux(root));
}

function desLinkedListAux(arr: number[]): ListNode | null {
    const n = arr.length;
    if (n === 0) {
        return null;
    }

    const head = new ListNode(arr[0]);
    let tail = head;
    for (let i = 1; i < n; i++) {
        const p = new ListNode(arr[i]);
        tail.next = p;
        tail = p;
    }
    return head;
}

export function desLinkedList(jsonStr: string): ListNode | null {
    return desLinkedListAux(desIntList(jsonStr));
}


function serLinkedListAux(head: ListNode | null): number[] {
    const result: number[] = [];
    let p: ListNode | null = head;
    while (p !== null) {
        result.push(p.val);
        p = p.next;
    }

    return result;
}

export function serLinkedList(head: ListNode | null): string {
    return serIntList(serLinkedListAux(head));
}

