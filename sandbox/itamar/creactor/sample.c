/* Generated by Pyrex 0.9.2.1 on Thu Jun 24 16:32:24 2004 */

#include "Python.h"
#include "structmember.h"
#ifndef PY_LONG_LONG
  #define PY_LONG_LONG LONG_LONG
#endif
#include "string.h"
#include "stdlib.h"


typedef struct {PyObject **p; char *s;} __Pyx_InternTabEntry; /*proto*/
typedef struct {PyObject **p; char *s; long n;} __Pyx_StringTabEntry; /*proto*/
static PyObject *__Pyx_UnpackItem(PyObject *, int); /*proto*/
static int __Pyx_EndUnpack(PyObject *, int); /*proto*/
static int __Pyx_PrintItem(PyObject *); /*proto*/
static int __Pyx_PrintNewline(void); /*proto*/
static void __Pyx_Raise(PyObject *type, PyObject *value, PyObject *tb); /*proto*/
static void __Pyx_ReRaise(void); /*proto*/
static PyObject *__Pyx_Import(PyObject *name, PyObject *from_list); /*proto*/
static PyObject *__Pyx_GetExcValue(void); /*proto*/
static int __Pyx_ArgTypeTest(PyObject *obj, PyTypeObject *type, int none_allowed, char *name); /*proto*/
static int __Pyx_TypeTest(PyObject *obj, PyTypeObject *type); /*proto*/
static int __Pyx_GetStarArgs(PyObject **args, PyObject **kwds, char *kwd_list[], int nargs, PyObject **args2, PyObject **kwds2); /*proto*/
static void __Pyx_WriteUnraisable(char *name); /*proto*/
static void __Pyx_AddTraceback(char *funcname); /*proto*/
static PyTypeObject *__Pyx_ImportType(char *module_name, char *class_name, long size);  /*proto*/
static int __Pyx_SetVtable(PyObject *dict, void *vtable); /*proto*/
static int __Pyx_GetVtable(PyObject *dict, void **vtabptr); /*proto*/
static PyObject *__Pyx_CreateClass(PyObject *bases, PyObject *dict, PyObject *name, char *modname); /*proto*/
static int __Pyx_InternStrings(__Pyx_InternTabEntry *t); /*proto*/
static int __Pyx_InitStrings(__Pyx_StringTabEntry *t); /*proto*/
static PyObject *__Pyx_GetName(PyObject *dict, PyObject *name); /*proto*/

static PyObject *__pyx_m;
static PyObject *__pyx_b;
static int __pyx_lineno;
static char *__pyx_filename;
staticforward char **__pyx_f;

/* Declarations from tcp */


struct __pyx_obj_3tcp__CMixin {
  PyObject_HEAD
  char (*_c_buffer);
  unsigned int _c_buflen;
  char (*_c_readbuf);
  unsigned int _c_readlen;
};


struct __pyx_obj_3tcp_CProtocol {
  PyObject_HEAD
};

static PyTypeObject *__pyx_ptype_3tcp__CMixin = 0;
static PyTypeObject *__pyx_ptype_3tcp_CProtocol = 0;

/* Declarations from sample */

staticforward PyTypeObject __pyx_type_6sample_SampleProtocol;

struct __pyx_obj_6sample_SampleProtocol {
  struct __pyx_obj_3tcp_CProtocol __pyx_base;
  struct __pyx_vtabstruct_6sample_SampleProtocol *__pyx_vtab;
  char (buf[100000]);
  char (*readbuf);
  int readlen;
  int counter;
};

struct __pyx_vtabstruct_6sample_SampleProtocol {
  void ((*lineReceived)(struct __pyx_obj_6sample_SampleProtocol *,char (*),int ));
};
static struct __pyx_vtabstruct_6sample_SampleProtocol *__pyx_vtabptr_6sample_SampleProtocol;

static PyTypeObject *__pyx_ptype_6sample_SampleProtocol = 0;

/* Implementation of sample */

static PyObject *__pyx_n_tcp;

static PyObject *__pyx_n_transport;
static PyObject *__pyx_n_setBuffer;

