#include <stdexcept>  // 用于抛出异常
#include "../rapidjson_helper.h"
#include "c_parse_module.h"

int des_int(const char* json_str) {
    int result;
    // 调用 des_src_int 解析 JSON 字符串为整数
    if (!des_src_int(json_str, &result)) {
        throw std::invalid_argument("Error parsing JSON or invalid integer.");
    }
    return result;
}

long long des_long(const char* json_str) {
    long long result;
    // 调用 des_src_long 解析 JSON 字符串为 long long
    if (!des_src_long(json_str, &result)) {
        throw std::invalid_argument("Error parsing JSON or invalid long long.");
    }
    return result;
}

int des_bool(const char* json_str) {
    bool result;
    // 调用 des_src_bool 解析 JSON 字符串为布尔值
    if (!des_src_bool(json_str, &result)) {
        throw std::invalid_argument("Error parsing JSON or invalid boolean.");
    }
    return result ? 1 : 0;  // 转换布尔值为整数 1 或 0
}

char* des_string(const char* json_str) {
    char* result = des_src_string(json_str);
    // 如果返回的字符串为空，抛出异常
    if (!result) {
        throw std::invalid_argument("Error parsing JSON or invalid string.");
    }
    return result;
}

int* des_int_list(const char* json_str, size_t* out_size) {
    // 调用 des_src_int_list 解析整数列表
    int* result = des_src_int_list(json_str, out_size);
    if (!result) {
        throw std::invalid_argument("Error parsing JSON or invalid integer list.");
    }
    return result;
}

long long* des_long_list(const char* json_str, size_t* out_size) {
    // 调用 des_src_long_list 解析 long long 列表
    long long* result = des_src_long_list(json_str, out_size);
    if (!result) {
        throw std::invalid_argument("Error parsing JSON or invalid long long list.");
    }
    return result;
}

int** des_int_list_list(const char* json_str, size_t* rows, size_t** cols) {
    // 调用 des_src_int_list_list 解析二维整数列表
    int** result = des_src_int_list_list(json_str, rows, cols);
    if (!result) {
        throw std::invalid_argument("Error parsing JSON or invalid integer list list.");
    }
    return result;
}

char** des_string_list(const char* json_str, size_t* out_size) {
    // 调用 des_src_string_list 解析字符串列表
    char** result = des_src_string_list(json_str, out_size);
    if (!result) {
        throw std::invalid_argument("Error parsing JSON or invalid string list.");
    }
    return result;
}

int* des_bool_list(const char* json_str, size_t* out_size) {
    // 调用 des_src_bool_list 解析布尔值列表
    bool* bool_array = des_src_bool_list(json_str, out_size);
    if (!bool_array) {
        throw std::invalid_argument("Error parsing JSON or invalid boolean list.");
    }
    
    // 将 bool 数组转换为 int 数组 (1 或 0)
    int* result = new int[*out_size];
    for (size_t i = 0; i < *out_size; ++i) {
        result[i] = bool_array[i] ? 1 : 0;
    }

    delete[] bool_array;  // 释放原始的 bool 数组
    return result;
}

double des_double(const char* json_str) {
    double result;
    // 调用 des_src_double 解析 double 值
    if (!des_src_double(json_str, &result)) {
        throw std::invalid_argument("Error parsing JSON or invalid double.");
    }
    return result;
}

double* des_double_list(const char* json_str, size_t* out_size) {
    // 调用 des_src_double_list 解析 double 数组
    double* result = des_src_double_list(json_str, out_size);
    if (!result) {
        throw std::invalid_argument("Error parsing JSON or invalid double list.");
    }
    return result;
}

int* des_tree_list(const char* json_str, size_t* out_size) {
    // 调用 des_src_tree_list 解析树形整数列表
    int* result = des_src_tree_list(json_str, out_size);
    if (!result) {
        throw std::invalid_argument("Error parsing JSON or invalid tree list.");
    }
    return result;
}

#include <stdexcept>  // 用于抛出异常

char* ser_int(int value) {
    // 调用 ser_src_int 进行整数序列化
    char* result = ser_src_int(value);
    if (!result) {
        throw std::invalid_argument("Error serializing integer.");
    }
    return result;
}

