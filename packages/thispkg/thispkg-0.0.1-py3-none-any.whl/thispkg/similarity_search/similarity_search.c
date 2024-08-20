#define PY_SSIZE_T_CLEAN
#include <Python.h>
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <numpy/arrayobject.h>
#include <math.h>

// Function prototypes
static double cosine_similarity(PyArrayObject *a, PyArrayObject *b);
static double euclidean_distance(PyArrayObject *a, PyArrayObject *b);
static double dot_product(PyArrayObject *a, PyArrayObject *b);

static double cosine_similarity(PyArrayObject *a, PyArrayObject *b) {
    npy_intp size = PyArray_SIZE(a);
    double *a_data = (double*)PyArray_DATA(a);
    double *b_data = (double*)PyArray_DATA(b);

    double dot = 0.0, norm_a = 0.0, norm_b = 0.0;
    for (npy_intp i = 0; i < size; i++) {
        dot += a_data[i] * b_data[i];
        norm_a += a_data[i] * a_data[i];
        norm_b += b_data[i] * b_data[i];
    }

    return dot / (sqrt(norm_a) * sqrt(norm_b));
}

static double euclidean_distance(PyArrayObject *a, PyArrayObject *b) {
    npy_intp size = PyArray_SIZE(a);
    double *a_data = (double*)PyArray_DATA(a);
    double *b_data = (double*)PyArray_DATA(b);

    double sum = 0.0;
    for (npy_intp i = 0; i < size; i++) {
        double diff = a_data[i] - b_data[i];
        sum += diff * diff;
    }

    return sqrt(sum);
}

static double dot_product(PyArrayObject *a, PyArrayObject *b) {
    npy_intp size = PyArray_SIZE(a);
    double *a_data = (double*)PyArray_DATA(a);
    double *b_data = (double*)PyArray_DATA(b);

    double dot = 0.0;
    for (npy_intp i = 0; i < size; i++) {
        dot += a_data[i] * b_data[i];
    }

    return dot;
}

static int compare_results(const void *a, const void *b) {
    PyObject *dict1 = *(PyObject**)a;
    PyObject *dict2 = *(PyObject**)b;

    PyObject *score1 = PyDict_GetItemString(dict1, "score");
    PyObject *score2 = PyDict_GetItemString(dict2, "score");

    double d1 = PyFloat_AsDouble(score1);
    double d2 = PyFloat_AsDouble(score2);

    // Sort in descending order
    return (d1 < d2) - (d1 > d2);
}

static PyObject* similarity_search(PyObject* self, PyObject* args, PyObject* kwargs) {
    PyObject *query_obj, *embeddings_obj;
    const char *algorithm;
    static char* kwlist[] = {"query", "embeddings", "algorithm", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OOs", kwlist,
                                     &query_obj, &embeddings_obj, &algorithm)) {
        return NULL;
    }

    // Extract query vector and topK
    PyObject *query_vector_obj = PyDict_GetItemString(query_obj, "vector");
    PyObject *topK_obj = PyDict_GetItemString(query_obj, "topK");
    if (!query_vector_obj || !topK_obj) {
        PyErr_SetString(PyExc_ValueError, "Invalid query object");
        return NULL;
    }

    PyArrayObject *query_vector = (PyArrayObject*)PyArray_FROM_OTF(query_vector_obj, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
    if (query_vector == NULL) {
        return NULL;
    }

    long topK = PyLong_AsLong(topK_obj);
    if (topK <= 0) {
        PyErr_SetString(PyExc_ValueError, "topK must be positive");
        Py_DECREF(query_vector);
        return NULL;
    }

    // Process embeddings
    if (!PyList_Check(embeddings_obj)) {
        PyErr_SetString(PyExc_TypeError, "embeddings must be a list");
        Py_DECREF(query_vector);
        return NULL;
    }

    Py_ssize_t num_embeddings = PyList_Size(embeddings_obj);
    PyObject *results = PyList_New(num_embeddings);

    if (results == NULL) {
        Py_DECREF(query_vector);
        return PyErr_NoMemory();
    }

    for (Py_ssize_t i = 0; i < num_embeddings; i++) {
        PyObject *embedding = PyList_GetItem(embeddings_obj, i);
        PyObject *embedding_vector_obj = PyDict_GetItemString(embedding, "vector");
        PyObject *embedding_id = PyDict_GetItemString(embedding, "id");

        if (!embedding_vector_obj || !embedding_id) {
            PyErr_SetString(PyExc_ValueError, "Invalid embedding object");
            Py_DECREF(query_vector);
            Py_DECREF(results);
            return NULL;
        }

        PyArrayObject *embedding_vector = (PyArrayObject*)PyArray_FROM_OTF(embedding_vector_obj, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
        if (embedding_vector == NULL) {
            Py_DECREF(query_vector);
            Py_DECREF(results);
            return NULL;
        }

        // Compute similarity
        double score;
        if (strcmp(algorithm, "cosine") == 0) {
            score = cosine_similarity(query_vector, embedding_vector);
        } else if (strcmp(algorithm, "euclidean") == 0) {
            score = euclidean_distance(query_vector, embedding_vector);
        } else if (strcmp(algorithm, "dot") == 0) {
            score = dot_product(query_vector, embedding_vector);
        } else {
            PyErr_SetString(PyExc_ValueError, "Invalid algorithm");
            Py_DECREF(query_vector);
            Py_DECREF(embedding_vector);
            Py_DECREF(results);
            return NULL;
        }

        // Create result dict
        PyObject *result = PyDict_New();
        if (result == NULL) {
            Py_DECREF(query_vector);
            Py_DECREF(embedding_vector);
            Py_DECREF(results);
            return PyErr_NoMemory();
        }

        PyDict_SetItemString(result, "id", embedding_id);
        PyDict_SetItemString(result, "score", PyFloat_FromDouble(score));

        // Insert result into the list
        PyList_SET_ITEM(results, i, result);  // PyList_SET_ITEM steals a reference, so no need to Py_DECREF(result)
        Py_DECREF(embedding_vector);
    }

    Py_DECREF(query_vector);

    // Sort the results
    PyObject **result_array = PySequence_Fast_ITEMS(results);
    Py_ssize_t result_count = PyList_GET_SIZE(results);
    qsort(result_array, result_count, sizeof(PyObject*), compare_results);

    // Trim to topK results
    if (result_count > topK) {
        for (Py_ssize_t i = topK; i < result_count; i++) {
            Py_DECREF(PyList_GET_ITEM(results, i));
        }
        PyList_SetSlice(results, topK, result_count, NULL);
    }

    return results;
}

static PyMethodDef SimilarityMethods[] = {
    {"similarity_search", (PyCFunction)similarity_search, METH_VARARGS | METH_KEYWORDS,
     "Compute similarity between query and embeddings"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef similaritymodule = {
    PyModuleDef_HEAD_INIT,
    "similarity_search",
    NULL,
    -1,
    SimilarityMethods
};

PyMODINIT_FUNC PyInit_similarity_search(void) {
    import_array();
    return PyModule_Create(&similaritymodule);
}
