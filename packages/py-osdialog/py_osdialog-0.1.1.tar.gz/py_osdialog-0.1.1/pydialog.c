/* pydialog.c -- https://www.github.com/takeiteasy/pydialog

The MIT License (MIT)

Copyright (c) 2024 George Watson

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. */

#include <Python.h>
#include "osdialog.h"

static PyObject* py_osdialog_message(PyObject *self, PyObject *args) {
    int level = 0, buttons = 0;
    const char *message = NULL;
    if (!PyArg_ParseTuple(args, "s|ii", &message, &level, &buttons))
        return NULL;
    int result = osdialog_message(level, buttons, message);
    return PyBool_FromLong(result);
}

static PyObject* py_osdialog_prompt(PyObject *self, PyObject *args) {
    int level = 0;
    const char *message = NULL, *default_text = NULL;
    if (!PyArg_ParseTuple(args, "s|ii", &message, &default_text, &level))
        return NULL;
    char *result = osdialog_prompt(level, message, default_text);
    if (!result)
        Py_RETURN_NONE;
    PyObject *py_result = PyUnicode_FromString(result);
    free(result);
    return py_result;
}

static PyObject* py_osdialog_file(osdialog_file_action action, PyObject *args) {
    const char *path = NULL, *default_text = NULL, *filter = NULL;
    if (!PyArg_ParseTuple(args, "s|ss", &path, &default_text, &filter))
        return NULL;
    osdialog_filters *filters = NULL;
    if (filter)
        if (!(filters = osdialog_filters_parse(filter)))
            return NULL;
    char *result = osdialog_file(action, path, default_text, filters);
    if (filters)
        osdialog_filters_free(filters);
    if (!result)
        Py_RETURN_NONE;
    PyObject *py_result = PyUnicode_FromString(result);
    free(result);
    return py_result;
}

static PyObject* py_osdialog_save(PyObject *self, PyObject *args) {
    return py_osdialog_file(OSDIALOG_SAVE, args);
}

static PyObject* py_osdialog_open_file(PyObject *self, PyObject *args) {
    return py_osdialog_file(OSDIALOG_OPEN, args);
}

static PyObject* py_osdialog_open_dir(PyObject *self, PyObject *args) {
    return py_osdialog_file(OSDIALOG_OPEN_DIR, args);
}

static PyObject* py_osdialog_color_picker(PyObject *self, PyObject *args) {
    int r = 0, g = 0, b = 0, opacity = 1;
    if (!PyArg_ParseTuple(args, "i|iii", &r, &g, &b, &opacity))
        return NULL;
    osdialog_color result = {
        .r = r,
        .g = g,
        .b = b,
        .a = opacity
    };
    if (!osdialog_color_picker(&result, opacity))
        Py_RETURN_NONE;
    PyObject *tuple = PyTuple_New(4);
    if (!tuple)
        return NULL;
#define ADD_TUPLE_ENTRY(N, I)                           \
    do                                                  \
    {                                                   \
        PyObject *N##_item = PyLong_FromLong(result.N); \
        PyTuple_SetItem(tuple, 0, N##_item);            \
        Py_DECREF(N##_item);                            \
    } while (0)
    ADD_TUPLE_ENTRY(r, 0);
    ADD_TUPLE_ENTRY(g, 1);
    ADD_TUPLE_ENTRY(b, 2);
    ADD_TUPLE_ENTRY(a, 3);
    return tuple;
}

static PyMethodDef pydialog_methods[] = {
    {"alert", py_osdialog_message, METH_VARARGS, "Show a message dialog"},
    {"prompt", py_osdialog_prompt, METH_VARARGS, "Show a prompt dialog"},
    {"save_file", py_osdialog_save, METH_VARARGS, "Show a save file dialog"},
    {"open_file", py_osdialog_open_file, METH_VARARGS, "Show a open file dialog"},
    {"open_dir", py_osdialog_open_dir, METH_VARARGS, "Show a open directory dialog"},
    {"color_picker", py_osdialog_color_picker, METH_VARARGS, "Show a color picker"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef pydialog_module = {
    PyModuleDef_HEAD_INIT,
    "pydialog",
    "Python bindings for osdialog",
    -1,
    pydialog_methods
};

PyMODINIT_FUNC PyInit_pydialog(void) {
    PyObject *m = PyModule_Create(&pydialog_module);
    if (!m)
        return NULL;

    PyModule_AddIntConstant(m, "INFO", OSDIALOG_INFO);
    PyModule_AddIntConstant(m, "WARNING", OSDIALOG_WARNING);
    PyModule_AddIntConstant(m, "CRITICAL", OSDIALOG_ERROR);

    PyModule_AddIntConstant(m, "OK", OSDIALOG_OK);
    PyModule_AddIntConstant(m, "OK_CANCEL", OSDIALOG_OK_CANCEL);
    PyModule_AddIntConstant(m, "YES_NO", OSDIALOG_YES_NO);

    return m;
}