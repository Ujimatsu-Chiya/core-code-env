#ifndef RAPIDJSON_HELPER_H
#define RAPIDJSON_HELPER_H

// C-style JSON helper APIs used by language bridges.
// All heap objects returned from this file must be freed by callers.
#include <stddef.h>

#ifdef __cplusplus
extern "C"
{
#endif

    // Scalar deserialization.
    bool des_src_int(const char *json_str, int *out_value);
    bool des_src_long(const char *json_str, long long *out_value);
    bool des_src_bool(const char *json_str, bool *out_value);
    char *des_src_string(const char *json_str);

    // List deserialization.
    int *des_src_int_list(const char *json_str, size_t *out_size);
    long long *des_src_long_list(const char *json_str, size_t *out_size);
    int **des_src_int_list_list(const char *json_str, size_t *rows, size_t **cols);
    char **des_src_string_list(const char *json_str, size_t *out_size);
    bool *des_src_bool_list(const char *json_str, size_t *out_size);
    bool des_src_double(const char *json_str, double *out_value);
    double *des_src_double_list(const char *json_str, size_t *out_size);
    int *des_src_tree_list(const char *json_str, size_t *out_size);

    // Parse a 2D params array where each value is returned as raw JSON text.
    char ***des_src_json_value_list_list(const char *json_str, size_t *rows, size_t **cols);
    void delete_src_json_value_list_list(char ***values, size_t rows, const size_t *cols);

    // Scalar/list serialization to JSON text.
    char *ser_src_int(int value);
    char *ser_src_long(long long value);
    char *ser_src_bool(bool value);
    char *ser_src_string(const char *value);
    char *ser_src_int_list(const int *values, size_t size);
    char *ser_src_long_list(const long long *values, size_t size);
    char *ser_src_int_list_list(const int **values, size_t rows, const size_t *cols);
    char *ser_src_string_list(const char **values, size_t size);
    char *ser_src_bool_list(const bool *values, size_t size);
    char *ser_src_double(double value);
    char *ser_src_double_list(const double *values, size_t size);
    char *ser_src_tree_list(const int *values, size_t size);

#ifdef __cplusplus
}
#endif

#endif // RAPIDJSON_HELPER_H
