#ifndef PY_PARSE_MODULE_H
#define PY_PARSE_MODULE_H

#ifdef __cplusplus
extern "C" {
#endif

#include <Python.h>

/* Function Declarations */
static PyObject* des_int_list(PyObject* self, PyObject* args);
static PyObject* des_long_list(PyObject* self, PyObject* args);
static PyObject* des_bool(PyObject* self, PyObject* args);
static PyObject* des_int(PyObject* self, PyObject* args);
static PyObject* des_long(PyObject* self, PyObject* args);
static PyObject* des_string(PyObject* self, PyObject* args);
static PyObject* des_int_list_list(PyObject* self, PyObject* args);
static PyObject* des_string_list(PyObject* self, PyObject* args);
static PyObject* des_bool_list(PyObject* self, PyObject* args);
static PyObject* des_double(PyObject* self, PyObject* args);
static PyObject* des_double_list(PyObject* self, PyObject* args);
static PyObject* des_tree_list(PyObject* self, PyObject* args);

static PyObject* ser_int(PyObject* self, PyObject* args);
static PyObject* ser_long(PyObject* self, PyObject* args);
static PyObject* ser_bool(PyObject* self, PyObject* args);
static PyObject* ser_string(PyObject* self, PyObject* args);
static PyObject* ser_int_list(PyObject* self, PyObject* args);
static PyObject* ser_long_list(PyObject* self, PyObject* args);
static PyObject* ser_double(PyObject* self, PyObject* args);
static PyObject* ser_double_list(PyObject* self, PyObject* args);
static PyObject* ser_int_list_list(PyObject* self, PyObject* args);
static PyObject* ser_string_list(PyObject* self, PyObject* args);
static PyObject* ser_bool_list(PyObject* self, PyObject* args);
static PyObject* ser_tree_list(PyObject* self, PyObject* args);

#ifdef __cplusplus
}
#endif

#endif /* PY_PARSE_MODULE_H */
