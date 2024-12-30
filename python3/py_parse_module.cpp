#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "../rapidjson_helper.h"
#include "py_parse_module.h"
#include <stdlib.h>
#include <new>

// Helper function to throw Python exceptions
static void throw_python_exception(PyObject* exception_type, const char* message) {
    PyErr_SetString(exception_type, message);
}


static PyObject* des_int_list(PyObject* self, PyObject* args) {
    const char* json_str;
    if (!PyArg_ParseTuple(args, "s", &json_str)) {
        return nullptr; // Argument parsing failed
    }

    size_t size = 0;
    int* int_array = des_src_int_list(json_str, &size);

    if (!int_array) {
        throw_python_exception(PyExc_ValueError, "Error parsing JSON or invalid array.");
        return nullptr;
    }

    PyObject* py_list = PyList_New(size);
    if (!py_list) {
        delete[] int_array;
        throw_python_exception(PyExc_MemoryError, "Failed to allocate memory for Python list.");
        return nullptr;
    }

    for (size_t i = 0; i < size; i++) {
        PyList_SetItem(py_list, i, PyLong_FromLong(int_array[i]));
    }

    delete[] int_array;
    return py_list;
}

static PyObject* des_long_list(PyObject* self, PyObject* args) {
    const char* json_str;
    if (!PyArg_ParseTuple(args, "s", &json_str)) {
        return nullptr;
    }

    size_t size = 0;
    long long* long_array = des_src_long_list(json_str, &size);

    if (!long_array) {
        throw_python_exception(PyExc_ValueError, "Error parsing JSON or invalid array.");
        return nullptr;
    }

    PyObject* py_list = PyList_New(size);
    if (!py_list) {
        delete[] long_array;
        throw_python_exception(PyExc_MemoryError, "Failed to allocate memory for Python list.");
        return nullptr;
    }

    for (size_t i = 0; i < size; i++) {
        PyList_SetItem(py_list, i, PyLong_FromLongLong(long_array[i]));
    }

    delete[] long_array;
    return py_list;
}

static PyObject* des_bool(PyObject* self, PyObject* args) {
    const char* json_str;
    if (!PyArg_ParseTuple(args, "s", &json_str)) {
        return nullptr;
    }

    bool value;
    if (!des_src_bool(json_str, &value)) {
        throw_python_exception(PyExc_ValueError, "Error parsing JSON or invalid boolean.");
        return nullptr;
    }

    return PyBool_FromLong(value);
}

static PyObject* des_int(PyObject* self, PyObject* args) {
    const char* json_str;
    if (!PyArg_ParseTuple(args, "s", &json_str)) {
        return nullptr;
    }

    int value;
    if (!des_src_int(json_str, &value)) {
        throw_python_exception(PyExc_ValueError, "Error parsing JSON or invalid integer.");
        return nullptr;
    }

    return PyLong_FromLong(value);
}

static PyObject* des_long(PyObject* self, PyObject* args) {
    const char* json_str;
    if (!PyArg_ParseTuple(args, "s", &json_str)) {
        return nullptr;
    }

    long long value;
    if (!des_src_long(json_str, &value)) {
        throw_python_exception(PyExc_ValueError, "Error parsing JSON or invalid long integer.");
        return nullptr;
    }

    return PyLong_FromLongLong(value);
}

static PyObject* des_string(PyObject* self, PyObject* args) {
    const char* json_str;
    if (!PyArg_ParseTuple(args, "s", &json_str)) {
        return nullptr;
    }

    char* result = des_src_string(json_str);
    if (!result) {
        throw_python_exception(PyExc_ValueError, "Error parsing JSON or invalid string.");
        return nullptr;
    }

    PyObject* py_string = PyUnicode_FromString(result);
    delete[] result;
    return py_string;
}

