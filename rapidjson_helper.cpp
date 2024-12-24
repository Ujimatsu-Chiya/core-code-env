#include "rapidjson_helper.h"
#include <cstdlib>
#include <rapidjson/document.h>
#include <rapidjson/writer.h>
#include <rapidjson/stringbuffer.h>
#include <climits>

using namespace rapidjson;

// 解析JSON字符串并返回一个int数组，动态分配内存
int* des_src_int_list(const char* json_str, size_t* out_size) {
    // 使用RapidJSON解析JSON字符串
    Document doc;
    doc.Parse(json_str);

    // 检查解析是否有错误
    if (doc.HasParseError()) {
        return nullptr;  // 返回nullptr表示解析失败
    }

    // 检查是否是一个有效的数组
    if (!doc.IsArray()) {
        return nullptr;  // 返回nullptr表示输入不是有效的JSON数组
    }

    // 获取数组的大小
    size_t size = doc.Size();
    *out_size = size;

    // 动态分配int数组来存储解析的整数
    int* int_array = new(std::nothrow) int[size];
    if (!int_array) {
        return nullptr;  // 如果内存分配失败，返回nullptr
    }

    // 遍历JSON数组并提取整数值
    for (size_t i = 0; i < size; i++) {
        if (doc[i].IsInt()) {
            int_array[i] = doc[i].GetInt();  // 将整数存入数组
        } else {
            delete[] int_array;  // 如果遇到非整数，释放内存
            return nullptr;
        }
    }

    return int_array;  // 返回解析后的int数组
}

// 解析JSON字符串并返回一个long long数组，动态分配内存
long long* des_src_long_list(const char* json_str, size_t* out_size) {
    // 使用RapidJSON解析JSON字符串
    Document doc;
    doc.Parse(json_str);

    // 检查解析是否有错误
    if (doc.HasParseError()) {
        return nullptr;  // 返回nullptr表示解析失败
    }

    // 检查是否是一个有效的数组
    if (!doc.IsArray()) {
        return nullptr;  // 返回nullptr表示输入不是有效的JSON数组
    }

    // 获取数组的大小
    size_t size = doc.Size();
    *out_size = size;

    // 动态分配long long数组来存储解析的整数
    long long* long_array = new(std::nothrow) long long[size];
    if (!long_array) {
        return nullptr;  // 如果内存分配失败，返回nullptr
    }

    // 遍历JSON数组并提取long long值
    for (size_t i = 0; i < size; i++) {
        if (doc[i].IsInt64()) {
            long_array[i] = doc[i].GetInt64();  // 将long long整数存入数组
        } else {
            delete[] long_array;  // 如果遇到非long long整数，释放内存
            return nullptr;
        }
    }

    return long_array;  // 返回解析后的long long数组
}

// 解析JSON字符串并返回一个布尔值
bool des_src_bool(const char* json_str, bool* out_value) {
    // 使用RapidJSON解析JSON字符串
    Document doc;
    doc.Parse(json_str);

    // 检查解析是否有错误
    if (doc.HasParseError()) {
        return false;  // 返回false表示解析失败
    }

    // 检查是否是一个有效的布尔值
    if (!doc.IsBool()) {
        return false;  // 返回false表示输入不是布尔值
    }

    // 提取布尔值
    *out_value = doc.GetBool();

    return true;  // 返回true表示解析成功
}

// 解析JSON字符串并返回一个int值
bool des_src_int(const char* json_str, int* out_value) {
    // 使用RapidJSON解析JSON字符串
    Document doc;
    doc.Parse(json_str);

    // 检查解析是否有错误
    if (doc.HasParseError()) {
        return false;  // 返回false表示解析失败
    }

    // 检查是否是一个有效的int值
    if (!doc.IsInt()) {
        return false;  // 返回false表示输入不是int值
    }

    // 提取int值
    *out_value = doc.GetInt();

    return true;  // 返回true表示解析成功
}

// 解析JSON字符串并返回一个long long值
bool des_src_long(const char* json_str, long long* out_value) {
    // 使用RapidJSON解析JSON字符串
    Document doc;
    doc.Parse(json_str);

    // 检查解析是否有错误
    if (doc.HasParseError()) {
        return false;  // 返回false表示解析失败
    }

    // 检查是否是一个有效的long long值
    if (!doc.IsInt64()) {
        return false;  // 返回false表示输入不是long long值
    }

    // 提取long long值
    *out_value = doc.GetInt64();

    return true;  // 返回true表示解析成功
}

