#ifndef CPP_PARSE_MODULE_H
#define CPP_PARSE_MODULE_H

// C++ wrappers around rapidjson_helper C APIs.
// Public interfaces use std::string/std::vector and hide raw memory handling.
#include <string>
#include <vector>

// Deserialization helpers.
std::vector<int> des_int_list(const std::string &json_str);
int des_int(const std::string &json_str);
long long des_long(const std::string &json_str);
bool des_bool(const std::string &json_str);
std::string des_string(const std::string &json_str);
std::vector<long long> des_long_list(const std::string &json_str);
std::vector<std::vector<int>> des_int_list_list(const std::string &json_str);
std::vector<std::string> des_string_list(const std::string &json_str);
std::vector<bool> des_bool_list(const std::string &json_str);
double des_double(const std::string &json_str);
std::vector<double> des_double_list(const std::string &json_str);
std::vector<int> des_tree_list(const std::string &json_str);

// For system-design input: each params item stays as raw JSON fragment text.
std::vector<std::vector<std::string>> des_json_value_list_list(const std::string &json_str);

// Serialization helpers.
std::string ser_int(int value);
std::string ser_long(long long value);
std::string ser_bool(bool value);
std::string ser_string(const std::string &value);
std::string ser_int_list(const std::vector<int> &values);
std::string ser_long_list(const std::vector<long long> &values);
std::string ser_int_list_list(const std::vector<std::vector<int>> &values);
std::string ser_string_list(const std::vector<std::string> &values);
std::string ser_bool_list(const std::vector<bool> &values);
std::string ser_double(double value);
std::string ser_double_list(const std::vector<double> &values);
std::string ser_tree_list(const std::vector<int> &values);

#endif
