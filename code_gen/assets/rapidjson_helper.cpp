// RapidJSON-backed C helper implementation for all language bridges.
#include "rapidjson_helper.h"
#include <cstdlib>
#include <cstring>
#include <rapidjson/document.h>
#include <rapidjson/writer.h>
#include <rapidjson/stringbuffer.h>
#include <climits>

using namespace rapidjson;

// Parse a JSON array into an int array allocated on heap.
int *des_src_int_list(const char *json_str, size_t *out_size)
{

    Document doc;
    doc.Parse(json_str);

    if (doc.HasParseError())
    {
        return nullptr;
    }

    if (!doc.IsArray())
    {
        return nullptr;
    }

    size_t size = doc.Size();
    *out_size = size;

    int *int_array = new (std::nothrow) int[size];
    if (!int_array)
    {
        return nullptr;
    }

    for (size_t i = 0; i < size; i++)
    {
        if (doc[i].IsInt())
        {
            int_array[i] = doc[i].GetInt();
        }
        else
        {
            delete[] int_array;
            return nullptr;
        }
    }

    return int_array;
}

// Parse a JSON array into a long long array allocated on heap.
long long *des_src_long_list(const char *json_str, size_t *out_size)
{

    Document doc;
    doc.Parse(json_str);

    if (doc.HasParseError())
    {
        return nullptr;
    }

    if (!doc.IsArray())
    {
        return nullptr;
    }

    size_t size = doc.Size();
    *out_size = size;

    long long *long_array = new (std::nothrow) long long[size];
    if (!long_array)
    {
        return nullptr;
    }

    for (size_t i = 0; i < size; i++)
    {
        if (doc[i].IsInt64())
        {
            long_array[i] = doc[i].GetInt64();
        }
        else
        {
            delete[] long_array;
            return nullptr;
        }
    }

    return long_array;
}

// Parse a JSON boolean value.
bool des_src_bool(const char *json_str, bool *out_value)
{

    Document doc;
    doc.Parse(json_str);

    if (doc.HasParseError())
    {
        return false;
    }

    if (!doc.IsBool())
    {
        return false;
    }

    *out_value = doc.GetBool();

    return true;
}

// Parse a JSON integer value.
bool des_src_int(const char *json_str, int *out_value)
{

    Document doc;
    doc.Parse(json_str);

    if (doc.HasParseError())
    {
        return false;
    }

    if (!doc.IsInt())
    {
        return false;
    }

    *out_value = doc.GetInt();

    return true;
}

// Parse a JSON int64 value.
bool des_src_long(const char *json_str, long long *out_value)
{

    Document doc;
    doc.Parse(json_str);

    if (doc.HasParseError())
    {
        return false;
    }

    if (!doc.IsInt64())
    {
        return false;
    }

    *out_value = doc.GetInt64();

    return true;
}

// Parse a JSON string and return a heap-allocated C string.
char *des_src_string(const char *json_str)
{
    Document doc;
    doc.Parse(json_str);

    if (doc.HasParseError() || !doc.IsString())
    {
        return nullptr;
    }

    const char *str = doc.GetString();
    size_t len = strlen(str) + 1;
    char *result = new (std::nothrow) char[len];
    if (!result)
    {
        return nullptr;
    }
    strncpy(result, str, len);
    return result;
}

// Parse a JSON 2D int array into heap-allocated matrix + shape info.
int **des_src_int_list_list(const char *json_str, size_t *rows, size_t **cols)
{
    Document doc;
    doc.Parse(json_str);

    if (doc.HasParseError() || !doc.IsArray())
    {
        return nullptr;
    }

    *rows = doc.Size();
    int **out_array = new (std::nothrow) int *[*rows];
    *cols = new (std::nothrow) size_t[*rows];

    if (!out_array || !*cols)
    {
        delete[] out_array;
        delete[] *cols;
        return nullptr;
    }

    for (size_t i = 0; i < *rows; i++)
    {
        if (!doc[i].IsArray())
        {
            delete[] out_array;
            delete[] *cols;
            return nullptr;
        }

        (*cols)[i] = doc[i].Size();
        out_array[i] = new (std::nothrow) int[(*cols)[i]];

        if (!out_array[i])
        {
            delete[] out_array;
            delete[] *cols;
            return nullptr;
        }

        for (size_t j = 0; j < (*cols)[i]; j++)
        {
            if (!doc[i][j].IsInt())
            {
                delete[] out_array;
                delete[] *cols;
                return nullptr;
            }
            out_array[i][j] = doc[i][j].GetInt();
        }
    }

    return out_array;
}