// 解析JSON字符串并返回一个字符串值
char* des_src_string(const char* json_str) {
    Document doc;
    doc.Parse(json_str);

    if (doc.HasParseError() || !doc.IsString()) {
        return nullptr;  // 返回nullptr表示解析失败
    }

    const char* str = doc.GetString();
    size_t len = strlen(str) + 1;
    char* result = new(std::nothrow) char[len];
    if (!result) {
        return nullptr;  // 如果内存分配失败，返回nullptr
    }
    strncpy(result, str, len);
    return result;  // 返回动态分配的字符串
}

// 解析JSON字符串并返回一个int型二维数组
int** des_src_int_list_list(const char* json_str, size_t* rows, size_t** cols) {
    Document doc;
    doc.Parse(json_str);

    if (doc.HasParseError() || !doc.IsArray()) {
        return nullptr;  // 返回nullptr表示解析失败
    }

    *rows = doc.Size();
    int** out_array = new(std::nothrow) int*[*rows];
    *cols = new(std::nothrow) size_t[*rows];

    if (!out_array || !*cols) {
        delete[] out_array;  // 释放已分配的内存
        delete[] *cols;
        return nullptr;  // 如果内存分配失败，返回nullptr
    }

    for (size_t i = 0; i < *rows; i++) {
        if (!doc[i].IsArray()) {
            delete[] out_array;  // 释放已分配的内存
            delete[] *cols;
            return nullptr;
        }

        (*cols)[i] = doc[i].Size();
        out_array[i] = new(std::nothrow) int[(*cols)[i]];

        if (!out_array[i]) {
            delete[] out_array;  // 释放已分配的内存
            delete[] *cols;
            return nullptr;
        }

        for (size_t j = 0; j < (*cols)[i]; j++) {
            if (!doc[i][j].IsInt()) {
                delete[] out_array;  // 释放已分配的内存
                delete[] *cols;
                return nullptr;
            }
            out_array[i][j] = doc[i][j].GetInt();
        }
    }

    return out_array;  // 返回解析后的二维数组
}

// 解析JSON字符串并返回一个字符串数组
char** des_src_string_list(const char* json_str, size_t* out_size) {
    Document doc;
    doc.Parse(json_str);

    if (doc.HasParseError() || !doc.IsArray()) {
        return nullptr;  // 返回nullptr表示解析失败
    }

    *out_size = doc.Size();
    char** out_array = new(std::nothrow) char*[*out_size];

    if (!out_array) {
        return nullptr;  // 如果内存分配失败，返回nullptr
    }

    for (size_t i = 0; i < *out_size; i++) {
        if (!doc[i].IsString()) {
            delete[] out_array;  // 释放已分配的内存
            return nullptr;
        }
        const char* str = doc[i].GetString();
        size_t len = strlen(str) + 1;
        out_array[i] = new(std::nothrow) char[len];
        if (!out_array[i]) {
            delete[] out_array;  // 释放已分配的内存
            return nullptr;
        }
        strncpy(out_array[i], str, len);
    }

    return out_array;  // 返回解析后的字符串数组
}

// 解析JSON字符串并返回一个布尔数组
bool* des_src_bool_list(const char* json_str, size_t* out_size) {
    Document doc;
    doc.Parse(json_str);

    if (doc.HasParseError() || !doc.IsArray()) {
        return nullptr;  // 返回nullptr表示解析失败
    }

    *out_size = doc.Size();
    bool* out_array = new(std::nothrow) bool[*out_size];

    if (!out_array) {
        return nullptr;  // 如果内存分配失败，返回nullptr
    }

    for (size_t i = 0; i < *out_size; i++) {
        if (!doc[i].IsBool()) {
            delete[] out_array;  // 释放已分配的内存
            return nullptr;
        }
        out_array[i] = doc[i].GetBool();
    }

    return out_array;  // 返回解析后的布尔数组
}

// 解析JSON字符串并返回一个double值
bool des_src_double(const char* json_str, double* out_value) {
    Document doc;
    doc.Parse(json_str);

    // 检查解析是否有错误
    if (doc.HasParseError()) {
        return false;  // 返回false表示解析失败
    }

    // 检查是否是一个有效的double值
    if (!doc.IsDouble()) {
        return false;  // 返回false表示输入不是double值
    }

    // 提取double值
    *out_value = doc.GetDouble();

    return true;  // 返回true表示解析成功
}

