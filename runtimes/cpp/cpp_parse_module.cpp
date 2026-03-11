// C++ wrappers that convert raw C allocations into std::string/std::vector APIs.
#include <vector>
#include <stdexcept>
#include "../rapidjson_helper.h"
#include "cpp_parse_module.h"

// Take ownership of C heap string and convert to std::string.
static std::string from_owned_cstr(char *raw)
{
    if (!raw)
    {
        throw std::invalid_argument("Error serializing value.");
    }
    std::string result(raw);
    delete[] raw;
    return result;
}

std::vector<int> des_int_list(const std::string &json_str)
{
    // Initialize size variable
    size_t size = 0;

    // Call des_src_int_list to get the array of integers
    int *int_array = des_src_int_list(json_str.c_str(), &size);

    // Check if the des_src_int_list function failed
    if (!int_array)
    {
        throw std::invalid_argument("Error parsing JSON or invalid array.");
    }

    // Create a vector to hold the integers
    std::vector<int> result(int_array, int_array + size);

    // Free the memory allocated by des_src_int_list
    delete[] int_array;

    return result;
}

int des_int(const std::string &json_str)
{
    int result;
    if (!des_src_int(json_str.c_str(), &result))
    {
        throw std::invalid_argument("Error parsing JSON or invalid integer.");
    }
    return result;
}

long long des_long(const std::string &json_str)
{
    long long result;
    if (!des_src_long(json_str.c_str(), &result))
    {
        throw std::invalid_argument("Error parsing JSON or invalid long long.");
    }
    return result;
}

bool des_bool(const std::string &json_str)
{
    bool result;
    if (!des_src_bool(json_str.c_str(), &result))
    {
        throw std::invalid_argument("Error parsing JSON or invalid boolean.");
    }
    return result;
}

std::string des_string(const std::string &json_str)
{
    char *str = des_src_string(json_str.c_str());
    if (!str)
    {
        throw std::invalid_argument("Error parsing JSON or invalid string.");
    }
    std::string result(str);
    delete[] str; // Clean up memory
    return result;
}

std::vector<long long> des_long_list(const std::string &json_str)
{
    size_t size = 0;
    long long *long_array = des_src_long_list(json_str.c_str(), &size);
    if (!long_array)
    {
        throw std::invalid_argument("Error parsing JSON or invalid array of long longs.");
    }
    std::vector<long long> result(long_array, long_array + size);
    delete[] long_array; // Clean up memory
    return result;
}

std::vector<std::vector<int>> des_int_list_list(const std::string &json_str)
{
    size_t rows = 0;
    size_t *cols = nullptr;
    int **int_array = des_src_int_list_list(json_str.c_str(), &rows, &cols);

    if (!int_array)
    {
        throw std::invalid_argument("Error parsing JSON or invalid array of int lists.");
    }

    std::vector<std::vector<int>> result;
    for (size_t i = 0; i < rows; ++i)
    {
        result.push_back(std::vector<int>(int_array[i], int_array[i] + cols[i]));
    }

    // Clean up allocated memory
    for (size_t i = 0; i < rows; ++i)
    {
        delete[] int_array[i];
    }
    delete[] int_array;
    delete[] cols;

    return result;
}

std::vector<std::string> des_string_list(const std::string &json_str)
{
    size_t size = 0;
    char **string_array = des_src_string_list(json_str.c_str(), &size);
    if (!string_array)
    {
        throw std::invalid_argument("Error parsing JSON or invalid array of strings.");
    }

    std::vector<std::string> result;
    for (size_t i = 0; i < size; ++i)
    {
        result.push_back(std::string(string_array[i]));
        delete[] string_array[i]; // Clean up each string
    }

    delete[] string_array; // Clean up the array of string pointers
    return result;
}

std::vector<bool> des_bool_list(const std::string &json_str)
{
    size_t size = 0;
    bool *bool_array = des_src_bool_list(json_str.c_str(), &size);
    if (!bool_array)
    {
        throw std::invalid_argument("Error parsing JSON or invalid array of booleans.");
    }

    std::vector<bool> result(bool_array, bool_array + size);
    delete[] bool_array; // Clean up memory
    return result;
}

double des_double(const std::string &json_str)
{
    double result;
    if (!des_src_double(json_str.c_str(), &result))
    {
        throw std::invalid_argument("Error parsing JSON or invalid double.");
    }
    return result;
}

std::vector<double> des_double_list(const std::string &json_str)
{
    size_t size = 0;
    double *double_array = des_src_double_list(json_str.c_str(), &size);
    if (!double_array)
    {
        throw std::invalid_argument("Error parsing JSON or invalid array of doubles.");
    }

    std::vector<double> result(double_array, double_array + size);
    delete[] double_array; // Clean up memory
    return result;
}

