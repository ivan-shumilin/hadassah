! function(e, t) {
  "use strict";
  "object" == typeof module && "object" == typeof module.exports ? module.exports = e.document ? t(e, !0) : function(e) {
    if (!e.document) throw new Error("jQuery requires a window with a document");
    return t(e)
  } : t(e)
}("undefined" != typeof window ? window : this, (function(e, t) {
  "use strict";
  var n = [],
    r = Object.getPrototypeOf,
    i = n.slice,
    o = n.flat ? function(e) {
      return n.flat.call(e)
    } : function(e) {
      return n.concat.apply([], e)
    },
    a = n.push,
    s = n.indexOf,
    l = {},
    c = l.toString,
    u = l.hasOwnProperty,
    d = u.toString,
    p = d.call(Object),
    f = {},
    h = function(e) {
      return "function" == typeof e && "number" != typeof e.nodeType
    },
    m = function(e) {
      return null != e && e === e.window
    },
    g = e.document,
    v = {
      type: !0,
      src: !0,
      nonce: !0,
      noModule: !0
    };

  function y(e, t, n) {
    var r, i, o = (n = n || g).createElement("script");
    if (o.text = e, t)
      for (r in v)(i = t[r] || t.getAttribute && t.getAttribute(r)) && o.setAttribute(r, i);
    n.head.appendChild(o).parentNode.removeChild(o)
  }

  function b(e) {
    return null == e ? e + "" : "object" == typeof e || "function" == typeof e ? l[c.call(e)] || "object" : typeof e
  }
  var w = "3.5.1",
    x = function(e, t) {
      return new x.fn.init(e, t)
    };

  function S(e) {
    var t = !!e && "length" in e && e.length,
      n = b(e);
    return !h(e) && !m(e) && ("array" === n || 0 === t || "number" == typeof t && 0 < t && t - 1 in e)
  }
  x.fn = x.prototype = {
    jquery: w,
    constructor: x,
    length: 0,
    toArray: function() {
      return i.call(this)
    },
    get: function(e) {
      return null == e ? i.call(this) : e < 0 ? this[e + this.length] : this[e]
    },
    pushStack: function(e) {
      var t = x.merge(this.constructor(), e);
      return t.prevObject = this, t
    },
    each: function(e) {
      return x.each(this, e)
    },
    map: function(e) {
      return this.pushStack(x.map(this, (function(t, n) {
        return e.call(t, n, t)
      })))
    },
    slice: function() {
      return this.pushStack(i.apply(this, arguments))
    },
    first: function() {
      return this.eq(0)
    },
    last: function() {
      return this.eq(-1)
    },
    even: function() {
      return this.pushStack(x.grep(this, (function(e, t) {
        return (t + 1) % 2
      })))
    },
    odd: function() {
      return this.pushStack(x.grep(this, (function(e, t) {
        return t % 2
      })))
    },
    eq: function(e) {
      var t = this.length,
        n = +e + (e < 0 ? t : 0);
      return this.pushStack(0 <= n && n < t ? [this[n]] : [])
    },
    end: function() {
      return this.prevObject || this.constructor()
    },
    push: a,
    sort: n.sort,
    splice: n.splice
  }, x.extend = x.fn.extend = function() {
    var e, t, n, r, i, o, a = arguments[0] || {},
      s = 1,
      l = arguments.length,
      c = !1;
    for ("boolean" == typeof a && (c = a, a = arguments[s] || {}, s++), "object" == typeof a || h(a) || (a = {}), s === l && (a = this, s--); s < l; s++)
      if (null != (e = arguments[s]))
        for (t in e) r = e[t], "__proto__" !== t && a !== r && (c && r && (x.isPlainObject(r) || (i = Array.isArray(r))) ? (n = a[t], o = i && !Array.isArray(n) ? [] : i || x.isPlainObject(n) ? n : {}, i = !1, a[t] = x.extend(c, o, r)) : void 0 !== r && (a[t] = r));
    return a
  }, x.extend({
    expando: "jQuery" + (w + Math.random()).replace(/\D/g, ""),
    isReady: !0,
    error: function(e) {
      throw new Error(e)
    },
    noop: function() {},
    isPlainObject: function(e) {
      var t, n;
      return !(!e || "[object Object]" !== c.call(e) || (t = r(e)) && ("function" != typeof(n = u.call(t, "constructor") && t.constructor) || d.call(n) !== p))
    },
    isEmptyObject: function(e) {
      var t;
      for (t in e) return !1;
      return !0
    },
    globalEval: function(e, t, n) {
      y(e, {
        nonce: t && t.nonce
      }, n)
    },
    each: function(e, t) {
      var n, r = 0;
      if (S(e))
        for (n = e.length; r < n && !1 !== t.call(e[r], r, e[r]); r++);
      else
        for (r in e)
          if (!1 === t.call(e[r], r, e[r])) break;
      return e
    },
    makeArray: function(e, t) {
      var n = t || [];
      return null != e && (S(Object(e)) ? x.merge(n, "string" == typeof e ? [e] : e) : a.call(n, e)), n
    },
    inArray: function(e, t, n) {
      return null == t ? -1 : s.call(t, e, n)
    },
    merge: function(e, t) {
      for (var n = +t.length, r = 0, i = e.length; r < n; r++) e[i++] = t[r];
      return e.length = i, e
    },
    grep: function(e, t, n) {
      for (var r = [], i = 0, o = e.length, a = !n; i < o; i++) !t(e[i], i) !== a && r.push(e[i]);
      return r
    },
    map: function(e, t, n) {
      var r, i, a = 0,
        s = [];
      if (S(e))
        for (r = e.length; a < r; a++) null != (i = t(e[a], a, n)) && s.push(i);
      else
        for (a in e) null != (i = t(e[a], a, n)) && s.push(i);
      return o(s)
    },
    guid: 1,
    support: f
  }), "function" == typeof Symbol && (x.fn[Symbol.iterator] = n[Symbol.iterator]), x.each("Boolean Number String Function Array Date RegExp Object Error Symbol".split(" "), (function(e, t) {
    l["[object " + t + "]"] = t.toLowerCase()
  }));
  var C = function(e) {
    var t, n, r, i, o, a, s, l, c, u, d, p, f, h, m, g, v, y, b, w = "sizzle" + 1 * new Date,
      x = e.document,
      S = 0,
      C = 0,
      E = le(),
      T = le(),
      k = le(),
      D = le(),
      O = function(e, t) {
        return e === t && (d = !0), 0
      },
      A = {}.hasOwnProperty,
      _ = [],
      M = _.pop,
      L = _.push,
      I = _.push,
      P = _.slice,
      j = function(e, t) {
        for (var n = 0, r = e.length; n < r; n++)
          if (e[n] === t) return n;
        return -1
      },
      N = "checked|selected|async|autofocus|autoplay|controls|defer|disabled|hidden|ismap|loop|multiple|open|readonly|required|scoped",
      z = "[\\x20\\t\\r\\n\\f]",
      R = "(?:\\\\[\\da-fA-F]{1,6}" + z + "?|\\\\[^\\r\\n\\f]|[\\w-]|[^\0-\\x7f])+",
      $ = "\\[" + z + "*(" + R + ")(?:" + z + "*([*^$|!~]?=)" + z + "*(?:'((?:\\\\.|[^\\\\'])*)'|\"((?:\\\\.|[^\\\\\"])*)\"|(" + R + "))|)" + z + "*\\]",
      H = ":(" + R + ")(?:\\((('((?:\\\\.|[^\\\\'])*)'|\"((?:\\\\.|[^\\\\\"])*)\")|((?:\\\\.|[^\\\\()[\\]]|" + $ + ")*)|.*)\\)|)",
      F = new RegExp(z + "+", "g"),
      B = new RegExp("^" + z + "+|((?:^|[^\\\\])(?:\\\\.)*)" + z + "+$", "g"),
      q = new RegExp("^" + z + "*," + z + "*"),
      W = new RegExp("^" + z + "*([>+~]|" + z + ")" + z + "*"),
      Y = new RegExp(z + "|>"),
      U = new RegExp(H),
      V = new RegExp("^" + R + "$"),
      X = {
        ID: new RegExp("^#(" + R + ")"),
        CLASS: new RegExp("^\\.(" + R + ")"),
        TAG: new RegExp("^(" + R + "|[*])"),
        ATTR: new RegExp("^" + $),
        PSEUDO: new RegExp("^" + H),
        CHILD: new RegExp("^:(only|first|last|nth|nth-last)-(child|of-type)(?:\\(" + z + "*(even|odd|(([+-]|)(\\d*)n|)" + z + "*(?:([+-]|)" + z + "*(\\d+)|))" + z + "*\\)|)", "i"),
        bool: new RegExp("^(?:" + N + ")$", "i"),
        needsContext: new RegExp("^" + z + "*[>+~]|:(even|odd|eq|gt|lt|nth|first|last)(?:\\(" + z + "*((?:-\\d)?\\d*)" + z + "*\\)|)(?=[^-]|$)", "i")
      },
      G = /HTML$/i,
      Z = /^(?:input|select|textarea|button)$/i,
      K = /^h\d$/i,
      J = /^[^{]+\{\s*\[native \w/,
      Q = /^(?:#([\w-]+)|(\w+)|\.([\w-]+))$/,
      ee = /[+~]/,
      te = new RegExp("\\\\[\\da-fA-F]{1,6}" + z + "?|\\\\([^\\r\\n\\f])", "g"),
      ne = function(e, t) {
        var n = "0x" + e.slice(1) - 65536;
        return t || (n < 0 ? String.fromCharCode(n + 65536) : String.fromCharCode(n >> 10 | 55296, 1023 & n | 56320))
      },
      re = /([\0-\x1f\x7f]|^-?\d)|^-$|[^\0-\x1f\x7f-\uFFFF\w-]/g,
      ie = function(e, t) {
        return t ? "\0" === e ? "�" : e.slice(0, -1) + "\\" + e.charCodeAt(e.length - 1).toString(16) + " " : "\\" + e
      },
      oe = function() {
        p()
      },
      ae = we((function(e) {
        return !0 === e.disabled && "fieldset" === e.nodeName.toLowerCase()
      }), {
        dir: "parentNode",
        next: "legend"
      });
    try {
      I.apply(_ = P.call(x.childNodes), x.childNodes), _[x.childNodes.length].nodeType
    } catch (t) {
      I = {
        apply: _.length ? function(e, t) {
          L.apply(e, P.call(t))
        } : function(e, t) {
          for (var n = e.length, r = 0; e[n++] = t[r++];);
          e.length = n - 1
        }
      }
    }

    function se(e, t, r, i) {
      var o, s, c, u, d, h, v, y = t && t.ownerDocument,
        x = t ? t.nodeType : 9;
      if (r = r || [], "string" != typeof e || !e || 1 !== x && 9 !== x && 11 !== x) return r;
      if (!i && (p(t), t = t || f, m)) {
        if (11 !== x && (d = Q.exec(e)))
          if (o = d[1]) {
            if (9 === x) {
              if (!(c = t.getElementById(o))) return r;
              if (c.id === o) return r.push(c), r
            } else if (y && (c = y.getElementById(o)) && b(t, c) && c.id === o) return r.push(c), r
          } else {
            if (d[2]) return I.apply(r, t.getElementsByTagName(e)), r;
            if ((o = d[3]) && n.getElementsByClassName && t.getElementsByClassName) return I.apply(r, t.getElementsByClassName(o)), r
          } if (n.qsa && !D[e + " "] && (!g || !g.test(e)) && (1 !== x || "object" !== t.nodeName.toLowerCase())) {
          if (v = e, y = t, 1 === x && (Y.test(e) || W.test(e))) {
            for ((y = ee.test(e) && ve(t.parentNode) || t) === t && n.scope || ((u = t.getAttribute("id")) ? u = u.replace(re, ie) : t.setAttribute("id", u = w)), s = (h = a(e)).length; s--;) h[s] = (u ? "#" + u : ":scope") + " " + be(h[s]);
            v = h.join(",")
          }
          try {
            return I.apply(r, y.querySelectorAll(v)), r
          } catch (t) {
            D(e, !0)
          } finally {
            u === w && t.removeAttribute("id")
          }
        }
      }
      return l(e.replace(B, "$1"), t, r, i)
    }

    function le() {
      var e = [];
      return function t(n, i) {
        return e.push(n + " ") > r.cacheLength && delete t[e.shift()], t[n + " "] = i
      }
    }

    function ce(e) {
      return e[w] = !0, e
    }

    function ue(e) {
      var t = f.createElement("fieldset");
      try {
        return !!e(t)
      } catch (e) {
        return !1
      } finally {
        t.parentNode && t.parentNode.removeChild(t), t = null
      }
    }

    function de(e, t) {
      for (var n = e.split("|"), i = n.length; i--;) r.attrHandle[n[i]] = t
    }

    function pe(e, t) {
      var n = t && e,
        r = n && 1 === e.nodeType && 1 === t.nodeType && e.sourceIndex - t.sourceIndex;
      if (r) return r;
      if (n)
        for (; n = n.nextSibling;)
          if (n === t) return -1;
      return e ? 1 : -1
    }

    function fe(e) {
      return function(t) {
        return "input" === t.nodeName.toLowerCase() && t.type === e
      }
    }

    function he(e) {
      return function(t) {
        var n = t.nodeName.toLowerCase();
        return ("input" === n || "button" === n) && t.type === e
      }
    }

    function me(e) {
      return function(t) {
        return "form" in t ? t.parentNode && !1 === t.disabled ? "label" in t ? "label" in t.parentNode ? t.parentNode.disabled === e : t.disabled === e : t.isDisabled === e || t.isDisabled !== !e && ae(t) === e : t.disabled === e : "label" in t && t.disabled === e
      }
    }

    function ge(e) {
      return ce((function(t) {
        return t = +t, ce((function(n, r) {
          for (var i, o = e([], n.length, t), a = o.length; a--;) n[i = o[a]] && (n[i] = !(r[i] = n[i]))
        }))
      }))
    }

    function ve(e) {
      return e && void 0 !== e.getElementsByTagName && e
    }
    for (t in n = se.support = {}, o = se.isXML = function(e) {
        var t = e.namespaceURI,
          n = (e.ownerDocument || e).documentElement;
        return !G.test(t || n && n.nodeName || "HTML")
      }, p = se.setDocument = function(e) {
        var t, i, a = e ? e.ownerDocument || e : x;
        return a != f && 9 === a.nodeType && a.documentElement && (h = (f = a).documentElement, m = !o(f), x != f && (i = f.defaultView) && i.top !== i && (i.addEventListener ? i.addEventListener("unload", oe, !1) : i.attachEvent && i.attachEvent("onunload", oe)), n.scope = ue((function(e) {
          return h.appendChild(e).appendChild(f.createElement("div")), void 0 !== e.querySelectorAll && !e.querySelectorAll(":scope fieldset div").length
        })), n.attributes = ue((function(e) {
          return e.className = "i", !e.getAttribute("className")
        })), n.getElementsByTagName = ue((function(e) {
          return e.appendChild(f.createComment("")), !e.getElementsByTagName("*").length
        })), n.getElementsByClassName = J.test(f.getElementsByClassName), n.getById = ue((function(e) {
          return h.appendChild(e).id = w, !f.getElementsByName || !f.getElementsByName(w).length
        })), n.getById ? (r.filter.ID = function(e) {
          var t = e.replace(te, ne);
          return function(e) {
            return e.getAttribute("id") === t
          }
        }, r.find.ID = function(e, t) {
          if (void 0 !== t.getElementById && m) {
            var n = t.getElementById(e);
            return n ? [n] : []
          }
        }) : (r.filter.ID = function(e) {
          var t = e.replace(te, ne);
          return function(e) {
            var n = void 0 !== e.getAttributeNode && e.getAttributeNode("id");
            return n && n.value === t
          }
        }, r.find.ID = function(e, t) {
          if (void 0 !== t.getElementById && m) {
            var n, r, i, o = t.getElementById(e);
            if (o) {
              if ((n = o.getAttributeNode("id")) && n.value === e) return [o];
              for (i = t.getElementsByName(e), r = 0; o = i[r++];)
                if ((n = o.getAttributeNode("id")) && n.value === e) return [o]
            }
            return []
          }
        }), r.find.TAG = n.getElementsByTagName ? function(e, t) {
          return void 0 !== t.getElementsByTagName ? t.getElementsByTagName(e) : n.qsa ? t.querySelectorAll(e) : void 0
        } : function(e, t) {
          var n, r = [],
            i = 0,
            o = t.getElementsByTagName(e);
          if ("*" === e) {
            for (; n = o[i++];) 1 === n.nodeType && r.push(n);
            return r
          }
          return o
        }, r.find.CLASS = n.getElementsByClassName && function(e, t) {
          if (void 0 !== t.getElementsByClassName && m) return t.getElementsByClassName(e)
        }, v = [], g = [], (n.qsa = J.test(f.querySelectorAll)) && (ue((function(e) {
          var t;
          h.appendChild(e).innerHTML = "<a id='" + w + "'></a><select id='" + w + "-\r\\' msallowcapture=''><option selected=''></option></select>", e.querySelectorAll("[msallowcapture^='']").length && g.push("[*^$]=" + z + "*(?:''|\"\")"), e.querySelectorAll("[selected]").length || g.push("\\[" + z + "*(?:value|" + N + ")"), e.querySelectorAll("[id~=" + w + "-]").length || g.push("~="), (t = f.createElement("input")).setAttribute("name", ""), e.appendChild(t), e.querySelectorAll("[name='']").length || g.push("\\[" + z + "*name" + z + "*=" + z + "*(?:''|\"\")"), e.querySelectorAll(":checked").length || g.push(":checked"), e.querySelectorAll("a#" + w + "+*").length || g.push(".#.+[+~]"), e.querySelectorAll("\\\f"), g.push("[\\r\\n\\f]")
        })), ue((function(e) {
          e.innerHTML = "<a href='' disabled='disabled'></a><select disabled='disabled'><option/></select>";
          var t = f.createElement("input");
          t.setAttribute("type", "hidden"), e.appendChild(t).setAttribute("name", "D"), e.querySelectorAll("[name=d]").length && g.push("name" + z + "*[*^$|!~]?="), 2 !== e.querySelectorAll(":enabled").length && g.push(":enabled", ":disabled"), h.appendChild(e).disabled = !0, 2 !== e.querySelectorAll(":disabled").length && g.push(":enabled", ":disabled"), e.querySelectorAll("*,:x"), g.push(",.*:")
        }))), (n.matchesSelector = J.test(y = h.matches || h.webkitMatchesSelector || h.mozMatchesSelector || h.oMatchesSelector || h.msMatchesSelector)) && ue((function(e) {
          n.disconnectedMatch = y.call(e, "*"), y.call(e, "[s!='']:x"), v.push("!=", H)
        })), g = g.length && new RegExp(g.join("|")), v = v.length && new RegExp(v.join("|")), t = J.test(h.compareDocumentPosition), b = t || J.test(h.contains) ? function(e, t) {
          var n = 9 === e.nodeType ? e.documentElement : e,
            r = t && t.parentNode;
          return e === r || !(!r || 1 !== r.nodeType || !(n.contains ? n.contains(r) : e.compareDocumentPosition && 16 & e.compareDocumentPosition(r)))
        } : function(e, t) {
          if (t)
            for (; t = t.parentNode;)
              if (t === e) return !0;
          return !1
        }, O = t ? function(e, t) {
          if (e === t) return d = !0, 0;
          var r = !e.compareDocumentPosition - !t.compareDocumentPosition;
          return r || (1 & (r = (e.ownerDocument || e) == (t.ownerDocument || t) ? e.compareDocumentPosition(t) : 1) || !n.sortDetached && t.compareDocumentPosition(e) === r ? e == f || e.ownerDocument == x && b(x, e) ? -1 : t == f || t.ownerDocument == x && b(x, t) ? 1 : u ? j(u, e) - j(u, t) : 0 : 4 & r ? -1 : 1)
        } : function(e, t) {
          if (e === t) return d = !0, 0;
          var n, r = 0,
            i = e.parentNode,
            o = t.parentNode,
            a = [e],
            s = [t];
          if (!i || !o) return e == f ? -1 : t == f ? 1 : i ? -1 : o ? 1 : u ? j(u, e) - j(u, t) : 0;
          if (i === o) return pe(e, t);
          for (n = e; n = n.parentNode;) a.unshift(n);
          for (n = t; n = n.parentNode;) s.unshift(n);
          for (; a[r] === s[r];) r++;
          return r ? pe(a[r], s[r]) : a[r] == x ? -1 : s[r] == x ? 1 : 0
        }), f
      }, se.matches = function(e, t) {
        return se(e, null, null, t)
      }, se.matchesSelector = function(e, t) {
        if (p(e), n.matchesSelector && m && !D[t + " "] && (!v || !v.test(t)) && (!g || !g.test(t))) try {
          var r = y.call(e, t);
          if (r || n.disconnectedMatch || e.document && 11 !== e.document.nodeType) return r
        } catch (e) {
          D(t, !0)
        }
        return 0 < se(t, f, null, [e]).length
      }, se.contains = function(e, t) {
        return (e.ownerDocument || e) != f && p(e), b(e, t)
      }, se.attr = function(e, t) {
        (e.ownerDocument || e) != f && p(e);
        var i = r.attrHandle[t.toLowerCase()],
          o = i && A.call(r.attrHandle, t.toLowerCase()) ? i(e, t, !m) : void 0;
        return void 0 !== o ? o : n.attributes || !m ? e.getAttribute(t) : (o = e.getAttributeNode(t)) && o.specified ? o.value : null
      }, se.escape = function(e) {
        return (e + "").replace(re, ie)
      }, se.error = function(e) {
        throw new Error("Syntax error, unrecognized expression: " + e)
      }, se.uniqueSort = function(e) {
        var t, r = [],
          i = 0,
          o = 0;
        if (d = !n.detectDuplicates, u = !n.sortStable && e.slice(0), e.sort(O), d) {
          for (; t = e[o++];) t === e[o] && (i = r.push(o));
          for (; i--;) e.splice(r[i], 1)
        }
        return u = null, e
      }, i = se.getText = function(e) {
        var t, n = "",
          r = 0,
          o = e.nodeType;
        if (o) {
          if (1 === o || 9 === o || 11 === o) {
            if ("string" == typeof e.textContent) return e.textContent;
            for (e = e.firstChild; e; e = e.nextSibling) n += i(e)
          } else if (3 === o || 4 === o) return e.nodeValue
        } else
          for (; t = e[r++];) n += i(t);
        return n
      }, (r = se.selectors = {
        cacheLength: 50,
        createPseudo: ce,
        match: X,
        attrHandle: {},
        find: {},
        relative: {
          ">": {
            dir: "parentNode",
            first: !0
          },
          " ": {
            dir: "parentNode"
          },
          "+": {
            dir: "previousSibling",
            first: !0
          },
          "~": {
            dir: "previousSibling"
          }
        },
        preFilter: {
          ATTR: function(e) {
            return e[1] = e[1].replace(te, ne), e[3] = (e[3] || e[4] || e[5] || "").replace(te, ne), "~=" === e[2] && (e[3] = " " + e[3] + " "), e.slice(0, 4)
          },
          CHILD: function(e) {
            return e[1] = e[1].toLowerCase(), "nth" === e[1].slice(0, 3) ? (e[3] || se.error(e[0]), e[4] = +(e[4] ? e[5] + (e[6] || 1) : 2 * ("even" === e[3] || "odd" === e[3])), e[5] = +(e[7] + e[8] || "odd" === e[3])) : e[3] && se.error(e[0]), e
          },
          PSEUDO: function(e) {
            var t, n = !e[6] && e[2];
            return X.CHILD.test(e[0]) ? null : (e[3] ? e[2] = e[4] || e[5] || "" : n && U.test(n) && (t = a(n, !0)) && (t = n.indexOf(")", n.length - t) - n.length) && (e[0] = e[0].slice(0, t), e[2] = n.slice(0, t)), e.slice(0, 3))
          }
        },
        filter: {
          TAG: function(e) {
            var t = e.replace(te, ne).toLowerCase();
            return "*" === e ? function() {
              return !0
            } : function(e) {
              return e.nodeName && e.nodeName.toLowerCase() === t
            }
          },
          CLASS: function(e) {
            var t = E[e + " "];
            return t || (t = new RegExp("(^|" + z + ")" + e + "(" + z + "|$)")) && E(e, (function(e) {
              return t.test("string" == typeof e.className && e.className || void 0 !== e.getAttribute && e.getAttribute("class") || "")
            }))
          },
          ATTR: function(e, t, n) {
            return function(r) {
              var i = se.attr(r, e);
              return null == i ? "!=" === t : !t || (i += "", "=" === t ? i === n : "!=" === t ? i !== n : "^=" === t ? n && 0 === i.indexOf(n) : "*=" === t ? n && -1 < i.indexOf(n) : "$=" === t ? n && i.slice(-n.length) === n : "~=" === t ? -1 < (" " + i.replace(F, " ") + " ").indexOf(n) : "|=" === t && (i === n || i.slice(0, n.length + 1) === n + "-"))
            }
          },
          CHILD: function(e, t, n, r, i) {
            var o = "nth" !== e.slice(0, 3),
              a = "last" !== e.slice(-4),
              s = "of-type" === t;
            return 1 === r && 0 === i ? function(e) {
              return !!e.parentNode
            } : function(t, n, l) {
              var c, u, d, p, f, h, m = o !== a ? "nextSibling" : "previousSibling",
                g = t.parentNode,
                v = s && t.nodeName.toLowerCase(),
                y = !l && !s,
                b = !1;
              if (g) {
                if (o) {
                  for (; m;) {
                    for (p = t; p = p[m];)
                      if (s ? p.nodeName.toLowerCase() === v : 1 === p.nodeType) return !1;
                    h = m = "only" === e && !h && "nextSibling"
                  }
                  return !0
                }
                if (h = [a ? g.firstChild : g.lastChild], a && y) {
                  for (b = (f = (c = (u = (d = (p = g)[w] || (p[w] = {}))[p.uniqueID] || (d[p.uniqueID] = {}))[e] || [])[0] === S && c[1]) && c[2], p = f && g.childNodes[f]; p = ++f && p && p[m] || (b = f = 0) || h.pop();)
                    if (1 === p.nodeType && ++b && p === t) {
                      u[e] = [S, f, b];
                      break
                    }
                } else if (y && (b = f = (c = (u = (d = (p = t)[w] || (p[w] = {}))[p.uniqueID] || (d[p.uniqueID] = {}))[e] || [])[0] === S && c[1]), !1 === b)
                  for (;
                    (p = ++f && p && p[m] || (b = f = 0) || h.pop()) && ((s ? p.nodeName.toLowerCase() !== v : 1 !== p.nodeType) || !++b || (y && ((u = (d = p[w] || (p[w] = {}))[p.uniqueID] || (d[p.uniqueID] = {}))[e] = [S, b]), p !== t)););
                return (b -= i) === r || b % r == 0 && 0 <= b / r
              }
            }
          },
          PSEUDO: function(e, t) {
            var n, i = r.pseudos[e] || r.setFilters[e.toLowerCase()] || se.error("unsupported pseudo: " + e);
            return i[w] ? i(t) : 1 < i.length ? (n = [e, e, "", t], r.setFilters.hasOwnProperty(e.toLowerCase()) ? ce((function(e, n) {
              for (var r, o = i(e, t), a = o.length; a--;) e[r = j(e, o[a])] = !(n[r] = o[a])
            })) : function(e) {
              return i(e, 0, n)
            }) : i
          }
        },
        pseudos: {
          not: ce((function(e) {
            var t = [],
              n = [],
              r = s(e.replace(B, "$1"));
            return r[w] ? ce((function(e, t, n, i) {
              for (var o, a = r(e, null, i, []), s = e.length; s--;)(o = a[s]) && (e[s] = !(t[s] = o))
            })) : function(e, i, o) {
              return t[0] = e, r(t, null, o, n), t[0] = null, !n.pop()
            }
          })),
          has: ce((function(e) {
            return function(t) {
              return 0 < se(e, t).length
            }
          })),
          contains: ce((function(e) {
            return e = e.replace(te, ne),
              function(t) {
                return -1 < (t.textContent || i(t)).indexOf(e)
              }
          })),
          lang: ce((function(e) {
            return V.test(e || "") || se.error("unsupported lang: " + e), e = e.replace(te, ne).toLowerCase(),
              function(t) {
                var n;
                do {
                  if (n = m ? t.lang : t.getAttribute("xml:lang") || t.getAttribute("lang")) return (n = n.toLowerCase()) === e || 0 === n.indexOf(e + "-")
                } while ((t = t.parentNode) && 1 === t.nodeType);
                return !1
              }
          })),
          target: function(t) {
            var n = e.location && e.location.hash;
            return n && n.slice(1) === t.id
          },
          root: function(e) {
            return e === h
          },
          focus: function(e) {
            return e === f.activeElement && (!f.hasFocus || f.hasFocus()) && !!(e.type || e.href || ~e.tabIndex)
          },
          enabled: me(!1),
          disabled: me(!0),
          checked: function(e) {
            var t = e.nodeName.toLowerCase();
            return "input" === t && !!e.checked || "option" === t && !!e.selected
          },
          selected: function(e) {
            return e.parentNode && e.parentNode.selectedIndex, !0 === e.selected
          },
          empty: function(e) {
            for (e = e.firstChild; e; e = e.nextSibling)
              if (e.nodeType < 6) return !1;
            return !0
          },
          parent: function(e) {
            return !r.pseudos.empty(e)
          },
          header: function(e) {
            return K.test(e.nodeName)
          },
          input: function(e) {
            return Z.test(e.nodeName)
          },
          button: function(e) {
            var t = e.nodeName.toLowerCase();
            return "input" === t && "button" === e.type || "button" === t
          },
          text: function(e) {
            var t;
            return "input" === e.nodeName.toLowerCase() && "text" === e.type && (null == (t = e.getAttribute("type")) || "text" === t.toLowerCase())
          },
          first: ge((function() {
            return [0]
          })),
          last: ge((function(e, t) {
            return [t - 1]
          })),
          eq: ge((function(e, t, n) {
            return [n < 0 ? n + t : n]
          })),
          even: ge((function(e, t) {
            for (var n = 0; n < t; n += 2) e.push(n);
            return e
          })),
          odd: ge((function(e, t) {
            for (var n = 1; n < t; n += 2) e.push(n);
            return e
          })),
          lt: ge((function(e, t, n) {
            for (var r = n < 0 ? n + t : t < n ? t : n; 0 <= --r;) e.push(r);
            return e
          })),
          gt: ge((function(e, t, n) {
            for (var r = n < 0 ? n + t : n; ++r < t;) e.push(r);
            return e
          }))
        }
      }).pseudos.nth = r.pseudos.eq, {
        radio: !0,
        checkbox: !0,
        file: !0,
        password: !0,
        image: !0
      }) r.pseudos[t] = fe(t);
    for (t in {
        submit: !0,
        reset: !0
      }) r.pseudos[t] = he(t);

    function ye() {}

    function be(e) {
      for (var t = 0, n = e.length, r = ""; t < n; t++) r += e[t].value;
      return r
    }

    function we(e, t, n) {
      var r = t.dir,
        i = t.next,
        o = i || r,
        a = n && "parentNode" === o,
        s = C++;
      return t.first ? function(t, n, i) {
        for (; t = t[r];)
          if (1 === t.nodeType || a) return e(t, n, i);
        return !1
      } : function(t, n, l) {
        var c, u, d, p = [S, s];
        if (l) {
          for (; t = t[r];)
            if ((1 === t.nodeType || a) && e(t, n, l)) return !0
        } else
          for (; t = t[r];)
            if (1 === t.nodeType || a)
              if (u = (d = t[w] || (t[w] = {}))[t.uniqueID] || (d[t.uniqueID] = {}), i && i === t.nodeName.toLowerCase()) t = t[r] || t;
              else {
                if ((c = u[o]) && c[0] === S && c[1] === s) return p[2] = c[2];
                if ((u[o] = p)[2] = e(t, n, l)) return !0
              } return !1
      }
    }

    function xe(e) {
      return 1 < e.length ? function(t, n, r) {
        for (var i = e.length; i--;)
          if (!e[i](t, n, r)) return !1;
        return !0
      } : e[0]
    }

    function Se(e, t, n, r, i) {
      for (var o, a = [], s = 0, l = e.length, c = null != t; s < l; s++)(o = e[s]) && (n && !n(o, r, i) || (a.push(o), c && t.push(s)));
      return a
    }

    function Ce(e, t, n, r, i, o) {
      return r && !r[w] && (r = Ce(r)), i && !i[w] && (i = Ce(i, o)), ce((function(o, a, s, l) {
        var c, u, d, p = [],
          f = [],
          h = a.length,
          m = o || function(e, t, n) {
            for (var r = 0, i = t.length; r < i; r++) se(e, t[r], n);
            return n
          }(t || "*", s.nodeType ? [s] : s, []),
          g = !e || !o && t ? m : Se(m, p, e, s, l),
          v = n ? i || (o ? e : h || r) ? [] : a : g;
        if (n && n(g, v, s, l), r)
          for (c = Se(v, f), r(c, [], s, l), u = c.length; u--;)(d = c[u]) && (v[f[u]] = !(g[f[u]] = d));
        if (o) {
          if (i || e) {
            if (i) {
              for (c = [], u = v.length; u--;)(d = v[u]) && c.push(g[u] = d);
              i(null, v = [], c, l)
            }
            for (u = v.length; u--;)(d = v[u]) && -1 < (c = i ? j(o, d) : p[u]) && (o[c] = !(a[c] = d))
          }
        } else v = Se(v === a ? v.splice(h, v.length) : v), i ? i(null, a, v, l) : I.apply(a, v)
      }))
    }

    function Ee(e) {
      for (var t, n, i, o = e.length, a = r.relative[e[0].type], s = a || r.relative[" "], l = a ? 1 : 0, u = we((function(e) {
          return e === t
        }), s, !0), d = we((function(e) {
          return -1 < j(t, e)
        }), s, !0), p = [function(e, n, r) {
          var i = !a && (r || n !== c) || ((t = n).nodeType ? u(e, n, r) : d(e, n, r));
          return t = null, i
        }]; l < o; l++)
        if (n = r.relative[e[l].type]) p = [we(xe(p), n)];
        else {
          if ((n = r.filter[e[l].type].apply(null, e[l].matches))[w]) {
            for (i = ++l; i < o && !r.relative[e[i].type]; i++);
            return Ce(1 < l && xe(p), 1 < l && be(e.slice(0, l - 1).concat({
              value: " " === e[l - 2].type ? "*" : ""
            })).replace(B, "$1"), n, l < i && Ee(e.slice(l, i)), i < o && Ee(e = e.slice(i)), i < o && be(e))
          }
          p.push(n)
        } return xe(p)
    }
    return ye.prototype = r.filters = r.pseudos, r.setFilters = new ye, a = se.tokenize = function(e, t) {
      var n, i, o, a, s, l, c, u = T[e + " "];
      if (u) return t ? 0 : u.slice(0);
      for (s = e, l = [], c = r.preFilter; s;) {
        for (a in n && !(i = q.exec(s)) || (i && (s = s.slice(i[0].length) || s), l.push(o = [])), n = !1, (i = W.exec(s)) && (n = i.shift(), o.push({
            value: n,
            type: i[0].replace(B, " ")
          }), s = s.slice(n.length)), r.filter) !(i = X[a].exec(s)) || c[a] && !(i = c[a](i)) || (n = i.shift(), o.push({
          value: n,
          type: a,
          matches: i
        }), s = s.slice(n.length));
        if (!n) break
      }
      return t ? s.length : s ? se.error(e) : T(e, l).slice(0)
    }, s = se.compile = function(e, t) {
      var n, i, o, s, l, u, d = [],
        h = [],
        g = k[e + " "];
      if (!g) {
        for (t || (t = a(e)), n = t.length; n--;)(g = Ee(t[n]))[w] ? d.push(g) : h.push(g);
        (g = k(e, (i = h, s = 0 < (o = d).length, l = 0 < i.length, u = function(e, t, n, a, u) {
          var d, h, g, v = 0,
            y = "0",
            b = e && [],
            w = [],
            x = c,
            C = e || l && r.find.TAG("*", u),
            E = S += null == x ? 1 : Math.random() || .1,
            T = C.length;
          for (u && (c = t == f || t || u); y !== T && null != (d = C[y]); y++) {
            if (l && d) {
              for (h = 0, t || d.ownerDocument == f || (p(d), n = !m); g = i[h++];)
                if (g(d, t || f, n)) {
                  a.push(d);
                  break
                } u && (S = E)
            }
            s && ((d = !g && d) && v--, e && b.push(d))
          }
          if (v += y, s && y !== v) {
            for (h = 0; g = o[h++];) g(b, w, t, n);
            if (e) {
              if (0 < v)
                for (; y--;) b[y] || w[y] || (w[y] = M.call(a));
              w = Se(w)
            }
            I.apply(a, w), u && !e && 0 < w.length && 1 < v + o.length && se.uniqueSort(a)
          }
          return u && (S = E, c = x), b
        }, s ? ce(u) : u))).selector = e
      }
      return g
    }, l = se.select = function(e, t, n, i) {
      var o, l, c, u, d, p = "function" == typeof e && e,
        f = !i && a(e = p.selector || e);
      if (n = n || [], 1 === f.length) {
        if (2 < (l = f[0] = f[0].slice(0)).length && "ID" === (c = l[0]).type && 9 === t.nodeType && m && r.relative[l[1].type]) {
          if (!(t = (r.find.ID(c.matches[0].replace(te, ne), t) || [])[0])) return n;
          p && (t = t.parentNode), e = e.slice(l.shift().value.length)
        }
        for (o = X.needsContext.test(e) ? 0 : l.length; o-- && (c = l[o], !r.relative[u = c.type]);)
          if ((d = r.find[u]) && (i = d(c.matches[0].replace(te, ne), ee.test(l[0].type) && ve(t.parentNode) || t))) {
            if (l.splice(o, 1), !(e = i.length && be(l))) return I.apply(n, i), n;
            break
          }
      }
      return (p || s(e, f))(i, t, !m, n, !t || ee.test(e) && ve(t.parentNode) || t), n
    }, n.sortStable = w.split("").sort(O).join("") === w, n.detectDuplicates = !!d, p(), n.sortDetached = ue((function(e) {
      return 1 & e.compareDocumentPosition(f.createElement("fieldset"))
    })), ue((function(e) {
      return e.innerHTML = "<a href='#'></a>", "#" === e.firstChild.getAttribute("href")
    })) || de("type|href|height|width", (function(e, t, n) {
      if (!n) return e.getAttribute(t, "type" === t.toLowerCase() ? 1 : 2)
    })), n.attributes && ue((function(e) {
      return e.innerHTML = "<input/>", e.firstChild.setAttribute("value", ""), "" === e.firstChild.getAttribute("value")
    })) || de("value", (function(e, t, n) {
      if (!n && "input" === e.nodeName.toLowerCase()) return e.defaultValue
    })), ue((function(e) {
      return null == e.getAttribute("disabled")
    })) || de(N, (function(e, t, n) {
      var r;
      if (!n) return !0 === e[t] ? t.toLowerCase() : (r = e.getAttributeNode(t)) && r.specified ? r.value : null
    })), se
  }(e);
  x.find = C, x.expr = C.selectors, x.expr[":"] = x.expr.pseudos, x.uniqueSort = x.unique = C.uniqueSort, x.text = C.getText, x.isXMLDoc = C.isXML, x.contains = C.contains, x.escapeSelector = C.escape;
  var E = function(e, t, n) {
      for (var r = [], i = void 0 !== n;
        (e = e[t]) && 9 !== e.nodeType;)
        if (1 === e.nodeType) {
          if (i && x(e).is(n)) break;
          r.push(e)
        } return r
    },
    T = function(e, t) {
      for (var n = []; e; e = e.nextSibling) 1 === e.nodeType && e !== t && n.push(e);
      return n
    },
    k = x.expr.match.needsContext;

  function D(e, t) {
    return e.nodeName && e.nodeName.toLowerCase() === t.toLowerCase()
  }
  var O = /^<([a-z][^\/\0>:\x20\t\r\n\f]*)[\x20\t\r\n\f]*\/?>(?:<\/\1>|)$/i;

  function A(e, t, n) {
    return h(t) ? x.grep(e, (function(e, r) {
      return !!t.call(e, r, e) !== n
    })) : t.nodeType ? x.grep(e, (function(e) {
      return e === t !== n
    })) : "string" != typeof t ? x.grep(e, (function(e) {
      return -1 < s.call(t, e) !== n
    })) : x.filter(t, e, n)
  }
  x.filter = function(e, t, n) {
    var r = t[0];
    return n && (e = ":not(" + e + ")"), 1 === t.length && 1 === r.nodeType ? x.find.matchesSelector(r, e) ? [r] : [] : x.find.matches(e, x.grep(t, (function(e) {
      return 1 === e.nodeType
    })))
  }, x.fn.extend({
    find: function(e) {
      var t, n, r = this.length,
        i = this;
      if ("string" != typeof e) return this.pushStack(x(e).filter((function() {
        for (t = 0; t < r; t++)
          if (x.contains(i[t], this)) return !0
      })));
      for (n = this.pushStack([]), t = 0; t < r; t++) x.find(e, i[t], n);
      return 1 < r ? x.uniqueSort(n) : n
    },
    filter: function(e) {
      return this.pushStack(A(this, e || [], !1))
    },
    not: function(e) {
      return this.pushStack(A(this, e || [], !0))
    },
    is: function(e) {
      return !!A(this, "string" == typeof e && k.test(e) ? x(e) : e || [], !1).length
    }
  });
  var _, M = /^(?:\s*(<[\w\W]+>)[^>]*|#([\w-]+))$/;
  (x.fn.init = function(e, t, n) {
    var r, i;
    if (!e) return this;
    if (n = n || _, "string" == typeof e) {
      if (!(r = "<" === e[0] && ">" === e[e.length - 1] && 3 <= e.length ? [null, e, null] : M.exec(e)) || !r[1] && t) return !t || t.jquery ? (t || n).find(e) : this.constructor(t).find(e);
      if (r[1]) {
        if (t = t instanceof x ? t[0] : t, x.merge(this, x.parseHTML(r[1], t && t.nodeType ? t.ownerDocument || t : g, !0)), O.test(r[1]) && x.isPlainObject(t))
          for (r in t) h(this[r]) ? this[r](t[r]) : this.attr(r, t[r]);
        return this
      }
      return (i = g.getElementById(r[2])) && (this[0] = i, this.length = 1), this
    }
    return e.nodeType ? (this[0] = e, this.length = 1, this) : h(e) ? void 0 !== n.ready ? n.ready(e) : e(x) : x.makeArray(e, this)
  }).prototype = x.fn, _ = x(g);
  var L = /^(?:parents|prev(?:Until|All))/,
    I = {
      children: !0,
      contents: !0,
      next: !0,
      prev: !0
    };

  function P(e, t) {
    for (;
      (e = e[t]) && 1 !== e.nodeType;);
    return e
  }
  x.fn.extend({
    has: function(e) {
      var t = x(e, this),
        n = t.length;
      return this.filter((function() {
        for (var e = 0; e < n; e++)
          if (x.contains(this, t[e])) return !0
      }))
    },
    closest: function(e, t) {
      var n, r = 0,
        i = this.length,
        o = [],
        a = "string" != typeof e && x(e);
      if (!k.test(e))
        for (; r < i; r++)
          for (n = this[r]; n && n !== t; n = n.parentNode)
            if (n.nodeType < 11 && (a ? -1 < a.index(n) : 1 === n.nodeType && x.find.matchesSelector(n, e))) {
              o.push(n);
              break
            } return this.pushStack(1 < o.length ? x.uniqueSort(o) : o)
    },
    index: function(e) {
      return e ? "string" == typeof e ? s.call(x(e), this[0]) : s.call(this, e.jquery ? e[0] : e) : this[0] && this[0].parentNode ? this.first().prevAll().length : -1
    },
    add: function(e, t) {
      return this.pushStack(x.uniqueSort(x.merge(this.get(), x(e, t))))
    },
    addBack: function(e) {
      return this.add(null == e ? this.prevObject : this.prevObject.filter(e))
    }
  }), x.each({
    parent: function(e) {
      var t = e.parentNode;
      return t && 11 !== t.nodeType ? t : null
    },
    parents: function(e) {
      return E(e, "parentNode")
    },
    parentsUntil: function(e, t, n) {
      return E(e, "parentNode", n)
    },
    next: function(e) {
      return P(e, "nextSibling")
    },
    prev: function(e) {
      return P(e, "previousSibling")
    },
    nextAll: function(e) {
      return E(e, "nextSibling")
    },
    prevAll: function(e) {
      return E(e, "previousSibling")
    },
    nextUntil: function(e, t, n) {
      return E(e, "nextSibling", n)
    },
    prevUntil: function(e, t, n) {
      return E(e, "previousSibling", n)
    },
    siblings: function(e) {
      return T((e.parentNode || {}).firstChild, e)
    },
    children: function(e) {
      return T(e.firstChild)
    },
    contents: function(e) {
      return null != e.contentDocument && r(e.contentDocument) ? e.contentDocument : (D(e, "template") && (e = e.content || e), x.merge([], e.childNodes))
    }
  }, (function(e, t) {
    x.fn[e] = function(n, r) {
      var i = x.map(this, t, n);
      return "Until" !== e.slice(-5) && (r = n), r && "string" == typeof r && (i = x.filter(r, i)), 1 < this.length && (I[e] || x.uniqueSort(i), L.test(e) && i.reverse()), this.pushStack(i)
    }
  }));
  var j = /[^\x20\t\r\n\f]+/g;

  function N(e) {
    return e
  }

  function z(e) {
    throw e
  }

  function R(e, t, n, r) {
    var i;
    try {
      e && h(i = e.promise) ? i.call(e).done(t).fail(n) : e && h(i = e.then) ? i.call(e, t, n) : t.apply(void 0, [e].slice(r))
    } catch (e) {
      n.apply(void 0, [e])
    }
  }
  x.Callbacks = function(e) {
    var t, n;
    e = "string" == typeof e ? (t = e, n = {}, x.each(t.match(j) || [], (function(e, t) {
      n[t] = !0
    })), n) : x.extend({}, e);
    var r, i, o, a, s = [],
      l = [],
      c = -1,
      u = function() {
        for (a = a || e.once, o = r = !0; l.length; c = -1)
          for (i = l.shift(); ++c < s.length;) !1 === s[c].apply(i[0], i[1]) && e.stopOnFalse && (c = s.length, i = !1);
        e.memory || (i = !1), r = !1, a && (s = i ? [] : "")
      },
      d = {
        add: function() {
          return s && (i && !r && (c = s.length - 1, l.push(i)), function t(n) {
            x.each(n, (function(n, r) {
              h(r) ? e.unique && d.has(r) || s.push(r) : r && r.length && "string" !== b(r) && t(r)
            }))
          }(arguments), i && !r && u()), this
        },
        remove: function() {
          return x.each(arguments, (function(e, t) {
            for (var n; - 1 < (n = x.inArray(t, s, n));) s.splice(n, 1), n <= c && c--
          })), this
        },
        has: function(e) {
          return e ? -1 < x.inArray(e, s) : 0 < s.length
        },
        empty: function() {
          return s && (s = []), this
        },
        disable: function() {
          return a = l = [], s = i = "", this
        },
        disabled: function() {
          return !s
        },
        lock: function() {
          return a = l = [], i || r || (s = i = ""), this
        },
        locked: function() {
          return !!a
        },
        fireWith: function(e, t) {
          return a || (t = [e, (t = t || []).slice ? t.slice() : t], l.push(t), r || u()), this
        },
        fire: function() {
          return d.fireWith(this, arguments), this
        },
        fired: function() {
          return !!o
        }
      };
    return d
  }, x.extend({
    Deferred: function(t) {
      var n = [
          ["notify", "progress", x.Callbacks("memory"), x.Callbacks("memory"), 2],
          ["resolve", "done", x.Callbacks("once memory"), x.Callbacks("once memory"), 0, "resolved"],
          ["reject", "fail", x.Callbacks("once memory"), x.Callbacks("once memory"), 1, "rejected"]
        ],
        r = "pending",
        i = {
          state: function() {
            return r
          },
          always: function() {
            return o.done(arguments).fail(arguments), this
          },
          catch: function(e) {
            return i.then(null, e)
          },
          pipe: function() {
            var e = arguments;
            return x.Deferred((function(t) {
              x.each(n, (function(n, r) {
                var i = h(e[r[4]]) && e[r[4]];
                o[r[1]]((function() {
                  var e = i && i.apply(this, arguments);
                  e && h(e.promise) ? e.promise().progress(t.notify).done(t.resolve).fail(t.reject) : t[r[0] + "With"](this, i ? [e] : arguments)
                }))
              })), e = null
            })).promise()
          },
          then: function(t, r, i) {
            var o = 0;

            function a(t, n, r, i) {
              return function() {
                var s = this,
                  l = arguments,
                  c = function() {
                    var e, c;
                    if (!(t < o)) {
                      if ((e = r.apply(s, l)) === n.promise()) throw new TypeError("Thenable self-resolution");
                      c = e && ("object" == typeof e || "function" == typeof e) && e.then, h(c) ? i ? c.call(e, a(o, n, N, i), a(o, n, z, i)) : (o++, c.call(e, a(o, n, N, i), a(o, n, z, i), a(o, n, N, n.notifyWith))) : (r !== N && (s = void 0, l = [e]), (i || n.resolveWith)(s, l))
                    }
                  },
                  u = i ? c : function() {
                    try {
                      c()
                    } catch (e) {
                      x.Deferred.exceptionHook && x.Deferred.exceptionHook(e, u.stackTrace), o <= t + 1 && (r !== z && (s = void 0, l = [e]), n.rejectWith(s, l))
                    }
                  };
                t ? u() : (x.Deferred.getStackHook && (u.stackTrace = x.Deferred.getStackHook()), e.setTimeout(u))
              }
            }
            return x.Deferred((function(e) {
              n[0][3].add(a(0, e, h(i) ? i : N, e.notifyWith)), n[1][3].add(a(0, e, h(t) ? t : N)), n[2][3].add(a(0, e, h(r) ? r : z))
            })).promise()
          },
          promise: function(e) {
            return null != e ? x.extend(e, i) : i
          }
        },
        o = {};
      return x.each(n, (function(e, t) {
        var a = t[2],
          s = t[5];
        i[t[1]] = a.add, s && a.add((function() {
          r = s
        }), n[3 - e][2].disable, n[3 - e][3].disable, n[0][2].lock, n[0][3].lock), a.add(t[3].fire), o[t[0]] = function() {
          return o[t[0] + "With"](this === o ? void 0 : this, arguments), this
        }, o[t[0] + "With"] = a.fireWith
      })), i.promise(o), t && t.call(o, o), o
    },
    when: function(e) {
      var t = arguments.length,
        n = t,
        r = Array(n),
        o = i.call(arguments),
        a = x.Deferred(),
        s = function(e) {
          return function(n) {
            r[e] = this, o[e] = 1 < arguments.length ? i.call(arguments) : n, --t || a.resolveWith(r, o)
          }
        };
      if (t <= 1 && (R(e, a.done(s(n)).resolve, a.reject, !t), "pending" === a.state() || h(o[n] && o[n].then))) return a.then();
      for (; n--;) R(o[n], s(n), a.reject);
      return a.promise()
    }
  });
  var $ = /^(Eval|Internal|Range|Reference|Syntax|Type|URI)Error$/;
  x.Deferred.exceptionHook = function(t, n) {
    e.console && e.console.warn && t && $.test(t.name) && e.console.warn("jQuery.Deferred exception: " + t.message, t.stack, n)
  }, x.readyException = function(t) {
    e.setTimeout((function() {
      throw t
    }))
  };
  var H = x.Deferred();

  function F() {
    g.removeEventListener("DOMContentLoaded", F), e.removeEventListener("load", F), x.ready()
  }
  x.fn.ready = function(e) {
    return H.then(e).catch((function(e) {
      x.readyException(e)
    })), this
  }, x.extend({
    isReady: !1,
    readyWait: 1,
    ready: function(e) {
      (!0 === e ? --x.readyWait : x.isReady) || (x.isReady = !0) !== e && 0 < --x.readyWait || H.resolveWith(g, [x])
    }
  }), x.ready.then = H.then, "complete" === g.readyState || "loading" !== g.readyState && !g.documentElement.doScroll ? e.setTimeout(x.ready) : (g.addEventListener("DOMContentLoaded", F), e.addEventListener("load", F));
  var B = function(e, t, n, r, i, o, a) {
      var s = 0,
        l = e.length,
        c = null == n;
      if ("object" === b(n))
        for (s in i = !0, n) B(e, t, s, n[s], !0, o, a);
      else if (void 0 !== r && (i = !0, h(r) || (a = !0), c && (a ? (t.call(e, r), t = null) : (c = t, t = function(e, t, n) {
          return c.call(x(e), n)
        })), t))
        for (; s < l; s++) t(e[s], n, a ? r : r.call(e[s], s, t(e[s], n)));
      return i ? e : c ? t.call(e) : l ? t(e[0], n) : o
    },
    q = /^-ms-/,
    W = /-([a-z])/g;

  function Y(e, t) {
    return t.toUpperCase()
  }

  function U(e) {
    return e.replace(q, "ms-").replace(W, Y)
  }
  var V = function(e) {
    return 1 === e.nodeType || 9 === e.nodeType || !+e.nodeType
  };

  function X() {
    this.expando = x.expando + X.uid++
  }
  X.uid = 1, X.prototype = {
    cache: function(e) {
      var t = e[this.expando];
      return t || (t = {}, V(e) && (e.nodeType ? e[this.expando] = t : Object.defineProperty(e, this.expando, {
        value: t,
        configurable: !0
      }))), t
    },
    set: function(e, t, n) {
      var r, i = this.cache(e);
      if ("string" == typeof t) i[U(t)] = n;
      else
        for (r in t) i[U(r)] = t[r];
      return i
    },
    get: function(e, t) {
      return void 0 === t ? this.cache(e) : e[this.expando] && e[this.expando][U(t)]
    },
    access: function(e, t, n) {
      return void 0 === t || t && "string" == typeof t && void 0 === n ? this.get(e, t) : (this.set(e, t, n), void 0 !== n ? n : t)
    },
    remove: function(e, t) {
      var n, r = e[this.expando];
      if (void 0 !== r) {
        if (void 0 !== t) {
          n = (t = Array.isArray(t) ? t.map(U) : (t = U(t)) in r ? [t] : t.match(j) || []).length;
          for (; n--;) delete r[t[n]]
        }(void 0 === t || x.isEmptyObject(r)) && (e.nodeType ? e[this.expando] = void 0 : delete e[this.expando])
      }
    },
    hasData: function(e) {
      var t = e[this.expando];
      return void 0 !== t && !x.isEmptyObject(t)
    }
  };
  var G = new X,
    Z = new X,
    K = /^(?:\{[\w\W]*\}|\[[\w\W]*\])$/,
    J = /[A-Z]/g;

  function Q(e, t, n) {
    var r, i;
    if (void 0 === n && 1 === e.nodeType)
      if (r = "data-" + t.replace(J, "-$&").toLowerCase(), "string" == typeof(n = e.getAttribute(r))) {
        try {
          n = "true" === (i = n) || "false" !== i && ("null" === i ? null : i === +i + "" ? +i : K.test(i) ? JSON.parse(i) : i)
        } catch (e) {}
        Z.set(e, t, n)
      } else n = void 0;
    return n
  }
  x.extend({
    hasData: function(e) {
      return Z.hasData(e) || G.hasData(e)
    },
    data: function(e, t, n) {
      return Z.access(e, t, n)
    },
    removeData: function(e, t) {
      Z.remove(e, t)
    },
    _data: function(e, t, n) {
      return G.access(e, t, n)
    },
    _removeData: function(e, t) {
      G.remove(e, t)
    }
  }), x.fn.extend({
    data: function(e, t) {
      var n, r, i, o = this[0],
        a = o && o.attributes;
      if (void 0 === e) {
        if (this.length && (i = Z.get(o), 1 === o.nodeType && !G.get(o, "hasDataAttrs"))) {
          for (n = a.length; n--;) a[n] && 0 === (r = a[n].name).indexOf("data-") && (r = U(r.slice(5)), Q(o, r, i[r]));
          G.set(o, "hasDataAttrs", !0)
        }
        return i
      }
      return "object" == typeof e ? this.each((function() {
        Z.set(this, e)
      })) : B(this, (function(t) {
        var n;
        if (o && void 0 === t) return void 0 !== (n = Z.get(o, e)) || void 0 !== (n = Q(o, e)) ? n : void 0;
        this.each((function() {
          Z.set(this, e, t)
        }))
      }), null, t, 1 < arguments.length, null, !0)
    },
    removeData: function(e) {
      return this.each((function() {
        Z.remove(this, e)
      }))
    }
  }), x.extend({
    queue: function(e, t, n) {
      var r;
      if (e) return t = (t || "fx") + "queue", r = G.get(e, t), n && (!r || Array.isArray(n) ? r = G.access(e, t, x.makeArray(n)) : r.push(n)), r || []
    },
    dequeue: function(e, t) {
      t = t || "fx";
      var n = x.queue(e, t),
        r = n.length,
        i = n.shift(),
        o = x._queueHooks(e, t);
      "inprogress" === i && (i = n.shift(), r--), i && ("fx" === t && n.unshift("inprogress"), delete o.stop, i.call(e, (function() {
        x.dequeue(e, t)
      }), o)), !r && o && o.empty.fire()
    },
    _queueHooks: function(e, t) {
      var n = t + "queueHooks";
      return G.get(e, n) || G.access(e, n, {
        empty: x.Callbacks("once memory").add((function() {
          G.remove(e, [t + "queue", n])
        }))
      })
    }
  }), x.fn.extend({
    queue: function(e, t) {
      var n = 2;
      return "string" != typeof e && (t = e, e = "fx", n--), arguments.length < n ? x.queue(this[0], e) : void 0 === t ? this : this.each((function() {
        var n = x.queue(this, e, t);
        x._queueHooks(this, e), "fx" === e && "inprogress" !== n[0] && x.dequeue(this, e)
      }))
    },
    dequeue: function(e) {
      return this.each((function() {
        x.dequeue(this, e)
      }))
    },
    clearQueue: function(e) {
      return this.queue(e || "fx", [])
    },
    promise: function(e, t) {
      var n, r = 1,
        i = x.Deferred(),
        o = this,
        a = this.length,
        s = function() {
          --r || i.resolveWith(o, [o])
        };
      for ("string" != typeof e && (t = e, e = void 0), e = e || "fx"; a--;)(n = G.get(o[a], e + "queueHooks")) && n.empty && (r++, n.empty.add(s));
      return s(), i.promise(t)
    }
  });
  var ee = /[+-]?(?:\d*\.|)\d+(?:[eE][+-]?\d+|)/.source,
    te = new RegExp("^(?:([+-])=|)(" + ee + ")([a-z%]*)$", "i"),
    ne = ["Top", "Right", "Bottom", "Left"],
    re = g.documentElement,
    ie = function(e) {
      return x.contains(e.ownerDocument, e)
    },
    oe = {
      composed: !0
    };
  re.getRootNode && (ie = function(e) {
    return x.contains(e.ownerDocument, e) || e.getRootNode(oe) === e.ownerDocument
  });
  var ae = function(e, t) {
    return "none" === (e = t || e).style.display || "" === e.style.display && ie(e) && "none" === x.css(e, "display")
  };

  function se(e, t, n, r) {
    var i, o, a = 20,
      s = r ? function() {
        return r.cur()
      } : function() {
        return x.css(e, t, "")
      },
      l = s(),
      c = n && n[3] || (x.cssNumber[t] ? "" : "px"),
      u = e.nodeType && (x.cssNumber[t] || "px" !== c && +l) && te.exec(x.css(e, t));
    if (u && u[3] !== c) {
      for (l /= 2, c = c || u[3], u = +l || 1; a--;) x.style(e, t, u + c), (1 - o) * (1 - (o = s() / l || .5)) <= 0 && (a = 0), u /= o;
      u *= 2, x.style(e, t, u + c), n = n || []
    }
    return n && (u = +u || +l || 0, i = n[1] ? u + (n[1] + 1) * n[2] : +n[2], r && (r.unit = c, r.start = u, r.end = i)), i
  }
  var le = {};

  function ce(e, t) {
    for (var n, r, i, o, a, s, l, c = [], u = 0, d = e.length; u < d; u++)(r = e[u]).style && (n = r.style.display, t ? ("none" === n && (c[u] = G.get(r, "display") || null, c[u] || (r.style.display = "")), "" === r.style.display && ae(r) && (c[u] = (l = a = o = void 0, a = (i = r).ownerDocument, s = i.nodeName, (l = le[s]) || (o = a.body.appendChild(a.createElement(s)), l = x.css(o, "display"), o.parentNode.removeChild(o), "none" === l && (l = "block"), le[s] = l)))) : "none" !== n && (c[u] = "none", G.set(r, "display", n)));
    for (u = 0; u < d; u++) null != c[u] && (e[u].style.display = c[u]);
    return e
  }
  x.fn.extend({
    show: function() {
      return ce(this, !0)
    },
    hide: function() {
      return ce(this)
    },
    toggle: function(e) {
      return "boolean" == typeof e ? e ? this.show() : this.hide() : this.each((function() {
        ae(this) ? x(this).show() : x(this).hide()
      }))
    }
  });
  var ue, de, pe = /^(?:checkbox|radio)$/i,
    fe = /<([a-z][^\/\0>\x20\t\r\n\f]*)/i,
    he = /^$|^module$|\/(?:java|ecma)script/i;
  ue = g.createDocumentFragment().appendChild(g.createElement("div")), (de = g.createElement("input")).setAttribute("type", "radio"), de.setAttribute("checked", "checked"), de.setAttribute("name", "t"), ue.appendChild(de), f.checkClone = ue.cloneNode(!0).cloneNode(!0).lastChild.checked, ue.innerHTML = "<textarea>x</textarea>", f.noCloneChecked = !!ue.cloneNode(!0).lastChild.defaultValue, ue.innerHTML = "<option></option>", f.option = !!ue.lastChild;
  var me = {
    thead: [1, "<table>", "</table>"],
    col: [2, "<table><colgroup>", "</colgroup></table>"],
    tr: [2, "<table><tbody>", "</tbody></table>"],
    td: [3, "<table><tbody><tr>", "</tr></tbody></table>"],
    _default: [0, "", ""]
  };

  function ge(e, t) {
    var n;
    return n = void 0 !== e.getElementsByTagName ? e.getElementsByTagName(t || "*") : void 0 !== e.querySelectorAll ? e.querySelectorAll(t || "*") : [], void 0 === t || t && D(e, t) ? x.merge([e], n) : n
  }

  function ve(e, t) {
    for (var n = 0, r = e.length; n < r; n++) G.set(e[n], "globalEval", !t || G.get(t[n], "globalEval"))
  }
  me.tbody = me.tfoot = me.colgroup = me.caption = me.thead, me.th = me.td, f.option || (me.optgroup = me.option = [1, "<select multiple='multiple'>", "</select>"]);
  var ye = /<|&#?\w+;/;

  function be(e, t, n, r, i) {
    for (var o, a, s, l, c, u, d = t.createDocumentFragment(), p = [], f = 0, h = e.length; f < h; f++)
      if ((o = e[f]) || 0 === o)
        if ("object" === b(o)) x.merge(p, o.nodeType ? [o] : o);
        else if (ye.test(o)) {
      for (a = a || d.appendChild(t.createElement("div")), s = (fe.exec(o) || ["", ""])[1].toLowerCase(), l = me[s] || me._default, a.innerHTML = l[1] + x.htmlPrefilter(o) + l[2], u = l[0]; u--;) a = a.lastChild;
      x.merge(p, a.childNodes), (a = d.firstChild).textContent = ""
    } else p.push(t.createTextNode(o));
    for (d.textContent = "", f = 0; o = p[f++];)
      if (r && -1 < x.inArray(o, r)) i && i.push(o);
      else if (c = ie(o), a = ge(d.appendChild(o), "script"), c && ve(a), n)
      for (u = 0; o = a[u++];) he.test(o.type || "") && n.push(o);
    return d
  }
  var we = /^key/,
    xe = /^(?:mouse|pointer|contextmenu|drag|drop)|click/,
    Se = /^([^.]*)(?:\.(.+)|)/;

  function Ce() {
    return !0
  }

  function Ee() {
    return !1
  }

  function Te(e, t) {
    return e === function() {
      try {
        return g.activeElement
      } catch (e) {}
    }() == ("focus" === t)
  }

  function ke(e, t, n, r, i, o) {
    var a, s;
    if ("object" == typeof t) {
      for (s in "string" != typeof n && (r = r || n, n = void 0), t) ke(e, s, n, r, t[s], o);
      return e
    }
    if (null == r && null == i ? (i = n, r = n = void 0) : null == i && ("string" == typeof n ? (i = r, r = void 0) : (i = r, r = n, n = void 0)), !1 === i) i = Ee;
    else if (!i) return e;
    return 1 === o && (a = i, (i = function(e) {
      return x().off(e), a.apply(this, arguments)
    }).guid = a.guid || (a.guid = x.guid++)), e.each((function() {
      x.event.add(this, t, i, r, n)
    }))
  }

  function De(e, t, n) {
    n ? (G.set(e, t, !1), x.event.add(e, t, {
      namespace: !1,
      handler: function(e) {
        var r, o, a = G.get(this, t);
        if (1 & e.isTrigger && this[t]) {
          if (a.length)(x.event.special[t] || {}).delegateType && e.stopPropagation();
          else if (a = i.call(arguments), G.set(this, t, a), r = n(this, t), this[t](), a !== (o = G.get(this, t)) || r ? G.set(this, t, !1) : o = {}, a !== o) return e.stopImmediatePropagation(), e.preventDefault(), o.value
        } else a.length && (G.set(this, t, {
          value: x.event.trigger(x.extend(a[0], x.Event.prototype), a.slice(1), this)
        }), e.stopImmediatePropagation())
      }
    })) : void 0 === G.get(e, t) && x.event.add(e, t, Ce)
  }
  x.event = {
    global: {},
    add: function(e, t, n, r, i) {
      var o, a, s, l, c, u, d, p, f, h, m, g = G.get(e);
      if (V(e))
        for (n.handler && (n = (o = n).handler, i = o.selector), i && x.find.matchesSelector(re, i), n.guid || (n.guid = x.guid++), (l = g.events) || (l = g.events = Object.create(null)), (a = g.handle) || (a = g.handle = function(t) {
            return void 0 !== x && x.event.triggered !== t.type ? x.event.dispatch.apply(e, arguments) : void 0
          }), c = (t = (t || "").match(j) || [""]).length; c--;) f = m = (s = Se.exec(t[c]) || [])[1], h = (s[2] || "").split(".").sort(), f && (d = x.event.special[f] || {}, f = (i ? d.delegateType : d.bindType) || f, d = x.event.special[f] || {}, u = x.extend({
          type: f,
          origType: m,
          data: r,
          handler: n,
          guid: n.guid,
          selector: i,
          needsContext: i && x.expr.match.needsContext.test(i),
          namespace: h.join(".")
        }, o), (p = l[f]) || ((p = l[f] = []).delegateCount = 0, d.setup && !1 !== d.setup.call(e, r, h, a) || e.addEventListener && e.addEventListener(f, a)), d.add && (d.add.call(e, u), u.handler.guid || (u.handler.guid = n.guid)), i ? p.splice(p.delegateCount++, 0, u) : p.push(u), x.event.global[f] = !0)
    },
    remove: function(e, t, n, r, i) {
      var o, a, s, l, c, u, d, p, f, h, m, g = G.hasData(e) && G.get(e);
      if (g && (l = g.events)) {
        for (c = (t = (t || "").match(j) || [""]).length; c--;)
          if (f = m = (s = Se.exec(t[c]) || [])[1], h = (s[2] || "").split(".").sort(), f) {
            for (d = x.event.special[f] || {}, p = l[f = (r ? d.delegateType : d.bindType) || f] || [], s = s[2] && new RegExp("(^|\\.)" + h.join("\\.(?:.*\\.|)") + "(\\.|$)"), a = o = p.length; o--;) u = p[o], !i && m !== u.origType || n && n.guid !== u.guid || s && !s.test(u.namespace) || r && r !== u.selector && ("**" !== r || !u.selector) || (p.splice(o, 1), u.selector && p.delegateCount--, d.remove && d.remove.call(e, u));
            a && !p.length && (d.teardown && !1 !== d.teardown.call(e, h, g.handle) || x.removeEvent(e, f, g.handle), delete l[f])
          } else
            for (f in l) x.event.remove(e, f + t[c], n, r, !0);
        x.isEmptyObject(l) && G.remove(e, "handle events")
      }
    },
    dispatch: function(e) {
      var t, n, r, i, o, a, s = new Array(arguments.length),
        l = x.event.fix(e),
        c = (G.get(this, "events") || Object.create(null))[l.type] || [],
        u = x.event.special[l.type] || {};
      for (s[0] = l, t = 1; t < arguments.length; t++) s[t] = arguments[t];
      if (l.delegateTarget = this, !u.preDispatch || !1 !== u.preDispatch.call(this, l)) {
        for (a = x.event.handlers.call(this, l, c), t = 0;
          (i = a[t++]) && !l.isPropagationStopped();)
          for (l.currentTarget = i.elem, n = 0;
            (o = i.handlers[n++]) && !l.isImmediatePropagationStopped();) l.rnamespace && !1 !== o.namespace && !l.rnamespace.test(o.namespace) || (l.handleObj = o, l.data = o.data, void 0 !== (r = ((x.event.special[o.origType] || {}).handle || o.handler).apply(i.elem, s)) && !1 === (l.result = r) && (l.preventDefault(), l.stopPropagation()));
        return u.postDispatch && u.postDispatch.call(this, l), l.result
      }
    },
    handlers: function(e, t) {
      var n, r, i, o, a, s = [],
        l = t.delegateCount,
        c = e.target;
      if (l && c.nodeType && !("click" === e.type && 1 <= e.button))
        for (; c !== this; c = c.parentNode || this)
          if (1 === c.nodeType && ("click" !== e.type || !0 !== c.disabled)) {
            for (o = [], a = {}, n = 0; n < l; n++) void 0 === a[i = (r = t[n]).selector + " "] && (a[i] = r.needsContext ? -1 < x(i, this).index(c) : x.find(i, this, null, [c]).length), a[i] && o.push(r);
            o.length && s.push({
              elem: c,
              handlers: o
            })
          } return c = this, l < t.length && s.push({
        elem: c,
        handlers: t.slice(l)
      }), s
    },
    addProp: function(e, t) {
      Object.defineProperty(x.Event.prototype, e, {
        enumerable: !0,
        configurable: !0,
        get: h(t) ? function() {
          if (this.originalEvent) return t(this.originalEvent)
        } : function() {
          if (this.originalEvent) return this.originalEvent[e]
        },
        set: function(t) {
          Object.defineProperty(this, e, {
            enumerable: !0,
            configurable: !0,
            writable: !0,
            value: t
          })
        }
      })
    },
    fix: function(e) {
      return e[x.expando] ? e : new x.Event(e)
    },
    special: {
      load: {
        noBubble: !0
      },
      click: {
        setup: function(e) {
          var t = this || e;
          return pe.test(t.type) && t.click && D(t, "input") && De(t, "click", Ce), !1
        },
        trigger: function(e) {
          var t = this || e;
          return pe.test(t.type) && t.click && D(t, "input") && De(t, "click"), !0
        },
        _default: function(e) {
          var t = e.target;
          return pe.test(t.type) && t.click && D(t, "input") && G.get(t, "click") || D(t, "a")
        }
      },
      beforeunload: {
        postDispatch: function(e) {
          void 0 !== e.result && e.originalEvent && (e.originalEvent.returnValue = e.result)
        }
      }
    }
  }, x.removeEvent = function(e, t, n) {
    e.removeEventListener && e.removeEventListener(t, n)
  }, x.Event = function(e, t) {
    if (!(this instanceof x.Event)) return new x.Event(e, t);
    e && e.type ? (this.originalEvent = e, this.type = e.type, this.isDefaultPrevented = e.defaultPrevented || void 0 === e.defaultPrevented && !1 === e.returnValue ? Ce : Ee, this.target = e.target && 3 === e.target.nodeType ? e.target.parentNode : e.target, this.currentTarget = e.currentTarget, this.relatedTarget = e.relatedTarget) : this.type = e, t && x.extend(this, t), this.timeStamp = e && e.timeStamp || Date.now(), this[x.expando] = !0
  }, x.Event.prototype = {
    constructor: x.Event,
    isDefaultPrevented: Ee,
    isPropagationStopped: Ee,
    isImmediatePropagationStopped: Ee,
    isSimulated: !1,
    preventDefault: function() {
      var e = this.originalEvent;
      this.isDefaultPrevented = Ce, e && !this.isSimulated && e.preventDefault()
    },
    stopPropagation: function() {
      var e = this.originalEvent;
      this.isPropagationStopped = Ce, e && !this.isSimulated && e.stopPropagation()
    },
    stopImmediatePropagation: function() {
      var e = this.originalEvent;
      this.isImmediatePropagationStopped = Ce, e && !this.isSimulated && e.stopImmediatePropagation(), this.stopPropagation()
    }
  }, x.each({
    altKey: !0,
    bubbles: !0,
    cancelable: !0,
    changedTouches: !0,
    ctrlKey: !0,
    detail: !0,
    eventPhase: !0,
    metaKey: !0,
    pageX: !0,
    pageY: !0,
    shiftKey: !0,
    view: !0,
    char: !0,
    code: !0,
    charCode: !0,
    key: !0,
    keyCode: !0,
    button: !0,
    buttons: !0,
    clientX: !0,
    clientY: !0,
    offsetX: !0,
    offsetY: !0,
    pointerId: !0,
    pointerType: !0,
    screenX: !0,
    screenY: !0,
    targetTouches: !0,
    toElement: !0,
    touches: !0,
    which: function(e) {
      var t = e.button;
      return null == e.which && we.test(e.type) ? null != e.charCode ? e.charCode : e.keyCode : !e.which && void 0 !== t && xe.test(e.type) ? 1 & t ? 1 : 2 & t ? 3 : 4 & t ? 2 : 0 : e.which
    }
  }, x.event.addProp), x.each({
    focus: "focusin",
    blur: "focusout"
  }, (function(e, t) {
    x.event.special[e] = {
      setup: function() {
        return De(this, e, Te), !1
      },
      trigger: function() {
        return De(this, e), !0
      },
      delegateType: t
    }
  })), x.each({
    mouseenter: "mouseover",
    mouseleave: "mouseout",
    pointerenter: "pointerover",
    pointerleave: "pointerout"
  }, (function(e, t) {
    x.event.special[e] = {
      delegateType: t,
      bindType: t,
      handle: function(e) {
        var n, r = e.relatedTarget,
          i = e.handleObj;
        return r && (r === this || x.contains(this, r)) || (e.type = i.origType, n = i.handler.apply(this, arguments), e.type = t), n
      }
    }
  })), x.fn.extend({
    on: function(e, t, n, r) {
      return ke(this, e, t, n, r)
    },
    one: function(e, t, n, r) {
      return ke(this, e, t, n, r, 1)
    },
    off: function(e, t, n) {
      var r, i;
      if (e && e.preventDefault && e.handleObj) return r = e.handleObj, x(e.delegateTarget).off(r.namespace ? r.origType + "." + r.namespace : r.origType, r.selector, r.handler), this;
      if ("object" == typeof e) {
        for (i in e) this.off(i, t, e[i]);
        return this
      }
      return !1 !== t && "function" != typeof t || (n = t, t = void 0), !1 === n && (n = Ee), this.each((function() {
        x.event.remove(this, e, n, t)
      }))
    }
  });
  var Oe = /<script|<style|<link/i,
    Ae = /checked\s*(?:[^=]|=\s*.checked.)/i,
    _e = /^\s*<!(?:\[CDATA\[|--)|(?:\]\]|--)>\s*$/g;

  function Me(e, t) {
    return D(e, "table") && D(11 !== t.nodeType ? t : t.firstChild, "tr") && x(e).children("tbody")[0] || e
  }

  function Le(e) {
    return e.type = (null !== e.getAttribute("type")) + "/" + e.type, e
  }

  function Ie(e) {
    return "true/" === (e.type || "").slice(0, 5) ? e.type = e.type.slice(5) : e.removeAttribute("type"), e
  }

  function Pe(e, t) {
    var n, r, i, o, a, s;
    if (1 === t.nodeType) {
      if (G.hasData(e) && (s = G.get(e).events))
        for (i in G.remove(t, "handle events"), s)
          for (n = 0, r = s[i].length; n < r; n++) x.event.add(t, i, s[i][n]);
      Z.hasData(e) && (o = Z.access(e), a = x.extend({}, o), Z.set(t, a))
    }
  }

  function je(e, t, n, r) {
    t = o(t);
    var i, a, s, l, c, u, d = 0,
      p = e.length,
      m = p - 1,
      g = t[0],
      v = h(g);
    if (v || 1 < p && "string" == typeof g && !f.checkClone && Ae.test(g)) return e.each((function(i) {
      var o = e.eq(i);
      v && (t[0] = g.call(this, i, o.html())), je(o, t, n, r)
    }));
    if (p && (a = (i = be(t, e[0].ownerDocument, !1, e, r)).firstChild, 1 === i.childNodes.length && (i = a), a || r)) {
      for (l = (s = x.map(ge(i, "script"), Le)).length; d < p; d++) c = i, d !== m && (c = x.clone(c, !0, !0), l && x.merge(s, ge(c, "script"))), n.call(e[d], c, d);
      if (l)
        for (u = s[s.length - 1].ownerDocument, x.map(s, Ie), d = 0; d < l; d++) c = s[d], he.test(c.type || "") && !G.access(c, "globalEval") && x.contains(u, c) && (c.src && "module" !== (c.type || "").toLowerCase() ? x._evalUrl && !c.noModule && x._evalUrl(c.src, {
          nonce: c.nonce || c.getAttribute("nonce")
        }, u) : y(c.textContent.replace(_e, ""), c, u))
    }
    return e
  }

  function Ne(e, t, n) {
    for (var r, i = t ? x.filter(t, e) : e, o = 0; null != (r = i[o]); o++) n || 1 !== r.nodeType || x.cleanData(ge(r)), r.parentNode && (n && ie(r) && ve(ge(r, "script")), r.parentNode.removeChild(r));
    return e
  }
  x.extend({
    htmlPrefilter: function(e) {
      return e
    },
    clone: function(e, t, n) {
      var r, i, o, a, s, l, c, u = e.cloneNode(!0),
        d = ie(e);
      if (!(f.noCloneChecked || 1 !== e.nodeType && 11 !== e.nodeType || x.isXMLDoc(e)))
        for (a = ge(u), r = 0, i = (o = ge(e)).length; r < i; r++) s = o[r], "input" === (c = (l = a[r]).nodeName.toLowerCase()) && pe.test(s.type) ? l.checked = s.checked : "input" !== c && "textarea" !== c || (l.defaultValue = s.defaultValue);
      if (t)
        if (n)
          for (o = o || ge(e), a = a || ge(u), r = 0, i = o.length; r < i; r++) Pe(o[r], a[r]);
        else Pe(e, u);
      return 0 < (a = ge(u, "script")).length && ve(a, !d && ge(e, "script")), u
    },
    cleanData: function(e) {
      for (var t, n, r, i = x.event.special, o = 0; void 0 !== (n = e[o]); o++)
        if (V(n)) {
          if (t = n[G.expando]) {
            if (t.events)
              for (r in t.events) i[r] ? x.event.remove(n, r) : x.removeEvent(n, r, t.handle);
            n[G.expando] = void 0
          }
          n[Z.expando] && (n[Z.expando] = void 0)
        }
    }
  }), x.fn.extend({
    detach: function(e) {
      return Ne(this, e, !0)
    },
    remove: function(e) {
      return Ne(this, e)
    },
    text: function(e) {
      return B(this, (function(e) {
        return void 0 === e ? x.text(this) : this.empty().each((function() {
          1 !== this.nodeType && 11 !== this.nodeType && 9 !== this.nodeType || (this.textContent = e)
        }))
      }), null, e, arguments.length)
    },
    append: function() {
      return je(this, arguments, (function(e) {
        1 !== this.nodeType && 11 !== this.nodeType && 9 !== this.nodeType || Me(this, e).appendChild(e)
      }))
    },
    prepend: function() {
      return je(this, arguments, (function(e) {
        if (1 === this.nodeType || 11 === this.nodeType || 9 === this.nodeType) {
          var t = Me(this, e);
          t.insertBefore(e, t.firstChild)
        }
      }))
    },
    before: function() {
      return je(this, arguments, (function(e) {
        this.parentNode && this.parentNode.insertBefore(e, this)
      }))
    },
    after: function() {
      return je(this, arguments, (function(e) {
        this.parentNode && this.parentNode.insertBefore(e, this.nextSibling)
      }))
    },
    empty: function() {
      for (var e, t = 0; null != (e = this[t]); t++) 1 === e.nodeType && (x.cleanData(ge(e, !1)), e.textContent = "");
      return this
    },
    clone: function(e, t) {
      return e = null != e && e, t = null == t ? e : t, this.map((function() {
        return x.clone(this, e, t)
      }))
    },
    html: function(e) {
      return B(this, (function(e) {
        var t = this[0] || {},
          n = 0,
          r = this.length;
        if (void 0 === e && 1 === t.nodeType) return t.innerHTML;
        if ("string" == typeof e && !Oe.test(e) && !me[(fe.exec(e) || ["", ""])[1].toLowerCase()]) {
          e = x.htmlPrefilter(e);
          try {
            for (; n < r; n++) 1 === (t = this[n] || {}).nodeType && (x.cleanData(ge(t, !1)), t.innerHTML = e);
            t = 0
          } catch (e) {}
        }
        t && this.empty().append(e)
      }), null, e, arguments.length)
    },
    replaceWith: function() {
      var e = [];
      return je(this, arguments, (function(t) {
        var n = this.parentNode;
        x.inArray(this, e) < 0 && (x.cleanData(ge(this)), n && n.replaceChild(t, this))
      }), e)
    }
  }), x.each({
    appendTo: "append",
    prependTo: "prepend",
    insertBefore: "before",
    insertAfter: "after",
    replaceAll: "replaceWith"
  }, (function(e, t) {
    x.fn[e] = function(e) {
      for (var n, r = [], i = x(e), o = i.length - 1, s = 0; s <= o; s++) n = s === o ? this : this.clone(!0), x(i[s])[t](n), a.apply(r, n.get());
      return this.pushStack(r)
    }
  }));
  var ze = new RegExp("^(" + ee + ")(?!px)[a-z%]+$", "i"),
    Re = function(t) {
      var n = t.ownerDocument.defaultView;
      return n && n.opener || (n = e), n.getComputedStyle(t)
    },
    $e = function(e, t, n) {
      var r, i, o = {};
      for (i in t) o[i] = e.style[i], e.style[i] = t[i];
      for (i in r = n.call(e), t) e.style[i] = o[i];
      return r
    },
    He = new RegExp(ne.join("|"), "i");

  function Fe(e, t, n) {
    var r, i, o, a, s = e.style;
    return (n = n || Re(e)) && ("" !== (a = n.getPropertyValue(t) || n[t]) || ie(e) || (a = x.style(e, t)), !f.pixelBoxStyles() && ze.test(a) && He.test(t) && (r = s.width, i = s.minWidth, o = s.maxWidth, s.minWidth = s.maxWidth = s.width = a, a = n.width, s.width = r, s.minWidth = i, s.maxWidth = o)), void 0 !== a ? a + "" : a
  }

  function Be(e, t) {
    return {
      get: function() {
        if (!e()) return (this.get = t).apply(this, arguments);
        delete this.get
      }
    }
  }! function() {
    function t() {
      if (u) {
        c.style.cssText = "position:absolute;left:-11111px;width:60px;margin-top:1px;padding:0;border:0", u.style.cssText = "position:relative;display:block;box-sizing:border-box;overflow:scroll;margin:auto;border:1px;padding:1px;width:60%;top:1%", re.appendChild(c).appendChild(u);
        var t = e.getComputedStyle(u);
        r = "1%" !== t.top, l = 12 === n(t.marginLeft), u.style.right = "60%", a = 36 === n(t.right), i = 36 === n(t.width), u.style.position = "absolute", o = 12 === n(u.offsetWidth / 3), re.removeChild(c), u = null
      }
    }

    function n(e) {
      return Math.round(parseFloat(e))
    }
    var r, i, o, a, s, l, c = g.createElement("div"),
      u = g.createElement("div");
    u.style && (u.style.backgroundClip = "content-box", u.cloneNode(!0).style.backgroundClip = "", f.clearCloneStyle = "content-box" === u.style.backgroundClip, x.extend(f, {
      boxSizingReliable: function() {
        return t(), i
      },
      pixelBoxStyles: function() {
        return t(), a
      },
      pixelPosition: function() {
        return t(), r
      },
      reliableMarginLeft: function() {
        return t(), l
      },
      scrollboxSize: function() {
        return t(), o
      },
      reliableTrDimensions: function() {
        var t, n, r, i;
        return null == s && (t = g.createElement("table"), n = g.createElement("tr"), r = g.createElement("div"), t.style.cssText = "position:absolute;left:-11111px", n.style.height = "1px", r.style.height = "9px", re.appendChild(t).appendChild(n).appendChild(r), i = e.getComputedStyle(n), s = 3 < parseInt(i.height), re.removeChild(t)), s
      }
    }))
  }();
  var qe = ["Webkit", "Moz", "ms"],
    We = g.createElement("div").style,
    Ye = {};

  function Ue(e) {
    return x.cssProps[e] || Ye[e] || (e in We ? e : Ye[e] = function(e) {
      for (var t = e[0].toUpperCase() + e.slice(1), n = qe.length; n--;)
        if ((e = qe[n] + t) in We) return e
    }(e) || e)
  }
  var Ve = /^(none|table(?!-c[ea]).+)/,
    Xe = /^--/,
    Ge = {
      position: "absolute",
      visibility: "hidden",
      display: "block"
    },
    Ze = {
      letterSpacing: "0",
      fontWeight: "400"
    };

  function Ke(e, t, n) {
    var r = te.exec(t);
    return r ? Math.max(0, r[2] - (n || 0)) + (r[3] || "px") : t
  }

  function Je(e, t, n, r, i, o) {
    var a = "width" === t ? 1 : 0,
      s = 0,
      l = 0;
    if (n === (r ? "border" : "content")) return 0;
    for (; a < 4; a += 2) "margin" === n && (l += x.css(e, n + ne[a], !0, i)), r ? ("content" === n && (l -= x.css(e, "padding" + ne[a], !0, i)), "margin" !== n && (l -= x.css(e, "border" + ne[a] + "Width", !0, i))) : (l += x.css(e, "padding" + ne[a], !0, i), "padding" !== n ? l += x.css(e, "border" + ne[a] + "Width", !0, i) : s += x.css(e, "border" + ne[a] + "Width", !0, i));
    return !r && 0 <= o && (l += Math.max(0, Math.ceil(e["offset" + t[0].toUpperCase() + t.slice(1)] - o - l - s - .5)) || 0), l
  }

  function Qe(e, t, n) {
    var r = Re(e),
      i = (!f.boxSizingReliable() || n) && "border-box" === x.css(e, "boxSizing", !1, r),
      o = i,
      a = Fe(e, t, r),
      s = "offset" + t[0].toUpperCase() + t.slice(1);
    if (ze.test(a)) {
      if (!n) return a;
      a = "auto"
    }
    return (!f.boxSizingReliable() && i || !f.reliableTrDimensions() && D(e, "tr") || "auto" === a || !parseFloat(a) && "inline" === x.css(e, "display", !1, r)) && e.getClientRects().length && (i = "border-box" === x.css(e, "boxSizing", !1, r), (o = s in e) && (a = e[s])), (a = parseFloat(a) || 0) + Je(e, t, n || (i ? "border" : "content"), o, r, a) + "px"
  }

  function et(e, t, n, r, i) {
    return new et.prototype.init(e, t, n, r, i)
  }
  x.extend({
    cssHooks: {
      opacity: {
        get: function(e, t) {
          if (t) {
            var n = Fe(e, "opacity");
            return "" === n ? "1" : n
          }
        }
      }
    },
    cssNumber: {
      animationIterationCount: !0,
      columnCount: !0,
      fillOpacity: !0,
      flexGrow: !0,
      flexShrink: !0,
      fontWeight: !0,
      gridArea: !0,
      gridColumn: !0,
      gridColumnEnd: !0,
      gridColumnStart: !0,
      gridRow: !0,
      gridRowEnd: !0,
      gridRowStart: !0,
      lineHeight: !0,
      opacity: !0,
      order: !0,
      orphans: !0,
      widows: !0,
      zIndex: !0,
      zoom: !0
    },
    cssProps: {},
    style: function(e, t, n, r) {
      if (e && 3 !== e.nodeType && 8 !== e.nodeType && e.style) {
        var i, o, a, s = U(t),
          l = Xe.test(t),
          c = e.style;
        if (l || (t = Ue(s)), a = x.cssHooks[t] || x.cssHooks[s], void 0 === n) return a && "get" in a && void 0 !== (i = a.get(e, !1, r)) ? i : c[t];
        "string" == (o = typeof n) && (i = te.exec(n)) && i[1] && (n = se(e, t, i), o = "number"), null != n && n == n && ("number" !== o || l || (n += i && i[3] || (x.cssNumber[s] ? "" : "px")), f.clearCloneStyle || "" !== n || 0 !== t.indexOf("background") || (c[t] = "inherit"), a && "set" in a && void 0 === (n = a.set(e, n, r)) || (l ? c.setProperty(t, n) : c[t] = n))
      }
    },
    css: function(e, t, n, r) {
      var i, o, a, s = U(t);
      return Xe.test(t) || (t = Ue(s)), (a = x.cssHooks[t] || x.cssHooks[s]) && "get" in a && (i = a.get(e, !0, n)), void 0 === i && (i = Fe(e, t, r)), "normal" === i && t in Ze && (i = Ze[t]), "" === n || n ? (o = parseFloat(i), !0 === n || isFinite(o) ? o || 0 : i) : i
    }
  }), x.each(["height", "width"], (function(e, t) {
    x.cssHooks[t] = {
      get: function(e, n, r) {
        if (n) return !Ve.test(x.css(e, "display")) || e.getClientRects().length && e.getBoundingClientRect().width ? Qe(e, t, r) : $e(e, Ge, (function() {
          return Qe(e, t, r)
        }))
      },
      set: function(e, n, r) {
        var i, o = Re(e),
          a = !f.scrollboxSize() && "absolute" === o.position,
          s = (a || r) && "border-box" === x.css(e, "boxSizing", !1, o),
          l = r ? Je(e, t, r, s, o) : 0;
        return s && a && (l -= Math.ceil(e["offset" + t[0].toUpperCase() + t.slice(1)] - parseFloat(o[t]) - Je(e, t, "border", !1, o) - .5)), l && (i = te.exec(n)) && "px" !== (i[3] || "px") && (e.style[t] = n, n = x.css(e, t)), Ke(0, n, l)
      }
    }
  })), x.cssHooks.marginLeft = Be(f.reliableMarginLeft, (function(e, t) {
    if (t) return (parseFloat(Fe(e, "marginLeft")) || e.getBoundingClientRect().left - $e(e, {
      marginLeft: 0
    }, (function() {
      return e.getBoundingClientRect().left
    }))) + "px"
  })), x.each({
    margin: "",
    padding: "",
    border: "Width"
  }, (function(e, t) {
    x.cssHooks[e + t] = {
      expand: function(n) {
        for (var r = 0, i = {}, o = "string" == typeof n ? n.split(" ") : [n]; r < 4; r++) i[e + ne[r] + t] = o[r] || o[r - 2] || o[0];
        return i
      }
    }, "margin" !== e && (x.cssHooks[e + t].set = Ke)
  })), x.fn.extend({
    css: function(e, t) {
      return B(this, (function(e, t, n) {
        var r, i, o = {},
          a = 0;
        if (Array.isArray(t)) {
          for (r = Re(e), i = t.length; a < i; a++) o[t[a]] = x.css(e, t[a], !1, r);
          return o
        }
        return void 0 !== n ? x.style(e, t, n) : x.css(e, t)
      }), e, t, 1 < arguments.length)
    }
  }), ((x.Tween = et).prototype = {
    constructor: et,
    init: function(e, t, n, r, i, o) {
      this.elem = e, this.prop = n, this.easing = i || x.easing._default, this.options = t, this.start = this.now = this.cur(), this.end = r, this.unit = o || (x.cssNumber[n] ? "" : "px")
    },
    cur: function() {
      var e = et.propHooks[this.prop];
      return e && e.get ? e.get(this) : et.propHooks._default.get(this)
    },
    run: function(e) {
      var t, n = et.propHooks[this.prop];
      return this.options.duration ? this.pos = t = x.easing[this.easing](e, this.options.duration * e, 0, 1, this.options.duration) : this.pos = t = e, this.now = (this.end - this.start) * t + this.start, this.options.step && this.options.step.call(this.elem, this.now, this), n && n.set ? n.set(this) : et.propHooks._default.set(this), this
    }
  }).init.prototype = et.prototype, (et.propHooks = {
    _default: {
      get: function(e) {
        var t;
        return 1 !== e.elem.nodeType || null != e.elem[e.prop] && null == e.elem.style[e.prop] ? e.elem[e.prop] : (t = x.css(e.elem, e.prop, "")) && "auto" !== t ? t : 0
      },
      set: function(e) {
        x.fx.step[e.prop] ? x.fx.step[e.prop](e) : 1 !== e.elem.nodeType || !x.cssHooks[e.prop] && null == e.elem.style[Ue(e.prop)] ? e.elem[e.prop] = e.now : x.style(e.elem, e.prop, e.now + e.unit)
      }
    }
  }).scrollTop = et.propHooks.scrollLeft = {
    set: function(e) {
      e.elem.nodeType && e.elem.parentNode && (e.elem[e.prop] = e.now)
    }
  }, x.easing = {
    linear: function(e) {
      return e
    },
    swing: function(e) {
      return .5 - Math.cos(e * Math.PI) / 2
    },
    _default: "swing"
  }, x.fx = et.prototype.init, x.fx.step = {};
  var tt, nt, rt, it, ot = /^(?:toggle|show|hide)$/,
    at = /queueHooks$/;

  function st() {
    nt && (!1 === g.hidden && e.requestAnimationFrame ? e.requestAnimationFrame(st) : e.setTimeout(st, x.fx.interval), x.fx.tick())
  }

  function lt() {
    return e.setTimeout((function() {
      tt = void 0
    })), tt = Date.now()
  }

  function ct(e, t) {
    var n, r = 0,
      i = {
        height: e
      };
    for (t = t ? 1 : 0; r < 4; r += 2 - t) i["margin" + (n = ne[r])] = i["padding" + n] = e;
    return t && (i.opacity = i.width = e), i
  }

  function ut(e, t, n) {
    for (var r, i = (dt.tweeners[t] || []).concat(dt.tweeners["*"]), o = 0, a = i.length; o < a; o++)
      if (r = i[o].call(n, t, e)) return r
  }

  function dt(e, t, n) {
    var r, i, o = 0,
      a = dt.prefilters.length,
      s = x.Deferred().always((function() {
        delete l.elem
      })),
      l = function() {
        if (i) return !1;
        for (var t = tt || lt(), n = Math.max(0, c.startTime + c.duration - t), r = 1 - (n / c.duration || 0), o = 0, a = c.tweens.length; o < a; o++) c.tweens[o].run(r);
        return s.notifyWith(e, [c, r, n]), r < 1 && a ? n : (a || s.notifyWith(e, [c, 1, 0]), s.resolveWith(e, [c]), !1)
      },
      c = s.promise({
        elem: e,
        props: x.extend({}, t),
        opts: x.extend(!0, {
          specialEasing: {},
          easing: x.easing._default
        }, n),
        originalProperties: t,
        originalOptions: n,
        startTime: tt || lt(),
        duration: n.duration,
        tweens: [],
        createTween: function(t, n) {
          var r = x.Tween(e, c.opts, t, n, c.opts.specialEasing[t] || c.opts.easing);
          return c.tweens.push(r), r
        },
        stop: function(t) {
          var n = 0,
            r = t ? c.tweens.length : 0;
          if (i) return this;
          for (i = !0; n < r; n++) c.tweens[n].run(1);
          return t ? (s.notifyWith(e, [c, 1, 0]), s.resolveWith(e, [c, t])) : s.rejectWith(e, [c, t]), this
        }
      }),
      u = c.props;
    for (function(e, t) {
        var n, r, i, o, a;
        for (n in e)
          if (i = t[r = U(n)], o = e[n], Array.isArray(o) && (i = o[1], o = e[n] = o[0]), n !== r && (e[r] = o, delete e[n]), (a = x.cssHooks[r]) && "expand" in a)
            for (n in o = a.expand(o), delete e[r], o) n in e || (e[n] = o[n], t[n] = i);
          else t[r] = i
      }(u, c.opts.specialEasing); o < a; o++)
      if (r = dt.prefilters[o].call(c, e, u, c.opts)) return h(r.stop) && (x._queueHooks(c.elem, c.opts.queue).stop = r.stop.bind(r)), r;
    return x.map(u, ut, c), h(c.opts.start) && c.opts.start.call(e, c), c.progress(c.opts.progress).done(c.opts.done, c.opts.complete).fail(c.opts.fail).always(c.opts.always), x.fx.timer(x.extend(l, {
      elem: e,
      anim: c,
      queue: c.opts.queue
    })), c
  }
  x.Animation = x.extend(dt, {
    tweeners: {
      "*": [function(e, t) {
        var n = this.createTween(e, t);
        return se(n.elem, e, te.exec(t), n), n
      }]
    },
    tweener: function(e, t) {
      h(e) ? (t = e, e = ["*"]) : e = e.match(j);
      for (var n, r = 0, i = e.length; r < i; r++) n = e[r], dt.tweeners[n] = dt.tweeners[n] || [], dt.tweeners[n].unshift(t)
    },
    prefilters: [function(e, t, n) {
      var r, i, o, a, s, l, c, u, d = "width" in t || "height" in t,
        p = this,
        f = {},
        h = e.style,
        m = e.nodeType && ae(e),
        g = G.get(e, "fxshow");
      for (r in n.queue || (null == (a = x._queueHooks(e, "fx")).unqueued && (a.unqueued = 0, s = a.empty.fire, a.empty.fire = function() {
          a.unqueued || s()
        }), a.unqueued++, p.always((function() {
          p.always((function() {
            a.unqueued--, x.queue(e, "fx").length || a.empty.fire()
          }))
        }))), t)
        if (i = t[r], ot.test(i)) {
          if (delete t[r], o = o || "toggle" === i, i === (m ? "hide" : "show")) {
            if ("show" !== i || !g || void 0 === g[r]) continue;
            m = !0
          }
          f[r] = g && g[r] || x.style(e, r)
        } if ((l = !x.isEmptyObject(t)) || !x.isEmptyObject(f))
        for (r in d && 1 === e.nodeType && (n.overflow = [h.overflow, h.overflowX, h.overflowY], null == (c = g && g.display) && (c = G.get(e, "display")), "none" === (u = x.css(e, "display")) && (c ? u = c : (ce([e], !0), c = e.style.display || c, u = x.css(e, "display"), ce([e]))), ("inline" === u || "inline-block" === u && null != c) && "none" === x.css(e, "float") && (l || (p.done((function() {
            h.display = c
          })), null == c && (u = h.display, c = "none" === u ? "" : u)), h.display = "inline-block")), n.overflow && (h.overflow = "hidden", p.always((function() {
            h.overflow = n.overflow[0], h.overflowX = n.overflow[1], h.overflowY = n.overflow[2]
          }))), l = !1, f) l || (g ? "hidden" in g && (m = g.hidden) : g = G.access(e, "fxshow", {
          display: c
        }), o && (g.hidden = !m), m && ce([e], !0), p.done((function() {
          for (r in m || ce([e]), G.remove(e, "fxshow"), f) x.style(e, r, f[r])
        }))), l = ut(m ? g[r] : 0, r, p), r in g || (g[r] = l.start, m && (l.end = l.start, l.start = 0))
    }],
    prefilter: function(e, t) {
      t ? dt.prefilters.unshift(e) : dt.prefilters.push(e)
    }
  }), x.speed = function(e, t, n) {
    var r = e && "object" == typeof e ? x.extend({}, e) : {
      complete: n || !n && t || h(e) && e,
      duration: e,
      easing: n && t || t && !h(t) && t
    };
    return x.fx.off ? r.duration = 0 : "number" != typeof r.duration && (r.duration in x.fx.speeds ? r.duration = x.fx.speeds[r.duration] : r.duration = x.fx.speeds._default), null != r.queue && !0 !== r.queue || (r.queue = "fx"), r.old = r.complete, r.complete = function() {
      h(r.old) && r.old.call(this), r.queue && x.dequeue(this, r.queue)
    }, r
  }, x.fn.extend({
    fadeTo: function(e, t, n, r) {
      return this.filter(ae).css("opacity", 0).show().end().animate({
        opacity: t
      }, e, n, r)
    },
    animate: function(e, t, n, r) {
      var i = x.isEmptyObject(e),
        o = x.speed(t, n, r),
        a = function() {
          var t = dt(this, x.extend({}, e), o);
          (i || G.get(this, "finish")) && t.stop(!0)
        };
      return a.finish = a, i || !1 === o.queue ? this.each(a) : this.queue(o.queue, a)
    },
    stop: function(e, t, n) {
      var r = function(e) {
        var t = e.stop;
        delete e.stop, t(n)
      };
      return "string" != typeof e && (n = t, t = e, e = void 0), t && this.queue(e || "fx", []), this.each((function() {
        var t = !0,
          i = null != e && e + "queueHooks",
          o = x.timers,
          a = G.get(this);
        if (i) a[i] && a[i].stop && r(a[i]);
        else
          for (i in a) a[i] && a[i].stop && at.test(i) && r(a[i]);
        for (i = o.length; i--;) o[i].elem !== this || null != e && o[i].queue !== e || (o[i].anim.stop(n), t = !1, o.splice(i, 1));
        !t && n || x.dequeue(this, e)
      }))
    },
    finish: function(e) {
      return !1 !== e && (e = e || "fx"), this.each((function() {
        var t, n = G.get(this),
          r = n[e + "queue"],
          i = n[e + "queueHooks"],
          o = x.timers,
          a = r ? r.length : 0;
        for (n.finish = !0, x.queue(this, e, []), i && i.stop && i.stop.call(this, !0), t = o.length; t--;) o[t].elem === this && o[t].queue === e && (o[t].anim.stop(!0), o.splice(t, 1));
        for (t = 0; t < a; t++) r[t] && r[t].finish && r[t].finish.call(this);
        delete n.finish
      }))
    }
  }), x.each(["toggle", "show", "hide"], (function(e, t) {
    var n = x.fn[t];
    x.fn[t] = function(e, r, i) {
      return null == e || "boolean" == typeof e ? n.apply(this, arguments) : this.animate(ct(t, !0), e, r, i)
    }
  })), x.each({
    slideDown: ct("show"),
    slideUp: ct("hide"),
    slideToggle: ct("toggle"),
    fadeIn: {
      opacity: "show"
    },
    fadeOut: {
      opacity: "hide"
    },
    fadeToggle: {
      opacity: "toggle"
    }
  }, (function(e, t) {
    x.fn[e] = function(e, n, r) {
      return this.animate(t, e, n, r)
    }
  })), x.timers = [], x.fx.tick = function() {
    var e, t = 0,
      n = x.timers;
    for (tt = Date.now(); t < n.length; t++)(e = n[t])() || n[t] !== e || n.splice(t--, 1);
    n.length || x.fx.stop(), tt = void 0
  }, x.fx.timer = function(e) {
    x.timers.push(e), x.fx.start()
  }, x.fx.interval = 13, x.fx.start = function() {
    nt || (nt = !0, st())
  }, x.fx.stop = function() {
    nt = null
  }, x.fx.speeds = {
    slow: 600,
    fast: 200,
    _default: 400
  }, x.fn.delay = function(t, n) {
    return t = x.fx && x.fx.speeds[t] || t, n = n || "fx", this.queue(n, (function(n, r) {
      var i = e.setTimeout(n, t);
      r.stop = function() {
        e.clearTimeout(i)
      }
    }))
  }, rt = g.createElement("input"), it = g.createElement("select").appendChild(g.createElement("option")), rt.type = "checkbox", f.checkOn = "" !== rt.value, f.optSelected = it.selected, (rt = g.createElement("input")).value = "t", rt.type = "radio", f.radioValue = "t" === rt.value;
  var pt, ft = x.expr.attrHandle;
  x.fn.extend({
    attr: function(e, t) {
      return B(this, x.attr, e, t, 1 < arguments.length)
    },
    removeAttr: function(e) {
      return this.each((function() {
        x.removeAttr(this, e)
      }))
    }
  }), x.extend({
    attr: function(e, t, n) {
      var r, i, o = e.nodeType;
      if (3 !== o && 8 !== o && 2 !== o) return void 0 === e.getAttribute ? x.prop(e, t, n) : (1 === o && x.isXMLDoc(e) || (i = x.attrHooks[t.toLowerCase()] || (x.expr.match.bool.test(t) ? pt : void 0)), void 0 !== n ? null === n ? void x.removeAttr(e, t) : i && "set" in i && void 0 !== (r = i.set(e, n, t)) ? r : (e.setAttribute(t, n + ""), n) : i && "get" in i && null !== (r = i.get(e, t)) ? r : null == (r = x.find.attr(e, t)) ? void 0 : r)
    },
    attrHooks: {
      type: {
        set: function(e, t) {
          if (!f.radioValue && "radio" === t && D(e, "input")) {
            var n = e.value;
            return e.setAttribute("type", t), n && (e.value = n), t
          }
        }
      }
    },
    removeAttr: function(e, t) {
      var n, r = 0,
        i = t && t.match(j);
      if (i && 1 === e.nodeType)
        for (; n = i[r++];) e.removeAttribute(n)
    }
  }), pt = {
    set: function(e, t, n) {
      return !1 === t ? x.removeAttr(e, n) : e.setAttribute(n, n), n
    }
  }, x.each(x.expr.match.bool.source.match(/\w+/g), (function(e, t) {
    var n = ft[t] || x.find.attr;
    ft[t] = function(e, t, r) {
      var i, o, a = t.toLowerCase();
      return r || (o = ft[a], ft[a] = i, i = null != n(e, t, r) ? a : null, ft[a] = o), i
    }
  }));
  var ht = /^(?:input|select|textarea|button)$/i,
    mt = /^(?:a|area)$/i;

  function gt(e) {
    return (e.match(j) || []).join(" ")
  }

  function vt(e) {
    return e.getAttribute && e.getAttribute("class") || ""
  }

  function yt(e) {
    return Array.isArray(e) ? e : "string" == typeof e && e.match(j) || []
  }
  x.fn.extend({
    prop: function(e, t) {
      return B(this, x.prop, e, t, 1 < arguments.length)
    },
    removeProp: function(e) {
      return this.each((function() {
        delete this[x.propFix[e] || e]
      }))
    }
  }), x.extend({
    prop: function(e, t, n) {
      var r, i, o = e.nodeType;
      if (3 !== o && 8 !== o && 2 !== o) return 1 === o && x.isXMLDoc(e) || (t = x.propFix[t] || t, i = x.propHooks[t]), void 0 !== n ? i && "set" in i && void 0 !== (r = i.set(e, n, t)) ? r : e[t] = n : i && "get" in i && null !== (r = i.get(e, t)) ? r : e[t]
    },
    propHooks: {
      tabIndex: {
        get: function(e) {
          var t = x.find.attr(e, "tabindex");
          return t ? parseInt(t, 10) : ht.test(e.nodeName) || mt.test(e.nodeName) && e.href ? 0 : -1
        }
      }
    },
    propFix: {
      for: "htmlFor",
      class: "className"
    }
  }), f.optSelected || (x.propHooks.selected = {
    get: function(e) {
      var t = e.parentNode;
      return t && t.parentNode && t.parentNode.selectedIndex, null
    },
    set: function(e) {
      var t = e.parentNode;
      t && (t.selectedIndex, t.parentNode && t.parentNode.selectedIndex)
    }
  }), x.each(["tabIndex", "readOnly", "maxLength", "cellSpacing", "cellPadding", "rowSpan", "colSpan", "useMap", "frameBorder", "contentEditable"], (function() {
    x.propFix[this.toLowerCase()] = this
  })), x.fn.extend({
    addClass: function(e) {
      var t, n, r, i, o, a, s, l = 0;
      if (h(e)) return this.each((function(t) {
        x(this).addClass(e.call(this, t, vt(this)))
      }));
      if ((t = yt(e)).length)
        for (; n = this[l++];)
          if (i = vt(n), r = 1 === n.nodeType && " " + gt(i) + " ") {
            for (a = 0; o = t[a++];) r.indexOf(" " + o + " ") < 0 && (r += o + " ");
            i !== (s = gt(r)) && n.setAttribute("class", s)
          } return this
    },
    removeClass: function(e) {
      var t, n, r, i, o, a, s, l = 0;
      if (h(e)) return this.each((function(t) {
        x(this).removeClass(e.call(this, t, vt(this)))
      }));
      if (!arguments.length) return this.attr("class", "");
      if ((t = yt(e)).length)
        for (; n = this[l++];)
          if (i = vt(n), r = 1 === n.nodeType && " " + gt(i) + " ") {
            for (a = 0; o = t[a++];)
              for (; - 1 < r.indexOf(" " + o + " ");) r = r.replace(" " + o + " ", " ");
            i !== (s = gt(r)) && n.setAttribute("class", s)
          } return this
    },
    toggleClass: function(e, t) {
      var n = typeof e,
        r = "string" === n || Array.isArray(e);
      return "boolean" == typeof t && r ? t ? this.addClass(e) : this.removeClass(e) : h(e) ? this.each((function(n) {
        x(this).toggleClass(e.call(this, n, vt(this), t), t)
      })) : this.each((function() {
        var t, i, o, a;
        if (r)
          for (i = 0, o = x(this), a = yt(e); t = a[i++];) o.hasClass(t) ? o.removeClass(t) : o.addClass(t);
        else void 0 !== e && "boolean" !== n || ((t = vt(this)) && G.set(this, "__className__", t), this.setAttribute && this.setAttribute("class", t || !1 === e ? "" : G.get(this, "__className__") || ""))
      }))
    },
    hasClass: function(e) {
      var t, n, r = 0;
      for (t = " " + e + " "; n = this[r++];)
        if (1 === n.nodeType && -1 < (" " + gt(vt(n)) + " ").indexOf(t)) return !0;
      return !1
    }
  });
  var bt = /\r/g;
  x.fn.extend({
    val: function(e) {
      var t, n, r, i = this[0];
      return arguments.length ? (r = h(e), this.each((function(n) {
        var i;
        1 === this.nodeType && (null == (i = r ? e.call(this, n, x(this).val()) : e) ? i = "" : "number" == typeof i ? i += "" : Array.isArray(i) && (i = x.map(i, (function(e) {
          return null == e ? "" : e + ""
        }))), (t = x.valHooks[this.type] || x.valHooks[this.nodeName.toLowerCase()]) && "set" in t && void 0 !== t.set(this, i, "value") || (this.value = i))
      }))) : i ? (t = x.valHooks[i.type] || x.valHooks[i.nodeName.toLowerCase()]) && "get" in t && void 0 !== (n = t.get(i, "value")) ? n : "string" == typeof(n = i.value) ? n.replace(bt, "") : null == n ? "" : n : void 0
    }
  }), x.extend({
    valHooks: {
      option: {
        get: function(e) {
          var t = x.find.attr(e, "value");
          return null != t ? t : gt(x.text(e))
        }
      },
      select: {
        get: function(e) {
          var t, n, r, i = e.options,
            o = e.selectedIndex,
            a = "select-one" === e.type,
            s = a ? null : [],
            l = a ? o + 1 : i.length;
          for (r = o < 0 ? l : a ? o : 0; r < l; r++)
            if (((n = i[r]).selected || r === o) && !n.disabled && (!n.parentNode.disabled || !D(n.parentNode, "optgroup"))) {
              if (t = x(n).val(), a) return t;
              s.push(t)
            } return s
        },
        set: function(e, t) {
          for (var n, r, i = e.options, o = x.makeArray(t), a = i.length; a--;)((r = i[a]).selected = -1 < x.inArray(x.valHooks.option.get(r), o)) && (n = !0);
          return n || (e.selectedIndex = -1), o
        }
      }
    }
  }), x.each(["radio", "checkbox"], (function() {
    x.valHooks[this] = {
      set: function(e, t) {
        if (Array.isArray(t)) return e.checked = -1 < x.inArray(x(e).val(), t)
      }
    }, f.checkOn || (x.valHooks[this].get = function(e) {
      return null === e.getAttribute("value") ? "on" : e.value
    })
  })), f.focusin = "onfocusin" in e;
  var wt = /^(?:focusinfocus|focusoutblur)$/,
    xt = function(e) {
      e.stopPropagation()
    };
  x.extend(x.event, {
    trigger: function(t, n, r, i) {
      var o, a, s, l, c, d, p, f, v = [r || g],
        y = u.call(t, "type") ? t.type : t,
        b = u.call(t, "namespace") ? t.namespace.split(".") : [];
      if (a = f = s = r = r || g, 3 !== r.nodeType && 8 !== r.nodeType && !wt.test(y + x.event.triggered) && (-1 < y.indexOf(".") && (y = (b = y.split(".")).shift(), b.sort()), c = y.indexOf(":") < 0 && "on" + y, (t = t[x.expando] ? t : new x.Event(y, "object" == typeof t && t)).isTrigger = i ? 2 : 3, t.namespace = b.join("."), t.rnamespace = t.namespace ? new RegExp("(^|\\.)" + b.join("\\.(?:.*\\.|)") + "(\\.|$)") : null, t.result = void 0, t.target || (t.target = r), n = null == n ? [t] : x.makeArray(n, [t]), p = x.event.special[y] || {}, i || !p.trigger || !1 !== p.trigger.apply(r, n))) {
        if (!i && !p.noBubble && !m(r)) {
          for (l = p.delegateType || y, wt.test(l + y) || (a = a.parentNode); a; a = a.parentNode) v.push(a), s = a;
          s === (r.ownerDocument || g) && v.push(s.defaultView || s.parentWindow || e)
        }
        for (o = 0;
          (a = v[o++]) && !t.isPropagationStopped();) f = a, t.type = 1 < o ? l : p.bindType || y, (d = (G.get(a, "events") || Object.create(null))[t.type] && G.get(a, "handle")) && d.apply(a, n), (d = c && a[c]) && d.apply && V(a) && (t.result = d.apply(a, n), !1 === t.result && t.preventDefault());
        return t.type = y, i || t.isDefaultPrevented() || p._default && !1 !== p._default.apply(v.pop(), n) || !V(r) || c && h(r[y]) && !m(r) && ((s = r[c]) && (r[c] = null), x.event.triggered = y, t.isPropagationStopped() && f.addEventListener(y, xt), r[y](), t.isPropagationStopped() && f.removeEventListener(y, xt), x.event.triggered = void 0, s && (r[c] = s)), t.result
      }
    },
    simulate: function(e, t, n) {
      var r = x.extend(new x.Event, n, {
        type: e,
        isSimulated: !0
      });
      x.event.trigger(r, null, t)
    }
  }), x.fn.extend({
    trigger: function(e, t) {
      return this.each((function() {
        x.event.trigger(e, t, this)
      }))
    },
    triggerHandler: function(e, t) {
      var n = this[0];
      if (n) return x.event.trigger(e, t, n, !0)
    }
  }), f.focusin || x.each({
    focus: "focusin",
    blur: "focusout"
  }, (function(e, t) {
    var n = function(e) {
      x.event.simulate(t, e.target, x.event.fix(e))
    };
    x.event.special[t] = {
      setup: function() {
        var r = this.ownerDocument || this.document || this,
          i = G.access(r, t);
        i || r.addEventListener(e, n, !0), G.access(r, t, (i || 0) + 1)
      },
      teardown: function() {
        var r = this.ownerDocument || this.document || this,
          i = G.access(r, t) - 1;
        i ? G.access(r, t, i) : (r.removeEventListener(e, n, !0), G.remove(r, t))
      }
    }
  }));
  var St = e.location,
    Ct = {
      guid: Date.now()
    },
    Et = /\?/;
  x.parseXML = function(t) {
    var n;
    if (!t || "string" != typeof t) return null;
    try {
      n = (new e.DOMParser).parseFromString(t, "text/xml")
    } catch (t) {
      n = void 0
    }
    return n && !n.getElementsByTagName("parsererror").length || x.error("Invalid XML: " + t), n
  };
  var Tt = /\[\]$/,
    kt = /\r?\n/g,
    Dt = /^(?:submit|button|image|reset|file)$/i,
    Ot = /^(?:input|select|textarea|keygen)/i;

  function At(e, t, n, r) {
    var i;
    if (Array.isArray(t)) x.each(t, (function(t, i) {
      n || Tt.test(e) ? r(e, i) : At(e + "[" + ("object" == typeof i && null != i ? t : "") + "]", i, n, r)
    }));
    else if (n || "object" !== b(t)) r(e, t);
    else
      for (i in t) At(e + "[" + i + "]", t[i], n, r)
  }
  x.param = function(e, t) {
    var n, r = [],
      i = function(e, t) {
        var n = h(t) ? t() : t;
        r[r.length] = encodeURIComponent(e) + "=" + encodeURIComponent(null == n ? "" : n)
      };
    if (null == e) return "";
    if (Array.isArray(e) || e.jquery && !x.isPlainObject(e)) x.each(e, (function() {
      i(this.name, this.value)
    }));
    else
      for (n in e) At(n, e[n], t, i);
    return r.join("&")
  }, x.fn.extend({
    serialize: function() {
      return x.param(this.serializeArray())
    },
    serializeArray: function() {
      return this.map((function() {
        var e = x.prop(this, "elements");
        return e ? x.makeArray(e) : this
      })).filter((function() {
        var e = this.type;
        return this.name && !x(this).is(":disabled") && Ot.test(this.nodeName) && !Dt.test(e) && (this.checked || !pe.test(e))
      })).map((function(e, t) {
        var n = x(this).val();
        return null == n ? null : Array.isArray(n) ? x.map(n, (function(e) {
          return {
            name: t.name,
            value: e.replace(kt, "\r\n")
          }
        })) : {
          name: t.name,
          value: n.replace(kt, "\r\n")
        }
      })).get()
    }
  });
  var _t = /%20/g,
    Mt = /#.*$/,
    Lt = /([?&])_=[^&]*/,
    It = /^(.*?):[ \t]*([^\r\n]*)$/gm,
    Pt = /^(?:GET|HEAD)$/,
    jt = /^\/\//,
    Nt = {},
    zt = {},
    Rt = "*/".concat("*"),
    $t = g.createElement("a");

  function Ht(e) {
    return function(t, n) {
      "string" != typeof t && (n = t, t = "*");
      var r, i = 0,
        o = t.toLowerCase().match(j) || [];
      if (h(n))
        for (; r = o[i++];) "+" === r[0] ? (r = r.slice(1) || "*", (e[r] = e[r] || []).unshift(n)) : (e[r] = e[r] || []).push(n)
    }
  }

  function Ft(e, t, n, r) {
    var i = {},
      o = e === zt;

    function a(s) {
      var l;
      return i[s] = !0, x.each(e[s] || [], (function(e, s) {
        var c = s(t, n, r);
        return "string" != typeof c || o || i[c] ? o ? !(l = c) : void 0 : (t.dataTypes.unshift(c), a(c), !1)
      })), l
    }
    return a(t.dataTypes[0]) || !i["*"] && a("*")
  }

  function Bt(e, t) {
    var n, r, i = x.ajaxSettings.flatOptions || {};
    for (n in t) void 0 !== t[n] && ((i[n] ? e : r || (r = {}))[n] = t[n]);
    return r && x.extend(!0, e, r), e
  }
  $t.href = St.href, x.extend({
    active: 0,
    lastModified: {},
    etag: {},
    ajaxSettings: {
      url: St.href,
      type: "GET",
      isLocal: /^(?:about|app|app-storage|.+-extension|file|res|widget):$/.test(St.protocol),
      global: !0,
      processData: !0,
      async: !0,
      contentType: "application/x-www-form-urlencoded; charset=UTF-8",
      accepts: {
        "*": Rt,
        text: "text/plain",
        html: "text/html",
        xml: "application/xml, text/xml",
        json: "application/json, text/javascript"
      },
      contents: {
        xml: /\bxml\b/,
        html: /\bhtml/,
        json: /\bjson\b/
      },
      responseFields: {
        xml: "responseXML",
        text: "responseText",
        json: "responseJSON"
      },
      converters: {
        "* text": String,
        "text html": !0,
        "text json": JSON.parse,
        "text xml": x.parseXML
      },
      flatOptions: {
        url: !0,
        context: !0
      }
    },
    ajaxSetup: function(e, t) {
      return t ? Bt(Bt(e, x.ajaxSettings), t) : Bt(x.ajaxSettings, e)
    },
    ajaxPrefilter: Ht(Nt),
    ajaxTransport: Ht(zt),
    ajax: function(t, n) {
      "object" == typeof t && (n = t, t = void 0), n = n || {};
      var r, i, o, a, s, l, c, u, d, p, f = x.ajaxSetup({}, n),
        h = f.context || f,
        m = f.context && (h.nodeType || h.jquery) ? x(h) : x.event,
        v = x.Deferred(),
        y = x.Callbacks("once memory"),
        b = f.statusCode || {},
        w = {},
        S = {},
        C = "canceled",
        E = {
          readyState: 0,
          getResponseHeader: function(e) {
            var t;
            if (c) {
              if (!a)
                for (a = {}; t = It.exec(o);) a[t[1].toLowerCase() + " "] = (a[t[1].toLowerCase() + " "] || []).concat(t[2]);
              t = a[e.toLowerCase() + " "]
            }
            return null == t ? null : t.join(", ")
          },
          getAllResponseHeaders: function() {
            return c ? o : null
          },
          setRequestHeader: function(e, t) {
            return null == c && (e = S[e.toLowerCase()] = S[e.toLowerCase()] || e, w[e] = t), this
          },
          overrideMimeType: function(e) {
            return null == c && (f.mimeType = e), this
          },
          statusCode: function(e) {
            var t;
            if (e)
              if (c) E.always(e[E.status]);
              else
                for (t in e) b[t] = [b[t], e[t]];
            return this
          },
          abort: function(e) {
            var t = e || C;
            return r && r.abort(t), T(0, t), this
          }
        };
      if (v.promise(E), f.url = ((t || f.url || St.href) + "").replace(jt, St.protocol + "//"), f.type = n.method || n.type || f.method || f.type, f.dataTypes = (f.dataType || "*").toLowerCase().match(j) || [""], null == f.crossDomain) {
        l = g.createElement("a");
        try {
          l.href = f.url, l.href = l.href, f.crossDomain = $t.protocol + "//" + $t.host != l.protocol + "//" + l.host
        } catch (t) {
          f.crossDomain = !0
        }
      }
      if (f.data && f.processData && "string" != typeof f.data && (f.data = x.param(f.data, f.traditional)), Ft(Nt, f, n, E), c) return E;
      for (d in (u = x.event && f.global) && 0 == x.active++ && x.event.trigger("ajaxStart"), f.type = f.type.toUpperCase(), f.hasContent = !Pt.test(f.type), i = f.url.replace(Mt, ""), f.hasContent ? f.data && f.processData && 0 === (f.contentType || "").indexOf("application/x-www-form-urlencoded") && (f.data = f.data.replace(_t, "+")) : (p = f.url.slice(i.length), f.data && (f.processData || "string" == typeof f.data) && (i += (Et.test(i) ? "&" : "?") + f.data, delete f.data), !1 === f.cache && (i = i.replace(Lt, "$1"), p = (Et.test(i) ? "&" : "?") + "_=" + Ct.guid++ + p), f.url = i + p), f.ifModified && (x.lastModified[i] && E.setRequestHeader("If-Modified-Since", x.lastModified[i]), x.etag[i] && E.setRequestHeader("If-None-Match", x.etag[i])), (f.data && f.hasContent && !1 !== f.contentType || n.contentType) && E.setRequestHeader("Content-Type", f.contentType), E.setRequestHeader("Accept", f.dataTypes[0] && f.accepts[f.dataTypes[0]] ? f.accepts[f.dataTypes[0]] + ("*" !== f.dataTypes[0] ? ", " + Rt + "; q=0.01" : "") : f.accepts["*"]), f.headers) E.setRequestHeader(d, f.headers[d]);
      if (f.beforeSend && (!1 === f.beforeSend.call(h, E, f) || c)) return E.abort();
      if (C = "abort", y.add(f.complete), E.done(f.success), E.fail(f.error), r = Ft(zt, f, n, E)) {
        if (E.readyState = 1, u && m.trigger("ajaxSend", [E, f]), c) return E;
        f.async && 0 < f.timeout && (s = e.setTimeout((function() {
          E.abort("timeout")
        }), f.timeout));
        try {
          c = !1, r.send(w, T)
        } catch (t) {
          if (c) throw t;
          T(-1, t)
        }
      } else T(-1, "No Transport");

      function T(t, n, a, l) {
        var d, p, g, w, S, C = n;
        c || (c = !0, s && e.clearTimeout(s), r = void 0, o = l || "", E.readyState = 0 < t ? 4 : 0, d = 200 <= t && t < 300 || 304 === t, a && (w = function(e, t, n) {
          for (var r, i, o, a, s = e.contents, l = e.dataTypes;
            "*" === l[0];) l.shift(), void 0 === r && (r = e.mimeType || t.getResponseHeader("Content-Type"));
          if (r)
            for (i in s)
              if (s[i] && s[i].test(r)) {
                l.unshift(i);
                break
              } if (l[0] in n) o = l[0];
          else {
            for (i in n) {
              if (!l[0] || e.converters[i + " " + l[0]]) {
                o = i;
                break
              }
              a || (a = i)
            }
            o = o || a
          }
          if (o) return o !== l[0] && l.unshift(o), n[o]
        }(f, E, a)), !d && -1 < x.inArray("script", f.dataTypes) && (f.converters["text script"] = function() {}), w = function(e, t, n, r) {
          var i, o, a, s, l, c = {},
            u = e.dataTypes.slice();
          if (u[1])
            for (a in e.converters) c[a.toLowerCase()] = e.converters[a];
          for (o = u.shift(); o;)
            if (e.responseFields[o] && (n[e.responseFields[o]] = t), !l && r && e.dataFilter && (t = e.dataFilter(t, e.dataType)), l = o, o = u.shift())
              if ("*" === o) o = l;
              else if ("*" !== l && l !== o) {
            if (!(a = c[l + " " + o] || c["* " + o]))
              for (i in c)
                if ((s = i.split(" "))[1] === o && (a = c[l + " " + s[0]] || c["* " + s[0]])) {
                  !0 === a ? a = c[i] : !0 !== c[i] && (o = s[0], u.unshift(s[1]));
                  break
                } if (!0 !== a)
              if (a && e.throws) t = a(t);
              else try {
                t = a(t)
              } catch (e) {
                return {
                  state: "parsererror",
                  error: a ? e : "No conversion from " + l + " to " + o
                }
              }
          }
          return {
            state: "success",
            data: t
          }
        }(f, w, E, d), d ? (f.ifModified && ((S = E.getResponseHeader("Last-Modified")) && (x.lastModified[i] = S), (S = E.getResponseHeader("etag")) && (x.etag[i] = S)), 204 === t || "HEAD" === f.type ? C = "nocontent" : 304 === t ? C = "notmodified" : (C = w.state, p = w.data, d = !(g = w.error))) : (g = C, !t && C || (C = "error", t < 0 && (t = 0))), E.status = t, E.statusText = (n || C) + "", d ? v.resolveWith(h, [p, C, E]) : v.rejectWith(h, [E, C, g]), E.statusCode(b), b = void 0, u && m.trigger(d ? "ajaxSuccess" : "ajaxError", [E, f, d ? p : g]), y.fireWith(h, [E, C]), u && (m.trigger("ajaxComplete", [E, f]), --x.active || x.event.trigger("ajaxStop")))
      }
      return E
    },
    getJSON: function(e, t, n) {
      return x.get(e, t, n, "json")
    },
    getScript: function(e, t) {
      return x.get(e, void 0, t, "script")
    }
  }), x.each(["get", "post"], (function(e, t) {
    x[t] = function(e, n, r, i) {
      return h(n) && (i = i || r, r = n, n = void 0), x.ajax(x.extend({
        url: e,
        type: t,
        dataType: i,
        data: n,
        success: r
      }, x.isPlainObject(e) && e))
    }
  })), x.ajaxPrefilter((function(e) {
    var t;
    for (t in e.headers) "content-type" === t.toLowerCase() && (e.contentType = e.headers[t] || "")
  })), x._evalUrl = function(e, t, n) {
    return x.ajax({
      url: e,
      type: "GET",
      dataType: "script",
      cache: !0,
      async: !1,
      global: !1,
      converters: {
        "text script": function() {}
      },
      dataFilter: function(e) {
        x.globalEval(e, t, n)
      }
    })
  }, x.fn.extend({
    wrapAll: function(e) {
      var t;
      return this[0] && (h(e) && (e = e.call(this[0])), t = x(e, this[0].ownerDocument).eq(0).clone(!0), this[0].parentNode && t.insertBefore(this[0]), t.map((function() {
        for (var e = this; e.firstElementChild;) e = e.firstElementChild;
        return e
      })).append(this)), this
    },
    wrapInner: function(e) {
      return h(e) ? this.each((function(t) {
        x(this).wrapInner(e.call(this, t))
      })) : this.each((function() {
        var t = x(this),
          n = t.contents();
        n.length ? n.wrapAll(e) : t.append(e)
      }))
    },
    wrap: function(e) {
      var t = h(e);
      return this.each((function(n) {
        x(this).wrapAll(t ? e.call(this, n) : e)
      }))
    },
    unwrap: function(e) {
      return this.parent(e).not("body").each((function() {
        x(this).replaceWith(this.childNodes)
      })), this
    }
  }), x.expr.pseudos.hidden = function(e) {
    return !x.expr.pseudos.visible(e)
  }, x.expr.pseudos.visible = function(e) {
    return !!(e.offsetWidth || e.offsetHeight || e.getClientRects().length)
  }, x.ajaxSettings.xhr = function() {
    try {
      return new e.XMLHttpRequest
    } catch (e) {}
  };
  var qt = {
      0: 200,
      1223: 204
    },
    Wt = x.ajaxSettings.xhr();
  f.cors = !!Wt && "withCredentials" in Wt, f.ajax = Wt = !!Wt, x.ajaxTransport((function(t) {
    var n, r;
    if (f.cors || Wt && !t.crossDomain) return {
      send: function(i, o) {
        var a, s = t.xhr();
        if (s.open(t.type, t.url, t.async, t.username, t.password), t.xhrFields)
          for (a in t.xhrFields) s[a] = t.xhrFields[a];
        for (a in t.mimeType && s.overrideMimeType && s.overrideMimeType(t.mimeType), t.crossDomain || i["X-Requested-With"] || (i["X-Requested-With"] = "XMLHttpRequest"), i) s.setRequestHeader(a, i[a]);
        n = function(e) {
          return function() {
            n && (n = r = s.onload = s.onerror = s.onabort = s.ontimeout = s.onreadystatechange = null, "abort" === e ? s.abort() : "error" === e ? "number" != typeof s.status ? o(0, "error") : o(s.status, s.statusText) : o(qt[s.status] || s.status, s.statusText, "text" !== (s.responseType || "text") || "string" != typeof s.responseText ? {
              binary: s.response
            } : {
              text: s.responseText
            }, s.getAllResponseHeaders()))
          }
        }, s.onload = n(), r = s.onerror = s.ontimeout = n("error"), void 0 !== s.onabort ? s.onabort = r : s.onreadystatechange = function() {
          4 === s.readyState && e.setTimeout((function() {
            n && r()
          }))
        }, n = n("abort");
        try {
          s.send(t.hasContent && t.data || null)
        } catch (i) {
          if (n) throw i
        }
      },
      abort: function() {
        n && n()
      }
    }
  })), x.ajaxPrefilter((function(e) {
    e.crossDomain && (e.contents.script = !1)
  })), x.ajaxSetup({
    accepts: {
      script: "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript"
    },
    contents: {
      script: /\b(?:java|ecma)script\b/
    },
    converters: {
      "text script": function(e) {
        return x.globalEval(e), e
      }
    }
  }), x.ajaxPrefilter("script", (function(e) {
    void 0 === e.cache && (e.cache = !1), e.crossDomain && (e.type = "GET")
  })), x.ajaxTransport("script", (function(e) {
    var t, n;
    if (e.crossDomain || e.scriptAttrs) return {
      send: function(r, i) {
        t = x("<script>").attr(e.scriptAttrs || {}).prop({
          charset: e.scriptCharset,
          src: e.url
        }).on("load error", n = function(e) {
          t.remove(), n = null, e && i("error" === e.type ? 404 : 200, e.type)
        }), g.head.appendChild(t[0])
      },
      abort: function() {
        n && n()
      }
    }
  }));
  var Yt, Ut = [],
    Vt = /(=)\?(?=&|$)|\?\?/;
  x.ajaxSetup({
    jsonp: "callback",
    jsonpCallback: function() {
      var e = Ut.pop() || x.expando + "_" + Ct.guid++;
      return this[e] = !0, e
    }
  }), x.ajaxPrefilter("json jsonp", (function(t, n, r) {
    var i, o, a, s = !1 !== t.jsonp && (Vt.test(t.url) ? "url" : "string" == typeof t.data && 0 === (t.contentType || "").indexOf("application/x-www-form-urlencoded") && Vt.test(t.data) && "data");
    if (s || "jsonp" === t.dataTypes[0]) return i = t.jsonpCallback = h(t.jsonpCallback) ? t.jsonpCallback() : t.jsonpCallback, s ? t[s] = t[s].replace(Vt, "$1" + i) : !1 !== t.jsonp && (t.url += (Et.test(t.url) ? "&" : "?") + t.jsonp + "=" + i), t.converters["script json"] = function() {
      return a || x.error(i + " was not called"), a[0]
    }, t.dataTypes[0] = "json", o = e[i], e[i] = function() {
      a = arguments
    }, r.always((function() {
      void 0 === o ? x(e).removeProp(i) : e[i] = o, t[i] && (t.jsonpCallback = n.jsonpCallback, Ut.push(i)), a && h(o) && o(a[0]), a = o = void 0
    })), "script"
  })), f.createHTMLDocument = ((Yt = g.implementation.createHTMLDocument("").body).innerHTML = "<form></form><form></form>", 2 === Yt.childNodes.length), x.parseHTML = function(e, t, n) {
    return "string" != typeof e ? [] : ("boolean" == typeof t && (n = t, t = !1), t || (f.createHTMLDocument ? ((r = (t = g.implementation.createHTMLDocument("")).createElement("base")).href = g.location.href, t.head.appendChild(r)) : t = g), o = !n && [], (i = O.exec(e)) ? [t.createElement(i[1])] : (i = be([e], t, o), o && o.length && x(o).remove(), x.merge([], i.childNodes)));
    var r, i, o
  }, x.fn.load = function(e, t, n) {
    var r, i, o, a = this,
      s = e.indexOf(" ");
    return -1 < s && (r = gt(e.slice(s)), e = e.slice(0, s)), h(t) ? (n = t, t = void 0) : t && "object" == typeof t && (i = "POST"), 0 < a.length && x.ajax({
      url: e,
      type: i || "GET",
      dataType: "html",
      data: t
    }).done((function(e) {
      o = arguments, a.html(r ? x("<div>").append(x.parseHTML(e)).find(r) : e)
    })).always(n && function(e, t) {
      a.each((function() {
        n.apply(this, o || [e.responseText, t, e])
      }))
    }), this
  }, x.expr.pseudos.animated = function(e) {
    return x.grep(x.timers, (function(t) {
      return e === t.elem
    })).length
  }, x.offset = {
    setOffset: function(e, t, n) {
      var r, i, o, a, s, l, c = x.css(e, "position"),
        u = x(e),
        d = {};
      "static" === c && (e.style.position = "relative"), s = u.offset(), o = x.css(e, "top"), l = x.css(e, "left"), ("absolute" === c || "fixed" === c) && -1 < (o + l).indexOf("auto") ? (a = (r = u.position()).top, i = r.left) : (a = parseFloat(o) || 0, i = parseFloat(l) || 0), h(t) && (t = t.call(e, n, x.extend({}, s))), null != t.top && (d.top = t.top - s.top + a), null != t.left && (d.left = t.left - s.left + i), "using" in t ? t.using.call(e, d) : ("number" == typeof d.top && (d.top += "px"), "number" == typeof d.left && (d.left += "px"), u.css(d))
    }
  }, x.fn.extend({
    offset: function(e) {
      if (arguments.length) return void 0 === e ? this : this.each((function(t) {
        x.offset.setOffset(this, e, t)
      }));
      var t, n, r = this[0];
      return r ? r.getClientRects().length ? (t = r.getBoundingClientRect(), n = r.ownerDocument.defaultView, {
        top: t.top + n.pageYOffset,
        left: t.left + n.pageXOffset
      }) : {
        top: 0,
        left: 0
      } : void 0
    },
    position: function() {
      if (this[0]) {
        var e, t, n, r = this[0],
          i = {
            top: 0,
            left: 0
          };
        if ("fixed" === x.css(r, "position")) t = r.getBoundingClientRect();
        else {
          for (t = this.offset(), n = r.ownerDocument, e = r.offsetParent || n.documentElement; e && (e === n.body || e === n.documentElement) && "static" === x.css(e, "position");) e = e.parentNode;
          e && e !== r && 1 === e.nodeType && ((i = x(e).offset()).top += x.css(e, "borderTopWidth", !0), i.left += x.css(e, "borderLeftWidth", !0))
        }
        return {
          top: t.top - i.top - x.css(r, "marginTop", !0),
          left: t.left - i.left - x.css(r, "marginLeft", !0)
        }
      }
    },
    offsetParent: function() {
      return this.map((function() {
        for (var e = this.offsetParent; e && "static" === x.css(e, "position");) e = e.offsetParent;
        return e || re
      }))
    }
  }), x.each({
    scrollLeft: "pageXOffset",
    scrollTop: "pageYOffset"
  }, (function(e, t) {
    var n = "pageYOffset" === t;
    x.fn[e] = function(r) {
      return B(this, (function(e, r, i) {
        var o;
        if (m(e) ? o = e : 9 === e.nodeType && (o = e.defaultView), void 0 === i) return o ? o[t] : e[r];
        o ? o.scrollTo(n ? o.pageXOffset : i, n ? i : o.pageYOffset) : e[r] = i
      }), e, r, arguments.length)
    }
  })), x.each(["top", "left"], (function(e, t) {
    x.cssHooks[t] = Be(f.pixelPosition, (function(e, n) {
      if (n) return n = Fe(e, t), ze.test(n) ? x(e).position()[t] + "px" : n
    }))
  })), x.each({
    Height: "height",
    Width: "width"
  }, (function(e, t) {
    x.each({
      padding: "inner" + e,
      content: t,
      "": "outer" + e
    }, (function(n, r) {
      x.fn[r] = function(i, o) {
        var a = arguments.length && (n || "boolean" != typeof i),
          s = n || (!0 === i || !0 === o ? "margin" : "border");
        return B(this, (function(t, n, i) {
          var o;
          return m(t) ? 0 === r.indexOf("outer") ? t["inner" + e] : t.document.documentElement["client" + e] : 9 === t.nodeType ? (o = t.documentElement, Math.max(t.body["scroll" + e], o["scroll" + e], t.body["offset" + e], o["offset" + e], o["client" + e])) : void 0 === i ? x.css(t, n, s) : x.style(t, n, i, s)
        }), t, a ? i : void 0, a)
      }
    }))
  })), x.each(["ajaxStart", "ajaxStop", "ajaxComplete", "ajaxError", "ajaxSuccess", "ajaxSend"], (function(e, t) {
    x.fn[t] = function(e) {
      return this.on(t, e)
    }
  })), x.fn.extend({
    bind: function(e, t, n) {
      return this.on(e, null, t, n)
    },
    unbind: function(e, t) {
      return this.off(e, null, t)
    },
    delegate: function(e, t, n, r) {
      return this.on(t, e, n, r)
    },
    undelegate: function(e, t, n) {
      return 1 === arguments.length ? this.off(e, "**") : this.off(t, e || "**", n)
    },
    hover: function(e, t) {
      return this.mouseenter(e).mouseleave(t || e)
    }
  }), x.each("blur focus focusin focusout resize scroll click dblclick mousedown mouseup mousemove mouseover mouseout mouseenter mouseleave change select submit keydown keypress keyup contextmenu".split(" "), (function(e, t) {
    x.fn[t] = function(e, n) {
      return 0 < arguments.length ? this.on(t, null, e, n) : this.trigger(t)
    }
  }));
  var Xt = /^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g;
  x.proxy = function(e, t) {
    var n, r, o;
    if ("string" == typeof t && (n = e[t], t = e, e = n), h(e)) return r = i.call(arguments, 2), (o = function() {
      return e.apply(t || this, r.concat(i.call(arguments)))
    }).guid = e.guid = e.guid || x.guid++, o
  }, x.holdReady = function(e) {
    e ? x.readyWait++ : x.ready(!0)
  }, x.isArray = Array.isArray, x.parseJSON = JSON.parse, x.nodeName = D, x.isFunction = h, x.isWindow = m, x.camelCase = U, x.type = b, x.now = Date.now, x.isNumeric = function(e) {
    var t = x.type(e);
    return ("number" === t || "string" === t) && !isNaN(e - parseFloat(e))
  }, x.trim = function(e) {
    return null == e ? "" : (e + "").replace(Xt, "")
  }, "function" == typeof define && define.amd && define("jquery", [], (function() {
    return x
  }));
  var Gt = e.jQuery,
    Zt = e.$;
  return x.noConflict = function(t) {
    return e.$ === x && (e.$ = Zt), t && e.jQuery === x && (e.jQuery = Gt), x
  }, void 0 === t && (e.jQuery = e.$ = x), x
})),
function(e, t) {
  "object" == typeof exports && "undefined" != typeof module ? module.exports = t() : "function" == typeof define && define.amd ? define(t) : (e = e || self).SimpleBar = t()
}(this, (function() {
  "use strict";
  var e = "undefined" != typeof globalThis ? globalThis : "undefined" != typeof window ? window : "undefined" != typeof global ? global : "undefined" != typeof self ? self : {};

  function t(e, t) {
    return e(t = {
      exports: {}
    }, t.exports), t.exports
  }
  var n, r, i = function(e) {
      return e && e.Math == Math && e
    },
    o = i("object" == typeof globalThis && globalThis) || i("object" == typeof window && window) || i("object" == typeof self && self) || i("object" == typeof e && e) || function() {
      return this
    }() || Function("return this")(),
    a = Object.defineProperty,
    s = function(e, t) {
      try {
        a(o, e, {
          value: t,
          configurable: !0,
          writable: !0
        })
      } catch (n) {
        o[e] = t
      }
      return t
    },
    l = o["__core-js_shared__"] || s("__core-js_shared__", {}),
    c = t((function(e) {
      (e.exports = function(e, t) {
        return l[e] || (l[e] = void 0 !== t ? t : {})
      })("versions", []).push({
        version: "3.22.6",
        mode: "global",
        copyright: "© 2014-2022 Denis Pushkarev (zloirock.ru)",
        license: "https://github.com/zloirock/core-js/blob/v3.22.6/LICENSE",
        source: "https://github.com/zloirock/core-js"
      })
    })),
    u = function(e) {
      try {
        return !!e()
      } catch (e) {
        return !0
      }
    },
    d = !u((function() {
      var e = function() {}.bind();
      return "function" != typeof e || e.hasOwnProperty("prototype")
    })),
    p = Function.prototype,
    f = p.bind,
    h = p.call,
    m = d && f.bind(h, h),
    g = d ? function(e) {
      return e && m(e)
    } : function(e) {
      return e && function() {
        return h.apply(e, arguments)
      }
    },
    v = o.TypeError,
    y = function(e) {
      if (null == e) throw v("Can't call method on " + e);
      return e
    },
    b = o.Object,
    w = function(e) {
      return b(y(e))
    },
    x = g({}.hasOwnProperty),
    S = Object.hasOwn || function(e, t) {
      return x(w(e), t)
    },
    C = 0,
    E = Math.random(),
    T = g(1..toString),
    k = function(e) {
      return "Symbol(" + (void 0 === e ? "" : e) + ")_" + T(++C + E, 36)
    },
    D = function(e) {
      return "function" == typeof e
    },
    O = function(e) {
      return D(e) ? e : void 0
    },
    A = function(e, t) {
      return arguments.length < 2 ? O(o[e]) : o[e] && o[e][t]
    },
    _ = A("navigator", "userAgent") || "",
    M = o.process,
    L = o.Deno,
    I = M && M.versions || L && L.version,
    P = I && I.v8;
  P && (r = (n = P.split("."))[0] > 0 && n[0] < 4 ? 1 : +(n[0] + n[1])), !r && _ && (!(n = _.match(/Edge\/(\d+)/)) || n[1] >= 74) && (n = _.match(/Chrome\/(\d+)/)) && (r = +n[1]);
  var j = r,
    N = !!Object.getOwnPropertySymbols && !u((function() {
      var e = Symbol();
      return !String(e) || !(Object(e) instanceof Symbol) || !Symbol.sham && j && j < 41
    })),
    z = N && !Symbol.sham && "symbol" == typeof Symbol.iterator,
    R = c("wks"),
    $ = o.Symbol,
    H = $ && $.for,
    F = z ? $ : $ && $.withoutSetter || k,
    B = function(e) {
      if (!S(R, e) || !N && "string" != typeof R[e]) {
        var t = "Symbol." + e;
        N && S($, e) ? R[e] = $[e] : R[e] = z && H ? H(t) : F(t)
      }
      return R[e]
    },
    q = {};
  q[B("toStringTag")] = "z";
  var W = "[object z]" === String(q),
    Y = !u((function() {
      return 7 != Object.defineProperty({}, 1, {
        get: function() {
          return 7
        }
      })[1]
    })),
    U = function(e) {
      return "object" == typeof e ? null !== e : D(e)
    },
    V = o.document,
    X = U(V) && U(V.createElement),
    G = function(e) {
      return X ? V.createElement(e) : {}
    },
    Z = !Y && !u((function() {
      return 7 != Object.defineProperty(G("div"), "a", {
        get: function() {
          return 7
        }
      }).a
    })),
    K = Y && u((function() {
      return 42 != Object.defineProperty((function() {}), "prototype", {
        value: 42,
        writable: !1
      }).prototype
    })),
    J = o.String,
    Q = o.TypeError,
    ee = function(e) {
      if (U(e)) return e;
      throw Q(J(e) + " is not an object")
    },
    te = Function.prototype.call,
    ne = d ? te.bind(te) : function() {
      return te.apply(te, arguments)
    },
    re = g({}.isPrototypeOf),
    ie = o.Object,
    oe = z ? function(e) {
      return "symbol" == typeof e
    } : function(e) {
      var t = A("Symbol");
      return D(t) && re(t.prototype, ie(e))
    },
    ae = o.String,
    se = function(e) {
      try {
        return ae(e)
      } catch (e) {
        return "Object"
      }
    },
    le = o.TypeError,
    ce = function(e) {
      if (D(e)) return e;
      throw le(se(e) + " is not a function")
    },
    ue = function(e, t) {
      var n = e[t];
      return null == n ? void 0 : ce(n)
    },
    de = o.TypeError,
    pe = o.TypeError,
    fe = B("toPrimitive"),
    he = function(e) {
      var t = function(e, t) {
        if (!U(e) || oe(e)) return e;
        var n, r = ue(e, fe);
        if (r) {
          if (void 0 === t && (t = "default"), n = ne(r, e, t), !U(n) || oe(n)) return n;
          throw pe("Can't convert object to primitive value")
        }
        return void 0 === t && (t = "number"),
          function(e, t) {
            var n, r;
            if ("string" === t && D(n = e.toString) && !U(r = ne(n, e))) return r;
            if (D(n = e.valueOf) && !U(r = ne(n, e))) return r;
            if ("string" !== t && D(n = e.toString) && !U(r = ne(n, e))) return r;
            throw de("Can't convert object to primitive value")
          }(e, t)
      }(e, "string");
      return oe(t) ? t : t + ""
    },
    me = o.TypeError,
    ge = Object.defineProperty,
    ve = Object.getOwnPropertyDescriptor,
    ye = {
      f: Y ? K ? function(e, t, n) {
        if (ee(e), t = he(t), ee(n), "function" == typeof e && "prototype" === t && "value" in n && "writable" in n && !n.writable) {
          var r = ve(e, t);
          r && r.writable && (e[t] = n.value, n = {
            configurable: "configurable" in n ? n.configurable : r.configurable,
            enumerable: "enumerable" in n ? n.enumerable : r.enumerable,
            writable: !1
          })
        }
        return ge(e, t, n)
      } : ge : function(e, t, n) {
        if (ee(e), t = he(t), ee(n), Z) try {
          return ge(e, t, n)
        } catch (e) {}
        if ("get" in n || "set" in n) throw me("Accessors not supported");
        return "value" in n && (e[t] = n.value), e
      }
    },
    be = function(e, t) {
      return {
        enumerable: !(1 & e),
        configurable: !(2 & e),
        writable: !(4 & e),
        value: t
      }
    },
    we = Y ? function(e, t, n) {
      return ye.f(e, t, be(1, n))
    } : function(e, t, n) {
      return e[t] = n, e
    },
    xe = Function.prototype,
    Se = Y && Object.getOwnPropertyDescriptor,
    Ce = S(xe, "name"),
    Ee = {
      EXISTS: Ce,
      PROPER: Ce && "something" === function() {}.name,
      CONFIGURABLE: Ce && (!Y || Y && Se(xe, "name").configurable)
    },
    Te = g(Function.toString);
  D(l.inspectSource) || (l.inspectSource = function(e) {
    return Te(e)
  });
  var ke, De, Oe, Ae = l.inspectSource,
    _e = o.WeakMap,
    Me = D(_e) && /native code/.test(Ae(_e)),
    Le = c("keys"),
    Ie = function(e) {
      return Le[e] || (Le[e] = k(e))
    },
    Pe = {},
    je = o.TypeError,
    Ne = o.WeakMap;
  if (Me || l.state) {
    var ze = l.state || (l.state = new Ne),
      Re = g(ze.get),
      $e = g(ze.has),
      He = g(ze.set);
    ke = function(e, t) {
      if ($e(ze, e)) throw new je("Object already initialized");
      return t.facade = e, He(ze, e, t), t
    }, De = function(e) {
      return Re(ze, e) || {}
    }, Oe = function(e) {
      return $e(ze, e)
    }
  } else {
    var Fe = Ie("state");
    Pe[Fe] = !0, ke = function(e, t) {
      if (S(e, Fe)) throw new je("Object already initialized");
      return t.facade = e, we(e, Fe, t), t
    }, De = function(e) {
      return S(e, Fe) ? e[Fe] : {}
    }, Oe = function(e) {
      return S(e, Fe)
    }
  }
  var Be = {
      set: ke,
      get: De,
      has: Oe,
      enforce: function(e) {
        return Oe(e) ? De(e) : ke(e, {})
      },
      getterFor: function(e) {
        return function(t) {
          var n;
          if (!U(t) || (n = De(t)).type !== e) throw je("Incompatible receiver, " + e + " required");
          return n
        }
      }
    },
    qe = t((function(e) {
      var t = Ee.CONFIGURABLE,
        n = Be.enforce,
        r = Be.get,
        i = Object.defineProperty,
        o = Y && !u((function() {
          return 8 !== i((function() {}), "length", {
            value: 8
          }).length
        })),
        a = String(String).split("String"),
        s = e.exports = function(e, r, s) {
          if ("Symbol(" === String(r).slice(0, 7) && (r = "[" + String(r).replace(/^Symbol\(([^)]*)\)/, "$1") + "]"), s && s.getter && (r = "get " + r), s && s.setter && (r = "set " + r), (!S(e, "name") || t && e.name !== r) && i(e, "name", {
              value: r,
              configurable: !0
            }), o && s && S(s, "arity") && e.length !== s.arity && i(e, "length", {
              value: s.arity
            }), s && S(s, "constructor") && s.constructor) {
            if (Y) try {
              i(e, "prototype", {
                writable: !1
              })
            } catch (e) {}
          } else e.prototype = void 0;
          var l = n(e);
          return S(l, "source") || (l.source = a.join("string" == typeof r ? r : "")), e
        };
      Function.prototype.toString = s((function() {
        return D(this) && r(this).source || Ae(this)
      }), "toString")
    })),
    We = function(e, t, n, r) {
      r || (r = {});
      var i = r.enumerable,
        o = void 0 !== r.name ? r.name : t;
      return D(n) && qe(n, o, r), r.global ? i ? e[t] = n : s(t, n) : (r.unsafe ? e[t] && (i = !0) : delete e[t], i ? e[t] = n : we(e, t, n)), e
    },
    Ye = g({}.toString),
    Ue = g("".slice),
    Ve = function(e) {
      return Ue(Ye(e), 8, -1)
    },
    Xe = B("toStringTag"),
    Ge = o.Object,
    Ze = "Arguments" == Ve(function() {
      return arguments
    }()),
    Ke = W ? Ve : function(e) {
      var t, n, r;
      return void 0 === e ? "Undefined" : null === e ? "Null" : "string" == typeof(n = function(e, t) {
        try {
          return e[t]
        } catch (e) {}
      }(t = Ge(e), Xe)) ? n : Ze ? Ve(t) : "Object" == (r = Ve(t)) && D(t.callee) ? "Arguments" : r
    },
    Je = W ? {}.toString : function() {
      return "[object " + Ke(this) + "]"
    };
  W || We(Object.prototype, "toString", Je, {
    unsafe: !0
  });
  var Qe = {
      CSSRuleList: 0,
      CSSStyleDeclaration: 0,
      CSSValueList: 0,
      ClientRectList: 0,
      DOMRectList: 0,
      DOMStringList: 0,
      DOMTokenList: 1,
      DataTransferItemList: 0,
      FileList: 0,
      HTMLAllCollection: 0,
      HTMLCollection: 0,
      HTMLFormElement: 0,
      HTMLSelectElement: 0,
      MediaList: 0,
      MimeTypeArray: 0,
      NamedNodeMap: 0,
      NodeList: 1,
      PaintRequestList: 0,
      Plugin: 0,
      PluginArray: 0,
      SVGLengthList: 0,
      SVGNumberList: 0,
      SVGPathSegList: 0,
      SVGPointList: 0,
      SVGStringList: 0,
      SVGTransformList: 0,
      SourceBufferList: 0,
      StyleSheetList: 0,
      TextTrackCueList: 0,
      TextTrackList: 0,
      TouchList: 0
    },
    et = G("span").classList,
    tt = et && et.constructor && et.constructor.prototype,
    nt = tt === Object.prototype ? void 0 : tt,
    rt = g(g.bind),
    it = function(e, t) {
      return ce(e), void 0 === t ? e : d ? rt(e, t) : function() {
        return e.apply(t, arguments)
      }
    },
    ot = o.Object,
    at = g("".split),
    st = u((function() {
      return !ot("z").propertyIsEnumerable(0)
    })) ? function(e) {
      return "String" == Ve(e) ? at(e, "") : ot(e)
    } : ot,
    lt = Math.ceil,
    ct = Math.floor,
    ut = Math.trunc || function(e) {
      var t = +e;
      return (t > 0 ? ct : lt)(t)
    },
    dt = function(e) {
      var t = +e;
      return t != t || 0 === t ? 0 : ut(t)
    },
    pt = Math.min,
    ft = function(e) {
      return e > 0 ? pt(dt(e), 9007199254740991) : 0
    },
    ht = function(e) {
      return ft(e.length)
    },
    mt = Array.isArray || function(e) {
      return "Array" == Ve(e)
    },
    gt = function() {},
    vt = [],
    yt = A("Reflect", "construct"),
    bt = /^\s*(?:class|function)\b/,
    wt = g(bt.exec),
    xt = !bt.exec(gt),
    St = function(e) {
      if (!D(e)) return !1;
      try {
        return yt(gt, vt, e), !0
      } catch (e) {
        return !1
      }
    },
    Ct = function(e) {
      if (!D(e)) return !1;
      switch (Ke(e)) {
        case "AsyncFunction":
        case "GeneratorFunction":
        case "AsyncGeneratorFunction":
          return !1
      }
      try {
        return xt || !!wt(bt, Ae(e))
      } catch (e) {
        return !0
      }
    };
  Ct.sham = !0;
  var Et = !yt || u((function() {
      var e;
      return St(St.call) || !St(Object) || !St((function() {
        e = !0
      })) || e
    })) ? Ct : St,
    Tt = B("species"),
    kt = o.Array,
    Dt = function(e, t) {
      return new(function(e) {
        var t;
        return mt(e) && (t = e.constructor, (Et(t) && (t === kt || mt(t.prototype)) || U(t) && null === (t = t[Tt])) && (t = void 0)), void 0 === t ? kt : t
      }(e))(0 === t ? 0 : t)
    },
    Ot = g([].push),
    At = function(e) {
      var t = 1 == e,
        n = 2 == e,
        r = 3 == e,
        i = 4 == e,
        o = 6 == e,
        a = 7 == e,
        s = 5 == e || o;
      return function(l, c, u, d) {
        for (var p, f, h = w(l), m = st(h), g = it(c, u), v = ht(m), y = 0, b = d || Dt, x = t ? b(l, v) : n || a ? b(l, 0) : void 0; v > y; y++)
          if ((s || y in m) && (f = g(p = m[y], y, h), e))
            if (t) x[y] = f;
            else if (f) switch (e) {
          case 3:
            return !0;
          case 5:
            return p;
          case 6:
            return y;
          case 2:
            Ot(x, p)
        } else switch (e) {
          case 4:
            return !1;
          case 7:
            Ot(x, p)
        }
        return o ? -1 : r || i ? i : x
      }
    },
    _t = {
      forEach: At(0),
      map: At(1),
      filter: At(2),
      some: At(3),
      every: At(4),
      find: At(5),
      findIndex: At(6),
      filterReject: At(7)
    },
    Mt = function(e, t) {
      var n = [][e];
      return !!n && u((function() {
        n.call(null, t || function() {
          return 1
        }, 1)
      }))
    },
    Lt = _t.forEach,
    It = Mt("forEach") ? [].forEach : function(e) {
      return Lt(this, e, arguments.length > 1 ? arguments[1] : void 0)
    },
    Pt = function(e) {
      if (e && e.forEach !== It) try {
        we(e, "forEach", It)
      } catch (t) {
        e.forEach = It
      }
    };
  for (var jt in Qe) Qe[jt] && Pt(o[jt] && o[jt].prototype);
  Pt(nt);
  var Nt = !("undefined" == typeof window || !window.document || !window.document.createElement),
    zt = {}.propertyIsEnumerable,
    Rt = Object.getOwnPropertyDescriptor,
    $t = {
      f: Rt && !zt.call({
        1: 2
      }, 1) ? function(e) {
        var t = Rt(this, e);
        return !!t && t.enumerable
      } : zt
    },
    Ht = function(e) {
      return st(y(e))
    },
    Ft = Object.getOwnPropertyDescriptor,
    Bt = {
      f: Y ? Ft : function(e, t) {
        if (e = Ht(e), t = he(t), Z) try {
          return Ft(e, t)
        } catch (e) {}
        if (S(e, t)) return be(!ne($t.f, e, t), e[t])
      }
    },
    qt = Math.max,
    Wt = Math.min,
    Yt = function(e, t) {
      var n = dt(e);
      return n < 0 ? qt(n + t, 0) : Wt(n, t)
    },
    Ut = function(e) {
      return function(t, n, r) {
        var i, o = Ht(t),
          a = ht(o),
          s = Yt(r, a);
        if (e && n != n) {
          for (; a > s;)
            if ((i = o[s++]) != i) return !0
        } else
          for (; a > s; s++)
            if ((e || s in o) && o[s] === n) return e || s || 0;
        return !e && -1
      }
    },
    Vt = (Ut(!0), Ut(!1)),
    Xt = g([].push),
    Gt = function(e, t) {
      var n, r = Ht(e),
        i = 0,
        o = [];
      for (n in r) !S(Pe, n) && S(r, n) && Xt(o, n);
      for (; t.length > i;) S(r, n = t[i++]) && (~Vt(o, n) || Xt(o, n));
      return o
    },
    Zt = ["constructor", "hasOwnProperty", "isPrototypeOf", "propertyIsEnumerable", "toLocaleString", "toString", "valueOf"],
    Kt = Zt.concat("length", "prototype"),
    Jt = {
      f: Object.getOwnPropertyNames || function(e) {
        return Gt(e, Kt)
      }
    },
    Qt = {
      f: Object.getOwnPropertySymbols
    },
    en = g([].concat),
    tn = A("Reflect", "ownKeys") || function(e) {
      var t = Jt.f(ee(e)),
        n = Qt.f;
      return n ? en(t, n(e)) : t
    },
    nn = function(e, t, n) {
      for (var r = tn(t), i = ye.f, o = Bt.f, a = 0; a < r.length; a++) {
        var s = r[a];
        S(e, s) || n && S(n, s) || i(e, s, o(t, s))
      }
    },
    rn = /#|\.prototype\./,
    on = function(e, t) {
      var n = sn[an(e)];
      return n == cn || n != ln && (D(t) ? u(t) : !!t)
    },
    an = on.normalize = function(e) {
      return String(e).replace(rn, ".").toLowerCase()
    },
    sn = on.data = {},
    ln = on.NATIVE = "N",
    cn = on.POLYFILL = "P",
    un = on,
    dn = Bt.f,
    pn = function(e, t) {
      var n, r, i, a, l, c = e.target,
        u = e.global,
        d = e.stat;
      if (n = u ? o : d ? o[c] || s(c, {}) : (o[c] || {}).prototype)
        for (r in t) {
          if (a = t[r], i = e.dontCallGetSet ? (l = dn(n, r)) && l.value : n[r], !un(u ? r : c + (d ? "." : "#") + r, e.forced) && void 0 !== i) {
            if (typeof a == typeof i) continue;
            nn(a, i)
          }(e.sham || i && i.sham) && we(a, "sham", !0), We(n, r, a, e)
        }
    },
    fn = o.String,
    hn = function(e) {
      if ("Symbol" === Ke(e)) throw TypeError("Cannot convert a Symbol value to a string");
      return fn(e)
    },
    mn = "\t\n\v\f\r                　\u2028\u2029\ufeff",
    gn = g("".replace),
    vn = "[" + mn + "]",
    yn = RegExp("^" + vn + vn + "*"),
    bn = RegExp(vn + vn + "*$"),
    wn = function(e) {
      return function(t) {
        var n = hn(y(t));
        return 1 & e && (n = gn(n, yn, "")), 2 & e && (n = gn(n, bn, "")), n
      }
    },
    xn = (wn(1), wn(2), wn(3)),
    Sn = o.parseInt,
    Cn = o.Symbol,
    En = Cn && Cn.iterator,
    Tn = /^[+-]?0x/i,
    kn = g(Tn.exec),
    Dn = 8 !== Sn(mn + "08") || 22 !== Sn(mn + "0x16") || En && !u((function() {
      Sn(Object(En))
    })) ? function(e, t) {
      var n = xn(hn(e));
      return Sn(n, t >>> 0 || (kn(Tn, n) ? 16 : 10))
    } : Sn;
  pn({
    global: !0,
    forced: parseInt != Dn
  }, {
    parseInt: Dn
  });
  var On = Object.keys || function(e) {
      return Gt(e, Zt)
    },
    An = Object.assign,
    _n = Object.defineProperty,
    Mn = g([].concat),
    Ln = !An || u((function() {
      if (Y && 1 !== An({
          b: 1
        }, An(_n({}, "a", {
          enumerable: !0,
          get: function() {
            _n(this, "b", {
              value: 3,
              enumerable: !1
            })
          }
        }), {
          b: 2
        })).b) return !0;
      var e = {},
        t = {},
        n = Symbol();
      return e[n] = 7, "abcdefghijklmnopqrst".split("").forEach((function(e) {
        t[e] = e
      })), 7 != An({}, e)[n] || "abcdefghijklmnopqrst" != On(An({}, t)).join("")
    })) ? function(e, t) {
      for (var n = w(e), r = arguments.length, i = 1, o = Qt.f, a = $t.f; r > i;)
        for (var s, l = st(arguments[i++]), c = o ? Mn(On(l), o(l)) : On(l), u = c.length, d = 0; u > d;) s = c[d++], Y && !ne(a, l, s) || (n[s] = l[s]);
      return n
    } : An;
  pn({
    target: "Object",
    stat: !0,
    arity: 2,
    forced: Object.assign !== Ln
  }, {
    assign: Ln
  });
  var In = B("species"),
    Pn = _t.filter,
    jn = ("filter", j >= 51 || !u((function() {
      var e = [];
      return (e.constructor = {})[In] = function() {
        return {
          foo: 1
        }
      }, 1 !== e.filter(Boolean).foo
    })));
  pn({
    target: "Array",
    proto: !0,
    forced: !jn
  }, {
    filter: function(e) {
      return Pn(this, e, arguments.length > 1 ? arguments[1] : void 0)
    }
  });
  var Nn, zn = {
      f: Y && !K ? Object.defineProperties : function(e, t) {
        ee(e);
        for (var n, r = Ht(t), i = On(t), o = i.length, a = 0; o > a;) ye.f(e, n = i[a++], r[n]);
        return e
      }
    },
    Rn = A("document", "documentElement"),
    $n = Ie("IE_PROTO"),
    Hn = function() {},
    Fn = function(e) {
      return "<script>" + e + "<\/script>"
    },
    Bn = function(e) {
      e.write(Fn("")), e.close();
      var t = e.parentWindow.Object;
      return e = null, t
    },
    qn = function() {
      try {
        Nn = new ActiveXObject("htmlfile")
      } catch (e) {}
      var e, t;
      qn = "undefined" != typeof document ? document.domain && Nn ? Bn(Nn) : ((t = G("iframe")).style.display = "none", Rn.appendChild(t), t.src = String("javascript:"), (e = t.contentWindow.document).open(), e.write(Fn("document.F=Object")), e.close(), e.F) : Bn(Nn);
      for (var n = Zt.length; n--;) delete qn.prototype[Zt[n]];
      return qn()
    };
  Pe[$n] = !0;
  var Wn = Object.create || function(e, t) {
      var n;
      return null !== e ? (Hn.prototype = ee(e), n = new Hn, Hn.prototype = null, n[$n] = e) : n = qn(), void 0 === t ? n : zn.f(n, t)
    },
    Yn = ye.f,
    Un = B("unscopables"),
    Vn = Array.prototype;
  null == Vn[Un] && Yn(Vn, Un, {
    configurable: !0,
    value: Wn(null)
  });
  var Xn, Gn, Zn, Kn = function(e) {
      Vn[Un][e] = !0
    },
    Jn = {},
    Qn = !u((function() {
      function e() {}
      return e.prototype.constructor = null, Object.getPrototypeOf(new e) !== e.prototype
    })),
    er = Ie("IE_PROTO"),
    tr = o.Object,
    nr = tr.prototype,
    rr = Qn ? tr.getPrototypeOf : function(e) {
      var t = w(e);
      if (S(t, er)) return t[er];
      var n = t.constructor;
      return D(n) && t instanceof n ? n.prototype : t instanceof tr ? nr : null
    },
    ir = B("iterator"),
    or = !1;
  [].keys && ("next" in (Zn = [].keys()) ? (Gn = rr(rr(Zn))) !== Object.prototype && (Xn = Gn) : or = !0), (null == Xn || u((function() {
    var e = {};
    return Xn[ir].call(e) !== e
  }))) && (Xn = {}), D(Xn[ir]) || We(Xn, ir, (function() {
    return this
  }));
  var ar = {
      IteratorPrototype: Xn,
      BUGGY_SAFARI_ITERATORS: or
    },
    sr = ye.f,
    lr = B("toStringTag"),
    cr = function(e, t, n) {
      e && !n && (e = e.prototype), e && !S(e, lr) && sr(e, lr, {
        configurable: !0,
        value: t
      })
    },
    ur = ar.IteratorPrototype,
    dr = function() {
      return this
    },
    pr = o.String,
    fr = o.TypeError,
    hr = Object.setPrototypeOf || ("__proto__" in {} ? function() {
      var e, t = !1,
        n = {};
      try {
        (e = g(Object.getOwnPropertyDescriptor(Object.prototype, "__proto__").set))(n, []), t = n instanceof Array
      } catch (e) {}
      return function(n, r) {
        return ee(n),
          function(e) {
            if ("object" == typeof e || D(e)) return e;
            throw fr("Can't set " + pr(e) + " as a prototype")
          }(r), t ? e(n, r) : n.__proto__ = r, n
      }
    }() : void 0),
    mr = Ee.PROPER,
    gr = Ee.CONFIGURABLE,
    vr = ar.IteratorPrototype,
    yr = ar.BUGGY_SAFARI_ITERATORS,
    br = B("iterator"),
    wr = function() {
      return this
    },
    xr = function(e, t, n, r, i, o, a) {
      ! function(e, t, n, r) {
        var i = t + " Iterator";
        e.prototype = Wn(ur, {
          next: be(1, n)
        }), cr(e, i, !1), Jn[i] = dr
      }(n, t, r);
      var s, l, c, u = function(e) {
          if (e === i && m) return m;
          if (!yr && e in f) return f[e];
          switch (e) {
            case "keys":
            case "values":
            case "entries":
              return function() {
                return new n(this, e)
              }
          }
          return function() {
            return new n(this)
          }
        },
        d = t + " Iterator",
        p = !1,
        f = e.prototype,
        h = f[br] || f["@@iterator"] || i && f[i],
        m = !yr && h || u(i),
        g = "Array" == t && f.entries || h;
      if (g && (s = rr(g.call(new e))) !== Object.prototype && s.next && (rr(s) !== vr && (hr ? hr(s, vr) : D(s[br]) || We(s, br, wr)), cr(s, d, !0)), mr && "values" == i && h && "values" !== h.name && (gr ? we(f, "name", "values") : (p = !0, m = function() {
          return ne(h, this)
        })), i)
        if (l = {
            values: u("values"),
            keys: o ? m : u("keys"),
            entries: u("entries")
          }, a)
          for (c in l)(yr || p || !(c in f)) && We(f, c, l[c]);
        else pn({
          target: t,
          proto: !0,
          forced: yr || p
        }, l);
      return f[br] !== m && We(f, br, m, {
        name: i
      }), Jn[t] = m, l
    },
    Sr = ye.f,
    Cr = Be.set,
    Er = Be.getterFor("Array Iterator"),
    Tr = xr(Array, "Array", (function(e, t) {
      Cr(this, {
        type: "Array Iterator",
        target: Ht(e),
        index: 0,
        kind: t
      })
    }), (function() {
      var e = Er(this),
        t = e.target,
        n = e.kind,
        r = e.index++;
      return !t || r >= t.length ? (e.target = void 0, {
        value: void 0,
        done: !0
      }) : "keys" == n ? {
        value: r,
        done: !1
      } : "values" == n ? {
        value: t[r],
        done: !1
      } : {
        value: [r, t[r]],
        done: !1
      }
    }), "values"),
    kr = Jn.Arguments = Jn.Array;
  if (Kn("keys"), Kn("values"), Kn("entries"), Y && "values" !== kr.name) try {
    Sr(kr, "name", {
      value: "values"
    })
  } catch (e) {}
  var Dr = g("".charAt),
    Or = g("".charCodeAt),
    Ar = g("".slice),
    _r = function(e) {
      return function(t, n) {
        var r, i, o = hn(y(t)),
          a = dt(n),
          s = o.length;
        return a < 0 || a >= s ? e ? "" : void 0 : (r = Or(o, a)) < 55296 || r > 56319 || a + 1 === s || (i = Or(o, a + 1)) < 56320 || i > 57343 ? e ? Dr(o, a) : r : e ? Ar(o, a, a + 2) : i - 56320 + (r - 55296 << 10) + 65536
      }
    },
    Mr = {
      codeAt: _r(!1),
      charAt: _r(!0)
    },
    Lr = Mr.charAt,
    Ir = Be.set,
    Pr = Be.getterFor("String Iterator");
  xr(String, "String", (function(e) {
    Ir(this, {
      type: "String Iterator",
      string: hn(e),
      index: 0
    })
  }), (function() {
    var e, t = Pr(this),
      n = t.string,
      r = t.index;
    return r >= n.length ? {
      value: void 0,
      done: !0
    } : (e = Lr(n, r), t.index += e.length, {
      value: e,
      done: !1
    })
  }));
  var jr = function(e, t, n) {
      for (var r in t) We(e, r, t[r], n);
      return e
    },
    Nr = o.Array,
    zr = Math.max,
    Rr = Jt.f,
    $r = "object" == typeof window && window && Object.getOwnPropertyNames ? Object.getOwnPropertyNames(window) : [],
    Hr = {
      f: function(e) {
        return $r && "Window" == Ve(e) ? function(e) {
          try {
            return Rr(e)
          } catch (e) {
            return function(e, t, n) {
              for (var r, i, o, a, s = ht(e), l = Yt(void 0, s), c = Yt(s, s), u = Nr(zr(c - l, 0)), d = 0; l < c; l++, d++) r = u, i = d, o = e[l], (a = he(i)) in r ? ye.f(r, a, be(0, o)) : r[a] = o;
              return u.length = d, u
            }($r)
          }
        }(e) : Rr(Ht(e))
      }
    },
    Fr = u((function() {
      if ("function" == typeof ArrayBuffer) {
        var e = new ArrayBuffer(8);
        Object.isExtensible(e) && Object.defineProperty(e, "a", {
          value: 8
        })
      }
    })),
    Br = Object.isExtensible,
    qr = u((function() {
      Br(1)
    })) || Fr ? function(e) {
      return !!U(e) && (!Fr || "ArrayBuffer" != Ve(e)) && (!Br || Br(e))
    } : Br,
    Wr = !u((function() {
      return Object.isExtensible(Object.preventExtensions({}))
    })),
    Yr = t((function(e) {
      var t = ye.f,
        n = !1,
        r = k("meta"),
        i = 0,
        o = function(e) {
          t(e, r, {
            value: {
              objectID: "O" + i++,
              weakData: {}
            }
          })
        },
        a = e.exports = {
          enable: function() {
            a.enable = function() {}, n = !0;
            var e = Jt.f,
              t = g([].splice),
              i = {};
            i[r] = 1, e(i).length && (Jt.f = function(n) {
              for (var i = e(n), o = 0, a = i.length; o < a; o++)
                if (i[o] === r) {
                  t(i, o, 1);
                  break
                } return i
            }, pn({
              target: "Object",
              stat: !0,
              forced: !0
            }, {
              getOwnPropertyNames: Hr.f
            }))
          },
          fastKey: function(e, t) {
            if (!U(e)) return "symbol" == typeof e ? e : ("string" == typeof e ? "S" : "P") + e;
            if (!S(e, r)) {
              if (!qr(e)) return "F";
              if (!t) return "E";
              o(e)
            }
            return e[r].objectID
          },
          getWeakData: function(e, t) {
            if (!S(e, r)) {
              if (!qr(e)) return !0;
              if (!t) return !1;
              o(e)
            }
            return e[r].weakData
          },
          onFreeze: function(e) {
            return Wr && n && qr(e) && !S(e, r) && o(e), e
          }
        };
      Pe[r] = !0
    })),
    Ur = (Yr.enable, Yr.fastKey, Yr.getWeakData, Yr.onFreeze, B("iterator")),
    Vr = Array.prototype,
    Xr = B("iterator"),
    Gr = function(e) {
      if (null != e) return ue(e, Xr) || ue(e, "@@iterator") || Jn[Ke(e)]
    },
    Zr = o.TypeError,
    Kr = function(e, t, n) {
      var r, i;
      ee(e);
      try {
        if (!(r = ue(e, "return"))) {
          if ("throw" === t) throw n;
          return n
        }
        r = ne(r, e)
      } catch (e) {
        i = !0, r = e
      }
      if ("throw" === t) throw n;
      if (i) throw r;
      return ee(r), n
    },
    Jr = o.TypeError,
    Qr = function(e, t) {
      this.stopped = e, this.result = t
    },
    ei = Qr.prototype,
    ti = function(e, t, n) {
      var r, i, o, a, s, l, c, u, d = n && n.that,
        p = !(!n || !n.AS_ENTRIES),
        f = !(!n || !n.IS_ITERATOR),
        h = !(!n || !n.INTERRUPTED),
        m = it(t, d),
        g = function(e) {
          return r && Kr(r, "normal", e), new Qr(!0, e)
        },
        v = function(e) {
          return p ? (ee(e), h ? m(e[0], e[1], g) : m(e[0], e[1])) : h ? m(e, g) : m(e)
        };
      if (f) r = e;
      else {
        if (!(i = Gr(e))) throw Jr(se(e) + " is not iterable");
        if (void 0 !== (u = i) && (Jn.Array === u || Vr[Ur] === u)) {
          for (o = 0, a = ht(e); a > o; o++)
            if ((s = v(e[o])) && re(ei, s)) return s;
          return new Qr(!1)
        }
        r = function(e, t) {
          var n = arguments.length < 2 ? Gr(e) : t;
          if (ce(n)) return ee(ne(n, e));
          throw Zr(se(e) + " is not iterable")
        }(e, i)
      }
      for (l = r.next; !(c = ne(l, r)).done;) {
        try {
          s = v(c.value)
        } catch (e) {
          Kr(r, "throw", e)
        }
        if ("object" == typeof s && s && re(ei, s)) return s
      }
      return new Qr(!1)
    },
    ni = o.TypeError,
    ri = function(e, t) {
      if (re(t, e)) return e;
      throw ni("Incorrect invocation")
    },
    ii = B("iterator"),
    oi = !1;
  try {
    var ai = 0,
      si = {
        next: function() {
          return {
            done: !!ai++
          }
        },
        return: function() {
          oi = !0
        }
      };
    si[ii] = function() {
      return this
    }, Array.from(si, (function() {
      throw 2
    }))
  } catch (e) {}
  var li = Yr.getWeakData,
    ci = Be.set,
    ui = Be.getterFor,
    di = _t.find,
    pi = _t.findIndex,
    fi = g([].splice),
    hi = 0,
    mi = function(e) {
      return e.frozen || (e.frozen = new gi)
    },
    gi = function() {
      this.entries = []
    },
    vi = function(e, t) {
      return di(e.entries, (function(e) {
        return e[0] === t
      }))
    };
  gi.prototype = {
    get: function(e) {
      var t = vi(this, e);
      if (t) return t[1]
    },
    has: function(e) {
      return !!vi(this, e)
    },
    set: function(e, t) {
      var n = vi(this, e);
      n ? n[1] = t : this.entries.push([e, t])
    },
    delete: function(e) {
      var t = pi(this.entries, (function(t) {
        return t[0] === e
      }));
      return ~t && fi(this.entries, t, 1), !!~t
    }
  };
  var yi, bi = {
      getConstructor: function(e, t, n, r) {
        var i = e((function(e, i) {
            ri(e, o), ci(e, {
              type: t,
              id: hi++,
              frozen: void 0
            }), null != i && ti(i, e[r], {
              that: e,
              AS_ENTRIES: n
            })
          })),
          o = i.prototype,
          a = ui(t),
          s = function(e, t, n) {
            var r = a(e),
              i = li(ee(t), !0);
            return !0 === i ? mi(r).set(t, n) : i[r.id] = n, e
          };
        return jr(o, {
          delete: function(e) {
            var t = a(this);
            if (!U(e)) return !1;
            var n = li(e);
            return !0 === n ? mi(t).delete(e) : n && S(n, t.id) && delete n[t.id]
          },
          has: function(e) {
            var t = a(this);
            if (!U(e)) return !1;
            var n = li(e);
            return !0 === n ? mi(t).has(e) : n && S(n, t.id)
          }
        }), jr(o, n ? {
          get: function(e) {
            var t = a(this);
            if (U(e)) {
              var n = li(e);
              return !0 === n ? mi(t).get(e) : n ? n[t.id] : void 0
            }
          },
          set: function(e, t) {
            return s(this, e, t)
          }
        } : {
          add: function(e) {
            return s(this, e, !0)
          }
        }), i
      }
    },
    wi = Be.enforce,
    xi = !o.ActiveXObject && "ActiveXObject" in o,
    Si = function(e) {
      return function() {
        return e(this, arguments.length ? arguments[0] : void 0)
      }
    },
    Ci = function(e, t, n) {
      var r = -1 !== e.indexOf("Map"),
        i = -1 !== e.indexOf("Weak"),
        a = r ? "set" : "add",
        s = o[e],
        l = s && s.prototype,
        c = s,
        d = {},
        p = function(e) {
          var t = g(l[e]);
          We(l, e, "add" == e ? function(e) {
            return t(this, 0 === e ? 0 : e), this
          } : "delete" == e ? function(e) {
            return !(i && !U(e)) && t(this, 0 === e ? 0 : e)
          } : "get" == e ? function(e) {
            return i && !U(e) ? void 0 : t(this, 0 === e ? 0 : e)
          } : "has" == e ? function(e) {
            return !(i && !U(e)) && t(this, 0 === e ? 0 : e)
          } : function(e, n) {
            return t(this, 0 === e ? 0 : e, n), this
          })
        };
      if (un(e, !D(s) || !(i || l.forEach && !u((function() {
          (new s).entries().next()
        }))))) c = n.getConstructor(t, e, r, a), Yr.enable();
      else if (un(e, !0)) {
        var f = new c,
          h = f[a](i ? {} : -0, 1) != f,
          m = u((function() {
            f.has(1)
          })),
          v = function(e, t) {
            if (!oi) return !1;
            var n = !1;
            try {
              var r = {};
              r[ii] = function() {
                  return {
                    next: function() {
                      return {
                        done: n = !0
                      }
                    }
                  }
                },
                function(e) {
                  new s(e)
                }(r)
            } catch (e) {}
            return n
          }(),
          y = !i && u((function() {
            for (var e = new s, t = 5; t--;) e[a](t, t);
            return !e.has(-0)
          }));
        v || ((c = t((function(e, t) {
          ri(e, l);
          var n = function(e, t, n) {
            var r, i;
            return hr && D(r = t.constructor) && r !== n && U(i = r.prototype) && i !== n.prototype && hr(e, i), e
          }(new s, e, c);
          return null != t && ti(t, n[a], {
            that: n,
            AS_ENTRIES: r
          }), n
        }))).prototype = l, l.constructor = c), (m || y) && (p("delete"), p("has"), r && p("get")), (y || h) && p(a), i && l.clear && delete l.clear
      }
      return d[e] = c, pn({
        global: !0,
        constructor: !0,
        forced: c != s
      }, d), cr(c, e), i || n.setStrong(c, e, r), c
    }("WeakMap", Si, bi);
  if (Me && xi) {
    yi = bi.getConstructor(Si, "WeakMap", !0), Yr.enable();
    var Ei = Ci.prototype,
      Ti = g(Ei.delete),
      ki = g(Ei.has),
      Di = g(Ei.get),
      Oi = g(Ei.set);
    jr(Ei, {
      delete: function(e) {
        if (U(e) && !qr(e)) {
          var t = wi(this);
          return t.frozen || (t.frozen = new yi), Ti(this, e) || t.frozen.delete(e)
        }
        return Ti(this, e)
      },
      has: function(e) {
        if (U(e) && !qr(e)) {
          var t = wi(this);
          return t.frozen || (t.frozen = new yi), ki(this, e) || t.frozen.has(e)
        }
        return ki(this, e)
      },
      get: function(e) {
        if (U(e) && !qr(e)) {
          var t = wi(this);
          return t.frozen || (t.frozen = new yi), ki(this, e) ? Di(this, e) : t.frozen.get(e)
        }
        return Di(this, e)
      },
      set: function(e, t) {
        if (U(e) && !qr(e)) {
          var n = wi(this);
          n.frozen || (n.frozen = new yi), ki(this, e) ? Oi(this, e, t) : n.frozen.set(e, t)
        } else Oi(this, e, t);
        return this
      }
    })
  }
  var Ai = B("iterator"),
    _i = B("toStringTag"),
    Mi = Tr.values,
    Li = function(e, t) {
      if (e) {
        if (e[Ai] !== Mi) try {
          we(e, Ai, Mi)
        } catch (t) {
          e[Ai] = Mi
        }
        if (e[_i] || we(e, _i, t), Qe[t])
          for (var n in Tr)
            if (e[n] !== Tr[n]) try {
              we(e, n, Tr[n])
            } catch (t) {
              e[n] = Tr[n]
            }
      }
    };
  for (var Ii in Qe) Li(o[Ii] && o[Ii].prototype, Ii);
  Li(nt, "DOMTokenList");
  var Pi = /^\s+|\s+$/g,
    ji = /^[-+]0x[0-9a-f]+$/i,
    Ni = /^0b[01]+$/i,
    zi = /^0o[0-7]+$/i,
    Ri = parseInt,
    $i = "object" == typeof e && e && e.Object === Object && e,
    Hi = "object" == typeof self && self && self.Object === Object && self,
    Fi = $i || Hi || Function("return this")(),
    Bi = Object.prototype.toString,
    qi = Math.max,
    Wi = Math.min,
    Yi = function() {
      return Fi.Date.now()
    };

  function Ui(e) {
    var t = typeof e;
    return !!e && ("object" == t || "function" == t)
  }

  function Vi(e) {
    if ("number" == typeof e) return e;
    if (function(e) {
        return "symbol" == typeof e || function(e) {
          return !!e && "object" == typeof e
        }(e) && "[object Symbol]" == Bi.call(e)
      }(e)) return NaN;
    if (Ui(e)) {
      var t = "function" == typeof e.valueOf ? e.valueOf() : e;
      e = Ui(t) ? t + "" : t
    }
    if ("string" != typeof e) return 0 === e ? e : +e;
    e = e.replace(Pi, "");
    var n = Ni.test(e);
    return n || zi.test(e) ? Ri(e.slice(2), n ? 2 : 8) : ji.test(e) ? NaN : +e
  }
  var Xi = function(e, t, n) {
      var r = !0,
        i = !0;
      if ("function" != typeof e) throw new TypeError("Expected a function");
      return Ui(n) && (r = "leading" in n ? !!n.leading : r, i = "trailing" in n ? !!n.trailing : i),
        function(e, t, n) {
          var r, i, o, a, s, l, c = 0,
            u = !1,
            d = !1,
            p = !0;
          if ("function" != typeof e) throw new TypeError("Expected a function");

          function f(t) {
            var n = r,
              o = i;
            return r = i = void 0, c = t, a = e.apply(o, n)
          }

          function h(e) {
            return c = e, s = setTimeout(g, t), u ? f(e) : a
          }

          function m(e) {
            var n = e - l;
            return void 0 === l || n >= t || n < 0 || d && e - c >= o
          }

          function g() {
            var e = Yi();
            if (m(e)) return v(e);
            s = setTimeout(g, function(e) {
              var n = t - (e - l);
              return d ? Wi(n, o - (e - c)) : n
            }(e))
          }

          function v(e) {
            return s = void 0, p && r ? f(e) : (r = i = void 0, a)
          }

          function y() {
            var e = Yi(),
              n = m(e);
            if (r = arguments, i = this, l = e, n) {
              if (void 0 === s) return h(l);
              if (d) return s = setTimeout(g, t), f(l)
            }
            return void 0 === s && (s = setTimeout(g, t)), a
          }
          return t = Vi(t) || 0, Ui(n) && (u = !!n.leading, o = (d = "maxWait" in n) ? qi(Vi(n.maxWait) || 0, t) : o, p = "trailing" in n ? !!n.trailing : p), y.cancel = function() {
            void 0 !== s && clearTimeout(s), c = 0, r = l = i = s = void 0
          }, y.flush = function() {
            return void 0 === s ? a : v(Yi())
          }, y
        }(e, t, {
          leading: r,
          maxWait: t,
          trailing: i
        })
    },
    Gi = /^\s+|\s+$/g,
    Zi = /^[-+]0x[0-9a-f]+$/i,
    Ki = /^0b[01]+$/i,
    Ji = /^0o[0-7]+$/i,
    Qi = parseInt,
    eo = "object" == typeof e && e && e.Object === Object && e,
    to = "object" == typeof self && self && self.Object === Object && self,
    no = eo || to || Function("return this")(),
    ro = Object.prototype.toString,
    io = Math.max,
    oo = Math.min,
    ao = function() {
      return no.Date.now()
    };

  function so(e) {
    var t = typeof e;
    return !!e && ("object" == t || "function" == t)
  }

  function lo(e) {
    if ("number" == typeof e) return e;
    if (function(e) {
        return "symbol" == typeof e || function(e) {
          return !!e && "object" == typeof e
        }(e) && "[object Symbol]" == ro.call(e)
      }(e)) return NaN;
    if (so(e)) {
      var t = "function" == typeof e.valueOf ? e.valueOf() : e;
      e = so(t) ? t + "" : t
    }
    if ("string" != typeof e) return 0 === e ? e : +e;
    e = e.replace(Gi, "");
    var n = Ki.test(e);
    return n || Ji.test(e) ? Qi(e.slice(2), n ? 2 : 8) : Zi.test(e) ? NaN : +e
  }
  var co = function(e, t, n) {
      var r, i, o, a, s, l, c = 0,
        u = !1,
        d = !1,
        p = !0;
      if ("function" != typeof e) throw new TypeError("Expected a function");

      function f(t) {
        var n = r,
          o = i;
        return r = i = void 0, c = t, a = e.apply(o, n)
      }

      function h(e) {
        return c = e, s = setTimeout(g, t), u ? f(e) : a
      }

      function m(e) {
        var n = e - l;
        return void 0 === l || n >= t || n < 0 || d && e - c >= o
      }

      function g() {
        var e = ao();
        if (m(e)) return v(e);
        s = setTimeout(g, function(e) {
          var n = t - (e - l);
          return d ? oo(n, o - (e - c)) : n
        }(e))
      }

      function v(e) {
        return s = void 0, p && r ? f(e) : (r = i = void 0, a)
      }

      function y() {
        var e = ao(),
          n = m(e);
        if (r = arguments, i = this, l = e, n) {
          if (void 0 === s) return h(l);
          if (d) return s = setTimeout(g, t), f(l)
        }
        return void 0 === s && (s = setTimeout(g, t)), a
      }
      return t = lo(t) || 0, so(n) && (u = !!n.leading, o = (d = "maxWait" in n) ? io(lo(n.maxWait) || 0, t) : o, p = "trailing" in n ? !!n.trailing : p), y.cancel = function() {
        void 0 !== s && clearTimeout(s), c = 0, r = l = i = s = void 0
      }, y.flush = function() {
        return void 0 === s ? a : v(ao())
      }, y
    },
    uo = /^\[object .+?Constructor\]$/,
    po = "object" == typeof e && e && e.Object === Object && e,
    fo = "object" == typeof self && self && self.Object === Object && self,
    ho = po || fo || Function("return this")(),
    mo = Array.prototype,
    go = Function.prototype,
    vo = Object.prototype,
    yo = ho["__core-js_shared__"],
    bo = function() {
      var e = /[^.]+$/.exec(yo && yo.keys && yo.keys.IE_PROTO || "");
      return e ? "Symbol(src)_1." + e : ""
    }(),
    wo = go.toString,
    xo = vo.hasOwnProperty,
    So = vo.toString,
    Co = RegExp("^" + wo.call(xo).replace(/[\\^$.*+?()[\]{}|]/g, "\\$&").replace(/hasOwnProperty|(function).*?(?=\\\()| for .+?(?=\\\])/g, "$1.*?") + "$"),
    Eo = mo.splice,
    To = Lo(ho, "Map"),
    ko = Lo(Object, "create");

  function Do(e) {
    var t = -1,
      n = e ? e.length : 0;
    for (this.clear(); ++t < n;) {
      var r = e[t];
      this.set(r[0], r[1])
    }
  }

  function Oo(e) {
    var t = -1,
      n = e ? e.length : 0;
    for (this.clear(); ++t < n;) {
      var r = e[t];
      this.set(r[0], r[1])
    }
  }

  function Ao(e) {
    var t = -1,
      n = e ? e.length : 0;
    for (this.clear(); ++t < n;) {
      var r = e[t];
      this.set(r[0], r[1])
    }
  }

  function _o(e, t) {
    for (var n, r, i = e.length; i--;)
      if ((n = e[i][0]) === (r = t) || n != n && r != r) return i;
    return -1
  }

  function Mo(e, t) {
    var n, r, i = e.__data__;
    return ("string" == (r = typeof(n = t)) || "number" == r || "symbol" == r || "boolean" == r ? "__proto__" !== n : null === n) ? i["string" == typeof t ? "string" : "hash"] : i.map
  }

  function Lo(e, t) {
    var n = function(e, t) {
      return null == e ? void 0 : e[t]
    }(e, t);
    return function(e) {
      return !(!Po(e) || (t = e, bo && bo in t)) && (function(e) {
        var t = Po(e) ? So.call(e) : "";
        return "[object Function]" == t || "[object GeneratorFunction]" == t
      }(e) || function(e) {
        var t = !1;
        if (null != e && "function" != typeof e.toString) try {
          t = !!(e + "")
        } catch (e) {}
        return t
      }(e) ? Co : uo).test(function(e) {
        if (null != e) {
          try {
            return wo.call(e)
          } catch (e) {}
          try {
            return e + ""
          } catch (e) {}
        }
        return ""
      }(e));
      var t
    }(n) ? n : void 0
  }

  function Io(e, t) {
    if ("function" != typeof e || t && "function" != typeof t) throw new TypeError("Expected a function");
    var n = function() {
      var r = arguments,
        i = t ? t.apply(this, r) : r[0],
        o = n.cache;
      if (o.has(i)) return o.get(i);
      var a = e.apply(this, r);
      return n.cache = o.set(i, a), a
    };
    return n.cache = new(Io.Cache || Ao), n
  }

  function Po(e) {
    var t = typeof e;
    return !!e && ("object" == t || "function" == t)
  }
  Do.prototype.clear = function() {
    this.__data__ = ko ? ko(null) : {}
  }, Do.prototype.delete = function(e) {
    return this.has(e) && delete this.__data__[e]
  }, Do.prototype.get = function(e) {
    var t = this.__data__;
    if (ko) {
      var n = t[e];
      return "__lodash_hash_undefined__" === n ? void 0 : n
    }
    return xo.call(t, e) ? t[e] : void 0
  }, Do.prototype.has = function(e) {
    var t = this.__data__;
    return ko ? void 0 !== t[e] : xo.call(t, e)
  }, Do.prototype.set = function(e, t) {
    return this.__data__[e] = ko && void 0 === t ? "__lodash_hash_undefined__" : t, this
  }, Oo.prototype.clear = function() {
    this.__data__ = []
  }, Oo.prototype.delete = function(e) {
    var t = this.__data__,
      n = _o(t, e);
    return !(n < 0 || (n == t.length - 1 ? t.pop() : Eo.call(t, n, 1), 0))
  }, Oo.prototype.get = function(e) {
    var t = this.__data__,
      n = _o(t, e);
    return n < 0 ? void 0 : t[n][1]
  }, Oo.prototype.has = function(e) {
    return _o(this.__data__, e) > -1
  }, Oo.prototype.set = function(e, t) {
    var n = this.__data__,
      r = _o(n, e);
    return r < 0 ? n.push([e, t]) : n[r][1] = t, this
  }, Ao.prototype.clear = function() {
    this.__data__ = {
      hash: new Do,
      map: new(To || Oo),
      string: new Do
    }
  }, Ao.prototype.delete = function(e) {
    return Mo(this, e).delete(e)
  }, Ao.prototype.get = function(e) {
    return Mo(this, e).get(e)
  }, Ao.prototype.has = function(e) {
    return Mo(this, e).has(e)
  }, Ao.prototype.set = function(e, t) {
    return Mo(this, e).set(e, t), this
  }, Io.Cache = Ao;
  var jo, No = Io,
    zo = [],
    Ro = "ResizeObserver loop completed with undelivered notifications.";
  ! function(e) {
    e.BORDER_BOX = "border-box", e.CONTENT_BOX = "content-box", e.DEVICE_PIXEL_CONTENT_BOX = "device-pixel-content-box"
  }(jo || (jo = {}));
  var $o, Ho = function(e) {
      return Object.freeze(e)
    },
    Fo = function(e, t) {
      this.inlineSize = e, this.blockSize = t, Ho(this)
    },
    Bo = function() {
      function e(e, t, n, r) {
        return this.x = e, this.y = t, this.width = n, this.height = r, this.top = this.y, this.left = this.x, this.bottom = this.top + this.height, this.right = this.left + this.width, Ho(this)
      }
      return e.prototype.toJSON = function() {
        var e = this;
        return {
          x: e.x,
          y: e.y,
          top: e.top,
          right: e.right,
          bottom: e.bottom,
          left: e.left,
          width: e.width,
          height: e.height
        }
      }, e.fromRect = function(t) {
        return new e(t.x, t.y, t.width, t.height)
      }, e
    }(),
    qo = function(e) {
      return e instanceof SVGElement && "getBBox" in e
    },
    Wo = function(e) {
      if (qo(e)) {
        var t = e.getBBox(),
          n = t.width,
          r = t.height;
        return !n && !r
      }
      var i = e,
        o = i.offsetWidth,
        a = i.offsetHeight;
      return !(o || a || e.getClientRects().length)
    },
    Yo = function(e) {
      var t, n;
      if (e instanceof Element) return !0;
      var r = null === (n = null === (t = e) || void 0 === t ? void 0 : t.ownerDocument) || void 0 === n ? void 0 : n.defaultView;
      return !!(r && e instanceof r.Element)
    },
    Uo = "undefined" != typeof window ? window : {},
    Vo = new WeakMap,
    Xo = /auto|scroll/,
    Go = /^tb|vertical/,
    Zo = /msie|trident/i.test(Uo.navigator && Uo.navigator.userAgent),
    Ko = function(e) {
      return parseFloat(e || "0")
    },
    Jo = function(e, t, n) {
      return void 0 === e && (e = 0), void 0 === t && (t = 0), void 0 === n && (n = !1), new Fo((n ? t : e) || 0, (n ? e : t) || 0)
    },
    Qo = Ho({
      devicePixelContentBoxSize: Jo(),
      borderBoxSize: Jo(),
      contentBoxSize: Jo(),
      contentRect: new Bo(0, 0, 0, 0)
    }),
    ea = function(e, t) {
      if (void 0 === t && (t = !1), Vo.has(e) && !t) return Vo.get(e);
      if (Wo(e)) return Vo.set(e, Qo), Qo;
      var n = getComputedStyle(e),
        r = qo(e) && e.ownerSVGElement && e.getBBox(),
        i = !Zo && "border-box" === n.boxSizing,
        o = Go.test(n.writingMode || ""),
        a = !r && Xo.test(n.overflowY || ""),
        s = !r && Xo.test(n.overflowX || ""),
        l = r ? 0 : Ko(n.paddingTop),
        c = r ? 0 : Ko(n.paddingRight),
        u = r ? 0 : Ko(n.paddingBottom),
        d = r ? 0 : Ko(n.paddingLeft),
        p = r ? 0 : Ko(n.borderTopWidth),
        f = r ? 0 : Ko(n.borderRightWidth),
        h = r ? 0 : Ko(n.borderBottomWidth),
        m = d + c,
        g = l + u,
        v = (r ? 0 : Ko(n.borderLeftWidth)) + f,
        y = p + h,
        b = s ? e.offsetHeight - y - e.clientHeight : 0,
        w = a ? e.offsetWidth - v - e.clientWidth : 0,
        x = i ? m + v : 0,
        S = i ? g + y : 0,
        C = r ? r.width : Ko(n.width) - x - w,
        E = r ? r.height : Ko(n.height) - S - b,
        T = C + m + w + v,
        k = E + g + b + y,
        D = Ho({
          devicePixelContentBoxSize: Jo(Math.round(C * devicePixelRatio), Math.round(E * devicePixelRatio), o),
          borderBoxSize: Jo(T, k, o),
          contentBoxSize: Jo(C, E, o),
          contentRect: new Bo(d, l, C, E)
        });
      return Vo.set(e, D), D
    },
    ta = function(e, t, n) {
      var r = ea(e, n),
        i = r.borderBoxSize,
        o = r.contentBoxSize,
        a = r.devicePixelContentBoxSize;
      switch (t) {
        case jo.DEVICE_PIXEL_CONTENT_BOX:
          return a;
        case jo.BORDER_BOX:
          return i;
        default:
          return o
      }
    },
    na = function(e) {
      var t = ea(e);
      this.target = e, this.contentRect = t.contentRect, this.borderBoxSize = Ho([t.borderBoxSize]), this.contentBoxSize = Ho([t.contentBoxSize]), this.devicePixelContentBoxSize = Ho([t.devicePixelContentBoxSize])
    },
    ra = function(e) {
      if (Wo(e)) return 1 / 0;
      for (var t = 0, n = e.parentNode; n;) t += 1, n = n.parentNode;
      return t
    },
    ia = function() {
      var e = 1 / 0,
        t = [];
      zo.forEach((function(n) {
        if (0 !== n.activeTargets.length) {
          var r = [];
          n.activeTargets.forEach((function(t) {
            var n = new na(t.target),
              i = ra(t.target);
            r.push(n), t.lastReportedSize = ta(t.target, t.observedBox), i < e && (e = i)
          })), t.push((function() {
            n.callback.call(n.observer, r, n.observer)
          })), n.activeTargets.splice(0, n.activeTargets.length)
        }
      }));
      for (var n = 0, r = t; n < r.length; n++)(0, r[n])();
      return e
    },
    oa = function(e) {
      zo.forEach((function(t) {
        t.activeTargets.splice(0, t.activeTargets.length), t.skippedTargets.splice(0, t.skippedTargets.length), t.observationTargets.forEach((function(n) {
          n.isActive() && (ra(n.target) > e ? t.activeTargets.push(n) : t.skippedTargets.push(n))
        }))
      }))
    },
    aa = [],
    sa = 0,
    la = {
      attributes: !0,
      characterData: !0,
      childList: !0,
      subtree: !0
    },
    ca = ["resize", "load", "transitionend", "animationend", "animationstart", "animationiteration", "keyup", "keydown", "mouseup", "mousedown", "mouseover", "mouseout", "blur", "focus"],
    ua = function(e) {
      return void 0 === e && (e = 0), Date.now() + e
    },
    da = !1,
    pa = new(function() {
      function e() {
        var e = this;
        this.stopped = !0, this.listener = function() {
          return e.schedule()
        }
      }
      return e.prototype.run = function(e) {
        var t = this;
        if (void 0 === e && (e = 250), !da) {
          da = !0;
          var n, r = ua(e);
          n = function() {
              var n = !1;
              try {
                n = function() {
                  var e, t = 0;
                  for (oa(t); zo.some((function(e) {
                      return e.activeTargets.length > 0
                    }));) t = ia(), oa(t);
                  return zo.some((function(e) {
                    return e.skippedTargets.length > 0
                  })) && ("function" == typeof ErrorEvent ? e = new ErrorEvent("error", {
                    message: Ro
                  }) : ((e = document.createEvent("Event")).initEvent("error", !1, !1), e.message = Ro), window.dispatchEvent(e)), t > 0
                }()
              } finally {
                if (da = !1, e = r - ua(), !sa) return;
                n ? t.run(1e3) : e > 0 ? t.run(e) : t.start()
              }
            },
            function(e) {
              if (!$o) {
                var t = 0,
                  n = document.createTextNode("");
                new MutationObserver((function() {
                  return aa.splice(0).forEach((function(e) {
                    return e()
                  }))
                })).observe(n, {
                  characterData: !0
                }), $o = function() {
                  n.textContent = "" + (t ? t-- : t++)
                }
              }
              aa.push(e), $o()
            }((function() {
              requestAnimationFrame(n)
            }))
        }
      }, e.prototype.schedule = function() {
        this.stop(), this.run()
      }, e.prototype.observe = function() {
        var e = this,
          t = function() {
            return e.observer && e.observer.observe(document.body, la)
          };
        document.body ? t() : Uo.addEventListener("DOMContentLoaded", t)
      }, e.prototype.start = function() {
        var e = this;
        this.stopped && (this.stopped = !1, this.observer = new MutationObserver(this.listener), this.observe(), ca.forEach((function(t) {
          return Uo.addEventListener(t, e.listener, !0)
        })))
      }, e.prototype.stop = function() {
        var e = this;
        this.stopped || (this.observer && this.observer.disconnect(), ca.forEach((function(t) {
          return Uo.removeEventListener(t, e.listener, !0)
        })), this.stopped = !0)
      }, e
    }()),
    fa = function(e) {
      !sa && e > 0 && pa.start(), !(sa += e) && pa.stop()
    },
    ha = function() {
      function e(e, t) {
        this.target = e, this.observedBox = t || jo.CONTENT_BOX, this.lastReportedSize = {
          inlineSize: 0,
          blockSize: 0
        }
      }
      return e.prototype.isActive = function() {
        var e, t = ta(this.target, this.observedBox, !0);
        return e = this.target, qo(e) || function(e) {
          switch (e.tagName) {
            case "INPUT":
              if ("image" !== e.type) break;
            case "VIDEO":
            case "AUDIO":
            case "EMBED":
            case "OBJECT":
            case "CANVAS":
            case "IFRAME":
            case "IMG":
              return !0
          }
          return !1
        }(e) || "inline" !== getComputedStyle(e).display || (this.lastReportedSize = t), this.lastReportedSize.inlineSize !== t.inlineSize || this.lastReportedSize.blockSize !== t.blockSize
      }, e
    }(),
    ma = function(e, t) {
      this.activeTargets = [], this.skippedTargets = [], this.observationTargets = [], this.observer = e, this.callback = t
    },
    ga = new WeakMap,
    va = function(e, t) {
      for (var n = 0; n < e.length; n += 1)
        if (e[n].target === t) return n;
      return -1
    },
    ya = function() {
      function e() {}
      return e.connect = function(e, t) {
        var n = new ma(e, t);
        ga.set(e, n)
      }, e.observe = function(e, t, n) {
        var r = ga.get(e),
          i = 0 === r.observationTargets.length;
        va(r.observationTargets, t) < 0 && (i && zo.push(r), r.observationTargets.push(new ha(t, n && n.box)), fa(1), pa.schedule())
      }, e.unobserve = function(e, t) {
        var n = ga.get(e),
          r = va(n.observationTargets, t),
          i = 1 === n.observationTargets.length;
        r >= 0 && (i && zo.splice(zo.indexOf(n), 1), n.observationTargets.splice(r, 1), fa(-1))
      }, e.disconnect = function(e) {
        var t = this,
          n = ga.get(e);
        n.observationTargets.slice().forEach((function(n) {
          return t.unobserve(e, n.target)
        })), n.activeTargets.splice(0, n.activeTargets.length)
      }, e
    }(),
    ba = function() {
      function e(e) {
        if (0 === arguments.length) throw new TypeError("Failed to construct 'ResizeObserver': 1 argument required, but only 0 present.");
        if ("function" != typeof e) throw new TypeError("Failed to construct 'ResizeObserver': The callback provided as parameter 1 is not a function.");
        ya.connect(this, e)
      }
      return e.prototype.observe = function(e, t) {
        if (0 === arguments.length) throw new TypeError("Failed to execute 'observe' on 'ResizeObserver': 1 argument required, but only 0 present.");
        if (!Yo(e)) throw new TypeError("Failed to execute 'observe' on 'ResizeObserver': parameter 1 is not of type 'Element");
        ya.observe(this, e, t)
      }, e.prototype.unobserve = function(e) {
        if (0 === arguments.length) throw new TypeError("Failed to execute 'unobserve' on 'ResizeObserver': 1 argument required, but only 0 present.");
        if (!Yo(e)) throw new TypeError("Failed to execute 'unobserve' on 'ResizeObserver': parameter 1 is not of type 'Element");
        ya.unobserve(this, e)
      }, e.prototype.disconnect = function() {
        ya.disconnect(this)
      }, e.toString = function() {
        return "function ResizeObserver () { [polyfill code] }"
      }, e
    }(),
    wa = o.TypeError,
    xa = function(e) {
      return function(t, n, r, i) {
        ce(n);
        var o = w(t),
          a = st(o),
          s = ht(o),
          l = e ? s - 1 : 0,
          c = e ? -1 : 1;
        if (r < 2)
          for (;;) {
            if (l in a) {
              i = a[l], l += c;
              break
            }
            if (l += c, e ? l < 0 : s <= l) throw wa("Reduce of empty array with no initial value")
          }
        for (; e ? l >= 0 : s > l; l += c) l in a && (i = n(i, a[l], l, o));
        return i
      }
    },
    Sa = {
      left: xa(!1),
      right: xa(!0)
    },
    Ca = "process" == Ve(o.process),
    Ea = Sa.left,
    Ta = Mt("reduce");
  pn({
    target: "Array",
    proto: !0,
    forced: !Ta || !Ca && j > 79 && j < 83
  }, {
    reduce: function(e) {
      var t = arguments.length;
      return Ea(this, e, t, t > 1 ? arguments[1] : void 0)
    }
  });
  var ka, Da, Oa = function() {
      var e = ee(this),
        t = "";
      return e.hasIndices && (t += "d"), e.global && (t += "g"), e.ignoreCase && (t += "i"), e.multiline && (t += "m"), e.dotAll && (t += "s"), e.unicode && (t += "u"), e.sticky && (t += "y"), t
    },
    Aa = o.RegExp,
    _a = u((function() {
      var e = Aa("a", "y");
      return e.lastIndex = 2, null != e.exec("abcd")
    })),
    Ma = _a || u((function() {
      return !Aa("a", "y").sticky
    })),
    La = {
      BROKEN_CARET: _a || u((function() {
        var e = Aa("^r", "gy");
        return e.lastIndex = 2, null != e.exec("str")
      })),
      MISSED_STICKY: Ma,
      UNSUPPORTED_Y: _a
    },
    Ia = o.RegExp,
    Pa = u((function() {
      var e = Ia(".", "s");
      return !(e.dotAll && e.exec("\n") && "s" === e.flags)
    })),
    ja = o.RegExp,
    Na = u((function() {
      var e = ja("(?<a>b)", "g");
      return "b" !== e.exec("b").groups.a || "bc" !== "b".replace(e, "$<a>c")
    })),
    za = Be.get,
    Ra = c("native-string-replace", String.prototype.replace),
    $a = RegExp.prototype.exec,
    Ha = $a,
    Fa = g("".charAt),
    Ba = g("".indexOf),
    qa = g("".replace),
    Wa = g("".slice),
    Ya = (Da = /b*/g, ne($a, ka = /a/, "a"), ne($a, Da, "a"), 0 !== ka.lastIndex || 0 !== Da.lastIndex),
    Ua = La.BROKEN_CARET,
    Va = void 0 !== /()??/.exec("")[1];
  (Ya || Va || Ua || Pa || Na) && (Ha = function(e) {
    var t, n, r, i, o, a, s, l = this,
      c = za(l),
      u = hn(e),
      d = c.raw;
    if (d) return d.lastIndex = l.lastIndex, t = ne(Ha, d, u), l.lastIndex = d.lastIndex, t;
    var p = c.groups,
      f = Ua && l.sticky,
      h = ne(Oa, l),
      m = l.source,
      g = 0,
      v = u;
    if (f && (h = qa(h, "y", ""), -1 === Ba(h, "g") && (h += "g"), v = Wa(u, l.lastIndex), l.lastIndex > 0 && (!l.multiline || l.multiline && "\n" !== Fa(u, l.lastIndex - 1)) && (m = "(?: " + m + ")", v = " " + v, g++), n = new RegExp("^(?:" + m + ")", h)), Va && (n = new RegExp("^" + m + "$(?!\\s)", h)), Ya && (r = l.lastIndex), i = ne($a, f ? n : l, v), f ? i ? (i.input = Wa(i.input, g), i[0] = Wa(i[0], g), i.index = l.lastIndex, l.lastIndex += i[0].length) : l.lastIndex = 0 : Ya && i && (l.lastIndex = l.global ? i.index + i[0].length : r), Va && i && i.length > 1 && ne(Ra, i[0], n, (function() {
        for (o = 1; o < arguments.length - 2; o++) void 0 === arguments[o] && (i[o] = void 0)
      })), i && p)
      for (i.groups = a = Wn(null), o = 0; o < p.length; o++) a[(s = p[o])[0]] = i[s[1]];
    return i
  });
  var Xa = Ha;
  pn({
    target: "RegExp",
    proto: !0,
    forced: /./.exec !== Xa
  }, {
    exec: Xa
  });
  var Ga = B("species"),
    Za = RegExp.prototype,
    Ka = function(e, t, n, r) {
      var i = B(e),
        o = !u((function() {
          var t = {};
          return t[i] = function() {
            return 7
          }, 7 != "" [e](t)
        })),
        a = o && !u((function() {
          var t = !1,
            n = /a/;
          return "split" === e && ((n = {}).constructor = {}, n.constructor[Ga] = function() {
            return n
          }, n.flags = "", n[i] = /./ [i]), n.exec = function() {
            return t = !0, null
          }, n[i](""), !t
        }));
      if (!o || !a || n) {
        var s = g(/./ [i]),
          l = t(i, "" [e], (function(e, t, n, r, i) {
            var a = g(e),
              l = t.exec;
            return l === Xa || l === Za.exec ? o && !i ? {
              done: !0,
              value: s(t, n, r)
            } : {
              done: !0,
              value: a(n, t, r)
            } : {
              done: !1
            }
          }));
        We(String.prototype, e, l[0]), We(Za, i, l[1])
      }
      r && we(Za[i], "sham", !0)
    },
    Ja = Mr.charAt,
    Qa = function(e, t, n) {
      return t + (n ? Ja(e, t).length : 1)
    },
    es = o.TypeError,
    ts = function(e, t) {
      var n = e.exec;
      if (D(n)) {
        var r = ne(n, e, t);
        return null !== r && ee(r), r
      }
      if ("RegExp" === Ve(e)) return ne(Xa, e, t);
      throw es("RegExp#exec called on incompatible receiver")
    };
  Ka("match", (function(e, t, n) {
    return [function(t) {
      var n = y(this),
        r = null == t ? void 0 : ue(t, e);
      return r ? ne(r, t, n) : new RegExp(t)[e](hn(n))
    }, function(e) {
      var r = ee(this),
        i = hn(e),
        o = n(t, r, i);
      if (o.done) return o.value;
      if (!r.global) return ts(r, i);
      var a = r.unicode;
      r.lastIndex = 0;
      for (var s, l = [], c = 0; null !== (s = ts(r, i));) {
        var u = hn(s[0]);
        l[c] = u, "" === u && (r.lastIndex = Qa(i, ft(r.lastIndex), a)), c++
      }
      return 0 === c ? null : l
    }]
  }));
  var ns = Ee.EXISTS,
    rs = ye.f,
    is = Function.prototype,
    os = g(is.toString),
    as = /function\b(?:\s|\/\*[\S\s]*?\*\/|\/\/[^\n\r]*[\n\r]+)*([^\s(/]*)/,
    ss = g(as.exec);
  Y && !ns && rs(is, "name", {
    configurable: !0,
    get: function() {
      try {
        return ss(as, os(this))[1]
      } catch (e) {
        return ""
      }
    }
  });
  var ls = Function.prototype,
    cs = ls.apply,
    us = ls.call,
    ds = "object" == typeof Reflect && Reflect.apply || (d ? us.bind(cs) : function() {
      return us.apply(cs, arguments)
    }),
    ps = Math.floor,
    fs = g("".charAt),
    hs = g("".replace),
    ms = g("".slice),
    gs = /\$([$&'`]|\d{1,2}|<[^>]*>)/g,
    vs = /\$([$&'`]|\d{1,2})/g,
    ys = function(e, t, n, r, i, o) {
      var a = n + e.length,
        s = r.length,
        l = vs;
      return void 0 !== i && (i = w(i), l = gs), hs(o, l, (function(o, l) {
        var c;
        switch (fs(l, 0)) {
          case "$":
            return "$";
          case "&":
            return e;
          case "`":
            return ms(t, 0, n);
          case "'":
            return ms(t, a);
          case "<":
            c = i[ms(l, 1, -1)];
            break;
          default:
            var u = +l;
            if (0 === u) return o;
            if (u > s) {
              var d = ps(u / 10);
              return 0 === d ? o : d <= s ? void 0 === r[d - 1] ? fs(l, 1) : r[d - 1] + fs(l, 1) : o
            }
            c = r[u - 1]
        }
        return void 0 === c ? "" : c
      }))
    },
    bs = B("replace"),
    ws = Math.max,
    xs = Math.min,
    Ss = g([].concat),
    Cs = g([].push),
    Es = g("".indexOf),
    Ts = g("".slice),
    ks = "$0" === "a".replace(/./, "$0"),
    Ds = !!/./ [bs] && "" === /./ [bs]("a", "$0");
  Ka("replace", (function(e, t, n) {
    var r = Ds ? "$" : "$0";
    return [function(e, n) {
      var r = y(this),
        i = null == e ? void 0 : ue(e, bs);
      return i ? ne(i, e, r, n) : ne(t, hn(r), e, n)
    }, function(e, i) {
      var o = ee(this),
        a = hn(e);
      if ("string" == typeof i && -1 === Es(i, r) && -1 === Es(i, "$<")) {
        var s = n(t, o, a, i);
        if (s.done) return s.value
      }
      var l = D(i);
      l || (i = hn(i));
      var c = o.global;
      if (c) {
        var u = o.unicode;
        o.lastIndex = 0
      }
      for (var d = [];;) {
        var p = ts(o, a);
        if (null === p) break;
        if (Cs(d, p), !c) break;
        "" === hn(p[0]) && (o.lastIndex = Qa(a, ft(o.lastIndex), u))
      }
      for (var f, h = "", m = 0, g = 0; g < d.length; g++) {
        for (var v = hn((p = d[g])[0]), y = ws(xs(dt(p.index), a.length), 0), b = [], w = 1; w < p.length; w++) Cs(b, void 0 === (f = p[w]) ? f : String(f));
        var x = p.groups;
        if (l) {
          var S = Ss([v], b, y, a);
          void 0 !== x && Cs(S, x);
          var C = hn(ds(i, void 0, S))
        } else C = ys(v, a, y, b, x, i);
        y >= m && (h += Ts(a, m, y) + C, m = y + v.length)
      }
      return h + Ts(a, m)
    }]
  }), !!u((function() {
    var e = /./;
    return e.exec = function() {
      var e = [];
      return e.groups = {
        a: "7"
      }, e
    }, "7" !== "".replace(e, "$<a>")
  })) || !ks || Ds);
  var Os = function(e) {
    return Array.prototype.reduce.call(e, (function(e, t) {
      var n = t.name.match(/data-simplebar-(.+)/);
      if (n) {
        var r = n[1].replace(/\W+(.)/g, (function(e, t) {
          return t.toUpperCase()
        }));
        switch (t.value) {
          case "true":
            e[r] = !0;
            break;
          case "false":
            e[r] = !1;
            break;
          case void 0:
            e[r] = !0;
            break;
          default:
            e[r] = t.value
        }
      }
      return e
    }), {})
  };

  function As(e) {
    return e && e.ownerDocument && e.ownerDocument.defaultView ? e.ownerDocument.defaultView : window
  }

  function _s(e) {
    return e && e.ownerDocument ? e.ownerDocument : document
  }
  var Ms = null,
    Ls = null;

  function Is(e) {
    if (null === Ms) {
      var t = _s(e);
      if (void 0 === t) return Ms = 0;
      var n = t.body,
        r = t.createElement("div");
      r.classList.add("simplebar-hide-scrollbar"), n.appendChild(r);
      var i = r.getBoundingClientRect().right;
      n.removeChild(r), Ms = i
    }
    return Ms
  }
  Nt && window.addEventListener("resize", (function() {
    Ls !== window.devicePixelRatio && (Ls = window.devicePixelRatio, Ms = null)
  }));
  var Ps = function() {
    function e(t, n) {
      var r = this;
      this.onScroll = function() {
        var e = As(r.el);
        r.scrollXTicking || (e.requestAnimationFrame(r.scrollX), r.scrollXTicking = !0), r.scrollYTicking || (e.requestAnimationFrame(r.scrollY), r.scrollYTicking = !0)
      }, this.scrollX = function() {
        r.axis.x.isOverflowing && (r.showScrollbar("x"), r.positionScrollbar("x")), r.scrollXTicking = !1
      }, this.scrollY = function() {
        r.axis.y.isOverflowing && (r.showScrollbar("y"), r.positionScrollbar("y")), r.scrollYTicking = !1
      }, this.onMouseEnter = function() {
        r.showScrollbar("x"), r.showScrollbar("y")
      }, this.onMouseMove = function(e) {
        r.mouseX = e.clientX, r.mouseY = e.clientY, (r.axis.x.isOverflowing || r.axis.x.forceVisible) && r.onMouseMoveForAxis("x"), (r.axis.y.isOverflowing || r.axis.y.forceVisible) && r.onMouseMoveForAxis("y")
      }, this.onMouseLeave = function() {
        r.onMouseMove.cancel(), (r.axis.x.isOverflowing || r.axis.x.forceVisible) && r.onMouseLeaveForAxis("x"), (r.axis.y.isOverflowing || r.axis.y.forceVisible) && r.onMouseLeaveForAxis("y"), r.mouseX = -1, r.mouseY = -1
      }, this.onWindowResize = function() {
        r.scrollbarWidth = r.getScrollbarWidth(), r.hideNativeScrollbar()
      }, this.hideScrollbars = function() {
        r.axis.x.track.rect = r.axis.x.track.el.getBoundingClientRect(), r.axis.y.track.rect = r.axis.y.track.el.getBoundingClientRect(), r.isWithinBounds(r.axis.y.track.rect) || (r.axis.y.scrollbar.el.classList.remove(r.classNames.visible), r.axis.y.isVisible = !1), r.isWithinBounds(r.axis.x.track.rect) || (r.axis.x.scrollbar.el.classList.remove(r.classNames.visible), r.axis.x.isVisible = !1)
      }, this.onPointerEvent = function(e) {
        var t, n;
        r.axis.x.track.rect = r.axis.x.track.el.getBoundingClientRect(), r.axis.y.track.rect = r.axis.y.track.el.getBoundingClientRect(), (r.axis.x.isOverflowing || r.axis.x.forceVisible) && (t = r.isWithinBounds(r.axis.x.track.rect)), (r.axis.y.isOverflowing || r.axis.y.forceVisible) && (n = r.isWithinBounds(r.axis.y.track.rect)), (t || n) && (e.preventDefault(), e.stopPropagation(), "mousedown" === e.type && (t && (r.axis.x.scrollbar.rect = r.axis.x.scrollbar.el.getBoundingClientRect(), r.isWithinBounds(r.axis.x.scrollbar.rect) ? r.onDragStart(e, "x") : r.onTrackClick(e, "x")), n && (r.axis.y.scrollbar.rect = r.axis.y.scrollbar.el.getBoundingClientRect(), r.isWithinBounds(r.axis.y.scrollbar.rect) ? r.onDragStart(e, "y") : r.onTrackClick(e, "y"))))
      }, this.drag = function(t) {
        var n = r.axis[r.draggedAxis].track,
          i = n.rect[r.axis[r.draggedAxis].sizeAttr],
          o = r.axis[r.draggedAxis].scrollbar,
          a = r.contentWrapperEl[r.axis[r.draggedAxis].scrollSizeAttr],
          s = parseInt(r.elStyles[r.axis[r.draggedAxis].sizeAttr], 10);
        t.preventDefault(), t.stopPropagation();
        var l = (("y" === r.draggedAxis ? t.pageY : t.pageX) - n.rect[r.axis[r.draggedAxis].offsetAttr] - r.axis[r.draggedAxis].dragOffset) / (i - o.size) * (a - s);
        "x" === r.draggedAxis && (l = r.isRtl && e.getRtlHelpers().isRtlScrollbarInverted ? l - (i + o.size) : l, l = r.isRtl && e.getRtlHelpers().isRtlScrollingInverted ? -l : l), r.contentWrapperEl[r.axis[r.draggedAxis].scrollOffsetAttr] = l
      }, this.onEndDrag = function(e) {
        var t = _s(r.el),
          n = As(r.el);
        e.preventDefault(), e.stopPropagation(), r.el.classList.remove(r.classNames.dragging), t.removeEventListener("mousemove", r.drag, !0), t.removeEventListener("mouseup", r.onEndDrag, !0), r.removePreventClickId = n.setTimeout((function() {
          t.removeEventListener("click", r.preventClick, !0), t.removeEventListener("dblclick", r.preventClick, !0), r.removePreventClickId = null
        }))
      }, this.preventClick = function(e) {
        e.preventDefault(), e.stopPropagation()
      }, this.el = t, this.minScrollbarWidth = 20, this.options = Object.assign({}, e.defaultOptions, n), this.classNames = Object.assign({}, e.defaultOptions.classNames, this.options.classNames), this.axis = {
        x: {
          scrollOffsetAttr: "scrollLeft",
          sizeAttr: "width",
          scrollSizeAttr: "scrollWidth",
          offsetSizeAttr: "offsetWidth",
          offsetAttr: "left",
          overflowAttr: "overflowX",
          dragOffset: 0,
          isOverflowing: !0,
          isVisible: !1,
          forceVisible: !1,
          track: {},
          scrollbar: {}
        },
        y: {
          scrollOffsetAttr: "scrollTop",
          sizeAttr: "height",
          scrollSizeAttr: "scrollHeight",
          offsetSizeAttr: "offsetHeight",
          offsetAttr: "top",
          overflowAttr: "overflowY",
          dragOffset: 0,
          isOverflowing: !0,
          isVisible: !1,
          forceVisible: !1,
          track: {},
          scrollbar: {}
        }
      }, this.removePreventClickId = null, e.instances.has(this.el) || (this.recalculate = Xi(this.recalculate.bind(this), 64), this.onMouseMove = Xi(this.onMouseMove.bind(this), 64), this.hideScrollbars = co(this.hideScrollbars.bind(this), this.options.timeout), this.onWindowResize = co(this.onWindowResize.bind(this), 64, {
        leading: !0
      }), e.getRtlHelpers = No(e.getRtlHelpers), this.init())
    }
    e.getRtlHelpers = function() {
      var t = document.createElement("div");
      t.innerHTML = '<div class="hs-dummy-scrollbar-size"><div style="height: 200%; width: 200%; margin: 10px 0;"></div></div>';
      var n = t.firstElementChild;
      document.body.appendChild(n);
      var r = n.firstElementChild;
      n.scrollLeft = 0;
      var i = e.getOffset(n),
        o = e.getOffset(r);
      n.scrollLeft = 999;
      var a = e.getOffset(r);
      return {
        isRtlScrollingInverted: i.left !== o.left && o.left - a.left != 0,
        isRtlScrollbarInverted: i.left !== o.left
      }
    }, e.getOffset = function(e) {
      var t = e.getBoundingClientRect(),
        n = _s(e),
        r = As(e);
      return {
        top: t.top + (r.pageYOffset || n.documentElement.scrollTop),
        left: t.left + (r.pageXOffset || n.documentElement.scrollLeft)
      }
    };
    var t = e.prototype;
    return t.init = function() {
      e.instances.set(this.el, this), Nt && (this.initDOM(), this.setAccessibilityAttributes(), this.scrollbarWidth = this.getScrollbarWidth(), this.recalculate(), this.initListeners())
    }, t.initDOM = function() {
      var e = this;
      if (Array.prototype.filter.call(this.el.children, (function(t) {
          return t.classList.contains(e.classNames.wrapper)
        })).length) this.wrapperEl = this.el.querySelector("." + this.classNames.wrapper), this.contentWrapperEl = this.options.scrollableNode || this.el.querySelector("." + this.classNames.contentWrapper), this.contentEl = this.options.contentNode || this.el.querySelector("." + this.classNames.contentEl), this.offsetEl = this.el.querySelector("." + this.classNames.offset), this.maskEl = this.el.querySelector("." + this.classNames.mask), this.placeholderEl = this.findChild(this.wrapperEl, "." + this.classNames.placeholder), this.heightAutoObserverWrapperEl = this.el.querySelector("." + this.classNames.heightAutoObserverWrapperEl), this.heightAutoObserverEl = this.el.querySelector("." + this.classNames.heightAutoObserverEl), this.axis.x.track.el = this.findChild(this.el, "." + this.classNames.track + "." + this.classNames.horizontal), this.axis.y.track.el = this.findChild(this.el, "." + this.classNames.track + "." + this.classNames.vertical);
      else {
        for (this.wrapperEl = document.createElement("div"), this.contentWrapperEl = document.createElement("div"), this.offsetEl = document.createElement("div"), this.maskEl = document.createElement("div"), this.contentEl = document.createElement("div"), this.placeholderEl = document.createElement("div"), this.heightAutoObserverWrapperEl = document.createElement("div"), this.heightAutoObserverEl = document.createElement("div"), this.wrapperEl.classList.add(this.classNames.wrapper), this.contentWrapperEl.classList.add(this.classNames.contentWrapper), this.offsetEl.classList.add(this.classNames.offset), this.maskEl.classList.add(this.classNames.mask), this.contentEl.classList.add(this.classNames.contentEl), this.placeholderEl.classList.add(this.classNames.placeholder), this.heightAutoObserverWrapperEl.classList.add(this.classNames.heightAutoObserverWrapperEl), this.heightAutoObserverEl.classList.add(this.classNames.heightAutoObserverEl); this.el.firstChild;) this.contentEl.appendChild(this.el.firstChild);
        this.contentWrapperEl.appendChild(this.contentEl), this.offsetEl.appendChild(this.contentWrapperEl), this.maskEl.appendChild(this.offsetEl), this.heightAutoObserverWrapperEl.appendChild(this.heightAutoObserverEl), this.wrapperEl.appendChild(this.heightAutoObserverWrapperEl), this.wrapperEl.appendChild(this.maskEl), this.wrapperEl.appendChild(this.placeholderEl), this.el.appendChild(this.wrapperEl)
      }
      if (!this.axis.x.track.el || !this.axis.y.track.el) {
        var t = document.createElement("div"),
          n = document.createElement("div");
        t.classList.add(this.classNames.track), n.classList.add(this.classNames.scrollbar), t.appendChild(n), this.axis.x.track.el = t.cloneNode(!0), this.axis.x.track.el.classList.add(this.classNames.horizontal), this.axis.y.track.el = t.cloneNode(!0), this.axis.y.track.el.classList.add(this.classNames.vertical), this.el.appendChild(this.axis.x.track.el), this.el.appendChild(this.axis.y.track.el)
      }
      this.axis.x.scrollbar.el = this.axis.x.track.el.querySelector("." + this.classNames.scrollbar), this.axis.y.scrollbar.el = this.axis.y.track.el.querySelector("." + this.classNames.scrollbar), this.options.autoHide || (this.axis.x.scrollbar.el.classList.add(this.classNames.visible), this.axis.y.scrollbar.el.classList.add(this.classNames.visible)), this.el.setAttribute("data-simplebar", "init")
    }, t.setAccessibilityAttributes = function() {
      var e = this.options.ariaLabel || "scrollable content";
      this.contentWrapperEl.setAttribute("tabindex", "0"), this.contentWrapperEl.setAttribute("role", "region"), this.contentWrapperEl.setAttribute("aria-label", e)
    }, t.initListeners = function() {
      var e = this,
        t = As(this.el);
      this.options.autoHide && this.el.addEventListener("mouseenter", this.onMouseEnter), ["mousedown", "click", "dblclick"].forEach((function(t) {
        e.el.addEventListener(t, e.onPointerEvent, !0)
      })), ["touchstart", "touchend", "touchmove"].forEach((function(t) {
        e.el.addEventListener(t, e.onPointerEvent, {
          capture: !0,
          passive: !0
        })
      })), this.el.addEventListener("mousemove", this.onMouseMove), this.el.addEventListener("mouseleave", this.onMouseLeave), this.contentWrapperEl.addEventListener("scroll", this.onScroll), t.addEventListener("resize", this.onWindowResize);
      var n = !1,
        r = t.ResizeObserver || ba;
      this.resizeObserver = new r((function() {
        n && e.recalculate()
      })), this.resizeObserver.observe(this.el), this.resizeObserver.observe(this.contentEl), t.requestAnimationFrame((function() {
        n = !0
      })), this.mutationObserver = new t.MutationObserver(this.recalculate), this.mutationObserver.observe(this.contentEl, {
        childList: !0,
        subtree: !0,
        characterData: !0
      })
    }, t.recalculate = function() {
      var e = As(this.el);
      this.elStyles = e.getComputedStyle(this.el), this.isRtl = "rtl" === this.elStyles.direction;
      var t = this.heightAutoObserverEl.offsetHeight <= 1,
        n = this.heightAutoObserverEl.offsetWidth <= 1,
        r = this.contentEl.offsetWidth,
        i = this.contentWrapperEl.offsetWidth,
        o = this.elStyles.overflowX,
        a = this.elStyles.overflowY;
      this.contentEl.style.padding = this.elStyles.paddingTop + " " + this.elStyles.paddingRight + " " + this.elStyles.paddingBottom + " " + this.elStyles.paddingLeft, this.wrapperEl.style.margin = "-" + this.elStyles.paddingTop + " -" + this.elStyles.paddingRight + " -" + this.elStyles.paddingBottom + " -" + this.elStyles.paddingLeft;
      var s = this.contentEl.scrollHeight,
        l = this.contentEl.scrollWidth;
      this.contentWrapperEl.style.height = t ? "auto" : "100%", this.placeholderEl.style.width = n ? r + "px" : "auto", this.placeholderEl.style.height = s + "px";
      var c = this.contentWrapperEl.offsetHeight;
      this.axis.x.isOverflowing = l > r, this.axis.y.isOverflowing = s > c, this.axis.x.isOverflowing = "hidden" !== o && this.axis.x.isOverflowing, this.axis.y.isOverflowing = "hidden" !== a && this.axis.y.isOverflowing, this.axis.x.forceVisible = "x" === this.options.forceVisible || !0 === this.options.forceVisible, this.axis.y.forceVisible = "y" === this.options.forceVisible || !0 === this.options.forceVisible, this.hideNativeScrollbar();
      var u = this.axis.x.isOverflowing ? this.scrollbarWidth : 0,
        d = this.axis.y.isOverflowing ? this.scrollbarWidth : 0;
      this.axis.x.isOverflowing = this.axis.x.isOverflowing && l > i - d, this.axis.y.isOverflowing = this.axis.y.isOverflowing && s > c - u, this.axis.x.scrollbar.size = this.getScrollbarSize("x"), this.axis.y.scrollbar.size = this.getScrollbarSize("y"), this.axis.x.scrollbar.el.style.width = this.axis.x.scrollbar.size + "px", this.axis.y.scrollbar.el.style.height = this.axis.y.scrollbar.size + "px", this.positionScrollbar("x"), this.positionScrollbar("y"), this.toggleTrackVisibility("x"), this.toggleTrackVisibility("y")
    }, t.getScrollbarSize = function(e) {
      if (void 0 === e && (e = "y"), !this.axis[e].isOverflowing) return 0;
      var t, n = this.contentEl[this.axis[e].scrollSizeAttr],
        r = this.axis[e].track.el[this.axis[e].offsetSizeAttr],
        i = r / n;
      return t = Math.max(~~(i * r), this.options.scrollbarMinSize), this.options.scrollbarMaxSize && (t = Math.min(t, this.options.scrollbarMaxSize)), t
    }, t.positionScrollbar = function(t) {
      if (void 0 === t && (t = "y"), this.axis[t].isOverflowing) {
        var n = this.contentWrapperEl[this.axis[t].scrollSizeAttr],
          r = this.axis[t].track.el[this.axis[t].offsetSizeAttr],
          i = parseInt(this.elStyles[this.axis[t].sizeAttr], 10),
          o = this.axis[t].scrollbar,
          a = this.contentWrapperEl[this.axis[t].scrollOffsetAttr],
          s = (a = "x" === t && this.isRtl && e.getRtlHelpers().isRtlScrollingInverted ? -a : a) / (n - i),
          l = ~~((r - o.size) * s);
        l = "x" === t && this.isRtl && e.getRtlHelpers().isRtlScrollbarInverted ? l + (r - o.size) : l, o.el.style.transform = "x" === t ? "translate3d(" + l + "px, 0, 0)" : "translate3d(0, " + l + "px, 0)"
      }
    }, t.toggleTrackVisibility = function(e) {
      void 0 === e && (e = "y");
      var t = this.axis[e].track.el,
        n = this.axis[e].scrollbar.el;
      this.axis[e].isOverflowing || this.axis[e].forceVisible ? (t.style.visibility = "visible", this.contentWrapperEl.style[this.axis[e].overflowAttr] = "scroll") : (t.style.visibility = "hidden", this.contentWrapperEl.style[this.axis[e].overflowAttr] = "hidden"), this.axis[e].isOverflowing ? n.style.display = "block" : n.style.display = "none"
    }, t.hideNativeScrollbar = function() {
      this.offsetEl.style[this.isRtl ? "left" : "right"] = this.axis.y.isOverflowing || this.axis.y.forceVisible ? "-" + this.scrollbarWidth + "px" : 0, this.offsetEl.style.bottom = this.axis.x.isOverflowing || this.axis.x.forceVisible ? "-" + this.scrollbarWidth + "px" : 0
    }, t.onMouseMoveForAxis = function(e) {
      void 0 === e && (e = "y"), this.axis[e].track.rect = this.axis[e].track.el.getBoundingClientRect(), this.axis[e].scrollbar.rect = this.axis[e].scrollbar.el.getBoundingClientRect(), this.isWithinBounds(this.axis[e].scrollbar.rect) ? this.axis[e].scrollbar.el.classList.add(this.classNames.hover) : this.axis[e].scrollbar.el.classList.remove(this.classNames.hover), this.isWithinBounds(this.axis[e].track.rect) ? (this.showScrollbar(e), this.axis[e].track.el.classList.add(this.classNames.hover)) : this.axis[e].track.el.classList.remove(this.classNames.hover)
    }, t.onMouseLeaveForAxis = function(e) {
      void 0 === e && (e = "y"), this.axis[e].track.el.classList.remove(this.classNames.hover), this.axis[e].scrollbar.el.classList.remove(this.classNames.hover)
    }, t.showScrollbar = function(e) {
      void 0 === e && (e = "y");
      var t = this.axis[e].scrollbar.el;
      this.axis[e].isVisible || (t.classList.add(this.classNames.visible), this.axis[e].isVisible = !0), this.options.autoHide && this.hideScrollbars()
    }, t.onDragStart = function(e, t) {
      void 0 === t && (t = "y");
      var n = _s(this.el),
        r = As(this.el),
        i = this.axis[t].scrollbar,
        o = "y" === t ? e.pageY : e.pageX;
      this.axis[t].dragOffset = o - i.rect[this.axis[t].offsetAttr], this.draggedAxis = t, this.el.classList.add(this.classNames.dragging), n.addEventListener("mousemove", this.drag, !0), n.addEventListener("mouseup", this.onEndDrag, !0), null === this.removePreventClickId ? (n.addEventListener("click", this.preventClick, !0), n.addEventListener("dblclick", this.preventClick, !0)) : (r.clearTimeout(this.removePreventClickId), this.removePreventClickId = null)
    }, t.onTrackClick = function(e, t) {
      var n = this;
      if (void 0 === t && (t = "y"), this.options.clickOnTrack) {
        var r = As(this.el);
        this.axis[t].scrollbar.rect = this.axis[t].scrollbar.el.getBoundingClientRect();
        var i = this.axis[t].scrollbar.rect[this.axis[t].offsetAttr],
          o = parseInt(this.elStyles[this.axis[t].sizeAttr], 10),
          a = this.contentWrapperEl[this.axis[t].scrollOffsetAttr],
          s = ("y" === t ? this.mouseY - i : this.mouseX - i) < 0 ? -1 : 1,
          l = -1 === s ? a - o : a + o;
        ! function e() {
          var i, o; - 1 === s ? a > l && (a -= n.options.clickOnTrackSpeed, n.contentWrapperEl.scrollTo(((i = {})[n.axis[t].offsetAttr] = a, i)), r.requestAnimationFrame(e)) : a < l && (a += n.options.clickOnTrackSpeed, n.contentWrapperEl.scrollTo(((o = {})[n.axis[t].offsetAttr] = a, o)), r.requestAnimationFrame(e))
        }()
      }
    }, t.getContentElement = function() {
      return this.contentEl
    }, t.getScrollElement = function() {
      return this.contentWrapperEl
    }, t.getScrollbarWidth = function() {
      try {
        return "none" === getComputedStyle(this.contentWrapperEl, "::-webkit-scrollbar").display || "scrollbarWidth" in document.documentElement.style || "-ms-overflow-style" in document.documentElement.style ? 0 : Is(this.el)
      } catch (e) {
        return Is(this.el)
      }
    }, t.removeListeners = function() {
      var e = this,
        t = As(this.el);
      this.options.autoHide && this.el.removeEventListener("mouseenter", this.onMouseEnter), ["mousedown", "click", "dblclick"].forEach((function(t) {
        e.el.removeEventListener(t, e.onPointerEvent, !0)
      })), ["touchstart", "touchend", "touchmove"].forEach((function(t) {
        e.el.removeEventListener(t, e.onPointerEvent, {
          capture: !0,
          passive: !0
        })
      })), this.el.removeEventListener("mousemove", this.onMouseMove), this.el.removeEventListener("mouseleave", this.onMouseLeave), this.contentWrapperEl && this.contentWrapperEl.removeEventListener("scroll", this.onScroll), t.removeEventListener("resize", this.onWindowResize), this.mutationObserver && this.mutationObserver.disconnect(), this.resizeObserver && this.resizeObserver.disconnect(), this.recalculate.cancel(), this.onMouseMove.cancel(), this.hideScrollbars.cancel(), this.onWindowResize.cancel()
    }, t.unMount = function() {
      this.removeListeners(), e.instances.delete(this.el)
    }, t.isWithinBounds = function(e) {
      return this.mouseX >= e.left && this.mouseX <= e.left + e.width && this.mouseY >= e.top && this.mouseY <= e.top + e.height
    }, t.findChild = function(e, t) {
      var n = e.matches || e.webkitMatchesSelector || e.mozMatchesSelector || e.msMatchesSelector;
      return Array.prototype.filter.call(e.children, (function(e) {
        return n.call(e, t)
      }))[0]
    }, e
  }();
  return Ps.defaultOptions = {
    autoHide: !0,
    forceVisible: !1,
    clickOnTrack: !0,
    clickOnTrackSpeed: 40,
    classNames: {
      contentEl: "simplebar-content",
      contentWrapper: "simplebar-content-wrapper",
      offset: "simplebar-offset",
      mask: "simplebar-mask",
      wrapper: "simplebar-wrapper",
      placeholder: "simplebar-placeholder",
      scrollbar: "simplebar-scrollbar",
      track: "simplebar-track",
      heightAutoObserverWrapperEl: "simplebar-height-auto-observer-wrapper",
      heightAutoObserverEl: "simplebar-height-auto-observer",
      visible: "simplebar-visible",
      horizontal: "simplebar-horizontal",
      vertical: "simplebar-vertical",
      hover: "simplebar-hover",
      dragging: "simplebar-dragging"
    },
    scrollbarMinSize: 25,
    scrollbarMaxSize: 0,
    timeout: 1e3
  }, Ps.instances = new WeakMap, Ps.initDOMLoadedElements = function() {
    document.removeEventListener("DOMContentLoaded", this.initDOMLoadedElements), window.removeEventListener("load", this.initDOMLoadedElements), Array.prototype.forEach.call(document.querySelectorAll("[data-simplebar]"), (function(e) {
      "init" === e.getAttribute("data-simplebar") || Ps.instances.has(e) || new Ps(e, Os(e.attributes))
    }))
  }, Ps.removeObserver = function() {
    this.globalObserver.disconnect()
  }, Ps.initHtmlApi = function() {
    this.initDOMLoadedElements = this.initDOMLoadedElements.bind(this), "undefined" != typeof MutationObserver && (this.globalObserver = new MutationObserver(Ps.handleMutations), this.globalObserver.observe(document, {
      childList: !0,
      subtree: !0
    })), "complete" === document.readyState || "loading" !== document.readyState && !document.documentElement.doScroll ? window.setTimeout(this.initDOMLoadedElements) : (document.addEventListener("DOMContentLoaded", this.initDOMLoadedElements), window.addEventListener("load", this.initDOMLoadedElements))
  }, Ps.handleMutations = function(e) {
    e.forEach((function(e) {
      Array.prototype.forEach.call(e.addedNodes, (function(e) {
        1 === e.nodeType && (e.hasAttribute("data-simplebar") ? !Ps.instances.has(e) && document.documentElement.contains(e) && new Ps(e, Os(e.attributes)) : Array.prototype.forEach.call(e.querySelectorAll("[data-simplebar]"), (function(e) {
          "init" !== e.getAttribute("data-simplebar") && !Ps.instances.has(e) && document.documentElement.contains(e) && new Ps(e, Os(e.attributes))
        })))
      })), Array.prototype.forEach.call(e.removedNodes, (function(e) {
        1 === e.nodeType && ("init" === e.getAttribute("data-simplebar") ? Ps.instances.has(e) && !document.documentElement.contains(e) && Ps.instances.get(e).unMount() : Array.prototype.forEach.call(e.querySelectorAll('[data-simplebar="init"]'), (function(e) {
          Ps.instances.has(e) && !document.documentElement.contains(e) && Ps.instances.get(e).unMount()
        })))
      }))
    }))
  }, Ps.getOptions = Os, Nt && Ps.initHtmlApi(), Ps
})),
function(e) {
  "function" == typeof define && define.amd ? define(["jquery"], e) : e("object" == typeof exports ? require("jquery") : window.jQuery || window.Zepto)
}((function(e) {
  var t, n, r, i, o, a, s = "Close",
    l = "BeforeClose",
    c = "MarkupParse",
    u = "Open",
    d = "Change",
    p = "mfp",
    f = "." + p,
    h = "mfp-ready",
    m = "mfp-removing",
    g = "mfp-prevent-close",
    v = function() {},
    y = !!window.jQuery,
    b = e(window),
    w = function(e, n) {
      t.ev.on(p + e + f, n)
    },
    x = function(t, n, r, i) {
      var o = document.createElement("div");
      return o.className = "mfp-" + t, r && (o.innerHTML = r), i ? n && n.appendChild(o) : (o = e(o), n && o.appendTo(n)), o
    },
    S = function(n, r) {
      t.ev.triggerHandler(p + n, r), t.st.callbacks && (n = n.charAt(0).toLowerCase() + n.slice(1), t.st.callbacks[n] && t.st.callbacks[n].apply(t, e.isArray(r) ? r : [r]))
    },
    C = function(n) {
      return n === a && t.currTemplate.closeBtn || (t.currTemplate.closeBtn = e(t.st.closeMarkup.replace("%title%", t.st.tClose)), a = n), t.currTemplate.closeBtn
    },
    E = function() {
      e.magnificPopup.instance || ((t = new v).init(), e.magnificPopup.instance = t)
    };
  v.prototype = {
    constructor: v,
    init: function() {
      var n = navigator.appVersion;
      t.isLowIE = t.isIE8 = document.all && !document.addEventListener, t.isAndroid = /android/gi.test(n), t.isIOS = /iphone|ipad|ipod/gi.test(n), t.supportsTransition = function() {
        var e = document.createElement("p").style,
          t = ["ms", "O", "Moz", "Webkit"];
        if (void 0 !== e.transition) return !0;
        for (; t.length;)
          if (t.pop() + "Transition" in e) return !0;
        return !1
      }(), t.probablyMobile = t.isAndroid || t.isIOS || /(Opera Mini)|Kindle|webOS|BlackBerry|(Opera Mobi)|(Windows Phone)|IEMobile/i.test(navigator.userAgent), r = e(document), t.popupsCache = {}
    },
    open: function(n) {
      var i;
      if (!1 === n.isObj) {
        t.items = n.items.toArray(), t.index = 0;
        var a, s = n.items;
        for (i = 0; i < s.length; i++)
          if ((a = s[i]).parsed && (a = a.el[0]), a === n.el[0]) {
            t.index = i;
            break
          }
      } else t.items = e.isArray(n.items) ? n.items : [n.items], t.index = n.index || 0;
      if (!t.isOpen) {
        t.types = [], o = "", n.mainEl && n.mainEl.length ? t.ev = n.mainEl.eq(0) : t.ev = r, n.key ? (t.popupsCache[n.key] || (t.popupsCache[n.key] = {}), t.currTemplate = t.popupsCache[n.key]) : t.currTemplate = {}, t.st = e.extend(!0, {}, e.magnificPopup.defaults, n), t.fixedContentPos = "auto" === t.st.fixedContentPos ? !t.probablyMobile : t.st.fixedContentPos, t.st.modal && (t.st.closeOnContentClick = !1, t.st.closeOnBgClick = !1, t.st.showCloseBtn = !1, t.st.enableEscapeKey = !1), t.bgOverlay || (t.bgOverlay = x("bg").on("click" + f, (function() {
          t.close()
        })), t.wrap = x("wrap").attr("tabindex", -1).on("click" + f, (function(e) {
          t._checkIfClose(e.target) && t.close()
        })), t.container = x("container", t.wrap)), t.contentContainer = x("content"), t.st.preloader && (t.preloader = x("preloader", t.container, t.st.tLoading));
        var l = e.magnificPopup.modules;
        for (i = 0; i < l.length; i++) {
          var d = l[i];
          d = d.charAt(0).toUpperCase() + d.slice(1), t["init" + d].call(t)
        }
        S("BeforeOpen"), t.st.showCloseBtn && (t.st.closeBtnInside ? (w(c, (function(e, t, n, r) {
          n.close_replaceWith = C(r.type)
        })), o += " mfp-close-btn-in") : t.wrap.append(C())), t.st.alignTop && (o += " mfp-align-top"), t.fixedContentPos ? t.wrap.css({
          overflow: t.st.overflowY,
          overflowX: "hidden",
          overflowY: t.st.overflowY
        }) : t.wrap.css({
          top: b.scrollTop(),
          position: "absolute"
        }), (!1 === t.st.fixedBgPos || "auto" === t.st.fixedBgPos && !t.fixedContentPos) && t.bgOverlay.css({
          height: r.height(),
          position: "absolute"
        }), t.st.enableEscapeKey && r.on("keyup" + f, (function(e) {
          27 === e.keyCode && t.close()
        })), b.on("resize" + f, (function() {
          t.updateSize()
        })), t.st.closeOnContentClick || (o += " mfp-auto-cursor"), o && t.wrap.addClass(o);
        var p = t.wH = b.height(),
          m = {};
        if (t.fixedContentPos && t._hasScrollBar(p)) {
          var g = t._getScrollbarSize();
          g && (m.marginRight = g)
        }
        t.fixedContentPos && (t.isIE7 ? e("body, html").css("overflow", "hidden") : m.overflow = "hidden");
        var v = t.st.mainClass;
        return t.isIE7 && (v += " mfp-ie7"), v && t._addClassToMFP(v), t.updateItemHTML(), S("BuildControls"), e("html").css(m), t.bgOverlay.add(t.wrap).prependTo(t.st.prependTo || e(document.body)), t._lastFocusedEl = document.activeElement, setTimeout((function() {
          t.content ? (t._addClassToMFP(h), t._setFocus()) : t.bgOverlay.addClass(h), r.on("focusin" + f, t._onFocusIn)
        }), 16), t.isOpen = !0, t.updateSize(p), S(u), n
      }
      t.updateItemHTML()
    },
    close: function() {
      t.isOpen && (S(l), t.isOpen = !1, t.st.removalDelay && !t.isLowIE && t.supportsTransition ? (t._addClassToMFP(m), setTimeout((function() {
        t._close()
      }), t.st.removalDelay)) : t._close())
    },
    _close: function() {
      S(s);
      var n = m + " " + h + " ";
      if (t.bgOverlay.detach(), t.wrap.detach(), t.container.empty(), t.st.mainClass && (n += t.st.mainClass + " "), t._removeClassFromMFP(n), t.fixedContentPos) {
        var i = {
          marginRight: ""
        };
        t.isIE7 ? e("body, html").css("overflow", "") : i.overflow = "", e("html").css(i)
      }
      r.off("keyup.mfp focusin" + f), t.ev.off(f), t.wrap.attr("class", "mfp-wrap").removeAttr("style"), t.bgOverlay.attr("class", "mfp-bg"), t.container.attr("class", "mfp-container"), !t.st.showCloseBtn || t.st.closeBtnInside && !0 !== t.currTemplate[t.currItem.type] || t.currTemplate.closeBtn && t.currTemplate.closeBtn.detach(), t.st.autoFocusLast && t._lastFocusedEl && e(t._lastFocusedEl).focus(), t.currItem = null, t.content = null, t.currTemplate = null, t.prevHeight = 0, S("AfterClose")
    },
    updateSize: function(e) {
      if (t.isIOS) {
        var n = document.documentElement.clientWidth / window.innerWidth,
          r = window.innerHeight * n;
        t.wrap.css("height", r), t.wH = r
      } else t.wH = e || b.height();
      t.fixedContentPos || t.wrap.css("height", t.wH), S("Resize")
    },
    updateItemHTML: function() {
      var n = t.items[t.index];
      t.contentContainer.detach(), t.content && t.content.detach(), n.parsed || (n = t.parseEl(t.index));
      var r = n.type;
      if (S("BeforeChange", [t.currItem ? t.currItem.type : "", r]), t.currItem = n, !t.currTemplate[r]) {
        var o = !!t.st[r] && t.st[r].markup;
        S("FirstMarkupParse", o), t.currTemplate[r] = !o || e(o)
      }
      i && i !== n.type && t.container.removeClass("mfp-" + i + "-holder");
      var a = t["get" + r.charAt(0).toUpperCase() + r.slice(1)](n, t.currTemplate[r]);
      t.appendContent(a, r), n.preloaded = !0, S(d, n), i = n.type, t.container.prepend(t.contentContainer), S("AfterChange")
    },
    appendContent: function(e, n) {
      t.content = e, e ? t.st.showCloseBtn && t.st.closeBtnInside && !0 === t.currTemplate[n] ? t.content.find(".mfp-close").length || t.content.append(C()) : t.content = e : t.content = "", S("BeforeAppend"), t.container.addClass("mfp-" + n + "-holder"), t.contentContainer.append(t.content)
    },
    parseEl: function(n) {
      var r, i = t.items[n];
      if (i.tagName ? i = {
          el: e(i)
        } : (r = i.type, i = {
          data: i,
          src: i.src
        }), i.el) {
        for (var o = t.types, a = 0; a < o.length; a++)
          if (i.el.hasClass("mfp-" + o[a])) {
            r = o[a];
            break
          } i.src = i.el.attr("data-mfp-src"), i.src || (i.src = i.el.attr("href"))
      }
      return i.type = r || t.st.type || "inline", i.index = n, i.parsed = !0, t.items[n] = i, S("ElementParse", i), t.items[n]
    },
    addGroup: function(e, n) {
      var r = function(r) {
        r.mfpEl = this, t._openClick(r, e, n)
      };
      n || (n = {});
      var i = "click.magnificPopup";
      n.mainEl = e, n.items ? (n.isObj = !0, e.off(i).on(i, r)) : (n.isObj = !1, n.delegate ? e.off(i).on(i, n.delegate, r) : (n.items = e, e.off(i).on(i, r)))
    },
    _openClick: function(n, r, i) {
      if ((void 0 !== i.midClick ? i.midClick : e.magnificPopup.defaults.midClick) || !(2 === n.which || n.ctrlKey || n.metaKey || n.altKey || n.shiftKey)) {
        var o = void 0 !== i.disableOn ? i.disableOn : e.magnificPopup.defaults.disableOn;
        if (o)
          if (e.isFunction(o)) {
            if (!o.call(t)) return !0
          } else if (b.width() < o) return !0;
        n.type && (n.preventDefault(), t.isOpen && n.stopPropagation()), i.el = e(n.mfpEl), i.delegate && (i.items = r.find(i.delegate)), t.open(i)
      }
    },
    updateStatus: function(e, r) {
      if (t.preloader) {
        n !== e && t.container.removeClass("mfp-s-" + n), r || "loading" !== e || (r = t.st.tLoading);
        var i = {
          status: e,
          text: r
        };
        S("UpdateStatus", i), e = i.status, r = i.text, t.preloader.html(r), t.preloader.find("a").on("click", (function(e) {
          e.stopImmediatePropagation()
        })), t.container.addClass("mfp-s-" + e), n = e
      }
    },
    _checkIfClose: function(n) {
      if (!e(n).hasClass(g)) {
        var r = t.st.closeOnContentClick,
          i = t.st.closeOnBgClick;
        if (r && i) return !0;
        if (!t.content || e(n).hasClass("mfp-close") || t.preloader && n === t.preloader[0]) return !0;
        if (n === t.content[0] || e.contains(t.content[0], n)) {
          if (r) return !0
        } else if (i && e.contains(document, n)) return !0;
        return !1
      }
    },
    _addClassToMFP: function(e) {
      t.bgOverlay.addClass(e), t.wrap.addClass(e)
    },
    _removeClassFromMFP: function(e) {
      this.bgOverlay.removeClass(e), t.wrap.removeClass(e)
    },
    _hasScrollBar: function(e) {
      return (t.isIE7 ? r.height() : document.body.scrollHeight) > (e || b.height())
    },
    _setFocus: function() {
      (t.st.focus ? t.content.find(t.st.focus).eq(0) : t.wrap).focus()
    },
    _onFocusIn: function(n) {
      return n.target === t.wrap[0] || e.contains(t.wrap[0], n.target) ? void 0 : (t._setFocus(), !1)
    },
    _parseMarkup: function(t, n, r) {
      var i;
      r.data && (n = e.extend(r.data, n)), S(c, [t, n, r]), e.each(n, (function(n, r) {
        if (void 0 === r || !1 === r) return !0;
        if ((i = n.split("_")).length > 1) {
          var o = t.find(f + "-" + i[0]);
          if (o.length > 0) {
            var a = i[1];
            "replaceWith" === a ? o[0] !== r[0] && o.replaceWith(r) : "img" === a ? o.is("img") ? o.attr("src", r) : o.replaceWith(e("<img>").attr("src", r).attr("class", o.attr("class"))) : o.attr(i[1], r)
          }
        } else t.find(f + "-" + n).html(r)
      }))
    },
    _getScrollbarSize: function() {
      if (void 0 === t.scrollbarSize) {
        var e = document.createElement("div");
        e.style.cssText = "width: 99px; height: 99px; overflow: scroll; position: absolute; top: -9999px;", document.body.appendChild(e), t.scrollbarSize = e.offsetWidth - e.clientWidth, document.body.removeChild(e)
      }
      return t.scrollbarSize
    }
  }, e.magnificPopup = {
    instance: null,
    proto: v.prototype,
    modules: [],
    open: function(t, n) {
      return E(), (t = t ? e.extend(!0, {}, t) : {}).isObj = !0, t.index = n || 0, this.instance.open(t)
    },
    close: function() {
      return e.magnificPopup.instance && e.magnificPopup.instance.close()
    },
    registerModule: function(t, n) {
      n.options && (e.magnificPopup.defaults[t] = n.options), e.extend(this.proto, n.proto), this.modules.push(t)
    },
    defaults: {
      disableOn: 0,
      key: null,
      midClick: !1,
      mainClass: "",
      preloader: !0,
      focus: "",
      closeOnContentClick: !1,
      closeOnBgClick: !0,
      closeBtnInside: !0,
      showCloseBtn: !0,
      enableEscapeKey: !0,
      modal: !1,
      alignTop: !1,
      removalDelay: 0,
      prependTo: null,
      fixedContentPos: "auto",
      fixedBgPos: "auto",
      overflowY: "auto",
      closeMarkup: '<button title="%title%" type="button" class="mfp-close">&#215;</button>',
      tClose: "Close (Esc)",
      tLoading: "Loading...",
      autoFocusLast: !0
    }
  }, e.fn.magnificPopup = function(n) {
    E();
    var r = e(this);
    if ("string" == typeof n)
      if ("open" === n) {
        var i, o = y ? r.data("magnificPopup") : r[0].magnificPopup,
          a = parseInt(arguments[1], 10) || 0;
        o.items ? i = o.items[a] : (i = r, o.delegate && (i = i.find(o.delegate)), i = i.eq(a)), t._openClick({
          mfpEl: i
        }, r, o)
      } else t.isOpen && t[n].apply(t, Array.prototype.slice.call(arguments, 1));
    else n = e.extend(!0, {}, n), y ? r.data("magnificPopup", n) : r[0].magnificPopup = n, t.addGroup(r, n);
    return r
  };
  var T, k, D, O = "inline",
    A = function() {
      D && (k.after(D.addClass(T)).detach(), D = null)
    };
  e.magnificPopup.registerModule(O, {
    options: {
      hiddenClass: "hide",
      markup: "",
      tNotFound: "Content not found"
    },
    proto: {
      initInline: function() {
        t.types.push(O), w(s + "." + O, (function() {
          A()
        }))
      },
      getInline: function(n, r) {
        if (A(), n.src) {
          var i = t.st.inline,
            o = e(n.src);
          if (o.length) {
            var a = o[0].parentNode;
            a && a.tagName && (k || (T = i.hiddenClass, k = x(T), T = "mfp-" + T), D = o.after(k).detach().removeClass(T)), t.updateStatus("ready")
          } else t.updateStatus("error", i.tNotFound), o = e("<div>");
          return n.inlineElement = o, o
        }
        return t.updateStatus("ready"), t._parseMarkup(r, {}, n), r
      }
    }
  });
  var _, M = "ajax",
    L = function() {
      _ && e(document.body).removeClass(_)
    },
    I = function() {
      L(), t.req && t.req.abort()
    };
  e.magnificPopup.registerModule(M, {
    options: {
      settings: null,
      cursor: "mfp-ajax-cur",
      tError: '<a href="%url%">The content</a> could not be loaded.'
    },
    proto: {
      initAjax: function() {
        t.types.push(M), _ = t.st.ajax.cursor, w(s + "." + M, I), w("BeforeChange." + M, I)
      },
      getAjax: function(n) {
        _ && e(document.body).addClass(_), t.updateStatus("loading");
        var r = e.extend({
          url: n.src,
          success: function(r, i, o) {
            var a = {
              data: r,
              xhr: o
            };
            S("ParseAjax", a), t.appendContent(e(a.data), M), n.finished = !0, L(), t._setFocus(), setTimeout((function() {
              t.wrap.addClass(h)
            }), 16), t.updateStatus("ready"), S("AjaxContentAdded")
          },
          error: function() {
            L(), n.finished = n.loadError = !0, t.updateStatus("error", t.st.ajax.tError.replace("%url%", n.src))
          }
        }, t.st.ajax.settings);
        return t.req = e.ajax(r), ""
      }
    }
  });
  var P, j = function(n) {
    if (n.data && void 0 !== n.data.title) return n.data.title;
    var r = t.st.image.titleSrc;
    if (r) {
      if (e.isFunction(r)) return r.call(t, n);
      if (n.el) return n.el.attr(r) || ""
    }
    return ""
  };
  e.magnificPopup.registerModule("image", {
    options: {
      markup: '<div class="mfp-figure"><div class="mfp-close"></div><figure><div class="mfp-img"></div><figcaption><div class="mfp-bottom-bar"><div class="mfp-title"></div><div class="mfp-counter"></div></div></figcaption></figure></div>',
      cursor: "mfp-zoom-out-cur",
      titleSrc: "title",
      verticalFit: !0,
      tError: '<a href="%url%">The image</a> could not be loaded.'
    },
    proto: {
      initImage: function() {
        var n = t.st.image,
          r = ".image";
        t.types.push("image"), w(u + r, (function() {
          "image" === t.currItem.type && n.cursor && e(document.body).addClass(n.cursor)
        })), w(s + r, (function() {
          n.cursor && e(document.body).removeClass(n.cursor), b.off("resize" + f)
        })), w("Resize" + r, t.resizeImage), t.isLowIE && w("AfterChange", t.resizeImage)
      },
      resizeImage: function() {
        var e = t.currItem;
        if (e && e.img && t.st.image.verticalFit) {
          var n = 0;
          t.isLowIE && (n = parseInt(e.img.css("padding-top"), 10) + parseInt(e.img.css("padding-bottom"), 10)), e.img.css("max-height", t.wH - n)
        }
      },
      _onImageHasSize: function(e) {
        e.img && (e.hasSize = !0, P && clearInterval(P), e.isCheckingImgSize = !1, S("ImageHasSize", e), e.imgHidden && (t.content && t.content.removeClass("mfp-loading"), e.imgHidden = !1))
      },
      findImageSize: function(e) {
        var n = 0,
          r = e.img[0],
          i = function(o) {
            P && clearInterval(P), P = setInterval((function() {
              return r.naturalWidth > 0 ? void t._onImageHasSize(e) : (n > 200 && clearInterval(P), void(3 === ++n ? i(10) : 40 === n ? i(50) : 100 === n && i(500)))
            }), o)
          };
        i(1)
      },
      getImage: function(n, r) {
        var i = 0,
          o = function() {
            n && (n.img[0].complete ? (n.img.off(".mfploader"), n === t.currItem && (t._onImageHasSize(n), t.updateStatus("ready")), n.hasSize = !0, n.loaded = !0, S("ImageLoadComplete")) : 200 > ++i ? setTimeout(o, 100) : a())
          },
          a = function() {
            n && (n.img.off(".mfploader"), n === t.currItem && (t._onImageHasSize(n), t.updateStatus("error", s.tError.replace("%url%", n.src))), n.hasSize = !0, n.loaded = !0, n.loadError = !0)
          },
          s = t.st.image,
          l = r.find(".mfp-img");
        if (l.length) {
          var c = document.createElement("img");
          c.className = "mfp-img", n.el && n.el.find("img").length && (c.alt = n.el.find("img").attr("alt")), n.img = e(c).on("load.mfploader", o).on("error.mfploader", a), c.src = n.src, l.is("img") && (n.img = n.img.clone()), (c = n.img[0]).naturalWidth > 0 ? n.hasSize = !0 : c.width || (n.hasSize = !1)
        }
        return t._parseMarkup(r, {
          title: j(n),
          img_replaceWith: n.img
        }, n), t.resizeImage(), n.hasSize ? (P && clearInterval(P), n.loadError ? (r.addClass("mfp-loading"), t.updateStatus("error", s.tError.replace("%url%", n.src))) : (r.removeClass("mfp-loading"), t.updateStatus("ready")), r) : (t.updateStatus("loading"), n.loading = !0, n.hasSize || (n.imgHidden = !0, r.addClass("mfp-loading"), t.findImageSize(n)), r)
      }
    }
  });
  var N;
  e.magnificPopup.registerModule("zoom", {
    options: {
      enabled: !1,
      easing: "ease-in-out",
      duration: 300,
      opener: function(e) {
        return e.is("img") ? e : e.find("img")
      }
    },
    proto: {
      initZoom: function() {
        var e, n = t.st.zoom,
          r = ".zoom";
        if (n.enabled && t.supportsTransition) {
          var i, o, a = n.duration,
            c = function(e) {
              var t = e.clone().removeAttr("style").removeAttr("class").addClass("mfp-animated-image"),
                r = "all " + n.duration / 1e3 + "s " + n.easing,
                i = {
                  position: "fixed",
                  zIndex: 9999,
                  left: 0,
                  top: 0,
                  "-webkit-backface-visibility": "hidden"
                },
                o = "transition";
              return i["-webkit-" + o] = i["-moz-" + o] = i["-o-" + o] = i[o] = r, t.css(i), t
            },
            u = function() {
              t.content.css("visibility", "visible")
            };
          w("BuildControls" + r, (function() {
            if (t._allowZoom()) {
              if (clearTimeout(i), t.content.css("visibility", "hidden"), !(e = t._getItemToZoom())) return void u();
              (o = c(e)).css(t._getOffset()), t.wrap.append(o), i = setTimeout((function() {
                o.css(t._getOffset(!0)), i = setTimeout((function() {
                  u(), setTimeout((function() {
                    o.remove(), e = o = null, S("ZoomAnimationEnded")
                  }), 16)
                }), a)
              }), 16)
            }
          })), w(l + r, (function() {
            if (t._allowZoom()) {
              if (clearTimeout(i), t.st.removalDelay = a, !e) {
                if (!(e = t._getItemToZoom())) return;
                o = c(e)
              }
              o.css(t._getOffset(!0)), t.wrap.append(o), t.content.css("visibility", "hidden"), setTimeout((function() {
                o.css(t._getOffset())
              }), 16)
            }
          })), w(s + r, (function() {
            t._allowZoom() && (u(), o && o.remove(), e = null)
          }))
        }
      },
      _allowZoom: function() {
        return "image" === t.currItem.type
      },
      _getItemToZoom: function() {
        return !!t.currItem.hasSize && t.currItem.img
      },
      _getOffset: function(n) {
        var r, i = (r = n ? t.currItem.img : t.st.zoom.opener(t.currItem.el || t.currItem)).offset(),
          o = parseInt(r.css("padding-top"), 10),
          a = parseInt(r.css("padding-bottom"), 10);
        i.top -= e(window).scrollTop() - o;
        var s = {
          width: r.width(),
          height: (y ? r.innerHeight() : r[0].offsetHeight) - a - o
        };
        return void 0 === N && (N = void 0 !== document.createElement("p").style.MozTransform), N ? s["-moz-transform"] = s.transform = "translate(" + i.left + "px," + i.top + "px)" : (s.left = i.left, s.top = i.top), s
      }
    }
  });
  var z = "iframe",
    R = function(e) {
      if (t.currTemplate[z]) {
        var n = t.currTemplate[z].find("iframe");
        n.length && (e || (n[0].src = "//about:blank"), t.isIE8 && n.css("display", e ? "block" : "none"))
      }
    };
  e.magnificPopup.registerModule(z, {
    options: {
      markup: '<div class="mfp-iframe-scaler"><div class="mfp-close"></div><iframe class="mfp-iframe" src="//about:blank" frameborder="0" allowfullscreen></iframe></div>',
      srcAction: "iframe_src",
      patterns: {
        youtube: {
          index: "youtube.com",
          id: "v=",
          src: "//www.youtube.com/embed/%id%?autoplay=1"
        },
        vimeo: {
          index: "vimeo.com/",
          id: "/",
          src: "//player.vimeo.com/video/%id%?autoplay=1"
        },
        gmaps: {
          index: "//maps.google.",
          src: "%id%&output=embed"
        }
      }
    },
    proto: {
      initIframe: function() {
        t.types.push(z), w("BeforeChange", (function(e, t, n) {
          t !== n && (t === z ? R() : n === z && R(!0))
        })), w(s + "." + z, (function() {
          R()
        }))
      },
      getIframe: function(n, r) {
        var i = n.src,
          o = t.st.iframe;
        e.each(o.patterns, (function() {
          return i.indexOf(this.index) > -1 ? (this.id && (i = "string" == typeof this.id ? i.substr(i.lastIndexOf(this.id) + this.id.length, i.length) : this.id.call(this, i)), i = this.src.replace("%id%", i), !1) : void 0
        }));
        var a = {};
        return o.srcAction && (a[o.srcAction] = i), t._parseMarkup(r, a, n), t.updateStatus("ready"), r
      }
    }
  });
  var $ = function(e) {
      var n = t.items.length;
      return e > n - 1 ? e - n : 0 > e ? n + e : e
    },
    H = function(e, t, n) {
      return e.replace(/%curr%/gi, t + 1).replace(/%total%/gi, n)
    };
  e.magnificPopup.registerModule("gallery", {
    options: {
      enabled: !1,
      arrowMarkup: '<button title="%title%" type="button" class="mfp-arrow mfp-arrow-%dir%"></button>',
      preload: [0, 2],
      navigateByImgClick: !0,
      arrows: !0,
      tPrev: "Previous (Left arrow key)",
      tNext: "Next (Right arrow key)",
      tCounter: "%curr% of %total%"
    },
    proto: {
      initGallery: function() {
        var n = t.st.gallery,
          i = ".mfp-gallery";
        return t.direction = !0, !(!n || !n.enabled) && (o += " mfp-gallery", w(u + i, (function() {
          n.navigateByImgClick && t.wrap.on("click" + i, ".mfp-img", (function() {
            return t.items.length > 1 ? (t.next(), !1) : void 0
          })), r.on("keydown" + i, (function(e) {
            37 === e.keyCode ? t.prev() : 39 === e.keyCode && t.next()
          }))
        })), w("UpdateStatus" + i, (function(e, n) {
          n.text && (n.text = H(n.text, t.currItem.index, t.items.length))
        })), w(c + i, (function(e, r, i, o) {
          var a = t.items.length;
          i.counter = a > 1 ? H(n.tCounter, o.index, a) : ""
        })), w("BuildControls" + i, (function() {
          if (t.items.length > 1 && n.arrows && !t.arrowLeft) {
            var r = n.arrowMarkup,
              i = t.arrowLeft = e(r.replace(/%title%/gi, n.tPrev).replace(/%dir%/gi, "left")).addClass(g),
              o = t.arrowRight = e(r.replace(/%title%/gi, n.tNext).replace(/%dir%/gi, "right")).addClass(g);
            i.click((function() {
              t.prev()
            })), o.click((function() {
              t.next()
            })), t.container.append(i.add(o))
          }
        })), w(d + i, (function() {
          t._preloadTimeout && clearTimeout(t._preloadTimeout), t._preloadTimeout = setTimeout((function() {
            t.preloadNearbyImages(), t._preloadTimeout = null
          }), 16)
        })), void w(s + i, (function() {
          r.off(i), t.wrap.off("click" + i), t.arrowRight = t.arrowLeft = null
        })))
      },
      next: function() {
        t.direction = !0, t.index = $(t.index + 1), t.updateItemHTML()
      },
      prev: function() {
        t.direction = !1, t.index = $(t.index - 1), t.updateItemHTML()
      },
      goTo: function(e) {
        t.direction = e >= t.index, t.index = e, t.updateItemHTML()
      },
      preloadNearbyImages: function() {
        var e, n = t.st.gallery.preload,
          r = Math.min(n[0], t.items.length),
          i = Math.min(n[1], t.items.length);
        for (e = 1; e <= (t.direction ? i : r); e++) t._preloadItem(t.index + e);
        for (e = 1; e <= (t.direction ? r : i); e++) t._preloadItem(t.index - e)
      },
      _preloadItem: function(n) {
        if (n = $(n), !t.items[n].preloaded) {
          var r = t.items[n];
          r.parsed || (r = t.parseEl(n)), S("LazyLoad", r), "image" === r.type && (r.img = e('<img class="mfp-img" />').on("load.mfploader", (function() {
            r.hasSize = !0
          })).on("error.mfploader", (function() {
            r.hasSize = !0, r.loadError = !0, S("LazyLoadError", r)
          })).attr("src", r.src)), r.preloaded = !0
        }
      }
    }
  });
  var F = "retina";
  e.magnificPopup.registerModule(F, {
    options: {
      replaceSrc: function(e) {
        return e.src.replace(/\.\w+$/, (function(e) {
          return "@2x" + e
        }))
      },
      ratio: 1
    },
    proto: {
      initRetina: function() {
        if (window.devicePixelRatio > 1) {
          var e = t.st.retina,
            n = e.ratio;
          (n = isNaN(n) ? n() : n) > 1 && (w("ImageHasSize." + F, (function(e, t) {
            t.img.css({
              "max-width": t.img[0].naturalWidth / n,
              width: "100%"
            })
          })), w("ElementParse." + F, (function(t, r) {
            r.src = e.replaceSrc(r, n)
          })))
        }
      }
    }
  }), E()
})),
function(e, t) {
  "object" == typeof exports && "undefined" != typeof module ? module.exports = t() : "function" == typeof define && define.amd ? define(t) : (e = "undefined" != typeof globalThis ? globalThis : e || self).flatpickr = t()
}(this, (function() {
  "use strict";
  var e = function() {
    return (e = Object.assign || function(e) {
      for (var t, n = 1, r = arguments.length; n < r; n++)
        for (var i in t = arguments[n]) Object.prototype.hasOwnProperty.call(t, i) && (e[i] = t[i]);
      return e
    }).apply(this, arguments)
  };

  function t() {
    for (var e = 0, t = 0, n = arguments.length; t < n; t++) e += arguments[t].length;
    var r = Array(e),
      i = 0;
    for (t = 0; t < n; t++)
      for (var o = arguments[t], a = 0, s = o.length; a < s; a++, i++) r[i] = o[a];
    return r
  }
  var n = ["onChange", "onClose", "onDayCreate", "onDestroy", "onKeyDown", "onMonthChange", "onOpen", "onParseConfig", "onReady", "onValueUpdate", "onYearChange", "onPreCalendarPosition"],
    r = {
      _disable: [],
      allowInput: !1,
      allowInvalidPreload: !1,
      altFormat: "F j, Y",
      altInput: !1,
      altInputClass: "form-control input",
      animate: "object" == typeof window && -1 === window.navigator.userAgent.indexOf("MSIE"),
      ariaDateFormat: "F j, Y",
      autoFillDefaultTime: !0,
      clickOpens: !0,
      closeOnSelect: !0,
      conjunction: ", ",
      dateFormat: "Y-m-d",
      defaultHour: 12,
      defaultMinute: 0,
      defaultSeconds: 0,
      disable: [],
      disableMobile: !1,
      enableSeconds: !1,
      enableTime: !1,
      errorHandler: function(e) {
        return "undefined" != typeof console && console.warn(e)
      },
      getWeek: function(e) {
        var t = new Date(e.getTime());
        t.setHours(0, 0, 0, 0), t.setDate(t.getDate() + 3 - (t.getDay() + 6) % 7);
        var n = new Date(t.getFullYear(), 0, 4);
        return 1 + Math.round(((t.getTime() - n.getTime()) / 864e5 - 3 + (n.getDay() + 6) % 7) / 7)
      },
      hourIncrement: 1,
      ignoredFocusElements: [],
      inline: !1,
      locale: "default",
      minuteIncrement: 5,
      mode: "single",
      monthSelectorType: "dropdown",
      nextArrow: "<svg version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' viewBox='0 0 17 17'><g></g><path d='M13.207 8.472l-7.854 7.854-0.707-0.707 7.146-7.146-7.146-7.148 0.707-0.707 7.854 7.854z' /></svg>",
      noCalendar: !1,
      now: new Date,
      onChange: [],
      onClose: [],
      onDayCreate: [],
      onDestroy: [],
      onKeyDown: [],
      onMonthChange: [],
      onOpen: [],
      onParseConfig: [],
      onReady: [],
      onValueUpdate: [],
      onYearChange: [],
      onPreCalendarPosition: [],
      plugins: [],
      position: "auto",
      positionElement: void 0,
      prevArrow: "<svg version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' viewBox='0 0 17 17'><g></g><path d='M5.207 8.471l7.146 7.147-0.707 0.707-7.853-7.854 7.854-7.853 0.707 0.707-7.147 7.146z' /></svg>",
      shorthandCurrentMonth: !1,
      showMonths: 1,
      static: !1,
      time_24hr: !1,
      weekNumbers: !1,
      wrap: !1
    },
    i = {
      weekdays: {
        shorthand: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
        longhand: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
      },
      months: {
        shorthand: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        longhand: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
      },
      daysInMonth: [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
      firstDayOfWeek: 0,
      ordinal: function(e) {
        var t = e % 100;
        if (t > 3 && t < 21) return "th";
        switch (t % 10) {
          case 1:
            return "st";
          case 2:
            return "nd";
          case 3:
            return "rd";
          default:
            return "th"
        }
      },
      rangeSeparator: " to ",
      weekAbbreviation: "Wk",
      scrollTitle: "Scroll to increment",
      toggleTitle: "Click to toggle",
      amPM: ["AM", "PM"],
      yearAriaLabel: "Year",
      monthAriaLabel: "Month",
      hourAriaLabel: "Hour",
      minuteAriaLabel: "Minute",
      time_24hr: !1
    },
    o = function(e, t) {
      return void 0 === t && (t = 2), ("000" + e).slice(-1 * t)
    },
    a = function(e) {
      return !0 === e ? 1 : 0
    };

  function s(e, t) {
    var n;
    return function() {
      var r = this,
        i = arguments;
      clearTimeout(n), n = setTimeout((function() {
        return e.apply(r, i)
      }), t)
    }
  }
  var l = function(e) {
    return e instanceof Array ? e : [e]
  };

  function c(e, t, n) {
    if (!0 === n) return e.classList.add(t);
    e.classList.remove(t)
  }

  function u(e, t, n) {
    var r = window.document.createElement(e);
    return t = t || "", n = n || "", r.className = t, void 0 !== n && (r.textContent = n), r
  }

  function d(e) {
    for (; e.firstChild;) e.removeChild(e.firstChild)
  }

  function p(e, t) {
    return t(e) ? e : e.parentNode ? p(e.parentNode, t) : void 0
  }

  function f(e, t) {
    var n = u("div", "numInputWrapper"),
      r = u("input", "numInput " + e),
      i = u("span", "arrowUp"),
      o = u("span", "arrowDown");
    if (-1 === navigator.userAgent.indexOf("MSIE 9.0") ? r.type = "number" : (r.type = "text", r.pattern = "\\d*"), void 0 !== t)
      for (var a in t) r.setAttribute(a, t[a]);
    return n.appendChild(r), n.appendChild(i), n.appendChild(o), n
  }

  function h(e) {
    try {
      return "function" == typeof e.composedPath ? e.composedPath()[0] : e.target
    } catch (t) {
      return e.target
    }
  }
  var m = function() {},
    g = function(e, t, n) {
      return n.months[t ? "shorthand" : "longhand"][e]
    },
    v = {
      D: m,
      F: function(e, t, n) {
        e.setMonth(n.months.longhand.indexOf(t))
      },
      G: function(e, t) {
        e.setHours((e.getHours() >= 12 ? 12 : 0) + parseFloat(t))
      },
      H: function(e, t) {
        e.setHours(parseFloat(t))
      },
      J: function(e, t) {
        e.setDate(parseFloat(t))
      },
      K: function(e, t, n) {
        e.setHours(e.getHours() % 12 + 12 * a(new RegExp(n.amPM[1], "i").test(t)))
      },
      M: function(e, t, n) {
        e.setMonth(n.months.shorthand.indexOf(t))
      },
      S: function(e, t) {
        e.setSeconds(parseFloat(t))
      },
      U: function(e, t) {
        return new Date(1e3 * parseFloat(t))
      },
      W: function(e, t, n) {
        var r = parseInt(t),
          i = new Date(e.getFullYear(), 0, 2 + 7 * (r - 1), 0, 0, 0, 0);
        return i.setDate(i.getDate() - i.getDay() + n.firstDayOfWeek), i
      },
      Y: function(e, t) {
        e.setFullYear(parseFloat(t))
      },
      Z: function(e, t) {
        return new Date(t)
      },
      d: function(e, t) {
        e.setDate(parseFloat(t))
      },
      h: function(e, t) {
        e.setHours((e.getHours() >= 12 ? 12 : 0) + parseFloat(t))
      },
      i: function(e, t) {
        e.setMinutes(parseFloat(t))
      },
      j: function(e, t) {
        e.setDate(parseFloat(t))
      },
      l: m,
      m: function(e, t) {
        e.setMonth(parseFloat(t) - 1)
      },
      n: function(e, t) {
        e.setMonth(parseFloat(t) - 1)
      },
      s: function(e, t) {
        e.setSeconds(parseFloat(t))
      },
      u: function(e, t) {
        return new Date(parseFloat(t))
      },
      w: m,
      y: function(e, t) {
        e.setFullYear(2e3 + parseFloat(t))
      }
    },
    y = {
      D: "",
      F: "",
      G: "(\\d\\d|\\d)",
      H: "(\\d\\d|\\d)",
      J: "(\\d\\d|\\d)\\w+",
      K: "",
      M: "",
      S: "(\\d\\d|\\d)",
      U: "(.+)",
      W: "(\\d\\d|\\d)",
      Y: "(\\d{4})",
      Z: "(.+)",
      d: "(\\d\\d|\\d)",
      h: "(\\d\\d|\\d)",
      i: "(\\d\\d|\\d)",
      j: "(\\d\\d|\\d)",
      l: "",
      m: "(\\d\\d|\\d)",
      n: "(\\d\\d|\\d)",
      s: "(\\d\\d|\\d)",
      u: "(.+)",
      w: "(\\d\\d|\\d)",
      y: "(\\d{2})"
    },
    b = {
      Z: function(e) {
        return e.toISOString()
      },
      D: function(e, t, n) {
        return t.weekdays.shorthand[b.w(e, t, n)]
      },
      F: function(e, t, n) {
        return g(b.n(e, t, n) - 1, !1, t)
      },
      G: function(e, t, n) {
        return o(b.h(e, t, n))
      },
      H: function(e) {
        return o(e.getHours())
      },
      J: function(e, t) {
        return void 0 !== t.ordinal ? e.getDate() + t.ordinal(e.getDate()) : e.getDate()
      },
      K: function(e, t) {
        return t.amPM[a(e.getHours() > 11)]
      },
      M: function(e, t) {
        return g(e.getMonth(), !0, t)
      },
      S: function(e) {
        return o(e.getSeconds())
      },
      U: function(e) {
        return e.getTime() / 1e3
      },
      W: function(e, t, n) {
        return n.getWeek(e)
      },
      Y: function(e) {
        return o(e.getFullYear(), 4)
      },
      d: function(e) {
        return o(e.getDate())
      },
      h: function(e) {
        return e.getHours() % 12 ? e.getHours() % 12 : 12
      },
      i: function(e) {
        return o(e.getMinutes())
      },
      j: function(e) {
        return e.getDate()
      },
      l: function(e, t) {
        return t.weekdays.longhand[e.getDay()]
      },
      m: function(e) {
        return o(e.getMonth() + 1)
      },
      n: function(e) {
        return e.getMonth() + 1
      },
      s: function(e) {
        return e.getSeconds()
      },
      u: function(e) {
        return e.getTime()
      },
      w: function(e) {
        return e.getDay()
      },
      y: function(e) {
        return String(e.getFullYear()).substring(2)
      }
    },
    w = function(e) {
      var t = e.config,
        n = void 0 === t ? r : t,
        o = e.l10n,
        a = void 0 === o ? i : o,
        s = e.isMobile,
        l = void 0 !== s && s;
      return function(e, t, r) {
        var i = r || a;
        return void 0 === n.formatDate || l ? t.split("").map((function(t, r, o) {
          return b[t] && "\\" !== o[r - 1] ? b[t](e, i, n) : "\\" !== t ? t : ""
        })).join("") : n.formatDate(e, t, i)
      }
    },
    x = function(e) {
      var t = e.config,
        n = void 0 === t ? r : t,
        o = e.l10n,
        a = void 0 === o ? i : o;
      return function(e, t, i, o) {
        if (0 === e || e) {
          var s, l = o || a,
            c = e;
          if (e instanceof Date) s = new Date(e.getTime());
          else if ("string" != typeof e && void 0 !== e.toFixed) s = new Date(e);
          else if ("string" == typeof e) {
            var u = t || (n || r).dateFormat,
              d = String(e).trim();
            if ("today" === d) s = new Date, i = !0;
            else if (n && n.parseDate) s = n.parseDate(e, u);
            else if (/Z$/.test(d) || /GMT$/.test(d)) s = new Date(e);
            else {
              for (var p = void 0, f = [], h = 0, m = 0, g = ""; h < u.length; h++) {
                var b = u[h],
                  w = "\\" === b,
                  x = "\\" === u[h - 1] || w;
                if (y[b] && !x) {
                  g += y[b];
                  var S = new RegExp(g).exec(e);
                  S && (p = !0) && f["Y" !== b ? "push" : "unshift"]({
                    fn: v[b],
                    val: S[++m]
                  })
                } else w || (g += ".")
              }
              s = n && n.noCalendar ? new Date((new Date).setHours(0, 0, 0, 0)) : new Date((new Date).getFullYear(), 0, 1, 0, 0, 0, 0), f.forEach((function(e) {
                var t = e.fn,
                  n = e.val;
                return s = t(s, n, l) || s
              })), s = p ? s : void 0
            }
          }
          if (s instanceof Date && !isNaN(s.getTime())) return !0 === i && s.setHours(0, 0, 0, 0), s;
          n.errorHandler(new Error("Invalid date provided: " + c))
        }
      }
    };

  function S(e, t, n) {
    return void 0 === n && (n = !0), !1 !== n ? new Date(e.getTime()).setHours(0, 0, 0, 0) - new Date(t.getTime()).setHours(0, 0, 0, 0) : e.getTime() - t.getTime()
  }
  var C = function(e, t, n) {
    return 3600 * e + 60 * t + n
  };

  function E(e) {
    var t = e.defaultHour,
      n = e.defaultMinute,
      r = e.defaultSeconds;
    if (void 0 !== e.minDate) {
      var i = e.minDate.getHours(),
        o = e.minDate.getMinutes(),
        a = e.minDate.getSeconds();
      t < i && (t = i), t === i && n < o && (n = o), t === i && n === o && r < a && (r = e.minDate.getSeconds())
    }
    if (void 0 !== e.maxDate) {
      var s = e.maxDate.getHours(),
        l = e.maxDate.getMinutes();
      (t = Math.min(t, s)) === s && (n = Math.min(l, n)), t === s && n === l && (r = e.maxDate.getSeconds())
    }
    return {
      hours: t,
      minutes: n,
      seconds: r
    }
  }

  function T(m, v) {
    var b = {
      config: e(e({}, r), D.defaultConfig),
      l10n: i
    };

    function T() {
      var e;
      return (null === (e = b.calendarContainer) || void 0 === e ? void 0 : e.getRootNode()).activeElement || document.activeElement
    }

    function k(e) {
      return e.bind(b)
    }

    function O() {
      var e = b.config;
      !1 === e.weekNumbers && 1 === e.showMonths || !0 !== e.noCalendar && window.requestAnimationFrame((function() {
        if (void 0 !== b.calendarContainer && (b.calendarContainer.style.visibility = "hidden", b.calendarContainer.style.display = "block"), void 0 !== b.daysContainer) {
          var t = (b.days.offsetWidth + 1) * e.showMonths;
          b.daysContainer.style.width = t + "px", b.calendarContainer.style.width = t + (void 0 !== b.weekWrapper ? b.weekWrapper.offsetWidth : 0) + "px", b.calendarContainer.style.removeProperty("visibility"), b.calendarContainer.style.removeProperty("display")
        }
      }))
    }

    function A(e) {
      if (0 === b.selectedDates.length) {
        var t = void 0 === b.config.minDate || S(new Date, b.config.minDate) >= 0 ? new Date : new Date(b.config.minDate.getTime()),
          n = E(b.config);
        t.setHours(n.hours, n.minutes, n.seconds, t.getMilliseconds()), b.selectedDates = [t], b.latestSelectedDateObj = t
      }
      void 0 !== e && "blur" !== e.type && function(e) {
        e.preventDefault();
        var t = "keydown" === e.type,
          n = h(e),
          r = n;
        void 0 !== b.amPM && n === b.amPM && (b.amPM.textContent = b.l10n.amPM[a(b.amPM.textContent === b.l10n.amPM[0])]);
        var i = parseFloat(r.getAttribute("min")),
          s = parseFloat(r.getAttribute("max")),
          l = parseFloat(r.getAttribute("step")),
          c = parseInt(r.value, 10),
          u = c + l * (e.delta || (t ? 38 === e.which ? 1 : -1 : 0));
        if (void 0 !== r.value && 2 === r.value.length) {
          var d = r === b.hourElement,
            p = r === b.minuteElement;
          u < i ? (u = s + u + a(!d) + (a(d) && a(!b.amPM)), p && R(void 0, -1, b.hourElement)) : u > s && (u = r === b.hourElement ? u - s - a(!b.amPM) : i, p && R(void 0, 1, b.hourElement)), b.amPM && d && (1 === l ? u + c === 23 : Math.abs(u - c) > l) && (b.amPM.textContent = b.l10n.amPM[a(b.amPM.textContent === b.l10n.amPM[0])]), r.value = o(u)
        }
      }(e);
      var r = b._input.value;
      _(), Se(), b._input.value !== r && b._debouncedChange()
    }

    function _() {
      if (void 0 !== b.hourElement && void 0 !== b.minuteElement) {
        var e, t, n = (parseInt(b.hourElement.value.slice(-2), 10) || 0) % 24,
          r = (parseInt(b.minuteElement.value, 10) || 0) % 60,
          i = void 0 !== b.secondElement ? (parseInt(b.secondElement.value, 10) || 0) % 60 : 0;
        void 0 !== b.amPM && (e = n, t = b.amPM.textContent, n = e % 12 + 12 * a(t === b.l10n.amPM[1]));
        var o = void 0 !== b.config.minTime || b.config.minDate && b.minDateHasTime && b.latestSelectedDateObj && 0 === S(b.latestSelectedDateObj, b.config.minDate, !0),
          s = void 0 !== b.config.maxTime || b.config.maxDate && b.maxDateHasTime && b.latestSelectedDateObj && 0 === S(b.latestSelectedDateObj, b.config.maxDate, !0);
        if (void 0 !== b.config.maxTime && void 0 !== b.config.minTime && b.config.minTime > b.config.maxTime) {
          var l = C(b.config.minTime.getHours(), b.config.minTime.getMinutes(), b.config.minTime.getSeconds()),
            c = C(b.config.maxTime.getHours(), b.config.maxTime.getMinutes(), b.config.maxTime.getSeconds()),
            u = C(n, r, i);
          if (u > c && u < l) {
            var d = function(e) {
              var t = Math.floor(e / 3600),
                n = (e - 3600 * t) / 60;
              return [t, n, e - 3600 * t - 60 * n]
            }(l);
            n = d[0], r = d[1], i = d[2]
          }
        } else {
          if (s) {
            var p = void 0 !== b.config.maxTime ? b.config.maxTime : b.config.maxDate;
            (n = Math.min(n, p.getHours())) === p.getHours() && (r = Math.min(r, p.getMinutes())), r === p.getMinutes() && (i = Math.min(i, p.getSeconds()))
          }
          if (o) {
            var f = void 0 !== b.config.minTime ? b.config.minTime : b.config.minDate;
            (n = Math.max(n, f.getHours())) === f.getHours() && r < f.getMinutes() && (r = f.getMinutes()), r === f.getMinutes() && (i = Math.max(i, f.getSeconds()))
          }
        }
        L(n, r, i)
      }
    }

    function M(e) {
      var t = e || b.latestSelectedDateObj;
      t && t instanceof Date && L(t.getHours(), t.getMinutes(), t.getSeconds())
    }

    function L(e, t, n) {
      void 0 !== b.latestSelectedDateObj && b.latestSelectedDateObj.setHours(e % 24, t, n || 0, 0), b.hourElement && b.minuteElement && !b.isMobile && (b.hourElement.value = o(b.config.time_24hr ? e : (12 + e) % 12 + 12 * a(e % 12 == 0)), b.minuteElement.value = o(t), void 0 !== b.amPM && (b.amPM.textContent = b.l10n.amPM[a(e >= 12)]), void 0 !== b.secondElement && (b.secondElement.value = o(n)))
    }

    function I(e) {
      var t = h(e),
        n = parseInt(t.value) + (e.delta || 0);
      (n / 1e3 > 1 || "Enter" === e.key && !/[^\d]/.test(n.toString())) && Q(n)
    }

    function P(e, t, n, r) {
      return t instanceof Array ? t.forEach((function(t) {
        return P(e, t, n, r)
      })) : e instanceof Array ? e.forEach((function(e) {
        return P(e, t, n, r)
      })) : (e.addEventListener(t, n, r), void b._handlers.push({
        remove: function() {
          return e.removeEventListener(t, n, r)
        }
      }))
    }

    function j() {
      ve("onChange")
    }

    function N(e, t) {
      var n = void 0 !== e ? b.parseDate(e) : b.latestSelectedDateObj || (b.config.minDate && b.config.minDate > b.now ? b.config.minDate : b.config.maxDate && b.config.maxDate < b.now ? b.config.maxDate : b.now),
        r = b.currentYear,
        i = b.currentMonth;
      try {
        void 0 !== n && (b.currentYear = n.getFullYear(), b.currentMonth = n.getMonth())
      } catch (e) {
        e.message = "Invalid date supplied: " + n, b.config.errorHandler(e)
      }
      t && b.currentYear !== r && (ve("onYearChange"), Y()), !t || b.currentYear === r && b.currentMonth === i || ve("onMonthChange"), b.redraw()
    }

    function z(e) {
      var t = h(e);
      ~t.className.indexOf("arrow") && R(e, t.classList.contains("arrowUp") ? 1 : -1)
    }

    function R(e, t, n) {
      var r = e && h(e),
        i = n || r && r.parentNode && r.parentNode.firstChild,
        o = ye("increment");
      o.delta = t, i && i.dispatchEvent(o)
    }

    function $(e, t, n, r) {
      var i = ee(t, !0),
        o = u("span", e, t.getDate().toString());
      return o.dateObj = t, o.$i = r, o.setAttribute("aria-label", b.formatDate(t, b.config.ariaDateFormat)), -1 === e.indexOf("hidden") && 0 === S(t, b.now) && (b.todayDateElem = o, o.classList.add("today"), o.setAttribute("aria-current", "date")), i ? (o.tabIndex = -1, be(t) && (o.classList.add("selected"), b.selectedDateElem = o, "range" === b.config.mode && (c(o, "startRange", b.selectedDates[0] && 0 === S(t, b.selectedDates[0], !0)), c(o, "endRange", b.selectedDates[1] && 0 === S(t, b.selectedDates[1], !0)), "nextMonthDay" === e && o.classList.add("inRange")))) : o.classList.add("flatpickr-disabled"), "range" === b.config.mode && function(e) {
        return !("range" !== b.config.mode || b.selectedDates.length < 2) && S(e, b.selectedDates[0]) >= 0 && S(e, b.selectedDates[1]) <= 0
      }(t) && !be(t) && o.classList.add("inRange"), b.weekNumbers && 1 === b.config.showMonths && "prevMonthDay" !== e && r % 7 == 6 && b.weekNumbers.insertAdjacentHTML("beforeend", "<span class='flatpickr-day'>" + b.config.getWeek(t) + "</span>"), ve("onDayCreate", o), o
    }

    function H(e) {
      e.focus(), "range" === b.config.mode && ie(e)
    }

    function F(e) {
      for (var t = e > 0 ? 0 : b.config.showMonths - 1, n = e > 0 ? b.config.showMonths : -1, r = t; r != n; r += e)
        for (var i = b.daysContainer.children[r], o = e > 0 ? 0 : i.children.length - 1, a = e > 0 ? i.children.length : -1, s = o; s != a; s += e) {
          var l = i.children[s];
          if (-1 === l.className.indexOf("hidden") && ee(l.dateObj)) return l
        }
    }

    function B(e, t) {
      var n = T(),
        r = te(n || document.body),
        i = void 0 !== e ? e : r ? n : void 0 !== b.selectedDateElem && te(b.selectedDateElem) ? b.selectedDateElem : void 0 !== b.todayDateElem && te(b.todayDateElem) ? b.todayDateElem : F(t > 0 ? 1 : -1);
      void 0 === i ? b._input.focus() : r ? function(e, t) {
        for (var n = -1 === e.className.indexOf("Month") ? e.dateObj.getMonth() : b.currentMonth, r = t > 0 ? b.config.showMonths : -1, i = t > 0 ? 1 : -1, o = n - b.currentMonth; o != r; o += i)
          for (var a = b.daysContainer.children[o], s = n - b.currentMonth === o ? e.$i + t : t < 0 ? a.children.length - 1 : 0, l = a.children.length, c = s; c >= 0 && c < l && c != (t > 0 ? l : -1); c += i) {
            var u = a.children[c];
            if (-1 === u.className.indexOf("hidden") && ee(u.dateObj) && Math.abs(e.$i - c) >= Math.abs(t)) return H(u)
          }
        b.changeMonth(i), B(F(i), 0)
      }(i, t) : H(i)
    }

    function q(e, t) {
      for (var n = (new Date(e, t, 1).getDay() - b.l10n.firstDayOfWeek + 7) % 7, r = b.utils.getDaysInMonth((t - 1 + 12) % 12, e), i = b.utils.getDaysInMonth(t, e), o = window.document.createDocumentFragment(), a = b.config.showMonths > 1, s = a ? "prevMonthDay hidden" : "prevMonthDay", l = a ? "nextMonthDay hidden" : "nextMonthDay", c = r + 1 - n, d = 0; c <= r; c++, d++) o.appendChild($("flatpickr-day " + s, new Date(e, t - 1, c), 0, d));
      for (c = 1; c <= i; c++, d++) o.appendChild($("flatpickr-day", new Date(e, t, c), 0, d));
      for (var p = i + 1; p <= 42 - n && (1 === b.config.showMonths || d % 7 != 0); p++, d++) o.appendChild($("flatpickr-day " + l, new Date(e, t + 1, p % i), 0, d));
      var f = u("div", "dayContainer");
      return f.appendChild(o), f
    }

    function W() {
      if (void 0 !== b.daysContainer) {
        d(b.daysContainer), b.weekNumbers && d(b.weekNumbers);
        for (var e = document.createDocumentFragment(), t = 0; t < b.config.showMonths; t++) {
          var n = new Date(b.currentYear, b.currentMonth, 1);
          n.setMonth(b.currentMonth + t), e.appendChild(q(n.getFullYear(), n.getMonth()))
        }
        b.daysContainer.appendChild(e), b.days = b.daysContainer.firstChild, "range" === b.config.mode && 1 === b.selectedDates.length && ie()
      }
    }

    function Y() {
      if (!(b.config.showMonths > 1 || "dropdown" !== b.config.monthSelectorType)) {
        var e = function(e) {
          return !(void 0 !== b.config.minDate && b.currentYear === b.config.minDate.getFullYear() && e < b.config.minDate.getMonth() || void 0 !== b.config.maxDate && b.currentYear === b.config.maxDate.getFullYear() && e > b.config.maxDate.getMonth())
        };
        b.monthsDropdownContainer.tabIndex = -1, b.monthsDropdownContainer.innerHTML = "";
        for (var t = 0; t < 12; t++)
          if (e(t)) {
            var n = u("option", "flatpickr-monthDropdown-month");
            n.value = new Date(b.currentYear, t).getMonth().toString(), n.textContent = g(t, b.config.shorthandCurrentMonth, b.l10n), n.tabIndex = -1, b.currentMonth === t && (n.selected = !0), b.monthsDropdownContainer.appendChild(n)
          }
      }
    }

    function U() {
      var e, t = u("div", "flatpickr-month"),
        n = window.document.createDocumentFragment();
      b.config.showMonths > 1 || "static" === b.config.monthSelectorType ? e = u("span", "cur-month") : (b.monthsDropdownContainer = u("select", "flatpickr-monthDropdown-months"), b.monthsDropdownContainer.setAttribute("aria-label", b.l10n.monthAriaLabel), P(b.monthsDropdownContainer, "change", (function(e) {
        var t = h(e),
          n = parseInt(t.value, 10);
        b.changeMonth(n - b.currentMonth), ve("onMonthChange")
      })), Y(), e = b.monthsDropdownContainer);
      var r = f("cur-year", {
          tabindex: "-1"
        }),
        i = r.getElementsByTagName("input")[0];
      i.setAttribute("aria-label", b.l10n.yearAriaLabel), b.config.minDate && i.setAttribute("min", b.config.minDate.getFullYear().toString()), b.config.maxDate && (i.setAttribute("max", b.config.maxDate.getFullYear().toString()), i.disabled = !!b.config.minDate && b.config.minDate.getFullYear() === b.config.maxDate.getFullYear());
      var o = u("div", "flatpickr-current-month");
      return o.appendChild(e), o.appendChild(r), n.appendChild(o), t.appendChild(n), {
        container: t,
        yearElement: i,
        monthElement: e
      }
    }

    function V() {
      d(b.monthNav), b.monthNav.appendChild(b.prevMonthNav), b.config.showMonths && (b.yearElements = [], b.monthElements = []);
      for (var e = b.config.showMonths; e--;) {
        var t = U();
        b.yearElements.push(t.yearElement), b.monthElements.push(t.monthElement), b.monthNav.appendChild(t.container)
      }
      b.monthNav.appendChild(b.nextMonthNav)
    }

    function X() {
      b.weekdayContainer ? d(b.weekdayContainer) : b.weekdayContainer = u("div", "flatpickr-weekdays");
      for (var e = b.config.showMonths; e--;) {
        var t = u("div", "flatpickr-weekdaycontainer");
        b.weekdayContainer.appendChild(t)
      }
      return G(), b.weekdayContainer
    }

    function G() {
      if (b.weekdayContainer) {
        var e = b.l10n.firstDayOfWeek,
          n = t(b.l10n.weekdays.shorthand);
        e > 0 && e < n.length && (n = t(n.splice(e, n.length), n.splice(0, e)));
        for (var r = b.config.showMonths; r--;) b.weekdayContainer.children[r].innerHTML = "\n      <span class='flatpickr-weekday'>\n        " + n.join("</span><span class='flatpickr-weekday'>") + "\n      </span>\n      "
      }
    }

    function Z(e, t) {
      void 0 === t && (t = !0);
      var n = t ? e : e - b.currentMonth;
      n < 0 && !0 === b._hidePrevMonthArrow || n > 0 && !0 === b._hideNextMonthArrow || (b.currentMonth += n, (b.currentMonth < 0 || b.currentMonth > 11) && (b.currentYear += b.currentMonth > 11 ? 1 : -1, b.currentMonth = (b.currentMonth + 12) % 12, ve("onYearChange"), Y()), W(), ve("onMonthChange"), we())
    }

    function K(e) {
      return b.calendarContainer.contains(e)
    }

    function J(e) {
      if (b.isOpen && !b.config.inline) {
        var t = h(e),
          n = K(t),
          r = !(t === b.input || t === b.altInput || b.element.contains(t) || e.path && e.path.indexOf && (~e.path.indexOf(b.input) || ~e.path.indexOf(b.altInput)) || n || K(e.relatedTarget)),
          i = !b.config.ignoredFocusElements.some((function(e) {
            return e.contains(t)
          }));
        r && i && (b.config.allowInput && b.setDate(b._input.value, !1, b.config.altInput ? b.config.altFormat : b.config.dateFormat), void 0 !== b.timeContainer && void 0 !== b.minuteElement && void 0 !== b.hourElement && "" !== b.input.value && void 0 !== b.input.value && A(), b.close(), b.config && "range" === b.config.mode && 1 === b.selectedDates.length && b.clear(!1))
      }
    }

    function Q(e) {
      if (!(!e || b.config.minDate && e < b.config.minDate.getFullYear() || b.config.maxDate && e > b.config.maxDate.getFullYear())) {
        var t = e,
          n = b.currentYear !== t;
        b.currentYear = t || b.currentYear, b.config.maxDate && b.currentYear === b.config.maxDate.getFullYear() ? b.currentMonth = Math.min(b.config.maxDate.getMonth(), b.currentMonth) : b.config.minDate && b.currentYear === b.config.minDate.getFullYear() && (b.currentMonth = Math.max(b.config.minDate.getMonth(), b.currentMonth)), n && (b.redraw(), ve("onYearChange"), Y())
      }
    }

    function ee(e, t) {
      var n;
      void 0 === t && (t = !0);
      var r = b.parseDate(e, void 0, t);
      if (b.config.minDate && r && S(r, b.config.minDate, void 0 !== t ? t : !b.minDateHasTime) < 0 || b.config.maxDate && r && S(r, b.config.maxDate, void 0 !== t ? t : !b.maxDateHasTime) > 0) return !1;
      if (!b.config.enable && 0 === b.config.disable.length) return !0;
      if (void 0 === r) return !1;
      for (var i = !!b.config.enable, o = null !== (n = b.config.enable) && void 0 !== n ? n : b.config.disable, a = 0, s = void 0; a < o.length; a++) {
        if ("function" == typeof(s = o[a]) && s(r)) return i;
        if (s instanceof Date && void 0 !== r && s.getTime() === r.getTime()) return i;
        if ("string" == typeof s) {
          var l = b.parseDate(s, void 0, !0);
          return l && l.getTime() === r.getTime() ? i : !i
        }
        if ("object" == typeof s && void 0 !== r && s.from && s.to && r.getTime() >= s.from.getTime() && r.getTime() <= s.to.getTime()) return i
      }
      return !i
    }

    function te(e) {
      return void 0 !== b.daysContainer && -1 === e.className.indexOf("hidden") && -1 === e.className.indexOf("flatpickr-disabled") && b.daysContainer.contains(e)
    }

    function ne(e) {
      var t = e.target === b._input,
        n = b._input.value.trimEnd() !== xe();
      !t || !n || e.relatedTarget && K(e.relatedTarget) || b.setDate(b._input.value, !0, e.target === b.altInput ? b.config.altFormat : b.config.dateFormat)
    }

    function re(e) {
      var t = h(e),
        n = b.config.wrap ? m.contains(t) : t === b._input,
        r = b.config.allowInput,
        i = b.isOpen && (!r || !n),
        o = b.config.inline && n && !r;
      if (13 === e.keyCode && n) {
        if (r) return b.setDate(b._input.value, !0, t === b.altInput ? b.config.altFormat : b.config.dateFormat), b.close(), t.blur();
        b.open()
      } else if (K(t) || i || o) {
        var a = !!b.timeContainer && b.timeContainer.contains(t);
        switch (e.keyCode) {
          case 13:
            a ? (e.preventDefault(), A(), de()) : pe(e);
            break;
          case 27:
            e.preventDefault(), de();
            break;
          case 8:
          case 46:
            n && !b.config.allowInput && (e.preventDefault(), b.clear());
            break;
          case 37:
          case 39:
            if (a || n) b.hourElement && b.hourElement.focus();
            else {
              e.preventDefault();
              var s = T();
              if (void 0 !== b.daysContainer && (!1 === r || s && te(s))) {
                var l = 39 === e.keyCode ? 1 : -1;
                e.ctrlKey ? (e.stopPropagation(), Z(l), B(F(1), 0)) : B(void 0, l)
              }
            }
            break;
          case 38:
          case 40:
            e.preventDefault();
            var c = 40 === e.keyCode ? 1 : -1;
            b.daysContainer && void 0 !== t.$i || t === b.input || t === b.altInput ? e.ctrlKey ? (e.stopPropagation(), Q(b.currentYear - c), B(F(1), 0)) : a || B(void 0, 7 * c) : t === b.currentYearElement ? Q(b.currentYear - c) : b.config.enableTime && (!a && b.hourElement && b.hourElement.focus(), A(e), b._debouncedChange());
            break;
          case 9:
            if (a) {
              var u = [b.hourElement, b.minuteElement, b.secondElement, b.amPM].concat(b.pluginElements).filter((function(e) {
                  return e
                })),
                d = u.indexOf(t);
              if (-1 !== d) {
                var p = u[d + (e.shiftKey ? -1 : 1)];
                e.preventDefault(), (p || b._input).focus()
              }
            } else !b.config.noCalendar && b.daysContainer && b.daysContainer.contains(t) && e.shiftKey && (e.preventDefault(), b._input.focus())
        }
      }
      if (void 0 !== b.amPM && t === b.amPM) switch (e.key) {
        case b.l10n.amPM[0].charAt(0):
        case b.l10n.amPM[0].charAt(0).toLowerCase():
          b.amPM.textContent = b.l10n.amPM[0], _(), Se();
          break;
        case b.l10n.amPM[1].charAt(0):
        case b.l10n.amPM[1].charAt(0).toLowerCase():
          b.amPM.textContent = b.l10n.amPM[1], _(), Se()
      }(n || K(t)) && ve("onKeyDown", e)
    }

    function ie(e, t) {
      if (void 0 === t && (t = "flatpickr-day"), 1 === b.selectedDates.length && (!e || e.classList.contains(t) && !e.classList.contains("flatpickr-disabled"))) {
        for (var n = e ? e.dateObj.getTime() : b.days.firstElementChild.dateObj.getTime(), r = b.parseDate(b.selectedDates[0], void 0, !0).getTime(), i = Math.min(n, b.selectedDates[0].getTime()), o = Math.max(n, b.selectedDates[0].getTime()), a = !1, s = 0, l = 0, c = i; c < o; c += 864e5) ee(new Date(c), !0) || (a = a || c > i && c < o, c < r && (!s || c > s) ? s = c : c > r && (!l || c < l) && (l = c));
        Array.from(b.rContainer.querySelectorAll("*:nth-child(-n+" + b.config.showMonths + ") > ." + t)).forEach((function(t) {
          var i, o, c, u = t.dateObj.getTime(),
            d = s > 0 && u < s || l > 0 && u > l;
          if (d) return t.classList.add("notAllowed"), void["inRange", "startRange", "endRange"].forEach((function(e) {
            t.classList.remove(e)
          }));
          a && !d || (["startRange", "inRange", "endRange", "notAllowed"].forEach((function(e) {
            t.classList.remove(e)
          })), void 0 !== e && (e.classList.add(n <= b.selectedDates[0].getTime() ? "startRange" : "endRange"), r < n && u === r ? t.classList.add("startRange") : r > n && u === r && t.classList.add("endRange"), u >= s && (0 === l || u <= l) && (o = r, c = n, (i = u) > Math.min(o, c) && i < Math.max(o, c)) && t.classList.add("inRange")))
        }))
      }
    }

    function oe() {
      !b.isOpen || b.config.static || b.config.inline || ce()
    }

    function ae(e) {
      return function(t) {
        var n = b.config["_" + e + "Date"] = b.parseDate(t, b.config.dateFormat),
          r = b.config["_" + ("min" === e ? "max" : "min") + "Date"];
        void 0 !== n && (b["min" === e ? "minDateHasTime" : "maxDateHasTime"] = n.getHours() > 0 || n.getMinutes() > 0 || n.getSeconds() > 0), b.selectedDates && (b.selectedDates = b.selectedDates.filter((function(e) {
          return ee(e)
        })), b.selectedDates.length || "min" !== e || M(n), Se()), b.daysContainer && (ue(), void 0 !== n ? b.currentYearElement[e] = n.getFullYear().toString() : b.currentYearElement.removeAttribute(e), b.currentYearElement.disabled = !!r && void 0 !== n && r.getFullYear() === n.getFullYear())
      }
    }

    function se() {
      return b.config.wrap ? m.querySelector("[data-input]") : m
    }

    function le() {
      "object" != typeof b.config.locale && void 0 === D.l10ns[b.config.locale] && b.config.errorHandler(new Error("flatpickr: invalid locale " + b.config.locale)), b.l10n = e(e({}, D.l10ns.default), "object" == typeof b.config.locale ? b.config.locale : "default" !== b.config.locale ? D.l10ns[b.config.locale] : void 0), y.D = "(" + b.l10n.weekdays.shorthand.join("|") + ")", y.l = "(" + b.l10n.weekdays.longhand.join("|") + ")", y.M = "(" + b.l10n.months.shorthand.join("|") + ")", y.F = "(" + b.l10n.months.longhand.join("|") + ")", y.K = "(" + b.l10n.amPM[0] + "|" + b.l10n.amPM[1] + "|" + b.l10n.amPM[0].toLowerCase() + "|" + b.l10n.amPM[1].toLowerCase() + ")", void 0 === e(e({}, v), JSON.parse(JSON.stringify(m.dataset || {}))).time_24hr && void 0 === D.defaultConfig.time_24hr && (b.config.time_24hr = b.l10n.time_24hr), b.formatDate = w(b), b.parseDate = x({
        config: b.config,
        l10n: b.l10n
      })
    }

    function ce(e) {
      if ("function" != typeof b.config.position) {
        if (void 0 !== b.calendarContainer) {
          ve("onPreCalendarPosition");
          var t = e || b._positionElement,
            n = Array.prototype.reduce.call(b.calendarContainer.children, (function(e, t) {
              return e + t.offsetHeight
            }), 0),
            r = b.calendarContainer.offsetWidth,
            i = b.config.position.split(" "),
            o = i[0],
            a = i.length > 1 ? i[1] : null,
            s = t.getBoundingClientRect(),
            l = window.innerHeight - s.bottom,
            u = "above" === o || "below" !== o && l < n && s.top > n,
            d = window.pageYOffset + s.top + (u ? -n - 2 : t.offsetHeight + 2);
          if (c(b.calendarContainer, "arrowTop", !u), c(b.calendarContainer, "arrowBottom", u), !b.config.inline) {
            var p = window.pageXOffset + s.left,
              f = !1,
              h = !1;
            "center" === a ? (p -= (r - s.width) / 2, f = !0) : "right" === a && (p -= r - s.width, h = !0), c(b.calendarContainer, "arrowLeft", !f && !h), c(b.calendarContainer, "arrowCenter", f), c(b.calendarContainer, "arrowRight", h);
            var m = window.document.body.offsetWidth - (window.pageXOffset + s.right),
              g = p + r > window.document.body.offsetWidth,
              v = m + r > window.document.body.offsetWidth;
            if (c(b.calendarContainer, "rightMost", g), !b.config.static)
              if (b.calendarContainer.style.top = d + "px", g)
                if (v) {
                  var y = function() {
                    for (var e = null, t = 0; t < document.styleSheets.length; t++) {
                      var n = document.styleSheets[t];
                      if (n.cssRules) {
                        try {
                          n.cssRules
                        } catch (e) {
                          continue
                        }
                        e = n;
                        break
                      }
                    }
                    return null != e ? e : (r = document.createElement("style"), document.head.appendChild(r), r.sheet);
                    var r
                  }();
                  if (void 0 === y) return;
                  var w = window.document.body.offsetWidth,
                    x = Math.max(0, w / 2 - r / 2),
                    S = y.cssRules.length,
                    C = "{left:" + s.left + "px;right:auto;}";
                  c(b.calendarContainer, "rightMost", !1), c(b.calendarContainer, "centerMost", !0), y.insertRule(".flatpickr-calendar.centerMost:before,.flatpickr-calendar.centerMost:after" + C, S), b.calendarContainer.style.left = x + "px", b.calendarContainer.style.right = "auto"
                } else b.calendarContainer.style.left = "auto", b.calendarContainer.style.right = m + "px";
            else b.calendarContainer.style.left = p + "px", b.calendarContainer.style.right = "auto"
          }
        }
      } else b.config.position(b, e)
    }

    function ue() {
      b.config.noCalendar || b.isMobile || (Y(), we(), W())
    }

    function de() {
      b._input.focus(), -1 !== window.navigator.userAgent.indexOf("MSIE") || void 0 !== navigator.msMaxTouchPoints ? setTimeout(b.close, 0) : b.close()
    }

    function pe(e) {
      e.preventDefault(), e.stopPropagation();
      var t = p(h(e), (function(e) {
        return e.classList && e.classList.contains("flatpickr-day") && !e.classList.contains("flatpickr-disabled") && !e.classList.contains("notAllowed")
      }));
      if (void 0 !== t) {
        var n = t,
          r = b.latestSelectedDateObj = new Date(n.dateObj.getTime()),
          i = (r.getMonth() < b.currentMonth || r.getMonth() > b.currentMonth + b.config.showMonths - 1) && "range" !== b.config.mode;
        if (b.selectedDateElem = n, "single" === b.config.mode) b.selectedDates = [r];
        else if ("multiple" === b.config.mode) {
          var o = be(r);
          o ? b.selectedDates.splice(parseInt(o), 1) : b.selectedDates.push(r)
        } else "range" === b.config.mode && (2 === b.selectedDates.length && b.clear(!1, !1), b.latestSelectedDateObj = r, b.selectedDates.push(r), 0 !== S(r, b.selectedDates[0], !0) && b.selectedDates.sort((function(e, t) {
          return e.getTime() - t.getTime()
        })));
        if (_(), i) {
          var a = b.currentYear !== r.getFullYear();
          b.currentYear = r.getFullYear(), b.currentMonth = r.getMonth(), a && (ve("onYearChange"), Y()), ve("onMonthChange")
        }
        if (we(), W(), Se(), i || "range" === b.config.mode || 1 !== b.config.showMonths ? void 0 !== b.selectedDateElem && void 0 === b.hourElement && b.selectedDateElem && b.selectedDateElem.focus() : H(n), void 0 !== b.hourElement && void 0 !== b.hourElement && b.hourElement.focus(), b.config.closeOnSelect) {
          var s = "single" === b.config.mode && !b.config.enableTime,
            l = "range" === b.config.mode && 2 === b.selectedDates.length && !b.config.enableTime;
          (s || l) && de()
        }
        j()
      }
    }
    b.parseDate = x({
      config: b.config,
      l10n: b.l10n
    }), b._handlers = [], b.pluginElements = [], b.loadedPlugins = [], b._bind = P, b._setHoursFromDate = M, b._positionCalendar = ce, b.changeMonth = Z, b.changeYear = Q, b.clear = function(e, t) {
      if (void 0 === e && (e = !0), void 0 === t && (t = !0), b.input.value = "", void 0 !== b.altInput && (b.altInput.value = ""), void 0 !== b.mobileInput && (b.mobileInput.value = ""), b.selectedDates = [], b.latestSelectedDateObj = void 0, !0 === t && (b.currentYear = b._initialDate.getFullYear(), b.currentMonth = b._initialDate.getMonth()), !0 === b.config.enableTime) {
        var n = E(b.config);
        L(n.hours, n.minutes, n.seconds)
      }
      b.redraw(), e && ve("onChange")
    }, b.close = function() {
      b.isOpen = !1, b.isMobile || (void 0 !== b.calendarContainer && b.calendarContainer.classList.remove("open"), void 0 !== b._input && b._input.classList.remove("active")), ve("onClose")
    }, b.onMouseOver = ie, b._createElement = u, b.createDay = $, b.destroy = function() {
      void 0 !== b.config && ve("onDestroy");
      for (var e = b._handlers.length; e--;) b._handlers[e].remove();
      if (b._handlers = [], b.mobileInput) b.mobileInput.parentNode && b.mobileInput.parentNode.removeChild(b.mobileInput), b.mobileInput = void 0;
      else if (b.calendarContainer && b.calendarContainer.parentNode)
        if (b.config.static && b.calendarContainer.parentNode) {
          var t = b.calendarContainer.parentNode;
          if (t.lastChild && t.removeChild(t.lastChild), t.parentNode) {
            for (; t.firstChild;) t.parentNode.insertBefore(t.firstChild, t);
            t.parentNode.removeChild(t)
          }
        } else b.calendarContainer.parentNode.removeChild(b.calendarContainer);
      b.altInput && (b.input.type = "text", b.altInput.parentNode && b.altInput.parentNode.removeChild(b.altInput), delete b.altInput), b.input && (b.input.type = b.input._type, b.input.classList.remove("flatpickr-input"), b.input.removeAttribute("readonly")), ["_showTimeInput", "latestSelectedDateObj", "_hideNextMonthArrow", "_hidePrevMonthArrow", "__hideNextMonthArrow", "__hidePrevMonthArrow", "isMobile", "isOpen", "selectedDateElem", "minDateHasTime", "maxDateHasTime", "days", "daysContainer", "_input", "_positionElement", "innerContainer", "rContainer", "monthNav", "todayDateElem", "calendarContainer", "weekdayContainer", "prevMonthNav", "nextMonthNav", "monthsDropdownContainer", "currentMonthElement", "currentYearElement", "navigationCurrentMonth", "selectedDateElem", "config"].forEach((function(e) {
        try {
          delete b[e]
        } catch (e) {}
      }))
    }, b.isEnabled = ee, b.jumpToDate = N, b.updateValue = Se, b.open = function(e, t) {
      if (void 0 === t && (t = b._positionElement), !0 === b.isMobile) {
        if (e) {
          e.preventDefault();
          var n = h(e);
          n && n.blur()
        }
        return void 0 !== b.mobileInput && (b.mobileInput.focus(), b.mobileInput.click()), void ve("onOpen")
      }
      if (!b._input.disabled && !b.config.inline) {
        var r = b.isOpen;
        b.isOpen = !0, r || (b.calendarContainer.classList.add("open"), b._input.classList.add("active"), ve("onOpen"), ce(t)), !0 === b.config.enableTime && !0 === b.config.noCalendar && (!1 !== b.config.allowInput || void 0 !== e && b.timeContainer.contains(e.relatedTarget) || setTimeout((function() {
          return b.hourElement.select()
        }), 50))
      }
    }, b.redraw = ue, b.set = function(e, t) {
      if (null !== e && "object" == typeof e)
        for (var r in Object.assign(b.config, e), e) void 0 !== fe[r] && fe[r].forEach((function(e) {
          return e()
        }));
      else b.config[e] = t, void 0 !== fe[e] ? fe[e].forEach((function(e) {
        return e()
      })) : n.indexOf(e) > -1 && (b.config[e] = l(t));
      b.redraw(), Se(!0)
    }, b.setDate = function(e, t, n) {
      if (void 0 === t && (t = !1), void 0 === n && (n = b.config.dateFormat), 0 !== e && !e || e instanceof Array && 0 === e.length) return b.clear(t);
      he(e, n), b.latestSelectedDateObj = b.selectedDates[b.selectedDates.length - 1], b.redraw(), N(void 0, t), M(), 0 === b.selectedDates.length && b.clear(!1), Se(t), t && ve("onChange")
    }, b.toggle = function(e) {
      if (!0 === b.isOpen) return b.close();
      b.open(e)
    };
    var fe = {
      locale: [le, G],
      showMonths: [V, O, X],
      minDate: [N],
      maxDate: [N],
      positionElement: [ge],
      clickOpens: [function() {
        !0 === b.config.clickOpens ? (P(b._input, "focus", b.open), P(b._input, "click", b.open)) : (b._input.removeEventListener("focus", b.open), b._input.removeEventListener("click", b.open))
      }]
    };

    function he(e, t) {
      var n = [];
      if (e instanceof Array) n = e.map((function(e) {
        return b.parseDate(e, t)
      }));
      else if (e instanceof Date || "number" == typeof e) n = [b.parseDate(e, t)];
      else if ("string" == typeof e) switch (b.config.mode) {
        case "single":
        case "time":
          n = [b.parseDate(e, t)];
          break;
        case "multiple":
          n = e.split(b.config.conjunction).map((function(e) {
            return b.parseDate(e, t)
          }));
          break;
        case "range":
          n = e.split(b.l10n.rangeSeparator).map((function(e) {
            return b.parseDate(e, t)
          }))
      } else b.config.errorHandler(new Error("Invalid date supplied: " + JSON.stringify(e)));
      b.selectedDates = b.config.allowInvalidPreload ? n : n.filter((function(e) {
        return e instanceof Date && ee(e, !1)
      })), "range" === b.config.mode && b.selectedDates.sort((function(e, t) {
        return e.getTime() - t.getTime()
      }))
    }

    function me(e) {
      return e.slice().map((function(e) {
        return "string" == typeof e || "number" == typeof e || e instanceof Date ? b.parseDate(e, void 0, !0) : e && "object" == typeof e && e.from && e.to ? {
          from: b.parseDate(e.from, void 0),
          to: b.parseDate(e.to, void 0)
        } : e
      })).filter((function(e) {
        return e
      }))
    }

    function ge() {
      b._positionElement = b.config.positionElement || b._input
    }

    function ve(e, t) {
      if (void 0 !== b.config) {
        var n = b.config[e];
        if (void 0 !== n && n.length > 0)
          for (var r = 0; n[r] && r < n.length; r++) n[r](b.selectedDates, b.input.value, b, t);
        "onChange" === e && (b.input.dispatchEvent(ye("change")), b.input.dispatchEvent(ye("input")))
      }
    }

    function ye(e) {
      var t = document.createEvent("Event");
      return t.initEvent(e, !0, !0), t
    }

    function be(e) {
      for (var t = 0; t < b.selectedDates.length; t++) {
        var n = b.selectedDates[t];
        if (n instanceof Date && 0 === S(n, e)) return "" + t
      }
      return !1
    }

    function we() {
      b.config.noCalendar || b.isMobile || !b.monthNav || (b.yearElements.forEach((function(e, t) {
        var n = new Date(b.currentYear, b.currentMonth, 1);
        n.setMonth(b.currentMonth + t), b.config.showMonths > 1 || "static" === b.config.monthSelectorType ? b.monthElements[t].textContent = g(n.getMonth(), b.config.shorthandCurrentMonth, b.l10n) + " " : b.monthsDropdownContainer.value = n.getMonth().toString(), e.value = n.getFullYear().toString()
      })), b._hidePrevMonthArrow = void 0 !== b.config.minDate && (b.currentYear === b.config.minDate.getFullYear() ? b.currentMonth <= b.config.minDate.getMonth() : b.currentYear < b.config.minDate.getFullYear()), b._hideNextMonthArrow = void 0 !== b.config.maxDate && (b.currentYear === b.config.maxDate.getFullYear() ? b.currentMonth + 1 > b.config.maxDate.getMonth() : b.currentYear > b.config.maxDate.getFullYear()))
    }

    function xe(e) {
      var t = e || (b.config.altInput ? b.config.altFormat : b.config.dateFormat);
      return b.selectedDates.map((function(e) {
        return b.formatDate(e, t)
      })).filter((function(e, t, n) {
        return "range" !== b.config.mode || b.config.enableTime || n.indexOf(e) === t
      })).join("range" !== b.config.mode ? b.config.conjunction : b.l10n.rangeSeparator)
    }

    function Se(e) {
      void 0 === e && (e = !0), void 0 !== b.mobileInput && b.mobileFormatStr && (b.mobileInput.value = void 0 !== b.latestSelectedDateObj ? b.formatDate(b.latestSelectedDateObj, b.mobileFormatStr) : ""), b.input.value = xe(b.config.dateFormat), void 0 !== b.altInput && (b.altInput.value = xe(b.config.altFormat)), !1 !== e && ve("onValueUpdate")
    }

    function Ce(e) {
      var t = h(e),
        n = b.prevMonthNav.contains(t),
        r = b.nextMonthNav.contains(t);
      n || r ? Z(n ? -1 : 1) : b.yearElements.indexOf(t) >= 0 ? t.select() : t.classList.contains("arrowUp") ? b.changeYear(b.currentYear + 1) : t.classList.contains("arrowDown") && b.changeYear(b.currentYear - 1)
    }
    return function() {
      b.element = b.input = m, b.isOpen = !1,
        function() {
          var t = ["wrap", "weekNumbers", "allowInput", "allowInvalidPreload", "clickOpens", "time_24hr", "enableTime", "noCalendar", "altInput", "shorthandCurrentMonth", "inline", "static", "enableSeconds", "disableMobile"],
            i = e(e({}, JSON.parse(JSON.stringify(m.dataset || {}))), v),
            o = {};
          b.config.parseDate = i.parseDate, b.config.formatDate = i.formatDate, Object.defineProperty(b.config, "enable", {
            get: function() {
              return b.config._enable
            },
            set: function(e) {
              b.config._enable = me(e)
            }
          }), Object.defineProperty(b.config, "disable", {
            get: function() {
              return b.config._disable
            },
            set: function(e) {
              b.config._disable = me(e)
            }
          });
          var a = "time" === i.mode;
          if (!i.dateFormat && (i.enableTime || a)) {
            var s = D.defaultConfig.dateFormat || r.dateFormat;
            o.dateFormat = i.noCalendar || a ? "H:i" + (i.enableSeconds ? ":S" : "") : s + " H:i" + (i.enableSeconds ? ":S" : "")
          }
          if (i.altInput && (i.enableTime || a) && !i.altFormat) {
            var c = D.defaultConfig.altFormat || r.altFormat;
            o.altFormat = i.noCalendar || a ? "h:i" + (i.enableSeconds ? ":S K" : " K") : c + " h:i" + (i.enableSeconds ? ":S" : "") + " K"
          }
          Object.defineProperty(b.config, "minDate", {
            get: function() {
              return b.config._minDate
            },
            set: ae("min")
          }), Object.defineProperty(b.config, "maxDate", {
            get: function() {
              return b.config._maxDate
            },
            set: ae("max")
          });
          var u = function(e) {
            return function(t) {
              b.config["min" === e ? "_minTime" : "_maxTime"] = b.parseDate(t, "H:i:S")
            }
          };
          Object.defineProperty(b.config, "minTime", {
            get: function() {
              return b.config._minTime
            },
            set: u("min")
          }), Object.defineProperty(b.config, "maxTime", {
            get: function() {
              return b.config._maxTime
            },
            set: u("max")
          }), "time" === i.mode && (b.config.noCalendar = !0, b.config.enableTime = !0), Object.assign(b.config, o, i);
          for (var d = 0; d < t.length; d++) b.config[t[d]] = !0 === b.config[t[d]] || "true" === b.config[t[d]];
          for (n.filter((function(e) {
              return void 0 !== b.config[e]
            })).forEach((function(e) {
              b.config[e] = l(b.config[e] || []).map(k)
            })), b.isMobile = !b.config.disableMobile && !b.config.inline && "single" === b.config.mode && !b.config.disable.length && !b.config.enable && !b.config.weekNumbers && /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent), d = 0; d < b.config.plugins.length; d++) {
            var p = b.config.plugins[d](b) || {};
            for (var f in p) n.indexOf(f) > -1 ? b.config[f] = l(p[f]).map(k).concat(b.config[f]) : void 0 === i[f] && (b.config[f] = p[f])
          }
          i.altInputClass || (b.config.altInputClass = se().className + " " + b.config.altInputClass), ve("onParseConfig")
        }(), le(), b.input = se(), b.input ? (b.input._type = b.input.type, b.input.type = "text", b.input.classList.add("flatpickr-input"), b._input = b.input, b.config.altInput && (b.altInput = u(b.input.nodeName, b.config.altInputClass), b._input = b.altInput, b.altInput.placeholder = b.input.placeholder, b.altInput.disabled = b.input.disabled, b.altInput.required = b.input.required, b.altInput.tabIndex = b.input.tabIndex, b.altInput.type = "text", b.input.setAttribute("type", "hidden"), !b.config.static && b.input.parentNode && b.input.parentNode.insertBefore(b.altInput, b.input.nextSibling)), b.config.allowInput || b._input.setAttribute("readonly", "readonly"), ge()) : b.config.errorHandler(new Error("Invalid input element specified")),
        function() {
          b.selectedDates = [], b.now = b.parseDate(b.config.now) || new Date;
          var e = b.config.defaultDate || ("INPUT" !== b.input.nodeName && "TEXTAREA" !== b.input.nodeName || !b.input.placeholder || b.input.value !== b.input.placeholder ? b.input.value : null);
          e && he(e, b.config.dateFormat), b._initialDate = b.selectedDates.length > 0 ? b.selectedDates[0] : b.config.minDate && b.config.minDate.getTime() > b.now.getTime() ? b.config.minDate : b.config.maxDate && b.config.maxDate.getTime() < b.now.getTime() ? b.config.maxDate : b.now, b.currentYear = b._initialDate.getFullYear(), b.currentMonth = b._initialDate.getMonth(), b.selectedDates.length > 0 && (b.latestSelectedDateObj = b.selectedDates[0]), void 0 !== b.config.minTime && (b.config.minTime = b.parseDate(b.config.minTime, "H:i")), void 0 !== b.config.maxTime && (b.config.maxTime = b.parseDate(b.config.maxTime, "H:i")), b.minDateHasTime = !!b.config.minDate && (b.config.minDate.getHours() > 0 || b.config.minDate.getMinutes() > 0 || b.config.minDate.getSeconds() > 0), b.maxDateHasTime = !!b.config.maxDate && (b.config.maxDate.getHours() > 0 || b.config.maxDate.getMinutes() > 0 || b.config.maxDate.getSeconds() > 0)
        }(), b.utils = {
          getDaysInMonth: function(e, t) {
            return void 0 === e && (e = b.currentMonth), void 0 === t && (t = b.currentYear), 1 === e && (t % 4 == 0 && t % 100 != 0 || t % 400 == 0) ? 29 : b.l10n.daysInMonth[e]
          }
        }, b.isMobile || function() {
          var e = window.document.createDocumentFragment();
          if (b.calendarContainer = u("div", "flatpickr-calendar"), b.calendarContainer.tabIndex = -1, !b.config.noCalendar) {
            if (e.appendChild((b.monthNav = u("div", "flatpickr-months"), b.yearElements = [], b.monthElements = [], b.prevMonthNav = u("span", "flatpickr-prev-month"), b.prevMonthNav.innerHTML = b.config.prevArrow, b.nextMonthNav = u("span", "flatpickr-next-month"), b.nextMonthNav.innerHTML = b.config.nextArrow, V(), Object.defineProperty(b, "_hidePrevMonthArrow", {
                get: function() {
                  return b.__hidePrevMonthArrow
                },
                set: function(e) {
                  b.__hidePrevMonthArrow !== e && (c(b.prevMonthNav, "flatpickr-disabled", e), b.__hidePrevMonthArrow = e)
                }
              }), Object.defineProperty(b, "_hideNextMonthArrow", {
                get: function() {
                  return b.__hideNextMonthArrow
                },
                set: function(e) {
                  b.__hideNextMonthArrow !== e && (c(b.nextMonthNav, "flatpickr-disabled", e), b.__hideNextMonthArrow = e)
                }
              }), b.currentYearElement = b.yearElements[0], we(), b.monthNav)), b.innerContainer = u("div", "flatpickr-innerContainer"), b.config.weekNumbers) {
              var t = function() {
                  b.calendarContainer.classList.add("hasWeeks");
                  var e = u("div", "flatpickr-weekwrapper");
                  e.appendChild(u("span", "flatpickr-weekday", b.l10n.weekAbbreviation));
                  var t = u("div", "flatpickr-weeks");
                  return e.appendChild(t), {
                    weekWrapper: e,
                    weekNumbers: t
                  }
                }(),
                n = t.weekWrapper,
                r = t.weekNumbers;
              b.innerContainer.appendChild(n), b.weekNumbers = r, b.weekWrapper = n
            }
            b.rContainer = u("div", "flatpickr-rContainer"), b.rContainer.appendChild(X()), b.daysContainer || (b.daysContainer = u("div", "flatpickr-days"), b.daysContainer.tabIndex = -1), W(), b.rContainer.appendChild(b.daysContainer), b.innerContainer.appendChild(b.rContainer), e.appendChild(b.innerContainer)
          }
          b.config.enableTime && e.appendChild(function() {
            b.calendarContainer.classList.add("hasTime"), b.config.noCalendar && b.calendarContainer.classList.add("noCalendar");
            var e = E(b.config);
            b.timeContainer = u("div", "flatpickr-time"), b.timeContainer.tabIndex = -1;
            var t = u("span", "flatpickr-time-separator", ":"),
              n = f("flatpickr-hour", {
                "aria-label": b.l10n.hourAriaLabel
              });
            b.hourElement = n.getElementsByTagName("input")[0];
            var r = f("flatpickr-minute", {
              "aria-label": b.l10n.minuteAriaLabel
            });
            if (b.minuteElement = r.getElementsByTagName("input")[0], b.hourElement.tabIndex = b.minuteElement.tabIndex = -1, b.hourElement.value = o(b.latestSelectedDateObj ? b.latestSelectedDateObj.getHours() : b.config.time_24hr ? e.hours : function(e) {
                switch (e % 24) {
                  case 0:
                  case 12:
                    return 12;
                  default:
                    return e % 12
                }
              }(e.hours)), b.minuteElement.value = o(b.latestSelectedDateObj ? b.latestSelectedDateObj.getMinutes() : e.minutes), b.hourElement.setAttribute("step", b.config.hourIncrement.toString()), b.minuteElement.setAttribute("step", b.config.minuteIncrement.toString()), b.hourElement.setAttribute("min", b.config.time_24hr ? "0" : "1"), b.hourElement.setAttribute("max", b.config.time_24hr ? "23" : "12"), b.hourElement.setAttribute("maxlength", "2"), b.minuteElement.setAttribute("min", "0"), b.minuteElement.setAttribute("max", "59"), b.minuteElement.setAttribute("maxlength", "2"), b.timeContainer.appendChild(n), b.timeContainer.appendChild(t), b.timeContainer.appendChild(r), b.config.time_24hr && b.timeContainer.classList.add("time24hr"), b.config.enableSeconds) {
              b.timeContainer.classList.add("hasSeconds");
              var i = f("flatpickr-second");
              b.secondElement = i.getElementsByTagName("input")[0], b.secondElement.value = o(b.latestSelectedDateObj ? b.latestSelectedDateObj.getSeconds() : e.seconds), b.secondElement.setAttribute("step", b.minuteElement.getAttribute("step")), b.secondElement.setAttribute("min", "0"), b.secondElement.setAttribute("max", "59"), b.secondElement.setAttribute("maxlength", "2"), b.timeContainer.appendChild(u("span", "flatpickr-time-separator", ":")), b.timeContainer.appendChild(i)
            }
            return b.config.time_24hr || (b.amPM = u("span", "flatpickr-am-pm", b.l10n.amPM[a((b.latestSelectedDateObj ? b.hourElement.value : b.config.defaultHour) > 11)]), b.amPM.title = b.l10n.toggleTitle, b.amPM.tabIndex = -1, b.timeContainer.appendChild(b.amPM)), b.timeContainer
          }()), c(b.calendarContainer, "rangeMode", "range" === b.config.mode), c(b.calendarContainer, "animate", !0 === b.config.animate), c(b.calendarContainer, "multiMonth", b.config.showMonths > 1), b.calendarContainer.appendChild(e);
          var i = void 0 !== b.config.appendTo && void 0 !== b.config.appendTo.nodeType;
          if ((b.config.inline || b.config.static) && (b.calendarContainer.classList.add(b.config.inline ? "inline" : "static"), b.config.inline && (!i && b.element.parentNode ? b.element.parentNode.insertBefore(b.calendarContainer, b._input.nextSibling) : void 0 !== b.config.appendTo && b.config.appendTo.appendChild(b.calendarContainer)), b.config.static)) {
            var s = u("div", "flatpickr-wrapper");
            b.element.parentNode && b.element.parentNode.insertBefore(s, b.element), s.appendChild(b.element), b.altInput && s.appendChild(b.altInput), s.appendChild(b.calendarContainer)
          }
          b.config.static || b.config.inline || (void 0 !== b.config.appendTo ? b.config.appendTo : window.document.body).appendChild(b.calendarContainer)
        }(),
        function() {
          if (b.config.wrap && ["open", "close", "toggle", "clear"].forEach((function(e) {
              Array.prototype.forEach.call(b.element.querySelectorAll("[data-" + e + "]"), (function(t) {
                return P(t, "click", b[e])
              }))
            })), b.isMobile) ! function() {
            var e = b.config.enableTime ? b.config.noCalendar ? "time" : "datetime-local" : "date";
            b.mobileInput = u("input", b.input.className + " flatpickr-mobile"), b.mobileInput.tabIndex = 1, b.mobileInput.type = e, b.mobileInput.disabled = b.input.disabled, b.mobileInput.required = b.input.required, b.mobileInput.placeholder = b.input.placeholder, b.mobileFormatStr = "datetime-local" === e ? "Y-m-d\\TH:i:S" : "date" === e ? "Y-m-d" : "H:i:S", b.selectedDates.length > 0 && (b.mobileInput.defaultValue = b.mobileInput.value = b.formatDate(b.selectedDates[0], b.mobileFormatStr)), b.config.minDate && (b.mobileInput.min = b.formatDate(b.config.minDate, "Y-m-d")), b.config.maxDate && (b.mobileInput.max = b.formatDate(b.config.maxDate, "Y-m-d")), b.input.getAttribute("step") && (b.mobileInput.step = String(b.input.getAttribute("step"))), b.input.type = "hidden", void 0 !== b.altInput && (b.altInput.type = "hidden");
            try {
              b.input.parentNode && b.input.parentNode.insertBefore(b.mobileInput, b.input.nextSibling)
            } catch (e) {}
            P(b.mobileInput, "change", (function(e) {
              b.setDate(h(e).value, !1, b.mobileFormatStr), ve("onChange"), ve("onClose")
            }))
          }();
          else {
            var e = s(oe, 50);
            if (b._debouncedChange = s(j, 300), b.daysContainer && !/iPhone|iPad|iPod/i.test(navigator.userAgent) && P(b.daysContainer, "mouseover", (function(e) {
                "range" === b.config.mode && ie(h(e))
              })), P(b._input, "keydown", re), void 0 !== b.calendarContainer && P(b.calendarContainer, "keydown", re), b.config.inline || b.config.static || P(window, "resize", e), void 0 !== window.ontouchstart ? P(window.document, "touchstart", J) : P(window.document, "mousedown", J), P(window.document, "focus", J, {
                capture: !0
              }), !0 === b.config.clickOpens && (P(b._input, "focus", b.open), P(b._input, "click", b.open)), void 0 !== b.daysContainer && (P(b.monthNav, "click", Ce), P(b.monthNav, ["keyup", "increment"], I), P(b.daysContainer, "click", pe)), void 0 !== b.timeContainer && void 0 !== b.minuteElement && void 0 !== b.hourElement) {
              P(b.timeContainer, ["increment"], A), P(b.timeContainer, "blur", A, {
                capture: !0
              }), P(b.timeContainer, "click", z), P([b.hourElement, b.minuteElement], ["focus", "click"], (function(e) {
                return h(e).select()
              })), void 0 !== b.secondElement && P(b.secondElement, "focus", (function() {
                return b.secondElement && b.secondElement.select()
              })), void 0 !== b.amPM && P(b.amPM, "click", (function(e) {
                A(e)
              }))
            }
            b.config.allowInput && P(b._input, "blur", ne)
          }
        }(), (b.selectedDates.length || b.config.noCalendar) && (b.config.enableTime && M(b.config.noCalendar ? b.latestSelectedDateObj : void 0), Se(!1)), O();
      var t = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
      !b.isMobile && t && ce(), ve("onReady")
    }(), b
  }

  function k(e, t) {
    for (var n = Array.prototype.slice.call(e).filter((function(e) {
        return e instanceof HTMLElement
      })), r = [], i = 0; i < n.length; i++) {
      var o = n[i];
      try {
        if (null !== o.getAttribute("data-fp-omit")) continue;
        void 0 !== o._flatpickr && (o._flatpickr.destroy(), o._flatpickr = void 0), o._flatpickr = T(o, t || {}), r.push(o._flatpickr)
      } catch (e) {
        console.error(e)
      }
    }
    return 1 === r.length ? r[0] : r
  }
  "function" != typeof Object.assign && (Object.assign = function(e) {
    for (var t = [], n = 1; n < arguments.length; n++) t[n - 1] = arguments[n];
    if (!e) throw TypeError("Cannot convert undefined or null to object");
    for (var r = function(t) {
        t && Object.keys(t).forEach((function(n) {
          return e[n] = t[n]
        }))
      }, i = 0, o = t; i < o.length; i++) {
      var a = o[i];
      r(a)
    }
    return e
  }), "undefined" != typeof HTMLElement && "undefined" != typeof HTMLCollection && "undefined" != typeof NodeList && (HTMLCollection.prototype.flatpickr = NodeList.prototype.flatpickr = function(e) {
    return k(this, e)
  }, HTMLElement.prototype.flatpickr = function(e) {
    return k([this], e)
  });
  var D = function(e, t) {
    return "string" == typeof e ? k(window.document.querySelectorAll(e), t) : e instanceof Node ? k([e], t) : k(e, t)
  };
  return D.defaultConfig = {}, D.l10ns = {
    en: e({}, i),
    default: e({}, i)
  }, D.localize = function(t) {
    D.l10ns.default = e(e({}, D.l10ns.default), t)
  }, D.setDefaults = function(t) {
    D.defaultConfig = e(e({}, D.defaultConfig), t)
  }, D.parseDate = x({}), D.formatDate = w({}), D.compareDates = S, "undefined" != typeof jQuery && void 0 !== jQuery.fn && (jQuery.fn.flatpickr = function(e) {
    return k(this, e)
  }), Date.prototype.fp_incr = function(e) {
    return new Date(this.getFullYear(), this.getMonth(), this.getDate() + ("string" == typeof e ? parseInt(e, 10) : e))
  }, "undefined" != typeof window && (window.flatpickr = D), D
})),
function(e, t) {
  "object" == typeof exports && "undefined" != typeof module ? t(exports) : "function" == typeof define && define.amd ? define(["exports"], t) : t((e = "undefined" != typeof globalThis ? globalThis : e || self).ru = {})
}(this, (function(e) {
  "use strict";
  var t = "undefined" != typeof window && void 0 !== window.flatpickr ? window.flatpickr : {
      l10ns: {}
    },
    n = {
      weekdays: {
        shorthand: ["Вс", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб"],
        longhand: ["Воскресенье", "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
      },
      months: {
        shorthand: ["Янв", "Фев", "Март", "Апр", "Май", "Июнь", "Июль", "Авг", "Сен", "Окт", "Ноя", "Дек"],
        longhand: ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
      },
      firstDayOfWeek: 1,
      ordinal: function() {
        return ""
      },
      rangeSeparator: " — ",
      weekAbbreviation: "Нед.",
      scrollTitle: "Прокрутите для увеличения",
      toggleTitle: "Нажмите для переключения",
      amPM: ["ДП", "ПП"],
      yearAriaLabel: "Год",
      time_24hr: !0
    };
  t.l10ns.ru = n;
  var r = t.l10ns;
  e.Russian = n, e.default = r, Object.defineProperty(e, "__esModule", {
    value: !0
  })
})),
function(e, t) {
  "object" == typeof exports && "object" == typeof module ? module.exports = t() : "function" == typeof define && define.amd ? define([], t) : "object" == typeof exports ? exports.Cleave = t() : e.Cleave = t()
}(this, (function() {
  return function(e) {
    function t(r) {
      if (n[r]) return n[r].exports;
      var i = n[r] = {
        exports: {},
        id: r,
        loaded: !1
      };
      return e[r].call(i.exports, i, i.exports, t), i.loaded = !0, i.exports
    }
    var n = {};
    return t.m = e, t.c = n, t.p = "", t(0)
  }([function(e, t, n) {
    (function(t) {
      "use strict";
      var r = function(e, t) {
        var n = this,
          i = !1;
        if ("string" == typeof e ? (n.element = document.querySelector(e), i = document.querySelectorAll(e).length > 1) : void 0 !== e.length && e.length > 0 ? (n.element = e[0], i = e.length > 1) : n.element = e, !n.element) throw new Error("[cleave.js] Please check the element");
        if (i) try {
          console.warn("[cleave.js] Multiple input fields matched, cleave.js will only take the first one.")
        } catch (e) {}
        t.initValue = n.element.value, n.properties = r.DefaultProperties.assign({}, t), n.init()
      };
      r.prototype = {
        init: function() {
          var e = this,
            t = e.properties;
          return t.numeral || t.phone || t.creditCard || t.time || t.date || 0 !== t.blocksLength || t.prefix ? (t.maxLength = r.Util.getMaxLength(t.blocks), e.isAndroid = r.Util.isAndroid(), e.lastInputValue = "", e.isBackward = "", e.onChangeListener = e.onChange.bind(e), e.onKeyDownListener = e.onKeyDown.bind(e), e.onFocusListener = e.onFocus.bind(e), e.onCutListener = e.onCut.bind(e), e.onCopyListener = e.onCopy.bind(e), e.initSwapHiddenInput(), e.element.addEventListener("input", e.onChangeListener), e.element.addEventListener("keydown", e.onKeyDownListener), e.element.addEventListener("focus", e.onFocusListener), e.element.addEventListener("cut", e.onCutListener), e.element.addEventListener("copy", e.onCopyListener), e.initPhoneFormatter(), e.initDateFormatter(), e.initTimeFormatter(), e.initNumeralFormatter(), void((t.initValue || t.prefix && !t.noImmediatePrefix) && e.onInput(t.initValue))) : void e.onInput(t.initValue)
        },
        initSwapHiddenInput: function() {
          var e = this;
          if (e.properties.swapHiddenInput) {
            var t = e.element.cloneNode(!0);
            e.element.parentNode.insertBefore(t, e.element), e.elementSwapHidden = e.element, e.elementSwapHidden.type = "hidden", e.element = t, e.element.id = ""
          }
        },
        initNumeralFormatter: function() {
          var e = this.properties;
          e.numeral && (e.numeralFormatter = new r.NumeralFormatter(e.numeralDecimalMark, e.numeralIntegerScale, e.numeralDecimalScale, e.numeralThousandsGroupStyle, e.numeralPositiveOnly, e.stripLeadingZeroes, e.prefix, e.signBeforePrefix, e.tailPrefix, e.delimiter))
        },
        initTimeFormatter: function() {
          var e = this.properties;
          e.time && (e.timeFormatter = new r.TimeFormatter(e.timePattern, e.timeFormat), e.blocks = e.timeFormatter.getBlocks(), e.blocksLength = e.blocks.length, e.maxLength = r.Util.getMaxLength(e.blocks))
        },
        initDateFormatter: function() {
          var e = this.properties;
          e.date && (e.dateFormatter = new r.DateFormatter(e.datePattern, e.dateMin, e.dateMax), e.blocks = e.dateFormatter.getBlocks(), e.blocksLength = e.blocks.length, e.maxLength = r.Util.getMaxLength(e.blocks))
        },
        initPhoneFormatter: function() {
          var e = this.properties;
          if (e.phone) try {
            e.phoneFormatter = new r.PhoneFormatter(new e.root.Cleave.AsYouTypeFormatter(e.phoneRegionCode), e.delimiter)
          } catch (e) {
            throw new Error("[cleave.js] Please include phone-type-formatter.{country}.js lib")
          }
        },
        onKeyDown: function(e) {
          var t = this,
            n = e.which || e.keyCode;
          t.lastInputValue = t.element.value, t.isBackward = 8 === n
        },
        onChange: function(e) {
          var t = this,
            n = t.properties,
            i = r.Util;
          t.isBackward = t.isBackward || "deleteContentBackward" === e.inputType;
          var o = i.getPostDelimiter(t.lastInputValue, n.delimiter, n.delimiters);
          t.isBackward && o ? n.postDelimiterBackspace = o : n.postDelimiterBackspace = !1, this.onInput(this.element.value)
        },
        onFocus: function() {
          var e = this,
            t = e.properties;
          e.lastInputValue = e.element.value, t.prefix && t.noImmediatePrefix && !e.element.value && this.onInput(t.prefix), r.Util.fixPrefixCursor(e.element, t.prefix, t.delimiter, t.delimiters)
        },
        onCut: function(e) {
          r.Util.checkFullSelection(this.element.value) && (this.copyClipboardData(e), this.onInput(""))
        },
        onCopy: function(e) {
          r.Util.checkFullSelection(this.element.value) && this.copyClipboardData(e)
        },
        copyClipboardData: function(e) {
          var t, n = this.properties,
            i = r.Util,
            o = this.element.value;
          t = n.copyDelimiter ? o : i.stripDelimiters(o, n.delimiter, n.delimiters);
          try {
            e.clipboardData ? e.clipboardData.setData("Text", t) : window.clipboardData.setData("Text", t), e.preventDefault()
          } catch (e) {}
        },
        onInput: function(e) {
          var t = this,
            n = t.properties,
            i = r.Util,
            o = i.getPostDelimiter(e, n.delimiter, n.delimiters);
          return n.numeral || !n.postDelimiterBackspace || o || (e = i.headStr(e, e.length - n.postDelimiterBackspace.length)), n.phone ? (!n.prefix || n.noImmediatePrefix && !e.length ? n.result = n.phoneFormatter.format(e) : n.result = n.prefix + n.phoneFormatter.format(e).slice(n.prefix.length), void t.updateValueState()) : n.numeral ? (n.prefix && n.noImmediatePrefix && 0 === e.length ? n.result = "" : n.result = n.numeralFormatter.format(e), void t.updateValueState()) : (n.date && (e = n.dateFormatter.getValidatedDate(e)), n.time && (e = n.timeFormatter.getValidatedTime(e)), e = i.stripDelimiters(e, n.delimiter, n.delimiters), e = i.getPrefixStrippedValue(e, n.prefix, n.prefixLength, n.result, n.delimiter, n.delimiters, n.noImmediatePrefix, n.tailPrefix, n.signBeforePrefix), e = n.numericOnly ? i.strip(e, /[^\d]/g) : e, e = n.uppercase ? e.toUpperCase() : e, e = n.lowercase ? e.toLowerCase() : e, n.prefix && (n.tailPrefix ? e += n.prefix : e = n.prefix + e, 0 === n.blocksLength) ? (n.result = e, void t.updateValueState()) : (n.creditCard && t.updateCreditCardPropsByValue(e), e = i.headStr(e, n.maxLength), n.result = i.getFormattedValue(e, n.blocks, n.blocksLength, n.delimiter, n.delimiters, n.delimiterLazyShow), void t.updateValueState()))
        },
        updateCreditCardPropsByValue: function(e) {
          var t, n = this.properties,
            i = r.Util;
          i.headStr(n.result, 4) !== i.headStr(e, 4) && (t = r.CreditCardDetector.getInfo(e, n.creditCardStrictMode), n.blocks = t.blocks, n.blocksLength = n.blocks.length, n.maxLength = i.getMaxLength(n.blocks), n.creditCardType !== t.type && (n.creditCardType = t.type, n.onCreditCardTypeChanged.call(this, n.creditCardType)))
        },
        updateValueState: function() {
          var e = this,
            t = r.Util,
            n = e.properties;
          if (e.element) {
            var i = e.element.selectionEnd,
              o = e.element.value,
              a = n.result;
            if (i = t.getNextCursorPosition(i, o, a, n.delimiter, n.delimiters), e.isAndroid) return void window.setTimeout((function() {
              e.element.value = a, t.setSelection(e.element, i, n.document, !1), e.callOnValueChanged()
            }), 1);
            e.element.value = a, n.swapHiddenInput && (e.elementSwapHidden.value = e.getRawValue()), t.setSelection(e.element, i, n.document, !1), e.callOnValueChanged()
          }
        },
        callOnValueChanged: function() {
          var e = this,
            t = e.properties;
          t.onValueChanged.call(e, {
            target: {
              name: e.element.name,
              value: t.result,
              rawValue: e.getRawValue()
            }
          })
        },
        setPhoneRegionCode: function(e) {
          var t = this;
          t.properties.phoneRegionCode = e, t.initPhoneFormatter(), t.onChange()
        },
        setRawValue: function(e) {
          var t = this,
            n = t.properties;
          e = null != e ? e.toString() : "", n.numeral && (e = e.replace(".", n.numeralDecimalMark)), n.postDelimiterBackspace = !1, t.element.value = e, t.onInput(e)
        },
        getRawValue: function() {
          var e = this.properties,
            t = r.Util,
            n = this.element.value;
          return e.rawValueTrimPrefix && (n = t.getPrefixStrippedValue(n, e.prefix, e.prefixLength, e.result, e.delimiter, e.delimiters, e.noImmediatePrefix, e.tailPrefix, e.signBeforePrefix)), e.numeral ? e.numeralFormatter.getRawValue(n) : t.stripDelimiters(n, e.delimiter, e.delimiters)
        },
        getISOFormatDate: function() {
          var e = this.properties;
          return e.date ? e.dateFormatter.getISOFormatDate() : ""
        },
        getISOFormatTime: function() {
          var e = this.properties;
          return e.time ? e.timeFormatter.getISOFormatTime() : ""
        },
        getFormattedValue: function() {
          return this.element.value
        },
        destroy: function() {
          var e = this;
          e.element.removeEventListener("input", e.onChangeListener), e.element.removeEventListener("keydown", e.onKeyDownListener), e.element.removeEventListener("focus", e.onFocusListener), e.element.removeEventListener("cut", e.onCutListener), e.element.removeEventListener("copy", e.onCopyListener)
        },
        toString: function() {
          return "[Cleave Object]"
        }
      }, r.NumeralFormatter = n(1), r.DateFormatter = n(2), r.TimeFormatter = n(3), r.PhoneFormatter = n(4), r.CreditCardDetector = n(5), r.Util = n(6), r.DefaultProperties = n(7), ("object" == typeof t && t ? t : window).Cleave = r, e.exports = r
    }).call(t, function() {
      return this
    }())
  }, function(e, t) {
    "use strict";
    var n = function(e, t, r, i, o, a, s, l, c, u) {
      var d = this;
      d.numeralDecimalMark = e || ".", d.numeralIntegerScale = t > 0 ? t : 0, d.numeralDecimalScale = r >= 0 ? r : 2, d.numeralThousandsGroupStyle = i || n.groupStyle.thousand, d.numeralPositiveOnly = !!o, d.stripLeadingZeroes = !1 !== a, d.prefix = s || "" === s ? s : "", d.signBeforePrefix = !!l, d.tailPrefix = !!c, d.delimiter = u || "" === u ? u : ",", d.delimiterRE = u ? new RegExp("\\" + u, "g") : ""
    };
    n.groupStyle = {
      thousand: "thousand",
      lakh: "lakh",
      wan: "wan",
      none: "none"
    }, n.prototype = {
      getRawValue: function(e) {
        return e.replace(this.delimiterRE, "").replace(this.numeralDecimalMark, ".")
      },
      format: function(e) {
        var t, r, i, o, a = this,
          s = "";
        switch (e = e.replace(/[A-Za-z]/g, "").replace(a.numeralDecimalMark, "M").replace(/[^\dM-]/g, "").replace(/^\-/, "N").replace(/\-/g, "").replace("N", a.numeralPositiveOnly ? "" : "-").replace("M", a.numeralDecimalMark), a.stripLeadingZeroes && (e = e.replace(/^(-)?0+(?=\d)/, "$1")), r = "-" === e.slice(0, 1) ? "-" : "", i = void 0 !== a.prefix ? a.signBeforePrefix ? r + a.prefix : a.prefix + r : r, o = e, e.indexOf(a.numeralDecimalMark) >= 0 && (o = (t = e.split(a.numeralDecimalMark))[0], s = a.numeralDecimalMark + t[1].slice(0, a.numeralDecimalScale)), "-" === r && (o = o.slice(1)), a.numeralIntegerScale > 0 && (o = o.slice(0, a.numeralIntegerScale)), a.numeralThousandsGroupStyle) {
          case n.groupStyle.lakh:
            o = o.replace(/(\d)(?=(\d\d)+\d$)/g, "$1" + a.delimiter);
            break;
          case n.groupStyle.wan:
            o = o.replace(/(\d)(?=(\d{4})+$)/g, "$1" + a.delimiter);
            break;
          case n.groupStyle.thousand:
            o = o.replace(/(\d)(?=(\d{3})+$)/g, "$1" + a.delimiter)
        }
        return a.tailPrefix ? r + o.toString() + (a.numeralDecimalScale > 0 ? s.toString() : "") + a.prefix : i + o.toString() + (a.numeralDecimalScale > 0 ? s.toString() : "")
      }
    }, e.exports = n
  }, function(e, t) {
    "use strict";
    var n = function(e, t, n) {
      var r = this;
      r.date = [], r.blocks = [], r.datePattern = e, r.dateMin = t.split("-").reverse().map((function(e) {
        return parseInt(e, 10)
      })), 2 === r.dateMin.length && r.dateMin.unshift(0), r.dateMax = n.split("-").reverse().map((function(e) {
        return parseInt(e, 10)
      })), 2 === r.dateMax.length && r.dateMax.unshift(0), r.initBlocks()
    };
    n.prototype = {
      initBlocks: function() {
        var e = this;
        e.datePattern.forEach((function(t) {
          "Y" === t ? e.blocks.push(4) : e.blocks.push(2)
        }))
      },
      getISOFormatDate: function() {
        var e = this,
          t = e.date;
        return t[2] ? t[2] + "-" + e.addLeadingZero(t[1]) + "-" + e.addLeadingZero(t[0]) : ""
      },
      getBlocks: function() {
        return this.blocks
      },
      getValidatedDate: function(e) {
        var t = this,
          n = "";
        return e = e.replace(/[^\d]/g, ""), t.blocks.forEach((function(r, i) {
          if (e.length > 0) {
            var o = e.slice(0, r),
              a = o.slice(0, 1),
              s = e.slice(r);
            switch (t.datePattern[i]) {
              case "d":
                "00" === o ? o = "01" : parseInt(a, 10) > 3 ? o = "0" + a : parseInt(o, 10) > 31 && (o = "31");
                break;
              case "m":
                "00" === o ? o = "01" : parseInt(a, 10) > 1 ? o = "0" + a : parseInt(o, 10) > 12 && (o = "12")
            }
            n += o, e = s
          }
        })), this.getFixedDateString(n)
      },
      getFixedDateString: function(e) {
        var t, n, r, i = this,
          o = i.datePattern,
          a = [],
          s = 0,
          l = 0,
          c = 0,
          u = 0,
          d = 0,
          p = 0,
          f = !1;
        4 === e.length && "y" !== o[0].toLowerCase() && "y" !== o[1].toLowerCase() && (d = 2 - (u = "d" === o[0] ? 0 : 2), t = parseInt(e.slice(u, u + 2), 10), n = parseInt(e.slice(d, d + 2), 10), a = this.getFixedDate(t, n, 0)), 8 === e.length && (o.forEach((function(e, t) {
          switch (e) {
            case "d":
              s = t;
              break;
            case "m":
              l = t;
              break;
            default:
              c = t
          }
        })), p = 2 * c, u = s <= c ? 2 * s : 2 * s + 2, d = l <= c ? 2 * l : 2 * l + 2, t = parseInt(e.slice(u, u + 2), 10), n = parseInt(e.slice(d, d + 2), 10), r = parseInt(e.slice(p, p + 4), 10), f = 4 === e.slice(p, p + 4).length, a = this.getFixedDate(t, n, r)), 4 !== e.length || "y" !== o[0] && "y" !== o[1] || (p = 2 - (d = "m" === o[0] ? 0 : 2), n = parseInt(e.slice(d, d + 2), 10), r = parseInt(e.slice(p, p + 2), 10), f = 2 === e.slice(p, p + 2).length, a = [0, n, r]), 6 !== e.length || "Y" !== o[0] && "Y" !== o[1] || (p = 2 - .5 * (d = "m" === o[0] ? 0 : 4), n = parseInt(e.slice(d, d + 2), 10), r = parseInt(e.slice(p, p + 4), 10), f = 4 === e.slice(p, p + 4).length, a = [0, n, r]), a = i.getRangeFixedDate(a), i.date = a;
        var h = 0 === a.length ? e : o.reduce((function(e, t) {
          switch (t) {
            case "d":
              return e + (0 === a[0] ? "" : i.addLeadingZero(a[0]));
            case "m":
              return e + (0 === a[1] ? "" : i.addLeadingZero(a[1]));
            case "y":
              return e + (f ? i.addLeadingZeroForYear(a[2], !1) : "");
            case "Y":
              return e + (f ? i.addLeadingZeroForYear(a[2], !0) : "")
          }
        }), "");
        return h
      },
      getRangeFixedDate: function(e) {
        var t = this,
          n = t.datePattern,
          r = t.dateMin || [],
          i = t.dateMax || [];
        return !e.length || r.length < 3 && i.length < 3 || n.find((function(e) {
          return "y" === e.toLowerCase()
        })) && 0 === e[2] ? e : i.length && (i[2] < e[2] || i[2] === e[2] && (i[1] < e[1] || i[1] === e[1] && i[0] < e[0])) ? i : r.length && (r[2] > e[2] || r[2] === e[2] && (r[1] > e[1] || r[1] === e[1] && r[0] > e[0])) ? r : e
      },
      getFixedDate: function(e, t, n) {
        return e = Math.min(e, 31), t = Math.min(t, 12), n = parseInt(n || 0, 10), (t < 7 && t % 2 == 0 || t > 8 && t % 2 == 1) && (e = Math.min(e, 2 === t ? this.isLeapYear(n) ? 29 : 28 : 30)), [e, t, n]
      },
      isLeapYear: function(e) {
        return e % 4 == 0 && e % 100 != 0 || e % 400 == 0
      },
      addLeadingZero: function(e) {
        return (e < 10 ? "0" : "") + e
      },
      addLeadingZeroForYear: function(e, t) {
        return t ? (e < 10 ? "000" : e < 100 ? "00" : e < 1e3 ? "0" : "") + e : (e < 10 ? "0" : "") + e
      }
    }, e.exports = n
  }, function(e, t) {
    "use strict";
    var n = function(e, t) {
      var n = this;
      n.time = [], n.blocks = [], n.timePattern = e, n.timeFormat = t, n.initBlocks()
    };
    n.prototype = {
      initBlocks: function() {
        var e = this;
        e.timePattern.forEach((function() {
          e.blocks.push(2)
        }))
      },
      getISOFormatTime: function() {
        var e = this,
          t = e.time;
        return t[2] ? e.addLeadingZero(t[0]) + ":" + e.addLeadingZero(t[1]) + ":" + e.addLeadingZero(t[2]) : ""
      },
      getBlocks: function() {
        return this.blocks
      },
      getTimeFormatOptions: function() {
        return "12" === String(this.timeFormat) ? {
          maxHourFirstDigit: 1,
          maxHours: 12,
          maxMinutesFirstDigit: 5,
          maxMinutes: 60
        } : {
          maxHourFirstDigit: 2,
          maxHours: 23,
          maxMinutesFirstDigit: 5,
          maxMinutes: 60
        }
      },
      getValidatedTime: function(e) {
        var t = this,
          n = "";
        e = e.replace(/[^\d]/g, "");
        var r = t.getTimeFormatOptions();
        return t.blocks.forEach((function(i, o) {
          if (e.length > 0) {
            var a = e.slice(0, i),
              s = a.slice(0, 1),
              l = e.slice(i);
            switch (t.timePattern[o]) {
              case "h":
                parseInt(s, 10) > r.maxHourFirstDigit ? a = "0" + s : parseInt(a, 10) > r.maxHours && (a = r.maxHours + "");
                break;
              case "m":
              case "s":
                parseInt(s, 10) > r.maxMinutesFirstDigit ? a = "0" + s : parseInt(a, 10) > r.maxMinutes && (a = r.maxMinutes + "")
            }
            n += a, e = l
          }
        })), this.getFixedTimeString(n)
      },
      getFixedTimeString: function(e) {
        var t, n, r, i = this,
          o = i.timePattern,
          a = [],
          s = 0,
          l = 0,
          c = 0,
          u = 0,
          d = 0,
          p = 0;
        return 6 === e.length && (o.forEach((function(e, t) {
          switch (e) {
            case "s":
              s = 2 * t;
              break;
            case "m":
              l = 2 * t;
              break;
            case "h":
              c = 2 * t
          }
        })), p = c, d = l, u = s, t = parseInt(e.slice(u, u + 2), 10), n = parseInt(e.slice(d, d + 2), 10), r = parseInt(e.slice(p, p + 2), 10), a = this.getFixedTime(r, n, t)), 4 === e.length && i.timePattern.indexOf("s") < 0 && (o.forEach((function(e, t) {
          switch (e) {
            case "m":
              l = 2 * t;
              break;
            case "h":
              c = 2 * t
          }
        })), p = c, d = l, t = 0, n = parseInt(e.slice(d, d + 2), 10), r = parseInt(e.slice(p, p + 2), 10), a = this.getFixedTime(r, n, t)), i.time = a, 0 === a.length ? e : o.reduce((function(e, t) {
          switch (t) {
            case "s":
              return e + i.addLeadingZero(a[2]);
            case "m":
              return e + i.addLeadingZero(a[1]);
            case "h":
              return e + i.addLeadingZero(a[0])
          }
        }), "")
      },
      getFixedTime: function(e, t, n) {
        return n = Math.min(parseInt(n || 0, 10), 60), t = Math.min(t, 60), [e = Math.min(e, 60), t, n]
      },
      addLeadingZero: function(e) {
        return (e < 10 ? "0" : "") + e
      }
    }, e.exports = n
  }, function(e, t) {
    "use strict";
    var n = function(e, t) {
      var n = this;
      n.delimiter = t || "" === t ? t : " ", n.delimiterRE = t ? new RegExp("\\" + t, "g") : "", n.formatter = e
    };
    n.prototype = {
      setFormatter: function(e) {
        this.formatter = e
      },
      format: function(e) {
        var t = this;
        t.formatter.clear();
        for (var n, r = "", i = !1, o = 0, a = (e = (e = (e = e.replace(/[^\d+]/g, "")).replace(/^\+/, "B").replace(/\+/g, "").replace("B", "+")).replace(t.delimiterRE, "")).length; o < a; o++) n = t.formatter.inputDigit(e.charAt(o)), /[\s()-]/g.test(n) ? (r = n, i = !0) : i || (r = n);
        return (r = r.replace(/[()]/g, "")).replace(/[\s-]/g, t.delimiter)
      }
    }, e.exports = n
  }, function(e, t) {
    "use strict";
    var n = {
      blocks: {
        uatp: [4, 5, 6],
        amex: [4, 6, 5],
        diners: [4, 6, 4],
        discover: [4, 4, 4, 4],
        mastercard: [4, 4, 4, 4],
        dankort: [4, 4, 4, 4],
        instapayment: [4, 4, 4, 4],
        jcb15: [4, 6, 5],
        jcb: [4, 4, 4, 4],
        maestro: [4, 4, 4, 4],
        visa: [4, 4, 4, 4],
        mir: [4, 4, 4, 4],
        unionPay: [4, 4, 4, 4],
        general: [4, 4, 4, 4]
      },
      re: {
        uatp: /^(?!1800)1\d{0,14}/,
        amex: /^3[47]\d{0,13}/,
        discover: /^(?:6011|65\d{0,2}|64[4-9]\d?)\d{0,12}/,
        diners: /^3(?:0([0-5]|9)|[689]\d?)\d{0,11}/,
        mastercard: /^(5[1-5]\d{0,2}|22[2-9]\d{0,1}|2[3-7]\d{0,2})\d{0,12}/,
        dankort: /^(5019|4175|4571)\d{0,12}/,
        instapayment: /^63[7-9]\d{0,13}/,
        jcb15: /^(?:2131|1800)\d{0,11}/,
        jcb: /^(?:35\d{0,2})\d{0,12}/,
        maestro: /^(?:5[0678]\d{0,2}|6304|67\d{0,2})\d{0,12}/,
        mir: /^220[0-4]\d{0,12}/,
        visa: /^4\d{0,15}/,
        unionPay: /^(62|81)\d{0,14}/
      },
      getStrictBlocks: function(e) {
        var t = e.reduce((function(e, t) {
          return e + t
        }), 0);
        return e.concat(19 - t)
      },
      getInfo: function(e, t) {
        var r = n.blocks,
          i = n.re;
        for (var o in t = !!t, i)
          if (i[o].test(e)) {
            var a = r[o];
            return {
              type: o,
              blocks: t ? this.getStrictBlocks(a) : a
            }
          } return {
          type: "unknown",
          blocks: t ? this.getStrictBlocks(r.general) : r.general
        }
      }
    };
    e.exports = n
  }, function(e, t) {
    "use strict";
    var n = {
      noop: function() {},
      strip: function(e, t) {
        return e.replace(t, "")
      },
      getPostDelimiter: function(e, t, n) {
        if (0 === n.length) return e.slice(-t.length) === t ? t : "";
        var r = "";
        return n.forEach((function(t) {
          e.slice(-t.length) === t && (r = t)
        })), r
      },
      getDelimiterREByDelimiter: function(e) {
        return new RegExp(e.replace(/([.?*+^$[\]\\(){}|-])/g, "\\$1"), "g")
      },
      getNextCursorPosition: function(e, t, n, r, i) {
        return t.length === e ? n.length : e + this.getPositionOffset(e, t, n, r, i)
      },
      getPositionOffset: function(e, t, n, r, i) {
        var o, a, s;
        return o = this.stripDelimiters(t.slice(0, e), r, i), a = this.stripDelimiters(n.slice(0, e), r, i), 0 !== (s = o.length - a.length) ? s / Math.abs(s) : 0
      },
      stripDelimiters: function(e, t, n) {
        var r = this;
        if (0 === n.length) {
          var i = t ? r.getDelimiterREByDelimiter(t) : "";
          return e.replace(i, "")
        }
        return n.forEach((function(t) {
          t.split("").forEach((function(t) {
            e = e.replace(r.getDelimiterREByDelimiter(t), "")
          }))
        })), e
      },
      headStr: function(e, t) {
        return e.slice(0, t)
      },
      getMaxLength: function(e) {
        return e.reduce((function(e, t) {
          return e + t
        }), 0)
      },
      getPrefixStrippedValue: function(e, t, n, r, i, o, a, s, l) {
        if (0 === n) return e;
        if (e === t && "" !== e) return "";
        if (l && "-" == e.slice(0, 1)) {
          var c = "-" == r.slice(0, 1) ? r.slice(1) : r;
          return "-" + this.getPrefixStrippedValue(e.slice(1), t, n, c, i, o, a, s, l)
        }
        if (r.slice(0, n) !== t && !s) return a && !r && e ? e : "";
        if (r.slice(-n) !== t && s) return a && !r && e ? e : "";
        var u = this.stripDelimiters(r, i, o);
        return e.slice(0, n) === t || s ? e.slice(-n) !== t && s ? u.slice(0, -n - 1) : s ? e.slice(0, -n) : e.slice(n) : u.slice(n)
      },
      getFirstDiffIndex: function(e, t) {
        for (var n = 0; e.charAt(n) === t.charAt(n);)
          if ("" === e.charAt(n++)) return -1;
        return n
      },
      getFormattedValue: function(e, t, n, r, i, o) {
        var a = "",
          s = i.length > 0,
          l = "";
        return 0 === n ? e : (t.forEach((function(t, c) {
          if (e.length > 0) {
            var u = e.slice(0, t),
              d = e.slice(t);
            l = s ? i[o ? c - 1 : c] || l : r, o ? (c > 0 && (a += l), a += u) : (a += u, u.length === t && c < n - 1 && (a += l)), e = d
          }
        })), a)
      },
      fixPrefixCursor: function(e, t, n, r) {
        if (e) {
          var i = e.value,
            o = n || r[0] || " ";
          if (e.setSelectionRange && t && !(t.length + o.length <= i.length)) {
            var a = 2 * i.length;
            setTimeout((function() {
              e.setSelectionRange(a, a)
            }), 1)
          }
        }
      },
      checkFullSelection: function(e) {
        try {
          return (window.getSelection() || document.getSelection() || {}).toString().length === e.length
        } catch (e) {}
        return !1
      },
      setSelection: function(e, t, n) {
        if (e === this.getActiveElement(n) && !(e && e.value.length <= t))
          if (e.createTextRange) {
            var r = e.createTextRange();
            r.move("character", t), r.select()
          } else try {
            e.setSelectionRange(t, t)
          } catch (e) {
            console.warn("The input element type does not support selection")
          }
      },
      getActiveElement: function(e) {
        var t = e.activeElement;
        return t && t.shadowRoot ? this.getActiveElement(t.shadowRoot) : t
      },
      isAndroid: function() {
        return navigator && /android/i.test(navigator.userAgent)
      },
      isAndroidBackspaceKeydown: function(e, t) {
        return !!(this.isAndroid() && e && t) && t === e.slice(0, -1)
      }
    };
    e.exports = n
  }, function(e, t) {
    (function(t) {
      "use strict";
      var n = {
        assign: function(e, n) {
          return n = n || {}, (e = e || {}).creditCard = !!n.creditCard, e.creditCardStrictMode = !!n.creditCardStrictMode, e.creditCardType = "", e.onCreditCardTypeChanged = n.onCreditCardTypeChanged || function() {}, e.phone = !!n.phone, e.phoneRegionCode = n.phoneRegionCode || "AU", e.phoneFormatter = {}, e.time = !!n.time, e.timePattern = n.timePattern || ["h", "m", "s"], e.timeFormat = n.timeFormat || "24", e.timeFormatter = {}, e.date = !!n.date, e.datePattern = n.datePattern || ["d", "m", "Y"], e.dateMin = n.dateMin || "", e.dateMax = n.dateMax || "", e.dateFormatter = {}, e.numeral = !!n.numeral, e.numeralIntegerScale = n.numeralIntegerScale > 0 ? n.numeralIntegerScale : 0, e.numeralDecimalScale = n.numeralDecimalScale >= 0 ? n.numeralDecimalScale : 2, e.numeralDecimalMark = n.numeralDecimalMark || ".", e.numeralThousandsGroupStyle = n.numeralThousandsGroupStyle || "thousand", e.numeralPositiveOnly = !!n.numeralPositiveOnly, e.stripLeadingZeroes = !1 !== n.stripLeadingZeroes, e.signBeforePrefix = !!n.signBeforePrefix, e.tailPrefix = !!n.tailPrefix, e.swapHiddenInput = !!n.swapHiddenInput, e.numericOnly = e.creditCard || e.date || !!n.numericOnly, e.uppercase = !!n.uppercase, e.lowercase = !!n.lowercase, e.prefix = e.creditCard || e.date ? "" : n.prefix || "", e.noImmediatePrefix = !!n.noImmediatePrefix, e.prefixLength = e.prefix.length, e.rawValueTrimPrefix = !!n.rawValueTrimPrefix, e.copyDelimiter = !!n.copyDelimiter, e.initValue = void 0 !== n.initValue && null !== n.initValue ? n.initValue.toString() : "", e.delimiter = n.delimiter || "" === n.delimiter ? n.delimiter : n.date ? "/" : n.time ? ":" : n.numeral ? "," : (n.phone, " "), e.delimiterLength = e.delimiter.length, e.delimiterLazyShow = !!n.delimiterLazyShow, e.delimiters = n.delimiters || [], e.blocks = n.blocks || [], e.blocksLength = e.blocks.length, e.root = "object" == typeof t && t ? t : window, e.document = n.document || e.root.document, e.maxLength = 0, e.backspace = !1, e.result = "", e.onValueChanged = n.onValueChanged || function() {}, e
        }
      };
      e.exports = n
    }).call(t, function() {
      return this
    }())
  }])
})),
function(e) {
  "function" == typeof define && define.amd ? define(["jquery"], e) : "object" == typeof module && module.exports ? module.exports = function(t, n) {
    return void 0 === n && (n = "undefined" != typeof window ? require("jquery") : require("jquery")(t)), e(n), n
  } : e(jQuery)
}((function(e) {
  var t, n, r, i, o, a, s, l, c, u, d, p, f, h, m = (e && e.fn && e.fn.select2 && e.fn.select2.amd && (S = e.fn.select2.amd), S && S.requirejs || (S ? n = S : S = {}, l = {}, c = {}, u = {}, d = {}, p = Object.prototype.hasOwnProperty, f = [].slice, h = /\.js$/, a = function(e, t) {
    var n, r, i = w(e),
      o = i[0];
    t = t[1];
    return e = i[1], o && (n = b(o = v(o, t))), o ? e = n && n.normalize ? n.normalize(e, (r = t, function(e) {
      return v(e, r)
    })) : v(e, t) : (o = (i = w(e = v(e, t)))[0], e = i[1], o && (n = b(o))), {
      f: o ? o + "!" + e : e,
      n: e,
      pr: o,
      p: n
    }
  }, s = {
    require: function(e) {
      return y(e)
    },
    exports: function(e) {
      var t = l[e];
      return void 0 !== t ? t : l[e] = {}
    },
    module: function(e) {
      return {
        id: e,
        uri: "",
        exports: l[e],
        config: (t = e, function() {
          return u && u.config && u.config[t] || {}
        })
      };
      var t
    }
  }, i = function(e, t, n, i) {
    var o, u, p, f, h, m = [],
      v = typeof n,
      w = x(i = i || e);
    if ("undefined" == v || "function" == v) {
      for (t = !t.length && n.length ? ["require", "exports", "module"] : t, f = 0; f < t.length; f += 1)
        if ("require" === (u = (p = a(t[f], w)).f)) m[f] = s.require(e);
        else if ("exports" === u) m[f] = s.exports(e), h = !0;
      else if ("module" === u) o = m[f] = s.module(e);
      else if (g(l, u) || g(c, u) || g(d, u)) m[f] = b(u);
      else {
        if (!p.p) throw new Error(e + " missing " + u);
        p.p.load(p.n, y(i, !0), function(e) {
          return function(t) {
            l[e] = t
          }
        }(u), {}), m[f] = l[u]
      }
      v = n ? n.apply(l[e], m) : void 0, e && (o && o.exports !== r && o.exports !== l[e] ? l[e] = o.exports : v === r && h || (l[e] = v))
    } else e && (l[e] = n)
  }, t = n = o = function(e, t, n, l, c) {
    if ("string" == typeof e) return s[e] ? s[e](t) : b(a(e, x(t)).f);
    if (!e.splice) {
      if ((u = e).deps && o(u.deps, u.callback), !t) return;
      t.splice ? (e = t, t = n, n = null) : e = r
    }
    return t = t || function() {}, "function" == typeof n && (n = l, l = c), l ? i(r, e, t, n) : setTimeout((function() {
      i(r, e, t, n)
    }), 4), o
  }, o.config = function(e) {
    return o(e)
  }, t._defined = l, (m = function(e, t, n) {
    if ("string" != typeof e) throw new Error("See almond README: incorrect module build, no module name");
    t.splice || (n = t, t = []), g(l, e) || g(c, e) || (c[e] = [e, t, n])
  }).amd = {
    jQuery: !0
  }, S.requirejs = t, S.require = n, S.define = m), S.define("almond", (function() {})), S.define("jquery", [], (function() {
    var t = e || $;
    return null == t && console && console.error && console.error("Select2: An instance of jQuery or a jQuery-compatible library was not found. Make sure that you are including jQuery before Select2 on your web page."), t
  })), S.define("select2/utils", ["jquery"], (function(e) {
    var t = {};

    function n(e) {
      var t, n = e.prototype,
        r = [];
      for (t in n) "function" == typeof n[t] && "constructor" !== t && r.push(t);
      return r
    }

    function r() {
      this.listeners = {}
    }
    t.Extend = function(e, t) {
      var n, r = {}.hasOwnProperty;

      function i() {
        this.constructor = e
      }
      for (n in t) r.call(t, n) && (e[n] = t[n]);
      return i.prototype = t.prototype, e.prototype = new i, e.__super__ = t.prototype, e
    }, t.Decorate = function(e, t) {
      var r = n(t),
        i = n(e);

      function o() {
        var n = Array.prototype.unshift,
          r = t.prototype.constructor.length,
          i = e.prototype.constructor;
        0 < r && (n.call(arguments, e.prototype.constructor), i = t.prototype.constructor), i.apply(this, arguments)
      }
      t.displayName = e.displayName, o.prototype = new function() {
        this.constructor = o
      };
      for (var a = 0; a < i.length; a++) {
        var s = i[a];
        o.prototype[s] = e.prototype[s]
      }
      for (var l = 0; l < r.length; l++) {
        var c = r[l];
        o.prototype[c] = function(e) {
          var n = function() {};
          e in o.prototype && (n = o.prototype[e]);
          var r = t.prototype[e];
          return function() {
            return Array.prototype.unshift.call(arguments, n), r.apply(this, arguments)
          }
        }(c)
      }
      return o
    }, r.prototype.on = function(e, t) {
      this.listeners = this.listeners || {}, e in this.listeners ? this.listeners[e].push(t) : this.listeners[e] = [t]
    }, r.prototype.trigger = function(e) {
      var t = Array.prototype.slice,
        n = t.call(arguments, 1);
      this.listeners = this.listeners || {}, null == n && (n = []), 0 === n.length && n.push({}), (n[0]._type = e) in this.listeners && this.invoke(this.listeners[e], t.call(arguments, 1)), "*" in this.listeners && this.invoke(this.listeners["*"], arguments)
    }, r.prototype.invoke = function(e, t) {
      for (var n = 0, r = e.length; n < r; n++) e[n].apply(this, t)
    }, t.Observable = r, t.generateChars = function(e) {
      for (var t = "", n = 0; n < e; n++) t += Math.floor(36 * Math.random()).toString(36);
      return t
    }, t.bind = function(e, t) {
      return function() {
        e.apply(t, arguments)
      }
    }, t._convertData = function(e) {
      for (var t in e) {
        var n = t.split("-"),
          r = e;
        if (1 !== n.length) {
          for (var i = 0; i < n.length; i++) {
            var o = n[i];
            (o = o.substring(0, 1).toLowerCase() + o.substring(1)) in r || (r[o] = {}), i == n.length - 1 && (r[o] = e[t]), r = r[o]
          }
          delete e[t]
        }
      }
      return e
    }, t.hasScroll = function(t, n) {
      var r = e(n),
        i = n.style.overflowX,
        o = n.style.overflowY;
      return (i !== o || "hidden" !== o && "visible" !== o) && ("scroll" === i || "scroll" === o || r.innerHeight() < n.scrollHeight || r.innerWidth() < n.scrollWidth)
    }, t.escapeMarkup = function(e) {
      var t = {
        "\\": "&#92;",
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;",
        "/": "&#47;"
      };
      return "string" != typeof e ? e : String(e).replace(/[&<>"'\/\\]/g, (function(e) {
        return t[e]
      }))
    }, t.__cache = {};
    var i = 0;
    return t.GetUniqueElementId = function(e) {
      var n = e.getAttribute("data-select2-id");
      return null != n || (n = e.id ? "select2-data-" + e.id : "select2-data-" + (++i).toString() + "-" + t.generateChars(4), e.setAttribute("data-select2-id", n)), n
    }, t.StoreData = function(e, n, r) {
      e = t.GetUniqueElementId(e), t.__cache[e] || (t.__cache[e] = {}), t.__cache[e][n] = r
    }, t.GetData = function(n, r) {
      var i = t.GetUniqueElementId(n);
      return r ? t.__cache[i] && null != t.__cache[i][r] ? t.__cache[i][r] : e(n).data(r) : t.__cache[i]
    }, t.RemoveData = function(e) {
      var n = t.GetUniqueElementId(e);
      null != t.__cache[n] && delete t.__cache[n], e.removeAttribute("data-select2-id")
    }, t.copyNonInternalCssClasses = function(e, t) {
      var n = (n = e.getAttribute("class").trim().split(/\s+/)).filter((function(e) {
        return 0 === e.indexOf("select2-")
      }));
      t = (t = t.getAttribute("class").trim().split(/\s+/)).filter((function(e) {
        return 0 !== e.indexOf("select2-")
      })), t = n.concat(t);
      e.setAttribute("class", t.join(" "))
    }, t
  })), S.define("select2/results", ["jquery", "./utils"], (function(e, t) {
    function n(e, t, r) {
      this.$element = e, this.data = r, this.options = t, n.__super__.constructor.call(this)
    }
    return t.Extend(n, t.Observable), n.prototype.render = function() {
      var t = e('<ul class="select2-results__options" role="listbox"></ul>');
      return this.options.get("multiple") && t.attr("aria-multiselectable", "true"), this.$results = t
    }, n.prototype.clear = function() {
      this.$results.empty()
    }, n.prototype.displayMessage = function(t) {
      var n = this.options.get("escapeMarkup");
      this.clear(), this.hideLoading();
      var r = e('<li role="alert" aria-live="assertive" class="select2-results__option"></li>'),
        i = this.options.get("translations").get(t.message);
      r.append(n(i(t.args))), r[0].className += " select2-results__message", this.$results.append(r)
    }, n.prototype.hideMessages = function() {
      this.$results.find(".select2-results__message").remove()
    }, n.prototype.append = function(e) {
      this.hideLoading();
      var t = [];
      if (null != e.results && 0 !== e.results.length) {
        e.results = this.sort(e.results);
        for (var n = 0; n < e.results.length; n++) {
          var r = e.results[n];
          r = this.option(r);
          t.push(r)
        }
        this.$results.append(t)
      } else 0 === this.$results.children().length && this.trigger("results:message", {
        message: "noResults"
      })
    }, n.prototype.position = function(e, t) {
      t.find(".select2-results").append(e)
    }, n.prototype.sort = function(e) {
      return this.options.get("sorter")(e)
    }, n.prototype.highlightFirstItem = function() {
      var e = this.$results.find(".select2-results__option--selectable"),
        t = e.filter(".select2-results__option--selected");
      (0 < t.length ? t : e).first().trigger("mouseenter"), this.ensureHighlightVisible()
    }, n.prototype.setClasses = function() {
      var n = this;
      this.data.current((function(r) {
        var i = r.map((function(e) {
          return e.id.toString()
        }));
        n.$results.find(".select2-results__option--selectable").each((function() {
          var n = e(this),
            r = t.GetData(this, "data"),
            o = "" + r.id;
          null != r.element && r.element.selected || null == r.element && -1 < i.indexOf(o) ? (this.classList.add("select2-results__option--selected"), n.attr("aria-selected", "true")) : (this.classList.remove("select2-results__option--selected"), n.attr("aria-selected", "false"))
        }))
      }))
    }, n.prototype.showLoading = function(e) {
      this.hideLoading(), e = {
        disabled: !0,
        loading: !0,
        text: this.options.get("translations").get("searching")(e)
      }, (e = this.option(e)).className += " loading-results", this.$results.prepend(e)
    }, n.prototype.hideLoading = function() {
      this.$results.find(".loading-results").remove()
    }, n.prototype.option = function(n) {
      var r = document.createElement("li");
      r.classList.add("select2-results__option"), r.classList.add("select2-results__option--selectable");
      var i, o = {
          role: "option"
        },
        a = window.Element.prototype.matches || window.Element.prototype.msMatchesSelector || window.Element.prototype.webkitMatchesSelector;
      for (i in (null != n.element && a.call(n.element, ":disabled") || null == n.element && n.disabled) && (o["aria-disabled"] = "true", r.classList.remove("select2-results__option--selectable"), r.classList.add("select2-results__option--disabled")), null == n.id && r.classList.remove("select2-results__option--selectable"), null != n._resultId && (r.id = n._resultId), n.title && (r.title = n.title), n.children && (o.role = "group", o["aria-label"] = n.text, r.classList.remove("select2-results__option--selectable"), r.classList.add("select2-results__option--group")), o) {
        var s = o[i];
        r.setAttribute(i, s)
      }
      if (n.children) {
        var l = e(r),
          c = document.createElement("strong");
        c.className = "select2-results__group", this.template(n, c);
        for (var u = [], d = 0; d < n.children.length; d++) {
          var p = n.children[d];
          p = this.option(p);
          u.push(p)
        }(a = e("<ul></ul>", {
          class: "select2-results__options select2-results__options--nested",
          role: "none"
        })).append(u), l.append(c), l.append(a)
      } else this.template(n, r);
      return t.StoreData(r, "data", n), r
    }, n.prototype.bind = function(n, r) {
      var i = this,
        o = n.id + "-results";
      this.$results.attr("id", o), n.on("results:all", (function(e) {
        i.clear(), i.append(e.data), n.isOpen() && (i.setClasses(), i.highlightFirstItem())
      })), n.on("results:append", (function(e) {
        i.append(e.data), n.isOpen() && i.setClasses()
      })), n.on("query", (function(e) {
        i.hideMessages(), i.showLoading(e)
      })), n.on("select", (function() {
        n.isOpen() && (i.setClasses(), i.options.get("scrollAfterSelect") && i.highlightFirstItem())
      })), n.on("unselect", (function() {
        n.isOpen() && (i.setClasses(), i.options.get("scrollAfterSelect") && i.highlightFirstItem())
      })), n.on("open", (function() {
        i.$results.attr("aria-expanded", "true"), i.$results.attr("aria-hidden", "false"), i.setClasses(), i.ensureHighlightVisible()
      })), n.on("close", (function() {
        i.$results.attr("aria-expanded", "false"), i.$results.attr("aria-hidden", "true"), i.$results.removeAttr("aria-activedescendant")
      })), n.on("results:toggle", (function() {
        var e = i.getHighlightedResults();
        0 !== e.length && e.trigger("mouseup")
      })), n.on("results:select", (function() {
        var e, n = i.getHighlightedResults();
        0 !== n.length && (e = t.GetData(n[0], "data"), n.hasClass("select2-results__option--selected") ? i.trigger("close", {}) : i.trigger("select", {
          data: e
        }))
      })), n.on("results:previous", (function() {
        var e, t = i.getHighlightedResults(),
          n = i.$results.find(".select2-results__option--selectable"),
          r = n.index(t);
        r <= 0 || (e = r - 1, 0 === t.length && (e = 0), (r = n.eq(e)).trigger("mouseenter"), t = i.$results.offset().top, n = r.offset().top, r = i.$results.scrollTop() + (n - t), 0 === e ? i.$results.scrollTop(0) : n - t < 0 && i.$results.scrollTop(r))
      })), n.on("results:next", (function() {
        var e, t = i.getHighlightedResults(),
          n = i.$results.find(".select2-results__option--selectable"),
          r = n.index(t) + 1;
        r >= n.length || ((e = n.eq(r)).trigger("mouseenter"), t = i.$results.offset().top + i.$results.outerHeight(!1), n = e.offset().top + e.outerHeight(!1), e = i.$results.scrollTop() + n - t, 0 === r ? i.$results.scrollTop(0) : t < n && i.$results.scrollTop(e))
      })), n.on("results:focus", (function(e) {
        e.element[0].classList.add("select2-results__option--highlighted"), e.element[0].setAttribute("aria-selected", "true")
      })), n.on("results:message", (function(e) {
        i.displayMessage(e)
      })), e.fn.mousewheel && this.$results.on("mousewheel", (function(e) {
        var t = i.$results.scrollTop(),
          n = i.$results.get(0).scrollHeight - t + e.deltaY;
        t = 0 < e.deltaY && t - e.deltaY <= 0, n = e.deltaY < 0 && n <= i.$results.height();
        t ? (i.$results.scrollTop(0), e.preventDefault(), e.stopPropagation()) : n && (i.$results.scrollTop(i.$results.get(0).scrollHeight - i.$results.height()), e.preventDefault(), e.stopPropagation())
      })), this.$results.on("mouseup", ".select2-results__option--selectable", (function(n) {
        var r = e(this),
          o = t.GetData(this, "data");
        r.hasClass("select2-results__option--selected") ? i.options.get("multiple") ? i.trigger("unselect", {
          originalEvent: n,
          data: o
        }) : i.trigger("close", {}) : i.trigger("select", {
          originalEvent: n,
          data: o
        })
      })), this.$results.on("mouseenter", ".select2-results__option--selectable", (function(n) {
        var r = t.GetData(this, "data");
        i.getHighlightedResults().removeClass("select2-results__option--highlighted").attr("aria-selected", "false"), i.trigger("results:focus", {
          data: r,
          element: e(this)
        })
      }))
    }, n.prototype.getHighlightedResults = function() {
      return this.$results.find(".select2-results__option--highlighted")
    }, n.prototype.destroy = function() {
      this.$results.remove()
    }, n.prototype.ensureHighlightVisible = function() {
      var e, t, n, r, i = this.getHighlightedResults();
      0 !== i.length && (e = this.$results.find(".select2-results__option--selectable").index(i), r = this.$results.offset().top, t = i.offset().top, n = this.$results.scrollTop() + (t - r), r = t - r, n -= 2 * i.outerHeight(!1), e <= 2 ? this.$results.scrollTop(0) : (r > this.$results.outerHeight() || r < 0) && this.$results.scrollTop(n))
    }, n.prototype.template = function(t, n) {
      var r = this.options.get("templateResult"),
        i = this.options.get("escapeMarkup");
      null == (t = r(t, n)) ? n.style.display = "none" : "string" == typeof t ? n.innerHTML = i(t) : e(n).append(t)
    }, n
  })), S.define("select2/keys", [], (function() {
    return {
      BACKSPACE: 8,
      TAB: 9,
      ENTER: 13,
      SHIFT: 16,
      CTRL: 17,
      ALT: 18,
      ESC: 27,
      SPACE: 32,
      PAGE_UP: 33,
      PAGE_DOWN: 34,
      END: 35,
      HOME: 36,
      LEFT: 37,
      UP: 38,
      RIGHT: 39,
      DOWN: 40,
      DELETE: 46
    }
  })), S.define("select2/selection/base", ["jquery", "../utils", "../keys"], (function(e, t, n) {
    function r(e, t) {
      this.$element = e, this.options = t, r.__super__.constructor.call(this)
    }
    return t.Extend(r, t.Observable), r.prototype.render = function() {
      var n = e('<span class="select2-selection" role="combobox"  aria-haspopup="true" aria-expanded="false"></span>');
      return this._tabindex = 0, null != t.GetData(this.$element[0], "old-tabindex") ? this._tabindex = t.GetData(this.$element[0], "old-tabindex") : null != this.$element.attr("tabindex") && (this._tabindex = this.$element.attr("tabindex")), n.attr("title", this.$element.attr("title")), n.attr("tabindex", this._tabindex), n.attr("aria-disabled", "false"), this.$selection = n
    }, r.prototype.bind = function(e, t) {
      var r = this,
        i = e.id + "-results";
      this.container = e, this.$selection.on("focus", (function(e) {
        r.trigger("focus", e)
      })), this.$selection.on("blur", (function(e) {
        r._handleBlur(e)
      })), this.$selection.on("keydown", (function(e) {
        r.trigger("keypress", e), e.which === n.SPACE && e.preventDefault()
      })), e.on("results:focus", (function(e) {
        r.$selection.attr("aria-activedescendant", e.data._resultId)
      })), e.on("selection:update", (function(e) {
        r.update(e.data)
      })), e.on("open", (function() {
        r.$selection.attr("aria-expanded", "true"), r.$selection.attr("aria-owns", i), r._attachCloseHandler(e)
      })), e.on("close", (function() {
        r.$selection.attr("aria-expanded", "false"), r.$selection.removeAttr("aria-activedescendant"), r.$selection.removeAttr("aria-owns"), r.$selection.trigger("focus"), r._detachCloseHandler(e)
      })), e.on("enable", (function() {
        r.$selection.attr("tabindex", r._tabindex), r.$selection.attr("aria-disabled", "false")
      })), e.on("disable", (function() {
        r.$selection.attr("tabindex", "-1"), r.$selection.attr("aria-disabled", "true")
      }))
    }, r.prototype._handleBlur = function(t) {
      var n = this;
      window.setTimeout((function() {
        document.activeElement == n.$selection[0] || e.contains(n.$selection[0], document.activeElement) || n.trigger("blur", t)
      }), 1)
    }, r.prototype._attachCloseHandler = function(n) {
      e(document.body).on("mousedown.select2." + n.id, (function(n) {
        var r = e(n.target).closest(".select2");
        e(".select2.select2-container--open").each((function() {
          this != r[0] && t.GetData(this, "element").select2("close")
        }))
      }))
    }, r.prototype._detachCloseHandler = function(t) {
      e(document.body).off("mousedown.select2." + t.id)
    }, r.prototype.position = function(e, t) {
      t.find(".selection").append(e)
    }, r.prototype.destroy = function() {
      this._detachCloseHandler(this.container)
    }, r.prototype.update = function(e) {
      throw new Error("The `update` method must be defined in child classes.")
    }, r.prototype.isEnabled = function() {
      return !this.isDisabled()
    }, r.prototype.isDisabled = function() {
      return this.options.get("disabled")
    }, r
  })), S.define("select2/selection/single", ["jquery", "./base", "../utils", "../keys"], (function(e, t, n, r) {
    function i() {
      i.__super__.constructor.apply(this, arguments)
    }
    return n.Extend(i, t), i.prototype.render = function() {
      var e = i.__super__.render.call(this);
      return e[0].classList.add("select2-selection--single"), e.html('<span class="select2-selection__rendered"></span><span class="select2-selection__arrow" role="presentation"><b role="presentation"></b></span>'), e
    }, i.prototype.bind = function(e, t) {
      var n = this;
      i.__super__.bind.apply(this, arguments);
      var r = e.id + "-container";
      this.$selection.find(".select2-selection__rendered").attr("id", r).attr("role", "textbox").attr("aria-readonly", "true"), this.$selection.attr("aria-labelledby", r), this.$selection.attr("aria-controls", r), this.$selection.on("mousedown", (function(e) {
        1 === e.which && n.trigger("toggle", {
          originalEvent: e
        })
      })), this.$selection.on("focus", (function(e) {})), this.$selection.on("blur", (function(e) {})), e.on("focus", (function(t) {
        e.isOpen() || n.$selection.trigger("focus")
      }))
    }, i.prototype.clear = function() {
      var e = this.$selection.find(".select2-selection__rendered");
      e.empty(), e.removeAttr("title")
    }, i.prototype.display = function(e, t) {
      var n = this.options.get("templateSelection");
      return this.options.get("escapeMarkup")(n(e, t))
    }, i.prototype.selectionContainer = function() {
      return e("<span></span>")
    }, i.prototype.update = function(e) {
      var t, n;
      0 !== e.length ? (n = e[0], t = this.$selection.find(".select2-selection__rendered"), e = this.display(n, t), t.empty().append(e), (n = n.title || n.text) ? t.attr("title", n) : t.removeAttr("title")) : this.clear()
    }, i
  })), S.define("select2/selection/multiple", ["jquery", "./base", "../utils"], (function(e, t, n) {
    function r(e, t) {
      r.__super__.constructor.apply(this, arguments)
    }
    return n.Extend(r, t), r.prototype.render = function() {
      var e = r.__super__.render.call(this);
      return e[0].classList.add("select2-selection--multiple"), e.html('<ul class="select2-selection__rendered"></ul>'), e
    }, r.prototype.bind = function(t, i) {
      var o = this;
      r.__super__.bind.apply(this, arguments);
      var a = t.id + "-container";
      this.$selection.find(".select2-selection__rendered").attr("id", a), this.$selection.on("click", (function(e) {
        o.trigger("toggle", {
          originalEvent: e
        })
      })), this.$selection.on("click", ".select2-selection__choice__remove", (function(t) {
        var r;
        o.isDisabled() || (r = e(this).parent(), r = n.GetData(r[0], "data"), o.trigger("unselect", {
          originalEvent: t,
          data: r
        }))
      })), this.$selection.on("keydown", ".select2-selection__choice__remove", (function(e) {
        o.isDisabled() || e.stopPropagation()
      }))
    }, r.prototype.clear = function() {
      var e = this.$selection.find(".select2-selection__rendered");
      e.empty(), e.removeAttr("title")
    }, r.prototype.display = function(e, t) {
      var n = this.options.get("templateSelection");
      return this.options.get("escapeMarkup")(n(e, t))
    }, r.prototype.selectionContainer = function() {
      return e('<li class="select2-selection__choice"><button type="button" class="select2-selection__choice__remove" tabindex="-1"><span aria-hidden="true">&times;</span></button><span class="select2-selection__choice__display"></span></li>')
    }, r.prototype.update = function(e) {
      if (this.clear(), 0 !== e.length) {
        for (var t = [], r = this.$selection.find(".select2-selection__rendered").attr("id") + "-choice-", i = 0; i < e.length; i++) {
          var o = e[i],
            a = this.selectionContainer(),
            s = this.display(o, a),
            l = r + n.generateChars(4) + "-";
          o.id ? l += o.id : l += n.generateChars(4), a.find(".select2-selection__choice__display").append(s).attr("id", l);
          var c = o.title || o.text;
          c && a.attr("title", c), s = this.options.get("translations").get("removeItem"), (c = a.find(".select2-selection__choice__remove")).attr("title", s()), c.attr("aria-label", s()), c.attr("aria-describedby", l), n.StoreData(a[0], "data", o), t.push(a)
        }
        this.$selection.find(".select2-selection__rendered").append(t)
      }
    }, r
  })), S.define("select2/selection/placeholder", [], (function() {
    function e(e, t, n) {
      this.placeholder = this.normalizePlaceholder(n.get("placeholder")), e.call(this, t, n)
    }
    return e.prototype.normalizePlaceholder = function(e, t) {
      return "string" == typeof t && (t = {
        id: "",
        text: t
      }), t
    }, e.prototype.createPlaceholder = function(e, t) {
      var n = this.selectionContainer();
      return n.html(this.display(t)), n[0].classList.add("select2-selection__placeholder"), n[0].classList.remove("select2-selection__choice"), t = t.title || t.text || n.text(), this.$selection.find(".select2-selection__rendered").attr("title", t), n
    }, e.prototype.update = function(e, t) {
      var n = 1 == t.length && t[0].id != this.placeholder.id;
      if (1 < t.length || n) return e.call(this, t);
      this.clear(), t = this.createPlaceholder(this.placeholder), this.$selection.find(".select2-selection__rendered").append(t)
    }, e
  })), S.define("select2/selection/allowClear", ["jquery", "../keys", "../utils"], (function(e, t, n) {
    function r() {}
    return r.prototype.bind = function(e, t, n) {
      var r = this;
      e.call(this, t, n), null == this.placeholder && this.options.get("debug") && window.console && console.error && console.error("Select2: The `allowClear` option should be used in combination with the `placeholder` option."), this.$selection.on("mousedown", ".select2-selection__clear", (function(e) {
        r._handleClear(e)
      })), t.on("keypress", (function(e) {
        r._handleKeyboardClear(e, t)
      }))
    }, r.prototype._handleClear = function(e, t) {
      if (!this.isDisabled()) {
        var r = this.$selection.find(".select2-selection__clear");
        if (0 !== r.length) {
          t.stopPropagation();
          var i = n.GetData(r[0], "data"),
            o = this.$element.val();
          this.$element.val(this.placeholder.id);
          var a = {
            data: i
          };
          if (this.trigger("clear", a), a.prevented) this.$element.val(o);
          else {
            for (var s = 0; s < i.length; s++)
              if (a = {
                  data: i[s]
                }, this.trigger("unselect", a), a.prevented) return void this.$element.val(o);
            this.$element.trigger("input").trigger("change"), this.trigger("toggle", {})
          }
        }
      }
    }, r.prototype._handleKeyboardClear = function(e, n, r) {
      r.isOpen() || n.which != t.DELETE && n.which != t.BACKSPACE || this._handleClear(n)
    }, r.prototype.update = function(t, r) {
      var i, o;
      t.call(this, r), this.$selection.find(".select2-selection__clear").remove(), this.$selection[0].classList.remove("select2-selection--clearable"), 0 < this.$selection.find(".select2-selection__placeholder").length || 0 === r.length || (i = this.$selection.find(".select2-selection__rendered").attr("id"), o = this.options.get("translations").get("removeAllItems"), (t = e('<button type="button" class="select2-selection__clear" tabindex="-1"><span aria-hidden="true">&times;</span></button>')).attr("title", o()), t.attr("aria-label", o()), t.attr("aria-describedby", i), n.StoreData(t[0], "data", r), this.$selection.prepend(t), this.$selection[0].classList.add("select2-selection--clearable"))
    }, r
  })), S.define("select2/selection/search", ["jquery", "../utils", "../keys"], (function(e, t, n) {
    function r(e, t, n) {
      e.call(this, t, n)
    }
    return r.prototype.render = function(t) {
      var n = this.options.get("translations").get("search"),
        r = e('<span class="select2-search select2-search--inline"><textarea class="select2-search__field" type="search" tabindex="-1" autocorrect="off" autocapitalize="none" spellcheck="false" role="searchbox" aria-autocomplete="list" ></textarea></span>');
      return this.$searchContainer = r, this.$search = r.find("textarea"), this.$search.prop("autocomplete", this.options.get("autocomplete")), this.$search.attr("aria-label", n()), t = t.call(this), this._transferTabIndex(), t.append(this.$searchContainer), t
    }, r.prototype.bind = function(e, r, i) {
      var o = this,
        a = r.id + "-results",
        s = r.id + "-container";
      e.call(this, r, i), o.$search.attr("aria-describedby", s), r.on("open", (function() {
        o.$search.attr("aria-controls", a), o.$search.trigger("focus")
      })), r.on("close", (function() {
        o.$search.val(""), o.resizeSearch(), o.$search.removeAttr("aria-controls"), o.$search.removeAttr("aria-activedescendant"), o.$search.trigger("focus")
      })), r.on("enable", (function() {
        o.$search.prop("disabled", !1), o._transferTabIndex()
      })), r.on("disable", (function() {
        o.$search.prop("disabled", !0)
      })), r.on("focus", (function(e) {
        o.$search.trigger("focus")
      })), r.on("results:focus", (function(e) {
        e.data._resultId ? o.$search.attr("aria-activedescendant", e.data._resultId) : o.$search.removeAttr("aria-activedescendant")
      })), this.$selection.on("focusin", ".select2-search--inline", (function(e) {
        o.trigger("focus", e)
      })), this.$selection.on("focusout", ".select2-search--inline", (function(e) {
        o._handleBlur(e)
      })), this.$selection.on("keydown", ".select2-search--inline", (function(e) {
        var r;
        e.stopPropagation(), o.trigger("keypress", e), o._keyUpPrevented = e.isDefaultPrevented(), e.which !== n.BACKSPACE || "" !== o.$search.val() || 0 < (r = o.$selection.find(".select2-selection__choice").last()).length && (r = t.GetData(r[0], "data"), o.searchRemoveChoice(r), e.preventDefault())
      })), this.$selection.on("click", ".select2-search--inline", (function(e) {
        o.$search.val() && e.stopPropagation()
      }));
      var l = (r = document.documentMode) && r <= 11;
      this.$selection.on("input.searchcheck", ".select2-search--inline", (function(e) {
        l ? o.$selection.off("input.search input.searchcheck") : o.$selection.off("keyup.search")
      })), this.$selection.on("keyup.search input.search", ".select2-search--inline", (function(e) {
        var t;
        l && "input" === e.type ? o.$selection.off("input.search input.searchcheck") : (t = e.which) != n.SHIFT && t != n.CTRL && t != n.ALT && t != n.TAB && o.handleSearch(e)
      }))
    }, r.prototype._transferTabIndex = function(e) {
      this.$search.attr("tabindex", this.$selection.attr("tabindex")), this.$selection.attr("tabindex", "-1")
    }, r.prototype.createPlaceholder = function(e, t) {
      this.$search.attr("placeholder", t.text)
    }, r.prototype.update = function(e, t) {
      var n = this.$search[0] == document.activeElement;
      this.$search.attr("placeholder", ""), e.call(this, t), this.resizeSearch(), n && this.$search.trigger("focus")
    }, r.prototype.handleSearch = function() {
      var e;
      this.resizeSearch(), this._keyUpPrevented || (e = this.$search.val(), this.trigger("query", {
        term: e
      })), this._keyUpPrevented = !1
    }, r.prototype.searchRemoveChoice = function(e, t) {
      this.trigger("unselect", {
        data: t
      }), this.$search.val(t.text), this.handleSearch()
    }, r.prototype.resizeSearch = function() {
      this.$search.css("width", "25px");
      var e = "100%";
      "" === this.$search.attr("placeholder") && (e = .75 * (this.$search.val().length + 1) + "em"), this.$search.css("width", e)
    }, r
  })), S.define("select2/selection/selectionCss", ["../utils"], (function(e) {
    function t() {}
    return t.prototype.render = function(t) {
      var n = t.call(this);
      return -1 !== (t = this.options.get("selectionCssClass") || "").indexOf(":all:") && (t = t.replace(":all:", ""), e.copyNonInternalCssClasses(n[0], this.$element[0])), n.addClass(t), n
    }, t
  })), S.define("select2/selection/eventRelay", ["jquery"], (function(e) {
    function t() {}
    return t.prototype.bind = function(t, n, r) {
      var i = this,
        o = ["open", "opening", "close", "closing", "select", "selecting", "unselect", "unselecting", "clear", "clearing"],
        a = ["opening", "closing", "selecting", "unselecting", "clearing"];
      t.call(this, n, r), n.on("*", (function(t, n) {
        var r; - 1 !== o.indexOf(t) && (n = n || {}, r = e.Event("select2:" + t, {
          params: n
        }), i.$element.trigger(r), -1 !== a.indexOf(t) && (n.prevented = r.isDefaultPrevented()))
      }))
    }, t
  })), S.define("select2/translation", ["jquery", "require"], (function(e, t) {
    function n(e) {
      this.dict = e || {}
    }
    return n.prototype.all = function() {
      return this.dict
    }, n.prototype.get = function(e) {
      return this.dict[e]
    }, n.prototype.extend = function(t) {
      this.dict = e.extend({}, t.all(), this.dict)
    }, n._cache = {}, n.loadPath = function(e) {
      var r;
      return e in n._cache || (r = t(e), n._cache[e] = r), new n(n._cache[e])
    }, n
  })), S.define("select2/diacritics", [], (function() {
    return {
      "Ⓐ": "A",
      "Ａ": "A",
      "À": "A",
      "Á": "A",
      "Â": "A",
      "Ầ": "A",
      "Ấ": "A",
      "Ẫ": "A",
      "Ẩ": "A",
      "Ã": "A",
      "Ā": "A",
      "Ă": "A",
      "Ằ": "A",
      "Ắ": "A",
      "Ẵ": "A",
      "Ẳ": "A",
      "Ȧ": "A",
      "Ǡ": "A",
      "Ä": "A",
      "Ǟ": "A",
      "Ả": "A",
      "Å": "A",
      "Ǻ": "A",
      "Ǎ": "A",
      "Ȁ": "A",
      "Ȃ": "A",
      "Ạ": "A",
      "Ậ": "A",
      "Ặ": "A",
      "Ḁ": "A",
      "Ą": "A",
      "Ⱥ": "A",
      "Ɐ": "A",
      "Ꜳ": "AA",
      "Æ": "AE",
      "Ǽ": "AE",
      "Ǣ": "AE",
      "Ꜵ": "AO",
      "Ꜷ": "AU",
      "Ꜹ": "AV",
      "Ꜻ": "AV",
      "Ꜽ": "AY",
      "Ⓑ": "B",
      "Ｂ": "B",
      "Ḃ": "B",
      "Ḅ": "B",
      "Ḇ": "B",
      "Ƀ": "B",
      "Ƃ": "B",
      "Ɓ": "B",
      "Ⓒ": "C",
      "Ｃ": "C",
      "Ć": "C",
      "Ĉ": "C",
      "Ċ": "C",
      "Č": "C",
      "Ç": "C",
      "Ḉ": "C",
      "Ƈ": "C",
      "Ȼ": "C",
      "Ꜿ": "C",
      "Ⓓ": "D",
      "Ｄ": "D",
      "Ḋ": "D",
      "Ď": "D",
      "Ḍ": "D",
      "Ḑ": "D",
      "Ḓ": "D",
      "Ḏ": "D",
      "Đ": "D",
      "Ƌ": "D",
      "Ɗ": "D",
      "Ɖ": "D",
      "Ꝺ": "D",
      "Ǳ": "DZ",
      "Ǆ": "DZ",
      "ǲ": "Dz",
      "ǅ": "Dz",
      "Ⓔ": "E",
      "Ｅ": "E",
      "È": "E",
      "É": "E",
      "Ê": "E",
      "Ề": "E",
      "Ế": "E",
      "Ễ": "E",
      "Ể": "E",
      "Ẽ": "E",
      "Ē": "E",
      "Ḕ": "E",
      "Ḗ": "E",
      "Ĕ": "E",
      "Ė": "E",
      "Ë": "E",
      "Ẻ": "E",
      "Ě": "E",
      "Ȅ": "E",
      "Ȇ": "E",
      "Ẹ": "E",
      "Ệ": "E",
      "Ȩ": "E",
      "Ḝ": "E",
      "Ę": "E",
      "Ḙ": "E",
      "Ḛ": "E",
      "Ɛ": "E",
      "Ǝ": "E",
      "Ⓕ": "F",
      "Ｆ": "F",
      "Ḟ": "F",
      "Ƒ": "F",
      "Ꝼ": "F",
      "Ⓖ": "G",
      "Ｇ": "G",
      "Ǵ": "G",
      "Ĝ": "G",
      "Ḡ": "G",
      "Ğ": "G",
      "Ġ": "G",
      "Ǧ": "G",
      "Ģ": "G",
      "Ǥ": "G",
      "Ɠ": "G",
      "Ꞡ": "G",
      "Ᵹ": "G",
      "Ꝿ": "G",
      "Ⓗ": "H",
      "Ｈ": "H",
      "Ĥ": "H",
      "Ḣ": "H",
      "Ḧ": "H",
      "Ȟ": "H",
      "Ḥ": "H",
      "Ḩ": "H",
      "Ḫ": "H",
      "Ħ": "H",
      "Ⱨ": "H",
      "Ⱶ": "H",
      "Ɥ": "H",
      "Ⓘ": "I",
      "Ｉ": "I",
      "Ì": "I",
      "Í": "I",
      "Î": "I",
      "Ĩ": "I",
      "Ī": "I",
      "Ĭ": "I",
      "İ": "I",
      "Ï": "I",
      "Ḯ": "I",
      "Ỉ": "I",
      "Ǐ": "I",
      "Ȉ": "I",
      "Ȋ": "I",
      "Ị": "I",
      "Į": "I",
      "Ḭ": "I",
      "Ɨ": "I",
      "Ⓙ": "J",
      "Ｊ": "J",
      "Ĵ": "J",
      "Ɉ": "J",
      "Ⓚ": "K",
      "Ｋ": "K",
      "Ḱ": "K",
      "Ǩ": "K",
      "Ḳ": "K",
      "Ķ": "K",
      "Ḵ": "K",
      "Ƙ": "K",
      "Ⱪ": "K",
      "Ꝁ": "K",
      "Ꝃ": "K",
      "Ꝅ": "K",
      "Ꞣ": "K",
      "Ⓛ": "L",
      "Ｌ": "L",
      "Ŀ": "L",
      "Ĺ": "L",
      "Ľ": "L",
      "Ḷ": "L",
      "Ḹ": "L",
      "Ļ": "L",
      "Ḽ": "L",
      "Ḻ": "L",
      "Ł": "L",
      "Ƚ": "L",
      "Ɫ": "L",
      "Ⱡ": "L",
      "Ꝉ": "L",
      "Ꝇ": "L",
      "Ꞁ": "L",
      "Ǉ": "LJ",
      "ǈ": "Lj",
      "Ⓜ": "M",
      "Ｍ": "M",
      "Ḿ": "M",
      "Ṁ": "M",
      "Ṃ": "M",
      "Ɱ": "M",
      "Ɯ": "M",
      "Ⓝ": "N",
      "Ｎ": "N",
      "Ǹ": "N",
      "Ń": "N",
      "Ñ": "N",
      "Ṅ": "N",
      "Ň": "N",
      "Ṇ": "N",
      "Ņ": "N",
      "Ṋ": "N",
      "Ṉ": "N",
      "Ƞ": "N",
      "Ɲ": "N",
      "Ꞑ": "N",
      "Ꞥ": "N",
      "Ǌ": "NJ",
      "ǋ": "Nj",
      "Ⓞ": "O",
      "Ｏ": "O",
      "Ò": "O",
      "Ó": "O",
      "Ô": "O",
      "Ồ": "O",
      "Ố": "O",
      "Ỗ": "O",
      "Ổ": "O",
      "Õ": "O",
      "Ṍ": "O",
      "Ȭ": "O",
      "Ṏ": "O",
      "Ō": "O",
      "Ṑ": "O",
      "Ṓ": "O",
      "Ŏ": "O",
      "Ȯ": "O",
      "Ȱ": "O",
      "Ö": "O",
      "Ȫ": "O",
      "Ỏ": "O",
      "Ő": "O",
      "Ǒ": "O",
      "Ȍ": "O",
      "Ȏ": "O",
      "Ơ": "O",
      "Ờ": "O",
      "Ớ": "O",
      "Ỡ": "O",
      "Ở": "O",
      "Ợ": "O",
      "Ọ": "O",
      "Ộ": "O",
      "Ǫ": "O",
      "Ǭ": "O",
      "Ø": "O",
      "Ǿ": "O",
      "Ɔ": "O",
      "Ɵ": "O",
      "Ꝋ": "O",
      "Ꝍ": "O",
      "Œ": "OE",
      "Ƣ": "OI",
      "Ꝏ": "OO",
      "Ȣ": "OU",
      "Ⓟ": "P",
      "Ｐ": "P",
      "Ṕ": "P",
      "Ṗ": "P",
      "Ƥ": "P",
      "Ᵽ": "P",
      "Ꝑ": "P",
      "Ꝓ": "P",
      "Ꝕ": "P",
      "Ⓠ": "Q",
      "Ｑ": "Q",
      "Ꝗ": "Q",
      "Ꝙ": "Q",
      "Ɋ": "Q",
      "Ⓡ": "R",
      "Ｒ": "R",
      "Ŕ": "R",
      "Ṙ": "R",
      "Ř": "R",
      "Ȑ": "R",
      "Ȓ": "R",
      "Ṛ": "R",
      "Ṝ": "R",
      "Ŗ": "R",
      "Ṟ": "R",
      "Ɍ": "R",
      "Ɽ": "R",
      "Ꝛ": "R",
      "Ꞧ": "R",
      "Ꞃ": "R",
      "Ⓢ": "S",
      "Ｓ": "S",
      "ẞ": "S",
      "Ś": "S",
      "Ṥ": "S",
      "Ŝ": "S",
      "Ṡ": "S",
      "Š": "S",
      "Ṧ": "S",
      "Ṣ": "S",
      "Ṩ": "S",
      "Ș": "S",
      "Ş": "S",
      "Ȿ": "S",
      "Ꞩ": "S",
      "Ꞅ": "S",
      "Ⓣ": "T",
      "Ｔ": "T",
      "Ṫ": "T",
      "Ť": "T",
      "Ṭ": "T",
      "Ț": "T",
      "Ţ": "T",
      "Ṱ": "T",
      "Ṯ": "T",
      "Ŧ": "T",
      "Ƭ": "T",
      "Ʈ": "T",
      "Ⱦ": "T",
      "Ꞇ": "T",
      "Ꜩ": "TZ",
      "Ⓤ": "U",
      "Ｕ": "U",
      "Ù": "U",
      "Ú": "U",
      "Û": "U",
      "Ũ": "U",
      "Ṹ": "U",
      "Ū": "U",
      "Ṻ": "U",
      "Ŭ": "U",
      "Ü": "U",
      "Ǜ": "U",
      "Ǘ": "U",
      "Ǖ": "U",
      "Ǚ": "U",
      "Ủ": "U",
      "Ů": "U",
      "Ű": "U",
      "Ǔ": "U",
      "Ȕ": "U",
      "Ȗ": "U",
      "Ư": "U",
      "Ừ": "U",
      "Ứ": "U",
      "Ữ": "U",
      "Ử": "U",
      "Ự": "U",
      "Ụ": "U",
      "Ṳ": "U",
      "Ų": "U",
      "Ṷ": "U",
      "Ṵ": "U",
      "Ʉ": "U",
      "Ⓥ": "V",
      "Ｖ": "V",
      "Ṽ": "V",
      "Ṿ": "V",
      "Ʋ": "V",
      "Ꝟ": "V",
      "Ʌ": "V",
      "Ꝡ": "VY",
      "Ⓦ": "W",
      "Ｗ": "W",
      "Ẁ": "W",
      "Ẃ": "W",
      "Ŵ": "W",
      "Ẇ": "W",
      "Ẅ": "W",
      "Ẉ": "W",
      "Ⱳ": "W",
      "Ⓧ": "X",
      "Ｘ": "X",
      "Ẋ": "X",
      "Ẍ": "X",
      "Ⓨ": "Y",
      "Ｙ": "Y",
      "Ỳ": "Y",
      "Ý": "Y",
      "Ŷ": "Y",
      "Ỹ": "Y",
      "Ȳ": "Y",
      "Ẏ": "Y",
      "Ÿ": "Y",
      "Ỷ": "Y",
      "Ỵ": "Y",
      "Ƴ": "Y",
      "Ɏ": "Y",
      "Ỿ": "Y",
      "Ⓩ": "Z",
      "Ｚ": "Z",
      "Ź": "Z",
      "Ẑ": "Z",
      "Ż": "Z",
      "Ž": "Z",
      "Ẓ": "Z",
      "Ẕ": "Z",
      "Ƶ": "Z",
      "Ȥ": "Z",
      "Ɀ": "Z",
      "Ⱬ": "Z",
      "Ꝣ": "Z",
      "ⓐ": "a",
      "ａ": "a",
      "ẚ": "a",
      "à": "a",
      "á": "a",
      "â": "a",
      "ầ": "a",
      "ấ": "a",
      "ẫ": "a",
      "ẩ": "a",
      "ã": "a",
      "ā": "a",
      "ă": "a",
      "ằ": "a",
      "ắ": "a",
      "ẵ": "a",
      "ẳ": "a",
      "ȧ": "a",
      "ǡ": "a",
      "ä": "a",
      "ǟ": "a",
      "ả": "a",
      "å": "a",
      "ǻ": "a",
      "ǎ": "a",
      "ȁ": "a",
      "ȃ": "a",
      "ạ": "a",
      "ậ": "a",
      "ặ": "a",
      "ḁ": "a",
      "ą": "a",
      "ⱥ": "a",
      "ɐ": "a",
      "ꜳ": "aa",
      "æ": "ae",
      "ǽ": "ae",
      "ǣ": "ae",
      "ꜵ": "ao",
      "ꜷ": "au",
      "ꜹ": "av",
      "ꜻ": "av",
      "ꜽ": "ay",
      "ⓑ": "b",
      "ｂ": "b",
      "ḃ": "b",
      "ḅ": "b",
      "ḇ": "b",
      "ƀ": "b",
      "ƃ": "b",
      "ɓ": "b",
      "ⓒ": "c",
      "ｃ": "c",
      "ć": "c",
      "ĉ": "c",
      "ċ": "c",
      "č": "c",
      "ç": "c",
      "ḉ": "c",
      "ƈ": "c",
      "ȼ": "c",
      "ꜿ": "c",
      "ↄ": "c",
      "ⓓ": "d",
      "ｄ": "d",
      "ḋ": "d",
      "ď": "d",
      "ḍ": "d",
      "ḑ": "d",
      "ḓ": "d",
      "ḏ": "d",
      "đ": "d",
      "ƌ": "d",
      "ɖ": "d",
      "ɗ": "d",
      "ꝺ": "d",
      "ǳ": "dz",
      "ǆ": "dz",
      "ⓔ": "e",
      "ｅ": "e",
      "è": "e",
      "é": "e",
      "ê": "e",
      "ề": "e",
      "ế": "e",
      "ễ": "e",
      "ể": "e",
      "ẽ": "e",
      "ē": "e",
      "ḕ": "e",
      "ḗ": "e",
      "ĕ": "e",
      "ė": "e",
      "ë": "e",
      "ẻ": "e",
      "ě": "e",
      "ȅ": "e",
      "ȇ": "e",
      "ẹ": "e",
      "ệ": "e",
      "ȩ": "e",
      "ḝ": "e",
      "ę": "e",
      "ḙ": "e",
      "ḛ": "e",
      "ɇ": "e",
      "ɛ": "e",
      "ǝ": "e",
      "ⓕ": "f",
      "ｆ": "f",
      "ḟ": "f",
      "ƒ": "f",
      "ꝼ": "f",
      "ⓖ": "g",
      "ｇ": "g",
      "ǵ": "g",
      "ĝ": "g",
      "ḡ": "g",
      "ğ": "g",
      "ġ": "g",
      "ǧ": "g",
      "ģ": "g",
      "ǥ": "g",
      "ɠ": "g",
      "ꞡ": "g",
      "ᵹ": "g",
      "ꝿ": "g",
      "ⓗ": "h",
      "ｈ": "h",
      "ĥ": "h",
      "ḣ": "h",
      "ḧ": "h",
      "ȟ": "h",
      "ḥ": "h",
      "ḩ": "h",
      "ḫ": "h",
      "ẖ": "h",
      "ħ": "h",
      "ⱨ": "h",
      "ⱶ": "h",
      "ɥ": "h",
      "ƕ": "hv",
      "ⓘ": "i",
      "ｉ": "i",
      "ì": "i",
      "í": "i",
      "î": "i",
      "ĩ": "i",
      "ī": "i",
      "ĭ": "i",
      "ï": "i",
      "ḯ": "i",
      "ỉ": "i",
      "ǐ": "i",
      "ȉ": "i",
      "ȋ": "i",
      "ị": "i",
      "į": "i",
      "ḭ": "i",
      "ɨ": "i",
      "ı": "i",
      "ⓙ": "j",
      "ｊ": "j",
      "ĵ": "j",
      "ǰ": "j",
      "ɉ": "j",
      "ⓚ": "k",
      "ｋ": "k",
      "ḱ": "k",
      "ǩ": "k",
      "ḳ": "k",
      "ķ": "k",
      "ḵ": "k",
      "ƙ": "k",
      "ⱪ": "k",
      "ꝁ": "k",
      "ꝃ": "k",
      "ꝅ": "k",
      "ꞣ": "k",
      "ⓛ": "l",
      "ｌ": "l",
      "ŀ": "l",
      "ĺ": "l",
      "ľ": "l",
      "ḷ": "l",
      "ḹ": "l",
      "ļ": "l",
      "ḽ": "l",
      "ḻ": "l",
      "ſ": "l",
      "ł": "l",
      "ƚ": "l",
      "ɫ": "l",
      "ⱡ": "l",
      "ꝉ": "l",
      "ꞁ": "l",
      "ꝇ": "l",
      "ǉ": "lj",
      "ⓜ": "m",
      "ｍ": "m",
      "ḿ": "m",
      "ṁ": "m",
      "ṃ": "m",
      "ɱ": "m",
      "ɯ": "m",
      "ⓝ": "n",
      "ｎ": "n",
      "ǹ": "n",
      "ń": "n",
      "ñ": "n",
      "ṅ": "n",
      "ň": "n",
      "ṇ": "n",
      "ņ": "n",
      "ṋ": "n",
      "ṉ": "n",
      "ƞ": "n",
      "ɲ": "n",
      "ŉ": "n",
      "ꞑ": "n",
      "ꞥ": "n",
      "ǌ": "nj",
      "ⓞ": "o",
      "ｏ": "o",
      "ò": "o",
      "ó": "o",
      "ô": "o",
      "ồ": "o",
      "ố": "o",
      "ỗ": "o",
      "ổ": "o",
      "õ": "o",
      "ṍ": "o",
      "ȭ": "o",
      "ṏ": "o",
      "ō": "o",
      "ṑ": "o",
      "ṓ": "o",
      "ŏ": "o",
      "ȯ": "o",
      "ȱ": "o",
      "ö": "o",
      "ȫ": "o",
      "ỏ": "o",
      "ő": "o",
      "ǒ": "o",
      "ȍ": "o",
      "ȏ": "o",
      "ơ": "o",
      "ờ": "o",
      "ớ": "o",
      "ỡ": "o",
      "ở": "o",
      "ợ": "o",
      "ọ": "o",
      "ộ": "o",
      "ǫ": "o",
      "ǭ": "o",
      "ø": "o",
      "ǿ": "o",
      "ɔ": "o",
      "ꝋ": "o",
      "ꝍ": "o",
      "ɵ": "o",
      "œ": "oe",
      "ƣ": "oi",
      "ȣ": "ou",
      "ꝏ": "oo",
      "ⓟ": "p",
      "ｐ": "p",
      "ṕ": "p",
      "ṗ": "p",
      "ƥ": "p",
      "ᵽ": "p",
      "ꝑ": "p",
      "ꝓ": "p",
      "ꝕ": "p",
      "ⓠ": "q",
      "ｑ": "q",
      "ɋ": "q",
      "ꝗ": "q",
      "ꝙ": "q",
      "ⓡ": "r",
      "ｒ": "r",
      "ŕ": "r",
      "ṙ": "r",
      "ř": "r",
      "ȑ": "r",
      "ȓ": "r",
      "ṛ": "r",
      "ṝ": "r",
      "ŗ": "r",
      "ṟ": "r",
      "ɍ": "r",
      "ɽ": "r",
      "ꝛ": "r",
      "ꞧ": "r",
      "ꞃ": "r",
      "ⓢ": "s",
      "ｓ": "s",
      "ß": "s",
      "ś": "s",
      "ṥ": "s",
      "ŝ": "s",
      "ṡ": "s",
      "š": "s",
      "ṧ": "s",
      "ṣ": "s",
      "ṩ": "s",
      "ș": "s",
      "ş": "s",
      "ȿ": "s",
      "ꞩ": "s",
      "ꞅ": "s",
      "ẛ": "s",
      "ⓣ": "t",
      "ｔ": "t",
      "ṫ": "t",
      "ẗ": "t",
      "ť": "t",
      "ṭ": "t",
      "ț": "t",
      "ţ": "t",
      "ṱ": "t",
      "ṯ": "t",
      "ŧ": "t",
      "ƭ": "t",
      "ʈ": "t",
      "ⱦ": "t",
      "ꞇ": "t",
      "ꜩ": "tz",
      "ⓤ": "u",
      "ｕ": "u",
      "ù": "u",
      "ú": "u",
      "û": "u",
      "ũ": "u",
      "ṹ": "u",
      "ū": "u",
      "ṻ": "u",
      "ŭ": "u",
      "ü": "u",
      "ǜ": "u",
      "ǘ": "u",
      "ǖ": "u",
      "ǚ": "u",
      "ủ": "u",
      "ů": "u",
      "ű": "u",
      "ǔ": "u",
      "ȕ": "u",
      "ȗ": "u",
      "ư": "u",
      "ừ": "u",
      "ứ": "u",
      "ữ": "u",
      "ử": "u",
      "ự": "u",
      "ụ": "u",
      "ṳ": "u",
      "ų": "u",
      "ṷ": "u",
      "ṵ": "u",
      "ʉ": "u",
      "ⓥ": "v",
      "ｖ": "v",
      "ṽ": "v",
      "ṿ": "v",
      "ʋ": "v",
      "ꝟ": "v",
      "ʌ": "v",
      "ꝡ": "vy",
      "ⓦ": "w",
      "ｗ": "w",
      "ẁ": "w",
      "ẃ": "w",
      "ŵ": "w",
      "ẇ": "w",
      "ẅ": "w",
      "ẘ": "w",
      "ẉ": "w",
      "ⱳ": "w",
      "ⓧ": "x",
      "ｘ": "x",
      "ẋ": "x",
      "ẍ": "x",
      "ⓨ": "y",
      "ｙ": "y",
      "ỳ": "y",
      "ý": "y",
      "ŷ": "y",
      "ỹ": "y",
      "ȳ": "y",
      "ẏ": "y",
      "ÿ": "y",
      "ỷ": "y",
      "ẙ": "y",
      "ỵ": "y",
      "ƴ": "y",
      "ɏ": "y",
      "ỿ": "y",
      "ⓩ": "z",
      "ｚ": "z",
      "ź": "z",
      "ẑ": "z",
      "ż": "z",
      "ž": "z",
      "ẓ": "z",
      "ẕ": "z",
      "ƶ": "z",
      "ȥ": "z",
      "ɀ": "z",
      "ⱬ": "z",
      "ꝣ": "z",
      "Ά": "Α",
      "Έ": "Ε",
      "Ή": "Η",
      "Ί": "Ι",
      "Ϊ": "Ι",
      "Ό": "Ο",
      "Ύ": "Υ",
      "Ϋ": "Υ",
      "Ώ": "Ω",
      "ά": "α",
      "έ": "ε",
      "ή": "η",
      "ί": "ι",
      "ϊ": "ι",
      "ΐ": "ι",
      "ό": "ο",
      "ύ": "υ",
      "ϋ": "υ",
      "ΰ": "υ",
      "ώ": "ω",
      "ς": "σ",
      "’": "'"
    }
  })), S.define("select2/data/base", ["../utils"], (function(e) {
    function t(e, n) {
      t.__super__.constructor.call(this)
    }
    return e.Extend(t, e.Observable), t.prototype.current = function(e) {
      throw new Error("The `current` method must be defined in child classes.")
    }, t.prototype.query = function(e, t) {
      throw new Error("The `query` method must be defined in child classes.")
    }, t.prototype.bind = function(e, t) {}, t.prototype.destroy = function() {}, t.prototype.generateResultId = function(t, n) {
      return t = t.id + "-result-", t += e.generateChars(4), null != n.id ? t += "-" + n.id.toString() : t += "-" + e.generateChars(4), t
    }, t
  })), S.define("select2/data/select", ["./base", "../utils", "jquery"], (function(e, t, n) {
    function r(e, t) {
      this.$element = e, this.options = t, r.__super__.constructor.call(this)
    }
    return t.Extend(r, e), r.prototype.current = function(e) {
      var t = this;
      e(Array.prototype.map.call(this.$element[0].querySelectorAll(":checked"), (function(e) {
        return t.item(n(e))
      })))
    }, r.prototype.select = function(e) {
      var t, n = this;
      if (e.selected = !0, null != e.element && "option" === e.element.tagName.toLowerCase()) return e.element.selected = !0, void this.$element.trigger("input").trigger("change");
      this.$element.prop("multiple") ? this.current((function(t) {
        var r = [];
        (e = [e]).push.apply(e, t);
        for (var i = 0; i < e.length; i++) {
          var o = e[i].id; - 1 === r.indexOf(o) && r.push(o)
        }
        n.$element.val(r), n.$element.trigger("input").trigger("change")
      })) : (t = e.id, this.$element.val(t), this.$element.trigger("input").trigger("change"))
    }, r.prototype.unselect = function(e) {
      var t = this;
      if (this.$element.prop("multiple")) {
        if (e.selected = !1, null != e.element && "option" === e.element.tagName.toLowerCase()) return e.element.selected = !1, void this.$element.trigger("input").trigger("change");
        this.current((function(n) {
          for (var r = [], i = 0; i < n.length; i++) {
            var o = n[i].id;
            o !== e.id && -1 === r.indexOf(o) && r.push(o)
          }
          t.$element.val(r), t.$element.trigger("input").trigger("change")
        }))
      }
    }, r.prototype.bind = function(e, t) {
      var n = this;
      (this.container = e).on("select", (function(e) {
        n.select(e.data)
      })), e.on("unselect", (function(e) {
        n.unselect(e.data)
      }))
    }, r.prototype.destroy = function() {
      this.$element.find("*").each((function() {
        t.RemoveData(this)
      }))
    }, r.prototype.query = function(e, t) {
      var r = [],
        i = this;
      this.$element.children().each((function() {
        var t;
        "option" !== this.tagName.toLowerCase() && "optgroup" !== this.tagName.toLowerCase() || (t = n(this), t = i.item(t), null !== (t = i.matches(e, t)) && r.push(t))
      })), t({
        results: r
      })
    }, r.prototype.addOptions = function(e) {
      this.$element.append(e)
    }, r.prototype.option = function(e) {
      var r;
      return e.children ? (r = document.createElement("optgroup")).label = e.text : void 0 !== (r = document.createElement("option")).textContent ? r.textContent = e.text : r.innerText = e.text, void 0 !== e.id && (r.value = e.id), e.disabled && (r.disabled = !0), e.selected && (r.selected = !0), e.title && (r.title = e.title), (e = this._normalizeItem(e)).element = r, t.StoreData(r, "data", e), n(r)
    }, r.prototype.item = function(e) {
      var r = {};
      if (null != (r = t.GetData(e[0], "data"))) return r;
      var i = e[0];
      if ("option" === i.tagName.toLowerCase()) r = {
        id: e.val(),
        text: e.text(),
        disabled: e.prop("disabled"),
        selected: e.prop("selected"),
        title: e.prop("title")
      };
      else if ("optgroup" === i.tagName.toLowerCase()) {
        r = {
          text: e.prop("label"),
          children: [],
          title: e.prop("title")
        };
        for (var o = e.children("option"), a = [], s = 0; s < o.length; s++) {
          var l = n(o[s]);
          l = this.item(l);
          a.push(l)
        }
        r.children = a
      }
      return (r = this._normalizeItem(r)).element = e[0], t.StoreData(e[0], "data", r), r
    }, r.prototype._normalizeItem = function(e) {
      return e !== Object(e) && (e = {
        id: e,
        text: e
      }), null != (e = n.extend({}, {
        text: ""
      }, e)).id && (e.id = e.id.toString()), null != e.text && (e.text = e.text.toString()), null == e._resultId && e.id && null != this.container && (e._resultId = this.generateResultId(this.container, e)), n.extend({}, {
        selected: !1,
        disabled: !1
      }, e)
    }, r.prototype.matches = function(e, t) {
      return this.options.get("matcher")(e, t)
    }, r
  })), S.define("select2/data/array", ["./select", "../utils", "jquery"], (function(e, t, n) {
    function r(e, t) {
      this._dataToConvert = t.get("data") || [], r.__super__.constructor.call(this, e, t)
    }
    return t.Extend(r, e), r.prototype.bind = function(e, t) {
      r.__super__.bind.call(this, e, t), this.addOptions(this.convertToOptions(this._dataToConvert))
    }, r.prototype.select = function(e) {
      var t = this.$element.find("option").filter((function(t, n) {
        return n.value == e.id.toString()
      }));
      0 === t.length && (t = this.option(e), this.addOptions(t)), r.__super__.select.call(this, e)
    }, r.prototype.convertToOptions = function(e) {
      for (var t = this, r = this.$element.find("option"), i = r.map((function() {
          return t.item(n(this)).id
        })).get(), o = [], a = 0; a < e.length; a++) {
        var s, l, c = this._normalizeItem(e[a]);
        0 <= i.indexOf(c.id) ? (s = r.filter(function(e) {
          return function() {
            return n(this).val() == e.id
          }
        }(c)), l = this.item(s), l = n.extend(!0, {}, c, l), l = this.option(l), s.replaceWith(l)) : (l = this.option(c), c.children && (c = this.convertToOptions(c.children), l.append(c)), o.push(l))
      }
      return o
    }, r
  })), S.define("select2/data/ajax", ["./array", "../utils", "jquery"], (function(e, t, n) {
    function r(e, t) {
      this.ajaxOptions = this._applyDefaults(t.get("ajax")), null != this.ajaxOptions.processResults && (this.processResults = this.ajaxOptions.processResults), r.__super__.constructor.call(this, e, t)
    }
    return t.Extend(r, e), r.prototype._applyDefaults = function(e) {
      var t = {
        data: function(e) {
          return n.extend({}, e, {
            q: e.term
          })
        },
        transport: function(e, t, r) {
          return (e = n.ajax(e)).then(t), e.fail(r), e
        }
      };
      return n.extend({}, t, e, !0)
    }, r.prototype.processResults = function(e) {
      return e
    }, r.prototype.query = function(e, t) {
      var r = this;
      null != this._request && ("function" == typeof this._request.abort && this._request.abort(), this._request = null);
      var i = n.extend({
        type: "GET"
      }, this.ajaxOptions);

      function o() {
        var n = i.transport(i, (function(n) {
          n = r.processResults(n, e), r.options.get("debug") && window.console && console.error && (n && n.results && Array.isArray(n.results) || console.error("Select2: The AJAX results did not return an array in the `results` key of the response.")), t(n)
        }), (function() {
          "status" in n && (0 === n.status || "0" === n.status) || r.trigger("results:message", {
            message: "errorLoading"
          })
        }));
        r._request = n
      }
      "function" == typeof i.url && (i.url = i.url.call(this.$element, e)), "function" == typeof i.data && (i.data = i.data.call(this.$element, e)), this.ajaxOptions.delay && null != e.term ? (this._queryTimeout && window.clearTimeout(this._queryTimeout), this._queryTimeout = window.setTimeout(o, this.ajaxOptions.delay)) : o()
    }, r
  })), S.define("select2/data/tags", ["jquery"], (function(e) {
    function t(e, t, n) {
      var r = n.get("tags"),
        i = n.get("createTag");
      if (void 0 !== i && (this.createTag = i), void 0 !== (i = n.get("insertTag")) && (this.insertTag = i), e.call(this, t, n), Array.isArray(r))
        for (var o = 0; o < r.length; o++) {
          var a = r[o];
          a = this._normalizeItem(a), a = this.option(a);
          this.$element.append(a)
        }
    }
    return t.prototype.query = function(e, t, n) {
      var r = this;
      this._removeOldTags(), null != t.term && null == t.page ? e.call(this, t, (function e(i, o) {
        for (var a = i.results, s = 0; s < a.length; s++) {
          var l = a[s],
            c = null != l.children && !e({
              results: l.children
            }, !0);
          if ((l.text || "").toUpperCase() === (t.term || "").toUpperCase() || c) return !o && (i.data = a, void n(i))
        }
        if (o) return !0;
        var u, d = r.createTag(t);
        null != d && ((u = r.option(d)).attr("data-select2-tag", "true"), r.addOptions([u]), r.insertTag(a, d)), i.results = a, n(i)
      })) : e.call(this, t, n)
    }, t.prototype.createTag = function(e, t) {
      return null == t.term || "" === (t = t.term.trim()) ? null : {
        id: t,
        text: t
      }
    }, t.prototype.insertTag = function(e, t, n) {
      t.unshift(n)
    }, t.prototype._removeOldTags = function(t) {
      this.$element.find("option[data-select2-tag]").each((function() {
        this.selected || e(this).remove()
      }))
    }, t
  })), S.define("select2/data/tokenizer", ["jquery"], (function(e) {
    function t(e, t, n) {
      var r = n.get("tokenizer");
      void 0 !== r && (this.tokenizer = r), e.call(this, t, n)
    }
    return t.prototype.bind = function(e, t, n) {
      e.call(this, t, n), this.$search = t.dropdown.$search || t.selection.$search || n.find(".select2-search__field")
    }, t.prototype.query = function(t, n, r) {
      var i = this;
      n.term = n.term || "";
      var o = this.tokenizer(n, this.options, (function(t) {
        var n, r = i._normalizeItem(t);
        i.$element.find("option").filter((function() {
          return e(this).val() === r.id
        })).length || ((n = i.option(r)).attr("data-select2-tag", !0), i._removeOldTags(), i.addOptions([n])), n = r, i.trigger("select", {
          data: n
        })
      }));
      o.term !== n.term && (this.$search.length && (this.$search.val(o.term), this.$search.trigger("focus")), n.term = o.term), t.call(this, n, r)
    }, t.prototype.tokenizer = function(t, n, r, i) {
      for (var o = r.get("tokenSeparators") || [], a = n.term, s = 0, l = this.createTag || function(e) {
          return {
            id: e.term,
            text: e.term
          }
        }; s < a.length;) {
        var c = a[s]; - 1 !== o.indexOf(c) ? (c = a.substr(0, s), null != (c = l(e.extend({}, n, {
          term: c
        }))) ? (i(c), a = a.substr(s + 1) || "", s = 0) : s++) : s++
      }
      return {
        term: a
      }
    }, t
  })), S.define("select2/data/minimumInputLength", [], (function() {
    function e(e, t, n) {
      this.minimumInputLength = n.get("minimumInputLength"), e.call(this, t, n)
    }
    return e.prototype.query = function(e, t, n) {
      t.term = t.term || "", t.term.length < this.minimumInputLength ? this.trigger("results:message", {
        message: "inputTooShort",
        args: {
          minimum: this.minimumInputLength,
          input: t.term,
          params: t
        }
      }) : e.call(this, t, n)
    }, e
  })), S.define("select2/data/maximumInputLength", [], (function() {
    function e(e, t, n) {
      this.maximumInputLength = n.get("maximumInputLength"), e.call(this, t, n)
    }
    return e.prototype.query = function(e, t, n) {
      t.term = t.term || "", 0 < this.maximumInputLength && t.term.length > this.maximumInputLength ? this.trigger("results:message", {
        message: "inputTooLong",
        args: {
          maximum: this.maximumInputLength,
          input: t.term,
          params: t
        }
      }) : e.call(this, t, n)
    }, e
  })), S.define("select2/data/maximumSelectionLength", [], (function() {
    function e(e, t, n) {
      this.maximumSelectionLength = n.get("maximumSelectionLength"), e.call(this, t, n)
    }
    return e.prototype.bind = function(e, t, n) {
      var r = this;
      e.call(this, t, n), t.on("select", (function() {
        r._checkIfMaximumSelected()
      }))
    }, e.prototype.query = function(e, t, n) {
      var r = this;
      this._checkIfMaximumSelected((function() {
        e.call(r, t, n)
      }))
    }, e.prototype._checkIfMaximumSelected = function(e, t) {
      var n = this;
      this.current((function(e) {
        e = null != e ? e.length : 0, 0 < n.maximumSelectionLength && e >= n.maximumSelectionLength ? n.trigger("results:message", {
          message: "maximumSelected",
          args: {
            maximum: n.maximumSelectionLength
          }
        }) : t && t()
      }))
    }, e
  })), S.define("select2/dropdown", ["jquery", "./utils"], (function(e, t) {
    function n(e, t) {
      this.$element = e, this.options = t, n.__super__.constructor.call(this)
    }
    return t.Extend(n, t.Observable), n.prototype.render = function() {
      var t = e('<span class="select2-dropdown"><span class="select2-results"></span></span>');
      return t.attr("dir", this.options.get("dir")), this.$dropdown = t
    }, n.prototype.bind = function() {}, n.prototype.position = function(e, t) {}, n.prototype.destroy = function() {
      this.$dropdown.remove()
    }, n
  })), S.define("select2/dropdown/search", ["jquery"], (function(e) {
    function t() {}
    return t.prototype.render = function(t) {
      var n = t.call(this),
        r = this.options.get("translations").get("search");
      t = e('<span class="select2-search select2-search--dropdown"><input class="select2-search__field" type="search" tabindex="-1" autocorrect="off" autocapitalize="none" spellcheck="false" role="searchbox" aria-autocomplete="list" /></span>');
      return this.$searchContainer = t, this.$search = t.find("input"), this.$search.prop("autocomplete", this.options.get("autocomplete")), this.$search.attr("aria-label", r()), n.prepend(t), n
    }, t.prototype.bind = function(t, n, r) {
      var i = this,
        o = n.id + "-results";
      t.call(this, n, r), this.$search.on("keydown", (function(e) {
        i.trigger("keypress", e), i._keyUpPrevented = e.isDefaultPrevented()
      })), this.$search.on("input", (function(t) {
        e(this).off("keyup")
      })), this.$search.on("keyup input", (function(e) {
        i.handleSearch(e)
      })), n.on("open", (function() {
        i.$search.attr("tabindex", 0), i.$search.attr("aria-controls", o), i.$search.trigger("focus"), window.setTimeout((function() {
          i.$search.trigger("focus")
        }), 0)
      })), n.on("close", (function() {
        i.$search.attr("tabindex", -1), i.$search.removeAttr("aria-controls"), i.$search.removeAttr("aria-activedescendant"), i.$search.val(""), i.$search.trigger("blur")
      })), n.on("focus", (function() {
        n.isOpen() || i.$search.trigger("focus")
      })), n.on("results:all", (function(e) {
        null != e.query.term && "" !== e.query.term || (i.showSearch(e) ? i.$searchContainer[0].classList.remove("select2-search--hide") : i.$searchContainer[0].classList.add("select2-search--hide"))
      })), n.on("results:focus", (function(e) {
        e.data._resultId ? i.$search.attr("aria-activedescendant", e.data._resultId) : i.$search.removeAttr("aria-activedescendant")
      }))
    }, t.prototype.handleSearch = function(e) {
      var t;
      this._keyUpPrevented || (t = this.$search.val(), this.trigger("query", {
        term: t
      })), this._keyUpPrevented = !1
    }, t.prototype.showSearch = function(e, t) {
      return !0
    }, t
  })), S.define("select2/dropdown/hidePlaceholder", [], (function() {
    function e(e, t, n, r) {
      this.placeholder = this.normalizePlaceholder(n.get("placeholder")), e.call(this, t, n, r)
    }
    return e.prototype.append = function(e, t) {
      t.results = this.removePlaceholder(t.results), e.call(this, t)
    }, e.prototype.normalizePlaceholder = function(e, t) {
      return "string" == typeof t && (t = {
        id: "",
        text: t
      }), t
    }, e.prototype.removePlaceholder = function(e, t) {
      for (var n = t.slice(0), r = t.length - 1; 0 <= r; r--) {
        var i = t[r];
        this.placeholder.id === i.id && n.splice(r, 1)
      }
      return n
    }, e
  })), S.define("select2/dropdown/infiniteScroll", ["jquery"], (function(e) {
    function t(e, t, n, r) {
      this.lastParams = {}, e.call(this, t, n, r), this.$loadingMore = this.createLoadingMore(), this.loading = !1
    }
    return t.prototype.append = function(e, t) {
      this.$loadingMore.remove(), this.loading = !1, e.call(this, t), this.showLoadingMore(t) && (this.$results.append(this.$loadingMore), this.loadMoreIfNeeded())
    }, t.prototype.bind = function(e, t, n) {
      var r = this;
      e.call(this, t, n), t.on("query", (function(e) {
        r.lastParams = e, r.loading = !0
      })), t.on("query:append", (function(e) {
        r.lastParams = e, r.loading = !0
      })), this.$results.on("scroll", this.loadMoreIfNeeded.bind(this))
    }, t.prototype.loadMoreIfNeeded = function() {
      var t = e.contains(document.documentElement, this.$loadingMore[0]);
      !this.loading && t && (t = this.$results.offset().top + this.$results.outerHeight(!1), this.$loadingMore.offset().top + this.$loadingMore.outerHeight(!1) <= t + 50 && this.loadMore())
    }, t.prototype.loadMore = function() {
      this.loading = !0;
      var t = e.extend({}, {
        page: 1
      }, this.lastParams);
      t.page++, this.trigger("query:append", t)
    }, t.prototype.showLoadingMore = function(e, t) {
      return t.pagination && t.pagination.more
    }, t.prototype.createLoadingMore = function() {
      var t = e('<li class="select2-results__option select2-results__option--load-more"role="option" aria-disabled="true"></li>'),
        n = this.options.get("translations").get("loadingMore");
      return t.html(n(this.lastParams)), t
    }, t
  })), S.define("select2/dropdown/attachBody", ["jquery", "../utils"], (function(e, t) {
    function n(t, n, r) {
      this.$dropdownParent = e(r.get("dropdownParent") || document.body), t.call(this, n, r)
    }
    return n.prototype.bind = function(e, t, n) {
      var r = this;
      e.call(this, t, n), t.on("open", (function() {
        r._showDropdown(), r._attachPositioningHandler(t), r._bindContainerResultHandlers(t)
      })), t.on("close", (function() {
        r._hideDropdown(), r._detachPositioningHandler(t)
      })), this.$dropdownContainer.on("mousedown", (function(e) {
        e.stopPropagation()
      }))
    }, n.prototype.destroy = function(e) {
      e.call(this), this.$dropdownContainer.remove()
    }, n.prototype.position = function(e, t, n) {
      t.attr("class", n.attr("class")), t[0].classList.remove("select2"), t[0].classList.add("select2-container--open"), t.css({
        position: "absolute",
        top: -999999
      }), this.$container = n
    }, n.prototype.render = function(t) {
      var n = e("<span></span>");
      t = t.call(this);
      return n.append(t), this.$dropdownContainer = n
    }, n.prototype._hideDropdown = function(e) {
      this.$dropdownContainer.detach()
    }, n.prototype._bindContainerResultHandlers = function(e, t) {
      var n;
      this._containerResultsHandlersBound || (n = this, t.on("results:all", (function() {
        n._positionDropdown(), n._resizeDropdown()
      })), t.on("results:append", (function() {
        n._positionDropdown(), n._resizeDropdown()
      })), t.on("results:message", (function() {
        n._positionDropdown(), n._resizeDropdown()
      })), t.on("select", (function() {
        n._positionDropdown(), n._resizeDropdown()
      })), t.on("unselect", (function() {
        n._positionDropdown(), n._resizeDropdown()
      })), this._containerResultsHandlersBound = !0)
    }, n.prototype._attachPositioningHandler = function(n, r) {
      var i = this,
        o = "scroll.select2." + r.id,
        a = "resize.select2." + r.id,
        s = "orientationchange.select2." + r.id;
      (r = this.$container.parents().filter(t.hasScroll)).each((function() {
        t.StoreData(this, "select2-scroll-position", {
          x: e(this).scrollLeft(),
          y: e(this).scrollTop()
        })
      })), r.on(o, (function(n) {
        var r = t.GetData(this, "select2-scroll-position");
        e(this).scrollTop(r.y)
      })), e(window).on(o + " " + a + " " + s, (function(e) {
        i._positionDropdown(), i._resizeDropdown()
      }))
    }, n.prototype._detachPositioningHandler = function(n, r) {
      var i = "scroll.select2." + r.id,
        o = "resize.select2." + r.id;
      r = "orientationchange.select2." + r.id;
      this.$container.parents().filter(t.hasScroll).off(i), e(window).off(i + " " + o + " " + r)
    }, n.prototype._positionDropdown = function() {
      var t = e(window),
        n = this.$dropdown[0].classList.contains("select2-dropdown--above"),
        r = this.$dropdown[0].classList.contains("select2-dropdown--below"),
        i = null,
        o = this.$container.offset();
      o.bottom = o.top + this.$container.outerHeight(!1);
      var a = {
        height: this.$container.outerHeight(!1)
      };
      a.top = o.top, a.bottom = o.top + a.height;
      var s = this.$dropdown.outerHeight(!1),
        l = t.scrollTop(),
        c = t.scrollTop() + t.height(),
        u = l < o.top - s;
      t = c > o.bottom + s, l = {
        left: o.left,
        top: a.bottom
      };
      "static" === (c = this.$dropdownParent).css("position") && (c = c.offsetParent()), o = {
        top: 0,
        left: 0
      }, (e.contains(document.body, c[0]) || c[0].isConnected) && (o = c.offset()), l.top -= o.top, l.left -= o.left, n || r || (i = "below"), t || !u || n ? !u && t && n && (i = "below") : i = "above", ("above" == i || n && "below" !== i) && (l.top = a.top - o.top - s), null != i && (this.$dropdown[0].classList.remove("select2-dropdown--below"), this.$dropdown[0].classList.remove("select2-dropdown--above"), this.$dropdown[0].classList.add("select2-dropdown--" + i), this.$container[0].classList.remove("select2-container--below"), this.$container[0].classList.remove("select2-container--above"), this.$container[0].classList.add("select2-container--" + i)), this.$dropdownContainer.css(l)
    }, n.prototype._resizeDropdown = function() {
      var e = {
        width: this.$container.outerWidth(!1) + "px"
      };
      this.options.get("dropdownAutoWidth") && (e.minWidth = e.width, e.position = "relative", e.width = "auto"), this.$dropdown.css(e)
    }, n.prototype._showDropdown = function(e) {
      this.$dropdownContainer.appendTo(this.$dropdownParent), this._positionDropdown(), this._resizeDropdown()
    }, n
  })), S.define("select2/dropdown/minimumResultsForSearch", [], (function() {
    function e(e, t, n, r) {
      this.minimumResultsForSearch = n.get("minimumResultsForSearch"), this.minimumResultsForSearch < 0 && (this.minimumResultsForSearch = 1 / 0), e.call(this, t, n, r)
    }
    return e.prototype.showSearch = function(e, t) {
      return !(function e(t) {
        for (var n = 0, r = 0; r < t.length; r++) {
          var i = t[r];
          i.children ? n += e(i.children) : n++
        }
        return n
      }(t.data.results) < this.minimumResultsForSearch) && e.call(this, t)
    }, e
  })), S.define("select2/dropdown/selectOnClose", ["../utils"], (function(e) {
    function t() {}
    return t.prototype.bind = function(e, t, n) {
      var r = this;
      e.call(this, t, n), t.on("close", (function(e) {
        r._handleSelectOnClose(e)
      }))
    }, t.prototype._handleSelectOnClose = function(t, n) {
      if (n && null != n.originalSelect2Event) {
        var r = n.originalSelect2Event;
        if ("select" === r._type || "unselect" === r._type) return
      }(r = this.getHighlightedResults()).length < 1 || null != (r = e.GetData(r[0], "data")).element && r.element.selected || null == r.element && r.selected || this.trigger("select", {
        data: r
      })
    }, t
  })), S.define("select2/dropdown/closeOnSelect", [], (function() {
    function e() {}
    return e.prototype.bind = function(e, t, n) {
      var r = this;
      e.call(this, t, n), t.on("select", (function(e) {
        r._selectTriggered(e)
      })), t.on("unselect", (function(e) {
        r._selectTriggered(e)
      }))
    }, e.prototype._selectTriggered = function(e, t) {
      var n = t.originalEvent;
      n && (n.ctrlKey || n.metaKey) || this.trigger("close", {
        originalEvent: n,
        originalSelect2Event: t
      })
    }, e
  })), S.define("select2/dropdown/dropdownCss", ["../utils"], (function(e) {
    function t() {}
    return t.prototype.render = function(t) {
      var n = t.call(this);
      return -1 !== (t = this.options.get("dropdownCssClass") || "").indexOf(":all:") && (t = t.replace(":all:", ""), e.copyNonInternalCssClasses(n[0], this.$element[0])), n.addClass(t), n
    }, t
  })), S.define("select2/dropdown/tagsSearchHighlight", ["../utils"], (function(e) {
    function t() {}
    return t.prototype.highlightFirstItem = function(t) {
      if (0 < (n = this.$results.find(".select2-results__option--selectable:not(.select2-results__option--selected)")).length) {
        var n, r = n.first();
        if ((n = e.GetData(r[0], "data").element) && n.getAttribute && "true" === n.getAttribute("data-select2-tag")) return void r.trigger("mouseenter")
      }
      t.call(this)
    }, t
  })), S.define("select2/i18n/en", [], (function() {
    return {
      errorLoading: function() {
        return "The results could not be loaded."
      },
      inputTooLong: function(e) {
        var t = e.input.length - e.maximum;
        e = "Please delete " + t + " character";
        return 1 != t && (e += "s"), e
      },
      inputTooShort: function(e) {
        return "Please enter " + (e.minimum - e.input.length) + " or more characters"
      },
      loadingMore: function() {
        return "Loading more results…"
      },
      maximumSelected: function(e) {
        var t = "You can only select " + e.maximum + " item";
        return 1 != e.maximum && (t += "s"), t
      },
      noResults: function() {
        return "No results found"
      },
      searching: function() {
        return "Searching…"
      },
      removeAllItems: function() {
        return "Remove all items"
      },
      removeItem: function() {
        return "Remove item"
      },
      search: function() {
        return "Search"
      }
    }
  })), S.define("select2/defaults", ["jquery", "./results", "./selection/single", "./selection/multiple", "./selection/placeholder", "./selection/allowClear", "./selection/search", "./selection/selectionCss", "./selection/eventRelay", "./utils", "./translation", "./diacritics", "./data/select", "./data/array", "./data/ajax", "./data/tags", "./data/tokenizer", "./data/minimumInputLength", "./data/maximumInputLength", "./data/maximumSelectionLength", "./dropdown", "./dropdown/search", "./dropdown/hidePlaceholder", "./dropdown/infiniteScroll", "./dropdown/attachBody", "./dropdown/minimumResultsForSearch", "./dropdown/selectOnClose", "./dropdown/closeOnSelect", "./dropdown/dropdownCss", "./dropdown/tagsSearchHighlight", "./i18n/en"], (function(e, t, n, r, i, o, a, s, l, c, u, d, p, f, h, m, g, v, y, b, w, x, S, C, E, T, k, D, O, A, _) {
    function M() {
      this.reset()
    }
    return M.prototype.apply = function(u) {
      var d;
      null == (u = e.extend(!0, {}, this.defaults, u)).dataAdapter && (null != u.ajax ? u.dataAdapter = h : null != u.data ? u.dataAdapter = f : u.dataAdapter = p, 0 < u.minimumInputLength && (u.dataAdapter = c.Decorate(u.dataAdapter, v)), 0 < u.maximumInputLength && (u.dataAdapter = c.Decorate(u.dataAdapter, y)), 0 < u.maximumSelectionLength && (u.dataAdapter = c.Decorate(u.dataAdapter, b)), u.tags && (u.dataAdapter = c.Decorate(u.dataAdapter, m)), null == u.tokenSeparators && null == u.tokenizer || (u.dataAdapter = c.Decorate(u.dataAdapter, g))), null == u.resultsAdapter && (u.resultsAdapter = t, null != u.ajax && (u.resultsAdapter = c.Decorate(u.resultsAdapter, C)), null != u.placeholder && (u.resultsAdapter = c.Decorate(u.resultsAdapter, S)), u.selectOnClose && (u.resultsAdapter = c.Decorate(u.resultsAdapter, k)), u.tags && (u.resultsAdapter = c.Decorate(u.resultsAdapter, A))), null == u.dropdownAdapter && (u.multiple ? u.dropdownAdapter = w : (d = c.Decorate(w, x), u.dropdownAdapter = d), 0 !== u.minimumResultsForSearch && (u.dropdownAdapter = c.Decorate(u.dropdownAdapter, T)), u.closeOnSelect && (u.dropdownAdapter = c.Decorate(u.dropdownAdapter, D)), null != u.dropdownCssClass && (u.dropdownAdapter = c.Decorate(u.dropdownAdapter, O)), u.dropdownAdapter = c.Decorate(u.dropdownAdapter, E)), null == u.selectionAdapter && (u.multiple ? u.selectionAdapter = r : u.selectionAdapter = n, null != u.placeholder && (u.selectionAdapter = c.Decorate(u.selectionAdapter, i)), u.allowClear && (u.selectionAdapter = c.Decorate(u.selectionAdapter, o)), u.multiple && (u.selectionAdapter = c.Decorate(u.selectionAdapter, a)), null != u.selectionCssClass && (u.selectionAdapter = c.Decorate(u.selectionAdapter, s)), u.selectionAdapter = c.Decorate(u.selectionAdapter, l)), u.language = this._resolveLanguage(u.language), u.language.push("en");
      for (var _ = [], M = 0; M < u.language.length; M++) {
        var L = u.language[M]; - 1 === _.indexOf(L) && _.push(L)
      }
      return u.language = _, u.translations = this._processTranslations(u.language, u.debug), u
    }, M.prototype.reset = function() {
      function t(e) {
        return e.replace(/[^\u0000-\u007E]/g, (function(e) {
          return d[e] || e
        }))
      }
      this.defaults = {
        amdLanguageBase: "./i18n/",
        autocomplete: "off",
        closeOnSelect: !0,
        debug: !1,
        dropdownAutoWidth: !1,
        escapeMarkup: c.escapeMarkup,
        language: {},
        matcher: function n(r, i) {
          if (null == r.term || "" === r.term.trim()) return i;
          if (i.children && 0 < i.children.length) {
            for (var o = e.extend(!0, {}, i), a = i.children.length - 1; 0 <= a; a--) null == n(r, i.children[a]) && o.children.splice(a, 1);
            return 0 < o.children.length ? o : n(r, o)
          }
          var s = t(i.text).toUpperCase(),
            l = t(r.term).toUpperCase();
          return -1 < s.indexOf(l) ? i : null
        },
        minimumInputLength: 0,
        maximumInputLength: 0,
        maximumSelectionLength: 0,
        minimumResultsForSearch: 0,
        selectOnClose: !1,
        scrollAfterSelect: !1,
        sorter: function(e) {
          return e
        },
        templateResult: function(e) {
          return e.text
        },
        templateSelection: function(e) {
          return e.text
        },
        theme: "default",
        width: "resolve"
      }
    }, M.prototype.applyFromElement = function(e, t) {
      var n = e.language,
        r = this.defaults.language,
        i = t.prop("lang");
      t = t.closest("[lang]").prop("lang"), t = Array.prototype.concat.call(this._resolveLanguage(i), this._resolveLanguage(n), this._resolveLanguage(r), this._resolveLanguage(t));
      return e.language = t, e
    }, M.prototype._resolveLanguage = function(t) {
      if (!t) return [];
      if (e.isEmptyObject(t)) return [];
      if (e.isPlainObject(t)) return [t];
      for (var n, r = Array.isArray(t) ? t : [t], i = [], o = 0; o < r.length; o++) i.push(r[o]), "string" == typeof r[o] && 0 < r[o].indexOf("-") && (n = r[o].split("-")[0], i.push(n));
      return i
    }, M.prototype._processTranslations = function(t, n) {
      for (var r = new u, i = 0; i < t.length; i++) {
        var o = new u,
          a = t[i];
        if ("string" == typeof a) try {
          o = u.loadPath(a)
        } catch (t) {
          try {
            a = this.defaults.amdLanguageBase + a, o = u.loadPath(a)
          } catch (t) {
            n && window.console && console.warn && console.warn('Select2: The language file for "' + a + '" could not be automatically loaded. A fallback will be used instead.')
          }
        } else o = e.isPlainObject(a) ? new u(a) : a;
        r.extend(o)
      }
      return r
    }, M.prototype.set = function(t, n) {
      var r = {};
      r[e.camelCase(t)] = n, r = c._convertData(r), e.extend(!0, this.defaults, r)
    }, new M
  })), S.define("select2/options", ["jquery", "./defaults", "./utils"], (function(e, t, n) {
    function r(e, n) {
      this.options = e, null != n && this.fromElement(n), null != n && (this.options = t.applyFromElement(this.options, n)), this.options = t.apply(this.options)
    }
    return r.prototype.fromElement = function(t) {
      var r = ["select2"];
      null == this.options.multiple && (this.options.multiple = t.prop("multiple")), null == this.options.disabled && (this.options.disabled = t.prop("disabled")), null == this.options.autocomplete && t.prop("autocomplete") && (this.options.autocomplete = t.prop("autocomplete")), null == this.options.dir && (t.prop("dir") ? this.options.dir = t.prop("dir") : t.closest("[dir]").prop("dir") ? this.options.dir = t.closest("[dir]").prop("dir") : this.options.dir = "ltr"), t.prop("disabled", this.options.disabled), t.prop("multiple", this.options.multiple), n.GetData(t[0], "select2Tags") && (this.options.debug && window.console && console.warn && console.warn('Select2: The `data-select2-tags` attribute has been changed to use the `data-data` and `data-tags="true"` attributes and will be removed in future versions of Select2.'), n.StoreData(t[0], "data", n.GetData(t[0], "select2Tags")), n.StoreData(t[0], "tags", !0)), n.GetData(t[0], "ajaxUrl") && (this.options.debug && window.console && console.warn && console.warn("Select2: The `data-ajax-url` attribute has been changed to `data-ajax--url` and support for the old attribute will be removed in future versions of Select2."), t.attr("ajax--url", n.GetData(t[0], "ajaxUrl")), n.StoreData(t[0], "ajax-Url", n.GetData(t[0], "ajaxUrl")));
      var i = {};

      function o(e, t) {
        return t.toUpperCase()
      }
      for (var a = 0; a < t[0].attributes.length; a++) {
        var s = t[0].attributes[a].name,
          l = "data-";
        s.substr(0, l.length) == l && (s = s.substring(l.length), l = n.GetData(t[0], s), i[s.replace(/-([a-z])/g, o)] = l)
      }
      e.fn.jquery && "1." == e.fn.jquery.substr(0, 2) && t[0].dataset && (i = e.extend(!0, {}, t[0].dataset, i));
      var c, u = e.extend(!0, {}, n.GetData(t[0]), i);
      for (c in u = n._convertData(u)) - 1 < r.indexOf(c) || (e.isPlainObject(this.options[c]) ? e.extend(this.options[c], u[c]) : this.options[c] = u[c]);
      return this
    }, r.prototype.get = function(e) {
      return this.options[e]
    }, r.prototype.set = function(e, t) {
      this.options[e] = t
    }, r
  })), S.define("select2/core", ["jquery", "./options", "./utils", "./keys"], (function(e, t, n, r) {
    var i = function(e, r) {
      null != n.GetData(e[0], "select2") && n.GetData(e[0], "select2").destroy(), this.$element = e, this.id = this._generateId(e), r = r || {}, this.options = new t(r, e), i.__super__.constructor.call(this);
      var o = e.attr("tabindex") || 0;
      n.StoreData(e[0], "old-tabindex", o), e.attr("tabindex", "-1"), r = this.options.get("dataAdapter"), this.dataAdapter = new r(e, this.options), o = this.render(), this._placeContainer(o), r = this.options.get("selectionAdapter"), this.selection = new r(e, this.options), this.$selection = this.selection.render(), this.selection.position(this.$selection, o), r = this.options.get("dropdownAdapter"), this.dropdown = new r(e, this.options), this.$dropdown = this.dropdown.render(), this.dropdown.position(this.$dropdown, o), o = this.options.get("resultsAdapter"), this.results = new o(e, this.options, this.dataAdapter), this.$results = this.results.render(), this.results.position(this.$results, this.$dropdown);
      var a = this;
      this._bindAdapters(), this._registerDomEvents(), this._registerDataEvents(), this._registerSelectionEvents(), this._registerDropdownEvents(), this._registerResultsEvents(), this._registerEvents(), this.dataAdapter.current((function(e) {
        a.trigger("selection:update", {
          data: e
        })
      })), e[0].classList.add("select2-hidden-accessible"), e.attr("aria-hidden", "true"), this._syncAttributes(), n.StoreData(e[0], "select2", this), e.data("select2", this)
    };
    return n.Extend(i, n.Observable), i.prototype._generateId = function(e) {
      return "select2-" + (null != e.attr("id") ? e.attr("id") : null != e.attr("name") ? e.attr("name") + "-" + n.generateChars(2) : n.generateChars(4)).replace(/(:|\.|\[|\]|,)/g, "")
    }, i.prototype._placeContainer = function(e) {
      e.insertAfter(this.$element);
      var t = this._resolveWidth(this.$element, this.options.get("width"));
      null != t && e.css("width", t)
    }, i.prototype._resolveWidth = function(e, t) {
      var n = /^width:(([-+]?([0-9]*\.)?[0-9]+)(px|em|ex|%|in|cm|mm|pt|pc))/i;
      if ("resolve" == t) {
        var r = this._resolveWidth(e, "style");
        return null != r ? r : this._resolveWidth(e, "element")
      }
      if ("element" == t) return (r = e.outerWidth(!1)) <= 0 ? "auto" : r + "px";
      if ("style" != t) return "computedstyle" != t ? t : window.getComputedStyle(e[0]).width;
      if ("string" != typeof(e = e.attr("style"))) return null;
      for (var i = e.split(";"), o = 0, a = i.length; o < a; o += 1) {
        var s = i[o].replace(/\s/g, "").match(n);
        if (null !== s && 1 <= s.length) return s[1]
      }
      return null
    }, i.prototype._bindAdapters = function() {
      this.dataAdapter.bind(this, this.$container), this.selection.bind(this, this.$container), this.dropdown.bind(this, this.$container), this.results.bind(this, this.$container)
    }, i.prototype._registerDomEvents = function() {
      var e = this;
      this.$element.on("change.select2", (function() {
        e.dataAdapter.current((function(t) {
          e.trigger("selection:update", {
            data: t
          })
        }))
      })), this.$element.on("focus.select2", (function(t) {
        e.trigger("focus", t)
      })), this._syncA = n.bind(this._syncAttributes, this), this._syncS = n.bind(this._syncSubtree, this), this._observer = new window.MutationObserver((function(t) {
        e._syncA(), e._syncS(t)
      })), this._observer.observe(this.$element[0], {
        attributes: !0,
        childList: !0,
        subtree: !1
      })
    }, i.prototype._registerDataEvents = function() {
      var e = this;
      this.dataAdapter.on("*", (function(t, n) {
        e.trigger(t, n)
      }))
    }, i.prototype._registerSelectionEvents = function() {
      var e = this,
        t = ["toggle", "focus"];
      this.selection.on("toggle", (function() {
        e.toggleDropdown()
      })), this.selection.on("focus", (function(t) {
        e.focus(t)
      })), this.selection.on("*", (function(n, r) {
        -1 === t.indexOf(n) && e.trigger(n, r)
      }))
    }, i.prototype._registerDropdownEvents = function() {
      var e = this;
      this.dropdown.on("*", (function(t, n) {
        e.trigger(t, n)
      }))
    }, i.prototype._registerResultsEvents = function() {
      var e = this;
      this.results.on("*", (function(t, n) {
        e.trigger(t, n)
      }))
    }, i.prototype._registerEvents = function() {
      var e = this;
      this.on("open", (function() {
        e.$container[0].classList.add("select2-container--open")
      })), this.on("close", (function() {
        e.$container[0].classList.remove("select2-container--open")
      })), this.on("enable", (function() {
        e.$container[0].classList.remove("select2-container--disabled")
      })), this.on("disable", (function() {
        e.$container[0].classList.add("select2-container--disabled")
      })), this.on("blur", (function() {
        e.$container[0].classList.remove("select2-container--focus")
      })), this.on("query", (function(t) {
        e.isOpen() || e.trigger("open", {}), this.dataAdapter.query(t, (function(n) {
          e.trigger("results:all", {
            data: n,
            query: t
          })
        }))
      })), this.on("query:append", (function(t) {
        this.dataAdapter.query(t, (function(n) {
          e.trigger("results:append", {
            data: n,
            query: t
          })
        }))
      })), this.on("keypress", (function(t) {
        var n = t.which;
        e.isOpen() ? n === r.ESC || n === r.UP && t.altKey ? (e.close(t), t.preventDefault()) : n === r.ENTER || n === r.TAB ? (e.trigger("results:select", {}), t.preventDefault()) : n === r.SPACE && t.ctrlKey ? (e.trigger("results:toggle", {}), t.preventDefault()) : n === r.UP ? (e.trigger("results:previous", {}), t.preventDefault()) : n === r.DOWN && (e.trigger("results:next", {}), t.preventDefault()) : (n === r.ENTER || n === r.SPACE || n === r.DOWN && t.altKey) && (e.open(), t.preventDefault())
      }))
    }, i.prototype._syncAttributes = function() {
      this.options.set("disabled", this.$element.prop("disabled")), this.isDisabled() ? (this.isOpen() && this.close(), this.trigger("disable", {})) : this.trigger("enable", {})
    }, i.prototype._isChangeMutation = function(e) {
      var t = this;
      if (e.addedNodes && 0 < e.addedNodes.length) {
        for (var n = 0; n < e.addedNodes.length; n++)
          if (e.addedNodes[n].selected) return !0
      } else {
        if (e.removedNodes && 0 < e.removedNodes.length) return !0;
        if (Array.isArray(e)) return e.some((function(e) {
          return t._isChangeMutation(e)
        }))
      }
      return !1
    }, i.prototype._syncSubtree = function(e) {
      e = this._isChangeMutation(e);
      var t = this;
      e && this.dataAdapter.current((function(e) {
        t.trigger("selection:update", {
          data: e
        })
      }))
    }, i.prototype.trigger = function(e, t) {
      var n = i.__super__.trigger;
      if (void 0 === t && (t = {}), e in (o = {
          open: "opening",
          close: "closing",
          select: "selecting",
          unselect: "unselecting",
          clear: "clearing"
        })) {
        var r = o[e],
          o = {
            prevented: !1,
            name: e,
            args: t
          };
        if (n.call(this, r, o), o.prevented) return void(t.prevented = !0)
      }
      n.call(this, e, t)
    }, i.prototype.toggleDropdown = function() {
      this.isDisabled() || (this.isOpen() ? this.close() : this.open())
    }, i.prototype.open = function() {
      this.isOpen() || this.isDisabled() || this.trigger("query", {})
    }, i.prototype.close = function(e) {
      this.isOpen() && this.trigger("close", {
        originalEvent: e
      })
    }, i.prototype.isEnabled = function() {
      return !this.isDisabled()
    }, i.prototype.isDisabled = function() {
      return this.options.get("disabled")
    }, i.prototype.isOpen = function() {
      return this.$container[0].classList.contains("select2-container--open")
    }, i.prototype.hasFocus = function() {
      return this.$container[0].classList.contains("select2-container--focus")
    }, i.prototype.focus = function(e) {
      this.hasFocus() || (this.$container[0].classList.add("select2-container--focus"), this.trigger("focus", {}))
    }, i.prototype.enable = function(e) {
      this.options.get("debug") && window.console && console.warn && console.warn('Select2: The `select2("enable")` method has been deprecated and will be removed in later Select2 versions. Use $element.prop("disabled") instead.'), null != e && 0 !== e.length || (e = [!0]), e = !e[0], this.$element.prop("disabled", e)
    }, i.prototype.data = function() {
      this.options.get("debug") && 0 < arguments.length && window.console && console.warn && console.warn('Select2: Data can no longer be set using `select2("data")`. You should consider setting the value instead using `$element.val()`.');
      var e = [];
      return this.dataAdapter.current((function(t) {
        e = t
      })), e
    }, i.prototype.val = function(e) {
      if (this.options.get("debug") && window.console && console.warn && console.warn('Select2: The `select2("val")` method has been deprecated and will be removed in later Select2 versions. Use $element.val() instead.'), null == e || 0 === e.length) return this.$element.val();
      e = e[0], Array.isArray(e) && (e = e.map((function(e) {
        return e.toString()
      }))), this.$element.val(e).trigger("input").trigger("change")
    }, i.prototype.destroy = function() {
      n.RemoveData(this.$container[0]), this.$container.remove(), this._observer.disconnect(), this._observer = null, this._syncA = null, this._syncS = null, this.$element.off(".select2"), this.$element.attr("tabindex", n.GetData(this.$element[0], "old-tabindex")), this.$element[0].classList.remove("select2-hidden-accessible"), this.$element.attr("aria-hidden", "false"), n.RemoveData(this.$element[0]), this.$element.removeData("select2"), this.dataAdapter.destroy(), this.selection.destroy(), this.dropdown.destroy(), this.results.destroy(), this.dataAdapter = null, this.selection = null, this.dropdown = null, this.results = null
    }, i.prototype.render = function() {
      var t = e('<span class="select2 select2-container"><span class="selection"></span><span class="dropdown-wrapper" aria-hidden="true"></span></span>');
      return t.attr("dir", this.options.get("dir")), this.$container = t, this.$container[0].classList.add("select2-container--" + this.options.get("theme")), n.StoreData(t[0], "element", this.$element), t
    }, i
  })), S.define("select2/dropdown/attachContainer", [], (function() {
    function e(e, t, n) {
      e.call(this, t, n)
    }
    return e.prototype.position = function(e, t, n) {
      n.find(".dropdown-wrapper").append(t), t[0].classList.add("select2-dropdown--below"), n[0].classList.add("select2-container--below")
    }, e
  })), S.define("select2/dropdown/stopPropagation", [], (function() {
    function e() {}
    return e.prototype.bind = function(e, t, n) {
      e.call(this, t, n), this.$dropdown.on(["blur", "change", "click", "dblclick", "focus", "focusin", "focusout", "input", "keydown", "keyup", "keypress", "mousedown", "mouseenter", "mouseleave", "mousemove", "mouseover", "mouseup", "search", "touchend", "touchstart"].join(" "), (function(e) {
        e.stopPropagation()
      }))
    }, e
  })), S.define("select2/selection/stopPropagation", [], (function() {
    function e() {}
    return e.prototype.bind = function(e, t, n) {
      e.call(this, t, n), this.$selection.on(["blur", "change", "click", "dblclick", "focus", "focusin", "focusout", "input", "keydown", "keyup", "keypress", "mousedown", "mouseenter", "mouseleave", "mousemove", "mouseover", "mouseup", "search", "touchend", "touchstart"].join(" "), (function(e) {
        e.stopPropagation()
      }))
    }, e
  })), m = function(e) {
    var t, n, r = ["wheel", "mousewheel", "DOMMouseScroll", "MozMousePixelScroll"],
      i = "onwheel" in document || 9 <= document.documentMode ? ["wheel"] : ["mousewheel", "DomMouseScroll", "MozMousePixelScroll"],
      o = Array.prototype.slice;
    if (e.event.fixHooks)
      for (var a = r.length; a;) e.event.fixHooks[r[--a]] = e.event.mouseHooks;
    var s = e.event.special.mousewheel = {
      version: "3.1.12",
      setup: function() {
        if (this.addEventListener)
          for (var t = i.length; t;) this.addEventListener(i[--t], l, !1);
        else this.onmousewheel = l;
        e.data(this, "mousewheel-line-height", s.getLineHeight(this)), e.data(this, "mousewheel-page-height", s.getPageHeight(this))
      },
      teardown: function() {
        if (this.removeEventListener)
          for (var t = i.length; t;) this.removeEventListener(i[--t], l, !1);
        else this.onmousewheel = null;
        e.removeData(this, "mousewheel-line-height"), e.removeData(this, "mousewheel-page-height")
      },
      getLineHeight: function(t) {
        var n = e(t);
        return (t = n["offsetParent" in e.fn ? "offsetParent" : "parent"]()).length || (t = e("body")), parseInt(t.css("fontSize"), 10) || parseInt(n.css("fontSize"), 10) || 16
      },
      getPageHeight: function(t) {
        return e(t).height()
      },
      settings: {
        adjustOldDeltas: !0,
        normalizeOffset: !0
      }
    };

    function l(r) {
      var i, a = r || window.event,
        l = o.call(arguments, 1),
        d = 0,
        p = 0,
        f = 0,
        h = 0,
        m = 0,
        g = 0;
      if ((r = e.event.fix(a)).type = "mousewheel", "detail" in a && (f = -1 * a.detail), "wheelDelta" in a && (f = a.wheelDelta), "wheelDeltaY" in a && (f = a.wheelDeltaY), "wheelDeltaX" in a && (p = -1 * a.wheelDeltaX), "axis" in a && a.axis === a.HORIZONTAL_AXIS && (p = -1 * f, f = 0), d = 0 === f ? p : f, "deltaY" in a && (d = f = -1 * a.deltaY), "deltaX" in a && (p = a.deltaX, 0 === f && (d = -1 * p)), 0 !== f || 0 !== p) return 1 === a.deltaMode ? (d *= i = e.data(this, "mousewheel-line-height"), f *= i, p *= i) : 2 === a.deltaMode && (d *= i = e.data(this, "mousewheel-page-height"), f *= i, p *= i), h = Math.max(Math.abs(f), Math.abs(p)), (!n || h < n) && u(a, n = h) && (n /= 40), u(a, h) && (d /= 40, p /= 40, f /= 40), d = Math[1 <= d ? "floor" : "ceil"](d / n), p = Math[1 <= p ? "floor" : "ceil"](p / n), f = Math[1 <= f ? "floor" : "ceil"](f / n), s.settings.normalizeOffset && this.getBoundingClientRect && (h = this.getBoundingClientRect(), m = r.clientX - h.left, g = r.clientY - h.top), r.deltaX = p, r.deltaY = f, r.deltaFactor = n, r.offsetX = m, r.offsetY = g, r.deltaMode = 0, l.unshift(r, d, p, f), t && clearTimeout(t), t = setTimeout(c, 200), (e.event.dispatch || e.event.handle).apply(this, l)
    }

    function c() {
      n = null
    }

    function u(e, t) {
      return s.settings.adjustOldDeltas && "mousewheel" === e.type && t % 120 == 0
    }
    e.fn.extend({
      mousewheel: function(e) {
        return e ? this.bind("mousewheel", e) : this.trigger("mousewheel")
      },
      unmousewheel: function(e) {
        return this.unbind("mousewheel", e)
      }
    })
  }, "function" == typeof S.define && S.define.amd ? S.define("jquery-mousewheel", ["jquery"], m) : "object" == typeof exports ? module.exports = m : m(e), S.define("jquery.select2", ["jquery", "jquery-mousewheel", "./select2/core", "./select2/defaults", "./select2/utils"], (function(e, t, n, r, i) {
    var o;
    return null == e.fn.select2 && (o = ["open", "close", "destroy"], e.fn.select2 = function(t) {
      if ("object" == typeof(t = t || {})) return this.each((function() {
        var r = e.extend(!0, {}, t);
        new n(e(this), r)
      })), this;
      if ("string" != typeof t) throw new Error("Invalid arguments for Select2: " + t);
      var r, a = Array.prototype.slice.call(arguments, 1);
      return this.each((function() {
        var e = i.GetData(this, "select2");
        null == e && window.console && console.error && console.error("The select2('" + t + "') method was called on an element that is not using Select2."), r = e[t].apply(e, a)
      })), -1 < o.indexOf(t) ? this : r
    }), null == e.fn.select2.defaults && (e.fn.select2.defaults = r), n
  })), {
    define: S.define,
    require: S.require
  });

  function g(e, t) {
    return p.call(e, t)
  }

  function v(e, t) {
    var n, r, i, o, a, s, l, c, d, p, f = t && t.split("/"),
      m = u.map,
      g = m && m["*"] || {};
    if (e) {
      for (t = (e = e.split("/")).length - 1, u.nodeIdCompat && h.test(e[t]) && (e[t] = e[t].replace(h, "")), "." === e[0].charAt(0) && f && (e = f.slice(0, f.length - 1).concat(e)), c = 0; c < e.length; c++) "." === (p = e[c]) ? (e.splice(c, 1), --c) : ".." === p && (0 === c || 1 === c && ".." === e[2] || ".." === e[c - 1] || 0 < c && (e.splice(c - 1, 2), c -= 2));
      e = e.join("/")
    }
    if ((f || g) && m) {
      for (c = (n = e.split("/")).length; 0 < c; --c) {
        if (r = n.slice(0, c).join("/"), f)
          for (d = f.length; 0 < d; --d)
            if (i = (i = m[f.slice(0, d).join("/")]) && i[r]) {
              o = i, a = c;
              break
            } if (o) break;
        !s && g && g[r] && (s = g[r], l = c)
      }!o && s && (o = s, a = l), o && (n.splice(0, a, o), e = n.join("/"))
    }
    return e
  }

  function y(e, t) {
    return function() {
      var n = f.call(arguments, 0);
      return "string" != typeof n[0] && 1 === n.length && n.push(null), o.apply(r, n.concat([e, t]))
    }
  }

  function b(e) {
    var t;
    if (g(c, e) && (t = c[e], delete c[e], d[e] = !0, i.apply(r, t)), !g(l, e) && !g(d, e)) throw new Error("No " + e);
    return l[e]
  }

  function w(e) {
    var t, n = e ? e.indexOf("!") : -1;
    return -1 < n && (t = e.substring(0, n), e = e.substring(n + 1, e.length)), [t, e]
  }

  function x(e) {
    return e ? w(e) : []
  }
  var S = m.require("jquery.select2");
  return e.fn.select2.amd = m, S
})),
function(e) {
  "function" == typeof define && define.amd ? define(["jquery"], e) : "object" == typeof exports ? module.exports = e(require("jquery")) : e(jQuery)
}((function(e) {
  "use strict";
  var t = !1,
    n = !1,
    r = 0,
    i = 2e3,
    o = 0,
    a = e,
    s = document,
    l = window,
    c = a(l),
    u = [],
    d = l.requestAnimationFrame || l.webkitRequestAnimationFrame || l.mozRequestAnimationFrame || !1,
    p = l.cancelAnimationFrame || l.webkitCancelAnimationFrame || l.mozCancelAnimationFrame || !1;
  if (d) l.cancelAnimationFrame || (p = function(e) {});
  else {
    var f = 0;
    d = function(e, t) {
      var n = (new Date).getTime(),
        r = Math.max(0, 16 - (n - f)),
        i = l.setTimeout((function() {
          e(n + r)
        }), r);
      return f = n + r, i
    }, p = function(e) {
      l.clearTimeout(e)
    }
  }
  var h = l.MutationObserver || l.WebKitMutationObserver || !1,
    m = Date.now || function() {
      return (new Date).getTime()
    },
    g = {
      zindex: "auto",
      cursoropacitymin: 0,
      cursoropacitymax: 1,
      cursorcolor: "#424242",
      cursorwidth: "6px",
      cursorborder: "1px solid #fff",
      cursorborderradius: "5px",
      scrollspeed: 40,
      mousescrollstep: 27,
      touchbehavior: !1,
      emulatetouch: !1,
      hwacceleration: !0,
      usetransition: !0,
      boxzoom: !1,
      dblclickzoom: !0,
      gesturezoom: !0,
      grabcursorenabled: !0,
      autohidemode: !0,
      background: "",
      iframeautoresize: !0,
      cursorminheight: 32,
      preservenativescrolling: !0,
      railoffset: !1,
      railhoffset: !1,
      bouncescroll: !0,
      spacebarenabled: !0,
      railpadding: {
        top: 0,
        right: 0,
        left: 0,
        bottom: 0
      },
      disableoutline: !0,
      horizrailenabled: !0,
      railalign: "right",
      railvalign: "bottom",
      enabletranslate3d: !0,
      enablemousewheel: !0,
      enablekeyboard: !0,
      smoothscroll: !0,
      sensitiverail: !0,
      enablemouselockapi: !0,
      cursorfixedheight: !1,
      directionlockdeadzone: 6,
      hidecursordelay: 400,
      nativeparentscrolling: !0,
      enablescrollonselection: !0,
      overflowx: !0,
      overflowy: !0,
      cursordragspeed: .3,
      rtlmode: "auto",
      cursordragontouch: !1,
      oneaxismousemode: "auto",
      scriptpath: function() {
        var e = s.currentScript || function() {
            var e = s.getElementsByTagName("script");
            return !!e.length && e[e.length - 1]
          }(),
          t = e ? e.src.split("?")[0] : "";
        return t.split("/").length > 0 ? t.split("/").slice(0, -1).join("/") + "/" : ""
      }(),
      preventmultitouchscrolling: !0,
      disablemutationobserver: !1,
      enableobserver: !0,
      scrollbarid: !1
    },
    v = !1,
    y = function() {
      if (v) return v;
      var e = s.createElement("DIV"),
        t = e.style,
        n = navigator.userAgent,
        r = navigator.platform,
        i = {};
      return i.haspointerlock = "pointerLockElement" in s || "webkitPointerLockElement" in s || "mozPointerLockElement" in s, i.isopera = "opera" in l, i.isopera12 = i.isopera && "getUserMedia" in navigator, i.isoperamini = "[object OperaMini]" === Object.prototype.toString.call(l.operamini), i.isie = "all" in s && "attachEvent" in e && !i.isopera, i.isieold = i.isie && !("msInterpolationMode" in t), i.isie7 = i.isie && !i.isieold && (!("documentMode" in s) || 7 === s.documentMode), i.isie8 = i.isie && "documentMode" in s && 8 === s.documentMode, i.isie9 = i.isie && "performance" in l && 9 === s.documentMode, i.isie10 = i.isie && "performance" in l && 10 === s.documentMode, i.isie11 = "msRequestFullscreen" in e && s.documentMode >= 11, i.ismsedge = "msCredentials" in l, i.ismozilla = "MozAppearance" in t, i.iswebkit = !i.ismsedge && "WebkitAppearance" in t, i.ischrome = i.iswebkit && "chrome" in l, i.ischrome38 = i.ischrome && "touchAction" in t, i.ischrome22 = !i.ischrome38 && i.ischrome && i.haspointerlock, i.ischrome26 = !i.ischrome38 && i.ischrome && "transition" in t, i.cantouch = "ontouchstart" in s.documentElement || "ontouchstart" in l, i.hasw3ctouch = !!l.PointerEvent && (navigator.maxTouchPoints > 0 || navigator.msMaxTouchPoints > 0), i.hasmstouch = !i.hasw3ctouch && (l.MSPointerEvent || !1), i.ismac = /^mac$/i.test(r), i.isios = i.cantouch && /iphone|ipad|ipod/i.test(r), i.isios4 = i.isios && !("seal" in Object), i.isios7 = i.isios && "webkitHidden" in s, i.isios8 = i.isios && "hidden" in s, i.isios10 = i.isios && l.Proxy, i.isandroid = /android/i.test(n), i.haseventlistener = "addEventListener" in e, i.trstyle = !1, i.hastransform = !1, i.hastranslate3d = !1, i.transitionstyle = !1, i.hastransition = !1, i.transitionend = !1, i.trstyle = "transform", i.hastransform = "transform" in t || function() {
        for (var e = ["msTransform", "webkitTransform", "MozTransform", "OTransform"], n = 0, r = e.length; n < r; n++)
          if (void 0 !== t[e[n]]) {
            i.trstyle = e[n];
            break
          } i.hastransform = !!i.trstyle
      }(), i.hastransform && (t[i.trstyle] = "translate3d(1px,2px,3px)", i.hastranslate3d = /translate3d/.test(t[i.trstyle])), i.transitionstyle = "transition", i.prefixstyle = "", i.transitionend = "transitionend", i.hastransition = "transition" in t || function() {
        i.transitionend = !1;
        for (var e = ["webkitTransition", "msTransition", "MozTransition", "OTransition", "OTransition", "KhtmlTransition"], n = ["-webkit-", "-ms-", "-moz-", "-o-", "-o", "-khtml-"], r = ["webkitTransitionEnd", "msTransitionEnd", "transitionend", "otransitionend", "oTransitionEnd", "KhtmlTransitionEnd"], o = 0, a = e.length; o < a; o++)
          if (e[o] in t) {
            i.transitionstyle = e[o], i.prefixstyle = n[o], i.transitionend = r[o];
            break
          } i.ischrome26 && (i.prefixstyle = n[1]), i.hastransition = i.transitionstyle
      }(), i.cursorgrabvalue = function() {
        var e = ["grab", "-webkit-grab", "-moz-grab"];
        (i.ischrome && !i.ischrome38 || i.isie) && (e = []);
        for (var n = 0, r = e.length; n < r; n++) {
          var o = e[n];
          if (t.cursor = o, t.cursor == o) return o
        }
        return "url(https://cdnjs.cloudflare.com/ajax/libs/slider-pro/1.3.0/css/images/openhand.cur),n-resize"
      }(), i.hasmousecapture = "setCapture" in e, i.hasMutationObserver = !1 !== h, e = null, v = i, i
    },
    b = function(e, f) {
      function v() {
        var e = E.doc.css(_.trstyle);
        return !(!e || "matrix" != e.substr(0, 6)) && e.replace(/^.*\((.*)\)$/g, "$1").replace(/px/g, "").split(/, +/)
      }

      function b(e, t, n) {
        var r = e.css(t),
          i = parseFloat(r);
        if (isNaN(i)) {
          var o = 3 == (i = I[r] || 0) ? n ? E.win.outerHeight() - E.win.innerHeight() : E.win.outerWidth() - E.win.innerWidth() : 1;
          return E.isie8 && i && (i += 1), o ? i : 0
        }
        return i
      }

      function x(e, t, n, r) {
        E._bind(e, t, (function(r) {
          var i = {
            original: r = r || l.event,
            target: r.target || r.srcElement,
            type: "wheel",
            deltaMode: "MozMousePixelScroll" == r.type ? 0 : 1,
            deltaX: 0,
            deltaZ: 0,
            preventDefault: function() {
              return r.preventDefault ? r.preventDefault() : r.returnValue = !1, !1
            },
            stopImmediatePropagation: function() {
              r.stopImmediatePropagation ? r.stopImmediatePropagation() : r.cancelBubble = !0
            }
          };
          return "mousewheel" == t ? (r.wheelDeltaX && (i.deltaX = -.025 * r.wheelDeltaX), r.wheelDeltaY && (i.deltaY = -.025 * r.wheelDeltaY), !i.deltaY && !i.deltaX && (i.deltaY = -.025 * r.wheelDelta)) : i.deltaY = r.detail, n.call(e, i)
        }), r)
      }

      function S(e, t, n, r) {
        E.scrollrunning || (E.newscrolly = E.getScrollTop(), E.newscrollx = E.getScrollLeft(), $ = m());
        var i = m() - $;
        if ($ = m(), i > 350 ? H = 1 : H += (2 - H) / 10, t = t * H | 0, e = e * H | 0) {
          if (r)
            if (e < 0) {
              if (E.getScrollLeft() >= E.page.maxw) return !0
            } else if (E.getScrollLeft() <= 0) return !0;
          var o = e > 0 ? 1 : -1;
          R !== o && (E.scrollmom && E.scrollmom.stop(), E.newscrollx = E.getScrollLeft(), R = o), E.lastdeltax -= e
        }
        if (t) {
          if (function() {
              var e = E.getScrollTop();
              if (t < 0) {
                if (e >= E.page.maxh) return !0
              } else if (e <= 0) return !0
            }()) {
            if (k.nativeparentscrolling && n && !E.ispage && !E.zoomactive) return !0;
            var a = E.view.h >> 1;
            E.newscrolly < -a ? (E.newscrolly = -a, t = -1) : E.newscrolly > E.page.maxh + a ? (E.newscrolly = E.page.maxh + a, t = 1) : t = 0
          }
          var s = t > 0 ? 1 : -1;
          z !== s && (E.scrollmom && E.scrollmom.stop(), E.newscrolly = E.getScrollTop(), z = s), E.lastdeltay -= t
        }(t || e) && E.synched("relativexy", (function() {
          var e = E.lastdeltay + E.newscrolly;
          E.lastdeltay = 0;
          var t = E.lastdeltax + E.newscrollx;
          E.lastdeltax = 0, E.rail.drag || E.doScrollPos(t, e)
        }))
      }

      function C(e, t, n) {
        var r, i;
        return !(n || !F) || (0 === e.deltaMode ? (r = -e.deltaX * (k.mousescrollstep / 54) | 0, i = -e.deltaY * (k.mousescrollstep / 54) | 0) : 1 === e.deltaMode && (r = -e.deltaX * k.mousescrollstep * 50 / 80 | 0, i = -e.deltaY * k.mousescrollstep * 50 / 80 | 0), t && k.oneaxismousemode && 0 === r && i && (r = i, i = 0, n && (r < 0 ? E.getScrollLeft() >= E.page.maxw : E.getScrollLeft() <= 0) && (i = r, r = 0)), E.isrtlmode && (r = -r), S(r, i, n, !0) ? void(n && (F = !0)) : (F = !1, e.stopImmediatePropagation(), e.preventDefault()))
      }
      var E = this;
      this.version = "3.7.6", this.name = "nicescroll", this.me = f;
      var T = a("body"),
        k = this.opt = {
          doc: T,
          win: !1
        };
      if (a.extend(k, g), k.snapbackspeed = 80, e)
        for (var D in k) void 0 !== e[D] && (k[D] = e[D]);
      if (k.disablemutationobserver && (h = !1), this.doc = k.doc, this.iddoc = this.doc && this.doc[0] && this.doc[0].id || "", this.ispage = /^BODY|HTML/.test(k.win ? k.win[0].nodeName : this.doc[0].nodeName), this.haswrapper = !1 !== k.win, this.win = k.win || (this.ispage ? c : this.doc), this.docscroll = this.ispage && !this.haswrapper ? c : this.win, this.body = T, this.viewport = !1, this.isfixed = !1, this.iframe = !1, this.isiframe = "IFRAME" == this.doc[0].nodeName && "IFRAME" == this.win[0].nodeName, this.istextarea = "TEXTAREA" == this.win[0].nodeName, this.forcescreen = !1, this.canshowonmouseevent = "scroll" != k.autohidemode, this.onmousedown = !1, this.onmouseup = !1, this.onmousemove = !1, this.onmousewheel = !1, this.onkeypress = !1, this.ongesturezoom = !1, this.onclick = !1, this.onscrollstart = !1, this.onscrollend = !1, this.onscrollcancel = !1, this.onzoomin = !1, this.onzoomout = !1, this.view = !1, this.page = !1, this.scroll = {
          x: 0,
          y: 0
        }, this.scrollratio = {
          x: 0,
          y: 0
        }, this.cursorheight = 20, this.scrollvaluemax = 0, "auto" == k.rtlmode) {
        var O = this.win[0] == l ? this.body : this.win,
          A = O.css("writing-mode") || O.css("-webkit-writing-mode") || O.css("-ms-writing-mode") || O.css("-moz-writing-mode");
        "horizontal-tb" == A || "lr-tb" == A || "" === A ? (this.isrtlmode = "rtl" == O.css("direction"), this.isvertical = !1) : (this.isrtlmode = "vertical-rl" == A || "tb" == A || "tb-rl" == A || "rl-tb" == A, this.isvertical = "vertical-rl" == A || "tb" == A || "tb-rl" == A)
      } else this.isrtlmode = !0 === k.rtlmode, this.isvertical = !1;
      if (this.scrollrunning = !1, this.scrollmom = !1, this.observer = !1, this.observerremover = !1, this.observerbody = !1, !1 !== k.scrollbarid) this.id = k.scrollbarid;
      else
        do {
          this.id = "ascrail" + i++
        } while (s.getElementById(this.id));
      this.rail = !1, this.cursor = !1, this.cursorfreezed = !1, this.selectiondrag = !1, this.zoom = !1, this.zoomactive = !1, this.hasfocus = !1, this.hasmousefocus = !1, this.railslocked = !1, this.locked = !1, this.hidden = !1, this.cursoractive = !0, this.wheelprevented = !1, this.overflowx = k.overflowx, this.overflowy = k.overflowy, this.nativescrollingarea = !1, this.checkarea = 0, this.events = [], this.saved = {}, this.delaylist = {}, this.synclist = {}, this.lastdeltax = 0, this.lastdeltay = 0, this.detected = y();
      var _ = a.extend({}, this.detected);
      this.canhwscroll = _.hastransform && k.hwacceleration, this.ishwscroll = this.canhwscroll && E.haswrapper, this.isrtlmode ? this.isvertical ? this.hasreversehr = !(_.iswebkit || _.isie || _.isie11) : this.hasreversehr = !(_.iswebkit || _.isie && !_.isie10 && !_.isie11) : this.hasreversehr = !1, this.istouchcapable = !1, (_.cantouch || !_.hasw3ctouch && !_.hasmstouch) && (!_.cantouch || _.isios || _.isandroid || !_.iswebkit && !_.ismozilla) || (this.istouchcapable = !0), k.enablemouselockapi || (_.hasmousecapture = !1, _.haspointerlock = !1), this.debounced = function(e, t, n) {
        E && (E.delaylist[e] || (E.delaylist[e] = {
          h: d((function() {
            E.delaylist[e].fn.call(E), E.delaylist[e] = !1
          }), n)
        }, t.call(E)), E.delaylist[e].fn = t)
      }, this.synched = function(e, t) {
        E.synclist[e] ? E.synclist[e] = t : (E.synclist[e] = t, d((function() {
          E && (E.synclist[e] && E.synclist[e].call(E), E.synclist[e] = null)
        })))
      }, this.unsynched = function(e) {
        E.synclist[e] && (E.synclist[e] = !1)
      }, this.css = function(e, t) {
        for (var n in t) E.saved.css.push([e, n, e.css(n)]), e.css(n, t[n])
      }, this.scrollTop = function(e) {
        return void 0 === e ? E.getScrollTop() : E.setScrollTop(e)
      }, this.scrollLeft = function(e) {
        return void 0 === e ? E.getScrollLeft() : E.setScrollLeft(e)
      };
      var M = function(e, t, n, r, i, o, a) {
        this.st = e, this.ed = t, this.spd = n, this.p1 = r || 0, this.p2 = i || 1, this.p3 = o || 0, this.p4 = a || 1, this.ts = m(), this.df = t - e
      };
      if (M.prototype = {
          B2: function(e) {
            return 3 * (1 - e) * (1 - e) * e
          },
          B3: function(e) {
            return 3 * (1 - e) * e * e
          },
          B4: function(e) {
            return e * e * e
          },
          getPos: function() {
            return (m() - this.ts) / this.spd
          },
          getNow: function() {
            var e = (m() - this.ts) / this.spd,
              t = this.B2(e) + this.B3(e) + this.B4(e);
            return e >= 1 ? this.ed : this.st + this.df * t | 0
          },
          update: function(e, t) {
            return this.st = this.getNow(), this.ed = e, this.spd = t, this.ts = m(), this.df = this.ed - this.st, this
          }
        }, this.ishwscroll) {
        this.doc.translate = {
          x: 0,
          y: 0,
          tx: "0px",
          ty: "0px"
        }, _.hastranslate3d && _.isios && this.doc.css("-webkit-backface-visibility", "hidden"), this.getScrollTop = function(e) {
          if (!e) {
            var t = v();
            if (t) return 16 == t.length ? -t[13] : -t[5];
            if (E.timerscroll && E.timerscroll.bz) return E.timerscroll.bz.getNow()
          }
          return E.doc.translate.y
        }, this.getScrollLeft = function(e) {
          if (!e) {
            var t = v();
            if (t) return 16 == t.length ? -t[12] : -t[4];
            if (E.timerscroll && E.timerscroll.bh) return E.timerscroll.bh.getNow()
          }
          return E.doc.translate.x
        }, this.notifyScrollEvent = function(e) {
          var t = s.createEvent("UIEvents");
          t.initUIEvent("scroll", !1, !1, l, 1), t.niceevent = !0, e.dispatchEvent(t)
        };
        var L = this.isrtlmode ? 1 : -1;
        _.hastranslate3d && k.enabletranslate3d ? (this.setScrollTop = function(e, t) {
          E.doc.translate.y = e, E.doc.translate.ty = -1 * e + "px", E.doc.css(_.trstyle, "translate3d(" + E.doc.translate.tx + "," + E.doc.translate.ty + ",0)"), t || E.notifyScrollEvent(E.win[0])
        }, this.setScrollLeft = function(e, t) {
          E.doc.translate.x = e, E.doc.translate.tx = e * L + "px", E.doc.css(_.trstyle, "translate3d(" + E.doc.translate.tx + "," + E.doc.translate.ty + ",0)"), t || E.notifyScrollEvent(E.win[0])
        }) : (this.setScrollTop = function(e, t) {
          E.doc.translate.y = e, E.doc.translate.ty = -1 * e + "px", E.doc.css(_.trstyle, "translate(" + E.doc.translate.tx + "," + E.doc.translate.ty + ")"), t || E.notifyScrollEvent(E.win[0])
        }, this.setScrollLeft = function(e, t) {
          E.doc.translate.x = e, E.doc.translate.tx = e * L + "px", E.doc.css(_.trstyle, "translate(" + E.doc.translate.tx + "," + E.doc.translate.ty + ")"), t || E.notifyScrollEvent(E.win[0])
        })
      } else this.getScrollTop = function() {
        return E.docscroll.scrollTop()
      }, this.setScrollTop = function(e) {
        E.docscroll.scrollTop(e)
      }, this.getScrollLeft = function() {
        return E.hasreversehr ? E.detected.ismozilla ? E.page.maxw - Math.abs(E.docscroll.scrollLeft()) : E.page.maxw - E.docscroll.scrollLeft() : E.docscroll.scrollLeft()
      }, this.setScrollLeft = function(e) {
        return setTimeout((function() {
          if (E) return E.hasreversehr && (e = E.detected.ismozilla ? -(E.page.maxw - e) : E.page.maxw - e), E.docscroll.scrollLeft(e)
        }), 1)
      };
      this.getTarget = function(e) {
        return !!e && (e.target ? e.target : !!e.srcElement && e.srcElement)
      }, this.hasParent = function(e, t) {
        if (!e) return !1;
        for (var n = e.target || e.srcElement || e || !1; n && n.id != t;) n = n.parentNode || !1;
        return !1 !== n
      };
      var I = {
        thin: 1,
        medium: 3,
        thick: 5
      };
      this.getDocumentScrollOffset = function() {
        return {
          top: l.pageYOffset || s.documentElement.scrollTop,
          left: l.pageXOffset || s.documentElement.scrollLeft
        }
      }, this.getOffset = function() {
        if (E.isfixed) {
          var e = E.win.offset(),
            t = E.getDocumentScrollOffset();
          return e.top -= t.top, e.left -= t.left, e
        }
        var n = E.win.offset();
        if (!E.viewport) return n;
        var r = E.viewport.offset();
        return {
          top: n.top - r.top,
          left: n.left - r.left
        }
      }, this.updateScrollBar = function(e) {
        var t, n;
        if (E.ishwscroll) E.rail.css({
          height: E.win.innerHeight() - (k.railpadding.top + k.railpadding.bottom)
        }), E.railh && E.railh.css({
          width: E.win.innerWidth() - (k.railpadding.left + k.railpadding.right)
        });
        else {
          var r = E.getOffset();
          if ((t = {
              top: r.top,
              left: r.left - (k.railpadding.left + k.railpadding.right)
            }).top += b(E.win, "border-top-width", !0), t.left += E.rail.align ? E.win.outerWidth() - b(E.win, "border-right-width") - E.rail.width : b(E.win, "border-left-width"), (n = k.railoffset) && (n.top && (t.top += n.top), n.left && (t.left += n.left)), E.railslocked || E.rail.css({
              top: t.top,
              left: t.left,
              height: (e ? e.h : E.win.innerHeight()) - (k.railpadding.top + k.railpadding.bottom)
            }), E.zoom && E.zoom.css({
              top: t.top + 1,
              left: 1 == E.rail.align ? t.left - 20 : t.left + E.rail.width + 4
            }), E.railh && !E.railslocked) {
            t = {
              top: r.top,
              left: r.left
            }, (n = k.railhoffset) && (n.top && (t.top += n.top), n.left && (t.left += n.left));
            var i = E.railh.align ? t.top + b(E.win, "border-top-width", !0) + E.win.innerHeight() - E.railh.height : t.top + b(E.win, "border-top-width", !0),
              o = t.left + b(E.win, "border-left-width");
            E.railh.css({
              top: i - (k.railpadding.top + k.railpadding.bottom),
              left: o,
              width: E.railh.width
            })
          }
        }
      }, this.doRailClick = function(e, t, n) {
        var r, i, o, a;
        E.railslocked || (E.cancelEvent(e), "pageY" in e || (e.pageX = e.clientX + s.documentElement.scrollLeft, e.pageY = e.clientY + s.documentElement.scrollTop), t ? (r = n ? E.doScrollLeft : E.doScrollTop, o = n ? (e.pageX - E.railh.offset().left - E.cursorwidth / 2) * E.scrollratio.x : (e.pageY - E.rail.offset().top - E.cursorheight / 2) * E.scrollratio.y, E.unsynched("relativexy"), r(0 | o)) : (r = n ? E.doScrollLeftBy : E.doScrollBy, o = n ? E.scroll.x : E.scroll.y, a = n ? e.pageX - E.railh.offset().left : e.pageY - E.rail.offset().top, i = n ? E.view.w : E.view.h, r(o >= a ? i : -i)))
      }, E.newscrolly = E.newscrollx = 0, E.hasanimationframe = "requestAnimationFrame" in l, E.hascancelanimationframe = "cancelAnimationFrame" in l, E.hasborderbox = !1, this.init = function() {
        if (E.saved.css = [], _.isoperamini) return !0;
        if (_.isandroid && !("hidden" in s)) return !0;
        k.emulatetouch = k.emulatetouch || k.touchbehavior, E.hasborderbox = l.getComputedStyle && "border-box" === l.getComputedStyle(s.body)["box-sizing"];
        var e = {
          "overflow-y": "hidden"
        };
        if ((_.isie11 || _.isie10) && (e["-ms-overflow-style"] = "none"), E.ishwscroll && (this.doc.css(_.transitionstyle, _.prefixstyle + "transform 0ms ease-out"), _.transitionend && E.bind(E.doc, _.transitionend, E.onScrollTransitionEnd, !1)), E.zindex = "auto", E.ispage || "auto" != k.zindex ? E.zindex = k.zindex : E.zindex = function() {
            var e = E.win;
            if ("zIndex" in e) return e.zIndex();
            for (; e.length > 0;) {
              if (9 == e[0].nodeType) return !1;
              var t = e.css("zIndex");
              if (!isNaN(t) && 0 !== t) return parseInt(t);
              e = e.parent()
            }
            return !1
          }() || "auto", !E.ispage && "auto" != E.zindex && E.zindex > o && (o = E.zindex), E.isie && 0 === E.zindex && "auto" == k.zindex && (E.zindex = "auto"), !E.ispage || !_.isieold) {
          var i = E.docscroll;
          E.ispage && (i = E.haswrapper ? E.win : E.doc), E.css(i, e), E.ispage && (_.isie11 || _.isie) && E.css(a("html"), e), !_.isios || E.ispage || E.haswrapper || E.css(T, {
            "-webkit-overflow-scrolling": "touch"
          });
          var u = a(s.createElement("div"));
          u.css({
            position: "relative",
            top: 0,
            float: "right",
            width: k.cursorwidth,
            height: 0,
            "background-color": k.cursorcolor,
            border: k.cursorborder,
            "background-clip": "padding-box",
            "-webkit-border-radius": k.cursorborderradius,
            "-moz-border-radius": k.cursorborderradius,
            "border-radius": k.cursorborderradius
          }), u.addClass("nicescroll-cursors"), E.cursor = u;
          var d = a(s.createElement("div"));
          d.attr("id", E.id), d.addClass("nicescroll-rails nicescroll-rails-vr");
          var p, f, m = ["left", "right", "top", "bottom"];
          for (var g in m) f = m[g], (p = k.railpadding[f] || 0) && d.css("padding-" + f, p + "px");
          d.append(u), d.width = Math.max(parseFloat(k.cursorwidth), u.outerWidth()), d.css({
            width: d.width + "px",
            zIndex: E.zindex,
            background: k.background,
            cursor: "default"
          }), d.visibility = !0, d.scrollable = !0, d.align = "left" == k.railalign ? 0 : 1, E.rail = d, E.rail.drag = !1;
          var v, y = !1;
          if (!k.boxzoom || E.ispage || _.isieold || (y = s.createElement("div"), E.bind(y, "click", E.doZoom), E.bind(y, "mouseenter", (function() {
              E.zoom.css("opacity", k.cursoropacitymax)
            })), E.bind(y, "mouseleave", (function() {
              E.zoom.css("opacity", k.cursoropacitymin)
            })), E.zoom = a(y), E.zoom.css({
              cursor: "pointer",
              zIndex: E.zindex,
              backgroundImage: "url(" + k.scriptpath + "zoomico.png)",
              height: 18,
              width: 18,
              backgroundPosition: "0 0"
            }), k.dblclickzoom && E.bind(E.win, "dblclick", E.doZoom), _.cantouch && k.gesturezoom && (E.ongesturezoom = function(e) {
              return e.scale > 1.5 && E.doZoomIn(e), e.scale < .8 && E.doZoomOut(e), E.cancelEvent(e)
            }, E.bind(E.win, "gestureend", E.ongesturezoom))), E.railh = !1, k.horizrailenabled && (E.css(i, {
              overflowX: "hidden"
            }), (u = a(s.createElement("div"))).css({
              position: "absolute",
              top: 0,
              height: k.cursorwidth,
              width: 0,
              backgroundColor: k.cursorcolor,
              border: k.cursorborder,
              backgroundClip: "padding-box",
              "-webkit-border-radius": k.cursorborderradius,
              "-moz-border-radius": k.cursorborderradius,
              "border-radius": k.cursorborderradius
            }), _.isieold && u.css("overflow", "hidden"), u.addClass("nicescroll-cursors"), E.cursorh = u, (v = a(s.createElement("div"))).attr("id", E.id + "-hr"), v.addClass("nicescroll-rails nicescroll-rails-hr"), v.height = Math.max(parseFloat(k.cursorwidth), u.outerHeight()), v.css({
              height: v.height + "px",
              zIndex: E.zindex,
              background: k.background
            }), v.append(u), v.visibility = !0, v.scrollable = !0, v.align = "top" == k.railvalign ? 0 : 1, E.railh = v, E.railh.drag = !1), E.ispage) d.css({
            position: "fixed",
            top: 0,
            height: "100%"
          }), d.css(d.align ? {
            right: 0
          } : {
            left: 0
          }), E.body.append(d), E.railh && (v.css({
            position: "fixed",
            left: 0,
            width: "100%"
          }), v.css(v.align ? {
            bottom: 0
          } : {
            top: 0
          }), E.body.append(v));
          else {
            if (E.ishwscroll) {
              "static" == E.win.css("position") && E.css(E.win, {
                position: "relative"
              });
              var b = "HTML" == E.win[0].nodeName ? E.body : E.win;
              a(b).scrollTop(0).scrollLeft(0), E.zoom && (E.zoom.css({
                position: "absolute",
                top: 1,
                right: 0,
                "margin-right": d.width + 4
              }), b.append(E.zoom)), d.css({
                position: "absolute",
                top: 0
              }), d.css(d.align ? {
                right: 0
              } : {
                left: 0
              }), b.append(d), v && (v.css({
                position: "absolute",
                left: 0,
                bottom: 0
              }), v.css(v.align ? {
                bottom: 0
              } : {
                top: 0
              }), b.append(v))
            } else {
              E.isfixed = "fixed" == E.win.css("position");
              var x = E.isfixed ? "fixed" : "absolute";
              E.isfixed || (E.viewport = E.getViewport(E.win[0])), E.viewport && (E.body = E.viewport, /fixed|absolute/.test(E.viewport.css("position")) || E.css(E.viewport, {
                position: "relative"
              })), d.css({
                position: x
              }), E.zoom && E.zoom.css({
                position: x
              }), E.updateScrollBar(), E.body.append(d), E.zoom && E.body.append(E.zoom), E.railh && (v.css({
                position: x
              }), E.body.append(v))
            }
            _.isios && E.css(E.win, {
              "-webkit-tap-highlight-color": "rgba(0,0,0,0)",
              "-webkit-touch-callout": "none"
            }), k.disableoutline && (_.isie && E.win.attr("hideFocus", "true"), _.iswebkit && E.win.css("outline", "none"))
          }
          if (!1 === k.autohidemode ? (E.autohidedom = !1, E.rail.css({
              opacity: k.cursoropacitymax
            }), E.railh && E.railh.css({
              opacity: k.cursoropacitymax
            })) : !0 === k.autohidemode || "leave" === k.autohidemode ? (E.autohidedom = a().add(E.rail), _.isie8 && (E.autohidedom = E.autohidedom.add(E.cursor)), E.railh && (E.autohidedom = E.autohidedom.add(E.railh)), E.railh && _.isie8 && (E.autohidedom = E.autohidedom.add(E.cursorh))) : "scroll" == k.autohidemode ? (E.autohidedom = a().add(E.rail), E.railh && (E.autohidedom = E.autohidedom.add(E.railh))) : "cursor" == k.autohidemode ? (E.autohidedom = a().add(E.cursor), E.railh && (E.autohidedom = E.autohidedom.add(E.cursorh))) : "hidden" == k.autohidemode && (E.autohidedom = !1, E.hide(), E.railslocked = !1), _.cantouch || E.istouchcapable || k.emulatetouch || _.hasmstouch) {
            E.scrollmom = new w(E), E.ontouchstart = function(e) {
              if (E.locked) return !1;
              if (e.pointerType && ("mouse" === e.pointerType || e.pointerType === e.MSPOINTER_TYPE_MOUSE)) return !1;
              if (E.hasmoving = !1, E.scrollmom.timer && (E.triggerScrollEnd(), E.scrollmom.stop()), !E.railslocked) {
                var t = E.getTarget(e);
                if (t && /INPUT/i.test(t.nodeName) && /range/i.test(t.type)) return E.stopPropagation(e);
                var n = "mousedown" === e.type;
                if (!("clientX" in e) && "changedTouches" in e && (e.clientX = e.changedTouches[0].clientX, e.clientY = e.changedTouches[0].clientY), E.forcescreen) {
                  var r = e;
                  (e = {
                    original: e.original ? e.original : e
                  }).clientX = r.screenX, e.clientY = r.screenY
                }
                if (E.rail.drag = {
                    x: e.clientX,
                    y: e.clientY,
                    sx: E.scroll.x,
                    sy: E.scroll.y,
                    st: E.getScrollTop(),
                    sl: E.getScrollLeft(),
                    pt: 2,
                    dl: !1,
                    tg: t
                  }, E.ispage || !k.directionlockdeadzone) E.rail.drag.dl = "f";
                else {
                  var i = {
                      w: c.width(),
                      h: c.height()
                    },
                    o = E.getContentSize(),
                    s = o.h - i.h,
                    l = o.w - i.w;
                  E.rail.scrollable && !E.railh.scrollable ? E.rail.drag.ck = s > 0 && "v" : !E.rail.scrollable && E.railh.scrollable ? E.rail.drag.ck = l > 0 && "h" : E.rail.drag.ck = !1
                }
                if (k.emulatetouch && E.isiframe && _.isie) {
                  var u = E.win.position();
                  E.rail.drag.x += u.left, E.rail.drag.y += u.top
                }
                if (E.hasmoving = !1, E.lastmouseup = !1, E.scrollmom.reset(e.clientX, e.clientY), t && n) {
                  if (!/INPUT|SELECT|BUTTON|TEXTAREA/i.test(t.nodeName)) return _.hasmousecapture && t.setCapture(), k.emulatetouch ? (t.onclick && !t._onclick && (t._onclick = t.onclick, t.onclick = function(e) {
                    if (E.hasmoving) return !1;
                    t._onclick.call(this, e)
                  }), E.cancelEvent(e)) : E.stopPropagation(e);
                  /SUBMIT|CANCEL|BUTTON/i.test(a(t).attr("type")) && (E.preventclick = {
                    tg: t,
                    click: !1
                  })
                }
              }
            }, E.ontouchend = function(e) {
              if (!E.rail.drag) return !0;
              if (2 == E.rail.drag.pt) {
                if (e.pointerType && ("mouse" === e.pointerType || e.pointerType === e.MSPOINTER_TYPE_MOUSE)) return !1;
                E.rail.drag = !1;
                var t = "mouseup" === e.type;
                if (E.hasmoving && (E.scrollmom.doMomentum(), E.lastmouseup = !0, E.hideCursor(), _.hasmousecapture && s.releaseCapture(), t)) return E.cancelEvent(e)
              } else if (1 == E.rail.drag.pt) return E.onmouseup(e)
            };
            var S = k.emulatetouch && E.isiframe && !_.hasmousecapture,
              C = .3 * k.directionlockdeadzone | 0;
            E.ontouchmove = function(e, t) {
              if (!E.rail.drag) return !0;
              if (e.targetTouches && k.preventmultitouchscrolling && e.targetTouches.length > 1) return !0;
              if (e.pointerType && ("mouse" === e.pointerType || e.pointerType === e.MSPOINTER_TYPE_MOUSE)) return !0;
              if (2 == E.rail.drag.pt) {
                var n, r;
                if ("changedTouches" in e && (e.clientX = e.changedTouches[0].clientX, e.clientY = e.changedTouches[0].clientY), r = n = 0, S && !t) {
                  var i = E.win.position();
                  r = -i.left, n = -i.top
                }
                var o = e.clientY + n,
                  a = o - E.rail.drag.y,
                  l = e.clientX + r,
                  c = l - E.rail.drag.x,
                  u = E.rail.drag.st - a;
                if (E.ishwscroll && k.bouncescroll) u < 0 ? u = Math.round(u / 2) : u > E.page.maxh && (u = E.page.maxh + Math.round((u - E.page.maxh) / 2));
                else if (u < 0 ? (u = 0, o = 0) : u > E.page.maxh && (u = E.page.maxh, o = 0), 0 === o && !E.hasmoving) return E.ispage || (E.rail.drag = !1), !0;
                var d = E.getScrollLeft();
                if (E.railh && E.railh.scrollable && (d = E.isrtlmode ? c - E.rail.drag.sl : E.rail.drag.sl - c, E.ishwscroll && k.bouncescroll ? d < 0 ? d = Math.round(d / 2) : d > E.page.maxw && (d = E.page.maxw + Math.round((d - E.page.maxw) / 2)) : (d < 0 && (d = 0, l = 0), d > E.page.maxw && (d = E.page.maxw, l = 0))), !E.hasmoving) {
                  if (E.rail.drag.y === e.clientY && E.rail.drag.x === e.clientX) return E.cancelEvent(e);
                  var p = Math.abs(a),
                    f = Math.abs(c),
                    h = k.directionlockdeadzone;
                  if (E.rail.drag.ck ? "v" == E.rail.drag.ck ? f > h && p <= C ? E.rail.drag = !1 : p > h && (E.rail.drag.dl = "v") : "h" == E.rail.drag.ck && (p > h && f <= C ? E.rail.drag = !1 : f > h && (E.rail.drag.dl = "h")) : p > h && f > h ? E.rail.drag.dl = "f" : p > h ? E.rail.drag.dl = f > C ? "f" : "v" : f > h && (E.rail.drag.dl = p > C ? "f" : "h"), !E.rail.drag.dl) return E.cancelEvent(e);
                  E.triggerScrollStart(e.clientX, e.clientY, 0, 0, 0), E.hasmoving = !0
                }
                return E.preventclick && !E.preventclick.click && (E.preventclick.click = E.preventclick.tg.onclick || !1, E.preventclick.tg.onclick = E.onpreventclick), E.rail.drag.dl && ("v" == E.rail.drag.dl ? d = E.rail.drag.sl : "h" == E.rail.drag.dl && (u = E.rail.drag.st)), E.synched("touchmove", (function() {
                  E.rail.drag && 2 == E.rail.drag.pt && (E.prepareTransition && E.resetTransition(), E.rail.scrollable && E.setScrollTop(u), E.scrollmom.update(l, o), E.railh && E.railh.scrollable ? (E.setScrollLeft(d), E.showCursor(u, d)) : E.showCursor(u), _.isie10 && s.selection.clear())
                })), E.cancelEvent(e)
              }
              return 1 == E.rail.drag.pt ? E.onmousemove(e) : void 0
            }, E.ontouchstartCursor = function(e, t) {
              if (!E.rail.drag || 3 == E.rail.drag.pt) {
                if (E.locked) return E.cancelEvent(e);
                E.cancelScroll(), E.rail.drag = {
                  x: e.touches[0].clientX,
                  y: e.touches[0].clientY,
                  sx: E.scroll.x,
                  sy: E.scroll.y,
                  pt: 3,
                  hr: !!t
                };
                var n = E.getTarget(e);
                return !E.ispage && _.hasmousecapture && n.setCapture(), E.isiframe && !_.hasmousecapture && (E.saved.csspointerevents = E.doc.css("pointer-events"), E.css(E.doc, {
                  "pointer-events": "none"
                })), E.cancelEvent(e)
              }
            }, E.ontouchendCursor = function(e) {
              if (E.rail.drag) {
                if (_.hasmousecapture && s.releaseCapture(), E.isiframe && !_.hasmousecapture && E.doc.css("pointer-events", E.saved.csspointerevents), 3 != E.rail.drag.pt) return;
                return E.rail.drag = !1, E.cancelEvent(e)
              }
            }, E.ontouchmoveCursor = function(e) {
              if (E.rail.drag) {
                if (3 != E.rail.drag.pt) return;
                if (E.cursorfreezed = !0, E.rail.drag.hr) {
                  E.scroll.x = E.rail.drag.sx + (e.touches[0].clientX - E.rail.drag.x), E.scroll.x < 0 && (E.scroll.x = 0);
                  var t = E.scrollvaluemaxw;
                  E.scroll.x > t && (E.scroll.x = t)
                } else {
                  E.scroll.y = E.rail.drag.sy + (e.touches[0].clientY - E.rail.drag.y), E.scroll.y < 0 && (E.scroll.y = 0);
                  var n = E.scrollvaluemax;
                  E.scroll.y > n && (E.scroll.y = n)
                }
                return E.synched("touchmove", (function() {
                  E.rail.drag && 3 == E.rail.drag.pt && (E.showCursor(), E.rail.drag.hr ? E.doScrollLeft(Math.round(E.scroll.x * E.scrollratio.x), k.cursordragspeed) : E.doScrollTop(Math.round(E.scroll.y * E.scrollratio.y), k.cursordragspeed))
                })), E.cancelEvent(e)
              }
            }
          }
          if (E.onmousedown = function(e, t) {
              if (!E.rail.drag || 1 == E.rail.drag.pt) {
                if (E.railslocked) return E.cancelEvent(e);
                E.cancelScroll(), E.rail.drag = {
                  x: e.clientX,
                  y: e.clientY,
                  sx: E.scroll.x,
                  sy: E.scroll.y,
                  pt: 1,
                  hr: t || !1
                };
                var n = E.getTarget(e);
                return _.hasmousecapture && n.setCapture(), E.isiframe && !_.hasmousecapture && (E.saved.csspointerevents = E.doc.css("pointer-events"), E.css(E.doc, {
                  "pointer-events": "none"
                })), E.hasmoving = !1, E.cancelEvent(e)
              }
            }, E.onmouseup = function(e) {
              if (E.rail.drag) return 1 != E.rail.drag.pt || (_.hasmousecapture && s.releaseCapture(), E.isiframe && !_.hasmousecapture && E.doc.css("pointer-events", E.saved.csspointerevents), E.rail.drag = !1, E.cursorfreezed = !1, E.hasmoving && E.triggerScrollEnd(), E.cancelEvent(e))
            }, E.onmousemove = function(e) {
              if (E.rail.drag) {
                if (1 !== E.rail.drag.pt) return;
                if (_.ischrome && 0 === e.which) return E.onmouseup(e);
                if (E.cursorfreezed = !0, E.hasmoving || E.triggerScrollStart(e.clientX, e.clientY, 0, 0, 0), E.hasmoving = !0, E.rail.drag.hr) {
                  E.scroll.x = E.rail.drag.sx + (e.clientX - E.rail.drag.x), E.scroll.x < 0 && (E.scroll.x = 0);
                  var t = E.scrollvaluemaxw;
                  E.scroll.x > t && (E.scroll.x = t)
                } else {
                  E.scroll.y = E.rail.drag.sy + (e.clientY - E.rail.drag.y), E.scroll.y < 0 && (E.scroll.y = 0);
                  var n = E.scrollvaluemax;
                  E.scroll.y > n && (E.scroll.y = n)
                }
                return E.synched("mousemove", (function() {
                  E.cursorfreezed && (E.showCursor(), E.rail.drag.hr ? E.scrollLeft(Math.round(E.scroll.x * E.scrollratio.x)) : E.scrollTop(Math.round(E.scroll.y * E.scrollratio.y)))
                })), E.cancelEvent(e)
              }
              E.checkarea = 0
            }, _.cantouch || k.emulatetouch) E.onpreventclick = function(e) {
            if (E.preventclick) return E.preventclick.tg.onclick = E.preventclick.click, E.preventclick = !1, E.cancelEvent(e)
          }, E.onclick = !_.isios && function(e) {
            return !E.lastmouseup || (E.lastmouseup = !1, E.cancelEvent(e))
          }, k.grabcursorenabled && _.cursorgrabvalue && (E.css(E.ispage ? E.doc : E.win, {
            cursor: _.cursorgrabvalue
          }), E.css(E.rail, {
            cursor: _.cursorgrabvalue
          }));
          else {
            var D = function(e) {
              if (E.selectiondrag) {
                if (e) {
                  var t = E.win.outerHeight(),
                    n = e.pageY - E.selectiondrag.top;
                  n > 0 && n < t && (n = 0), n >= t && (n -= t), E.selectiondrag.df = n
                }
                if (0 !== E.selectiondrag.df) {
                  var r = -2 * E.selectiondrag.df / 6 | 0;
                  E.doScrollBy(r), E.debounced("doselectionscroll", (function() {
                    D()
                  }), 50)
                }
              }
            };
            E.hasTextSelected = "getSelection" in s ? function() {
              return s.getSelection().rangeCount > 0
            } : "selection" in s ? function() {
              return "None" != s.selection.type
            } : function() {
              return !1
            }, E.onselectionstart = function(e) {
              E.ispage || (E.selectiondrag = E.win.offset())
            }, E.onselectionend = function(e) {
              E.selectiondrag = !1
            }, E.onselectiondrag = function(e) {
              E.selectiondrag && E.hasTextSelected() && E.debounced("selectionscroll", (function() {
                D(e)
              }), 250)
            }
          }
          if (_.hasw3ctouch ? (E.css(E.ispage ? a("html") : E.win, {
              "touch-action": "none"
            }), E.css(E.rail, {
              "touch-action": "none"
            }), E.css(E.cursor, {
              "touch-action": "none"
            }), E.bind(E.win, "pointerdown", E.ontouchstart), E.bind(s, "pointerup", E.ontouchend), E.delegate(s, "pointermove", E.ontouchmove)) : _.hasmstouch ? (E.css(E.ispage ? a("html") : E.win, {
              "-ms-touch-action": "none"
            }), E.css(E.rail, {
              "-ms-touch-action": "none"
            }), E.css(E.cursor, {
              "-ms-touch-action": "none"
            }), E.bind(E.win, "MSPointerDown", E.ontouchstart), E.bind(s, "MSPointerUp", E.ontouchend), E.delegate(s, "MSPointerMove", E.ontouchmove), E.bind(E.cursor, "MSGestureHold", (function(e) {
              e.preventDefault()
            })), E.bind(E.cursor, "contextmenu", (function(e) {
              e.preventDefault()
            }))) : _.cantouch && (E.bind(E.win, "touchstart", E.ontouchstart, !1, !0), E.bind(s, "touchend", E.ontouchend, !1, !0), E.bind(s, "touchcancel", E.ontouchend, !1, !0), E.delegate(s, "touchmove", E.ontouchmove, !1, !0)), k.emulatetouch && (E.bind(E.win, "mousedown", E.ontouchstart, !1, !0), E.bind(s, "mouseup", E.ontouchend, !1, !0), E.bind(s, "mousemove", E.ontouchmove, !1, !0)), (k.cursordragontouch || !_.cantouch && !k.emulatetouch) && (E.rail.css({
              cursor: "default"
            }), E.railh && E.railh.css({
              cursor: "default"
            }), E.jqbind(E.rail, "mouseenter", (function() {
              if (!E.ispage && !E.win.is(":visible")) return !1;
              E.canshowonmouseevent && E.showCursor(), E.rail.active = !0
            })), E.jqbind(E.rail, "mouseleave", (function() {
              E.rail.active = !1, E.rail.drag || E.hideCursor()
            })), k.sensitiverail && (E.bind(E.rail, "click", (function(e) {
              E.doRailClick(e, !1, !1)
            })), E.bind(E.rail, "dblclick", (function(e) {
              E.doRailClick(e, !0, !1)
            })), E.bind(E.cursor, "click", (function(e) {
              E.cancelEvent(e)
            })), E.bind(E.cursor, "dblclick", (function(e) {
              E.cancelEvent(e)
            }))), E.railh && (E.jqbind(E.railh, "mouseenter", (function() {
              if (!E.ispage && !E.win.is(":visible")) return !1;
              E.canshowonmouseevent && E.showCursor(), E.rail.active = !0
            })), E.jqbind(E.railh, "mouseleave", (function() {
              E.rail.active = !1, E.rail.drag || E.hideCursor()
            })), k.sensitiverail && (E.bind(E.railh, "click", (function(e) {
              E.doRailClick(e, !1, !0)
            })), E.bind(E.railh, "dblclick", (function(e) {
              E.doRailClick(e, !0, !0)
            })), E.bind(E.cursorh, "click", (function(e) {
              E.cancelEvent(e)
            })), E.bind(E.cursorh, "dblclick", (function(e) {
              E.cancelEvent(e)
            }))))), k.cursordragontouch && (this.istouchcapable || _.cantouch) && (E.bind(E.cursor, "touchstart", E.ontouchstartCursor), E.bind(E.cursor, "touchmove", E.ontouchmoveCursor), E.bind(E.cursor, "touchend", E.ontouchendCursor), E.cursorh && E.bind(E.cursorh, "touchstart", (function(e) {
              E.ontouchstartCursor(e, !0)
            })), E.cursorh && E.bind(E.cursorh, "touchmove", E.ontouchmoveCursor), E.cursorh && E.bind(E.cursorh, "touchend", E.ontouchendCursor)), k.emulatetouch || _.isandroid || _.isios ? (E.bind(_.hasmousecapture ? E.win : s, "mouseup", E.ontouchend), E.onclick && E.bind(s, "click", E.onclick), k.cursordragontouch ? (E.bind(E.cursor, "mousedown", E.onmousedown), E.bind(E.cursor, "mouseup", E.onmouseup), E.cursorh && E.bind(E.cursorh, "mousedown", (function(e) {
              E.onmousedown(e, !0)
            })), E.cursorh && E.bind(E.cursorh, "mouseup", E.onmouseup)) : (E.bind(E.rail, "mousedown", (function(e) {
              e.preventDefault()
            })), E.railh && E.bind(E.railh, "mousedown", (function(e) {
              e.preventDefault()
            })))) : (E.bind(_.hasmousecapture ? E.win : s, "mouseup", E.onmouseup), E.bind(s, "mousemove", E.onmousemove), E.onclick && E.bind(s, "click", E.onclick), E.bind(E.cursor, "mousedown", E.onmousedown), E.bind(E.cursor, "mouseup", E.onmouseup), E.railh && (E.bind(E.cursorh, "mousedown", (function(e) {
              E.onmousedown(e, !0)
            })), E.bind(E.cursorh, "mouseup", E.onmouseup)), !E.ispage && k.enablescrollonselection && (E.bind(E.win[0], "mousedown", E.onselectionstart), E.bind(s, "mouseup", E.onselectionend), E.bind(E.cursor, "mouseup", E.onselectionend), E.cursorh && E.bind(E.cursorh, "mouseup", E.onselectionend), E.bind(s, "mousemove", E.onselectiondrag)), E.zoom && (E.jqbind(E.zoom, "mouseenter", (function() {
              E.canshowonmouseevent && E.showCursor(), E.rail.active = !0
            })), E.jqbind(E.zoom, "mouseleave", (function() {
              E.rail.active = !1, E.rail.drag || E.hideCursor()
            })))), k.enablemousewheel && (E.isiframe || E.mousewheel(_.isie && E.ispage ? s : E.win, E.onmousewheel), E.mousewheel(E.rail, E.onmousewheel), E.railh && E.mousewheel(E.railh, E.onmousewheelhr)), E.ispage || _.cantouch || /HTML|^BODY/.test(E.win[0].nodeName) || (E.win.attr("tabindex") || E.win.attr({
              tabindex: ++r
            }), E.bind(E.win, "focus", (function(e) {
              t = E.getTarget(e).id || E.getTarget(e) || !1, E.hasfocus = !0, E.canshowonmouseevent && E.noticeCursor()
            })), E.bind(E.win, "blur", (function(e) {
              t = !1, E.hasfocus = !1
            })), E.bind(E.win, "mouseenter", (function(e) {
              n = E.getTarget(e).id || E.getTarget(e) || !1, E.hasmousefocus = !0, E.canshowonmouseevent && E.noticeCursor()
            })), E.bind(E.win, "mouseleave", (function(e) {
              n = !1, E.hasmousefocus = !1, E.rail.drag || E.hideCursor()
            }))), E.onkeypress = function(e) {
              if (E.railslocked && 0 === E.page.maxh) return !0;
              e = e || l.event;
              var r = E.getTarget(e);
              if (r && /INPUT|TEXTAREA|SELECT|OPTION/.test(r.nodeName) && (!r.getAttribute("type") && !r.type || !/submit|button|cancel/i.tp)) return !0;
              if (a(r).attr("contenteditable")) return !0;
              if (E.hasfocus || E.hasmousefocus && !t || E.ispage && !t && !n) {
                var i = e.keyCode;
                if (E.railslocked && 27 != i) return E.cancelEvent(e);
                var o = e.ctrlKey || !1,
                  s = e.shiftKey || !1,
                  c = !1;
                switch (i) {
                  case 38:
                  case 63233:
                    E.doScrollBy(72), c = !0;
                    break;
                  case 40:
                  case 63235:
                    E.doScrollBy(-72), c = !0;
                    break;
                  case 37:
                  case 63232:
                    E.railh && (o ? E.doScrollLeft(0) : E.doScrollLeftBy(72), c = !0);
                    break;
                  case 39:
                  case 63234:
                    E.railh && (o ? E.doScrollLeft(E.page.maxw) : E.doScrollLeftBy(-72), c = !0);
                    break;
                  case 33:
                  case 63276:
                    E.doScrollBy(E.view.h), c = !0;
                    break;
                  case 34:
                  case 63277:
                    E.doScrollBy(-E.view.h), c = !0;
                    break;
                  case 36:
                  case 63273:
                    E.railh && o ? E.doScrollPos(0, 0) : E.doScrollTo(0), c = !0;
                    break;
                  case 35:
                  case 63275:
                    E.railh && o ? E.doScrollPos(E.page.maxw, E.page.maxh) : E.doScrollTo(E.page.maxh), c = !0;
                    break;
                  case 32:
                    k.spacebarenabled && (s ? E.doScrollBy(E.view.h) : E.doScrollBy(-E.view.h), c = !0);
                    break;
                  case 27:
                    E.zoomactive && (E.doZoom(), c = !0)
                }
                if (c) return E.cancelEvent(e)
              }
            }, k.enablekeyboard && E.bind(s, _.isopera && !_.isopera12 ? "keypress" : "keydown", E.onkeypress), E.bind(s, "keydown", (function(e) {
              e.ctrlKey && (E.wheelprevented = !0)
            })), E.bind(s, "keyup", (function(e) {
              e.ctrlKey || (E.wheelprevented = !1)
            })), E.bind(l, "blur", (function(e) {
              E.wheelprevented = !1
            })), E.bind(l, "resize", E.onscreenresize), E.bind(l, "orientationchange", E.onscreenresize), E.bind(l, "load", E.lazyResize), _.ischrome && !E.ispage && !E.haswrapper) {
            var O = E.win.attr("style"),
              A = parseFloat(E.win.css("width")) + 1;
            E.win.css("width", A), E.synched("chromefix", (function() {
              E.win.attr("style", O)
            }))
          }
          if (E.onAttributeChange = function(e) {
              E.lazyResize(E.isieold ? 250 : 30)
            }, k.enableobserver && (E.isie11 || !1 === h || (E.observerbody = new h((function(e) {
              if (e.forEach((function(e) {
                  if ("attributes" == e.type) return T.hasClass("modal-open") && T.hasClass("modal-dialog") && !a.contains(a(".modal-dialog")[0], E.doc[0]) ? E.hide() : E.show()
                })), E.me.clientWidth != E.page.width || E.me.clientHeight != E.page.height) return E.lazyResize(30)
            })), E.observerbody.observe(s.body, {
              childList: !0,
              subtree: !0,
              characterData: !1,
              attributes: !0,
              attributeFilter: ["class"]
            })), !E.ispage && !E.haswrapper)) {
            var M = E.win[0];
            !1 !== h ? (E.observer = new h((function(e) {
              e.forEach(E.onAttributeChange)
            })), E.observer.observe(M, {
              childList: !0,
              characterData: !1,
              attributes: !0,
              subtree: !1
            }), E.observerremover = new h((function(e) {
              e.forEach((function(e) {
                if (e.removedNodes.length > 0)
                  for (var t in e.removedNodes)
                    if (E && e.removedNodes[t] === M) return E.remove()
              }))
            })), E.observerremover.observe(M.parentNode, {
              childList: !0,
              characterData: !1,
              attributes: !1,
              subtree: !1
            })) : (E.bind(M, _.isie && !_.isie9 ? "propertychange" : "DOMAttrModified", E.onAttributeChange), _.isie9 && M.attachEvent("onpropertychange", E.onAttributeChange), E.bind(M, "DOMNodeRemoved", (function(e) {
              e.target === M && E.remove()
            })))
          }!E.ispage && k.boxzoom && E.bind(l, "resize", E.resizeZoom), E.istextarea && (E.bind(E.win, "keydown", E.lazyResize), E.bind(E.win, "mouseup", E.lazyResize)), E.lazyResize(30)
        }
        if ("IFRAME" == this.doc[0].nodeName) {
          var L = function() {
            var t;
            E.iframexd = !1;
            try {
              (t = "contentDocument" in this ? this.contentDocument : this.contentWindow._doc).domain
            } catch (e) {
              E.iframexd = !0, t = !1
            }
            if (E.iframexd) return "console" in l && console.log("NiceScroll error: policy restriced iframe"), !0;
            if (E.forcescreen = !0, E.isiframe && (E.iframe = {
                doc: a(t),
                html: E.doc.contents().find("html")[0],
                body: E.doc.contents().find("body")[0]
              }, E.getContentSize = function() {
                return {
                  w: Math.max(E.iframe.html.scrollWidth, E.iframe.body.scrollWidth),
                  h: Math.max(E.iframe.html.scrollHeight, E.iframe.body.scrollHeight)
                }
              }, E.docscroll = a(E.iframe.body)), !_.isios && k.iframeautoresize && !E.isiframe) {
              E.win.scrollTop(0), E.doc.height("");
              var n = Math.max(t.getElementsByTagName("html")[0].scrollHeight, t.body.scrollHeight);
              E.doc.height(n)
            }
            E.lazyResize(30), E.css(a(E.iframe.body), e), _.isios && E.haswrapper && E.css(a(t.body), {
              "-webkit-transform": "translate3d(0,0,0)"
            }), "contentWindow" in this ? E.bind(this.contentWindow, "scroll", E.onscroll) : E.bind(t, "scroll", E.onscroll), k.enablemousewheel && E.mousewheel(t, E.onmousewheel), k.enablekeyboard && E.bind(t, _.isopera ? "keypress" : "keydown", E.onkeypress), _.cantouch ? (E.bind(t, "touchstart", E.ontouchstart), E.bind(t, "touchmove", E.ontouchmove)) : k.emulatetouch && (E.bind(t, "mousedown", E.ontouchstart), E.bind(t, "mousemove", (function(e) {
              return E.ontouchmove(e, !0)
            })), k.grabcursorenabled && _.cursorgrabvalue && E.css(a(t.body), {
              cursor: _.cursorgrabvalue
            })), E.bind(t, "mouseup", E.ontouchend), E.zoom && (k.dblclickzoom && E.bind(t, "dblclick", E.doZoom), E.ongesturezoom && E.bind(t, "gestureend", E.ongesturezoom))
          };
          this.doc[0].readyState && "complete" === this.doc[0].readyState && setTimeout((function() {
            L.call(E.doc[0], !1)
          }), 500), E.bind(this.doc, "load", L)
        }
      }, this.showCursor = function(e, t) {
        if (E.cursortimeout && (clearTimeout(E.cursortimeout), E.cursortimeout = 0), E.rail) {
          if (E.autohidedom && (E.autohidedom.stop().css({
              opacity: k.cursoropacitymax
            }), E.cursoractive = !0), E.rail.drag && 1 == E.rail.drag.pt || (void 0 !== e && !1 !== e && (E.scroll.y = e / E.scrollratio.y | 0), void 0 !== t && (E.scroll.x = t / E.scrollratio.x | 0)), E.cursor.css({
              height: E.cursorheight,
              top: E.scroll.y
            }), E.cursorh) {
            var n = E.hasreversehr ? E.scrollvaluemaxw - E.scroll.x : E.scroll.x;
            E.cursorh.css({
              width: E.cursorwidth,
              left: !E.rail.align && E.rail.visibility ? n + E.rail.width : n
            }), E.cursoractive = !0
          }
          E.zoom && E.zoom.stop().css({
            opacity: k.cursoropacitymax
          })
        }
      }, this.hideCursor = function(e) {
        E.cursortimeout || E.rail && E.autohidedom && (E.hasmousefocus && "leave" === k.autohidemode || (E.cursortimeout = setTimeout((function() {
          E.rail.active && E.showonmouseevent || (E.autohidedom.stop().animate({
            opacity: k.cursoropacitymin
          }), E.zoom && E.zoom.stop().animate({
            opacity: k.cursoropacitymin
          }), E.cursoractive = !1), E.cursortimeout = 0
        }), e || k.hidecursordelay)))
      }, this.noticeCursor = function(e, t, n) {
        E.showCursor(t, n), E.rail.active || E.hideCursor(e)
      }, this.getContentSize = E.ispage ? function() {
        return {
          w: Math.max(s.body.scrollWidth, s.documentElement.scrollWidth),
          h: Math.max(s.body.scrollHeight, s.documentElement.scrollHeight)
        }
      } : E.haswrapper ? function() {
        return {
          w: E.doc[0].offsetWidth,
          h: E.doc[0].offsetHeight
        }
      } : function() {
        return {
          w: E.docscroll[0].scrollWidth,
          h: E.docscroll[0].scrollHeight
        }
      }, this.onResize = function(e, t) {
        if (!E || !E.win) return !1;
        var n = E.page.maxh,
          r = E.page.maxw,
          i = E.view.h,
          o = E.view.w;
        if (E.view = {
            w: E.ispage ? E.win.width() : E.win[0].clientWidth,
            h: E.ispage ? E.win.height() : E.win[0].clientHeight
          }, E.page = t || E.getContentSize(), E.page.maxh = Math.max(0, E.page.h - E.view.h), E.page.maxw = Math.max(0, E.page.w - E.view.w), E.page.maxh == n && E.page.maxw == r && E.view.w == o && E.view.h == i) {
          if (E.ispage) return E;
          var a = E.win.offset();
          if (E.lastposition) {
            var s = E.lastposition;
            if (s.top == a.top && s.left == a.left) return E
          }
          E.lastposition = a
        }
        return 0 === E.page.maxh ? (E.hideRail(), E.scrollvaluemax = 0, E.scroll.y = 0, E.scrollratio.y = 0, E.cursorheight = 0, E.setScrollTop(0), E.rail && (E.rail.scrollable = !1)) : (E.page.maxh -= k.railpadding.top + k.railpadding.bottom, E.rail.scrollable = !0), 0 === E.page.maxw ? (E.hideRailHr(), E.scrollvaluemaxw = 0, E.scroll.x = 0, E.scrollratio.x = 0, E.cursorwidth = 0, E.setScrollLeft(0), E.railh && (E.railh.scrollable = !1)) : (E.page.maxw -= k.railpadding.left + k.railpadding.right, E.railh && (E.railh.scrollable = k.horizrailenabled)), E.railslocked = E.locked || 0 === E.page.maxh && 0 === E.page.maxw, E.railslocked ? (E.ispage || E.updateScrollBar(E.view), !1) : (E.hidden || (E.rail.visibility || E.showRail(), E.railh && !E.railh.visibility && E.showRailHr()), E.istextarea && E.win.css("resize") && "none" != E.win.css("resize") && (E.view.h -= 20), E.cursorheight = Math.min(E.view.h, Math.round(E.view.h * (E.view.h / E.page.h))), E.cursorheight = k.cursorfixedheight ? k.cursorfixedheight : Math.max(k.cursorminheight, E.cursorheight), E.cursorwidth = Math.min(E.view.w, Math.round(E.view.w * (E.view.w / E.page.w))), E.cursorwidth = k.cursorfixedheight ? k.cursorfixedheight : Math.max(k.cursorminheight, E.cursorwidth), E.scrollvaluemax = E.view.h - E.cursorheight - (k.railpadding.top + k.railpadding.bottom), E.hasborderbox || (E.scrollvaluemax -= E.cursor[0].offsetHeight - E.cursor[0].clientHeight), E.railh && (E.railh.width = E.page.maxh > 0 ? E.view.w - E.rail.width : E.view.w, E.scrollvaluemaxw = E.railh.width - E.cursorwidth - (k.railpadding.left + k.railpadding.right)), E.ispage || E.updateScrollBar(E.view), E.scrollratio = {
          x: E.page.maxw / E.scrollvaluemaxw,
          y: E.page.maxh / E.scrollvaluemax
        }, E.getScrollTop() > E.page.maxh ? E.doScrollTop(E.page.maxh) : (E.scroll.y = E.getScrollTop() / E.scrollratio.y | 0, E.scroll.x = E.getScrollLeft() / E.scrollratio.x | 0, E.cursoractive && E.noticeCursor()), E.scroll.y && 0 === E.getScrollTop() && E.doScrollTo(E.scroll.y * E.scrollratio.y | 0), E)
      }, this.resize = E.onResize;
      var P = 0;
      this.onscreenresize = function(e) {
        clearTimeout(P);
        var t = !E.ispage && !E.haswrapper;
        t && E.hideRails(), P = setTimeout((function() {
          E && (t && E.showRails(), E.resize()), P = 0
        }), 120)
      }, this.lazyResize = function(e) {
        return clearTimeout(P), e = isNaN(e) ? 240 : e, P = setTimeout((function() {
          E && E.resize(), P = 0
        }), e), E
      }, this.jqbind = function(e, t, n) {
        E.events.push({
          e: e,
          n: t,
          f: n,
          q: !0
        }), a(e).on(t, n)
      }, this.mousewheel = function(e, t, n) {
        var r = "jquery" in e ? e[0] : e;
        if ("onwheel" in s.createElement("div")) E._bind(r, "wheel", t, n || !1);
        else {
          var i = void 0 !== s.onmousewheel ? "mousewheel" : "DOMMouseScroll";
          x(r, i, t, n || !1), "DOMMouseScroll" == i && x(r, "MozMousePixelScroll", t, n || !1)
        }
      };
      var j = !1;
      if (_.haseventlistener) {
        try {
          var N = Object.defineProperty({}, "passive", {
            get: function() {
              j = !0
            }
          });
          l.addEventListener("test", null, N)
        } catch (e) {}
        this.stopPropagation = function(e) {
          return !!e && ((e = e.original ? e.original : e).stopPropagation(), !1)
        }, this.cancelEvent = function(e) {
          return e.cancelable && e.preventDefault(), e.stopImmediatePropagation(), e.preventManipulation && e.preventManipulation(), !1
        }
      } else Event.prototype.preventDefault = function() {
        this.returnValue = !1
      }, Event.prototype.stopPropagation = function() {
        this.cancelBubble = !0
      }, l.constructor.prototype.addEventListener = s.constructor.prototype.addEventListener = Element.prototype.addEventListener = function(e, t, n) {
        this.attachEvent("on" + e, t)
      }, l.constructor.prototype.removeEventListener = s.constructor.prototype.removeEventListener = Element.prototype.removeEventListener = function(e, t, n) {
        this.detachEvent("on" + e, t)
      }, this.cancelEvent = function(e) {
        return (e = e || l.event) && (e.cancelBubble = !0, e.cancel = !0, e.returnValue = !1), !1
      }, this.stopPropagation = function(e) {
        return (e = e || l.event) && (e.cancelBubble = !0), !1
      };
      this.delegate = function(e, t, n, r, i) {
        var o = u[t] || !1;
        o || (o = {
          a: [],
          l: [],
          f: function(e) {
            for (var t = o.l, n = !1, r = t.length - 1; r >= 0; r--)
              if (!1 === (n = t[r].call(e.target, e))) return !1;
            return n
          }
        }, E.bind(e, t, o.f, r, i), u[t] = o), E.ispage ? (o.a = [E.id].concat(o.a), o.l = [n].concat(o.l)) : (o.a.push(E.id), o.l.push(n))
      }, this.undelegate = function(e, t, n, r, i) {
        var o = u[t] || !1;
        if (o && o.l)
          for (var a = 0, s = o.l.length; a < s; a++) o.a[a] === E.id && (o.a.splice(a), o.l.splice(a), 0 === o.a.length && (E._unbind(e, t, o.l.f), u[t] = null))
      }, this.bind = function(e, t, n, r, i) {
        var o = "jquery" in e ? e[0] : e;
        E._bind(o, t, n, r || !1, i || !1)
      }, this._bind = function(e, t, n, r, i) {
        E.events.push({
          e: e,
          n: t,
          f: n,
          b: r,
          q: !1
        }), j && i ? e.addEventListener(t, n, {
          passive: !1,
          capture: r
        }) : e.addEventListener(t, n, r || !1)
      }, this._unbind = function(e, t, n, r) {
        u[t] ? E.undelegate(e, t, n, r) : e.removeEventListener(t, n, r)
      }, this.unbindAll = function() {
        for (var e = 0; e < E.events.length; e++) {
          var t = E.events[e];
          t.q ? t.e.unbind(t.n, t.f) : E._unbind(t.e, t.n, t.f, t.b)
        }
      }, this.showRails = function() {
        return E.showRail().showRailHr()
      }, this.showRail = function() {
        return 0 === E.page.maxh || !E.ispage && "none" == E.win.css("display") || (E.rail.visibility = !0, E.rail.css("display", "block")), E
      }, this.showRailHr = function() {
        return E.railh && (0 === E.page.maxw || !E.ispage && "none" == E.win.css("display") || (E.railh.visibility = !0, E.railh.css("display", "block"))), E
      }, this.hideRails = function() {
        return E.hideRail().hideRailHr()
      }, this.hideRail = function() {
        return E.rail.visibility = !1, E.rail.css("display", "none"), E
      }, this.hideRailHr = function() {
        return E.railh && (E.railh.visibility = !1, E.railh.css("display", "none")), E
      }, this.show = function() {
        return E.hidden = !1, E.railslocked = !1, E.showRails()
      }, this.hide = function() {
        return E.hidden = !0, E.railslocked = !0, E.hideRails()
      }, this.toggle = function() {
        return E.hidden ? E.show() : E.hide()
      }, this.remove = function() {
        for (var e in E.stop(), E.cursortimeout && clearTimeout(E.cursortimeout), E.delaylist) E.delaylist[e] && p(E.delaylist[e].h);
        E.doZoomOut(), E.unbindAll(), _.isie9 && E.win[0].detachEvent("onpropertychange", E.onAttributeChange), !1 !== E.observer && E.observer.disconnect(), !1 !== E.observerremover && E.observerremover.disconnect(), !1 !== E.observerbody && E.observerbody.disconnect(), E.events = null, E.cursor && E.cursor.remove(), E.cursorh && E.cursorh.remove(), E.rail && E.rail.remove(), E.railh && E.railh.remove(), E.zoom && E.zoom.remove();
        for (var t = 0; t < E.saved.css.length; t++) {
          var n = E.saved.css[t];
          n[0].css(n[1], void 0 === n[2] ? "" : n[2])
        }
        E.saved = !1, E.me.data("__nicescroll", "");
        var r = a.nicescroll;
        for (var i in r.each((function(e) {
            if (this && this.id === E.id) {
              delete r[e];
              for (var t = ++e; t < r.length; t++, e++) r[e] = r[t];
              --r.length && delete r[r.length]
            }
          })), E) E[i] = null, delete E[i];
        E = null
      }, this.scrollstart = function(e) {
        return this.onscrollstart = e, E
      }, this.scrollend = function(e) {
        return this.onscrollend = e, E
      }, this.scrollcancel = function(e) {
        return this.onscrollcancel = e, E
      }, this.zoomin = function(e) {
        return this.onzoomin = e, E
      }, this.zoomout = function(e) {
        return this.onzoomout = e, E
      }, this.isScrollable = function(e) {
        var t = e.target ? e.target : e;
        if ("OPTION" == t.nodeName) return !0;
        for (; t && 1 == t.nodeType && t !== this.me[0] && !/^BODY|HTML/.test(t.nodeName);) {
          var n = a(t),
            r = n.css("overflowY") || n.css("overflowX") || n.css("overflow") || "";
          if (/scroll|auto/.test(r)) return t.clientHeight != t.scrollHeight;
          t = !!t.parentNode && t.parentNode
        }
        return !1
      }, this.getViewport = function(e) {
        for (var t = !(!e || !e.parentNode) && e.parentNode; t && 1 == t.nodeType && !/^BODY|HTML/.test(t.nodeName);) {
          var n = a(t);
          if (/fixed|absolute/.test(n.css("position"))) return n;
          var r = n.css("overflowY") || n.css("overflowX") || n.css("overflow") || "";
          if (/scroll|auto/.test(r) && t.clientHeight != t.scrollHeight) return n;
          if (n.getNiceScroll().length > 0) return n;
          t = !!t.parentNode && t.parentNode
        }
        return !1
      }, this.triggerScrollStart = function(e, t, n, r, i) {
        if (E.onscrollstart) {
          var o = {
            type: "scrollstart",
            current: {
              x: e,
              y: t
            },
            request: {
              x: n,
              y: r
            },
            end: {
              x: E.newscrollx,
              y: E.newscrolly
            },
            speed: i
          };
          E.onscrollstart.call(E, o)
        }
      }, this.triggerScrollEnd = function() {
        if (E.onscrollend) {
          var e = E.getScrollLeft(),
            t = E.getScrollTop(),
            n = {
              type: "scrollend",
              current: {
                x: e,
                y: t
              },
              end: {
                x: e,
                y: t
              }
            };
          E.onscrollend.call(E, n)
        }
      };
      var z = 0,
        R = 0,
        $ = 0,
        H = 1,
        F = !1;
      if (this.onmousewheel = function(e) {
          if (E.wheelprevented || E.locked) return !1;
          if (E.railslocked) return E.debounced("checkunlock", E.resize, 250), !1;
          if (E.rail.drag) return E.cancelEvent(e);
          if ("auto" === k.oneaxismousemode && 0 !== e.deltaX && (k.oneaxismousemode = !1), k.oneaxismousemode && 0 === e.deltaX && !E.rail.scrollable) return !E.railh || !E.railh.scrollable || E.onmousewheelhr(e);
          var t = m(),
            n = !1;
          if (k.preservenativescrolling && E.checkarea + 600 < t && (E.nativescrollingarea = E.isScrollable(e), n = !0), E.checkarea = t, E.nativescrollingarea) return !0;
          var r = C(e, !1, n);
          return r && (E.checkarea = 0), r
        }, this.onmousewheelhr = function(e) {
          if (!E.wheelprevented) {
            if (E.railslocked || !E.railh.scrollable) return !0;
            if (E.rail.drag) return E.cancelEvent(e);
            var t = m(),
              n = !1;
            return k.preservenativescrolling && E.checkarea + 600 < t && (E.nativescrollingarea = E.isScrollable(e), n = !0), E.checkarea = t, !!E.nativescrollingarea || (E.railslocked ? E.cancelEvent(e) : C(e, !0, n))
          }
        }, this.stop = function() {
          return E.cancelScroll(), E.scrollmon && E.scrollmon.stop(), E.cursorfreezed = !1, E.scroll.y = Math.round(E.getScrollTop() * (1 / E.scrollratio.y)), E.noticeCursor(), E
        }, this.getTransitionSpeed = function(e) {
          return 80 + e / 72 * k.scrollspeed | 0
        }, k.smoothscroll)
        if (E.ishwscroll && _.hastransition && k.usetransition && k.smoothscroll) {
          var B = "";
          this.resetTransition = function() {
            B = "", E.doc.css(_.prefixstyle + "transition-duration", "0ms")
          }, this.prepareTransition = function(e, t) {
            var n = t ? e : E.getTransitionSpeed(e),
              r = n + "ms";
            return B !== r && (B = r, E.doc.css(_.prefixstyle + "transition-duration", r)), n
          }, this.doScrollLeft = function(e, t) {
            var n = E.scrollrunning ? E.newscrolly : E.getScrollTop();
            E.doScrollPos(e, n, t)
          }, this.doScrollTop = function(e, t) {
            var n = E.scrollrunning ? E.newscrollx : E.getScrollLeft();
            E.doScrollPos(n, e, t)
          }, this.cursorupdate = {
            running: !1,
            start: function() {
              var e = this;
              if (!e.running) {
                e.running = !0;
                var t = function() {
                  e.running && d(t), E.showCursor(E.getScrollTop(), E.getScrollLeft()), E.notifyScrollEvent(E.win[0])
                };
                d(t)
              }
            },
            stop: function() {
              this.running = !1
            }
          }, this.doScrollPos = function(e, t, n) {
            var r = E.getScrollTop(),
              i = E.getScrollLeft();
            if (((E.newscrolly - r) * (t - r) < 0 || (E.newscrollx - i) * (e - i) < 0) && E.cancelScroll(), k.bouncescroll ? (t < 0 ? t = t / 2 | 0 : t > E.page.maxh && (t = E.page.maxh + (t - E.page.maxh) / 2 | 0), e < 0 ? e = e / 2 | 0 : e > E.page.maxw && (e = E.page.maxw + (e - E.page.maxw) / 2 | 0)) : (t < 0 ? t = 0 : t > E.page.maxh && (t = E.page.maxh), e < 0 ? e = 0 : e > E.page.maxw && (e = E.page.maxw)), E.scrollrunning && e == E.newscrollx && t == E.newscrolly) return !1;
            E.newscrolly = t, E.newscrollx = e;
            var o = E.getScrollTop(),
              a = E.getScrollLeft(),
              s = {};
            s.x = e - a, s.y = t - o;
            var l = 0 | Math.sqrt(s.x * s.x + s.y * s.y),
              c = E.prepareTransition(l);
            E.scrollrunning || (E.scrollrunning = !0, E.triggerScrollStart(a, o, e, t, c), E.cursorupdate.start()), E.scrollendtrapped = !0, _.transitionend || (E.scrollendtrapped && clearTimeout(E.scrollendtrapped), E.scrollendtrapped = setTimeout(E.onScrollTransitionEnd, c)), E.setScrollTop(E.newscrolly), E.setScrollLeft(E.newscrollx)
          }, this.cancelScroll = function() {
            if (!E.scrollendtrapped) return !0;
            var e = E.getScrollTop(),
              t = E.getScrollLeft();
            return E.scrollrunning = !1, _.transitionend || clearTimeout(_.transitionend), E.scrollendtrapped = !1, E.resetTransition(), E.setScrollTop(e), E.railh && E.setScrollLeft(t), E.timerscroll && E.timerscroll.tm && clearInterval(E.timerscroll.tm), E.timerscroll = !1, E.cursorfreezed = !1, E.cursorupdate.stop(), E.showCursor(e, t), E
          }, this.onScrollTransitionEnd = function() {
            if (E.scrollendtrapped) {
              var e = E.getScrollTop(),
                t = E.getScrollLeft();
              if (e < 0 ? e = 0 : e > E.page.maxh && (e = E.page.maxh), t < 0 ? t = 0 : t > E.page.maxw && (t = E.page.maxw), e != E.newscrolly || t != E.newscrollx) return E.doScrollPos(t, e, k.snapbackspeed);
              E.scrollrunning && E.triggerScrollEnd(), E.scrollrunning = !1, E.scrollendtrapped = !1, E.resetTransition(), E.timerscroll = !1, E.setScrollTop(e), E.railh && E.setScrollLeft(t), E.cursorupdate.stop(), E.noticeCursor(!1, e, t), E.cursorfreezed = !1
            }
          }
        } else this.doScrollLeft = function(e, t) {
          var n = E.scrollrunning ? E.newscrolly : E.getScrollTop();
          E.doScrollPos(e, n, t)
        }, this.doScrollTop = function(e, t) {
          var n = E.scrollrunning ? E.newscrollx : E.getScrollLeft();
          E.doScrollPos(n, e, t)
        }, this.doScrollPos = function(e, t, n) {
          var r = E.getScrollTop(),
            i = E.getScrollLeft();
          ((E.newscrolly - r) * (t - r) < 0 || (E.newscrollx - i) * (e - i) < 0) && E.cancelScroll();
          var o = !1;
          if (E.bouncescroll && E.rail.visibility || (t < 0 ? (t = 0, o = !0) : t > E.page.maxh && (t = E.page.maxh, o = !0)), E.bouncescroll && E.railh.visibility || (e < 0 ? (e = 0, o = !0) : e > E.page.maxw && (e = E.page.maxw, o = !0)), E.scrollrunning && E.newscrolly === t && E.newscrollx === e) return !0;
          E.newscrolly = t, E.newscrollx = e, E.dst = {}, E.dst.x = e - i, E.dst.y = t - r, E.dst.px = i, E.dst.py = r;
          var a = 0 | Math.sqrt(E.dst.x * E.dst.x + E.dst.y * E.dst.y),
            s = E.getTransitionSpeed(a);
          E.bzscroll = {};
          var l = o ? 1 : .58;
          E.bzscroll.x = new M(i, E.newscrollx, s, 0, 0, l, 1), E.bzscroll.y = new M(r, E.newscrolly, s, 0, 0, l, 1), m();
          var c = function() {
            if (E.scrollrunning) {
              var e = E.bzscroll.y.getPos();
              E.setScrollLeft(E.bzscroll.x.getNow()), E.setScrollTop(E.bzscroll.y.getNow()), e <= 1 ? E.timer = d(c) : (E.scrollrunning = !1, E.timer = 0, E.triggerScrollEnd())
            }
          };
          E.scrollrunning || (E.triggerScrollStart(i, r, e, t, s), E.scrollrunning = !0, E.timer = d(c))
        }, this.cancelScroll = function() {
          return E.timer && p(E.timer), E.timer = 0, E.bzscroll = !1, E.scrollrunning = !1, E
        };
      else this.doScrollLeft = function(e, t) {
        var n = E.getScrollTop();
        E.doScrollPos(e, n, t)
      }, this.doScrollTop = function(e, t) {
        var n = E.getScrollLeft();
        E.doScrollPos(n, e, t)
      }, this.doScrollPos = function(e, t, n) {
        var r = e > E.page.maxw ? E.page.maxw : e;
        r < 0 && (r = 0);
        var i = t > E.page.maxh ? E.page.maxh : t;
        i < 0 && (i = 0), E.synched("scroll", (function() {
          E.setScrollTop(i), E.setScrollLeft(r)
        }))
      }, this.cancelScroll = function() {};
      this.doScrollBy = function(e, t) {
        S(0, e)
      }, this.doScrollLeftBy = function(e, t) {
        S(e, 0)
      }, this.doScrollTo = function(e, t) {
        var n = t ? Math.round(e * E.scrollratio.y) : e;
        n < 0 ? n = 0 : n > E.page.maxh && (n = E.page.maxh), E.cursorfreezed = !1, E.doScrollTop(e)
      }, this.checkContentSize = function() {
        var e = E.getContentSize();
        e.h == E.page.h && e.w == E.page.w || E.resize(!1, e)
      }, E.onscroll = function(e) {
        E.rail.drag || E.cursorfreezed || E.synched("scroll", (function() {
          E.scroll.y = Math.round(E.getScrollTop() / E.scrollratio.y), E.railh && (E.scroll.x = Math.round(E.getScrollLeft() / E.scrollratio.x)), E.noticeCursor()
        }))
      }, E.bind(E.docscroll, "scroll", E.onscroll), this.doZoomIn = function(e) {
        if (!E.zoomactive) {
          E.zoomactive = !0, E.zoomrestore = {
            style: {}
          };
          var t = ["position", "top", "left", "zIndex", "backgroundColor", "marginTop", "marginBottom", "marginLeft", "marginRight"],
            n = E.win[0].style;
          for (var r in t) {
            var i = t[r];
            E.zoomrestore.style[i] = void 0 !== n[i] ? n[i] : ""
          }
          E.zoomrestore.style.width = E.win.css("width"), E.zoomrestore.style.height = E.win.css("height"), E.zoomrestore.padding = {
            w: E.win.outerWidth() - E.win.width(),
            h: E.win.outerHeight() - E.win.height()
          }, _.isios4 && (E.zoomrestore.scrollTop = c.scrollTop(), c.scrollTop(0)), E.win.css({
            position: _.isios4 ? "absolute" : "fixed",
            top: 0,
            left: 0,
            zIndex: o + 100,
            margin: 0
          });
          var a = E.win.css("backgroundColor");
          return ("" === a || /transparent|rgba\(0, 0, 0, 0\)|rgba\(0,0,0,0\)/.test(a)) && E.win.css("backgroundColor", "#fff"), E.rail.css({
            zIndex: o + 101
          }), E.zoom.css({
            zIndex: o + 102
          }), E.zoom.css("backgroundPosition", "0 -18px"), E.resizeZoom(), E.onzoomin && E.onzoomin.call(E), E.cancelEvent(e)
        }
      }, this.doZoomOut = function(e) {
        if (E.zoomactive) return E.zoomactive = !1, E.win.css("margin", ""), E.win.css(E.zoomrestore.style), _.isios4 && c.scrollTop(E.zoomrestore.scrollTop), E.rail.css({
          "z-index": E.zindex
        }), E.zoom.css({
          "z-index": E.zindex
        }), E.zoomrestore = !1, E.zoom.css("backgroundPosition", "0 0"), E.onResize(), E.onzoomout && E.onzoomout.call(E), E.cancelEvent(e)
      }, this.doZoom = function(e) {
        return E.zoomactive ? E.doZoomOut(e) : E.doZoomIn(e)
      }, this.resizeZoom = function() {
        if (E.zoomactive) {
          var e = E.getScrollTop();
          E.win.css({
            width: c.width() - E.zoomrestore.padding.w + "px",
            height: c.height() - E.zoomrestore.padding.h + "px"
          }), E.onResize(), E.setScrollTop(Math.min(E.page.maxh, e))
        }
      }, this.init(), a.nicescroll.push(this)
    },
    w = function(e) {
      var t = this;
      this.nc = e, this.lastx = 0, this.lasty = 0, this.speedx = 0, this.speedy = 0, this.lasttime = 0, this.steptime = 0, this.snapx = !1, this.snapy = !1, this.demulx = 0, this.demuly = 0, this.lastscrollx = -1, this.lastscrolly = -1, this.chkx = 0, this.chky = 0, this.timer = 0, this.reset = function(e, n) {
        t.stop(), t.steptime = 0, t.lasttime = m(), t.speedx = 0, t.speedy = 0, t.lastx = e, t.lasty = n, t.lastscrollx = -1, t.lastscrolly = -1
      }, this.update = function(e, n) {
        var r = m();
        t.steptime = r - t.lasttime, t.lasttime = r;
        var i = n - t.lasty,
          o = e - t.lastx,
          a = t.nc.getScrollTop() + i,
          s = t.nc.getScrollLeft() + o;
        t.snapx = s < 0 || s > t.nc.page.maxw, t.snapy = a < 0 || a > t.nc.page.maxh, t.speedx = o, t.speedy = i, t.lastx = e, t.lasty = n
      }, this.stop = function() {
        t.nc.unsynched("domomentum2d"), t.timer && clearTimeout(t.timer), t.timer = 0, t.lastscrollx = -1, t.lastscrolly = -1
      }, this.doSnapy = function(e, n) {
        var r = !1;
        n < 0 ? (n = 0, r = !0) : n > t.nc.page.maxh && (n = t.nc.page.maxh, r = !0), e < 0 ? (e = 0, r = !0) : e > t.nc.page.maxw && (e = t.nc.page.maxw, r = !0), r ? t.nc.doScrollPos(e, n, t.nc.opt.snapbackspeed) : t.nc.triggerScrollEnd()
      }, this.doMomentum = function(e) {
        var n = m(),
          r = e ? n + e : t.lasttime,
          i = t.nc.getScrollLeft(),
          o = t.nc.getScrollTop(),
          a = t.nc.page.maxh,
          s = t.nc.page.maxw;
        t.speedx = s > 0 ? Math.min(60, t.speedx) : 0, t.speedy = a > 0 ? Math.min(60, t.speedy) : 0;
        var l = r && n - r <= 60;
        (o < 0 || o > a || i < 0 || i > s) && (l = !1);
        var c = !(!t.speedy || !l) && t.speedy,
          u = !(!t.speedx || !l) && t.speedx;
        if (c || u) {
          var d = Math.max(16, t.steptime);
          if (d > 50) {
            var p = d / 50;
            t.speedx *= p, t.speedy *= p, d = 50
          }
          t.demulxy = 0, t.lastscrollx = t.nc.getScrollLeft(), t.chkx = t.lastscrollx, t.lastscrolly = t.nc.getScrollTop(), t.chky = t.lastscrolly;
          var f = t.lastscrollx,
            h = t.lastscrolly,
            g = function() {
              var e = m() - n > 600 ? .04 : .02;
              t.speedx && (f = Math.floor(t.lastscrollx - t.speedx * (1 - t.demulxy)), t.lastscrollx = f, (f < 0 || f > s) && (e = .1)), t.speedy && (h = Math.floor(t.lastscrolly - t.speedy * (1 - t.demulxy)), t.lastscrolly = h, (h < 0 || h > a) && (e = .1)), t.demulxy = Math.min(1, t.demulxy + e), t.nc.synched("domomentum2d", (function() {
                t.speedx && (t.nc.getScrollLeft(), t.chkx = f, t.nc.setScrollLeft(f)), t.speedy && (t.nc.getScrollTop(), t.chky = h, t.nc.setScrollTop(h)), t.timer || (t.nc.hideCursor(), t.doSnapy(f, h))
              })), t.demulxy < 1 ? t.timer = setTimeout(g, d) : (t.stop(), t.nc.hideCursor(), t.doSnapy(f, h))
            };
          g()
        } else t.doSnapy(t.nc.getScrollLeft(), t.nc.getScrollTop())
      }
    },
    x = e.fn.scrollTop;
  e.cssHooks.pageYOffset = {
    get: function(e, t, n) {
      var r = a.data(e, "__nicescroll") || !1;
      return r && r.ishwscroll ? r.getScrollTop() : x.call(e)
    },
    set: function(e, t) {
      var n = a.data(e, "__nicescroll") || !1;
      return n && n.ishwscroll ? n.setScrollTop(parseInt(t)) : x.call(e, t), this
    }
  }, e.fn.scrollTop = function(e) {
    if (void 0 === e) {
      var t = !!this[0] && (a.data(this[0], "__nicescroll") || !1);
      return t && t.ishwscroll ? t.getScrollTop() : x.call(this)
    }
    return this.each((function() {
      var t = a.data(this, "__nicescroll") || !1;
      t && t.ishwscroll ? t.setScrollTop(parseInt(e)) : x.call(a(this), e)
    }))
  };
  var S = e.fn.scrollLeft;
  a.cssHooks.pageXOffset = {
    get: function(e, t, n) {
      var r = a.data(e, "__nicescroll") || !1;
      return r && r.ishwscroll ? r.getScrollLeft() : S.call(e)
    },
    set: function(e, t) {
      var n = a.data(e, "__nicescroll") || !1;
      return n && n.ishwscroll ? n.setScrollLeft(parseInt(t)) : S.call(e, t), this
    }
  }, e.fn.scrollLeft = function(e) {
    if (void 0 === e) {
      var t = !!this[0] && (a.data(this[0], "__nicescroll") || !1);
      return t && t.ishwscroll ? t.getScrollLeft() : S.call(this)
    }
    return this.each((function() {
      var t = a.data(this, "__nicescroll") || !1;
      t && t.ishwscroll ? t.setScrollLeft(parseInt(e)) : S.call(a(this), e)
    }))
  };
  var C = function(e) {
    var t = this;
    if (this.length = 0, this.name = "nicescrollarray", this.each = function(e) {
        return a.each(t, e), t
      }, this.push = function(e) {
        t[t.length] = e, t.length++
      }, this.eq = function(e) {
        return t[e]
      }, e)
      for (var n = 0; n < e.length; n++) {
        var r = a.data(e[n], "__nicescroll") || !1;
        r && (this[this.length] = r, this.length++)
      }
    return this
  };
  ! function(e, t, n) {
    for (var r = 0, i = t.length; r < i; r++) n(e, t[r])
  }(C.prototype, ["show", "hide", "toggle", "onResize", "resize", "remove", "stop", "doScrollPos"], (function(e, t) {
    e[t] = function() {
      var e = arguments;
      return this.each((function() {
        this[t].apply(this, e)
      }))
    }
  })), e.fn.getNiceScroll = function(e) {
    return void 0 === e ? new C(this) : this[e] && a.data(this[e], "__nicescroll") || !1
  }, (e.expr.pseudos || e.expr[":"]).nicescroll = function(e) {
    return void 0 !== a.data(e, "__nicescroll")
  }, a.fn.niceScroll = function(e, t) {
    void 0 !== t || "object" != typeof e || "jquery" in e || (t = e, e = !1);
    var n = new C;
    return this.each((function() {
      var r = a(this),
        i = a.extend({}, t);
      if (e) {
        var o = a(e);
        i.doc = o.length > 1 ? a(e, r) : o, i.win = r
      }!("doc" in i) || "win" in i || (i.win = r);
      var s = r.data("__nicescroll") || !1;
      s || (i.doc = i.doc || r, s = new b(i, r), r.data("__nicescroll", s)), n.push(s)
    })), 1 === n.length ? n[0] : n
  }, l.NiceScroll = {
    getjQuery: function() {
      return e
    }
  }, a.nicescroll || (a.nicescroll = new C, a.nicescroll.options = g)
})),
function(e, t) {
  "object" == typeof exports && "undefined" != typeof module ? t(exports) : "function" == typeof define && define.amd ? define(["exports"], t) : t((e = "undefined" != typeof globalThis ? globalThis : e || self).Popper = {})
}(this, (function(e) {
  "use strict";

  function t(e) {
    if (null == e) return window;
    if ("[object Window]" !== e.toString()) {
      var t = e.ownerDocument;
      return t && t.defaultView || window
    }
    return e
  }

  function n(e) {
    return e instanceof t(e).Element || e instanceof Element
  }

  function r(e) {
    return e instanceof t(e).HTMLElement || e instanceof HTMLElement
  }

  function i(e) {
    return "undefined" != typeof ShadowRoot && (e instanceof t(e).ShadowRoot || e instanceof ShadowRoot)
  }
  var o = Math.max,
    a = Math.min,
    s = Math.round;

  function l() {
    var e = navigator.userAgentData;
    return null != e && e.brands ? e.brands.map((function(e) {
      return e.brand + "/" + e.version
    })).join(" ") : navigator.userAgent
  }

  function c() {
    return !/^((?!chrome|android).)*safari/i.test(l())
  }

  function u(e, i, o) {
    void 0 === i && (i = !1), void 0 === o && (o = !1);
    var a = e.getBoundingClientRect(),
      l = 1,
      u = 1;
    i && r(e) && (l = e.offsetWidth > 0 && s(a.width) / e.offsetWidth || 1, u = e.offsetHeight > 0 && s(a.height) / e.offsetHeight || 1);
    var d = (n(e) ? t(e) : window).visualViewport,
      p = !c() && o,
      f = (a.left + (p && d ? d.offsetLeft : 0)) / l,
      h = (a.top + (p && d ? d.offsetTop : 0)) / u,
      m = a.width / l,
      g = a.height / u;
    return {
      width: m,
      height: g,
      top: h,
      right: f + m,
      bottom: h + g,
      left: f,
      x: f,
      y: h
    }
  }

  function d(e) {
    var n = t(e);
    return {
      scrollLeft: n.pageXOffset,
      scrollTop: n.pageYOffset
    }
  }

  function p(e) {
    return e ? (e.nodeName || "").toLowerCase() : null
  }

  function f(e) {
    return ((n(e) ? e.ownerDocument : e.document) || window.document).documentElement
  }

  function h(e) {
    return u(f(e)).left + d(e).scrollLeft
  }

  function m(e) {
    return t(e).getComputedStyle(e)
  }

  function g(e) {
    var t = m(e),
      n = t.overflow,
      r = t.overflowX,
      i = t.overflowY;
    return /auto|scroll|overlay|hidden/.test(n + i + r)
  }

  function v(e, n, i) {
    void 0 === i && (i = !1);
    var o, a, l = r(n),
      c = r(n) && function(e) {
        var t = e.getBoundingClientRect(),
          n = s(t.width) / e.offsetWidth || 1,
          r = s(t.height) / e.offsetHeight || 1;
        return 1 !== n || 1 !== r
      }(n),
      m = f(n),
      v = u(e, c, i),
      y = {
        scrollLeft: 0,
        scrollTop: 0
      },
      b = {
        x: 0,
        y: 0
      };
    return (l || !l && !i) && (("body" !== p(n) || g(m)) && (y = (o = n) !== t(o) && r(o) ? {
      scrollLeft: (a = o).scrollLeft,
      scrollTop: a.scrollTop
    } : d(o)), r(n) ? ((b = u(n, !0)).x += n.clientLeft, b.y += n.clientTop) : m && (b.x = h(m))), {
      x: v.left + y.scrollLeft - b.x,
      y: v.top + y.scrollTop - b.y,
      width: v.width,
      height: v.height
    }
  }

  function y(e) {
    var t = u(e),
      n = e.offsetWidth,
      r = e.offsetHeight;
    return Math.abs(t.width - n) <= 1 && (n = t.width), Math.abs(t.height - r) <= 1 && (r = t.height), {
      x: e.offsetLeft,
      y: e.offsetTop,
      width: n,
      height: r
    }
  }

  function b(e) {
    return "html" === p(e) ? e : e.assignedSlot || e.parentNode || (i(e) ? e.host : null) || f(e)
  }

  function w(e) {
    return ["html", "body", "#document"].indexOf(p(e)) >= 0 ? e.ownerDocument.body : r(e) && g(e) ? e : w(b(e))
  }

  function x(e, n) {
    var r;
    void 0 === n && (n = []);
    var i = w(e),
      o = i === (null == (r = e.ownerDocument) ? void 0 : r.body),
      a = t(i),
      s = o ? [a].concat(a.visualViewport || [], g(i) ? i : []) : i,
      l = n.concat(s);
    return o ? l : l.concat(x(b(s)))
  }

  function S(e) {
    return ["table", "td", "th"].indexOf(p(e)) >= 0
  }

  function C(e) {
    return r(e) && "fixed" !== m(e).position ? e.offsetParent : null
  }

  function E(e) {
    for (var n = t(e), o = C(e); o && S(o) && "static" === m(o).position;) o = C(o);
    return o && ("html" === p(o) || "body" === p(o) && "static" === m(o).position) ? n : o || function(e) {
      var t = /firefox/i.test(l());
      if (/Trident/i.test(l()) && r(e) && "fixed" === m(e).position) return null;
      var n = b(e);
      for (i(n) && (n = n.host); r(n) && ["html", "body"].indexOf(p(n)) < 0;) {
        var o = m(n);
        if ("none" !== o.transform || "none" !== o.perspective || "paint" === o.contain || -1 !== ["transform", "perspective"].indexOf(o.willChange) || t && "filter" === o.willChange || t && o.filter && "none" !== o.filter) return n;
        n = n.parentNode
      }
      return null
    }(e) || n
  }
  var T = "top",
    k = "bottom",
    D = "right",
    O = "left",
    A = "auto",
    _ = [T, k, D, O],
    M = "start",
    L = "end",
    I = "viewport",
    P = "popper",
    j = _.reduce((function(e, t) {
      return e.concat([t + "-" + M, t + "-" + L])
    }), []),
    N = [].concat(_, [A]).reduce((function(e, t) {
      return e.concat([t, t + "-" + M, t + "-" + L])
    }), []),
    z = ["beforeRead", "read", "afterRead", "beforeMain", "main", "afterMain", "beforeWrite", "write", "afterWrite"];

  function R(e) {
    var t = new Map,
      n = new Set,
      r = [];

    function i(e) {
      n.add(e.name), [].concat(e.requires || [], e.requiresIfExists || []).forEach((function(e) {
        if (!n.has(e)) {
          var r = t.get(e);
          r && i(r)
        }
      })), r.push(e)
    }
    return e.forEach((function(e) {
      t.set(e.name, e)
    })), e.forEach((function(e) {
      n.has(e.name) || i(e)
    })), r
  }

  function $(e) {
    return e.split("-")[0]
  }

  function H(e, t) {
    var n = t.getRootNode && t.getRootNode();
    if (e.contains(t)) return !0;
    if (n && i(n)) {
      var r = t;
      do {
        if (r && e.isSameNode(r)) return !0;
        r = r.parentNode || r.host
      } while (r)
    }
    return !1
  }

  function F(e) {
    return Object.assign({}, e, {
      left: e.x,
      top: e.y,
      right: e.x + e.width,
      bottom: e.y + e.height
    })
  }

  function B(e, r, i) {
    return r === I ? F(function(e, n) {
      var r = t(e),
        i = f(e),
        o = r.visualViewport,
        a = i.clientWidth,
        s = i.clientHeight,
        l = 0,
        u = 0;
      if (o) {
        a = o.width, s = o.height;
        var d = c();
        (d || !d && "fixed" === n) && (l = o.offsetLeft, u = o.offsetTop)
      }
      return {
        width: a,
        height: s,
        x: l + h(e),
        y: u
      }
    }(e, i)) : n(r) ? function(e, t) {
      var n = u(e, !1, "fixed" === t);
      return n.top = n.top + e.clientTop, n.left = n.left + e.clientLeft, n.bottom = n.top + e.clientHeight, n.right = n.left + e.clientWidth, n.width = e.clientWidth, n.height = e.clientHeight, n.x = n.left, n.y = n.top, n
    }(r, i) : F(function(e) {
      var t, n = f(e),
        r = d(e),
        i = null == (t = e.ownerDocument) ? void 0 : t.body,
        a = o(n.scrollWidth, n.clientWidth, i ? i.scrollWidth : 0, i ? i.clientWidth : 0),
        s = o(n.scrollHeight, n.clientHeight, i ? i.scrollHeight : 0, i ? i.clientHeight : 0),
        l = -r.scrollLeft + h(e),
        c = -r.scrollTop;
      return "rtl" === m(i || n).direction && (l += o(n.clientWidth, i ? i.clientWidth : 0) - a), {
        width: a,
        height: s,
        x: l,
        y: c
      }
    }(f(e)))
  }

  function q(e, t, i, s) {
    var l = "clippingParents" === t ? function(e) {
        var t = x(b(e)),
          i = ["absolute", "fixed"].indexOf(m(e).position) >= 0 && r(e) ? E(e) : e;
        return n(i) ? t.filter((function(e) {
          return n(e) && H(e, i) && "body" !== p(e)
        })) : []
      }(e) : [].concat(t),
      c = [].concat(l, [i]),
      u = c[0],
      d = c.reduce((function(t, n) {
        var r = B(e, n, s);
        return t.top = o(r.top, t.top), t.right = a(r.right, t.right), t.bottom = a(r.bottom, t.bottom), t.left = o(r.left, t.left), t
      }), B(e, u, s));
    return d.width = d.right - d.left, d.height = d.bottom - d.top, d.x = d.left, d.y = d.top, d
  }

  function W(e) {
    return e.split("-")[1]
  }

  function Y(e) {
    return ["top", "bottom"].indexOf(e) >= 0 ? "x" : "y"
  }

  function U(e) {
    var t, n = e.reference,
      r = e.element,
      i = e.placement,
      o = i ? $(i) : null,
      a = i ? W(i) : null,
      s = n.x + n.width / 2 - r.width / 2,
      l = n.y + n.height / 2 - r.height / 2;
    switch (o) {
      case T:
        t = {
          x: s,
          y: n.y - r.height
        };
        break;
      case k:
        t = {
          x: s,
          y: n.y + n.height
        };
        break;
      case D:
        t = {
          x: n.x + n.width,
          y: l
        };
        break;
      case O:
        t = {
          x: n.x - r.width,
          y: l
        };
        break;
      default:
        t = {
          x: n.x,
          y: n.y
        }
    }
    var c = o ? Y(o) : null;
    if (null != c) {
      var u = "y" === c ? "height" : "width";
      switch (a) {
        case M:
          t[c] = t[c] - (n[u] / 2 - r[u] / 2);
          break;
        case L:
          t[c] = t[c] + (n[u] / 2 - r[u] / 2)
      }
    }
    return t
  }

  function V(e) {
    return Object.assign({}, {
      top: 0,
      right: 0,
      bottom: 0,
      left: 0
    }, e)
  }

  function X(e, t) {
    return t.reduce((function(t, n) {
      return t[n] = e, t
    }), {})
  }

  function G(e, t) {
    void 0 === t && (t = {});
    var r = t,
      i = r.placement,
      o = void 0 === i ? e.placement : i,
      a = r.strategy,
      s = void 0 === a ? e.strategy : a,
      l = r.boundary,
      c = void 0 === l ? "clippingParents" : l,
      d = r.rootBoundary,
      p = void 0 === d ? I : d,
      h = r.elementContext,
      m = void 0 === h ? P : h,
      g = r.altBoundary,
      v = void 0 !== g && g,
      y = r.padding,
      b = void 0 === y ? 0 : y,
      w = V("number" != typeof b ? b : X(b, _)),
      x = m === P ? "reference" : P,
      S = e.rects.popper,
      C = e.elements[v ? x : m],
      E = q(n(C) ? C : C.contextElement || f(e.elements.popper), c, p, s),
      O = u(e.elements.reference),
      A = U({
        reference: O,
        element: S,
        strategy: "absolute",
        placement: o
      }),
      M = F(Object.assign({}, S, A)),
      L = m === P ? M : O,
      j = {
        top: E.top - L.top + w.top,
        bottom: L.bottom - E.bottom + w.bottom,
        left: E.left - L.left + w.left,
        right: L.right - E.right + w.right
      },
      N = e.modifiersData.offset;
    if (m === P && N) {
      var z = N[o];
      Object.keys(j).forEach((function(e) {
        var t = [D, k].indexOf(e) >= 0 ? 1 : -1,
          n = [T, k].indexOf(e) >= 0 ? "y" : "x";
        j[e] += z[n] * t
      }))
    }
    return j
  }
  var Z = {
    placement: "bottom",
    modifiers: [],
    strategy: "absolute"
  };

  function K() {
    for (var e = arguments.length, t = new Array(e), n = 0; n < e; n++) t[n] = arguments[n];
    return !t.some((function(e) {
      return !(e && "function" == typeof e.getBoundingClientRect)
    }))
  }

  function J(e) {
    void 0 === e && (e = {});
    var t = e,
      r = t.defaultModifiers,
      i = void 0 === r ? [] : r,
      o = t.defaultOptions,
      a = void 0 === o ? Z : o;
    return function(e, t, r) {
      void 0 === r && (r = a);
      var o, s, l = {
          placement: "bottom",
          orderedModifiers: [],
          options: Object.assign({}, Z, a),
          modifiersData: {},
          elements: {
            reference: e,
            popper: t
          },
          attributes: {},
          styles: {}
        },
        c = [],
        u = !1,
        d = {
          state: l,
          setOptions: function(r) {
            var o = "function" == typeof r ? r(l.options) : r;
            p(), l.options = Object.assign({}, a, l.options, o), l.scrollParents = {
              reference: n(e) ? x(e) : e.contextElement ? x(e.contextElement) : [],
              popper: x(t)
            };
            var s, u, f = function(e) {
              var t = R(e);
              return z.reduce((function(e, n) {
                return e.concat(t.filter((function(e) {
                  return e.phase === n
                })))
              }), [])
            }((s = [].concat(i, l.options.modifiers), u = s.reduce((function(e, t) {
              var n = e[t.name];
              return e[t.name] = n ? Object.assign({}, n, t, {
                options: Object.assign({}, n.options, t.options),
                data: Object.assign({}, n.data, t.data)
              }) : t, e
            }), {}), Object.keys(u).map((function(e) {
              return u[e]
            }))));
            return l.orderedModifiers = f.filter((function(e) {
              return e.enabled
            })), l.orderedModifiers.forEach((function(e) {
              var t = e.name,
                n = e.options,
                r = void 0 === n ? {} : n,
                i = e.effect;
              if ("function" == typeof i) {
                var o = i({
                  state: l,
                  name: t,
                  instance: d,
                  options: r
                });
                c.push(o || function() {})
              }
            })), d.update()
          },
          forceUpdate: function() {
            if (!u) {
              var e = l.elements,
                t = e.reference,
                n = e.popper;
              if (K(t, n)) {
                l.rects = {
                  reference: v(t, E(n), "fixed" === l.options.strategy),
                  popper: y(n)
                }, l.reset = !1, l.placement = l.options.placement, l.orderedModifiers.forEach((function(e) {
                  return l.modifiersData[e.name] = Object.assign({}, e.data)
                }));
                for (var r = 0; r < l.orderedModifiers.length; r++)
                  if (!0 !== l.reset) {
                    var i = l.orderedModifiers[r],
                      o = i.fn,
                      a = i.options,
                      s = void 0 === a ? {} : a,
                      c = i.name;
                    "function" == typeof o && (l = o({
                      state: l,
                      options: s,
                      name: c,
                      instance: d
                    }) || l)
                  } else l.reset = !1, r = -1
              }
            }
          },
          update: (o = function() {
            return new Promise((function(e) {
              d.forceUpdate(), e(l)
            }))
          }, function() {
            return s || (s = new Promise((function(e) {
              Promise.resolve().then((function() {
                s = void 0, e(o())
              }))
            }))), s
          }),
          destroy: function() {
            p(), u = !0
          }
        };
      if (!K(e, t)) return d;

      function p() {
        c.forEach((function(e) {
          return e()
        })), c = []
      }
      return d.setOptions(r).then((function(e) {
        !u && r.onFirstUpdate && r.onFirstUpdate(e)
      })), d
    }
  }
  var Q = {
      passive: !0
    },
    ee = {
      name: "eventListeners",
      enabled: !0,
      phase: "write",
      fn: function() {},
      effect: function(e) {
        var n = e.state,
          r = e.instance,
          i = e.options,
          o = i.scroll,
          a = void 0 === o || o,
          s = i.resize,
          l = void 0 === s || s,
          c = t(n.elements.popper),
          u = [].concat(n.scrollParents.reference, n.scrollParents.popper);
        return a && u.forEach((function(e) {
            e.addEventListener("scroll", r.update, Q)
          })), l && c.addEventListener("resize", r.update, Q),
          function() {
            a && u.forEach((function(e) {
              e.removeEventListener("scroll", r.update, Q)
            })), l && c.removeEventListener("resize", r.update, Q)
          }
      },
      data: {}
    },
    te = {
      name: "popperOffsets",
      enabled: !0,
      phase: "read",
      fn: function(e) {
        var t = e.state,
          n = e.name;
        t.modifiersData[n] = U({
          reference: t.rects.reference,
          element: t.rects.popper,
          strategy: "absolute",
          placement: t.placement
        })
      },
      data: {}
    },
    ne = {
      top: "auto",
      right: "auto",
      bottom: "auto",
      left: "auto"
    };

  function re(e) {
    var n, r = e.popper,
      i = e.popperRect,
      o = e.placement,
      a = e.variation,
      l = e.offsets,
      c = e.position,
      u = e.gpuAcceleration,
      d = e.adaptive,
      p = e.roundOffsets,
      h = e.isFixed,
      g = l.x,
      v = void 0 === g ? 0 : g,
      y = l.y,
      b = void 0 === y ? 0 : y,
      w = "function" == typeof p ? p({
        x: v,
        y: b
      }) : {
        x: v,
        y: b
      };
    v = w.x, b = w.y;
    var x = l.hasOwnProperty("x"),
      S = l.hasOwnProperty("y"),
      C = O,
      A = T,
      _ = window;
    if (d) {
      var M = E(r),
        I = "clientHeight",
        P = "clientWidth";
      M === t(r) && "static" !== m(M = f(r)).position && "absolute" === c && (I = "scrollHeight", P = "scrollWidth"), (o === T || (o === O || o === D) && a === L) && (A = k, b -= (h && M === _ && _.visualViewport ? _.visualViewport.height : M[I]) - i.height, b *= u ? 1 : -1), o !== O && (o !== T && o !== k || a !== L) || (C = D, v -= (h && M === _ && _.visualViewport ? _.visualViewport.width : M[P]) - i.width, v *= u ? 1 : -1)
    }
    var j, N = Object.assign({
        position: c
      }, d && ne),
      z = !0 === p ? function(e) {
        var t = e.x,
          n = e.y,
          r = window.devicePixelRatio || 1;
        return {
          x: s(t * r) / r || 0,
          y: s(n * r) / r || 0
        }
      }({
        x: v,
        y: b
      }) : {
        x: v,
        y: b
      };
    return v = z.x, b = z.y, u ? Object.assign({}, N, ((j = {})[A] = S ? "0" : "", j[C] = x ? "0" : "", j.transform = (_.devicePixelRatio || 1) <= 1 ? "translate(" + v + "px, " + b + "px)" : "translate3d(" + v + "px, " + b + "px, 0)", j)) : Object.assign({}, N, ((n = {})[A] = S ? b + "px" : "", n[C] = x ? v + "px" : "", n.transform = "", n))
  }
  var ie = {
      name: "computeStyles",
      enabled: !0,
      phase: "beforeWrite",
      fn: function(e) {
        var t = e.state,
          n = e.options,
          r = n.gpuAcceleration,
          i = void 0 === r || r,
          o = n.adaptive,
          a = void 0 === o || o,
          s = n.roundOffsets,
          l = void 0 === s || s,
          c = {
            placement: $(t.placement),
            variation: W(t.placement),
            popper: t.elements.popper,
            popperRect: t.rects.popper,
            gpuAcceleration: i,
            isFixed: "fixed" === t.options.strategy
          };
        null != t.modifiersData.popperOffsets && (t.styles.popper = Object.assign({}, t.styles.popper, re(Object.assign({}, c, {
          offsets: t.modifiersData.popperOffsets,
          position: t.options.strategy,
          adaptive: a,
          roundOffsets: l
        })))), null != t.modifiersData.arrow && (t.styles.arrow = Object.assign({}, t.styles.arrow, re(Object.assign({}, c, {
          offsets: t.modifiersData.arrow,
          position: "absolute",
          adaptive: !1,
          roundOffsets: l
        })))), t.attributes.popper = Object.assign({}, t.attributes.popper, {
          "data-popper-placement": t.placement
        })
      },
      data: {}
    },
    oe = {
      name: "applyStyles",
      enabled: !0,
      phase: "write",
      fn: function(e) {
        var t = e.state;
        Object.keys(t.elements).forEach((function(e) {
          var n = t.styles[e] || {},
            i = t.attributes[e] || {},
            o = t.elements[e];
          r(o) && p(o) && (Object.assign(o.style, n), Object.keys(i).forEach((function(e) {
            var t = i[e];
            !1 === t ? o.removeAttribute(e) : o.setAttribute(e, !0 === t ? "" : t)
          })))
        }))
      },
      effect: function(e) {
        var t = e.state,
          n = {
            popper: {
              position: t.options.strategy,
              left: "0",
              top: "0",
              margin: "0"
            },
            arrow: {
              position: "absolute"
            },
            reference: {}
          };
        return Object.assign(t.elements.popper.style, n.popper), t.styles = n, t.elements.arrow && Object.assign(t.elements.arrow.style, n.arrow),
          function() {
            Object.keys(t.elements).forEach((function(e) {
              var i = t.elements[e],
                o = t.attributes[e] || {},
                a = Object.keys(t.styles.hasOwnProperty(e) ? t.styles[e] : n[e]).reduce((function(e, t) {
                  return e[t] = "", e
                }), {});
              r(i) && p(i) && (Object.assign(i.style, a), Object.keys(o).forEach((function(e) {
                i.removeAttribute(e)
              })))
            }))
          }
      },
      requires: ["computeStyles"]
    },
    ae = {
      name: "offset",
      enabled: !0,
      phase: "main",
      requires: ["popperOffsets"],
      fn: function(e) {
        var t = e.state,
          n = e.options,
          r = e.name,
          i = n.offset,
          o = void 0 === i ? [0, 0] : i,
          a = N.reduce((function(e, n) {
            return e[n] = function(e, t, n) {
              var r = $(e),
                i = [O, T].indexOf(r) >= 0 ? -1 : 1,
                o = "function" == typeof n ? n(Object.assign({}, t, {
                  placement: e
                })) : n,
                a = o[0],
                s = o[1];
              return a = a || 0, s = (s || 0) * i, [O, D].indexOf(r) >= 0 ? {
                x: s,
                y: a
              } : {
                x: a,
                y: s
              }
            }(n, t.rects, o), e
          }), {}),
          s = a[t.placement],
          l = s.x,
          c = s.y;
        null != t.modifiersData.popperOffsets && (t.modifiersData.popperOffsets.x += l, t.modifiersData.popperOffsets.y += c), t.modifiersData[r] = a
      }
    },
    se = {
      left: "right",
      right: "left",
      bottom: "top",
      top: "bottom"
    };

  function le(e) {
    return e.replace(/left|right|bottom|top/g, (function(e) {
      return se[e]
    }))
  }
  var ce = {
    start: "end",
    end: "start"
  };

  function ue(e) {
    return e.replace(/start|end/g, (function(e) {
      return ce[e]
    }))
  }

  function de(e, t) {
    void 0 === t && (t = {});
    var n = t,
      r = n.placement,
      i = n.boundary,
      o = n.rootBoundary,
      a = n.padding,
      s = n.flipVariations,
      l = n.allowedAutoPlacements,
      c = void 0 === l ? N : l,
      u = W(r),
      d = u ? s ? j : j.filter((function(e) {
        return W(e) === u
      })) : _,
      p = d.filter((function(e) {
        return c.indexOf(e) >= 0
      }));
    0 === p.length && (p = d);
    var f = p.reduce((function(t, n) {
      return t[n] = G(e, {
        placement: n,
        boundary: i,
        rootBoundary: o,
        padding: a
      })[$(n)], t
    }), {});
    return Object.keys(f).sort((function(e, t) {
      return f[e] - f[t]
    }))
  }
  var pe = {
    name: "flip",
    enabled: !0,
    phase: "main",
    fn: function(e) {
      var t = e.state,
        n = e.options,
        r = e.name;
      if (!t.modifiersData[r]._skip) {
        for (var i = n.mainAxis, o = void 0 === i || i, a = n.altAxis, s = void 0 === a || a, l = n.fallbackPlacements, c = n.padding, u = n.boundary, d = n.rootBoundary, p = n.altBoundary, f = n.flipVariations, h = void 0 === f || f, m = n.allowedAutoPlacements, g = t.options.placement, v = $(g), y = l || (v !== g && h ? function(e) {
            if ($(e) === A) return [];
            var t = le(e);
            return [ue(e), t, ue(t)]
          }(g) : [le(g)]), b = [g].concat(y).reduce((function(e, n) {
            return e.concat($(n) === A ? de(t, {
              placement: n,
              boundary: u,
              rootBoundary: d,
              padding: c,
              flipVariations: h,
              allowedAutoPlacements: m
            }) : n)
          }), []), w = t.rects.reference, x = t.rects.popper, S = new Map, C = !0, E = b[0], _ = 0; _ < b.length; _++) {
          var L = b[_],
            I = $(L),
            P = W(L) === M,
            j = [T, k].indexOf(I) >= 0,
            N = j ? "width" : "height",
            z = G(t, {
              placement: L,
              boundary: u,
              rootBoundary: d,
              altBoundary: p,
              padding: c
            }),
            R = j ? P ? D : O : P ? k : T;
          w[N] > x[N] && (R = le(R));
          var H = le(R),
            F = [];
          if (o && F.push(z[I] <= 0), s && F.push(z[R] <= 0, z[H] <= 0), F.every((function(e) {
              return e
            }))) {
            E = L, C = !1;
            break
          }
          S.set(L, F)
        }
        if (C)
          for (var B = function(e) {
              var t = b.find((function(t) {
                var n = S.get(t);
                if (n) return n.slice(0, e).every((function(e) {
                  return e
                }))
              }));
              if (t) return E = t, "break"
            }, q = h ? 3 : 1; q > 0 && "break" !== B(q); q--);
        t.placement !== E && (t.modifiersData[r]._skip = !0, t.placement = E, t.reset = !0)
      }
    },
    requiresIfExists: ["offset"],
    data: {
      _skip: !1
    }
  };

  function fe(e, t, n) {
    return o(e, a(t, n))
  }
  var he = {
      name: "preventOverflow",
      enabled: !0,
      phase: "main",
      fn: function(e) {
        var t = e.state,
          n = e.options,
          r = e.name,
          i = n.mainAxis,
          s = void 0 === i || i,
          l = n.altAxis,
          c = void 0 !== l && l,
          u = n.boundary,
          d = n.rootBoundary,
          p = n.altBoundary,
          f = n.padding,
          h = n.tether,
          m = void 0 === h || h,
          g = n.tetherOffset,
          v = void 0 === g ? 0 : g,
          b = G(t, {
            boundary: u,
            rootBoundary: d,
            padding: f,
            altBoundary: p
          }),
          w = $(t.placement),
          x = W(t.placement),
          S = !x,
          C = Y(w),
          A = "x" === C ? "y" : "x",
          _ = t.modifiersData.popperOffsets,
          L = t.rects.reference,
          I = t.rects.popper,
          P = "function" == typeof v ? v(Object.assign({}, t.rects, {
            placement: t.placement
          })) : v,
          j = "number" == typeof P ? {
            mainAxis: P,
            altAxis: P
          } : Object.assign({
            mainAxis: 0,
            altAxis: 0
          }, P),
          N = t.modifiersData.offset ? t.modifiersData.offset[t.placement] : null,
          z = {
            x: 0,
            y: 0
          };
        if (_) {
          if (s) {
            var R, H = "y" === C ? T : O,
              F = "y" === C ? k : D,
              B = "y" === C ? "height" : "width",
              q = _[C],
              U = q + b[H],
              V = q - b[F],
              X = m ? -I[B] / 2 : 0,
              Z = x === M ? L[B] : I[B],
              K = x === M ? -I[B] : -L[B],
              J = t.elements.arrow,
              Q = m && J ? y(J) : {
                width: 0,
                height: 0
              },
              ee = t.modifiersData["arrow#persistent"] ? t.modifiersData["arrow#persistent"].padding : {
                top: 0,
                right: 0,
                bottom: 0,
                left: 0
              },
              te = ee[H],
              ne = ee[F],
              re = fe(0, L[B], Q[B]),
              ie = S ? L[B] / 2 - X - re - te - j.mainAxis : Z - re - te - j.mainAxis,
              oe = S ? -L[B] / 2 + X + re + ne + j.mainAxis : K + re + ne + j.mainAxis,
              ae = t.elements.arrow && E(t.elements.arrow),
              se = ae ? "y" === C ? ae.clientTop || 0 : ae.clientLeft || 0 : 0,
              le = null != (R = null == N ? void 0 : N[C]) ? R : 0,
              ce = q + oe - le,
              ue = fe(m ? a(U, q + ie - le - se) : U, q, m ? o(V, ce) : V);
            _[C] = ue, z[C] = ue - q
          }
          if (c) {
            var de, pe = "x" === C ? T : O,
              he = "x" === C ? k : D,
              me = _[A],
              ge = "y" === A ? "height" : "width",
              ve = me + b[pe],
              ye = me - b[he],
              be = -1 !== [T, O].indexOf(w),
              we = null != (de = null == N ? void 0 : N[A]) ? de : 0,
              xe = be ? ve : me - L[ge] - I[ge] - we + j.altAxis,
              Se = be ? me + L[ge] + I[ge] - we - j.altAxis : ye,
              Ce = m && be ? function(e, t, n) {
                var r = fe(e, t, n);
                return r > n ? n : r
              }(xe, me, Se) : fe(m ? xe : ve, me, m ? Se : ye);
            _[A] = Ce, z[A] = Ce - me
          }
          t.modifiersData[r] = z
        }
      },
      requiresIfExists: ["offset"]
    },
    me = {
      name: "arrow",
      enabled: !0,
      phase: "main",
      fn: function(e) {
        var t, n = e.state,
          r = e.name,
          i = e.options,
          o = n.elements.arrow,
          a = n.modifiersData.popperOffsets,
          s = $(n.placement),
          l = Y(s),
          c = [O, D].indexOf(s) >= 0 ? "height" : "width";
        if (o && a) {
          var u = function(e, t) {
              return V("number" != typeof(e = "function" == typeof e ? e(Object.assign({}, t.rects, {
                placement: t.placement
              })) : e) ? e : X(e, _))
            }(i.padding, n),
            d = y(o),
            p = "y" === l ? T : O,
            f = "y" === l ? k : D,
            h = n.rects.reference[c] + n.rects.reference[l] - a[l] - n.rects.popper[c],
            m = a[l] - n.rects.reference[l],
            g = E(o),
            v = g ? "y" === l ? g.clientHeight || 0 : g.clientWidth || 0 : 0,
            b = h / 2 - m / 2,
            w = u[p],
            x = v - d[c] - u[f],
            S = v / 2 - d[c] / 2 + b,
            C = fe(w, S, x),
            A = l;
          n.modifiersData[r] = ((t = {})[A] = C, t.centerOffset = C - S, t)
        }
      },
      effect: function(e) {
        var t = e.state,
          n = e.options.element,
          r = void 0 === n ? "[data-popper-arrow]" : n;
        null != r && ("string" != typeof r || (r = t.elements.popper.querySelector(r))) && H(t.elements.popper, r) && (t.elements.arrow = r)
      },
      requires: ["popperOffsets"],
      requiresIfExists: ["preventOverflow"]
    };

  function ge(e, t, n) {
    return void 0 === n && (n = {
      x: 0,
      y: 0
    }), {
      top: e.top - t.height - n.y,
      right: e.right - t.width + n.x,
      bottom: e.bottom - t.height + n.y,
      left: e.left - t.width - n.x
    }
  }

  function ve(e) {
    return [T, D, k, O].some((function(t) {
      return e[t] >= 0
    }))
  }
  var ye = {
      name: "hide",
      enabled: !0,
      phase: "main",
      requiresIfExists: ["preventOverflow"],
      fn: function(e) {
        var t = e.state,
          n = e.name,
          r = t.rects.reference,
          i = t.rects.popper,
          o = t.modifiersData.preventOverflow,
          a = G(t, {
            elementContext: "reference"
          }),
          s = G(t, {
            altBoundary: !0
          }),
          l = ge(a, r),
          c = ge(s, i, o),
          u = ve(l),
          d = ve(c);
        t.modifiersData[n] = {
          referenceClippingOffsets: l,
          popperEscapeOffsets: c,
          isReferenceHidden: u,
          hasPopperEscaped: d
        }, t.attributes.popper = Object.assign({}, t.attributes.popper, {
          "data-popper-reference-hidden": u,
          "data-popper-escaped": d
        })
      }
    },
    be = J({
      defaultModifiers: [ee, te, ie, oe]
    }),
    we = [ee, te, ie, oe, ae, pe, he, me, ye],
    xe = J({
      defaultModifiers: we
    });
  e.applyStyles = oe, e.arrow = me, e.computeStyles = ie, e.createPopper = xe, e.createPopperLite = be, e.defaultModifiers = we, e.detectOverflow = G, e.eventListeners = ee, e.flip = pe, e.hide = ye, e.offset = ae, e.popperGenerator = J, e.popperOffsets = te, e.preventOverflow = he, Object.defineProperty(e, "__esModule", {
    value: !0
  })
})),
function(e, t) {
  "object" == typeof exports && "undefined" != typeof module ? module.exports = t(require("@popperjs/core")) : "function" == typeof define && define.amd ? define(["@popperjs/core"], t) : (e = e || self).tippy = t(e.Popper)
}(this, (function(e) {
  "use strict";
  var t = "undefined" != typeof window && "undefined" != typeof document,
    n = !!t && !!window.msCrypto,
    r = {
      passive: !0,
      capture: !0
    },
    i = function() {
      return document.body
    };

  function o(e, t, n) {
    if (Array.isArray(e)) {
      var r = e[t];
      return null == r ? Array.isArray(n) ? n[t] : n : r
    }
    return e
  }

  function a(e, t) {
    var n = {}.toString.call(e);
    return 0 === n.indexOf("[object") && n.indexOf(t + "]") > -1
  }

  function s(e, t) {
    return "function" == typeof e ? e.apply(void 0, t) : e
  }

  function l(e, t) {
    return 0 === t ? e : function(r) {
      clearTimeout(n), n = setTimeout((function() {
        e(r)
      }), t)
    };
    var n
  }

  function c(e, t) {
    var n = Object.assign({}, e);
    return t.forEach((function(e) {
      delete n[e]
    })), n
  }

  function u(e) {
    return [].concat(e)
  }

  function d(e, t) {
    -1 === e.indexOf(t) && e.push(t)
  }

  function p(e) {
    return e.split("-")[0]
  }

  function f(e) {
    return [].slice.call(e)
  }

  function h(e) {
    return Object.keys(e).reduce((function(t, n) {
      return void 0 !== e[n] && (t[n] = e[n]), t
    }), {})
  }

  function m() {
    return document.createElement("div")
  }

  function g(e) {
    return ["Element", "Fragment"].some((function(t) {
      return a(e, t)
    }))
  }

  function v(e) {
    return a(e, "MouseEvent")
  }

  function y(e) {
    return !(!e || !e._tippy || e._tippy.reference !== e)
  }

  function b(e, t) {
    e.forEach((function(e) {
      e && (e.style.transitionDuration = t + "ms")
    }))
  }

  function w(e, t) {
    e.forEach((function(e) {
      e && e.setAttribute("data-state", t)
    }))
  }

  function x(e) {
    var t, n = u(e)[0];
    return null != n && null != (t = n.ownerDocument) && t.body ? n.ownerDocument : document
  }

  function S(e, t, n) {
    var r = t + "EventListener";
    ["transitionend", "webkitTransitionEnd"].forEach((function(t) {
      e[r](t, n)
    }))
  }

  function C(e, t) {
    for (var n = t; n;) {
      var r;
      if (e.contains(n)) return !0;
      n = null == n.getRootNode || null == (r = n.getRootNode()) ? void 0 : r.host
    }
    return !1
  }
  var E = {
      isTouch: !1
    },
    T = 0;

  function k() {
    E.isTouch || (E.isTouch = !0, window.performance && document.addEventListener("mousemove", D))
  }

  function D() {
    var e = performance.now();
    e - T < 20 && (E.isTouch = !1, document.removeEventListener("mousemove", D)), T = e
  }

  function O() {
    var e = document.activeElement;
    if (y(e)) {
      var t = e._tippy;
      e.blur && !t.state.isVisible && e.blur()
    }
  }
  var A = Object.assign({
      appendTo: i,
      aria: {
        content: "auto",
        expanded: "auto"
      },
      delay: 0,
      duration: [300, 250],
      getReferenceClientRect: null,
      hideOnClick: !0,
      ignoreAttributes: !1,
      interactive: !1,
      interactiveBorder: 2,
      interactiveDebounce: 0,
      moveTransition: "",
      offset: [0, 10],
      onAfterUpdate: function() {},
      onBeforeUpdate: function() {},
      onCreate: function() {},
      onDestroy: function() {},
      onHidden: function() {},
      onHide: function() {},
      onMount: function() {},
      onShow: function() {},
      onShown: function() {},
      onTrigger: function() {},
      onUntrigger: function() {},
      onClickOutside: function() {},
      placement: "top",
      plugins: [],
      popperOptions: {},
      render: null,
      showOnCreate: !1,
      touch: !0,
      trigger: "mouseenter focus",
      triggerTarget: null
    }, {
      animateFill: !1,
      followCursor: !1,
      inlinePositioning: !1,
      sticky: !1
    }, {
      allowHTML: !1,
      animation: "fade",
      arrow: !0,
      content: "",
      inertia: !1,
      maxWidth: 350,
      role: "tooltip",
      theme: "",
      zIndex: 9999
    }),
    _ = Object.keys(A);

  function M(e) {
    var t = (e.plugins || []).reduce((function(t, n) {
      var r, i = n.name,
        o = n.defaultValue;
      return i && (t[i] = void 0 !== e[i] ? e[i] : null != (r = A[i]) ? r : o), t
    }), {});
    return Object.assign({}, e, t)
  }

  function L(e, t) {
    var n = Object.assign({}, t, {
      content: s(t.content, [e])
    }, t.ignoreAttributes ? {} : function(e, t) {
      return (t ? Object.keys(M(Object.assign({}, A, {
        plugins: t
      }))) : _).reduce((function(t, n) {
        var r = (e.getAttribute("data-tippy-" + n) || "").trim();
        if (!r) return t;
        if ("content" === n) t[n] = r;
        else try {
          t[n] = JSON.parse(r)
        } catch (e) {
          t[n] = r
        }
        return t
      }), {})
    }(e, t.plugins));
    return n.aria = Object.assign({}, A.aria, n.aria), n.aria = {
      expanded: "auto" === n.aria.expanded ? t.interactive : n.aria.expanded,
      content: "auto" === n.aria.content ? t.interactive ? null : "describedby" : n.aria.content
    }, n
  }

  function I(e, t) {
    e.innerHTML = t
  }

  function P(e) {
    var t = m();
    return !0 === e ? t.className = "tippy-arrow" : (t.className = "tippy-svg-arrow", g(e) ? t.appendChild(e) : I(t, e)), t
  }

  function j(e, t) {
    g(t.content) ? (I(e, ""), e.appendChild(t.content)) : "function" != typeof t.content && (t.allowHTML ? I(e, t.content) : e.textContent = t.content)
  }

  function N(e) {
    var t = e.firstElementChild,
      n = f(t.children);
    return {
      box: t,
      content: n.find((function(e) {
        return e.classList.contains("tippy-content")
      })),
      arrow: n.find((function(e) {
        return e.classList.contains("tippy-arrow") || e.classList.contains("tippy-svg-arrow")
      })),
      backdrop: n.find((function(e) {
        return e.classList.contains("tippy-backdrop")
      }))
    }
  }

  function z(e) {
    var t = m(),
      n = m();
    n.className = "tippy-box", n.setAttribute("data-state", "hidden"), n.setAttribute("tabindex", "-1");
    var r = m();

    function i(n, r) {
      var i = N(t),
        o = i.box,
        a = i.content,
        s = i.arrow;
      r.theme ? o.setAttribute("data-theme", r.theme) : o.removeAttribute("data-theme"), "string" == typeof r.animation ? o.setAttribute("data-animation", r.animation) : o.removeAttribute("data-animation"), r.inertia ? o.setAttribute("data-inertia", "") : o.removeAttribute("data-inertia"), o.style.maxWidth = "number" == typeof r.maxWidth ? r.maxWidth + "px" : r.maxWidth, r.role ? o.setAttribute("role", r.role) : o.removeAttribute("role"), n.content === r.content && n.allowHTML === r.allowHTML || j(a, e.props), r.arrow ? s ? n.arrow !== r.arrow && (o.removeChild(s), o.appendChild(P(r.arrow))) : o.appendChild(P(r.arrow)) : s && o.removeChild(s)
    }
    return r.className = "tippy-content", r.setAttribute("data-state", "hidden"), j(r, e.props), t.appendChild(n), n.appendChild(r), i(e.props, e.props), {
      popper: t,
      onUpdate: i
    }
  }
  z.$$tippy = !0;
  var R = 1,
    $ = [],
    H = [];

  function F(t, a) {
    var c, g, y, T, k, D, O, _, I = L(t, Object.assign({}, A, M(h(a)))),
      P = !1,
      j = !1,
      z = !1,
      F = !1,
      B = [],
      q = l(we, I.interactiveDebounce),
      W = R++,
      Y = (_ = I.plugins).filter((function(e, t) {
        return _.indexOf(e) === t
      })),
      U = {
        id: W,
        reference: t,
        popper: m(),
        popperInstance: null,
        props: I,
        state: {
          isEnabled: !0,
          isVisible: !1,
          isDestroyed: !1,
          isMounted: !1,
          isShown: !1
        },
        plugins: Y,
        clearDelayTimeouts: function() {
          clearTimeout(c), clearTimeout(g), cancelAnimationFrame(y)
        },
        setProps: function(e) {
          if (!U.state.isDestroyed) {
            ae("onBeforeUpdate", [U, e]), ye();
            var n = U.props,
              r = L(t, Object.assign({}, n, h(e), {
                ignoreAttributes: !0
              }));
            U.props = r, ve(), n.interactiveDebounce !== r.interactiveDebounce && (ce(), q = l(we, r.interactiveDebounce)), n.triggerTarget && !r.triggerTarget ? u(n.triggerTarget).forEach((function(e) {
              e.removeAttribute("aria-expanded")
            })) : r.triggerTarget && t.removeAttribute("aria-expanded"), le(), oe(), G && G(n, r), U.popperInstance && (Ee(), ke().forEach((function(e) {
              requestAnimationFrame(e._tippy.popperInstance.forceUpdate)
            }))), ae("onAfterUpdate", [U, e])
          }
        },
        setContent: function(e) {
          U.setProps({
            content: e
          })
        },
        show: function() {
          var e = U.state.isVisible,
            t = U.state.isDestroyed,
            n = !U.state.isEnabled,
            r = E.isTouch && !U.props.touch,
            a = o(U.props.duration, 0, A.duration);
          if (!(e || t || n || r || te().hasAttribute("disabled") || (ae("onShow", [U], !1), !1 === U.props.onShow(U)))) {
            if (U.state.isVisible = !0, ee() && (X.style.visibility = "visible"), oe(), fe(), U.state.isMounted || (X.style.transition = "none"), ee()) {
              var l = re();
              b([l.box, l.content], 0)
            }
            D = function() {
                var e;
                if (U.state.isVisible && !F) {
                  if (F = !0, X.offsetHeight, X.style.transition = U.props.moveTransition, ee() && U.props.animation) {
                    var t = re(),
                      n = t.box,
                      r = t.content;
                    b([n, r], a), w([n, r], "visible")
                  }
                  se(), le(), d(H, U), null == (e = U.popperInstance) || e.forceUpdate(), ae("onMount", [U]), U.props.animation && ee() && function(e, t) {
                    me(e, (function() {
                      U.state.isShown = !0, ae("onShown", [U])
                    }))
                  }(a)
                }
              },
              function() {
                var e, t = U.props.appendTo,
                  n = te();
                (e = U.props.interactive && t === i || "parent" === t ? n.parentNode : s(t, [n])).contains(X) || e.appendChild(X), U.state.isMounted = !0, Ee()
              }()
          }
        },
        hide: function() {
          var e = !U.state.isVisible,
            t = U.state.isDestroyed,
            n = !U.state.isEnabled,
            r = o(U.props.duration, 1, A.duration);
          if (!(e || t || n) && (ae("onHide", [U], !1), !1 !== U.props.onHide(U))) {
            if (U.state.isVisible = !1, U.state.isShown = !1, F = !1, P = !1, ee() && (X.style.visibility = "hidden"), ce(), he(), oe(!0), ee()) {
              var i = re(),
                a = i.box,
                s = i.content;
              U.props.animation && (b([a, s], r), w([a, s], "hidden"))
            }
            se(), le(), U.props.animation ? ee() && function(e, t) {
              me(e, (function() {
                !U.state.isVisible && X.parentNode && X.parentNode.contains(X) && t()
              }))
            }(r, U.unmount) : U.unmount()
          }
        },
        hideWithInteractivity: function(e) {
          ne().addEventListener("mousemove", q), d($, q), q(e)
        },
        enable: function() {
          U.state.isEnabled = !0
        },
        disable: function() {
          U.hide(), U.state.isEnabled = !1
        },
        unmount: function() {
          U.state.isVisible && U.hide(), U.state.isMounted && (Te(), ke().forEach((function(e) {
            e._tippy.unmount()
          })), X.parentNode && X.parentNode.removeChild(X), H = H.filter((function(e) {
            return e !== U
          })), U.state.isMounted = !1, ae("onHidden", [U]))
        },
        destroy: function() {
          U.state.isDestroyed || (U.clearDelayTimeouts(), U.unmount(), ye(), delete t._tippy, U.state.isDestroyed = !0, ae("onDestroy", [U]))
        }
      };
    if (!I.render) return U;
    var V = I.render(U),
      X = V.popper,
      G = V.onUpdate;
    X.setAttribute("data-tippy-root", ""), X.id = "tippy-" + U.id, U.popper = X, t._tippy = U, X._tippy = U;
    var Z = Y.map((function(e) {
        return e.fn(U)
      })),
      K = t.hasAttribute("aria-expanded");
    return ve(), le(), oe(), ae("onCreate", [U]), I.showOnCreate && De(), X.addEventListener("mouseenter", (function() {
      U.props.interactive && U.state.isVisible && U.clearDelayTimeouts()
    })), X.addEventListener("mouseleave", (function() {
      U.props.interactive && U.props.trigger.indexOf("mouseenter") >= 0 && ne().addEventListener("mousemove", q)
    })), U;

    function J() {
      var e = U.props.touch;
      return Array.isArray(e) ? e : [e, 0]
    }

    function Q() {
      return "hold" === J()[0]
    }

    function ee() {
      var e;
      return !(null == (e = U.props.render) || !e.$$tippy)
    }

    function te() {
      return O || t
    }

    function ne() {
      var e = te().parentNode;
      return e ? x(e) : document
    }

    function re() {
      return N(X)
    }

    function ie(e) {
      return U.state.isMounted && !U.state.isVisible || E.isTouch || T && "focus" === T.type ? 0 : o(U.props.delay, e ? 0 : 1, A.delay)
    }

    function oe(e) {
      void 0 === e && (e = !1), X.style.pointerEvents = U.props.interactive && !e ? "" : "none", X.style.zIndex = "" + U.props.zIndex
    }

    function ae(e, t, n) {
      var r;
      void 0 === n && (n = !0), Z.forEach((function(n) {
        n[e] && n[e].apply(n, t)
      })), n && (r = U.props)[e].apply(r, t)
    }

    function se() {
      var e = U.props.aria;
      if (e.content) {
        var n = "aria-" + e.content,
          r = X.id;
        u(U.props.triggerTarget || t).forEach((function(e) {
          var t = e.getAttribute(n);
          if (U.state.isVisible) e.setAttribute(n, t ? t + " " + r : r);
          else {
            var i = t && t.replace(r, "").trim();
            i ? e.setAttribute(n, i) : e.removeAttribute(n)
          }
        }))
      }
    }

    function le() {
      !K && U.props.aria.expanded && u(U.props.triggerTarget || t).forEach((function(e) {
        U.props.interactive ? e.setAttribute("aria-expanded", U.state.isVisible && e === te() ? "true" : "false") : e.removeAttribute("aria-expanded")
      }))
    }

    function ce() {
      ne().removeEventListener("mousemove", q), $ = $.filter((function(e) {
        return e !== q
      }))
    }

    function ue(e) {
      if (!E.isTouch || !z && "mousedown" !== e.type) {
        var n = e.composedPath && e.composedPath()[0] || e.target;
        if (!U.props.interactive || !C(X, n)) {
          if (u(U.props.triggerTarget || t).some((function(e) {
              return C(e, n)
            }))) {
            if (E.isTouch) return;
            if (U.state.isVisible && U.props.trigger.indexOf("click") >= 0) return
          } else ae("onClickOutside", [U, e]);
          !0 === U.props.hideOnClick && (U.clearDelayTimeouts(), U.hide(), j = !0, setTimeout((function() {
            j = !1
          })), U.state.isMounted || he())
        }
      }
    }

    function de() {
      z = !0
    }

    function pe() {
      z = !1
    }

    function fe() {
      var e = ne();
      e.addEventListener("mousedown", ue, !0), e.addEventListener("touchend", ue, r), e.addEventListener("touchstart", pe, r), e.addEventListener("touchmove", de, r)
    }

    function he() {
      var e = ne();
      e.removeEventListener("mousedown", ue, !0), e.removeEventListener("touchend", ue, r), e.removeEventListener("touchstart", pe, r), e.removeEventListener("touchmove", de, r)
    }

    function me(e, t) {
      var n = re().box;

      function r(e) {
        e.target === n && (S(n, "remove", r), t())
      }
      if (0 === e) return t();
      S(n, "remove", k), S(n, "add", r), k = r
    }

    function ge(e, n, r) {
      void 0 === r && (r = !1), u(U.props.triggerTarget || t).forEach((function(t) {
        t.addEventListener(e, n, r), B.push({
          node: t,
          eventType: e,
          handler: n,
          options: r
        })
      }))
    }

    function ve() {
      var e;
      Q() && (ge("touchstart", be, {
        passive: !0
      }), ge("touchend", xe, {
        passive: !0
      })), (e = U.props.trigger, e.split(/\s+/).filter(Boolean)).forEach((function(e) {
        if ("manual" !== e) switch (ge(e, be), e) {
          case "mouseenter":
            ge("mouseleave", xe);
            break;
          case "focus":
            ge(n ? "focusout" : "blur", Se);
            break;
          case "focusin":
            ge("focusout", Se)
        }
      }))
    }

    function ye() {
      B.forEach((function(e) {
        var t = e.node,
          n = e.eventType,
          r = e.handler,
          i = e.options;
        t.removeEventListener(n, r, i)
      })), B = []
    }

    function be(e) {
      var t, n = !1;
      if (U.state.isEnabled && !Ce(e) && !j) {
        var r = "focus" === (null == (t = T) ? void 0 : t.type);
        T = e, O = e.currentTarget, le(), !U.state.isVisible && v(e) && $.forEach((function(t) {
          return t(e)
        })), "click" === e.type && (U.props.trigger.indexOf("mouseenter") < 0 || P) && !1 !== U.props.hideOnClick && U.state.isVisible ? n = !0 : De(e), "click" === e.type && (P = !n), n && !r && Oe(e)
      }
    }

    function we(e) {
      var t = e.target,
        n = te().contains(t) || X.contains(t);
      "mousemove" === e.type && n || function(e, t) {
        var n = t.clientX,
          r = t.clientY;
        return e.every((function(e) {
          var t = e.popperRect,
            i = e.popperState,
            o = e.props.interactiveBorder,
            a = p(i.placement),
            s = i.modifiersData.offset;
          if (!s) return !0;
          var l = "bottom" === a ? s.top.y : 0,
            c = "top" === a ? s.bottom.y : 0,
            u = "right" === a ? s.left.x : 0,
            d = "left" === a ? s.right.x : 0,
            f = t.top - r + l > o,
            h = r - t.bottom - c > o,
            m = t.left - n + u > o,
            g = n - t.right - d > o;
          return f || h || m || g
        }))
      }(ke().concat(X).map((function(e) {
        var t, n = null == (t = e._tippy.popperInstance) ? void 0 : t.state;
        return n ? {
          popperRect: e.getBoundingClientRect(),
          popperState: n,
          props: I
        } : null
      })).filter(Boolean), e) && (ce(), Oe(e))
    }

    function xe(e) {
      Ce(e) || U.props.trigger.indexOf("click") >= 0 && P || (U.props.interactive ? U.hideWithInteractivity(e) : Oe(e))
    }

    function Se(e) {
      U.props.trigger.indexOf("focusin") < 0 && e.target !== te() || U.props.interactive && e.relatedTarget && X.contains(e.relatedTarget) || Oe(e)
    }

    function Ce(e) {
      return !!E.isTouch && Q() !== e.type.indexOf("touch") >= 0
    }

    function Ee() {
      Te();
      var n = U.props,
        r = n.popperOptions,
        i = n.placement,
        o = n.offset,
        a = n.getReferenceClientRect,
        s = n.moveTransition,
        l = ee() ? N(X).arrow : null,
        c = a ? {
          getBoundingClientRect: a,
          contextElement: a.contextElement || te()
        } : t,
        u = [{
          name: "offset",
          options: {
            offset: o
          }
        }, {
          name: "preventOverflow",
          options: {
            padding: {
              top: 2,
              bottom: 2,
              left: 5,
              right: 5
            }
          }
        }, {
          name: "flip",
          options: {
            padding: 5
          }
        }, {
          name: "computeStyles",
          options: {
            adaptive: !s
          }
        }, {
          name: "$$tippy",
          enabled: !0,
          phase: "beforeWrite",
          requires: ["computeStyles"],
          fn: function(e) {
            var t = e.state;
            if (ee()) {
              var n = re().box;
              ["placement", "reference-hidden", "escaped"].forEach((function(e) {
                "placement" === e ? n.setAttribute("data-placement", t.placement) : t.attributes.popper["data-popper-" + e] ? n.setAttribute("data-" + e, "") : n.removeAttribute("data-" + e)
              })), t.attributes.popper = {}
            }
          }
        }];
      ee() && l && u.push({
        name: "arrow",
        options: {
          element: l,
          padding: 3
        }
      }), u.push.apply(u, (null == r ? void 0 : r.modifiers) || []), U.popperInstance = e.createPopper(c, X, Object.assign({}, r, {
        placement: i,
        onFirstUpdate: D,
        modifiers: u
      }))
    }

    function Te() {
      U.popperInstance && (U.popperInstance.destroy(), U.popperInstance = null)
    }

    function ke() {
      return f(X.querySelectorAll("[data-tippy-root]"))
    }

    function De(e) {
      U.clearDelayTimeouts(), e && ae("onTrigger", [U, e]), fe();
      var t = ie(!0),
        n = J(),
        r = n[0],
        i = n[1];
      E.isTouch && "hold" === r && i && (t = i), t ? c = setTimeout((function() {
        U.show()
      }), t) : U.show()
    }

    function Oe(e) {
      if (U.clearDelayTimeouts(), ae("onUntrigger", [U, e]), U.state.isVisible) {
        if (!(U.props.trigger.indexOf("mouseenter") >= 0 && U.props.trigger.indexOf("click") >= 0 && ["mouseleave", "mousemove"].indexOf(e.type) >= 0 && P)) {
          var t = ie(!1);
          t ? g = setTimeout((function() {
            U.state.isVisible && U.hide()
          }), t) : y = requestAnimationFrame((function() {
            U.hide()
          }))
        }
      } else he()
    }
  }

  function B(e, t) {
    void 0 === t && (t = {});
    var n = A.plugins.concat(t.plugins || []);
    document.addEventListener("touchstart", k, r), window.addEventListener("blur", O);
    var i = Object.assign({}, t, {
        plugins: n
      }),
      o = function(e) {
        return g(e) ? [e] : function(e) {
          return a(e, "NodeList")
        }(e) ? f(e) : Array.isArray(e) ? e : f(document.querySelectorAll(e))
      }(e).reduce((function(e, t) {
        var n = t && F(t, i);
        return n && e.push(n), e
      }), []);
    return g(e) ? o[0] : o
  }
  B.defaultProps = A, B.setDefaultProps = function(e) {
    Object.keys(e).forEach((function(t) {
      A[t] = e[t]
    }))
  }, B.currentInput = E;
  var q = Object.assign({}, e.applyStyles, {
      effect: function(e) {
        var t = e.state,
          n = {
            popper: {
              position: t.options.strategy,
              left: "0",
              top: "0",
              margin: "0"
            },
            arrow: {
              position: "absolute"
            },
            reference: {}
          };
        Object.assign(t.elements.popper.style, n.popper), t.styles = n, t.elements.arrow && Object.assign(t.elements.arrow.style, n.arrow)
      }
    }),
    W = {
      mouseover: "mouseenter",
      focusin: "focus",
      click: "click"
    },
    Y = {
      name: "animateFill",
      defaultValue: !1,
      fn: function(e) {
        var t;
        if (null == (t = e.props.render) || !t.$$tippy) return {};
        var n = N(e.popper),
          r = n.box,
          i = n.content,
          o = e.props.animateFill ? function() {
            var e = m();
            return e.className = "tippy-backdrop", w([e], "hidden"), e
          }() : null;
        return {
          onCreate: function() {
            o && (r.insertBefore(o, r.firstElementChild), r.setAttribute("data-animatefill", ""), r.style.overflow = "hidden", e.setProps({
              arrow: !1,
              animation: "shift-away"
            }))
          },
          onMount: function() {
            if (o) {
              var e = r.style.transitionDuration,
                t = Number(e.replace("ms", ""));
              i.style.transitionDelay = Math.round(t / 10) + "ms", o.style.transitionDuration = e, w([o], "visible")
            }
          },
          onShow: function() {
            o && (o.style.transitionDuration = "0ms")
          },
          onHide: function() {
            o && w([o], "hidden")
          }
        }
      }
    },
    U = {
      clientX: 0,
      clientY: 0
    },
    V = [];

  function X(e) {
    var t = e.clientX,
      n = e.clientY;
    U = {
      clientX: t,
      clientY: n
    }
  }
  var G = {
      name: "followCursor",
      defaultValue: !1,
      fn: function(e) {
        var t = e.reference,
          n = x(e.props.triggerTarget || t),
          r = !1,
          i = !1,
          o = !0,
          a = e.props;

        function s() {
          return "initial" === e.props.followCursor && e.state.isVisible
        }

        function l() {
          n.addEventListener("mousemove", d)
        }

        function c() {
          n.removeEventListener("mousemove", d)
        }

        function u() {
          r = !0, e.setProps({
            getReferenceClientRect: null
          }), r = !1
        }

        function d(n) {
          var r = !n.target || t.contains(n.target),
            i = e.props.followCursor,
            o = n.clientX,
            a = n.clientY,
            s = t.getBoundingClientRect(),
            l = o - s.left,
            c = a - s.top;
          !r && e.props.interactive || e.setProps({
            getReferenceClientRect: function() {
              var e = t.getBoundingClientRect(),
                n = o,
                r = a;
              "initial" === i && (n = e.left + l, r = e.top + c);
              var s = "horizontal" === i ? e.top : r,
                u = "vertical" === i ? e.right : n,
                d = "horizontal" === i ? e.bottom : r,
                p = "vertical" === i ? e.left : n;
              return {
                width: u - p,
                height: d - s,
                top: s,
                right: u,
                bottom: d,
                left: p
              }
            }
          })
        }

        function p() {
          e.props.followCursor && (V.push({
            instance: e,
            doc: n
          }), function(e) {
            e.addEventListener("mousemove", X)
          }(n))
        }

        function f() {
          0 === (V = V.filter((function(t) {
            return t.instance !== e
          }))).filter((function(e) {
            return e.doc === n
          })).length && function(e) {
            e.removeEventListener("mousemove", X)
          }(n)
        }
        return {
          onCreate: p,
          onDestroy: f,
          onBeforeUpdate: function() {
            a = e.props
          },
          onAfterUpdate: function(t, n) {
            var o = n.followCursor;
            r || void 0 !== o && a.followCursor !== o && (f(), o ? (p(), !e.state.isMounted || i || s() || l()) : (c(), u()))
          },
          onMount: function() {
            e.props.followCursor && !i && (o && (d(U), o = !1), s() || l())
          },
          onTrigger: function(e, t) {
            v(t) && (U = {
              clientX: t.clientX,
              clientY: t.clientY
            }), i = "focus" === t.type
          },
          onHidden: function() {
            e.props.followCursor && (u(), c(), o = !0)
          }
        }
      }
    },
    Z = {
      name: "inlinePositioning",
      defaultValue: !1,
      fn: function(e) {
        var t, n = e.reference,
          r = -1,
          i = !1,
          o = [],
          a = {
            name: "tippyInlinePositioning",
            enabled: !0,
            phase: "afterWrite",
            fn: function(i) {
              var a = i.state;
              e.props.inlinePositioning && (-1 !== o.indexOf(a.placement) && (o = []), t !== a.placement && -1 === o.indexOf(a.placement) && (o.push(a.placement), e.setProps({
                getReferenceClientRect: function() {
                  return function(e) {
                    return function(e, t, n, r) {
                      if (n.length < 2 || null === e) return t;
                      if (2 === n.length && r >= 0 && n[0].left > n[1].right) return n[r] || t;
                      switch (e) {
                        case "top":
                        case "bottom":
                          var i = n[0],
                            o = n[n.length - 1],
                            a = "top" === e,
                            s = i.top,
                            l = o.bottom,
                            c = a ? i.left : o.left,
                            u = a ? i.right : o.right;
                          return {
                            top: s, bottom: l, left: c, right: u, width: u - c, height: l - s
                          };
                        case "left":
                        case "right":
                          var d = Math.min.apply(Math, n.map((function(e) {
                              return e.left
                            }))),
                            p = Math.max.apply(Math, n.map((function(e) {
                              return e.right
                            }))),
                            f = n.filter((function(t) {
                              return "left" === e ? t.left === d : t.right === p
                            })),
                            h = f[0].top,
                            m = f[f.length - 1].bottom;
                          return {
                            top: h, bottom: m, left: d, right: p, width: p - d, height: m - h
                          };
                        default:
                          return t
                      }
                    }(p(e), n.getBoundingClientRect(), f(n.getClientRects()), r)
                  }(a.placement)
                }
              })), t = a.placement)
            }
          };

        function s() {
          var t;
          i || (t = function(e, t) {
            var n;
            return {
              popperOptions: Object.assign({}, e.popperOptions, {
                modifiers: [].concat(((null == (n = e.popperOptions) ? void 0 : n.modifiers) || []).filter((function(e) {
                  return e.name !== t.name
                })), [t])
              })
            }
          }(e.props, a), i = !0, e.setProps(t), i = !1)
        }
        return {
          onCreate: s,
          onAfterUpdate: s,
          onTrigger: function(t, n) {
            if (v(n)) {
              var i = f(e.reference.getClientRects()),
                o = i.find((function(e) {
                  return e.left - 2 <= n.clientX && e.right + 2 >= n.clientX && e.top - 2 <= n.clientY && e.bottom + 2 >= n.clientY
                })),
                a = i.indexOf(o);
              r = a > -1 ? a : r
            }
          },
          onHidden: function() {
            r = -1
          }
        }
      }
    },
    K = {
      name: "sticky",
      defaultValue: !1,
      fn: function(e) {
        var t = e.reference,
          n = e.popper;

        function r(t) {
          return !0 === e.props.sticky || e.props.sticky === t
        }
        var i = null,
          o = null;

        function a() {
          var s = r("reference") ? (e.popperInstance ? e.popperInstance.state.elements.reference : t).getBoundingClientRect() : null,
            l = r("popper") ? n.getBoundingClientRect() : null;
          (s && J(i, s) || l && J(o, l)) && e.popperInstance && e.popperInstance.update(), i = s, o = l, e.state.isMounted && requestAnimationFrame(a)
        }
        return {
          onMount: function() {
            e.props.sticky && a()
          }
        }
      }
    };

  function J(e, t) {
    return !e || !t || e.top !== t.top || e.right !== t.right || e.bottom !== t.bottom || e.left !== t.left
  }
  return t && function(e) {
    var t = document.createElement("style");
    t.textContent = '.tippy-box[data-animation=fade][data-state=hidden]{opacity:0}[data-tippy-root]{max-width:calc(100vw - 10px)}.tippy-box{position:relative;background-color:#333;color:#fff;border-radius:4px;font-size:14px;line-height:1.4;white-space:normal;outline:0;transition-property:transform,visibility,opacity}.tippy-box[data-placement^=top]>.tippy-arrow{bottom:0}.tippy-box[data-placement^=top]>.tippy-arrow:before{bottom:-7px;left:0;border-width:8px 8px 0;border-top-color:initial;transform-origin:center top}.tippy-box[data-placement^=bottom]>.tippy-arrow{top:0}.tippy-box[data-placement^=bottom]>.tippy-arrow:before{top:-7px;left:0;border-width:0 8px 8px;border-bottom-color:initial;transform-origin:center bottom}.tippy-box[data-placement^=left]>.tippy-arrow{right:0}.tippy-box[data-placement^=left]>.tippy-arrow:before{border-width:8px 0 8px 8px;border-left-color:initial;right:-7px;transform-origin:center left}.tippy-box[data-placement^=right]>.tippy-arrow{left:0}.tippy-box[data-placement^=right]>.tippy-arrow:before{left:-7px;border-width:8px 8px 8px 0;border-right-color:initial;transform-origin:center right}.tippy-box[data-inertia][data-state=visible]{transition-timing-function:cubic-bezier(.54,1.5,.38,1.11)}.tippy-arrow{width:16px;height:16px;color:#333}.tippy-arrow:before{content:"";position:absolute;border-color:transparent;border-style:solid}.tippy-content{position:relative;padding:5px 9px;z-index:1}', t.setAttribute("data-tippy-stylesheet", "");
    var n = document.head,
      r = document.querySelector("head>style,head>link");
    r ? n.insertBefore(t, r) : n.appendChild(t)
  }(), B.setDefaultProps({
    plugins: [Y, G, Z, K],
    render: z
  }), B.createSingleton = function(e, t) {
    var n;
    void 0 === t && (t = {});
    var r, i = e,
      o = [],
      a = [],
      s = t.overrides,
      l = [],
      d = !1;

    function p() {
      a = i.map((function(e) {
        return u(e.props.triggerTarget || e.reference)
      })).reduce((function(e, t) {
        return e.concat(t)
      }), [])
    }

    function f() {
      o = i.map((function(e) {
        return e.reference
      }))
    }

    function h(e) {
      i.forEach((function(t) {
        e ? t.enable() : t.disable()
      }))
    }

    function g(e) {
      return i.map((function(t) {
        var n = t.setProps;
        return t.setProps = function(i) {
            n(i), t.reference === r && e.setProps(i)
          },
          function() {
            t.setProps = n
          }
      }))
    }

    function v(e, t) {
      var n = a.indexOf(t);
      if (t !== r) {
        r = t;
        var l = (s || []).concat("content").reduce((function(e, t) {
          return e[t] = i[n].props[t], e
        }), {});
        e.setProps(Object.assign({}, l, {
          getReferenceClientRect: "function" == typeof l.getReferenceClientRect ? l.getReferenceClientRect : function() {
            var e;
            return null == (e = o[n]) ? void 0 : e.getBoundingClientRect()
          }
        }))
      }
    }
    h(!1), f(), p();
    var y = {
        fn: function() {
          return {
            onDestroy: function() {
              h(!0)
            },
            onHidden: function() {
              r = null
            },
            onClickOutside: function(e) {
              e.props.showOnCreate && !d && (d = !0, r = null)
            },
            onShow: function(e) {
              e.props.showOnCreate && !d && (d = !0, v(e, o[0]))
            },
            onTrigger: function(e, t) {
              v(e, t.currentTarget)
            }
          }
        }
      },
      b = B(m(), Object.assign({}, c(t, ["overrides"]), {
        plugins: [y].concat(t.plugins || []),
        triggerTarget: a,
        popperOptions: Object.assign({}, t.popperOptions, {
          modifiers: [].concat((null == (n = t.popperOptions) ? void 0 : n.modifiers) || [], [q])
        })
      })),
      w = b.show;
    b.show = function(e) {
      if (w(), !r && null == e) return v(b, o[0]);
      if (!r || null != e) {
        if ("number" == typeof e) return o[e] && v(b, o[e]);
        if (i.indexOf(e) >= 0) {
          var t = e.reference;
          return v(b, t)
        }
        return o.indexOf(e) >= 0 ? v(b, e) : void 0
      }
    }, b.showNext = function() {
      var e = o[0];
      if (!r) return b.show(0);
      var t = o.indexOf(r);
      b.show(o[t + 1] || e)
    }, b.showPrevious = function() {
      var e = o[o.length - 1];
      if (!r) return b.show(e);
      var t = o.indexOf(r),
        n = o[t - 1] || e;
      b.show(n)
    };
    var x = b.setProps;
    return b.setProps = function(e) {
      s = e.overrides || s, x(e)
    }, b.setInstances = function(e) {
      h(!0), l.forEach((function(e) {
        return e()
      })), i = e, h(!1), f(), p(), l = g(b), b.setProps({
        triggerTarget: a
      })
    }, l = g(b), b
  }, B.delegate = function(e, t) {
    var n = [],
      i = [],
      o = !1,
      a = t.target,
      s = c(t, ["target"]),
      l = Object.assign({}, s, {
        trigger: "manual",
        touch: !1
      }),
      d = Object.assign({
        touch: A.touch
      }, s, {
        showOnCreate: !0
      }),
      p = B(e, l);

    function f(e) {
      if (e.target && !o) {
        var n = e.target.closest(a);
        if (n) {
          var r = n.getAttribute("data-tippy-trigger") || t.trigger || A.trigger;
          if (!n._tippy && !("touchstart" === e.type && "boolean" == typeof d.touch || "touchstart" !== e.type && r.indexOf(W[e.type]) < 0)) {
            var s = B(n, d);
            s && (i = i.concat(s))
          }
        }
      }
    }

    function h(e, t, r, i) {
      void 0 === i && (i = !1), e.addEventListener(t, r, i), n.push({
        node: e,
        eventType: t,
        handler: r,
        options: i
      })
    }
    return u(p).forEach((function(e) {
      var t = e.destroy,
        a = e.enable,
        s = e.disable;
      e.destroy = function(e) {
          void 0 === e && (e = !0), e && i.forEach((function(e) {
            e.destroy()
          })), i = [], n.forEach((function(e) {
            var t = e.node,
              n = e.eventType,
              r = e.handler,
              i = e.options;
            t.removeEventListener(n, r, i)
          })), n = [], t()
        }, e.enable = function() {
          a(), i.forEach((function(e) {
            return e.enable()
          })), o = !1
        }, e.disable = function() {
          s(), i.forEach((function(e) {
            return e.disable()
          })), o = !0
        },
        function(e) {
          var t = e.reference;
          h(t, "touchstart", f, r), h(t, "mouseover", f), h(t, "focusin", f), h(t, "click", f)
        }(e)
    })), p
  }, B.hideAll = function(e) {
    var t = void 0 === e ? {} : e,
      n = t.exclude,
      r = t.duration;
    H.forEach((function(e) {
      var t = !1;
      if (n && (t = y(n) ? e.reference === n : e.popper === n.popper), !t) {
        var i = e.props.duration;
        e.setProps({
          duration: r
        }), e.hide(), e.state.isDestroyed || e.setProps({
          duration: i
        })
      }
    }))
  }, B.roundArrow = '<svg width="16" height="6" xmlns="http://www.w3.org/2000/svg"><path d="M0 6s1.796-.013 4.67-3.615C5.851.9 6.93.006 8 0c1.07-.006 2.148.887 3.343 2.385C14.233 6.005 16 6 16 6H0z"></svg>', B
}));
const defaults = {
  threshold: 50,
  passive: !1
};
class Xwiper {
  constructor(e, t = {}) {
    this.options = {
      ...defaults,
      ...t
    }, this.element = null, this.touchStartX = 0, this.touchStartY = 0, this.touchEndX = 0, this.touchEndY = 0, this.onSwipeLeftAgent = null, this.onSwipeRightAgent = null, this.onSwipeUpAgent = null, this.onSwipeDownAgent = null, this.onTapAgent = null, this.onTouchStart = this.onTouchStart.bind(this), this.onTouchEnd = this.onTouchEnd.bind(this), this.onSwipeLeft = this.onSwipeLeft.bind(this), this.onSwipeRight = this.onSwipeRight.bind(this), this.onSwipeUp = this.onSwipeUp.bind(this), this.onSwipeDown = this.onSwipeDown.bind(this), this.onTap = this.onTap.bind(this), this.destroy = this.destroy.bind(this), this.handleGesture = this.handleGesture.bind(this);
    let n = !!this.options.passive && {
      passive: !0
    };
    this.element = e instanceof EventTarget ? e : document.querySelector(e), this.element.addEventListener("touchstart", this.onTouchStart, n), this.element.addEventListener("touchend", this.onTouchEnd, n)
  }
  onTouchStart(e) {
    this.touchStartX = e.changedTouches[0].screenX, this.touchStartY = e.changedTouches[0].screenY
  }
  onTouchEnd(e) {
    this.touchEndX = e.changedTouches[0].screenX, this.touchEndY = e.changedTouches[0].screenY, this.handleGesture()
  }
  onSwipeLeft(e) {
    this.onSwipeLeftAgent = e
  }
  onSwipeRight(e) {
    this.onSwipeRightAgent = e
  }
  onSwipeUp(e) {
    this.onSwipeUpAgent = e
  }
  onSwipeDown(e) {
    this.onSwipeDownAgent = e
  }
  onTap(e) {
    this.onTapAgent = e
  }
  destroy() {
    this.element.removeEventListener("touchstart", this.onTouchStart), this.element.removeEventListener("touchend", this.onTouchEnd)
  }
  handleGesture() {
    return this.touchEndX + this.options.threshold <= this.touchStartX ? (this.onSwipeLeftAgent && this.onSwipeLeftAgent(), "swiped left") : this.touchEndX - this.options.threshold >= this.touchStartX ? (this.onSwipeRightAgent && this.onSwipeRightAgent(), "swiped right") : this.touchEndY + this.options.threshold <= this.touchStartY ? (this.onSwipeUpAgent && this.onSwipeUpAgent(), "swiped up") : this.touchEndY - this.options.threshold >= this.touchStartY ? (this.onSwipeDownAgent && this.onSwipeDownAgent(), "swiped down") : this.touchEndY === this.touchStartY ? (this.onTapAgent && this.onTapAgent(), "tap") : void 0
  }
}! function(e) {
  let t = {},
    n = 0;
  e.fn.once = function(r, i) {
    "string" != typeof r && (r in t || (t[r] = ++n), i || (i = r), r = "jquery-once-" + t[r]);
    let o = r + "-processed",
      a = this.not("." + o).addClass(o);
    return e.isFunction(i) ? a.each(i) : a
  }
}(jQuery),
function(e) {
  const t = () => {
    document.documentElement.style.setProperty("--app-height", `${window.innerHeight}px`)
  };
  window.addEventListener("resize", t), t();
  let n = function() {
    return e(window).width() <= 1440
  };

  function r() {
    e("[data-scrollbar]").once("scrollbar", (function() {
      new SimpleBar(this)
    })), e("[data-modal-link]").once("modal-link").click((function(t) {
      t.preventDefault();
      let n = e(this).attr("data-modal-link"),
        r = e("[data-modal=" + n + "]"),
        i = r.attr("data-modal-width") || null;
      0 !== r.length && e.magnificPopup.open({
        items: {
          src: r[0]
        },
        type: "inline",
        mainClass: e(this).attr("data-modal") + "-modal mfp-fade",
        closeOnBgClick: !1,
        showCloseBtn: !0,
        callbacks: {
          open: function() {
            i && e(this.container).find(".mfp-content").css("width", i + "px")
          }
        },
        removalDelay: 300
      })
    })), e("[data-modal-close]").once("modal-close").click((function(t) {
      t.preventDefault(), e.magnificPopup.close()
    })), e("[data-datepicker]").once().flatpickr({
      locale: "ru",
      dateFormat: "d.m.Y",
      disableMobile: "true"
    }), e("[data-timemask]").once((function() {
      new Cleave(this, {
        time: !0,
        timePattern: ["h", "m"]
      })
    })), e(".switch").once("switch", (function() {
      let t = e(this),
        n = t.find("a").length;
      t.css("grid-template-columns", "repeat(" + n + ", minmax(0, 1fr))")
    })), e(".form-group select").once().on("select2:open", (function(t) {
      setTimeout((() => {
        e(".select2-results__options").once().niceScroll({
          cursorcolor: "#0E7ABC",
          cursorwidth: "4px",
          railpadding: {
            top: 4,
            right: 0,
            left: 0,
            bottom: 4
          },
          cursoropacitymin: .2,
          cursoropacitymax: .6
        })
      }), 0)
    })).each((function() {
      e(this).select2({
        dropdownParent: ".dropdown-wrapper"
      })
    })), e(".table").once().on("table", (function() {
      let t = e(this),
        r = t.find(".tr");
      n() ? r.css("grid-template-columns", t.attr("data-columns-mobile")) : r.css("grid-template-columns", t.attr("data-columns")), t.show()
    })).trigger("table"), e(".tabs a").once("tabs").click((function(t) {
      t.preventDefault();
      let n = e(this);
      n.closest(".tabs").find("a").each((function() {
        let t = e(this);
        t.removeClass("active"), e('[data-tab-content="' + t.attr("data-tab") + '"]').removeClass("active")
      })), n.addClass("active"), e('[data-tab-content="' + n.attr("data-tab") + '"]').addClass("active")
    })), e(".eat-menu-block .menu a").once("tabs").click((function(t) {
      t.preventDefault();
      let n = e(this);
      n.closest(".menu").find("a").each((function() {
        let t = e(this);
        t.removeClass("active"), e('[data-eat-menu-tab-content="' + t.attr("data-tab") + '"]').removeClass("active")
      })), n.addClass("active"), e('[data-eat-menu-tab-content="' + n.attr("data-tab") + '"]').addClass("active")
    })), e("[data-fade-toggle-link]").once().click((function(t) {
      t.preventDefault();
      let n = e(this).attr("data-fade-toggle-link");
      e('[data-fade-toggle="' + n + '"]').stop().fadeToggle("fast")
    })), e("[data-eat-choose-grid] [data-toggle]").once("toggle-mobile").click((function(t) {
      t.preventDefault();
      let n = e(this).closest("[data-item]"),
        r = n.attr("data-item");
      e(window).width() <= 960 ? e('[data-eat-bottom-sheet="' + r + '"]').closest("[data-bottom-sheet]").addClass("open") : n.toggleClass("open")
    })), e("[data-eat-choose-grid] [data-choose]").once().on("choose", (function(t) {
      t.preventDefault();
      let n = e(this),
        r = n.closest("[data-item]"),
        i = n.closest("[data-eat-choose-grid]"),
        o = r.attr("data-item"),
        a = e('[data-eat-bottom-sheet="' + o + '"]');
      i.find("[data-item]").removeClass("active").each((function() {
        let t = e(this).attr("data-item");
        e('[data-eat-bottom-sheet="' + t + '"]').removeClass("active")
      })), r.addClass("active"), a.addClass("active")

      addHtmlDinner();
      addHtmlLunch();

    })).click((function(t) {
      t.preventDefault(), e(this).trigger("choose")
    })), e("[data-eat-bottom-sheet] [data-choose]").once().click((function(t) {
      t.preventDefault();
      let n = e(this).closest("[data-eat-bottom-sheet]").attr("data-eat-bottom-sheet");
      e('[data-eat-choose-grid] [data-item="' + n + '"]').find("[data-choose]").first().trigger("choose")
    })), e("[data-eat-history-grid] [data-toggle]").once().click((function(t) {
      t.preventDefault(), e(this).closest(".item").toggleClass("open")
    })), e(".review-form .item-rating").once().on("update", (function(t, n) {
      if (0 === (n = n ?? 0)) return;
      let r = e(this).find(".star");
      r.removeClass("active");
      for (let e = 1; e <= n; e++) r.filter('[data-value="' + e + '"]').addClass("active")
    })).each((function() {
      let t = e(this),
        n = t.closest("form").find('input[name="rating"]').val();
      t.trigger("update", [n])
    })).find(".star").on("update", (function() {
      let t = e(this);
      t.closest(".item-rating").trigger("update", [t.attr("data-value")])
    })).hover((function() {
      let t = e(this);
      t.closest(".item-rating").addClass("hover"), t.trigger("update")
    }), (function() {
      let t = e(this),
        n = t.closest(".item-rating"),
        r = t.closest("form").find('input[name="rating"]').val();
      n.removeClass("hover"), e(this).trigger("update", [r])
    })).click((function(t) {
      t.preventDefault();
      let n = e(this),
        r = n.closest(".item-rating"),
        i = n.closest("form");
      r.removeClass("hover"), i.find('input[name="rating"]').val(n.attr("data-value"))
    })), e("[data-sidebar-toggle]").once().click((function(t) {
      t.preventDefault(), e("body").toggleClass("sidebar-visible")
    })), e(".table .tr[data-patient-card-show]").once("patient-card-toggle").click((function() {
      let t = e(this);
      t.closest(".table").find(".tr").removeClass("active"), t.addClass("active"), e("body").addClass("patient-card-visible")
    })), e("[data-patient-card-toggle]").once().click((function() {
      e("body").toggleClass("patient-card-visible")
    })), e("[data-order-toggle]").once().click((function() {
      e("body").toggleClass("order-visible")
    })), e("[data-bottom-sheet-link]").once("bottom-sheet-link").click((function() {
      let t = e(this).attr("data-bottom-sheet-link");
      e('[data-bottom-sheet="' + t + '"]').addClass("open")
    })), e("[data-bottom-sheet]").find(".overlay, .toggle").once("close").click((function(t) {
      e(this).closest("[data-bottom-sheet]").removeClass("open")
    })), e("[data-tooltip]").once("tooltip", (function() {
      let t = e(this).attr("data-tooltip");
      tippy(this, {
        content: t,
        placement: "bottom-start",
        arrow: !0,
        arrowType: "round"
      })
    })), e(".report-block .main").once("responsive").on("responsiveUpdate", (function() {
      let t = e(this),
        r = t.find(".tr").first().outerWidth(),
        i = t.find(".head, .body");
      n() ? i.css("width", r + "px") : i.css("width", "auto")
    })).trigger("responsiveUpdate"), e("[data-bottom-sheet]").once("swipe-close", (function() {
      let t = e(this);
      new Xwiper(this).onSwipeDown((function() {
        t.closest("[data-bottom-sheet]").removeClass("open")
      }))
    })), e(".report-block .tags .more").once().click((function() {
      e(this).closest(".tags").toggleClass("open")
    })), e(".card-header-block .input-controls").find(".minus, .plus").once().click((function(t) {
      t.preventDefault();
      let n = e(this),
        r = n.closest(".input-controls").find('input[type="text"]'),
        i = parseInt(r.val() || 0);
      n.hasClass("plus") ? i++ : i--, i < 1 && (i = 1), r.val(i)
    })), e(".card-block .table .tr.parent > .td").once().click((function() {
      e(this).closest(".tr").toggleClass("open")
    })), e(".card-block .card-detail .toggle").once("toggle").click((function(t) {
      t.preventDefault();
      let n = e(this).closest(".card-detail"),
        r = n.find(".content");
      n.toggleClass("open"), r.stop().slideToggle("fast")
    }))
  }
  e(window).resize((function() {
    e(".report-block .main").trigger("responsiveUpdate")
  })), e(document).click((function(t) {
    let n = "[data-fade-toggle]",
      r = e(t.target);
    r.closest(n).length || !e(n).is(":visible") || r.closest("[data-fade-toggle-link]").length || r.filter("[data-fade-toggle-link]").length || e(n).fadeOut("fast")
  })), e(window).resize((function() {
    e(".table").trigger("table")
  })), e(document).ready((function() {
    r()
  })), e(document).ajaxComplete((function() {
    r()
  }))
}(jQuery);






  // для работы просмотра выбора пациента в ЛК врача
$('.switch a')
.once('switch')
.click(function(e) {
  e.preventDefault();

  let $this = $(this);

  $this
    .closest('.switch')
    .find('a')
    .each(function() {
      let item = $(this);

      item.removeClass('active');

      $('[data-tab-content="' + item.attr('data-tab') + '"]').removeClass('active');
    });

  $this.addClass('active');

  $('[data-tab-content="' + $this.attr('data-tab') + '"]').addClass('active');
});

function addHtmlDinner() {
  let products = document.querySelectorAll('#dinner>.eat-choose-block>.eat-choose-grid>.active>.info>.name')
  item = document.getElementById('dinner-rigth')
  while (item.firstChild) {
      item.removeChild(item.firstChild);
  }
  result = '';
  result += '<div class="title">Ужин</div>'
  for (var index = 0; index < products.length; index++ ) {
      result += '<div class="item"><div class="name">' + products[index].innerText + '</div></div>'
  }
  result += '</div>'
  item.insertAdjacentHTML("beforeend", result);
}

function addHtmlLunch() {
  let products = document.querySelectorAll('#lunch>.eat-choose-block>.eat-choose-grid>.active>.info>.name')
  item = document.getElementById('lunch-rigth')
  while (item.firstChild) {
      item.removeChild(item.firstChild);
  }
  result = '';
  result += '<div class="title">Обед</div>'
  for (var index = 0; index < products.length; index++ ) {
      result += '<div class="item"><div class="name">' + products[index].innerText + '</div></div>'
  }
  result += '</div>'
  item.insertAdjacentHTML("beforeend", result);
}


//  делаем нужную ссылку визуально активной
// function funonload() {
//   var page = document.getElementById('page')
//   document.getElementById(page.innerHTML).classList.add('active');
//   var list6 = document.getElementById('status').innerHTML
//   document.getElementById(list6).click();
// }
// window.onload = funonload;

function funonload() {
var page = document.getElementById('page')
document.getElementById(page.innerHTML).classList.add('active');
var messages = document.getElementsByClassName('messages')
if (messages.length != 0) {
  var link = document.getElementById(messages[0].value)
  link.click();
}

}
window.onload = funonload;