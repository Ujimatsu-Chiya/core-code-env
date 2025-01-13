#ifndef C_PARSE_MODULE_H
#define C_PARSE_MODULE_H

#include <stddef.h>  // 用于 size_t
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

int des_int(char* json_str);
long long des_long(char* json_str);
bool des_bool(char* json_str);
char* des_string(char* json_str);
int* des_int_list(char* json_str, size_t* out_size);
long long* des_long_list(char* json_str, size_t* out_size);
int** des_int_list_list(char* json_str, size_t* rows, size_t** cols);
char** des_string_list(char* json_str, size_t* out_size);
bool* des_bool_list(char* json_str, size_t* out_size);
double des_double(char* json_str);
double* des_double_list(char* json_str, size_t* out_size);
int* des_tree_list(char* json_str, size_t* out_size);

char* ser_int(int value);
char* ser_long(long long value);
char* ser_bool(bool value);
char* ser_string(char* value);
char* ser_int_list(int* values, size_t size);
char* ser_long_list(long long* values, size_t size);
char* ser_int_list_list(int** values, size_t rows, size_t* cols);
char* ser_string_list(char** values, size_t size);
char* ser_bool_list(bool* values, size_t size);
char* ser_double(double value);
char* ser_double_list(double* values, size_t size);
char* ser_tree_list(int* values, size_t size);

void delete_int_list(int* list);
void delete_bool_list(bool* list);
void delete_long_list(long long* list);
void delete_double_list(double* list);
void delete_string(char* list);
void delete_int_list_list(int** list, size_t rows);
void delete_string_list(char** list, size_t size);
void delete_size_t_list(size_t* list);


#ifdef __cplusplus
}
#endif

#endif  // C_PARSE_MODULE_H