std::vector<int> des_tree_list(const std::string &json_str)
{
    size_t size = 0;
    int *tree_array = des_src_tree_list(json_str.c_str(), &size);
    if (!tree_array)
    {
        throw std::invalid_argument("Error parsing JSON or invalid tree list.");
    }

    std::vector<int> result(tree_array, tree_array + size);
    delete[] tree_array; // Clean up memory
    return result;
}

// Deserialize system-design params as raw JSON fragments per argument.
std::vector<std::vector<std::string>> des_json_value_list_list(const std::string &json_str)
{
    size_t rows = 0;
    size_t *cols = nullptr;
    char ***raw_values = des_src_json_value_list_list(json_str.c_str(), &rows, &cols);
    if (!raw_values)
    {
        throw std::invalid_argument("Error parsing JSON or invalid json value list list.");
    }

    std::vector<std::vector<std::string>> result;
    try
    {
        result.reserve(rows);
        for (size_t i = 0; i < rows; ++i)
        {
            std::vector<std::string> row;
            row.reserve(cols[i]);
            for (size_t j = 0; j < cols[i]; ++j)
            {
                row.emplace_back(raw_values[i][j]);
            }
            result.push_back(std::move(row));
        }
    }
    catch (...)
    {
        delete_src_json_value_list_list(raw_values, rows, cols);
        delete[] cols;
        throw;
    }

    delete_src_json_value_list_list(raw_values, rows, cols);
    delete[] cols;
    return result;
}
std::string ser_int(int value)
{
    return from_owned_cstr(ser_src_int(value));
}

std::string ser_long(long long value)
{
    return from_owned_cstr(ser_src_long(value));
}

std::string ser_bool(bool value)
{
    return from_owned_cstr(ser_src_bool(value));
}

std::string ser_string(const std::string &value)
{
    return from_owned_cstr(ser_src_string(value.c_str()));
}

std::string ser_int_list(const std::vector<int> &values)
{
    return from_owned_cstr(ser_src_int_list(values.data(), values.size()));
}

std::string ser_long_list(const std::vector<long long> &values)
{
    return from_owned_cstr(ser_src_long_list(values.data(), values.size()));
}

std::string ser_int_list_list(const std::vector<std::vector<int>> &values)
{

    size_t rows = values.size();
    size_t *cols = new size_t[rows];

    // Prepare the 2D array
    int **int_array = new int *[rows];
    for (size_t i = 0; i < rows; ++i)
    {
        int_array[i] = new int[values[i].size()];
        cols[i] = values[i].size();
        std::copy(values[i].begin(), values[i].end(), int_array[i]);
    }

    // Serialize the 2D array
    // Use const_cast to remove const from int_array
    char *raw = ser_src_int_list_list(const_cast<const int **>(int_array), rows, cols);

    // Clean up the allocated memory
    for (size_t i = 0; i < rows; ++i)
    {
        delete[] int_array[i];
    }
    delete[] int_array;
    delete[] cols;

    return from_owned_cstr(raw);
}

std::string ser_string_list(const std::vector<std::string> &values)
{

    size_t size = values.size();
    const char **string_array = new const char *[size];

    // Prepare the string array
    for (size_t i = 0; i < size; ++i)
    {
        string_array[i] = values[i].c_str(); // Use string.c_str() to get a const char* for each string
    }

    // Serialize the string array
    char *raw = ser_src_string_list(string_array, size);

    delete[] string_array; // Clean up the array of string pointers
    return from_owned_cstr(raw);
}

std::string ser_bool_list(const std::vector<bool> &values)
{

    size_t size = values.size();
    bool *bool_array = new bool[size];

    // Copy values into the bool array
    std::copy(values.begin(), values.end(), bool_array);

    // Serialize the bool array
    char *raw = ser_src_bool_list(bool_array, size);

    delete[] bool_array; // Clean up memory
    return from_owned_cstr(raw);
}

std::string ser_double(double value)
{
    return from_owned_cstr(ser_src_double(value));
}

std::string ser_double_list(const std::vector<double> &values)
{

    size_t size = values.size();
    double *double_array = new double[size];

    // Copy values into the double array
    std::copy(values.begin(), values.end(), double_array);

    // Serialize the double array
    char *raw = ser_src_double_list(double_array, size);

    delete[] double_array; // Clean up memory
    return from_owned_cstr(raw);
}

std::string ser_tree_list(const std::vector<int> &values)
{

    size_t size = values.size();
    int *tree_array = new int[size];

    // Copy values into the tree array
    std::copy(values.begin(), values.end(), tree_array);

    // Serialize the tree array
    char *raw = ser_src_tree_list(tree_array, size);

    delete[] tree_array; // Clean up memory
    return from_owned_cstr(raw);
}