static PyObject *__pyx_f_6sample_14SampleProtocol_connectionMade(PyObject *__pyx_v_self, PyObject *__pyx_args, PyObject *__pyx_kwds); /*proto*/
static PyObject *__pyx_f_6sample_14SampleProtocol_connectionMade(PyObject *__pyx_v_self, PyObject *__pyx_args, PyObject *__pyx_kwds) {
  struct __pyx_obj_3tcp__CMixin *__pyx_v_transport;
  PyObject *__pyx_r;
  PyObject *__pyx_1 = 0;
  PyObject *__pyx_2 = 0;
  PyObject *__pyx_3 = 0;
  PyObject *__pyx_4 = 0;
  static char *__pyx_argnames[] = {0};
  if (!PyArg_ParseTupleAndKeywords(__pyx_args, __pyx_kwds, "", __pyx_argnames)) return 0;
  Py_INCREF((PyObject *)__pyx_v_self);
  ((PyObject*)__pyx_v_transport) = Py_None; Py_INCREF(((PyObject*)__pyx_v_transport));

  /* "/home/itamar/devel/python/Twisted/sandbox/itamar/creactor/sample.pyx":21 */
  ((struct __pyx_obj_6sample_SampleProtocol *)__pyx_v_self)->readbuf = ((struct __pyx_obj_6sample_SampleProtocol *)__pyx_v_self)->buf;

  /* "/home/itamar/devel/python/Twisted/sandbox/itamar/creactor/sample.pyx":22 */
  ((struct __pyx_obj_6sample_SampleProtocol *)__pyx_v_self)->readlen = 0;

  /* "/home/itamar/devel/python/Twisted/sandbox/itamar/creactor/sample.pyx":23 */
  ((struct __pyx_obj_6sample_SampleProtocol *)__pyx_v_self)->counter = 0;

  /* "/home/itamar/devel/python/Twisted/sandbox/itamar/creactor/sample.pyx":24 */
  __pyx_1 = PyObject_GetAttr(__pyx_v_self, __pyx_n_transport); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 24; goto __pyx_L1;}
  __pyx_2 = PyObject_GetAttr(__pyx_1, __pyx_n_setBuffer); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 24; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;
  __pyx_1 = PyString_FromString(((struct __pyx_obj_6sample_SampleProtocol *)__pyx_v_self)->buf); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 24; goto __pyx_L1;}
  __pyx_3 = PyInt_FromLong(100000); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 24; goto __pyx_L1;}
  __pyx_4 = PyTuple_New(2); if (!__pyx_4) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 24; goto __pyx_L1;}
  PyTuple_SET_ITEM(__pyx_4, 0, __pyx_1);
  PyTuple_SET_ITEM(__pyx_4, 1, __pyx_3);
  __pyx_1 = 0;
  __pyx_3 = 0;
  __pyx_1 = PyObject_CallObject(__pyx_2, __pyx_4); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 24; goto __pyx_L1;}
  Py_DECREF(__pyx_2); __pyx_2 = 0;
  Py_DECREF(__pyx_4); __pyx_4 = 0;
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  __pyx_r = Py_None; Py_INCREF(__pyx_r);
  goto __pyx_L0;
  __pyx_L1:;
  Py_XDECREF(__pyx_1);
  Py_XDECREF(__pyx_2);
  Py_XDECREF(__pyx_3);
  Py_XDECREF(__pyx_4);
  __Pyx_AddTraceback("sample.SampleProtocol.connectionMade");
  __pyx_r = 0;
  __pyx_L0:;
  Py_DECREF(__pyx_v_transport);
  Py_DECREF((PyObject *)__pyx_v_self);
  return __pyx_r;
}

static PyObject *__pyx_n_buffer;

