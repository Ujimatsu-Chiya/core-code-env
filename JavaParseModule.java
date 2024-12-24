public class JavaParseModule {
    static {
        System.loadLibrary("java_parse_module");  // 加载本地库
    }

    // Deserialization methods
    public native int[] desIntList(String arg);
    public native long[] desLongList(String arg);
    public native boolean[] desBoolList(String arg);
    public native int desInt(String arg);
    public native long desLong(String arg);
    public native String desString(String arg);
    public native int[][] desIntListList(String arg);
    public native String[] desStringList(String arg);
    public native double[] desDoubleList(String arg);
    public native boolean desBool(String arg);
    public native double desDouble(String arg);
    public native int[] desTreeList(String arg);

    // Serialization methods (now return String)
    public native String serInt(int value);
    public native String serLong(long value);
    public native String serBool(boolean value);
    public native String serString(String value);
    public native String serIntList(int[] value);
    public native String serLongList(long[] value);
    public native String serDouble(double value);
    public native String serDoubleList(double[] value);
    public native String serIntListList(Object[] value);
    public native String serStringList(String[] value);
    public native String serBoolList(boolean[] value);
    public native String serTreeList(int[] value);
}

/*
 * 
g++ -fPIC -shared -o libjava_parse_module.so java_parse_module.cpp rapidjson_helper.cpp -I$JAVA_HOME/include -I$JAVA_HOME/include/linux
javac JavaParseModule.java 
javac -h . JavaParseModule.java 
java -Djava.library.path=. JavaParseModule
 */