static PyObject* des_int_list_list(PyObject* self, PyObject* args) {
    const char* json_str;
    if (!PyArg_ParseTuple(args, "s", &json_str)) {
        return nullptr;
    }

    size_t rows = 0;
    size_t* cols = nullptr;
    int** int_list = des_src_int_list_list(json_str, &rows, &cols);

    if (!int_list) {
        throw_python_exception(PyExc_ValueError, "Error parsing JSON or invalid array of arrays.");
        return nullptr;
    }

    PyObject* py_outer_list = PyList_New(rows);
    if (!py_outer_list) {
        delete[] int_list;
        delete[] cols;
        throw_python_exception(PyExc_MemoryError, "Failed to allocate memory for outer list.");
        return nullptr;
    }

    for (size_t i = 0; i < rows; i++) {
        PyObject* py_inner_list = PyList_New(cols[i]);
        if (!py_inner_list) {
            delete[] int_list;
            delete[] cols;
            throw_python_exception(PyExc_MemoryError, "Failed to allocate memory for inner list.");
            Py_DECREF(py_outer_list);
            return nullptr;
        }

        for (size_t j = 0; j < cols[i]; j++) {
            PyList_SetItem(py_inner_list, j, PyLong_FromLong(int_list[i][j]));
        }

        PyList_SetItem(py_outer_list, i, py_inner_list);
        delete[] int_list[i];
    }

    delete[] int_list;
    delete[] cols;
    return py_outer_list;
}

static PyObject* des_string_list(PyObject* self, PyObject* args) {
    const char* json_str;
    if (!PyArg_ParseTuple(args, "s", &json_str)) {
        return nullptr;
    }

    size_t size = 0;
    char** string_array = des_src_string_list(json_str, &size);

    if (!string_array) {
        throw_python_exception(PyExc_ValueError, "Error parsing JSON or invalid string array.");
        return nullptr;
    }

    PyObject* py_list = PyList_New(size);
    if (!py_list) {
        delete[] string_array;
        throw_python_exception(PyExc_MemoryError, "Failed to allocate memory for Python list.");
        return nullptr;
    }

    for (size_t i = 0; i < size; i++) {
        PyList_SetItem(py_list, i, PyUnicode_FromString(string_array[i]));
        delete[] string_array[i];
    }

    delete[] string_array;
    return py_list;
}

static PyObject* des_bool_list(PyObject* self, PyObject* args) {
    const char* json_str;
    if (!PyArg_ParseTuple(args, "s", &json_str)) {
        return nullptr;  // Argument parsing failed
    }

    size_t size = 0;
    bool* bool_array = des_src_bool_list(json_str, &size);

    if (!bool_array) {
        throw_python_exception(PyExc_ValueError, "Error parsing JSON or invalid boolean array.");
        return nullptr;
    }

    PyObject* py_list = PyList_New(size);
    if (!py_list) {
        delete[] bool_array;
        throw_python_exception(PyExc_MemoryError, "Failed to allocate memory for Python list.");
        return nullptr;
    }

    for (size_t i = 0; i < size; i++) {
        PyList_SetItem(py_list, i, PyBool_FromLong(bool_array[i]));
    }

    delete[] bool_array;
    return py_list;
}

static PyObject* des_double(PyObject* self, PyObject* args) {
    const char* json_str;
    if (!PyArg_ParseTuple(args, "s", &json_str)) {
        return nullptr;
    }

    double value;
    if (!des_src_double(json_str, &value)) {
        throw_python_exception(PyExc_ValueError, "Error parsing JSON or invalid double.");
        return nullptr;
    }

    return PyFloat_FromDouble(value);  // 将 double 转换为 Python 的 float 对象
}

static PyObject* des_double_list(PyObject* self, PyObject* args) {
    const char* json_str;
    if (!PyArg_ParseTuple(args, "s", &json_str)) {
        return nullptr;
    }

    size_t size = 0;
    double* double_array = des_src_double_list(json_str, &size);

    if (!double_array) {
        throw_python_exception(PyExc_ValueError, "Error parsing JSON or invalid double array.");
        return nullptr;
    }

    PyObject* py_list = PyList_New(size);
    if (!py_list) {
        delete[] double_array;
        throw_python_exception(PyExc_MemoryError, "Failed to allocate memory for Python list.");
        return nullptr;
    }

    for (size_t i = 0; i < size; i++) {
        PyList_SetItem(py_list, i, PyFloat_FromDouble(double_array[i]));  // 将 double 转换为 Python 的 float 对象
    }

    delete[] double_array;
    return py_list;
}