// Parse a JSON string array into heap-allocated C string array.
char **des_src_string_list(const char *json_str, size_t *out_size)
{
    Document doc;
    doc.Parse(json_str);

    if (doc.HasParseError() || !doc.IsArray())
    {
        return nullptr;
    }

    *out_size = doc.Size();
    char **out_array = new (std::nothrow) char *[*out_size];

    if (!out_array)
    {
        return nullptr;
    }

    for (size_t i = 0; i < *out_size; i++)
    {
        if (!doc[i].IsString())
        {
            delete[] out_array;
            return nullptr;
        }
        const char *str = doc[i].GetString();
        size_t len = strlen(str) + 1;
        out_array[i] = new (std::nothrow) char[len];
        if (!out_array[i])
        {
            delete[] out_array;
            return nullptr;
        }
        strncpy(out_array[i], str, len);
    }

    return out_array;
}

// Parse a JSON boolean array into heap-allocated bool array.
bool *des_src_bool_list(const char *json_str, size_t *out_size)
{
    Document doc;
    doc.Parse(json_str);

    if (doc.HasParseError() || !doc.IsArray())
    {
        return nullptr;
    }

    *out_size = doc.Size();
    bool *out_array = new (std::nothrow) bool[*out_size];

    if (!out_array)
    {
        return nullptr;
    }

    for (size_t i = 0; i < *out_size; i++)
    {
        if (!doc[i].IsBool())
        {
            delete[] out_array;
            return nullptr;
        }
        out_array[i] = doc[i].GetBool();
    }

    return out_array;
}

// Parse a JSON double value.
bool des_src_double(const char *json_str, double *out_value)
{
    Document doc;
    doc.Parse(json_str);

    if (doc.HasParseError())
    {
        return false;
    }

    if (!doc.IsDouble())
    {
        return false;
    }

    *out_value = doc.GetDouble();

    return true;
}

// Parse a JSON double array into heap-allocated array.
double *des_src_double_list(const char *json_str, size_t *out_size)
{
    Document doc;
    doc.Parse(json_str);

    if (doc.HasParseError() || !doc.IsArray())
    {
        return nullptr;
    }

    *out_size = doc.Size();

    double *out_array = new (std::nothrow) double[*out_size];
    if (!out_array)
    {
        return nullptr;
    }

    for (size_t i = 0; i < *out_size; i++)
    {
        if (!doc[i].IsDouble())
        {
            delete[] out_array;
            return nullptr;
        }
        out_array[i] = doc[i].GetDouble();
    }

    return out_array;
}

// Parse a JSON tree-level list where null is encoded as INT_MIN.
int *des_src_tree_list(const char *json_str, size_t *out_size)
{
    Document doc;
    doc.Parse(json_str);

    if (doc.HasParseError())
    {
        return nullptr;
    }

    if (!doc.IsArray())
    {
        return nullptr;
    }

    size_t size = doc.Size();
    *out_size = size;

    int *int_array = new (std::nothrow) int[size];
    if (!int_array)
    {
        return nullptr;
    }

    for (size_t i = 0; i < size; i++)
    {
        if (doc[i].IsInt())
        {
            int_array[i] = doc[i].GetInt();
        }
        else if (doc[i].IsNull())
        {
            int_array[i] = INT_MIN;
        }
        else
        {
            delete[] int_array;
            return nullptr;
        }
    }

    return int_array;
}

// Duplicate a C string into heap memory.
static char *__copy_cstr__(const char *src)
{
    size_t len = strlen(src) + 1;
    char *out = new (std::nothrow) char[len];
    if (!out)
    {
        return nullptr;
    }
    memcpy(out, src, len);
    return out;
}

