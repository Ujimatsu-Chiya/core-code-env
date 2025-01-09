#include <jni.h>
#include "JavaParseModule.h"
#include "../rapidjson_helper.h"
#include <new>

// Helper function to throw Java exceptions
static void throw_java_exception(JNIEnv* env, const char* exception_class, const char* message) {
    jclass exClass = env->FindClass(exception_class);
    if (exClass != nullptr) {
        env->ThrowNew(exClass, message);
    }
}


JNIEXPORT jintArray JNICALL Java_JavaParseModule_desIntList(JNIEnv* env, jclass clazz, jstring arg) {
    // Convert jstring to C++ string
    const char* json_str = env->GetStringUTFChars(arg, nullptr);

    // Parse the JSON string using the existing des_src_int_list function
    size_t size = 0;
    int* int_array = des_src_int_list(json_str, &size);

    // Release the jstring memory
    env->ReleaseStringUTFChars(arg, json_str);

    // Check if the des_src_int_list function failed
    if (!int_array) {
        throw_java_exception(env, "java/lang/IllegalArgumentException", "Error parsing JSON or invalid array.");
        return nullptr;
    }

    // Create a jintArray to hold the integers
    jintArray result = env->NewIntArray(size);
    if (result == nullptr) {
        delete[] int_array;  // Free the allocated memory if allocation of jintArray fails
        throw_java_exception(env, "java/lang/OutOfMemoryError", "Failed to allocate memory for jintArray.");
        return nullptr;
    }

    // Fill the jintArray with the parsed values
    env->SetIntArrayRegion(result, 0, size, int_array);

    // Free the memory allocated for the C++ array
    delete[] int_array;

    return result;
}

JNIEXPORT jlongArray JNICALL Java_JavaParseModule_desLongList(JNIEnv* env, jclass clazz, jstring arg) {
    // Convert jstring to C++ string
    const char* json_str = env->GetStringUTFChars(arg, nullptr);

    // Parse the JSON string using the existing des_src_long_list function
    size_t size = 0;
    long long* long_array = des_src_long_list(json_str, &size);

    // Release the jstring memory
    env->ReleaseStringUTFChars(arg, json_str);

    // Check if the des_src_long_list function failed
    if (!long_array) {
        throw_java_exception(env, "java/lang/IllegalArgumentException", "Error parsing JSON or invalid array.");
        return nullptr;
    }

    // Create a jlongArray to hold the long integers
    jlongArray result = env->NewLongArray(size);
    if (result == nullptr) {
        delete[] long_array;  // Free the allocated memory if allocation of jlongArray fails
        throw_java_exception(env, "java/lang/OutOfMemoryError", "Failed to allocate memory for jlongArray.");
        return nullptr;
    }

    // Fill the jlongArray with the parsed values
    // Use reinterpret_cast to convert long long* to jlong*
    env->SetLongArrayRegion(result, 0, size, reinterpret_cast<jlong*>(long_array));

    // Free the memory allocated for the C++ array
    delete[] long_array;

    return result;
}

JNIEXPORT jbooleanArray JNICALL Java_JavaParseModule_desBoolList(JNIEnv* env, jclass clazz, jstring arg) {
    // Convert jstring to C++ string
    const char* json_str = env->GetStringUTFChars(arg, nullptr);

    // Parse the JSON string using the existing des_src_bool_list function
    size_t size = 0;
    bool* bool_array = des_src_bool_list(json_str, &size);

    // Release the jstring memory
    env->ReleaseStringUTFChars(arg, json_str);

    // Check if the des_src_bool_list function failed
    if (!bool_array) {
        throw_java_exception(env, "java/lang/IllegalArgumentException", "Error parsing JSON or invalid array.");
        return nullptr;
    }

    // Create a jbooleanArray to hold the boolean values
    jbooleanArray result = env->NewBooleanArray(size);
    if (result == nullptr) {
        delete[] bool_array;  // Free the allocated memory if allocation of jbooleanArray fails
        throw_java_exception(env, "java/lang/OutOfMemoryError", "Failed to allocate memory for jbooleanArray.");
        return nullptr;
    }

    // Create a temporary jboolean array to hold the values
    jboolean* jbool_array = new(std::nothrow) jboolean[size];
    for (size_t i = 0; i < size; i++) {
        // Convert bool to jboolean (JNI_TRUE or JNI_FALSE)
        jbool_array[i] = bool_array[i] ? JNI_TRUE : JNI_FALSE;
    }

    // Fill the jbooleanArray with the parsed values
    env->SetBooleanArrayRegion(result, 0, size, jbool_array);

    // Free the memory allocated for the temporary jboolean array
    delete[] jbool_array;

    // Free the memory allocated for the C++ bool array
    delete[] bool_array;

    return result;
}

