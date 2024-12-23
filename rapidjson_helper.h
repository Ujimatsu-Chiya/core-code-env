#ifndef RAPIDJSON_HELPER_H
#define RAPIDJSON_HELPER_H

#include <stddef.h>  // 用于 size_t

#ifdef __cplusplus
extern "C" {
#endif

bool des_src_int(const char* json_str, int* out_value);
bool des_src_long(const char* json_str, long long* out_value);
bool des_src_bool(const char* json_str, bool* out_value);
char* des_src_string(const char* json_str);
int* des_src_int_list(const char* json_str, size_t* out_size);
long long* des_src_long_list(const char* json_str, size_t* out_size);
int** des_src_int_list_list(const char* json_str, size_t* rows, size_t** cols);
char** des_src_string_list(const char* json_str, size_t* out_size);
bool* des_src_bool_list(const char* json_str, size_t* out_size);
bool des_src_double(const char* json_str, double* out_value);
double* des_src_double_list(const char* json_str, size_t* out_size);

char* ser_src_int(int value);
char* ser_src_long(long long value);
char* ser_src_bool(bool value);
char* ser_src_string(const char* value);
char* ser_src_int_list(const int* values, size_t size);
char* ser_src_long_list(const long long* values, size_t size);
char* ser_src_int_list_list(const int** values, size_t rows, const size_t* cols);
char* ser_src_string_list(const char** values, size_t size);
char* ser_src_bool_list(const bool* values, size_t size);
char* ser_src_double(double value);
char* ser_src_double_list(const double* values, size_t size);




#ifdef __cplusplus
}
#endif

#endif  // RAPIDJSON_HELPER_H