static PyObject* des_tree_list(PyObject* self, PyObject* args) {
    const char* json_str;
    if (!PyArg_ParseTuple(args, "s", &json_str)) {
        return nullptr; // Argument parsing failed
    }

    size_t size = 0;
    int* int_array = des_src_tree_list(json_str, &size);

    if (!int_array) {
        throw_python_exception(PyExc_ValueError, "Error parsing JSON or invalid array.");
        return nullptr;
    }

    PyObject* py_list = PyList_New(size);
    if (!py_list) {
        delete[] int_array;
        throw_python_exception(PyExc_MemoryError, "Failed to allocate memory for Python list.");
        return nullptr;
    }

    for (size_t i = 0; i < size; i++) {
        PyList_SetItem(py_list, i, PyLong_FromLong(int_array[i]));
    }

    delete[] int_array;
    return py_list;
}

// Serialization functions
static PyObject* ser_int(PyObject* self, PyObject* args) {
    int value;
    if (!PyArg_ParseTuple(args, "i", &value)) {
        return nullptr;
    }

    char* json_str = ser_src_int(value);
    if (!json_str) {
        throw_python_exception(PyExc_RuntimeError, "Error serializing integer.");
        return nullptr;
    }

    PyObject* result = PyUnicode_FromString(json_str);
    delete[] json_str;
    return result;
}

static PyObject* ser_long(PyObject* self, PyObject* args) {
    long long value;
    if (!PyArg_ParseTuple(args, "L", &value)) {
        return nullptr;
    }

    char* json_str = ser_src_long(value);
    if (!json_str) {
        throw_python_exception(PyExc_RuntimeError, "Error serializing long integer.");
        return nullptr;
    }

    PyObject* result = PyUnicode_FromString(json_str);
    delete[] json_str;
    return result;
}

static PyObject* ser_bool(PyObject* self, PyObject* args) {
    int value;
    if (!PyArg_ParseTuple(args, "p", &value)) {
        return nullptr;
    }

    char* json_str = ser_src_bool(value);
    if (!json_str) {
        throw_python_exception(PyExc_RuntimeError, "Error serializing boolean.");
        return nullptr;
    }

    PyObject* result = PyUnicode_FromString(json_str);
    delete[] json_str;
    return result;
}

static PyObject* ser_string(PyObject* self, PyObject* args) {
    const char* value;
    if (!PyArg_ParseTuple(args, "s", &value)) {
        return nullptr;
    }

    char* json_str = ser_src_string(value);
    if (!json_str) {
        throw_python_exception(PyExc_RuntimeError, "Error serializing string.");
        return nullptr;
    }

    PyObject* result = PyUnicode_FromString(json_str);
    delete[] json_str;
    return result;
}

static PyObject* ser_int_list(PyObject* self, PyObject* args) {
    PyObject* py_list;
    if (!PyArg_ParseTuple(args, "O", &py_list)) {
        return nullptr;
    }

    if (!PyList_Check(py_list)) {
        throw_python_exception(PyExc_TypeError, "Expected a list of integers.");
        return nullptr;
    }

    size_t size = PyList_Size(py_list);
    int* values = new int[size];
    if (!values) {
        throw_python_exception(PyExc_MemoryError, "Failed to allocate memory.");
        return nullptr;
    }

    for (size_t i = 0; i < size; i++) {
        PyObject* item = PyList_GetItem(py_list, i);
        if (!PyLong_Check(item)) {
            delete[] values;
            throw_python_exception(PyExc_TypeError, "List contains non-integer elements.");
            return nullptr;
        }
        values[i] = PyLong_AsLong(item);
    }

    char* json_str = ser_src_int_list(values, size);
    delete[] values;

    if (!json_str) {
        throw_python_exception(PyExc_RuntimeError, "Error serializing integer list.");
        return nullptr;
    }

    PyObject* result = PyUnicode_FromString(json_str);
    delete[] json_str;
    return result;
}