JNIEXPORT jint JNICALL Java_JavaParseModule_desInt(JNIEnv* env, jclass clazz, jstring arg) {
    // Convert jstring to C++ string
    const char* json_str = env->GetStringUTFChars(arg, nullptr);

    // Parse the JSON string using the existing des_src_int function
    int value = 0;
    if (!des_src_int(json_str, &value)) {
        env->ReleaseStringUTFChars(arg, json_str);
        throw_java_exception(env, "java/lang/IllegalArgumentException", "Error parsing JSON or invalid integer.");
        return 0;
    }

    // Release the jstring memory
    env->ReleaseStringUTFChars(arg, json_str);

    return value;
}

JNIEXPORT jlong JNICALL Java_JavaParseModule_desLong(JNIEnv* env, jclass clazz, jstring arg) {
    // Convert jstring to C++ string
    const char* json_str = env->GetStringUTFChars(arg, nullptr);

    // Parse the JSON string using the existing des_src_long function
    long long value = 0;
    if (!des_src_long(json_str, &value)) {
        env->ReleaseStringUTFChars(arg, json_str);
        throw_java_exception(env, "java/lang/IllegalArgumentException", "Error parsing JSON or invalid long.");
        return 0;
    }

    // Release the jstring memory
    env->ReleaseStringUTFChars(arg, json_str);

    return static_cast<jlong>(value);
}

JNIEXPORT jstring JNICALL Java_JavaParseModule_desString(JNIEnv* env, jclass clazz, jstring arg) {
    // Convert jstring to C++ string
    const char* json_str = env->GetStringUTFChars(arg, nullptr);

    // Parse the JSON string using the existing des_src_string function
    char* result_str = des_src_string(json_str);

    // Release the jstring memory
    env->ReleaseStringUTFChars(arg, json_str);

    // Check if the des_src_string function failed
    if (!result_str) {
        throw_java_exception(env, "java/lang/IllegalArgumentException", "Error parsing JSON or invalid string.");
        return nullptr;
    }

    // Convert C string to jstring and return
    jstring result = env->NewStringUTF(result_str);

    // Clean up the allocated C string
    delete[] result_str;

    return result;
}

JNIEXPORT jobjectArray JNICALL Java_JavaParseModule_desIntListList(JNIEnv* env, jclass clazz, jstring arg) {
    // Convert jstring to C++ string
    const char* json_str = env->GetStringUTFChars(arg, nullptr);

    // Parse the JSON string using the existing des_src_int_list_list function
    size_t rows = 0, *cols = nullptr;
    int** int_list_list = des_src_int_list_list(json_str, &rows, &cols);

    // Release the jstring memory
    env->ReleaseStringUTFChars(arg, json_str);

    // Check if the des_src_int_list_list function failed
    if (!int_list_list) {
        throw_java_exception(env, "java/lang/IllegalArgumentException", "Error parsing JSON or invalid int list list.");
        return nullptr;
    }

    // Create the outer jobjectArray (int[] array)
    jobjectArray result = env->NewObjectArray(rows, env->FindClass("[I"), nullptr);
    if (result == nullptr) {
        throw_java_exception(env, "java/lang/OutOfMemoryError", "Failed to allocate memory for outer jobjectArray.");
        return nullptr;
    }

    // Fill the outer array with inner arrays
    for (size_t i = 0; i < rows; i++) {
        jintArray inner_array = env->NewIntArray(cols[i]);
        env->SetIntArrayRegion(inner_array, 0, cols[i], int_list_list[i]);
        env->SetObjectArrayElement(result, i, inner_array);
        env->DeleteLocalRef(inner_array);  // Clean up the inner array reference
    }

    // Clean up allocated memory for the 2D array
    delete[] int_list_list;
    delete[] cols;

    return result;
}