// Free memory returned by des_src_json_value_list_list.
void delete_src_json_value_list_list(char ***values, size_t rows, const size_t *cols)
{
    if (!values)
    {
        return;
    }
    for (size_t i = 0; i < rows; ++i)
    {
        if (!values[i])
        {
            continue;
        }
        size_t col_count = cols ? cols[i] : 0;
        for (size_t j = 0; j < col_count; ++j)
        {
            delete[] values[i][j];
        }
        delete[] values[i];
    }
    delete[] values;
}

// Parse params line: JSON 2D array -> each element serialized as a JSON fragment string.
char ***des_src_json_value_list_list(const char *json_str, size_t *rows, size_t **cols)
{
    Document doc;
    doc.Parse(json_str);

    if (doc.HasParseError() || !doc.IsArray())
    {
        return nullptr;
    }

    *rows = doc.Size();
    *cols = new (std::nothrow) size_t[*rows]();
    char ***out_array = new (std::nothrow) char **[*rows]();
    if (!*cols || !out_array)
    {
        delete[] *cols;
        delete[] out_array;
        return nullptr;
    }

    for (size_t i = 0; i < *rows; ++i)
    {
        if (!doc[i].IsArray())
        {
            delete_src_json_value_list_list(out_array, *rows, *cols);
            delete[] *cols;
            return nullptr;
        }

        (*cols)[i] = doc[i].Size();
        out_array[i] = new (std::nothrow) char *[(*cols)[i]]();
        if (!out_array[i])
        {
            delete_src_json_value_list_list(out_array, *rows, *cols);
            delete[] *cols;
            return nullptr;
        }

        for (size_t j = 0; j < (*cols)[i]; ++j)
        {
            StringBuffer buffer;
            Writer<StringBuffer> writer(buffer);
            if (!doc[i][j].Accept(writer))
            {
                delete_src_json_value_list_list(out_array, *rows, *cols);
                delete[] *cols;
                return nullptr;
            }
            out_array[i][j] = __copy_cstr__(buffer.GetString());
            if (!out_array[i][j])
            {
                delete_src_json_value_list_list(out_array, *rows, *cols);
                delete[] *cols;
                return nullptr;
            }
        }
    }

    return out_array;
}

// Serialize int to JSON text.
char *ser_src_int(int value)
{
    StringBuffer buffer;
    Writer<StringBuffer> writer(buffer);
    writer.Int(value);

    size_t len = strlen(buffer.GetString()) + 1;
    char *result = new (std::nothrow) char[len];
    if (result)
    {
        strncpy(result, buffer.GetString(), len);
    }
    return result;
}

// Serialize long long to JSON text.
char *ser_src_long(long long value)
{
    StringBuffer buffer;
    Writer<StringBuffer> writer(buffer);
    writer.Int64(value);

    size_t len = strlen(buffer.GetString()) + 1;
    char *result = new (std::nothrow) char[len];
    if (result)
    {
        strncpy(result, buffer.GetString(), len);
    }
    return result;
}

// Serialize bool to JSON text.
char *ser_src_bool(bool value)
{
    StringBuffer buffer;
    Writer<StringBuffer> writer(buffer);
    writer.Bool(value);

    size_t len = strlen(buffer.GetString()) + 1;
    char *result = new (std::nothrow) char[len];
    if (result)
    {
        strncpy(result, buffer.GetString(), len);
    }
    return result;
}

// Serialize C string to JSON text.
char *ser_src_string(const char *value)
{
    StringBuffer buffer;
    Writer<StringBuffer> writer(buffer);
    writer.String(value);

    size_t len = strlen(buffer.GetString()) + 1;
    char *result = new (std::nothrow) char[len];
    if (result)
    {
        strncpy(result, buffer.GetString(), len);
    }
    return result;
}

// Serialize int array to JSON text.
char *ser_src_int_list(const int *values, size_t size)
{
    StringBuffer buffer;
    Writer<StringBuffer> writer(buffer);
    writer.StartArray();
    for (size_t i = 0; i < size; ++i)
    {
        writer.Int(values[i]);
    }
    writer.EndArray();

    size_t len = strlen(buffer.GetString()) + 1;
    char *result = new (std::nothrow) char[len];
    if (result)
    {
        strncpy(result, buffer.GetString(), len);
    }
    return result;
}

