#ifndef CPP_PARSE_MODULE_H
#define CPP_PARSE_MODULE_H

#include <stddef.h>  // 用于 size_t
#include <vector>
#include <string>

#ifdef __cplusplus
extern "C" {
#endif

// 反序列化函数，返回C++ STL容器
std::vector<int> des_int_list(const char* json_str);
int des_int(const char* json_str);
long long des_long(const char* json_str);
bool des_bool(const char* json_str);
std::string des_string(const char* json_str);
std::vector<long long> des_long_list(const char* json_str);
std::vector<std::vector<int>> des_int_list_list(const char* json_str);
std::vector<std::string> des_string_list(const char* json_str);
std::vector<bool> des_bool_list(const char* json_str);
double des_double(const char* json_str);
std::vector<double> des_double_list(const char* json_str);
std::vector<int> des_tree_list(const char* json_str);

// 序列化函数，返回char*类型
char* ser_int(int value);
char* ser_long(long long value);
char* ser_bool(bool value);
char* ser_string(std::string value);
char* ser_int_list(const std::vector<int>& values);
char* ser_long_list(const std::vector<long long>& values);
char* ser_int_list_list(const std::vector<std::vector<int>>& values);
char* ser_string_list(const std::vector<std::string>& values);
char* ser_bool_list(const std::vector<bool>& values);
char* ser_double(double value);
char* ser_double_list(const std::vector<double>& values);
char* ser_tree_list(const std::vector<int>& values);

#ifdef __cplusplus
}
#endif

#endif  // CPP_PARSE_MODULE_H

// g++ -shared -o libcpp_parse_module.so -fPIC cpp_parse_module.cpp rapidjson_helper.cpp
// g++ -o main main.cpp -L. -lcpp_parse_module -Wl,-rpath=.