static void __pyx_f_6sample_14SampleProtocol_cdataReceived(struct __pyx_obj_6sample_SampleProtocol *__pyx_v_self,char (*__pyx_v_buffer),int __pyx_v_buflen) {
  char (*__pyx_v_line_end);
  char (*__pyx_v_line);
  int __pyx_v_line_len;
  long __pyx_1;
  int __pyx_2;
  PyObject *__pyx_3 = 0;
  PyObject *__pyx_4 = 0;
  PyObject *__pyx_5 = 0;
  Py_INCREF((PyObject *)__pyx_v_self);

  /* "/home/itamar/devel/python/Twisted/sandbox/itamar/creactor/sample.pyx":30 */
  __pyx_v_self->readlen = (__pyx_v_self->readlen + __pyx_v_buflen);

  /* "/home/itamar/devel/python/Twisted/sandbox/itamar/creactor/sample.pyx":31 */
  while (1) {
    __pyx_L2:;
    __pyx_1 = 1;
    if (!__pyx_1) break;

    /* "/home/itamar/devel/python/Twisted/sandbox/itamar/creactor/sample.pyx":32 */
    __pyx_v_line_end = ((char (*))memchr(__pyx_v_self->readbuf,'\n',__pyx_v_self->readlen));

    /* "/home/itamar/devel/python/Twisted/sandbox/itamar/creactor/sample.pyx":33 */
    __pyx_2 = (__pyx_v_line_end != 0);
    if (__pyx_2) {

      /* "/home/itamar/devel/python/Twisted/sandbox/itamar/creactor/sample.pyx":34 */
      __pyx_v_line_len = ((__pyx_v_line_end - __pyx_v_self->readbuf) + 1);

      /* "/home/itamar/devel/python/Twisted/sandbox/itamar/creactor/sample.pyx":35 */
      strncpy(__pyx_v_line,__pyx_v_self->readbuf,__pyx_v_line_len);

      /* "/home/itamar/devel/python/Twisted/sandbox/itamar/creactor/sample.pyx":36 */
      __pyx_v_self->readbuf = (__pyx_v_self->readbuf + __pyx_v_line_len);

      /* "/home/itamar/devel/python/Twisted/sandbox/itamar/creactor/sample.pyx":37 */
      __pyx_v_self->readlen = (__pyx_v_self->readlen - __pyx_v_line_len);

      /* "/home/itamar/devel/python/Twisted/sandbox/itamar/creactor/sample.pyx":38 */
      ((struct __pyx_vtabstruct_6sample_SampleProtocol *)__pyx_v_self->__pyx_vtab)->lineReceived(__pyx_v_self,__pyx_v_line,__pyx_v_line_len);
      goto __pyx_L4;
    }
    /*else*/ {

      /* "/home/itamar/devel/python/Twisted/sandbox/itamar/creactor/sample.pyx":40 */
      goto __pyx_L3;
    }
    __pyx_L4:;
  }
  __pyx_L3:;

  /* "/home/itamar/devel/python/Twisted/sandbox/itamar/creactor/sample.pyx":41 */
  __pyx_2 = (__pyx_v_self->readbuf != __pyx_v_self->buf);
  if (__pyx_2) {
    __pyx_3 = PyObject_GetAttr(((PyObject *)__pyx_v_self), __pyx_n_buffer); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 41; goto __pyx_L1;}
    __pyx_4 = PyInt_FromLong(100000); if (!__pyx_4) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 41; goto __pyx_L1;}
    __pyx_5 = PyNumber_Add(__pyx_3, __pyx_4); if (!__pyx_5) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 41; goto __pyx_L1;}
    Py_DECREF(__pyx_3); __pyx_3 = 0;
    Py_DECREF(__pyx_4); __pyx_4 = 0;
    __pyx_3 = PyString_FromString(__pyx_v_self->readbuf); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 41; goto __pyx_L1;}
    __pyx_4 = PyNumber_Subtract(__pyx_5, __pyx_3); if (!__pyx_4) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 41; goto __pyx_L1;}
    Py_DECREF(__pyx_5); __pyx_5 = 0;
    Py_DECREF(__pyx_3); __pyx_3 = 0;
    __pyx_5 = PyInt_FromLong(__pyx_v_self->readlen); if (!__pyx_5) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 41; goto __pyx_L1;}
    __pyx_3 = PyNumber_Subtract(__pyx_4, __pyx_5); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 41; goto __pyx_L1;}
    Py_DECREF(__pyx_4); __pyx_4 = 0;
    Py_DECREF(__pyx_5); __pyx_5 = 0;
    __pyx_4 = PyInt_FromLong(8192); if (!__pyx_4) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 41; goto __pyx_L1;}
    if (PyObject_Cmp(__pyx_3, __pyx_4, &__pyx_2) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 41; goto __pyx_L1;}
    __pyx_2 = __pyx_2 < 0;
    Py_DECREF(__pyx_3); __pyx_3 = 0;
    Py_DECREF(__pyx_4); __pyx_4 = 0;
  }
  if (__pyx_2) {

    /* "/home/itamar/devel/python/Twisted/sandbox/itamar/creactor/sample.pyx":42 */
    strncpy(__pyx_v_self->buf,__pyx_v_self->readbuf,__pyx_v_self->readlen);

    /* "/home/itamar/devel/python/Twisted/sandbox/itamar/creactor/sample.pyx":43 */
    __pyx_v_self->readbuf = __pyx_v_self->buf;
    goto __pyx_L5;
  }
  __pyx_L5:;

  goto __pyx_L0;
  __pyx_L1:;
  Py_XDECREF(__pyx_3);
  Py_XDECREF(__pyx_4);
  Py_XDECREF(__pyx_5);
  __Pyx_WriteUnraisable("sample.SampleProtocol.cdataReceived");
  __pyx_L0:;
  Py_DECREF((PyObject *)__pyx_v_self);
}

