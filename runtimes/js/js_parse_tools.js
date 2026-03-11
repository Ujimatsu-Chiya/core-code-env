"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.desNumberList = desNumberList;
exports.desNumber = desNumber;
exports.desBool = desBool;
exports.desString = desString;
exports.desNumberListList = desNumberListList;
exports.desStringList = desStringList;
exports.desBoolList = desBoolList;
exports.desTreeList = desTreeList;
exports.serNumber = serNumber;
exports.serBool = serBool;
exports.serString = serString;
exports.serNumberList = serNumberList;
exports.serNumberListList = serNumberListList;
exports.serStringList = serStringList;
exports.serBoolList = serBoolList;
exports.serTreeList = serTreeList;
exports.desTree = desTree;
exports.serTree = serTree;
exports.desLinkedList = desLinkedList;
exports.serLinkedList = serLinkedList;
const ts_type_node_1 = require("./js_type_node");
function desNumberList(jsonStr) {
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
function desNumber(jsonStr) {
    const parsed = JSON.parse(jsonStr);
    if (typeof parsed !== "number") {
        throw new TypeError("Input is not a valid number");
    }
    return parsed;
}
function desBool(jsonStr) {
    const parsed = JSON.parse(jsonStr);
    if (typeof parsed !== "boolean") {
        throw new TypeError("Input is not a valid boolean");
    }
    return parsed;
}
function desString(jsonStr) {
    const parsed = JSON.parse(jsonStr);
    if (typeof parsed !== "string") {
        throw new TypeError("Input is not a valid string");
    }
    return parsed;
}
function desNumberListList(jsonStr) {
    const parsed = JSON.parse(jsonStr);
    if (!Array.isArray(parsed)) {
        throw new TypeError("Input is not a valid JSON array");
    }
    return parsed.map(row => {
        if (row === null)
            return [];
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
function desStringList(jsonStr) {
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
function desBoolList(jsonStr) {
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
function desTreeList(jsonStr) {
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
function serNumber(value) {
    return JSON.stringify(value);
}
function serBool(value) {
    return JSON.stringify(value);
}
function serString(value) {
    return JSON.stringify(value);
}
function serNumberList(values) {
    return JSON.stringify(values);
}
function serNumberListList(values) {
    return JSON.stringify(values);
}
function serStringList(values) {
    return JSON.stringify(values);
}
function serBoolList(values) {
    return JSON.stringify(values);
}
function serTreeList(values) {
    return JSON.stringify(values);
}
function desTreeAux(arr) {
    const n = arr.length;
    if (n === 0 || arr[0] === null) {
        return null;
    }
    const root = new ts_type_node_1.TreeNode(arr[0]);
    const q = [root];
    let p = 1;
    while (p < n) {
        const node = q.shift();
        if (p < n && arr[p] !== null) {
            node.left = new ts_type_node_1.TreeNode(arr[p]);
            q.push(node.left);
        }
        p++;
        if (p < n && arr[p] !== null) {
            node.right = new ts_type_node_1.TreeNode(arr[p]);
            q.push(node.right);
        }
        p++;
    }
    return root;
}
function desTree(jsonStr) {
    return desTreeAux(desTreeList(jsonStr));
}
function serTreeAux(root) {
    const result = [];
    if (root === null) {
        return [];
    }
    const q = [root];
    result.push(root.val);
    while (q.length > 0) {
        const u = q.shift();
        if (u.left !== null) {
            q.push(u.left);
            result.push(u.left.val);
        }
        else {
            result.push(null);
        }
        if (u.right !== null) {
            q.push(u.right);
            result.push(u.right.val);
        }
        else {
            result.push(null);
        }
    }
    while (result.length > 0 && result[result.length - 1] === null) {
        result.pop();
    }
    return result;
}
function serTree(root) {
    return serTreeList(serTreeAux(root));
}
function desLinkedListAux(arr) {
    const n = arr.length;
    if (n === 0) {
        return null;
    }
    const head = new ts_type_node_1.ListNode(arr[0]);
    let tail = head;
    for (let i = 1; i < n; i++) {
        const p = new ts_type_node_1.ListNode(arr[i]);
        tail.next = p;
        tail = p;
    }
    return head;
}
function desLinkedList(jsonStr) {
    return desLinkedListAux(desNumberList(jsonStr));
}
function serLinkedListAux(head) {
    const result = [];
    let p = head;
    while (p !== null) {
        result.push(p.val);
        p = p.next;
    }
    return result;
}
function serLinkedList(head) {
    return serNumberList(serLinkedListAux(head));
}