JNIEXPORT jobjectArray JNICALL Java_JavaParseModule_desStringList(JNIEnv* env, jclass clazz, jstring arg) {
    // Convert jstring to C++ string
    const char* json_str = env->GetStringUTFChars(arg, nullptr);

    // Parse the JSON string using the existing des_src_string_list function
    size_t size = 0;
    char** str_array = des_src_string_list(json_str, &size);

    // Release the jstring memory
    env->ReleaseStringUTFChars(arg, json_str);

    // Check if the des_src_string_list function failed
    if (!str_array) {
        throw_java_exception(env, "java/lang/IllegalArgumentException", "Error parsing JSON or invalid string list.");
        return nullptr;
    }

    // Create the jobjectArray for strings
    jobjectArray result = env->NewObjectArray(size, env->FindClass("java/lang/String"), nullptr);
    if (result == nullptr) {
        throw_java_exception(env, "java/lang/OutOfMemoryError", "Failed to allocate memory for jobjectArray.");
        return nullptr;
    }

    // Fill the jobjectArray with the parsed strings
    for (size_t i = 0; i < size; i++) {
        jstring java_str = env->NewStringUTF(str_array[i]);
        env->SetObjectArrayElement(result, i, java_str);
        env->DeleteLocalRef(java_str);  // Clean up the string reference
    }

    // Clean up allocated memory for the array
    delete[] str_array;

    return result;
}

JNIEXPORT jdoubleArray JNICALL Java_JavaParseModule_desDoubleList(JNIEnv* env, jclass clazz, jstring arg) {
    // Convert jstring to C++ string
    const char* json_str = env->GetStringUTFChars(arg, nullptr);

    // Parse the JSON string using the existing des_src_double_list function
    size_t size = 0;
    double* double_array = des_src_double_list(json_str, &size);

    // Release the jstring memory
    env->ReleaseStringUTFChars(arg, json_str);

    // Check if the des_src_double_list function failed
    if (!double_array) {
        throw_java_exception(env, "java/lang/IllegalArgumentException", "Error parsing JSON or invalid double list.");
        return nullptr;
    }

    // Create the jdoubleArray to hold the values
    jdoubleArray result = env->NewDoubleArray(size);
    if (result == nullptr) {
        delete[] double_array;  // Free the allocated memory if allocation of jdoubleArray fails
        throw_java_exception(env, "java/lang/OutOfMemoryError", "Failed to allocate memory for jdoubleArray.");
        return nullptr;
    }

    // Fill the jdoubleArray with the parsed values
    env->SetDoubleArrayRegion(result, 0, size, double_array);

    // Free the memory allocated for the C++ array
    delete[] double_array;

    return result;
}
JNIEXPORT jboolean JNICALL Java_JavaParseModule_desBool(JNIEnv* env, jclass clazz, jstring arg) {
    // Convert jstring to C++ string
    const char* json_str = env->GetStringUTFChars(arg, nullptr);

    // Parse the JSON string using the existing des_src_bool function
    bool value = false;
    if (!des_src_bool(json_str, &value)) {
        env->ReleaseStringUTFChars(arg, json_str);
        throw_java_exception(env, "java/lang/IllegalArgumentException", "Error parsing JSON or invalid boolean.");
        return JNI_FALSE;
    }

    // Release the jstring memory
    env->ReleaseStringUTFChars(arg, json_str);

    return value ? JNI_TRUE : JNI_FALSE;
}
JNIEXPORT jdouble JNICALL Java_JavaParseModule_desDouble(JNIEnv* env, jclass clazz, jstring arg) {
    // Convert jstring to C++ string
    const char* json_str = env->GetStringUTFChars(arg, nullptr);

    // Parse the JSON string using the existing des_src_double function
    double value = 0.0;
    if (!des_src_double(json_str, &value)) {
        env->ReleaseStringUTFChars(arg, json_str);
        throw_java_exception(env, "java/lang/IllegalArgumentException", "Error parsing JSON or invalid double.");
        return 0.0;
    }

    // Release the jstring memory
    env->ReleaseStringUTFChars(arg, json_str);

    return value;
}