static void __pyx_f_6sample_14SampleProtocol_lineReceived(struct __pyx_obj_6sample_SampleProtocol *__pyx_v_self,char (*__pyx_v_line),int __pyx_v_size) {
  Py_INCREF((PyObject *)__pyx_v_self);

  /* "/home/itamar/devel/python/Twisted/sandbox/itamar/creactor/sample.pyx":46 */
  __pyx_v_self->counter = (__pyx_v_self->counter + 1);

  /* "/home/itamar/devel/python/Twisted/sandbox/itamar/creactor/sample.pyx":47 */
  free(__pyx_v_line);

  goto __pyx_L0;
  __pyx_L1:;
  __Pyx_WriteUnraisable("sample.SampleProtocol.lineReceived");
  __pyx_L0:;
  Py_DECREF((PyObject *)__pyx_v_self);
}

static PyObject *__pyx_f_6sample_14SampleProtocol_connectionLost(PyObject *__pyx_v_self, PyObject *__pyx_args, PyObject *__pyx_kwds); /*proto*/
static PyObject *__pyx_f_6sample_14SampleProtocol_connectionLost(PyObject *__pyx_v_self, PyObject *__pyx_args, PyObject *__pyx_kwds) {
  PyObject *__pyx_v_reason = 0;
  PyObject *__pyx_r;
  PyObject *__pyx_1 = 0;
  static char *__pyx_argnames[] = {"reason",0};
  if (!PyArg_ParseTupleAndKeywords(__pyx_args, __pyx_kwds, "O", __pyx_argnames, &__pyx_v_reason)) return 0;
  Py_INCREF((PyObject *)__pyx_v_self);
  Py_INCREF(__pyx_v_reason);

  /* "/home/itamar/devel/python/Twisted/sandbox/itamar/creactor/sample.pyx":50 */
  __pyx_1 = PyInt_FromLong(((struct __pyx_obj_6sample_SampleProtocol *)__pyx_v_self)->counter); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 50; goto __pyx_L1;}
  if (__Pyx_PrintItem(__pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 50; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;
  if (__Pyx_PrintNewline() < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 50; goto __pyx_L1;}

  __pyx_r = Py_None; Py_INCREF(__pyx_r);
  goto __pyx_L0;
  __pyx_L1:;
  Py_XDECREF(__pyx_1);
  __Pyx_AddTraceback("sample.SampleProtocol.connectionLost");
  __pyx_r = 0;
  __pyx_L0:;
  Py_DECREF((PyObject *)__pyx_v_self);
  Py_DECREF(__pyx_v_reason);
  return __pyx_r;
}

static __Pyx_InternTabEntry __pyx_intern_tab[] = {
  {&__pyx_n_buffer, "buffer"},
  {&__pyx_n_setBuffer, "setBuffer"},
  {&__pyx_n_tcp, "tcp"},
  {&__pyx_n_transport, "transport"},
  {0, 0}
};
static struct __pyx_vtabstruct_6sample_SampleProtocol __pyx_vtable_6sample_SampleProtocol;

static PyObject *__pyx_tp_new_6sample_SampleProtocol(PyTypeObject *t, PyObject *a, PyObject *k) {
  PyObject *o = __pyx_ptype_3tcp_CProtocol->tp_new(t, a, k);
  struct __pyx_obj_6sample_SampleProtocol *p = (struct __pyx_obj_6sample_SampleProtocol *)o;
  (struct __pyx_vtabstruct_6sample_SampleProtocol *)p->__pyx_vtab = __pyx_vtabptr_6sample_SampleProtocol;
  return o;
}

static void __pyx_tp_dealloc_6sample_SampleProtocol(PyObject *o) {
  struct __pyx_obj_6sample_SampleProtocol *p = (struct __pyx_obj_6sample_SampleProtocol *)o;
  __pyx_ptype_3tcp_CProtocol->tp_dealloc(o);
}

static int __pyx_tp_traverse_6sample_SampleProtocol(PyObject *o, visitproc v, void *a) {
  int e;
  struct __pyx_obj_6sample_SampleProtocol *p = (struct __pyx_obj_6sample_SampleProtocol *)o;
  __pyx_ptype_3tcp_CProtocol->tp_traverse(o, v, a);
  return 0;
}

static int __pyx_tp_clear_6sample_SampleProtocol(PyObject *o) {
  struct __pyx_obj_6sample_SampleProtocol *p = (struct __pyx_obj_6sample_SampleProtocol *)o;
  __pyx_ptype_3tcp_CProtocol->tp_clear(o);
  return 0;
}

static struct PyMethodDef __pyx_methods_6sample_SampleProtocol[] = {
  {"connectionMade", (PyCFunction)__pyx_f_6sample_14SampleProtocol_connectionMade, METH_VARARGS|METH_KEYWORDS, 0},
  {"connectionLost", (PyCFunction)__pyx_f_6sample_14SampleProtocol_connectionLost, METH_VARARGS|METH_KEYWORDS, 0},
  {0, 0, 0, 0}
};

static PyNumberMethods __pyx_tp_as_number_SampleProtocol = {
  0, /*nb_add*/
  0, /*nb_subtract*/
  0, /*nb_multiply*/
  0, /*nb_divide*/
  0, /*nb_remainder*/
  0, /*nb_divmod*/
  0, /*nb_power*/
  0, /*nb_negative*/
  0, /*nb_positive*/
  0, /*nb_absolute*/
  0, /*nb_nonzero*/
  0, /*nb_invert*/
  0, /*nb_lshift*/
  0, /*nb_rshift*/
  0, /*nb_and*/
  0, /*nb_xor*/
  0, /*nb_or*/
  0, /*nb_coerce*/
  0, /*nb_int*/
  0, /*nb_long*/
  0, /*nb_float*/
  0, /*nb_oct*/
  0, /*nb_hex*/
  0, /*nb_inplace_add*/
  0, /*nb_inplace_subtract*/
  0, /*nb_inplace_multiply*/
  0, /*nb_inplace_divide*/
  0, /*nb_inplace_remainder*/
  0, /*nb_inplace_power*/
  0, /*nb_inplace_lshift*/
  0, /*nb_inplace_rshift*/
  0, /*nb_inplace_and*/
  0, /*nb_inplace_xor*/
  0, /*nb_inplace_or*/
  0, /*nb_floor_divide*/
  0, /*nb_true_divide*/
  0, /*nb_inplace_floor_divide*/
  0, /*nb_inplace_true_divide*/
};

static PySequenceMethods __pyx_tp_as_sequence_SampleProtocol = {
  0, /*sq_length*/
  0, /*sq_concat*/
  0, /*sq_repeat*/
  0, /*sq_item*/
  0, /*sq_slice*/
  0, /*sq_ass_item*/
  0, /*sq_ass_slice*/
  0, /*sq_contains*/
  0, /*sq_inplace_concat*/
  0, /*sq_inplace_repeat*/
};

static PyMappingMethods __pyx_tp_as_mapping_SampleProtocol = {
  0, /*mp_length*/
  0, /*mp_subscript*/
  0, /*mp_ass_subscript*/
};

static PyBufferProcs __pyx_tp_as_buffer_SampleProtocol = {
  0, /*bf_getreadbuffer*/
  0, /*bf_getwritebuffer*/
  0, /*bf_getsegcount*/
  0, /*bf_getcharbuffer*/
};

statichere PyTypeObject __pyx_type_6sample_SampleProtocol = {
  PyObject_HEAD_INIT(0)
  0, /*ob_size*/
  "sample.SampleProtocol", /*tp_name*/
  sizeof(struct __pyx_obj_6sample_SampleProtocol), /*tp_basicsize*/
  0, /*tp_itemsize*/
  __pyx_tp_dealloc_6sample_SampleProtocol, /*tp_dealloc*/
  0, /*tp_print*/
  0, /*tp_getattr*/
  0, /*tp_setattr*/
  0, /*tp_compare*/
  0, /*tp_repr*/
  &__pyx_tp_as_number_SampleProtocol, /*tp_as_number*/
  &__pyx_tp_as_sequence_SampleProtocol, /*tp_as_sequence*/
  &__pyx_tp_as_mapping_SampleProtocol, /*tp_as_mapping*/
  0, /*tp_hash*/
  0, /*tp_call*/
  0, /*tp_str*/
  0, /*tp_getattro*/
  0, /*tp_setattro*/
  &__pyx_tp_as_buffer_SampleProtocol, /*tp_as_buffer*/
  Py_TPFLAGS_DEFAULT|Py_TPFLAGS_CHECKTYPES|Py_TPFLAGS_BASETYPE, /*tp_flags*/
  "Count line size. Assumes lines smaller than 8192 bytes.", /*tp_doc*/
  __pyx_tp_traverse_6sample_SampleProtocol, /*tp_traverse*/
  __pyx_tp_clear_6sample_SampleProtocol, /*tp_clear*/
  0, /*tp_richcompare*/
  0, /*tp_weaklistoffset*/
  0, /*tp_iter*/
  0, /*tp_iternext*/
  __pyx_methods_6sample_SampleProtocol, /*tp_methods*/
  0, /*tp_members*/
  0, /*tp_getset*/
  0, /*tp_base*/
  0, /*tp_dict*/
  0, /*tp_descr_get*/
  0, /*tp_descr_set*/
  0, /*tp_dictoffset*/
  0, /*tp_init*/
  0, /*tp_alloc*/
  __pyx_tp_new_6sample_SampleProtocol, /*tp_new*/
  0, /*tp_free*/
  0, /*tp_is_gc*/
  0, /*tp_bases*/
  0, /*tp_mro*/
  0, /*tp_cache*/
  0, /*tp_subclasses*/
  0, /*tp_weaklist*/
};

static struct PyMethodDef __pyx_methods[] = {
  {0, 0, 0, 0}
};

DL_EXPORT(void) initsample(void); /*proto*/
DL_EXPORT(void) initsample(void) {
  __pyx_m = Py_InitModule4("sample", __pyx_methods, 0, 0, PYTHON_API_VERSION);
  if (!__pyx_m) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 1; goto __pyx_L1;};
  __pyx_b = PyImport_AddModule("__builtin__");
  if (!__pyx_b) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 1; goto __pyx_L1;};
  if (PyObject_SetAttrString(__pyx_m, "__builtins__", __pyx_b) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 1; goto __pyx_L1;};
  if (__Pyx_InternStrings(__pyx_intern_tab) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 1; goto __pyx_L1;};
  __pyx_ptype_3tcp__CMixin = __Pyx_ImportType("tcp", "_CMixin", sizeof(struct __pyx_obj_3tcp__CMixin)); if (!__pyx_ptype_3tcp__CMixin) {__pyx_filename = __pyx_f[1]; __pyx_lineno = 5; goto __pyx_L1;}
  __pyx_ptype_3tcp_CProtocol = __Pyx_ImportType("tcp", "CProtocol", sizeof(struct __pyx_obj_3tcp_CProtocol)); if (!__pyx_ptype_3tcp_CProtocol) {__pyx_filename = __pyx_f[1]; __pyx_lineno = 14; goto __pyx_L1;}
  __pyx_vtabptr_6sample_SampleProtocol = &__pyx_vtable_6sample_SampleProtocol;
  __pyx_vtable_6sample_SampleProtocol.__pyx_base.cdataReceived = (void *)__pyx_f_6sample_14SampleProtocol_cdataReceived;
  __pyx_vtable_6sample_SampleProtocol.lineReceived = (void *)__pyx_f_6sample_14SampleProtocol_lineReceived;
  __pyx_type_6sample_SampleProtocol.tp_base = __pyx_ptype_3tcp_CProtocol;
  if (PyType_Ready(&__pyx_type_6sample_SampleProtocol) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 11; goto __pyx_L1;}
  if (__Pyx_SetVtable(__pyx_type_6sample_SampleProtocol.tp_dict, __pyx_vtabptr_6sample_SampleProtocol) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 11; goto __pyx_L1;}
  if (PyObject_SetAttrString(__pyx_m, "SampleProtocol", (PyObject *)&__pyx_type_6sample_SampleProtocol) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 11; goto __pyx_L1;}
  __pyx_ptype_6sample_SampleProtocol = &__pyx_type_6sample_SampleProtocol;

  /* "/home/itamar/devel/python/Twisted/sandbox/itamar/creactor/sample.pyx":49 */
  return;
  __pyx_L1:;
  __Pyx_AddTraceback("sample");
}