// 解析JSON字符串并返回一个double数组
double* des_src_double_list(const char* json_str, size_t* out_size) {
    Document doc;
    doc.Parse(json_str);

    // 检查解析是否有错误，或者JSON不是数组
    if (doc.HasParseError() || !doc.IsArray()) {
        return nullptr;  // 返回nullptr表示解析失败
    }

    // 获取数组大小
    *out_size = doc.Size();

    // 动态分配内存来存储double数组
    double* out_array = new(std::nothrow) double[*out_size];
    if (!out_array) {
        return nullptr;  // 如果内存分配失败，返回nullptr
    }

    // 遍历JSON数组并解析每个元素
    for (size_t i = 0; i < *out_size; i++) {
        if (!doc[i].IsDouble()) {  // 检查元素是否是double类型
            delete[] out_array;  // 释放已分配的内存
            return nullptr;      // 返回nullptr表示解析失败
        }
        out_array[i] = doc[i].GetDouble();  // 提取double值
    }

    return out_array;  // 返回解析后的double数组
}

// 解析JSON字符串并返回一个int数组，处理null值
int* des_src_tree_list(const char* json_str, size_t* out_size) {
    Document doc;
    doc.Parse(json_str);

    // 检查解析是否有错误
    if (doc.HasParseError()) {
        return nullptr;  // 返回nullptr表示解析失败
    }

    // 检查是否是一个有效的数组
    if (!doc.IsArray()) {
        return nullptr;  // 返回nullptr表示输入不是有效的JSON数组
    }

    // 获取数组的大小
    size_t size = doc.Size();
    *out_size = size;

    // 动态分配int数组来存储解析的整数
    int* int_array = new(std::nothrow) int[size];
    if (!int_array) {
        return nullptr;  // 如果内存分配失败，返回nullptr
    }

    // 遍历JSON数组并提取整数值
    for (size_t i = 0; i < size; i++) {
        if (doc[i].IsInt()) {
            int_array[i] = doc[i].GetInt();  // 将整数存入数组
        } else if (doc[i].IsNull()) {
            int_array[i] = INT_MIN;  // 如果值为null，存储INT_MIN
        } else {
            delete[] int_array;  // 如果遇到非整数或非null值，释放内存
            return nullptr;
        }
    }

    return int_array;  // 返回解析后的int数组
}

// 解析整数并返回字符串
char* ser_src_int(int value) {
    StringBuffer buffer;
    Writer<StringBuffer> writer(buffer);
    writer.Int(value);

    // 使用new分配内存并复制返回结果
    size_t len = strlen(buffer.GetString()) + 1;
    char* result = new(std::nothrow) char[len];
    if (result) {
        strncpy(result, buffer.GetString(), len);
    }
    return result;
}

// 解析long long并返回字符串
char* ser_src_long(long long value) {
    StringBuffer buffer;
    Writer<StringBuffer> writer(buffer);
    writer.Int64(value);

    // 使用new分配内存并复制返回结果
    size_t len = strlen(buffer.GetString()) + 1;
    char* result = new(std::nothrow) char[len];
    if (result) {
        strncpy(result, buffer.GetString(), len);
    }
    return result;
}

// 解析布尔值并返回字符串
char* ser_src_bool(bool value) {
    StringBuffer buffer;
    Writer<StringBuffer> writer(buffer);
    writer.Bool(value);

    // 使用new分配内存并复制返回结果
    size_t len = strlen(buffer.GetString()) + 1;
    char* result = new(std::nothrow) char[len];
    if (result) {
        strncpy(result, buffer.GetString(), len);
    }
    return result;
}

// 解析字符串并返回字符串
char* ser_src_string(const char* value) {
    StringBuffer buffer;
    Writer<StringBuffer> writer(buffer);
    writer.String(value);

    // 使用new分配内存并复制返回结果
    size_t len = strlen(buffer.GetString()) + 1;
    char* result = new(std::nothrow) char[len];
    if (result) {
        strncpy(result, buffer.GetString(), len);
    }
    return result;
}

// 解析整数数组并返回字符串
char* ser_src_int_list(const int* values, size_t size) {
    StringBuffer buffer;
    Writer<StringBuffer> writer(buffer);
    writer.StartArray();
    for (size_t i = 0; i < size; ++i) {
        writer.Int(values[i]);
    }
    writer.EndArray();

    // 使用new分配内存并复制返回结果
    size_t len = strlen(buffer.GetString()) + 1;
    char* result = new(std::nothrow) char[len];
    if (result) {
        strncpy(result, buffer.GetString(), len);
    }
    return result;
}