JNIEXPORT jintArray JNICALL Java_JavaParseModule_desTreeList(JNIEnv* env, jclass clazz, jstring arg) {
    // Convert jstring to C++ string
    const char* json_str = env->GetStringUTFChars(arg, nullptr);

    // Parse the JSON string using the existing des_src_tree_list function
    size_t size = 0;
    int* tree_array = des_src_tree_list(json_str, &size);

    // Release the jstring memory
    env->ReleaseStringUTFChars(arg, json_str);

    // Check if the des_src_tree_list function failed
    if (!tree_array) {
        throw_java_exception(env, "java/lang/IllegalArgumentException", "Error parsing JSON or invalid tree list.");
        return nullptr;
    }

    // Create the jintArray to hold the integers
    jintArray result = env->NewIntArray(size);
    if (result == nullptr) {
        delete[] tree_array;  // Free the allocated memory if allocation of jintArray fails
        throw_java_exception(env, "java/lang/OutOfMemoryError", "Failed to allocate memory for jintArray.");
        return nullptr;
    }

    // Fill the jintArray with the parsed values
    env->SetIntArrayRegion(result, 0, size, tree_array);

    // Free the memory allocated for the C++ array
    delete[] tree_array;

    return result;
}

JNIEXPORT jstring JNICALL Java_JavaParseModule_serInt(JNIEnv* env, jclass clazz, jint value) {
    // Serialize the int value using the existing ser_src_int function
    char* result_str = ser_src_int(value);

    // Check if serialization failed
    if (!result_str) {
        throw_java_exception(env, "java/lang/IllegalArgumentException", "Error serializing int.");
        return nullptr;
    }

    // Convert C string to jstring and return
    jstring result = env->NewStringUTF(result_str);

    // Clean up the allocated C string
    delete[] result_str;

    return result;
}

JNIEXPORT jstring JNICALL Java_JavaParseModule_serLong(JNIEnv* env, jclass clazz, jlong value) {
    // Serialize the long value using the existing ser_src_long function
    char* result_str = ser_src_long(value);

    // Check if serialization failed
    if (!result_str) {
        throw_java_exception(env, "java/lang/IllegalArgumentException", "Error serializing long.");
        return nullptr;
    }

    // Convert C string to jstring and return
    jstring result = env->NewStringUTF(result_str);

    // Clean up the allocated C string
    delete[] result_str;

    return result;
}

JNIEXPORT jstring JNICALL Java_JavaParseModule_serBool(JNIEnv* env, jclass clazz, jboolean value) {
    // Serialize the boolean value using the existing ser_src_bool function
    char* result_str = ser_src_bool(value == JNI_TRUE);

    // Check if serialization failed
    if (!result_str) {
        throw_java_exception(env, "java/lang/IllegalArgumentException", "Error serializing boolean.");
        return nullptr;
    }

    // Convert C string to jstring and return
    jstring result = env->NewStringUTF(result_str);

    // Clean up the allocated C string
    delete[] result_str;

    return result;
}

JNIEXPORT jstring JNICALL Java_JavaParseModule_serString(JNIEnv* env, jclass clazz, jstring value) {
    // Convert jstring to C string
    const char* input_str = env->GetStringUTFChars(value, nullptr);

    // Serialize the string using the existing ser_src_string function
    char* result_str = ser_src_string(input_str);

    // Release the jstring memory
    env->ReleaseStringUTFChars(value, input_str);

    // Check if serialization failed
    if (!result_str) {
        throw_java_exception(env, "java/lang/IllegalArgumentException", "Error serializing string.");
        return nullptr;
    }

    // Convert C string to jstring and return
    jstring result = env->NewStringUTF(result_str);

    // Clean up the allocated C string
    delete[] result_str;

    return result;
}

JNIEXPORT jstring JNICALL Java_JavaParseModule_serIntList(JNIEnv* env, jclass clazz, jintArray value) {
    if (value == nullptr) {
        // Directly return the string "[]"
        return env->NewStringUTF("[]");
    }
    // Get the length of the jintArray
    jsize size = env->GetArrayLength(value);

    // Create a C++ array to hold the integers
    jint* values = env->GetIntArrayElements(value, nullptr);

    // Serialize the int array using the existing ser_src_int_list function
    char* result_str = ser_src_int_list(values, size);

    // Release the jintArray memory
    env->ReleaseIntArrayElements(value, values, 0);

    // Check if serialization failed
    if (!result_str) {
        throw_java_exception(env, "java/lang/IllegalArgumentException", "Error serializing int list.");
        return nullptr;
    }

    // Convert C string to jstring and return
    jstring result = env->NewStringUTF(result_str);

    // Clean up the allocated C string
    delete[] result_str;

    return result;
}