static char *__pyx_filenames[] = {
  "sample.pyx",
  "tcp.pxd",
};
statichere char **__pyx_f = __pyx_filenames;

/* Runtime support code */

static void __Pyx_WriteUnraisable(char *name) {
    PyObject *old_exc, *old_val, *old_tb;
    PyObject *ctx;
    PyErr_Fetch(&old_exc, &old_val, &old_tb);
    ctx = PyString_FromString(name);
    PyErr_Restore(old_exc, old_val, old_tb);
    if (!ctx)
        ctx = Py_None;
    PyErr_WriteUnraisable(ctx);
}

static PyObject *__Pyx_GetStdout(void) {
    PyObject *f = PySys_GetObject("stdout");
    if (!f) {
        PyErr_SetString(PyExc_RuntimeError, "lost sys.stdout");
    }
    return f;
}

static int __Pyx_PrintItem(PyObject *v) {
    PyObject *f;
    
    if (!(f = __Pyx_GetStdout()))
        return -1;
    if (PyFile_SoftSpace(f, 1)) {
        if (PyFile_WriteString(" ", f) < 0)
            return -1;
    }
    if (PyFile_WriteObject(v, f, Py_PRINT_RAW) < 0)
        return -1;
    if (PyString_Check(v)) {
        char *s = PyString_AsString(v);
        int len = PyString_Size(v);
        if (len > 0 &&
            isspace(Py_CHARMASK(s[len-1])) &&
            s[len-1] != ' ')
                PyFile_SoftSpace(f, 0);
    }
    return 0;
}

