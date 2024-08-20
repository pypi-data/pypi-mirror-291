#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <string.h>
#include <ctype.h>
#include <time.h>
#include <stdlib.h>
#include <stdint.h>

#define UNIQUE_ID_LENGTH 16
#define MAX_CLASS_NAME_LENGTH 100

static char base62_chars[] = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";

// Function to normalize class name by converting to lowercase and adding underscores before uppercase letters
static void normalize_class_name(const char *class_name, char *normalized_name) {
    int i, j = 0;
    for (i = 0; class_name[i] != '\0' && j < MAX_CLASS_NAME_LENGTH - 1; i++) {
        if (isupper(class_name[i]) && j > 0) {
            normalized_name[j++] = '_';
        }
        normalized_name[j++] = tolower(class_name[i]);
    }
    normalized_name[j] = '\0';
}

// Function to generate a unique 16-character ID using base62 encoding
static void generate_unique_id(char *unique_id) {
    unsigned char random_bytes[12];
    uint64_t timestamp = (uint64_t)time(NULL);
    
    // Generate 12 random bytes (96 bits) using a cryptographic random function
    FILE *fp = fopen("/dev/urandom", "rb");
    if (fp == NULL) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to open /dev/urandom");
        return;
    }
    fread(random_bytes, sizeof(random_bytes), 1, fp);
    fclose(fp);

    // Combine timestamp with random bytes for added entropy
    uint64_t combined1 = *((uint64_t*)random_bytes) ^ timestamp;
    uint64_t combined2 = *((uint64_t*)(random_bytes + 4)) ^ (timestamp << 32 | rand());

    // Generate the unique ID by shuffling and encoding the combined values
    for (int i = 0; i < UNIQUE_ID_LENGTH; i++) {
        if (i < 8) {
            unique_id[i] = base62_chars[combined1 % 62];
            combined1 /= 62;
        } else {
            unique_id[i] = base62_chars[combined2 % 62];
            combined2 /= 62;
        }
    }
    unique_id[UNIQUE_ID_LENGTH] = '\0';
}

// Python callable function to generate a unique ID based on the class name
static PyObject *generate_ouid(PyObject *self, PyObject *args) {
    const char *class_name;
    if (!PyArg_ParseTuple(args, "s", &class_name)) {
        return NULL;
    }

    char normalized_name[MAX_CLASS_NAME_LENGTH];
    normalize_class_name(class_name, normalized_name);

    char unique_id[UNIQUE_ID_LENGTH + 1];
    generate_unique_id(unique_id);

    char result[MAX_CLASS_NAME_LENGTH + UNIQUE_ID_LENGTH + 2];  // +2 for '.' and '\0'
    snprintf(result, sizeof(result), "%s.%s", normalized_name, unique_id);

    return PyUnicode_FromString(result);
}

static PyMethodDef OuidMethods[] = {
    {"ouid", generate_ouid, METH_VARARGS, "Generate a unique ID for a given class name."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef ouidmodule = {
    PyModuleDef_HEAD_INIT,
    "ouid",
    "Fast unique ID generation for classes",
    -1,
    OuidMethods
};

PyMODINIT_FUNC PyInit_ouid(void) {
    return PyModule_Create(&ouidmodule);
}
