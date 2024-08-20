#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdint.h>

static const char base64_table[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
static const char base64_url_table[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_";

static const uint8_t base64_reverse_table[256] = {
    64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
    64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
    64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 62, 64, 62, 64, 63,
    52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 64, 64, 64, 64, 64, 64,
    64,  0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14,
    15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 64, 64, 64, 64, 63,
    64, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
    41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 64, 64, 64, 64, 64,
    64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
    64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
    64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
    64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
    64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
    64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
    64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
    64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64
};

static PyObject* fast_b64encode(PyObject* self, PyObject* args) {
    Py_buffer view;
    if (!PyArg_ParseTuple(args, "y*", &view))
        return NULL;

    const unsigned char* data = view.buf;
    Py_ssize_t in_len = view.len;
    Py_ssize_t out_len = (in_len + 2) / 3 * 4;

    PyObject* result = PyBytes_FromStringAndSize(NULL, out_len);
    if (!result) {
        PyBuffer_Release(&view);
        return NULL;
    }

    unsigned char* out = (unsigned char*)PyBytes_AS_STRING(result);

    for (Py_ssize_t i = 0, j = 0; i < in_len;) {
        uint32_t octet_a = i < in_len ? data[i++] : 0;
        uint32_t octet_b = i < in_len ? data[i++] : 0;
        uint32_t octet_c = i < in_len ? data[i++] : 0;

        uint32_t triple = (octet_a << 0x10) + (octet_b << 0x08) + octet_c;

        out[j++] = base64_table[(triple >> 3 * 6) & 0x3F];
        out[j++] = base64_table[(triple >> 2 * 6) & 0x3F];
        out[j++] = base64_table[(triple >> 1 * 6) & 0x3F];
        out[j++] = base64_table[(triple >> 0 * 6) & 0x3F];
    }

    if (in_len % 3) {
        for (Py_ssize_t i = 0; i < 3 - (in_len % 3); i++)
            out[out_len - 1 - i] = '=';
    }

    PyBuffer_Release(&view);
    return result;
}

static PyObject* fast_b64decode(PyObject* self, PyObject* args) {
    Py_buffer view;
    if (!PyArg_ParseTuple(args, "y*", &view))
        return NULL;

    const unsigned char* data = view.buf;
    Py_ssize_t in_len = view.len;
    if (in_len % 4 != 0) {
        PyBuffer_Release(&view);
        PyErr_SetString(PyExc_ValueError, "Invalid base64-encoded string");
        return NULL;
    }

    Py_ssize_t out_len = in_len / 4 * 3;
    if (data[in_len - 1] == '=') out_len--;
    if (data[in_len - 2] == '=') out_len--;

    PyObject* result = PyBytes_FromStringAndSize(NULL, out_len);
    if (!result) {
        PyBuffer_Release(&view);
        return NULL;
    }

    unsigned char* out = (unsigned char*)PyBytes_AS_STRING(result);

    for (Py_ssize_t i = 0, j = 0; i < in_len;) {
        uint32_t sextet_a = base64_reverse_table[data[i++]];
        uint32_t sextet_b = base64_reverse_table[data[i++]];
        uint32_t sextet_c = base64_reverse_table[data[i++]];
        uint32_t sextet_d = base64_reverse_table[data[i++]];

        uint32_t triple = (sextet_a << 3 * 6)
                        + (sextet_b << 2 * 6)
                        + (sextet_c << 1 * 6)
                        + (sextet_d << 0 * 6);

        if (j < out_len) out[j++] = (triple >> 2 * 8) & 0xFF;
        if (j < out_len) out[j++] = (triple >> 1 * 8) & 0xFF;
        if (j < out_len) out[j++] = (triple >> 0 * 8) & 0xFF;
    }

    PyBuffer_Release(&view);
    return result;
}

static PyObject* fast_urlsafe_b64encode(PyObject* self, PyObject* args) {
    PyObject* result = fast_b64encode(self, args);
    if (!result) return NULL;

    char* data = PyBytes_AS_STRING(result);
    Py_ssize_t len = PyBytes_GET_SIZE(result);

    for (Py_ssize_t i = 0; i < len; i++) {
        if (data[i] == '+') data[i] = '-';
        else if (data[i] == '/') data[i] = '_';
    }

    return result;
}

static PyObject* fast_urlsafe_b64decode(PyObject* self, PyObject* args) {
    Py_buffer view;
    if (!PyArg_ParseTuple(args, "y*", &view))
        return NULL;

    PyObject* temp = PyBytes_FromStringAndSize(NULL, view.len);
    if (!temp) {
        PyBuffer_Release(&view);
        return NULL;
    }

    char* data = PyBytes_AS_STRING(temp);
    memcpy(data, view.buf, view.len);

    for (Py_ssize_t i = 0; i < view.len; i++) {
        if (data[i] == '-') data[i] = '+';
        else if (data[i] == '_') data[i] = '/';
    }

    PyBuffer_Release(&view);

    PyObject* result = fast_b64decode(self, Py_BuildValue("(O)", temp));
    Py_DECREF(temp);

    return result;
}

static PyMethodDef FastBase64Methods[] = {
    {"b64encode", fast_b64encode, METH_VARARGS, "Encode the bytes-like object s using Base64 and return a bytes object."},
    {"b64decode", fast_b64decode, METH_VARARGS, "Decode the Base64 encoded bytes-like object or ASCII string s."},
    {"urlsafe_b64encode", fast_urlsafe_b64encode, METH_VARARGS, "Encode bytes-like object using the URL- and filesystem-safe Base64 alphabet."},
    {"urlsafe_b64decode", fast_urlsafe_b64decode, METH_VARARGS, "Decode bytes-like object or ASCII string using the URL- and filesystem-safe Base64 alphabet."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef fast_base64module = {
    PyModuleDef_HEAD_INIT,
    "fast_base64",
    "Fast Base64 encoding and decoding",
    -1,
    FastBase64Methods
};

PyMODINIT_FUNC PyInit_fast_base64(void) {
    return PyModule_Create(&fast_base64module);
}