static int __Pyx_PrintNewline(void) {
    PyObject *f;
    
    if (!(f = __Pyx_GetStdout()))
        return -1;
    if (PyFile_WriteString("\n", f) < 0)
        return -1;
    PyFile_SoftSpace(f, 0);
    return 0;
}

static int __Pyx_InternStrings(__Pyx_InternTabEntry *t) {
    while (t->p) {
        *t->p = PyString_InternFromString(t->s);
        if (!*t->p)
            return -1;
        ++t;
    }
    return 0;
}

static PyTypeObject *__Pyx_ImportType(char *module_name, char *class_name, 
    long size) 
{
    PyObject *py_module_name = 0;
    PyObject *py_class_name = 0;
    PyObject *py_name_list = 0;
    PyObject *py_module = 0;
    PyObject *result = 0;
    
    py_module_name = PyString_FromString(module_name);
    if (!py_module_name)
        goto bad;
    py_class_name = PyString_FromString(class_name);
    if (!py_class_name)
        goto bad;
    py_name_list = PyList_New(1);
    if (!py_name_list)
        goto bad;
    Py_INCREF(py_class_name);
    if (PyList_SetItem(py_name_list, 0, py_class_name) < 0)
        goto bad;
    py_module = __Pyx_Import(py_module_name, py_name_list);
    if (!py_module)
        goto bad;
    result = PyObject_GetAttr(py_module, py_class_name);
    if (!result)
        goto bad;
    if (!PyType_Check(result)) {
        PyErr_Format(PyExc_TypeError, 
            "%s.%s is not a type object",
            module_name, class_name);
        goto bad;
    }
    if (((PyTypeObject *)result)->tp_basicsize != size) {
        PyErr_Format(PyExc_ValueError, 
            "%s.%s does not appear to be the correct type object",
            module_name, class_name);
        goto bad;
    }
    goto done;
bad:
    Py_XDECREF(result);
    result = 0;
done:
    Py_XDECREF(py_module_name);
    Py_XDECREF(py_class_name);
    Py_XDECREF(py_name_list);
    return (PyTypeObject *)result;
}