JNIEXPORT jstring JNICALL Java_JavaParseModule_serLongList(JNIEnv* env, jclass clazz, jlongArray value) {
    if (value == nullptr) {
        // Directly return the string "[]"
        return env->NewStringUTF("[]");
    }
    // Get the length of the jlongArray
    jsize size = env->GetArrayLength(value);

    // Create a C++ array to hold the long integers
    jlong* values = env->GetLongArrayElements(value, nullptr);

    // Serialize the long array using the existing ser_src_long_list function
    char* result_str = ser_src_long_list(reinterpret_cast<long long*>(values), size);

    // Release the jlongArray memory
    env->ReleaseLongArrayElements(value, values, 0);

    // Check if serialization failed
    if (!result_str) {
        throw_java_exception(env, "java/lang/IllegalArgumentException", "Error serializing long list.");
        return nullptr;
    }

    // Convert C string to jstring and return
    jstring result = env->NewStringUTF(result_str);

    // Clean up the allocated C string
    delete[] result_str;

    return result;
}

JNIEXPORT jstring JNICALL Java_JavaParseModule_serDouble(JNIEnv* env, jclass clazz, jdouble value) {
    // Serialize the double value using the existing ser_src_double function
    char* result_str = ser_src_double(value);

    // Check if serialization failed
    if (!result_str) {
        throw_java_exception(env, "java/lang/IllegalArgumentException", "Error serializing double.");
        return nullptr;
    }

    // Convert C string to jstring and return
    jstring result = env->NewStringUTF(result_str);

    // Clean up the allocated C string
    delete[] result_str;

    return result;
}
JNIEXPORT jstring JNICALL Java_JavaParseModule_serDoubleList(JNIEnv* env, jclass clazz, jdoubleArray value) {
    if (value == nullptr) {
        // Directly return the string "[]"
        return env->NewStringUTF("[]");
    }
    // Get the length of the jdoubleArray
    jsize size = env->GetArrayLength(value);

    // Create a C++ array to hold the double values
    jdouble* values = env->GetDoubleArrayElements(value, nullptr);

    // Serialize the double array using the existing ser_src_double_list function
    char* result_str = ser_src_double_list(values, size);

    // Release the jdoubleArray memory
    env->ReleaseDoubleArrayElements(value, values, 0);

    // Check if serialization failed
    if (!result_str) {
        throw_java_exception(env, "java/lang/IllegalArgumentException", "Error serializing double list.");
        return nullptr;
    }

    // Convert C string to jstring and return
    jstring result = env->NewStringUTF(result_str);

    // Clean up the allocated C string
    delete[] result_str;

    return result;
}
JNIEXPORT jstring JNICALL Java_JavaParseModule_serIntListList(JNIEnv* env, jclass clazz, jobjectArray value) {
    if (value == nullptr) {
        // Directly return the string "[]"
        return env->NewStringUTF("[]");
    }
    // Get the length of the jobjectArray (int[] array)
    jsize size = env->GetArrayLength(value);

    // Create a C++ array to hold the values (pointer to arrays of int)
    int** values = new int*[size];
    size_t* cols = new size_t[size];

    // Iterate over the jobjectArray to extract the inner jintArray
    for (jsize i = 0; i < size; ++i) {
        // Get the inner array from the jobjectArray
        jintArray inner_array = (jintArray)env->GetObjectArrayElement(value, i);

        // Get the length of the inner jintArray
        jsize inner_size = env->GetArrayLength(inner_array);
        cols[i] = inner_size;

        // Allocate memory for the C++ array and copy the elements
        jint* inner_values = new jint[inner_size];
        env->GetIntArrayRegion(inner_array, 0, inner_size, inner_values);

        // Assign the values to the 2D array
        values[i] = inner_values;

        // Release the reference to the inner jintArray (do not release elements since we already copied them)
        env->DeleteLocalRef(inner_array);
    }

    // Serialize the 2D int array using the existing ser_src_int_list_list function
    char* result_str = ser_src_int_list_list((const int**)values, size, cols);

    // Free the memory allocated for the 2D array and the columns array
    for (jsize i = 0; i < size; ++i) {
        delete[] values[i];  // Free each row's allocated memory
    }
    delete[] values;
    delete[] cols;

    // Check if serialization failed
    if (!result_str) {
        throw_java_exception(env, "java/lang/IllegalArgumentException", "Error serializing int list list.");
        return nullptr;
    }

    // Convert C string to jstring and return
    jstring result = env->NewStringUTF(result_str);

    // Clean up the allocated C string
    delete[] result_str;

    return result;
}


