/* DO NOT EDIT THIS FILE - it is machine generated */
#include <jni.h>
/* Header for class JavaParseModule */

#ifndef _Included_JavaParseModule
#define _Included_JavaParseModule
#ifdef __cplusplus
extern "C" {
#endif
/*
 * Class:     JavaParseModule
 * Method:    desIntList
 * Signature: (Ljava/lang/String;)[I
 */
JNIEXPORT jintArray JNICALL Java_JavaParseModule_desIntList
  (JNIEnv *, jobject, jstring);

/*
 * Class:     JavaParseModule
 * Method:    desLongList
 * Signature: (Ljava/lang/String;)[J
 */
JNIEXPORT jlongArray JNICALL Java_JavaParseModule_desLongList
  (JNIEnv *, jobject, jstring);

/*
 * Class:     JavaParseModule
 * Method:    desBoolList
 * Signature: (Ljava/lang/String;)[Z
 */
JNIEXPORT jbooleanArray JNICALL Java_JavaParseModule_desBoolList
  (JNIEnv *, jobject, jstring);

/*
 * Class:     JavaParseModule
 * Method:    desInt
 * Signature: (Ljava/lang/String;)I
 */
JNIEXPORT jint JNICALL Java_JavaParseModule_desInt
  (JNIEnv *, jobject, jstring);

/*
 * Class:     JavaParseModule
 * Method:    desLong
 * Signature: (Ljava/lang/String;)J
 */
JNIEXPORT jlong JNICALL Java_JavaParseModule_desLong
  (JNIEnv *, jobject, jstring);

/*
 * Class:     JavaParseModule
 * Method:    desString
 * Signature: (Ljava/lang/String;)Ljava/lang/String;
 */
JNIEXPORT jstring JNICALL Java_JavaParseModule_desString
  (JNIEnv *, jobject, jstring);

/*
 * Class:     JavaParseModule
 * Method:    desIntListList
 * Signature: (Ljava/lang/String;)[[I
 */
JNIEXPORT jobjectArray JNICALL Java_JavaParseModule_desIntListList
  (JNIEnv *, jobject, jstring);

/*
 * Class:     JavaParseModule
 * Method:    desStringList
 * Signature: (Ljava/lang/String;)[Ljava/lang/String;
 */
JNIEXPORT jobjectArray JNICALL Java_JavaParseModule_desStringList
  (JNIEnv *, jobject, jstring);

/*
 * Class:     JavaParseModule
 * Method:    desDoubleList
 * Signature: (Ljava/lang/String;)[D
 */
JNIEXPORT jdoubleArray JNICALL Java_JavaParseModule_desDoubleList
  (JNIEnv *, jobject, jstring);

/*
 * Class:     JavaParseModule
 * Method:    desBool
 * Signature: (Ljava/lang/String;)Z
 */
JNIEXPORT jboolean JNICALL Java_JavaParseModule_desBool
  (JNIEnv *, jobject, jstring);

/*
 * Class:     JavaParseModule
 * Method:    desDouble
 * Signature: (Ljava/lang/String;)D
 */
JNIEXPORT jdouble JNICALL Java_JavaParseModule_desDouble
  (JNIEnv *, jobject, jstring);

/*
 * Class:     JavaParseModule
 * Method:    desTreeList
 * Signature: (Ljava/lang/String;)[I
 */
JNIEXPORT jintArray JNICALL Java_JavaParseModule_desTreeList
  (JNIEnv *, jobject, jstring);

/*
 * Class:     JavaParseModule
 * Method:    serInt
 * Signature: (I)Ljava/lang/String;
 */
JNIEXPORT jstring JNICALL Java_JavaParseModule_serInt
  (JNIEnv *, jobject, jint);

/*
 * Class:     JavaParseModule
 * Method:    serLong
 * Signature: (J)Ljava/lang/String;
 */
JNIEXPORT jstring JNICALL Java_JavaParseModule_serLong
  (JNIEnv *, jobject, jlong);

/*
 * Class:     JavaParseModule
 * Method:    serBool
 * Signature: (Z)Ljava/lang/String;
 */
JNIEXPORT jstring JNICALL Java_JavaParseModule_serBool
  (JNIEnv *, jobject, jboolean);

/*
 * Class:     JavaParseModule
 * Method:    serString
 * Signature: (Ljava/lang/String;)Ljava/lang/String;
 */
JNIEXPORT jstring JNICALL Java_JavaParseModule_serString
  (JNIEnv *, jobject, jstring);

/*
 * Class:     JavaParseModule
 * Method:    serIntList
 * Signature: ([I)Ljava/lang/String;
 */
JNIEXPORT jstring JNICALL Java_JavaParseModule_serIntList
  (JNIEnv *, jobject, jintArray);

/*
 * Class:     JavaParseModule
 * Method:    serLongList
 * Signature: ([J)Ljava/lang/String;
 */
JNIEXPORT jstring JNICALL Java_JavaParseModule_serLongList
  (JNIEnv *, jobject, jlongArray);

/*
 * Class:     JavaParseModule
 * Method:    serDouble
 * Signature: (D)Ljava/lang/String;
 */
JNIEXPORT jstring JNICALL Java_JavaParseModule_serDouble
  (JNIEnv *, jobject, jdouble);

/*
 * Class:     JavaParseModule
 * Method:    serDoubleList
 * Signature: ([D)Ljava/lang/String;
 */
JNIEXPORT jstring JNICALL Java_JavaParseModule_serDoubleList
  (JNIEnv *, jobject, jdoubleArray);

/*
 * Class:     JavaParseModule
 * Method:    serIntListList
 * Signature: ([Ljava/lang/Object;)Ljava/lang/String;
 */
JNIEXPORT jstring JNICALL Java_JavaParseModule_serIntListList
  (JNIEnv *, jobject, jobjectArray);

/*
 * Class:     JavaParseModule
 * Method:    serStringList
 * Signature: ([Ljava/lang/String;)Ljava/lang/String;
 */
JNIEXPORT jstring JNICALL Java_JavaParseModule_serStringList
  (JNIEnv *, jobject, jobjectArray);

/*
 * Class:     JavaParseModule
 * Method:    serBoolList
 * Signature: ([Z)Ljava/lang/String;
 */
JNIEXPORT jstring JNICALL Java_JavaParseModule_serBoolList
  (JNIEnv *, jobject, jbooleanArray);

/*
 * Class:     JavaParseModule
 * Method:    serTreeList
 * Signature: ([I)Ljava/lang/String;
 */
JNIEXPORT jstring JNICALL Java_JavaParseModule_serTreeList
  (JNIEnv *, jobject, jintArray);

#ifdef __cplusplus
}
#endif
#endif