static PyObject* ser_long_list(PyObject* self, PyObject* args) {
    PyObject* py_list;
    if (!PyArg_ParseTuple(args, "O", &py_list)) {
        return nullptr;
    }

    if (!PyList_Check(py_list)) {
        throw_python_exception(PyExc_TypeError, "Expected a list of long integers.");
        return nullptr;
    }

    size_t size = PyList_Size(py_list);
    long long* values = new long long[size];
    if (!values) {
        throw_python_exception(PyExc_MemoryError, "Failed to allocate memory.");
        return nullptr;
    }

    for (size_t i = 0; i < size; i++) {
        PyObject* item = PyList_GetItem(py_list, i);
        if (!PyLong_Check(item)) {
            delete[] values;
            throw_python_exception(PyExc_TypeError, "List contains non-long integer elements.");
            return nullptr;
        }
        values[i] = PyLong_AsLongLong(item);
    }

    char* json_str = ser_src_long_list(values, size);
    delete[] values;

    if (!json_str) {
        throw_python_exception(PyExc_RuntimeError, "Error serializing long integer list.");
        return nullptr;
    }

    PyObject* result = PyUnicode_FromString(json_str);
    delete[] json_str;
    return result;
}

static PyObject* ser_double(PyObject* self, PyObject* args) {
    double value;
    if (!PyArg_ParseTuple(args, "d", &value)) {
        return nullptr;
    }

    char* json_str = ser_src_double(value);
    if (!json_str) {
        throw_python_exception(PyExc_RuntimeError, "Error serializing double.");
        return nullptr;
    }

    PyObject* result = PyUnicode_FromString(json_str);
    delete[] json_str;
    return result;
}

static PyObject* ser_double_list(PyObject* self, PyObject* args) {
    PyObject* py_list;
    if (!PyArg_ParseTuple(args, "O", &py_list)) {
        return nullptr;
    }

    if (!PyList_Check(py_list)) {
        throw_python_exception(PyExc_TypeError, "Expected a list of doubles.");
        return nullptr;
    }

    size_t size = PyList_Size(py_list);
    double* values = new double[size];
    if (!values) {
        throw_python_exception(PyExc_MemoryError, "Failed to allocate memory.");
        return nullptr;
    }

    for (size_t i = 0; i < size; i++) {
        PyObject* item = PyList_GetItem(py_list, i);
        if (!PyFloat_Check(item)) {
            delete[] values;
            throw_python_exception(PyExc_TypeError, "List contains non-double elements.");
            return nullptr;
        }
        values[i] = PyFloat_AsDouble(item);
    }

    char* json_str = ser_src_double_list(values, size);
    delete[] values;

    if (!json_str) {
        throw_python_exception(PyExc_RuntimeError, "Error serializing double list.");
        return nullptr;
    }

    PyObject* result = PyUnicode_FromString(json_str);
    delete[] json_str;
    return result;
}static PyObject* ser_int_list_list(PyObject* self, PyObject* args) {
    PyObject* py_outer_list;
    if (!PyArg_ParseTuple(args, "O", &py_outer_list)) {
        return nullptr;
    }

    if (!PyList_Check(py_outer_list)) {
        throw_python_exception(PyExc_TypeError, "Expected a list of lists of integers.");
        return nullptr;
    }

    size_t rows = PyList_Size(py_outer_list);
    size_t* cols = new(std::nothrow) size_t[rows];
    int** values = new(std::nothrow) int*[rows];
    if (!cols || !values) {
        if(cols){
            delete[] cols;
        }
        if(values){
            delete[] values;
        }
        throw_python_exception(PyExc_MemoryError, "Failed to allocate memory.");
        return nullptr;
    }

    for (size_t i = 0; i < rows; i++) {
        PyObject* py_inner_list = PyList_GetItem(py_outer_list, i);
        if (!PyList_Check(py_inner_list)) {
            delete[] cols;
            for (size_t j = 0; j < i; j++) {
                delete[] values[j];
            }
            delete[] values;
            throw_python_exception(PyExc_TypeError, "Inner elements are not lists.");
            return nullptr;
        }

        cols[i] = PyList_Size(py_inner_list);
        values[i] = new(std::nothrow) int[cols[i]];
        if (!values[i]) {
            delete[] cols;
            for (size_t j = 0; j < i; j++) {
                delete[] values[j];
            }
            delete[] values;
            throw_python_exception(PyExc_MemoryError, "Failed to allocate memory.");
            return nullptr;
        }

        for (size_t j = 0; j < cols[i]; j++) {
            PyObject* item = PyList_GetItem(py_inner_list, j);
            if (!PyLong_Check(item)) {
                delete[] cols;
                for (size_t k = 0; k <= i; k++) {
                    delete[] values[k];
                }
                delete[] values;
                throw_python_exception(PyExc_TypeError, "Inner list contains non-integer elements.");
                return nullptr;
            }
            values[i][j] = PyLong_AsLong(item);
        }
    }

    char* json_str = ser_src_int_list_list((const int**)values, rows, cols);

    for (size_t i = 0; i < rows; i++) {
        delete[] values[i];
    }
    delete[] values;
    delete[] cols;

    if (!json_str) {
        throw_python_exception(PyExc_RuntimeError, "Error serializing list of lists of integers.");
        return nullptr;
    }

    PyObject* result = PyUnicode_FromString(json_str);
    delete[] json_str;
    return result;
}

