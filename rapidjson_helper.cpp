#include "rapidjson_helper.h"
#include <stdlib.h>
#include <rapidjson/document.h>

using namespace rapidjson;

// 解析JSON字符串并返回一个int数组，动态分配内存
int* des_src_int_list(const char* json_str, size_t* out_size) {
    // 使用RapidJSON解析JSON字符串
    Document doc;
    doc.Parse(json_str);

    // 检查解析是否有错误
    if (doc.HasParseError()) {
        return NULL;  // 返回NULL表示解析失败
    }

    // 检查是否是一个有效的数组
    if (!doc.IsArray()) {
        return NULL;  // 返回NULL表示输入不是有效的JSON数组
    }

    // 获取数组的大小
    size_t size = doc.Size();
    *out_size = size;

    // 动态分配int数组来存储解析的整数
    int* int_array = (int*)malloc(size * sizeof(int));
    if (!int_array) {
        return NULL;  // 如果内存分配失败，返回NULL
    }

    // 遍历JSON数组并提取整数值
    for (size_t i = 0; i < size; i++) {
        if (doc[i].IsInt()) {
            int_array[i] = doc[i].GetInt();  // 将整数存入数组
        } else {
            free(int_array);  // 如果遇到非整数，释放内存
            return NULL;
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
        return NULL;  // 返回NULL表示解析失败
    }

    // 检查是否是一个有效的数组
    if (!doc.IsArray()) {
        return NULL;  // 返回NULL表示输入不是有效的JSON数组
    }

    // 获取数组的大小
    size_t size = doc.Size();
    *out_size = size;

    // 动态分配long long数组来存储解析的整数
    long long* long_array = (long long*)malloc(size * sizeof(long long));
    if (!long_array) {
        return NULL;  // 如果内存分配失败，返回NULL
    }

    // 遍历JSON数组并提取long long值
    for (size_t i = 0; i < size; i++) {
        if (doc[i].IsInt64()) {
            long_array[i] = doc[i].GetInt64();  // 将long long整数存入数组
        } else {
            free(long_array);  // 如果遇到非long long整数，释放内存
            return NULL;
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
        return NULL;  // 返回NULL表示解析失败
    }

    const char* str = doc.GetString();
    size_t len = strlen(str) + 1;
    char* result = (char*)malloc(len);
    if (!result) {
        return NULL;  // 如果内存分配失败，返回NULL
    }
    strncpy(result, str, len);
    return result;  // 返回动态分配的字符串
}

// 解析JSON字符串并返回一个int型二维数组
int** des_src_int_list_list(const char* json_str, size_t* rows, size_t** cols) {
    Document doc;
    doc.Parse(json_str);

    if (doc.HasParseError() || !doc.IsArray()) {
        return NULL;  // 返回NULL表示解析失败
    }

    *rows = doc.Size();
    int** out_array = (int**)malloc(*rows * sizeof(int*));
    *cols = (size_t*)malloc(*rows * sizeof(size_t));

    if (!out_array || !*cols) {
        return NULL;  // 如果内存分配失败，返回NULL
    }

    for (size_t i = 0; i < *rows; i++) {
        if (!doc[i].IsArray()) {
            return NULL;
        }

        (*cols)[i] = doc[i].Size();
        out_array[i] = (int*)malloc((*cols)[i] * sizeof(int));

        if (!out_array[i]) {
            return NULL;
        }

        for (size_t j = 0; j < (*cols)[i]; j++) {
            if (!doc[i][j].IsInt()) {
                return NULL;
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
        return NULL;  // 返回NULL表示解析失败
    }

    *out_size = doc.Size();
    char** out_array = (char**)malloc(*out_size * sizeof(char*));

    if (!out_array) {
        return NULL;  // 如果内存分配失败，返回NULL
    }

    for (size_t i = 0; i < *out_size; i++) {
        if (!doc[i].IsString()) {
            return NULL;
        }
        const char* str = doc[i].GetString();
        size_t len = strlen(str) + 1;
        out_array[i] = (char*)malloc(len);
        if (!out_array[i]) {
            return NULL;
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
        return NULL;  // 返回NULL表示解析失败
    }

    *out_size = doc.Size();
    bool* out_array = (bool*)malloc(*out_size * sizeof(bool));

    if (!out_array) {
        return NULL;  // 如果内存分配失败，返回NULL
    }

    for (size_t i = 0; i < *out_size; i++) {
        if (!doc[i].IsBool()) {
            return NULL;
        }
        out_array[i] = doc[i].GetBool();
    }

    return out_array;  // 返回解析后的布尔数组
}

bool des_src_double(const char* json_str, double* out_value) {
    // 使用RapidJSON解析JSON字符串
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

double* des_src_double_list(const char* json_str, size_t* out_size) {
    // 使用 RapidJSON 解析 JSON 字符串
    Document doc;
    doc.Parse(json_str);

    // 检查解析是否出错，或者 JSON 不是数组
    if (doc.HasParseError() || !doc.IsArray()) {
        return NULL;  // 返回 NULL 表示解析失败
    }

    // 获取数组大小
    *out_size = doc.Size();

    // 分配内存以存储 double 数组
    double* out_array = (double*)malloc(*out_size * sizeof(double));
    if (!out_array) {
        return NULL;  // 如果内存分配失败，返回 NULL
    }

    // 遍历 JSON 数组并解析每个元素
    for (size_t i = 0; i < *out_size; i++) {
        if (!doc[i].IsDouble()) {  // 检查元素是否是 double 类型
            free(out_array);  // 释放已分配的内存
            return NULL;      // 返回 NULL 表示解析失败
        }
        out_array[i] = doc[i].GetDouble();  // 提取 double 值
    }

    return out_array;  // 返回解析后的 double 数组
}

#include "rapidjson_helper.h"
#include <stdlib.h>
#include <rapidjson/document.h>
#include <rapidjson/writer.h>
#include <rapidjson/stringbuffer.h>

using namespace rapidjson;

char* ser_src_int(int value) {
    StringBuffer buffer;
    Writer<StringBuffer> writer(buffer);
    writer.Int(value);
    return strdup(buffer.GetString());
}

char* ser_src_long(long long value) {
    StringBuffer buffer;
    Writer<StringBuffer> writer(buffer);
    writer.Int64(value);
    return strdup(buffer.GetString());
}

char* ser_src_bool(bool value) {
    StringBuffer buffer;
    Writer<StringBuffer> writer(buffer);
    writer.Bool(value);
    return strdup(buffer.GetString());
}

char* ser_src_string(const char* value) {
    StringBuffer buffer;
    Writer<StringBuffer> writer(buffer);
    writer.String(value);
    return strdup(buffer.GetString());
}

char* ser_src_int_list(const int* values, size_t size) {
    StringBuffer buffer;
    Writer<StringBuffer> writer(buffer);
    writer.StartArray();
    for (size_t i = 0; i < size; ++i) {
        writer.Int(values[i]);
    }
    writer.EndArray();
    return strdup(buffer.GetString());
}

char* ser_src_long_list(const long long* values, size_t size) {
    StringBuffer buffer;
    Writer<StringBuffer> writer(buffer);
    writer.StartArray();
    for (size_t i = 0; i < size; ++i) {
        writer.Int64(values[i]);
    }
    writer.EndArray();
    return strdup(buffer.GetString());
}

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
    return strdup(buffer.GetString());
}

char* ser_src_string_list(const char** values, size_t size) {
    StringBuffer buffer;
    Writer<StringBuffer> writer(buffer);
    writer.StartArray();
    for (size_t i = 0; i < size; ++i) {
        writer.String(values[i]);
    }
    writer.EndArray();
    return strdup(buffer.GetString());
}

char* ser_src_bool_list(const bool* values, size_t size) {
    StringBuffer buffer;
    Writer<StringBuffer> writer(buffer);
    writer.StartArray();
    for (size_t i = 0; i < size; ++i) {
        writer.Bool(values[i]);
    }
    writer.EndArray();
    return strdup(buffer.GetString());
}

char* ser_src_double(double value) {
    StringBuffer buffer;
    Writer<StringBuffer> writer(buffer);
    writer.Double(value);
    return strdup(buffer.GetString());
}

char* ser_src_double_list(const double* values, size_t size) {
    StringBuffer buffer;
    Writer<StringBuffer> writer(buffer);
    writer.StartArray();
    for (size_t i = 0; i < size; ++i) {
        writer.Double(values[i]);
    }
    writer.EndArray();
    return strdup(buffer.GetString());
}
