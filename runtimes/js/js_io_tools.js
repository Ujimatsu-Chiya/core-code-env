"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.StdoutWrapper = exports.StdinWrapper = void 0;
const fs = require("fs");
const READ_PATH = 'user.in';
const WRITE_PATH = 'user.out';
class StdinWrapper {
    constructor() {
        const fileContent = fs.readFileSync(READ_PATH, 'utf-8');
        this.lines = fileContent.split('\n').map(line => line.trim());
        const emptyIndex = this.lines.findIndex(line => line === '');
        if (emptyIndex !== -1) {
            this.lines = this.lines.slice(0, emptyIndex);
        }
        this.currentLineIndex = 0;
    }
    readLine() {
        if (this.currentLineIndex < this.lines.length) {
            return this.lines[this.currentLineIndex++];
        }
        return null;
    }
}
exports.StdinWrapper = StdinWrapper;
class StdoutWrapper {
    constructor() {
        this.stdout = fs.createWriteStream(WRITE_PATH, { flags: 'w' });
    }
    writeLine(s) {
        this.stdout.write(s + '\n');
    }
}
exports.StdoutWrapper = StdoutWrapper;