static PyObject *__Pyx_Import(PyObject *name, PyObject *from_list) {
    PyObject *__import__ = 0;
    PyObject *empty_list = 0;
    PyObject *module = 0;
    PyObject *global_dict = 0;
    PyObject *empty_dict = 0;
    PyObject *list;
    __import__ = PyObject_GetAttrString(__pyx_b, "__import__");
    if (!__import__)
        goto bad;
    if (from_list)
        list = from_list;
    else {
        empty_list = PyList_New(0);
        if (!empty_list)
            goto bad;
        list = empty_list;
    }
    global_dict = PyModule_GetDict(__pyx_m);
    if (!global_dict)
        goto bad;
    empty_dict = PyDict_New();
    if (!empty_dict)
        goto bad;
    module = PyObject_CallFunction(__import__, "OOOO",
        name, global_dict, empty_dict, list);
bad:
    Py_XDECREF(empty_list);
    Py_XDECREF(__import__);
    Py_XDECREF(empty_dict);
    return module;
}

static int __Pyx_SetVtable(PyObject *dict, void *vtable) {
    PyObject *pycobj = 0;
    int result;
    
    pycobj = PyCObject_FromVoidPtr(vtable, 0);
    if (!pycobj)
        goto bad;
    if (PyDict_SetItemString(dict, "__pyx__vtable__", pycobj) < 0)
        goto bad;
    result = 0;
    goto done;

bad:
    result = -1;
done:
    Py_XDECREF(pycobj);
    return result;
}