static PyObject* ser_string_list(PyObject* self, PyObject* args) {
    PyObject* py_list;
    if (!PyArg_ParseTuple(args, "O", &py_list)) {
        return nullptr;
    }

    if (!PyList_Check(py_list)) {
        throw_python_exception(PyExc_TypeError, "Expected a list of strings.");
        return nullptr;
    }

    size_t size = PyList_Size(py_list);
    const char** values = new(std::nothrow) const char*[size];
    if (!values) {
        throw_python_exception(PyExc_MemoryError, "Failed to allocate memory.");
        return nullptr;
    }

    for (size_t i = 0; i < size; i++) {
        PyObject* item = PyList_GetItem(py_list, i);
        if (!PyUnicode_Check(item)) {
            delete[] values;
            throw_python_exception(PyExc_TypeError, "List contains non-string elements.");
            return nullptr;
        }
        values[i] = PyUnicode_AsUTF8(item);
    }

    char* json_str = ser_src_string_list(values, size);
    delete[] values;

    if (!json_str) {
        throw_python_exception(PyExc_RuntimeError, "Error serializing string list.");
        return nullptr;
    }

    PyObject* result = PyUnicode_FromString(json_str);
    delete[] json_str;
    return result;
}

static PyObject* ser_bool_list(PyObject* self, PyObject* args) {
    PyObject* py_list;
    if (!PyArg_ParseTuple(args, "O", &py_list)) {
        return nullptr;
    }

    if (!PyList_Check(py_list)) {
        throw_python_exception(PyExc_TypeError, "Expected a list of booleans.");
        return nullptr;
    }

    size_t size = PyList_Size(py_list);
    bool* values = new(std::nothrow) bool[size];
    if (!values) {
        throw_python_exception(PyExc_MemoryError, "Failed to allocate memory.");
        return nullptr;
    }

    for (size_t i = 0; i < size; i++) {
        PyObject* item = PyList_GetItem(py_list, i);
        if (!PyBool_Check(item)) {
            delete[] values;
            throw_python_exception(PyExc_TypeError, "List contains non-boolean elements.");
            return nullptr;
        }
        values[i] = PyObject_IsTrue(item);
    }

    char* json_str = ser_src_bool_list(values, size);
    delete[] values;

    if (!json_str) {
        throw_python_exception(PyExc_RuntimeError, "Error serializing boolean list.");
        return nullptr;
    }

    PyObject* result = PyUnicode_FromString(json_str);
    delete[] json_str;
    return result;
}

static PyObject* ser_tree_list(PyObject* self, PyObject* args) {
    PyObject* py_list;
    if (!PyArg_ParseTuple(args, "O", &py_list)) {
        return nullptr;
    }

    if (!PyList_Check(py_list)) {
        throw_python_exception(PyExc_TypeError, "Expected a list of integers.");
        return nullptr;
    }

    size_t size = PyList_Size(py_list);
    int* values = new(std::nothrow) int[size];
    if (!values) {
        throw_python_exception(PyExc_MemoryError, "Failed to allocate memory.");
        return nullptr;
    }

    for (size_t i = 0; i < size; i++) {
        PyObject* item = PyList_GetItem(py_list, i);
        if (!PyLong_Check(item)) {
            delete[] values;
            throw_python_exception(PyExc_TypeError, "List contains non-integer elements.");
            return nullptr;
        }
        values[i] = PyLong_AsLong(item);
    }

    char* json_str = ser_src_tree_list(values, size);
    delete[] values;

    if (!json_str) {
        throw_python_exception(PyExc_RuntimeError, "Error serializing integer list.");
        return nullptr;
    }

    PyObject* result = PyUnicode_FromString(json_str);
    delete[] json_str;
    return result;
}