// 解析long long数组并返回字符串
char* ser_src_long_list(const long long* values, size_t size) {
    StringBuffer buffer;
    Writer<StringBuffer> writer(buffer);
    writer.StartArray();
    for (size_t i = 0; i < size; ++i) {
        writer.Int64(values[i]);
    }
    writer.EndArray();

    // 使用new分配内存并复制返回结果
    size_t len = strlen(buffer.GetString()) + 1;
    char* result = new(std::nothrow) char[len];
    if (result) {
        strncpy(result, buffer.GetString(), len);
    }
    return result;
}

// 解析二维整数数组并返回字符串
char* ser_src_int_list_list(const int** values, size_t rows, const size_t* cols) {
    StringBuffer buffer;
    Writer<StringBuffer> writer(buffer);
    writer.StartArray();
    for (size_t i = 0; i < rows; ++i) {
        writer.StartArray();
        for (size_t j = 0; j < cols[i]; ++j) {
            writer.Int(values[i][j]);
        }
        writer.EndArray();
    }
    writer.EndArray();

    // 使用new分配内存并复制返回结果
    size_t len = strlen(buffer.GetString()) + 1;
    char* result = new(std::nothrow) char[len];
    if (result) {
        strncpy(result, buffer.GetString(), len);
    }
    return result;
}

// 解析字符串数组并返回字符串
char* ser_src_string_list(const char** values, size_t size) {
    StringBuffer buffer;
    Writer<StringBuffer> writer(buffer);
    writer.StartArray();
    for (size_t i = 0; i < size; ++i) {
        writer.String(values[i]);
    }
    writer.EndArray();

    // 使用new分配内存并复制返回结果
    size_t len = strlen(buffer.GetString()) + 1;
    char* result = new(std::nothrow) char[len];
    if (result) {
        strncpy(result, buffer.GetString(), len);
    }
    return result;
}

// 解析布尔值数组并返回字符串
char* ser_src_bool_list(const bool* values, size_t size) {
    StringBuffer buffer;
    Writer<StringBuffer> writer(buffer);
    writer.StartArray();
    for (size_t i = 0; i < size; ++i) {
        writer.Bool(values[i]);
    }
    writer.EndArray();

    // 使用new分配内存并复制返回结果
    size_t len = strlen(buffer.GetString()) + 1;
    char* result = new(std::nothrow) char[len];
    if (result) {
        strncpy(result, buffer.GetString(), len);
    }
    return result;
}

// 解析double并返回字符串
char* ser_src_double(double value) {
    StringBuffer buffer;
    Writer<StringBuffer> writer(buffer);
    writer.Double(value);

    // 使用new分配内存并复制返回结果
    size_t len = strlen(buffer.GetString()) + 1;
    char* result = new(std::nothrow) char[len];
    if (result) {
        strncpy(result, buffer.GetString(), len);
    }
    return result;
}

// 解析double数组并返回字符串
char* ser_src_double_list(const double* values, size_t size) {
    StringBuffer buffer;
    Writer<StringBuffer> writer(buffer);
    writer.StartArray();
    for (size_t i = 0; i < size; ++i) {
        writer.Double(values[i]);
    }
    writer.EndArray();

    // 使用new分配内存并复制返回结果
    size_t len = strlen(buffer.GetString()) + 1;
    char* result = new(std::nothrow) char[len];
    if (result) {
        strncpy(result, buffer.GetString(), len);
    }
    return result;
}

// 解析整数数组（处理null）并返回字符串
char* ser_src_tree_list(const int* values, size_t size) {
    StringBuffer buffer;
    Writer<StringBuffer> writer(buffer);

    // 开始 JSON 数组
    writer.StartArray();
    
    for (size_t i = 0; i < size; ++i) {
        if (values[i] == INT_MIN) {
            writer.Null();  // 如果值是 INT_MIN，写入 null
        } else {
            writer.Int(values[i]);  // 否则写入整数值
        }
    }

    // 结束 JSON 数组
    writer.EndArray();

    // 使用new分配内存并复制返回结果
    size_t len = strlen(buffer.GetString()) + 1;
    char* result = new(std::nothrow) char[len];
    if (result) {
        strncpy(result, buffer.GetString(), len);
    }
    return result;
}