#include "compile.h"
#include "frameobject.h"
#include "traceback.h"

static void __Pyx_AddTraceback(char *funcname) {
    PyObject *py_srcfile = 0;
    PyObject *py_funcname = 0;
    PyObject *py_globals = 0;
    PyObject *empty_tuple = 0;
    PyObject *empty_string = 0;
    PyCodeObject *py_code = 0;
    PyFrameObject *py_frame = 0;
    
    py_srcfile = PyString_FromString(__pyx_filename);
    if (!py_srcfile) goto bad;
    py_funcname = PyString_FromString(funcname);
    if (!py_funcname) goto bad;
    py_globals = PyModule_GetDict(__pyx_m);
    if (!py_globals) goto bad;
    empty_tuple = PyTuple_New(0);
    if (!empty_tuple) goto bad;
    empty_string = PyString_FromString("");
    if (!empty_string) goto bad;
    py_code = PyCode_New(
        0,            /*int argcount,*/
        0,            /*int nlocals,*/
        0,            /*int stacksize,*/
        0,            /*int flags,*/
        empty_string, /*PyObject *code,*/
        empty_tuple,  /*PyObject *consts,*/
        empty_tuple,  /*PyObject *names,*/
        empty_tuple,  /*PyObject *varnames,*/
        empty_tuple,  /*PyObject *freevars,*/
        empty_tuple,  /*PyObject *cellvars,*/
        py_srcfile,   /*PyObject *filename,*/
        py_funcname,  /*PyObject *name,*/
        __pyx_lineno,   /*int firstlineno,*/
        empty_string  /*PyObject *lnotab*/
    );
    if (!py_code) goto bad;
    py_frame = PyFrame_New(
        PyThreadState_Get(), /*PyThreadState *tstate,*/
        py_code,             /*PyCodeObject *code,*/
        py_globals,          /*PyObject *globals,*/
        0                    /*PyObject *locals*/
    );
    if (!py_frame) goto bad;
    py_frame->f_lineno = __pyx_lineno;
    PyTraceBack_Here(py_frame);
bad:
    Py_XDECREF(py_srcfile);
    Py_XDECREF(py_funcname);
    Py_XDECREF(empty_tuple);
    Py_XDECREF(empty_string);
    Py_XDECREF(py_code);
    Py_XDECREF(py_frame);
}