char* ser_long(long long value) {
    // 调用 ser_src_long 进行 long long 序列化
    char* result = ser_src_long(value);
    if (!result) {
        throw std::invalid_argument("Error serializing long long.");
    }
    return result;
}

char* ser_bool(int value) {
    // 将 int 类型的布尔值转换为 bool 类型
    bool bool_value = (value != 0);
    // 调用 ser_src_bool 进行布尔值序列化
    char* result = ser_src_bool(bool_value);
    if (!result) {
        throw std::invalid_argument("Error serializing boolean.");
    }
    return result;
}

char* ser_string(const char* value) {
    // 调用 ser_src_string 进行字符串序列化
    char* result = ser_src_string(value);
    if (!result) {
        throw std::invalid_argument("Error serializing string.");
    }
    return result;
}

char* ser_int_list(const int* values, size_t size) {
    // 调用 ser_src_int_list 进行整数数组序列化
    char* result = ser_src_int_list(values, size);
    if (!result) {
        throw std::invalid_argument("Error serializing integer list.");
    }
    return result;
}

char* ser_long_list(const long long* values, size_t size) {
    // 调用 ser_src_long_list 进行 long long 数组序列化
    char* result = ser_src_long_list(values, size);
    if (!result) {
        throw std::invalid_argument("Error serializing long long list.");
    }
    return result;
}

char* ser_int_list_list(const int** values, size_t rows, const size_t* cols) {
    // 调用 ser_src_int_list_list 进行二维整数数组序列化
    char* result = ser_src_int_list_list(values, rows, cols);
    if (!result) {
        throw std::invalid_argument("Error serializing integer list list.");
    }
    return result;
}

char* ser_string_list(const char** values, size_t size) {
    // 调用 ser_src_string_list 进行字符串数组序列化
    char* result = ser_src_string_list(values, size);
    if (!result) {
        throw std::invalid_argument("Error serializing string list.");
    }
    return result;
}

char* ser_bool_list(const int* values, size_t size) {
    // 将 int 类型的布尔值数组转换为 bool 数组
    bool* bool_values = new bool[size];
    for (size_t i = 0; i < size; ++i) {
        bool_values[i] = (values[i] != 0);
    }
    // 调用 ser_src_bool_list 进行布尔值数组序列化
    char* result = ser_src_bool_list(bool_values, size);
    delete[] bool_values;  // 释放临时的布尔值数组
    if (!result) {
        throw std::invalid_argument("Error serializing boolean list.");
    }
    return result;
}

char* ser_double(double value) {
    // 调用 ser_src_double 进行 double 序列化
    char* result = ser_src_double(value);
    if (!result) {
        throw std::invalid_argument("Error serializing double.");
    }
    return result;
}

char* ser_double_list(const double* values, size_t size) {
    // 调用 ser_src_double_list 进行 double 数组序列化
    char* result = ser_src_double_list(values, size);
    if (!result) {
        throw std::invalid_argument("Error serializing double list.");
    }
    return result;
}

char* ser_tree_list(const int* values, size_t size) {
    // 调用 ser_src_tree_list 进行树形整数列表序列化
    char* result = ser_src_tree_list(values, size);
    if (!result) {
        throw std::invalid_argument("Error serializing tree list.");
    }
    return result;
}

void delete_int_list(int* list) {
    if (list) {
        delete[] list;
    }
}

void delete_long_list(long long* list){
    if (list) {
        delete[] list;
    }
}

void delete_double_list(double* list) {
    if (list) {
        delete[] list;
    }
}

void delete_string(char* list) {
    if (list) {
        delete[] list;
    }
}

void delete_int_list_list(int** list, size_t rows) {
    if (list) {
        for (size_t i = 0; i < rows; ++i) {
            delete[] list[i];  // 释放每一行
        }
        delete[] list;  // 释放指向行的指针数组
    }
}

 void delete_string_list(char** list, size_t size) {
    if (list) {
        for (size_t i = 0; i < size; ++i) {
            delete[] list[i];  // 释放每个字符串
        }
        delete[] list;  // 释放指向字符串的指针数组
    }
}