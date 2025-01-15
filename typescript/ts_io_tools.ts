import * as fs from 'fs';


const READ_PATH = 'user.in';
const WRITE_PATH = 'user.out';

export class StdinWrapper {
    private lines: string[];
    private currentLineIndex: number;

    constructor() {
        const fileContent = fs.readFileSync(READ_PATH, 'utf-8');
        this.lines = fileContent.split('\n').map(line => line.trim());
        const emptyIndex = this.lines.findIndex(line => line === '');
        if (emptyIndex !== -1) {
            this.lines = this.lines.slice(0, emptyIndex);
        }
        this.currentLineIndex = 0;
    }
    public readLine(): string | null {
        if (this.currentLineIndex < this.lines.length) {
            return this.lines[this.currentLineIndex++];
        }
        return null;
    }
}

export class StdoutWrapper {
    private stdout: fs.WriteStream;

    constructor() {
        this.stdout = fs.createWriteStream(WRITE_PATH, { flags: 'w' });
    }

    public writeLine(s: string): void {
        this.stdout.write(s + '\n');
    }
}

