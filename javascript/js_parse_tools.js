"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.desIntList = desIntList;
exports.desInt = desInt;
exports.desBool = desBool;
exports.desString = desString;
exports.desIntListList = desIntListList;
exports.desStringList = desStringList;
exports.desBoolList = desBoolList;
exports.desTreeList = desTreeList;
exports.serInt = serInt;
exports.serBool = serBool;
exports.serString = serString;
exports.serIntList = serIntList;
exports.serIntListList = serIntListList;
exports.serStringList = serStringList;
exports.serBoolList = serBoolList;
exports.serTreeList = serTreeList;
exports.desTree = desTree;
exports.serTree = serTree;
exports.desLinkedList = desLinkedList;
exports.serLinkedList = serLinkedList;
var ts_type_node_1 = require("./ts_type_node");
function desIntList(jsonStr) {
    var parsed = JSON.parse(jsonStr);
    if (!Array.isArray(parsed)) {
        throw new TypeError("Input is not a valid JSON array");
    }
    return parsed.map(function (item) {
        if (typeof item !== "number") {
            throw new TypeError("Array contains non-number elements");
        }
        return item;
    });
}
function desInt(jsonStr) {
    var parsed = JSON.parse(jsonStr);
    if (typeof parsed !== "number") {
        throw new TypeError("Input is not a valid number");
    }
    return parsed;
}
function desBool(jsonStr) {
    var parsed = JSON.parse(jsonStr);
    if (typeof parsed !== "boolean") {
        throw new TypeError("Input is not a valid boolean");
    }
    return parsed;
}
function desString(jsonStr) {
    var parsed = JSON.parse(jsonStr);
    if (typeof parsed !== "string") {
        throw new TypeError("Input is not a valid string");
    }
    return parsed;
}
function desIntListList(jsonStr) {
    var parsed = JSON.parse(jsonStr);
    if (!Array.isArray(parsed)) {
        throw new TypeError("Input is not a valid JSON array");
    }
    return parsed.map(function (row) {
        if (row === null)
            return null;
        if (!Array.isArray(row)) {
            throw new TypeError("Row is not a valid array");
        }
        return row.map(function (item) {
            if (typeof item !== "number") {
                throw new TypeError("Array contains non-number elements");
            }
            return item;
        });
    });
}
function desStringList(jsonStr) {
    var parsed = JSON.parse(jsonStr);
    if (!Array.isArray(parsed)) {
        throw new TypeError("Input is not a valid JSON array");
    }
    return parsed.map(function (item) {
        if (typeof item !== "string") {
            throw new TypeError("Array contains non-string elements");
        }
        return item;
    });
}
function desBoolList(jsonStr) {
    var parsed = JSON.parse(jsonStr);
    if (!Array.isArray(parsed)) {
        throw new TypeError("Input is not a valid JSON array");
    }
    return parsed.map(function (item) {
        if (typeof item !== "boolean") {
            throw new TypeError("Array contains non-boolean elements");
        }
        return item;
    });
}
function desTreeList(jsonStr) {
    var parsed = JSON.parse(jsonStr);
    if (!Array.isArray(parsed)) {
        throw new TypeError("Input is not a valid JSON array");
    }
    return parsed.map(function (item) {
        if (item !== null && typeof item !== "number") {
            throw new TypeError("Array contains non-number and non-null elements");
        }
        return item;
    });
}
function serInt(value) {
    return JSON.stringify(value);
}
function serBool(value) {
    return JSON.stringify(value);
}
function serString(value) {
    return JSON.stringify(value);
}
function serIntList(values) {
    return JSON.stringify(values);
}
function serIntListList(values) {
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
    var n = arr.length;
    if (n === 0 || arr[0] === null) {
        return null;
    }
    var root = new ts_type_node_1.TreeNode(arr[0]);
    var q = [root];
    var p = 1;
    while (p < n) {
        var node = q.shift();
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
    var result = [];
    if (root === null) {
        return [];
    }
    var q = [root];
    result.push(root.val);
    while (q.length > 0) {
        var u = q.shift();
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
    var n = arr.length;
    if (n === 0) {
        return null;
    }
    var head = new ts_type_node_1.ListNode(arr[0]);
    var tail = head;
    for (var i = 1; i < n; i++) {
        var p = new ts_type_node_1.ListNode(arr[i]);
        tail.next = p;
        tail = p;
    }
    return head;
}
function desLinkedList(jsonStr) {
    return desLinkedListAux(desIntList(jsonStr));
}
function serLinkedListAux(head) {
    var result = [];
    var p = head;
    while (p !== null) {
        result.push(p.val);
        p = p.next;
    }
    return result;
}
function serLinkedList(head) {
    return serIntList(serLinkedListAux(head));
}
// var s = '[1,2,3,null, 5]'
// console.log(serTree(desTree(s)))