// Serialize long long array to JSON text.
char *ser_src_long_list(const long long *values, size_t size)
{
    StringBuffer buffer;
    Writer<StringBuffer> writer(buffer);
    writer.StartArray();
    for (size_t i = 0; i < size; ++i)
    {
        writer.Int64(values[i]);
    }
    writer.EndArray();

    size_t len = strlen(buffer.GetString()) + 1;
    char *result = new (std::nothrow) char[len];
    if (result)
    {
        strncpy(result, buffer.GetString(), len);
    }
    return result;
}

// Serialize 2D int array to JSON text.
char *ser_src_int_list_list(const int **values, size_t rows, const size_t *cols)
{
    StringBuffer buffer;
    Writer<StringBuffer> writer(buffer);
    writer.StartArray();
    for (size_t i = 0; i < rows; ++i)
    {
        writer.StartArray();
        for (size_t j = 0; j < cols[i]; ++j)
        {
            writer.Int(values[i][j]);
        }
        writer.EndArray();
    }
    writer.EndArray();

    size_t len = strlen(buffer.GetString()) + 1;
    char *result = new (std::nothrow) char[len];
    if (result)
    {
        strncpy(result, buffer.GetString(), len);
    }
    return result;
}

// Serialize C string array to JSON text.
char *ser_src_string_list(const char **values, size_t size)
{
    StringBuffer buffer;
    Writer<StringBuffer> writer(buffer);
    writer.StartArray();
    for (size_t i = 0; i < size; ++i)
    {
        writer.String(values[i]);
    }
    writer.EndArray();

    size_t len = strlen(buffer.GetString()) + 1;
    char *result = new (std::nothrow) char[len];
    if (result)
    {
        strncpy(result, buffer.GetString(), len);
    }
    return result;
}

// Serialize bool array to JSON text.
char *ser_src_bool_list(const bool *values, size_t size)
{
    StringBuffer buffer;
    Writer<StringBuffer> writer(buffer);
    writer.StartArray();
    for (size_t i = 0; i < size; ++i)
    {
        writer.Bool(values[i]);
    }
    writer.EndArray();

    size_t len = strlen(buffer.GetString()) + 1;
    char *result = new (std::nothrow) char[len];
    if (result)
    {
        strncpy(result, buffer.GetString(), len);
    }
    return result;
}

// Serialize double to JSON text.
char *ser_src_double(double value)
{
    StringBuffer buffer;
    Writer<StringBuffer> writer(buffer);
    writer.Double(value);

    size_t len = strlen(buffer.GetString()) + 1;
    char *result = new (std::nothrow) char[len];
    if (result)
    {
        strncpy(result, buffer.GetString(), len);
    }
    return result;
}

// Serialize double array to JSON text.
char *ser_src_double_list(const double *values, size_t size)
{
    StringBuffer buffer;
    Writer<StringBuffer> writer(buffer);
    writer.StartArray();
    for (size_t i = 0; i < size; ++i)
    {
        writer.Double(values[i]);
    }
    writer.EndArray();

    size_t len = strlen(buffer.GetString()) + 1;
    char *result = new (std::nothrow) char[len];
    if (result)
    {
        strncpy(result, buffer.GetString(), len);
    }
    return result;
}

// Serialize tree-level list where INT_MIN is emitted as null.
char *ser_src_tree_list(const int *values, size_t size)
{
    StringBuffer buffer;
    Writer<StringBuffer> writer(buffer);

    writer.StartArray();

    for (size_t i = 0; i < size; ++i)
    {
        if (values[i] == INT_MIN)
        {
            writer.Null();
        }
        else
        {
            writer.Int(values[i]);
        }
    }

    writer.EndArray();

    size_t len = strlen(buffer.GetString()) + 1;
    char *result = new (std::nothrow) char[len];
    if (result)
    {
        strncpy(result, buffer.GetString(), len);
    }
    return result;
}