JNIEXPORT jstring JNICALL Java_JavaParseModule_serStringList(JNIEnv* env, jclass clazz, jobjectArray value) {
    if (value == nullptr) {
        // Directly return the string "[]"
        return env->NewStringUTF("[]");
    }

    // Get the length of the jobjectArray
    jsize size = env->GetArrayLength(value);

    // Create a C++ array to hold the string values
    const char** values = new const char*[size];

    for (jsize i = 0; i < size; ++i) {
        jstring str = (jstring)env->GetObjectArrayElement(value, i);
        const char* str_value = env->GetStringUTFChars(str, nullptr);
        values[i] = str_value;
        env->ReleaseStringUTFChars(str, str_value);
    }

    // Serialize the string array using the existing ser_src_string_list function
    char* result_str = ser_src_string_list(values, size);

    // Free the memory allocated for the array
    delete[] values;

    // Check if serialization failed
    if (!result_str) {
        throw_java_exception(env, "java/lang/IllegalArgumentException", "Error serializing string list.");
        return nullptr;
    }

    // Convert C string to jstring and return
    jstring result = env->NewStringUTF(result_str);

    // Clean up the allocated C string
    delete[] result_str;

    return result;
}
JNIEXPORT jstring JNICALL Java_JavaParseModule_serBoolList(JNIEnv* env, jclass clazz, jbooleanArray value) {
    if (value == nullptr) {
        // Directly return the string "[]"
        return env->NewStringUTF("[]");
    }
    // Get the length of the jbooleanArray
    jsize size = env->GetArrayLength(value);

    // Create a C++ array to hold the boolean values
    jboolean* values = env->GetBooleanArrayElements(value, nullptr);

    // Serialize the boolean array using the existing ser_src_bool_list function
    char* result_str = ser_src_bool_list(reinterpret_cast<bool*>(values), size);

    // Release the jbooleanArray memory
    env->ReleaseBooleanArrayElements(value, values, 0);

    // Check if serialization failed
    if (!result_str) {
        throw_java_exception(env, "java/lang/IllegalArgumentException", "Error serializing boolean list.");
        return nullptr;
    }

    // Convert C string to jstring and return
    jstring result = env->NewStringUTF(result_str);

    // Clean up the allocated C string
    delete[] result_str;

    return result;
}
JNIEXPORT jstring JNICALL Java_JavaParseModule_serTreeList(JNIEnv* env, jclass clazz, jobjectArray value) {
    if (value == nullptr) {
        // Directly return the string "[]"
        return env->NewStringUTF("[]");
    }
    // Get the length of the jobjectArray
    jsize size = env->GetArrayLength(value);

    // Create a C++ array to hold the values (pointer to arrays of int)
    int* values = new int[size];

    for (jsize i = 0; i < size; ++i) {
        jintArray inner_array = (jintArray)env->GetObjectArrayElement(value, i);
        jsize inner_size = env->GetArrayLength(inner_array);
        jint* inner_values = env->GetIntArrayElements(inner_array, nullptr);

        values[i] = inner_values[0]; // Assuming that the first element represents the value to serialize

        env->ReleaseIntArrayElements(inner_array, inner_values, 0);
    }

    // Serialize the tree list using the existing ser_src_tree_list function
    char* result_str = ser_src_tree_list(values, size);

    // Free the memory allocated for the array
    delete[] values;

    // Check if serialization failed
    if (!result_str) {
        throw_java_exception(env, "java/lang/IllegalArgumentException", "Error serializing tree list.");
        return nullptr;
    }

    // Convert C string to jstring and return
    jstring result = env->NewStringUTF(result_str);

    // Clean up the allocated C string
    delete[] result_str;

    return result;
}
