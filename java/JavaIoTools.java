import java.io.*;
import java.nio.charset.StandardCharsets;

class StdinWrapper {
    private BufferedReader reader;
    private static String filePath = "user.in";
    public StdinWrapper() throws IOException {
        reader = new BufferedReader(new InputStreamReader(new FileInputStream(filePath), StandardCharsets.UTF_8));
    }

    public String readLine() throws IOException {
        String line = reader.readLine();
        if (line == null || line.isEmpty()) {
            return null;
        }
        return line;
    }
}

class StdoutWrapper {
    private BufferedWriter writer;
    private static String filePath = "user.out";

    public StdoutWrapper() throws IOException {
        writer = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(filePath), StandardCharsets.UTF_8));
    }

    public void writeLine(String s) throws IOException {
        writer.write(s);
        writer.newLine();
        writer.flush();
    }

}