// Method definitions
static PyMethodDef JsonParserMethods[] = {
    {
        "des_int_list", 
        des_int_list, 
        METH_VARARGS, 
        "Deserialize a JSON array of integers into a Python list.\n"
        "Arguments:\n"
        "    args (str): A JSON string containing an array of integers.\n"
        "Returns:\n"
        "    List[int]: A Python list of integers."
    },
    {
        "des_long_list", 
        des_long_list, 
        METH_VARARGS, 
        "Deserialize a JSON array of long integers into a Python list.\n"
        "Arguments:\n"
        "    args (str): A JSON string containing an array of long integers.\n"
        "Returns:\n"
        "    List[int]: A Python list of long integers."
    },
    {
        "des_bool", 
        des_bool, 
        METH_VARARGS, 
        "Deserialize a JSON boolean value.\n"
        "Arguments:\n"
        "    args (str): A JSON string containing a boolean value.\n"
        "Returns:\n"
        "    bool: A Python boolean value."
    },
    {
        "des_int", 
        des_int, 
        METH_VARARGS, 
        "Deserialize a JSON integer value.\n"
        "Arguments:\n"
        "    args (str): A JSON string containing a single integer.\n"
        "Returns:\n"
        "    int: A Python integer."
    },
    {
        "des_long", 
        des_long, 
        METH_VARARGS, 
        "Deserialize a JSON long integer value.\n"
        "Arguments:\n"
        "    args (str): A JSON string containing a single long integer.\n"
        "Returns:\n"
        "    int: A Python long integer."
    },
    {
        "des_string", 
        des_string, 
        METH_VARARGS, 
        "Deserialize a JSON string value.\n"
        "Arguments:\n"
        "    args (str): A JSON string containing a string value.\n"
        "Returns:\n"
        "    str: A Python string."
    },
    {
        "des_int_list_list", 
        des_int_list_list, 
        METH_VARARGS, 
        "Deserialize a JSON array of integer arrays into a Python list of lists.\n"
        "Arguments:\n"
        "    args (str): A JSON string containing an array of integer arrays.\n"
        "Returns:\n"
        "    List[List[int]]: A Python list of lists of integers."
    },
    {
        "des_string_list", 
        des_string_list, 
        METH_VARARGS, 
        "Deserialize a JSON array of strings into a Python list.\n"
        "Arguments:\n"
        "    args (str): A JSON string containing an array of strings.\n"
        "Returns:\n"
        "    List[str]: A Python list of strings."
    },
    {
        "des_bool_list", 
        des_bool_list, 
        METH_VARARGS, 
        "Deserialize a JSON array of booleans into a Python list.\n"
        "Arguments:\n"
        "    args (str): A JSON string containing an array of boolean values.\n"
        "Returns:\n"
        "    List[bool]: A Python list of booleans."
    },
    {
        "des_double", 
        des_double, 
        METH_VARARGS, 
        "Deserialize a JSON double value.\n"
        "Arguments:\n"
        "    args (str): A JSON string containing a double value.\n"
        "Returns:\n"
        "    float: A Python float."
    },
    {
        "des_double_list", 
        des_double_list, 
        METH_VARARGS, 
        "Deserialize a JSON array of double values into a Python list.\n"
        "Arguments:\n"
        "    args (str): A JSON string containing an array of doubles.\n"
        "Returns:\n"
        "    List[float]: A Python list of floats."
    },
    {
        "ser_int", 
        ser_int, 
        METH_VARARGS, 
        "Serialize an integer to JSON.\n"
        "Arguments:\n"
        "    args (int): An integer value to serialize.\n"
        "Returns:\n"
        "    str: A JSON string representing the integer."
    },
    {
        "ser_long", 
        ser_long, 
        METH_VARARGS, 
        "Serialize a long integer to JSON.\n"
        "Arguments:\n"
        "    args (long): A long integer value to serialize.\n"
        "Returns:\n"
        "    str: A JSON string representing the long integer."
    },
    {
        "ser_bool", 
        ser_bool, 
        METH_VARARGS, 
        "Serialize a boolean to JSON.\n"
        "Arguments:\n"
        "    args (bool): A boolean value to serialize.\n"
        "Returns:\n"
        "    str: A JSON string representing the boolean."
    },
    {
        "ser_string", 
        ser_string, 
        METH_VARARGS, 
        "Serialize a string to JSON.\n"
        "Arguments:\n"
        "    args (str): A string value to serialize.\n"
        "Returns:\n"
        "    str: A JSON string representing the string."
    },
    {
        "ser_int_list", 
        ser_int_list, 
        METH_VARARGS, 
        "Serialize a list of integers to JSON.\n"
        "Arguments:\n"
        "    args (List[int]): A list of integers to serialize.\n"
        "Returns:\n"
        "    str: A JSON string representing the list of integers."
    },
    {
        "ser_long_list", 
        ser_long_list, 
        METH_VARARGS, 
        "Serialize a list of long integers to JSON.\n"
        "Arguments:\n"
        "    args (List[long]): A list of long integers to serialize.\n"
        "Returns:\n"
        "    str: A JSON string representing the list of long integers."
    },
    {
        "ser_double", 
        ser_double, 
        METH_VARARGS, 
        "Serialize a double to JSON.\n"
        "Arguments:\n"
        "    args (float): A double value to serialize.\n"
        "Returns:\n"
        "    str: A JSON string representing the double."
    },
    {
        "ser_double_list", 
        ser_double_list, 
        METH_VARARGS, 
        "Serialize a list of doubles to JSON.\n"
        "Arguments:\n"
        "    args (List[float]): A list of doubles to serialize.\n"
        "Returns:\n"
        "    str: A JSON string representing the list of doubles."
    },
    {
        "ser_int_list_list", 
        ser_int_list_list, 
        METH_VARARGS, 
        "Serialize a list of lists of integers to JSON.\n"
        "Arguments:\n"
        "    args (List[List[int]]): A list of lists of integers to serialize.\n"
        "Returns:\n"
        "    str: A JSON string representing the list of lists of integers."
    },
    {
        "ser_string_list", 
        ser_string_list, 
        METH_VARARGS, 
        "Serialize a list of strings to JSON.\n"
        "Arguments:\n"
        "    args (List[str]): A list of strings to serialize.\n"
        "Returns:\n"
        "    str: A JSON string representing the list of strings."
    },
    {
        "ser_bool_list", 
        ser_bool_list, 
        METH_VARARGS, 
        "Serialize a list of booleans to JSON.\n"
        "Arguments:\n"
        "    args (List[bool]): A list of booleans to serialize.\n"
        "Returns:\n"
        "    str: A JSON string representing the list of booleans."
    },
    {
    "ser_tree_list", 
    ser_tree_list, 
    METH_VARARGS, 
    "Serialize a Python list of integers into a JSON array string.\n"
    "This function converts a Python list of integers into a JSON string, "
    "and converts any null elements in the list to null in the resulting JSON.\n"
    "Arguments:\n"
    "    py_list (List[int]): A Python list of integers, where null elements are represented as null in JSON.\n"
    "Returns:\n"
    "    str: A JSON string representing the list, with nulls converted to null in JSON."
    },
    {
    "des_tree_list", 
    des_tree_list, 
    METH_VARARGS, 
    "Deserialize a JSON array string into a Python list of integers.\n"
    "This function parses a JSON string representing an array of integers, "
    "where any null values in the JSON array are represented as INT_MIN in the resulting list.\n"
    "Arguments:\n"
    "    json_str (str): A JSON string containing an array of integers, where null values are represented as null in JSON.\n"
    "Returns:\n"
    "    List[int]: A Python list of integers, with INT_MIN for null values."
    },
    {NULL, NULL, 0, NULL} // Sentinel
};


// Module definition
static struct PyModuleDef py_parse_module_rmodule = {
    PyModuleDef_HEAD_INIT,
    "py_parse_module",   // Module name
    "A module for JSON parsing using RapidJSON.",  // Module description
    -1,             // Module size
    JsonParserMethods
};

// Module initialization
PyMODINIT_FUNC PyInit_py_parse_module(void) {
    return PyModule_Create(&py_parse_module_rmodule);
}