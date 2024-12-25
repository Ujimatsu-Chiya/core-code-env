public class JavaParseModule {
    static {
        System.loadLibrary("java_parse_module");  // 加载本地库
    }

    // Deserialization methods
    public static native int[] desIntList(String arg);
    public static native long[] desLongList(String arg);
    public static native boolean[] desBoolList(String arg);
    public static native int desInt(String arg);
    public static native long desLong(String arg);
    public static native String desString(String arg);
    public static native int[][] desIntListList(String arg);
    public static native String[] desStringList(String arg);
    public static native double[] desDoubleList(String arg);
    public static native boolean desBool(String arg);
    public static native double desDouble(String arg);
    public static native int[] desTreeList(String arg);

    // Serialization methods (now return String)
    public static native String serInt(int value);
    public static native String serLong(long value);
    public static native String serBool(boolean value);
    public static native String serString(String value);
    public static native String serIntList(int[] value);
    public static native String serLongList(long[] value);
    public static native String serDouble(double value);
    public static native String serDoubleList(double[] value);
    public static native String serIntListList(Object[] value);
    public static native String serStringList(String[] value);
    public static native String serBoolList(boolean[] value);
    public static native String serTreeList(int[] value);
}

/*
 * 
g++ -fPIC -shared -o libjava_parse_module.so java_parse_module.cpp rapidjson_helper.cpp -I$JAVA_HOME/include -I$JAVA_HOME/include/linux
javac JavaParseModule.java 
javac -h . JavaParseModule.java 
java -Djava.library.path=. JavaParseModule
 */