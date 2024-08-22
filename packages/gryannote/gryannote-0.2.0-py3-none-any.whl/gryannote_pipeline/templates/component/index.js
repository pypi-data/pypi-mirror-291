function sl() {
}
function wn(t, l) {
  return t != t ? l == l : t !== l || t && typeof t == "object" || typeof t == "function";
}
function Jl(t) {
  const l = typeof t == "string" && t.match(/^\s*(-?[\d.]+)([^\s]*)\s*$/);
  return l ? [parseFloat(l[1]), l[2] || "px"] : [
    /** @type {number} */
    t,
    "px"
  ];
}
const Jt = typeof window < "u";
let Rl = Jt ? () => window.performance.now() : () => Date.now(), Rt = Jt ? (t) => requestAnimationFrame(t) : sl;
const Ie = /* @__PURE__ */ new Set();
function Xt(t) {
  Ie.forEach((l) => {
    l.c(t) || (Ie.delete(l), l.f());
  }), Ie.size !== 0 && Rt(Xt);
}
function pn(t) {
  let l;
  return Ie.size === 0 && Rt(Xt), {
    promise: new Promise((e) => {
      Ie.add(l = { c: t, f: e });
    }),
    abort() {
      Ie.delete(l);
    }
  };
}
function kn(t) {
  const l = t - 1;
  return l * l * l + 1;
}
function Xl(t, { delay: l = 0, duration: e = 400, easing: n = kn, x: i = 0, y: f = 0, opacity: u = 0 } = {}) {
  const o = getComputedStyle(t), s = +o.opacity, r = o.transform === "none" ? "" : o.transform, a = s * (1 - u), [m, w] = Jl(i), [p, q] = Jl(f);
  return {
    delay: l,
    duration: e,
    easing: n,
    css: (k, d) => `
			transform: ${r} translate(${(1 - k) * m}${w}, ${(1 - k) * p}${q});
			opacity: ${s - a * d}`
  };
}
const Le = [];
function yn(t, l = sl) {
  let e;
  const n = /* @__PURE__ */ new Set();
  function i(o) {
    if (wn(t, o) && (t = o, e)) {
      const s = !Le.length;
      for (const r of n)
        r[1](), Le.push(r, t);
      if (s) {
        for (let r = 0; r < Le.length; r += 2)
          Le[r][0](Le[r + 1]);
        Le.length = 0;
      }
    }
  }
  function f(o) {
    i(o(t));
  }
  function u(o, s = sl) {
    const r = [o, s];
    return n.add(r), n.size === 1 && (e = l(i, f) || sl), o(t), () => {
      n.delete(r), n.size === 0 && e && (e(), e = null);
    };
  }
  return { set: i, update: f, subscribe: u };
}
function Yl(t) {
  return Object.prototype.toString.call(t) === "[object Date]";
}
function Nl(t, l, e, n) {
  if (typeof e == "number" || Yl(e)) {
    const i = n - e, f = (e - l) / (t.dt || 1 / 60), u = t.opts.stiffness * i, o = t.opts.damping * f, s = (u - o) * t.inv_mass, r = (f + s) * t.dt;
    return Math.abs(r) < t.opts.precision && Math.abs(i) < t.opts.precision ? n : (t.settled = !1, Yl(e) ? new Date(e.getTime() + r) : e + r);
  } else {
    if (Array.isArray(e))
      return e.map(
        (i, f) => Nl(t, l[f], e[f], n[f])
      );
    if (typeof e == "object") {
      const i = {};
      for (const f in e)
        i[f] = Nl(t, l[f], e[f], n[f]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof e} values`);
  }
}
function Gl(t, l = {}) {
  const e = yn(t), { stiffness: n = 0.15, damping: i = 0.8, precision: f = 0.01 } = l;
  let u, o, s, r = t, a = t, m = 1, w = 0, p = !1;
  function q(d, _ = {}) {
    a = d;
    const g = s = {};
    return t == null || _.hard || k.stiffness >= 1 && k.damping >= 1 ? (p = !0, u = Rl(), r = d, e.set(t = a), Promise.resolve()) : (_.soft && (w = 1 / ((_.soft === !0 ? 0.5 : +_.soft) * 60), m = 0), o || (u = Rl(), p = !1, o = pn((c) => {
      if (p)
        return p = !1, o = null, !1;
      m = Math.min(m + w, 1);
      const h = {
        inv_mass: m,
        opts: k,
        settled: !0,
        dt: (c - u) * 60 / 1e3
      }, S = Nl(h, r, t, a);
      return u = c, r = t, e.set(t = S), h.settled && (o = null), !h.settled;
    })), new Promise((c) => {
      o.promise.then(() => {
        g === s && c();
      });
    }));
  }
  const k = {
    set: q,
    update: (d, _) => q(d(a, t), _),
    subscribe: e.subscribe,
    stiffness: n,
    damping: i,
    precision: f
  };
  return k;
}
const {
  SvelteComponent: vn,
  add_render_callback: Yt,
  append: tl,
  attr: $,
  binding_callbacks: Kl,
  check_outros: Cn,
  create_bidirectional_transition: Ql,
  destroy_each: jn,
  detach: Ke,
  element: rl,
  empty: qn,
  ensure_array_like: Wl,
  group_outros: Sn,
  init: En,
  insert: Qe,
  listen: Fl,
  prevent_default: Nn,
  run_all: Fn,
  safe_not_equal: Ln,
  set_data: zn,
  set_style: Ce,
  space: Ll,
  text: Mn,
  toggle_class: oe,
  transition_in: vl,
  transition_out: xl
} = window.__gradio__svelte__internal, { createEventDispatcher: On } = window.__gradio__svelte__internal;
function $l(t, l, e) {
  const n = t.slice();
  return n[26] = l[e], n;
}
function et(t) {
  let l, e, n, i, f, u = Wl(
    /*filtered_indices*/
    t[1]
  ), o = [];
  for (let s = 0; s < u.length; s += 1)
    o[s] = lt($l(t, u, s));
  return {
    c() {
      l = rl("ul");
      for (let s = 0; s < o.length; s += 1)
        o[s].c();
      $(l, "class", "options svelte-yuohum"), $(l, "role", "listbox"), Ce(
        l,
        "top",
        /*top*/
        t[9]
      ), Ce(
        l,
        "bottom",
        /*bottom*/
        t[10]
      ), Ce(l, "max-height", `calc(${/*max_height*/
      t[11]}px - var(--window-padding))`), Ce(
        l,
        "width",
        /*input_width*/
        t[8] + "px"
      );
    },
    m(s, r) {
      Qe(s, l, r);
      for (let a = 0; a < o.length; a += 1)
        o[a] && o[a].m(l, null);
      t[23](l), n = !0, i || (f = Fl(l, "mousedown", Nn(
        /*mousedown_handler*/
        t[22]
      )), i = !0);
    },
    p(s, r) {
      if (r & /*filtered_indices, choices, selected_indices, active_index*/
      51) {
        u = Wl(
          /*filtered_indices*/
          s[1]
        );
        let a;
        for (a = 0; a < u.length; a += 1) {
          const m = $l(s, u, a);
          o[a] ? o[a].p(m, r) : (o[a] = lt(m), o[a].c(), o[a].m(l, null));
        }
        for (; a < o.length; a += 1)
          o[a].d(1);
        o.length = u.length;
      }
      r & /*top*/
      512 && Ce(
        l,
        "top",
        /*top*/
        s[9]
      ), r & /*bottom*/
      1024 && Ce(
        l,
        "bottom",
        /*bottom*/
        s[10]
      ), r & /*max_height*/
      2048 && Ce(l, "max-height", `calc(${/*max_height*/
      s[11]}px - var(--window-padding))`), r & /*input_width*/
      256 && Ce(
        l,
        "width",
        /*input_width*/
        s[8] + "px"
      );
    },
    i(s) {
      n || (s && Yt(() => {
        n && (e || (e = Ql(l, Xl, { duration: 200, y: 5 }, !0)), e.run(1));
      }), n = !0);
    },
    o(s) {
      s && (e || (e = Ql(l, Xl, { duration: 200, y: 5 }, !1)), e.run(0)), n = !1;
    },
    d(s) {
      s && Ke(l), jn(o, s), t[23](null), s && e && e.end(), i = !1, f();
    }
  };
}
function lt(t) {
  let l, e, n, i = (
    /*choices*/
    t[0][
      /*index*/
      t[26]
    ][0] + ""
  ), f, u, o, s, r;
  return {
    c() {
      l = rl("li"), e = rl("span"), e.textContent = "✓", n = Ll(), f = Mn(i), u = Ll(), $(e, "class", "inner-item svelte-yuohum"), oe(e, "hide", !/*selected_indices*/
      t[4].includes(
        /*index*/
        t[26]
      )), $(l, "class", "item svelte-yuohum"), $(l, "data-index", o = /*index*/
      t[26]), $(l, "aria-label", s = /*choices*/
      t[0][
        /*index*/
        t[26]
      ][0]), $(l, "data-testid", "dropdown-option"), $(l, "role", "option"), $(l, "aria-selected", r = /*selected_indices*/
      t[4].includes(
        /*index*/
        t[26]
      )), oe(
        l,
        "selected",
        /*selected_indices*/
        t[4].includes(
          /*index*/
          t[26]
        )
      ), oe(
        l,
        "active",
        /*index*/
        t[26] === /*active_index*/
        t[5]
      ), oe(
        l,
        "bg-gray-100",
        /*index*/
        t[26] === /*active_index*/
        t[5]
      ), oe(
        l,
        "dark:bg-gray-600",
        /*index*/
        t[26] === /*active_index*/
        t[5]
      );
    },
    m(a, m) {
      Qe(a, l, m), tl(l, e), tl(l, n), tl(l, f), tl(l, u);
    },
    p(a, m) {
      m & /*selected_indices, filtered_indices*/
      18 && oe(e, "hide", !/*selected_indices*/
      a[4].includes(
        /*index*/
        a[26]
      )), m & /*choices, filtered_indices*/
      3 && i !== (i = /*choices*/
      a[0][
        /*index*/
        a[26]
      ][0] + "") && zn(f, i), m & /*filtered_indices*/
      2 && o !== (o = /*index*/
      a[26]) && $(l, "data-index", o), m & /*choices, filtered_indices*/
      3 && s !== (s = /*choices*/
      a[0][
        /*index*/
        a[26]
      ][0]) && $(l, "aria-label", s), m & /*selected_indices, filtered_indices*/
      18 && r !== (r = /*selected_indices*/
      a[4].includes(
        /*index*/
        a[26]
      )) && $(l, "aria-selected", r), m & /*selected_indices, filtered_indices*/
      18 && oe(
        l,
        "selected",
        /*selected_indices*/
        a[4].includes(
          /*index*/
          a[26]
        )
      ), m & /*filtered_indices, active_index*/
      34 && oe(
        l,
        "active",
        /*index*/
        a[26] === /*active_index*/
        a[5]
      ), m & /*filtered_indices, active_index*/
      34 && oe(
        l,
        "bg-gray-100",
        /*index*/
        a[26] === /*active_index*/
        a[5]
      ), m & /*filtered_indices, active_index*/
      34 && oe(
        l,
        "dark:bg-gray-600",
        /*index*/
        a[26] === /*active_index*/
        a[5]
      );
    },
    d(a) {
      a && Ke(l);
    }
  };
}
function An(t) {
  let l, e, n, i, f;
  Yt(
    /*onwindowresize*/
    t[20]
  );
  let u = (
    /*show_options*/
    t[2] && !/*disabled*/
    t[3] && et(t)
  );
  return {
    c() {
      l = rl("div"), e = Ll(), u && u.c(), n = qn(), $(l, "class", "reference");
    },
    m(o, s) {
      Qe(o, l, s), t[21](l), Qe(o, e, s), u && u.m(o, s), Qe(o, n, s), i || (f = [
        Fl(
          window,
          "scroll",
          /*scroll_listener*/
          t[13]
        ),
        Fl(
          window,
          "resize",
          /*onwindowresize*/
          t[20]
        )
      ], i = !0);
    },
    p(o, [s]) {
      /*show_options*/
      o[2] && !/*disabled*/
      o[3] ? u ? (u.p(o, s), s & /*show_options, disabled*/
      12 && vl(u, 1)) : (u = et(o), u.c(), vl(u, 1), u.m(n.parentNode, n)) : u && (Sn(), xl(u, 1, 1, () => {
        u = null;
      }), Cn());
    },
    i(o) {
      vl(u);
    },
    o(o) {
      xl(u);
    },
    d(o) {
      o && (Ke(l), Ke(e), Ke(n)), t[21](null), u && u.d(o), i = !1, Fn(f);
    }
  };
}
function Vn(t, l, e) {
  var n, i;
  let { choices: f } = l, { filtered_indices: u } = l, { show_options: o = !1 } = l, { disabled: s = !1 } = l, { selected_indices: r = [] } = l, { active_index: a = null } = l, m, w, p, q, k, d, _, g, c, h;
  function S() {
    const { top: F, bottom: I } = k.getBoundingClientRect();
    e(17, m = F), e(18, w = h - I);
  }
  let y = null;
  function N() {
    o && (y !== null && clearTimeout(y), y = setTimeout(
      () => {
        S(), y = null;
      },
      10
    ));
  }
  const j = On();
  function E() {
    e(12, h = window.innerHeight);
  }
  function T(F) {
    Kl[F ? "unshift" : "push"](() => {
      k = F, e(6, k);
    });
  }
  const U = (F) => j("change", F);
  function le(F) {
    Kl[F ? "unshift" : "push"](() => {
      d = F, e(7, d);
    });
  }
  return t.$$set = (F) => {
    "choices" in F && e(0, f = F.choices), "filtered_indices" in F && e(1, u = F.filtered_indices), "show_options" in F && e(2, o = F.show_options), "disabled" in F && e(3, s = F.disabled), "selected_indices" in F && e(4, r = F.selected_indices), "active_index" in F && e(5, a = F.active_index);
  }, t.$$.update = () => {
    if (t.$$.dirty & /*show_options, refElement, listElement, selected_indices, _a, _b, distance_from_bottom, distance_from_top, input_height*/
    1016020) {
      if (o && k) {
        if (d && r.length > 0) {
          let I = d.querySelectorAll("li");
          for (const H of Array.from(I))
            if (H.getAttribute("data-index") === r[0].toString()) {
              e(15, n = d?.scrollTo) === null || n === void 0 || n.call(d, 0, H.offsetTop);
              break;
            }
        }
        S();
        const F = e(16, i = k.parentElement) === null || i === void 0 ? void 0 : i.getBoundingClientRect();
        e(19, p = F?.height || 0), e(8, q = F?.width || 0);
      }
      w > m ? (e(9, _ = `${m}px`), e(11, c = w), e(10, g = null)) : (e(10, g = `${w + p}px`), e(11, c = m - p), e(9, _ = null));
    }
  }, [
    f,
    u,
    o,
    s,
    r,
    a,
    k,
    d,
    q,
    _,
    g,
    c,
    h,
    N,
    j,
    n,
    i,
    m,
    w,
    p,
    E,
    T,
    U,
    le
  ];
}
class Gt extends vn {
  constructor(l) {
    super(), En(this, l, Vn, An, Ln, {
      choices: 0,
      filtered_indices: 1,
      show_options: 2,
      disabled: 3,
      selected_indices: 4,
      active_index: 5
    });
  }
}
const {
  SvelteComponent: Dn,
  assign: Bn,
  create_slot: Tn,
  detach: Un,
  element: Zn,
  get_all_dirty_from_scope: Pn,
  get_slot_changes: In,
  get_spread_update: Hn,
  init: Jn,
  insert: Rn,
  safe_not_equal: Xn,
  set_dynamic_element_data: tt,
  set_style: W,
  toggle_class: je,
  transition_in: Kt,
  transition_out: Qt,
  update_slot_base: Yn
} = window.__gradio__svelte__internal;
function Gn(t) {
  let l, e, n;
  const i = (
    /*#slots*/
    t[18].default
  ), f = Tn(
    i,
    t,
    /*$$scope*/
    t[17],
    null
  );
  let u = [
    { "data-testid": (
      /*test_id*/
      t[7]
    ) },
    { id: (
      /*elem_id*/
      t[2]
    ) },
    {
      class: e = "block " + /*elem_classes*/
      t[3].join(" ") + " svelte-1t38q2d"
    }
  ], o = {};
  for (let s = 0; s < u.length; s += 1)
    o = Bn(o, u[s]);
  return {
    c() {
      l = Zn(
        /*tag*/
        t[14]
      ), f && f.c(), tt(
        /*tag*/
        t[14]
      )(l, o), je(
        l,
        "hidden",
        /*visible*/
        t[10] === !1
      ), je(
        l,
        "padded",
        /*padding*/
        t[6]
      ), je(
        l,
        "border_focus",
        /*border_mode*/
        t[5] === "focus"
      ), je(l, "hide-container", !/*explicit_call*/
      t[8] && !/*container*/
      t[9]), W(
        l,
        "height",
        /*get_dimension*/
        t[15](
          /*height*/
          t[0]
        )
      ), W(l, "width", typeof /*width*/
      t[1] == "number" ? `calc(min(${/*width*/
      t[1]}px, 100%))` : (
        /*get_dimension*/
        t[15](
          /*width*/
          t[1]
        )
      )), W(
        l,
        "border-style",
        /*variant*/
        t[4]
      ), W(
        l,
        "overflow",
        /*allow_overflow*/
        t[11] ? "visible" : "hidden"
      ), W(
        l,
        "flex-grow",
        /*scale*/
        t[12]
      ), W(l, "min-width", `calc(min(${/*min_width*/
      t[13]}px, 100%))`), W(l, "border-width", "var(--block-border-width)");
    },
    m(s, r) {
      Rn(s, l, r), f && f.m(l, null), n = !0;
    },
    p(s, r) {
      f && f.p && (!n || r & /*$$scope*/
      131072) && Yn(
        f,
        i,
        s,
        /*$$scope*/
        s[17],
        n ? In(
          i,
          /*$$scope*/
          s[17],
          r,
          null
        ) : Pn(
          /*$$scope*/
          s[17]
        ),
        null
      ), tt(
        /*tag*/
        s[14]
      )(l, o = Hn(u, [
        (!n || r & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          s[7]
        ) },
        (!n || r & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          s[2]
        ) },
        (!n || r & /*elem_classes*/
        8 && e !== (e = "block " + /*elem_classes*/
        s[3].join(" ") + " svelte-1t38q2d")) && { class: e }
      ])), je(
        l,
        "hidden",
        /*visible*/
        s[10] === !1
      ), je(
        l,
        "padded",
        /*padding*/
        s[6]
      ), je(
        l,
        "border_focus",
        /*border_mode*/
        s[5] === "focus"
      ), je(l, "hide-container", !/*explicit_call*/
      s[8] && !/*container*/
      s[9]), r & /*height*/
      1 && W(
        l,
        "height",
        /*get_dimension*/
        s[15](
          /*height*/
          s[0]
        )
      ), r & /*width*/
      2 && W(l, "width", typeof /*width*/
      s[1] == "number" ? `calc(min(${/*width*/
      s[1]}px, 100%))` : (
        /*get_dimension*/
        s[15](
          /*width*/
          s[1]
        )
      )), r & /*variant*/
      16 && W(
        l,
        "border-style",
        /*variant*/
        s[4]
      ), r & /*allow_overflow*/
      2048 && W(
        l,
        "overflow",
        /*allow_overflow*/
        s[11] ? "visible" : "hidden"
      ), r & /*scale*/
      4096 && W(
        l,
        "flex-grow",
        /*scale*/
        s[12]
      ), r & /*min_width*/
      8192 && W(l, "min-width", `calc(min(${/*min_width*/
      s[13]}px, 100%))`);
    },
    i(s) {
      n || (Kt(f, s), n = !0);
    },
    o(s) {
      Qt(f, s), n = !1;
    },
    d(s) {
      s && Un(l), f && f.d(s);
    }
  };
}
function Kn(t) {
  let l, e = (
    /*tag*/
    t[14] && Gn(t)
  );
  return {
    c() {
      e && e.c();
    },
    m(n, i) {
      e && e.m(n, i), l = !0;
    },
    p(n, [i]) {
      /*tag*/
      n[14] && e.p(n, i);
    },
    i(n) {
      l || (Kt(e, n), l = !0);
    },
    o(n) {
      Qt(e, n), l = !1;
    },
    d(n) {
      e && e.d(n);
    }
  };
}
function Qn(t, l, e) {
  let { $$slots: n = {}, $$scope: i } = l, { height: f = void 0 } = l, { width: u = void 0 } = l, { elem_id: o = "" } = l, { elem_classes: s = [] } = l, { variant: r = "solid" } = l, { border_mode: a = "base" } = l, { padding: m = !0 } = l, { type: w = "normal" } = l, { test_id: p = void 0 } = l, { explicit_call: q = !1 } = l, { container: k = !0 } = l, { visible: d = !0 } = l, { allow_overflow: _ = !0 } = l, { scale: g = null } = l, { min_width: c = 0 } = l, h = w === "fieldset" ? "fieldset" : "div";
  const S = (y) => {
    if (y !== void 0) {
      if (typeof y == "number")
        return y + "px";
      if (typeof y == "string")
        return y;
    }
  };
  return t.$$set = (y) => {
    "height" in y && e(0, f = y.height), "width" in y && e(1, u = y.width), "elem_id" in y && e(2, o = y.elem_id), "elem_classes" in y && e(3, s = y.elem_classes), "variant" in y && e(4, r = y.variant), "border_mode" in y && e(5, a = y.border_mode), "padding" in y && e(6, m = y.padding), "type" in y && e(16, w = y.type), "test_id" in y && e(7, p = y.test_id), "explicit_call" in y && e(8, q = y.explicit_call), "container" in y && e(9, k = y.container), "visible" in y && e(10, d = y.visible), "allow_overflow" in y && e(11, _ = y.allow_overflow), "scale" in y && e(12, g = y.scale), "min_width" in y && e(13, c = y.min_width), "$$scope" in y && e(17, i = y.$$scope);
  }, [
    f,
    u,
    o,
    s,
    r,
    a,
    m,
    p,
    q,
    k,
    d,
    _,
    g,
    c,
    h,
    S,
    w,
    i,
    n
  ];
}
class Wn extends Dn {
  constructor(l) {
    super(), Jn(this, l, Qn, Kn, Xn, {
      height: 0,
      width: 1,
      elem_id: 2,
      elem_classes: 3,
      variant: 4,
      border_mode: 5,
      padding: 6,
      type: 16,
      test_id: 7,
      explicit_call: 8,
      container: 9,
      visible: 10,
      allow_overflow: 11,
      scale: 12,
      min_width: 13
    });
  }
}
const {
  SvelteComponent: xn,
  attr: $n,
  create_slot: ei,
  detach: li,
  element: ti,
  get_all_dirty_from_scope: ni,
  get_slot_changes: ii,
  init: si,
  insert: oi,
  safe_not_equal: fi,
  transition_in: ui,
  transition_out: ri,
  update_slot_base: ai
} = window.__gradio__svelte__internal;
function _i(t) {
  let l, e;
  const n = (
    /*#slots*/
    t[1].default
  ), i = ei(
    n,
    t,
    /*$$scope*/
    t[0],
    null
  );
  return {
    c() {
      l = ti("div"), i && i.c(), $n(l, "class", "svelte-1hnfib2");
    },
    m(f, u) {
      oi(f, l, u), i && i.m(l, null), e = !0;
    },
    p(f, [u]) {
      i && i.p && (!e || u & /*$$scope*/
      1) && ai(
        i,
        n,
        f,
        /*$$scope*/
        f[0],
        e ? ii(
          n,
          /*$$scope*/
          f[0],
          u,
          null
        ) : ni(
          /*$$scope*/
          f[0]
        ),
        null
      );
    },
    i(f) {
      e || (ui(i, f), e = !0);
    },
    o(f) {
      ri(i, f), e = !1;
    },
    d(f) {
      f && li(l), i && i.d(f);
    }
  };
}
function ci(t, l, e) {
  let { $$slots: n = {}, $$scope: i } = l;
  return t.$$set = (f) => {
    "$$scope" in f && e(0, i = f.$$scope);
  }, [i, n];
}
class di extends xn {
  constructor(l) {
    super(), si(this, l, ci, _i, fi, {});
  }
}
const {
  SvelteComponent: mi,
  attr: nt,
  check_outros: bi,
  create_component: hi,
  create_slot: gi,
  destroy_component: wi,
  detach: ol,
  element: pi,
  empty: ki,
  get_all_dirty_from_scope: yi,
  get_slot_changes: vi,
  group_outros: Ci,
  init: ji,
  insert: fl,
  mount_component: qi,
  safe_not_equal: Si,
  set_data: Ei,
  space: Ni,
  text: Fi,
  toggle_class: ze,
  transition_in: Ye,
  transition_out: ul,
  update_slot_base: Li
} = window.__gradio__svelte__internal;
function it(t) {
  let l, e;
  return l = new di({
    props: {
      $$slots: { default: [zi] },
      $$scope: { ctx: t }
    }
  }), {
    c() {
      hi(l.$$.fragment);
    },
    m(n, i) {
      qi(l, n, i), e = !0;
    },
    p(n, i) {
      const f = {};
      i & /*$$scope, info*/
      10 && (f.$$scope = { dirty: i, ctx: n }), l.$set(f);
    },
    i(n) {
      e || (Ye(l.$$.fragment, n), e = !0);
    },
    o(n) {
      ul(l.$$.fragment, n), e = !1;
    },
    d(n) {
      wi(l, n);
    }
  };
}
function zi(t) {
  let l;
  return {
    c() {
      l = Fi(
        /*info*/
        t[1]
      );
    },
    m(e, n) {
      fl(e, l, n);
    },
    p(e, n) {
      n & /*info*/
      2 && Ei(
        l,
        /*info*/
        e[1]
      );
    },
    d(e) {
      e && ol(l);
    }
  };
}
function Mi(t) {
  let l, e, n, i;
  const f = (
    /*#slots*/
    t[2].default
  ), u = gi(
    f,
    t,
    /*$$scope*/
    t[3],
    null
  );
  let o = (
    /*info*/
    t[1] && it(t)
  );
  return {
    c() {
      l = pi("span"), u && u.c(), e = Ni(), o && o.c(), n = ki(), nt(l, "data-testid", "block-info"), nt(l, "class", "svelte-22c38v"), ze(l, "sr-only", !/*show_label*/
      t[0]), ze(l, "hide", !/*show_label*/
      t[0]), ze(
        l,
        "has-info",
        /*info*/
        t[1] != null
      );
    },
    m(s, r) {
      fl(s, l, r), u && u.m(l, null), fl(s, e, r), o && o.m(s, r), fl(s, n, r), i = !0;
    },
    p(s, [r]) {
      u && u.p && (!i || r & /*$$scope*/
      8) && Li(
        u,
        f,
        s,
        /*$$scope*/
        s[3],
        i ? vi(
          f,
          /*$$scope*/
          s[3],
          r,
          null
        ) : yi(
          /*$$scope*/
          s[3]
        ),
        null
      ), (!i || r & /*show_label*/
      1) && ze(l, "sr-only", !/*show_label*/
      s[0]), (!i || r & /*show_label*/
      1) && ze(l, "hide", !/*show_label*/
      s[0]), (!i || r & /*info*/
      2) && ze(
        l,
        "has-info",
        /*info*/
        s[1] != null
      ), /*info*/
      s[1] ? o ? (o.p(s, r), r & /*info*/
      2 && Ye(o, 1)) : (o = it(s), o.c(), Ye(o, 1), o.m(n.parentNode, n)) : o && (Ci(), ul(o, 1, 1, () => {
        o = null;
      }), bi());
    },
    i(s) {
      i || (Ye(u, s), Ye(o), i = !0);
    },
    o(s) {
      ul(u, s), ul(o), i = !1;
    },
    d(s) {
      s && (ol(l), ol(e), ol(n)), u && u.d(s), o && o.d(s);
    }
  };
}
function Oi(t, l, e) {
  let { $$slots: n = {}, $$scope: i } = l, { show_label: f = !0 } = l, { info: u = void 0 } = l;
  return t.$$set = (o) => {
    "show_label" in o && e(0, f = o.show_label), "info" in o && e(1, u = o.info), "$$scope" in o && e(3, i = o.$$scope);
  }, [f, u, n, i];
}
class Wt extends mi {
  constructor(l) {
    super(), ji(this, l, Oi, Mi, Si, { show_label: 0, info: 1 });
  }
}
const {
  SvelteComponent: Ai,
  append: Vi,
  attr: Me,
  detach: Di,
  init: Bi,
  insert: Ti,
  noop: Cl,
  safe_not_equal: Ui,
  svg_element: st
} = window.__gradio__svelte__internal;
function Zi(t) {
  let l, e;
  return {
    c() {
      l = st("svg"), e = st("path"), Me(e, "d", "M5 8l4 4 4-4z"), Me(l, "class", "dropdown-arrow svelte-145leq6"), Me(l, "xmlns", "http://www.w3.org/2000/svg"), Me(l, "width", "100%"), Me(l, "height", "100%"), Me(l, "viewBox", "0 0 18 18");
    },
    m(n, i) {
      Ti(n, l, i), Vi(l, e);
    },
    p: Cl,
    i: Cl,
    o: Cl,
    d(n) {
      n && Di(l);
    }
  };
}
class xt extends Ai {
  constructor(l) {
    super(), Bi(this, l, null, Zi, Ui, {});
  }
}
const {
  SvelteComponent: Pi,
  append: Ii,
  attr: jl,
  detach: Hi,
  init: Ji,
  insert: Ri,
  noop: ql,
  safe_not_equal: Xi,
  svg_element: ot
} = window.__gradio__svelte__internal;
function Yi(t) {
  let l, e;
  return {
    c() {
      l = ot("svg"), e = ot("path"), jl(e, "d", "M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"), jl(l, "xmlns", "http://www.w3.org/2000/svg"), jl(l, "viewBox", "0 0 24 24");
    },
    m(n, i) {
      Ri(n, l, i), Ii(l, e);
    },
    p: ql,
    i: ql,
    o: ql,
    d(n) {
      n && Hi(l);
    }
  };
}
class $t extends Pi {
  constructor(l) {
    super(), Ji(this, l, null, Yi, Xi, {});
  }
}
const Gi = [
  { color: "red", primary: 600, secondary: 100 },
  { color: "green", primary: 600, secondary: 100 },
  { color: "blue", primary: 600, secondary: 100 },
  { color: "yellow", primary: 500, secondary: 100 },
  { color: "purple", primary: 600, secondary: 100 },
  { color: "teal", primary: 600, secondary: 100 },
  { color: "orange", primary: 600, secondary: 100 },
  { color: "cyan", primary: 600, secondary: 100 },
  { color: "lime", primary: 500, secondary: 100 },
  { color: "pink", primary: 600, secondary: 100 }
], ft = {
  inherit: "inherit",
  current: "currentColor",
  transparent: "transparent",
  black: "#000",
  white: "#fff",
  slate: {
    50: "#f8fafc",
    100: "#f1f5f9",
    200: "#e2e8f0",
    300: "#cbd5e1",
    400: "#94a3b8",
    500: "#64748b",
    600: "#475569",
    700: "#334155",
    800: "#1e293b",
    900: "#0f172a",
    950: "#020617"
  },
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
    950: "#030712"
  },
  zinc: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b"
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a"
  },
  stone: {
    50: "#fafaf9",
    100: "#f5f5f4",
    200: "#e7e5e4",
    300: "#d6d3d1",
    400: "#a8a29e",
    500: "#78716c",
    600: "#57534e",
    700: "#44403c",
    800: "#292524",
    900: "#1c1917",
    950: "#0c0a09"
  },
  red: {
    50: "#fef2f2",
    100: "#fee2e2",
    200: "#fecaca",
    300: "#fca5a5",
    400: "#f87171",
    500: "#ef4444",
    600: "#dc2626",
    700: "#b91c1c",
    800: "#991b1b",
    900: "#7f1d1d",
    950: "#450a0a"
  },
  orange: {
    50: "#fff7ed",
    100: "#ffedd5",
    200: "#fed7aa",
    300: "#fdba74",
    400: "#fb923c",
    500: "#f97316",
    600: "#ea580c",
    700: "#c2410c",
    800: "#9a3412",
    900: "#7c2d12",
    950: "#431407"
  },
  amber: {
    50: "#fffbeb",
    100: "#fef3c7",
    200: "#fde68a",
    300: "#fcd34d",
    400: "#fbbf24",
    500: "#f59e0b",
    600: "#d97706",
    700: "#b45309",
    800: "#92400e",
    900: "#78350f",
    950: "#451a03"
  },
  yellow: {
    50: "#fefce8",
    100: "#fef9c3",
    200: "#fef08a",
    300: "#fde047",
    400: "#facc15",
    500: "#eab308",
    600: "#ca8a04",
    700: "#a16207",
    800: "#854d0e",
    900: "#713f12",
    950: "#422006"
  },
  lime: {
    50: "#f7fee7",
    100: "#ecfccb",
    200: "#d9f99d",
    300: "#bef264",
    400: "#a3e635",
    500: "#84cc16",
    600: "#65a30d",
    700: "#4d7c0f",
    800: "#3f6212",
    900: "#365314",
    950: "#1a2e05"
  },
  green: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16"
  },
  emerald: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22"
  },
  teal: {
    50: "#f0fdfa",
    100: "#ccfbf1",
    200: "#99f6e4",
    300: "#5eead4",
    400: "#2dd4bf",
    500: "#14b8a6",
    600: "#0d9488",
    700: "#0f766e",
    800: "#115e59",
    900: "#134e4a",
    950: "#042f2e"
  },
  cyan: {
    50: "#ecfeff",
    100: "#cffafe",
    200: "#a5f3fc",
    300: "#67e8f9",
    400: "#22d3ee",
    500: "#06b6d4",
    600: "#0891b2",
    700: "#0e7490",
    800: "#155e75",
    900: "#164e63",
    950: "#083344"
  },
  sky: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49"
  },
  blue: {
    50: "#eff6ff",
    100: "#dbeafe",
    200: "#bfdbfe",
    300: "#93c5fd",
    400: "#60a5fa",
    500: "#3b82f6",
    600: "#2563eb",
    700: "#1d4ed8",
    800: "#1e40af",
    900: "#1e3a8a",
    950: "#172554"
  },
  indigo: {
    50: "#eef2ff",
    100: "#e0e7ff",
    200: "#c7d2fe",
    300: "#a5b4fc",
    400: "#818cf8",
    500: "#6366f1",
    600: "#4f46e5",
    700: "#4338ca",
    800: "#3730a3",
    900: "#312e81",
    950: "#1e1b4b"
  },
  violet: {
    50: "#f5f3ff",
    100: "#ede9fe",
    200: "#ddd6fe",
    300: "#c4b5fd",
    400: "#a78bfa",
    500: "#8b5cf6",
    600: "#7c3aed",
    700: "#6d28d9",
    800: "#5b21b6",
    900: "#4c1d95",
    950: "#2e1065"
  },
  purple: {
    50: "#faf5ff",
    100: "#f3e8ff",
    200: "#e9d5ff",
    300: "#d8b4fe",
    400: "#c084fc",
    500: "#a855f7",
    600: "#9333ea",
    700: "#7e22ce",
    800: "#6b21a8",
    900: "#581c87",
    950: "#3b0764"
  },
  fuchsia: {
    50: "#fdf4ff",
    100: "#fae8ff",
    200: "#f5d0fe",
    300: "#f0abfc",
    400: "#e879f9",
    500: "#d946ef",
    600: "#c026d3",
    700: "#a21caf",
    800: "#86198f",
    900: "#701a75",
    950: "#4a044e"
  },
  pink: {
    50: "#fdf2f8",
    100: "#fce7f3",
    200: "#fbcfe8",
    300: "#f9a8d4",
    400: "#f472b6",
    500: "#ec4899",
    600: "#db2777",
    700: "#be185d",
    800: "#9d174d",
    900: "#831843",
    950: "#500724"
  },
  rose: {
    50: "#fff1f2",
    100: "#ffe4e6",
    200: "#fecdd3",
    300: "#fda4af",
    400: "#fb7185",
    500: "#f43f5e",
    600: "#e11d48",
    700: "#be123c",
    800: "#9f1239",
    900: "#881337",
    950: "#4c0519"
  }
};
Gi.reduce(
  (t, { color: l, primary: e, secondary: n }) => ({
    ...t,
    [l]: {
      primary: ft[l][e],
      secondary: ft[l][n]
    }
  }),
  {}
);
function Ki(t, l) {
  return (t % l + l) % l;
}
function zl(t, l) {
  return t.reduce((e, n, i) => ((!l || n[0].toLowerCase().includes(l.toLowerCase())) && e.push(i), e), []);
}
function en(t, l, e) {
  t("change", l), e || t("input");
}
function ln(t, l, e) {
  if (t.key === "Escape")
    return [!1, l];
  if ((t.key === "ArrowDown" || t.key === "ArrowUp") && e.length >= 0)
    if (l === null)
      l = t.key === "ArrowDown" ? e[0] : e[e.length - 1];
    else {
      const n = e.indexOf(l), i = t.key === "ArrowUp" ? -1 : 1;
      l = e[Ki(n + i, e.length)];
    }
  return [!0, l];
}
const {
  SvelteComponent: Qi,
  append: Ne,
  attr: x,
  binding_callbacks: Wi,
  check_outros: xi,
  create_component: Ml,
  destroy_component: Ol,
  detach: Ul,
  element: Be,
  group_outros: $i,
  init: es,
  insert: Zl,
  listen: Xe,
  mount_component: Al,
  run_all: ls,
  safe_not_equal: ts,
  set_data: ns,
  set_input_value: ut,
  space: Sl,
  text: is,
  toggle_class: Oe,
  transition_in: Te,
  transition_out: Ge
} = window.__gradio__svelte__internal, { createEventDispatcher: ss, afterUpdate: os } = window.__gradio__svelte__internal;
function fs(t) {
  let l;
  return {
    c() {
      l = is(
        /*label*/
        t[0]
      );
    },
    m(e, n) {
      Zl(e, l, n);
    },
    p(e, n) {
      n[0] & /*label*/
      1 && ns(
        l,
        /*label*/
        e[0]
      );
    },
    d(e) {
      e && Ul(l);
    }
  };
}
function rt(t) {
  let l, e, n;
  return e = new xt({}), {
    c() {
      l = Be("div"), Ml(e.$$.fragment), x(l, "class", "icon-wrap svelte-1m1zvyj");
    },
    m(i, f) {
      Zl(i, l, f), Al(e, l, null), n = !0;
    },
    i(i) {
      n || (Te(e.$$.fragment, i), n = !0);
    },
    o(i) {
      Ge(e.$$.fragment, i), n = !1;
    },
    d(i) {
      i && Ul(l), Ol(e);
    }
  };
}
function us(t) {
  let l, e, n, i, f, u, o, s, r, a, m, w, p, q;
  e = new Wt({
    props: {
      show_label: (
        /*show_label*/
        t[4]
      ),
      info: (
        /*info*/
        t[1]
      ),
      $$slots: { default: [fs] },
      $$scope: { ctx: t }
    }
  });
  let k = !/*disabled*/
  t[3] && rt();
  return m = new Gt({
    props: {
      show_options: (
        /*show_options*/
        t[12]
      ),
      choices: (
        /*choices*/
        t[2]
      ),
      filtered_indices: (
        /*filtered_indices*/
        t[10]
      ),
      disabled: (
        /*disabled*/
        t[3]
      ),
      selected_indices: (
        /*selected_index*/
        t[11] === null ? [] : [
          /*selected_index*/
          t[11]
        ]
      ),
      active_index: (
        /*active_index*/
        t[14]
      )
    }
  }), m.$on(
    "change",
    /*handle_option_selected*/
    t[16]
  ), {
    c() {
      l = Be("div"), Ml(e.$$.fragment), n = Sl(), i = Be("div"), f = Be("div"), u = Be("div"), o = Be("input"), r = Sl(), k && k.c(), a = Sl(), Ml(m.$$.fragment), x(o, "role", "listbox"), x(o, "aria-controls", "dropdown-options"), x(
        o,
        "aria-expanded",
        /*show_options*/
        t[12]
      ), x(
        o,
        "aria-label",
        /*label*/
        t[0]
      ), x(o, "class", "border-none svelte-1m1zvyj"), o.disabled = /*disabled*/
      t[3], x(o, "autocomplete", "off"), o.readOnly = s = !/*filterable*/
      t[7], Oe(o, "subdued", !/*choices_names*/
      t[13].includes(
        /*input_text*/
        t[9]
      ) && !/*allow_custom_value*/
      t[6]), x(u, "class", "secondary-wrap svelte-1m1zvyj"), x(f, "class", "wrap-inner svelte-1m1zvyj"), Oe(
        f,
        "show_options",
        /*show_options*/
        t[12]
      ), x(i, "class", "wrap svelte-1m1zvyj"), x(l, "class", "svelte-1m1zvyj"), Oe(
        l,
        "container",
        /*container*/
        t[5]
      );
    },
    m(d, _) {
      Zl(d, l, _), Al(e, l, null), Ne(l, n), Ne(l, i), Ne(i, f), Ne(f, u), Ne(u, o), ut(
        o,
        /*input_text*/
        t[9]
      ), t[29](o), Ne(u, r), k && k.m(u, null), Ne(i, a), Al(m, i, null), w = !0, p || (q = [
        Xe(
          o,
          "input",
          /*input_input_handler*/
          t[28]
        ),
        Xe(
          o,
          "keydown",
          /*handle_key_down*/
          t[19]
        ),
        Xe(
          o,
          "keyup",
          /*keyup_handler*/
          t[30]
        ),
        Xe(
          o,
          "blur",
          /*handle_blur*/
          t[18]
        ),
        Xe(
          o,
          "focus",
          /*handle_focus*/
          t[17]
        )
      ], p = !0);
    },
    p(d, _) {
      const g = {};
      _[0] & /*show_label*/
      16 && (g.show_label = /*show_label*/
      d[4]), _[0] & /*info*/
      2 && (g.info = /*info*/
      d[1]), _[0] & /*label*/
      1 | _[1] & /*$$scope*/
      4 && (g.$$scope = { dirty: _, ctx: d }), e.$set(g), (!w || _[0] & /*show_options*/
      4096) && x(
        o,
        "aria-expanded",
        /*show_options*/
        d[12]
      ), (!w || _[0] & /*label*/
      1) && x(
        o,
        "aria-label",
        /*label*/
        d[0]
      ), (!w || _[0] & /*disabled*/
      8) && (o.disabled = /*disabled*/
      d[3]), (!w || _[0] & /*filterable*/
      128 && s !== (s = !/*filterable*/
      d[7])) && (o.readOnly = s), _[0] & /*input_text*/
      512 && o.value !== /*input_text*/
      d[9] && ut(
        o,
        /*input_text*/
        d[9]
      ), (!w || _[0] & /*choices_names, input_text, allow_custom_value*/
      8768) && Oe(o, "subdued", !/*choices_names*/
      d[13].includes(
        /*input_text*/
        d[9]
      ) && !/*allow_custom_value*/
      d[6]), /*disabled*/
      d[3] ? k && ($i(), Ge(k, 1, 1, () => {
        k = null;
      }), xi()) : k ? _[0] & /*disabled*/
      8 && Te(k, 1) : (k = rt(), k.c(), Te(k, 1), k.m(u, null)), (!w || _[0] & /*show_options*/
      4096) && Oe(
        f,
        "show_options",
        /*show_options*/
        d[12]
      );
      const c = {};
      _[0] & /*show_options*/
      4096 && (c.show_options = /*show_options*/
      d[12]), _[0] & /*choices*/
      4 && (c.choices = /*choices*/
      d[2]), _[0] & /*filtered_indices*/
      1024 && (c.filtered_indices = /*filtered_indices*/
      d[10]), _[0] & /*disabled*/
      8 && (c.disabled = /*disabled*/
      d[3]), _[0] & /*selected_index*/
      2048 && (c.selected_indices = /*selected_index*/
      d[11] === null ? [] : [
        /*selected_index*/
        d[11]
      ]), _[0] & /*active_index*/
      16384 && (c.active_index = /*active_index*/
      d[14]), m.$set(c), (!w || _[0] & /*container*/
      32) && Oe(
        l,
        "container",
        /*container*/
        d[5]
      );
    },
    i(d) {
      w || (Te(e.$$.fragment, d), Te(k), Te(m.$$.fragment, d), w = !0);
    },
    o(d) {
      Ge(e.$$.fragment, d), Ge(k), Ge(m.$$.fragment, d), w = !1;
    },
    d(d) {
      d && Ul(l), Ol(e), t[29](null), k && k.d(), Ol(m), p = !1, ls(q);
    }
  };
}
function rs(t, l, e) {
  let { label: n } = l, { info: i = void 0 } = l, { value: f = [] } = l, u = [], { value_is_output: o = !1 } = l, { choices: s } = l, r, { disabled: a = !1 } = l, { show_label: m } = l, { container: w = !0 } = l, { allow_custom_value: p = !1 } = l, { filterable: q = !0 } = l, k, d = !1, _, g, c = "", h = "", S = !1, y = [], N = null, j = null, E;
  const T = ss();
  f ? (E = s.map((b) => b[1]).indexOf(f), j = E, j === -1 ? (u = f, j = null) : ([c, u] = s[j], h = c), le()) : s.length > 0 && (E = 0, j = 0, [c, f] = s[j], u = f, h = c);
  function U() {
    e(13, _ = s.map((b) => b[0])), e(24, g = s.map((b) => b[1]));
  }
  function le() {
    U(), f === void 0 ? (e(9, c = ""), e(11, j = null)) : g.includes(f) ? (e(9, c = _[g.indexOf(f)]), e(11, j = g.indexOf(f))) : p ? (e(9, c = f), e(11, j = null)) : (e(9, c = ""), e(11, j = null)), e(27, E = j);
  }
  function F(b) {
    if (e(11, j = parseInt(b.detail.target.dataset.index)), isNaN(j)) {
      e(11, j = null);
      return;
    }
    e(12, d = !1), e(14, N = null), k.blur();
  }
  function I(b) {
    e(10, y = s.map((G, K) => K)), e(12, d = !0), T("focus");
  }
  function H() {
    p ? e(20, f = c) : e(9, c = _[g.indexOf(f)]), e(12, d = !1), e(14, N = null), T("blur");
  }
  function de(b) {
    e(12, [d, N] = ln(b, N, y), d, (e(14, N), e(2, s), e(23, r), e(6, p), e(9, c), e(10, y), e(8, k), e(25, h), e(11, j), e(27, E), e(26, S), e(24, g))), b.key === "Enter" && (N !== null ? (e(11, j = N), e(12, d = !1), k.blur(), e(14, N = null)) : _.includes(c) ? (e(11, j = _.indexOf(c)), e(12, d = !1), e(14, N = null), k.blur()) : p && (e(20, f = c), e(11, j = null), e(12, d = !1), e(14, N = null), k.blur()));
  }
  os(() => {
    e(21, o = !1), e(26, S = !0);
  });
  function pe() {
    c = this.value, e(9, c), e(11, j), e(27, E), e(26, S), e(2, s), e(24, g);
  }
  function ke(b) {
    Wi[b ? "unshift" : "push"](() => {
      k = b, e(8, k);
    });
  }
  const ye = (b) => T("key_up", { key: b.key, input_value: c });
  return t.$$set = (b) => {
    "label" in b && e(0, n = b.label), "info" in b && e(1, i = b.info), "value" in b && e(20, f = b.value), "value_is_output" in b && e(21, o = b.value_is_output), "choices" in b && e(2, s = b.choices), "disabled" in b && e(3, a = b.disabled), "show_label" in b && e(4, m = b.show_label), "container" in b && e(5, w = b.container), "allow_custom_value" in b && e(6, p = b.allow_custom_value), "filterable" in b && e(7, q = b.filterable);
  }, t.$$.update = () => {
    t.$$.dirty[0] & /*selected_index, old_selected_index, initialized, choices, choices_values*/
    218105860 && j !== E && j !== null && S && (e(9, [c, f] = s[j], c, (e(20, f), e(11, j), e(27, E), e(26, S), e(2, s), e(24, g))), e(27, E = j), T("select", {
      index: j,
      value: g[j],
      selected: !0
    })), t.$$.dirty[0] & /*value, old_value, value_is_output*/
    7340032 && f != u && (le(), en(T, f, o), e(22, u = f)), t.$$.dirty[0] & /*choices*/
    4 && U(), t.$$.dirty[0] & /*choices, old_choices, allow_custom_value, input_text, filtered_indices, filter_input*/
    8390468 && s !== r && (p || le(), e(23, r = s), e(10, y = zl(s, c)), !p && y.length > 0 && e(14, N = y[0]), k == document.activeElement && e(12, d = !0)), t.$$.dirty[0] & /*input_text, old_input_text, choices, allow_custom_value, filtered_indices*/
    33556036 && c !== h && (e(10, y = zl(s, c)), e(25, h = c), !p && y.length > 0 && e(14, N = y[0]));
  }, [
    n,
    i,
    s,
    a,
    m,
    w,
    p,
    q,
    k,
    c,
    y,
    j,
    d,
    _,
    N,
    T,
    F,
    I,
    H,
    de,
    f,
    o,
    u,
    r,
    g,
    h,
    S,
    E,
    pe,
    ke,
    ye
  ];
}
class as extends Qi {
  constructor(l) {
    super(), es(
      this,
      l,
      rs,
      us,
      ts,
      {
        label: 0,
        info: 1,
        value: 20,
        value_is_output: 21,
        choices: 2,
        disabled: 3,
        show_label: 4,
        container: 5,
        allow_custom_value: 6,
        filterable: 7
      },
      null,
      [-1, -1]
    );
  }
}
function Ue(t) {
  let l = ["", "k", "M", "G", "T", "P", "E", "Z"], e = 0;
  for (; t > 1e3 && e < l.length - 1; )
    t /= 1e3, e++;
  let n = l[e];
  return (Number.isInteger(t) ? t : t.toFixed(1)) + n;
}
const {
  SvelteComponent: _s,
  append: ie,
  attr: O,
  component_subscribe: at,
  detach: cs,
  element: ds,
  init: ms,
  insert: bs,
  noop: _t,
  safe_not_equal: hs,
  set_style: nl,
  svg_element: se,
  toggle_class: ct
} = window.__gradio__svelte__internal, { onMount: gs } = window.__gradio__svelte__internal;
function ws(t) {
  let l, e, n, i, f, u, o, s, r, a, m, w;
  return {
    c() {
      l = ds("div"), e = se("svg"), n = se("g"), i = se("path"), f = se("path"), u = se("path"), o = se("path"), s = se("g"), r = se("path"), a = se("path"), m = se("path"), w = se("path"), O(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), O(i, "fill", "#FF7C00"), O(i, "fill-opacity", "0.4"), O(i, "class", "svelte-43sxxs"), O(f, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), O(f, "fill", "#FF7C00"), O(f, "class", "svelte-43sxxs"), O(u, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), O(u, "fill", "#FF7C00"), O(u, "fill-opacity", "0.4"), O(u, "class", "svelte-43sxxs"), O(o, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), O(o, "fill", "#FF7C00"), O(o, "class", "svelte-43sxxs"), nl(n, "transform", "translate(" + /*$top*/
      t[1][0] + "px, " + /*$top*/
      t[1][1] + "px)"), O(r, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), O(r, "fill", "#FF7C00"), O(r, "fill-opacity", "0.4"), O(r, "class", "svelte-43sxxs"), O(a, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), O(a, "fill", "#FF7C00"), O(a, "class", "svelte-43sxxs"), O(m, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), O(m, "fill", "#FF7C00"), O(m, "fill-opacity", "0.4"), O(m, "class", "svelte-43sxxs"), O(w, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), O(w, "fill", "#FF7C00"), O(w, "class", "svelte-43sxxs"), nl(s, "transform", "translate(" + /*$bottom*/
      t[2][0] + "px, " + /*$bottom*/
      t[2][1] + "px)"), O(e, "viewBox", "-1200 -1200 3000 3000"), O(e, "fill", "none"), O(e, "xmlns", "http://www.w3.org/2000/svg"), O(e, "class", "svelte-43sxxs"), O(l, "class", "svelte-43sxxs"), ct(
        l,
        "margin",
        /*margin*/
        t[0]
      );
    },
    m(p, q) {
      bs(p, l, q), ie(l, e), ie(e, n), ie(n, i), ie(n, f), ie(n, u), ie(n, o), ie(e, s), ie(s, r), ie(s, a), ie(s, m), ie(s, w);
    },
    p(p, [q]) {
      q & /*$top*/
      2 && nl(n, "transform", "translate(" + /*$top*/
      p[1][0] + "px, " + /*$top*/
      p[1][1] + "px)"), q & /*$bottom*/
      4 && nl(s, "transform", "translate(" + /*$bottom*/
      p[2][0] + "px, " + /*$bottom*/
      p[2][1] + "px)"), q & /*margin*/
      1 && ct(
        l,
        "margin",
        /*margin*/
        p[0]
      );
    },
    i: _t,
    o: _t,
    d(p) {
      p && cs(l);
    }
  };
}
function ps(t, l, e) {
  let n, i;
  var f = this && this.__awaiter || function(p, q, k, d) {
    function _(g) {
      return g instanceof k ? g : new k(function(c) {
        c(g);
      });
    }
    return new (k || (k = Promise))(function(g, c) {
      function h(N) {
        try {
          y(d.next(N));
        } catch (j) {
          c(j);
        }
      }
      function S(N) {
        try {
          y(d.throw(N));
        } catch (j) {
          c(j);
        }
      }
      function y(N) {
        N.done ? g(N.value) : _(N.value).then(h, S);
      }
      y((d = d.apply(p, q || [])).next());
    });
  };
  let { margin: u = !0 } = l;
  const o = Gl([0, 0]);
  at(t, o, (p) => e(1, n = p));
  const s = Gl([0, 0]);
  at(t, s, (p) => e(2, i = p));
  let r;
  function a() {
    return f(this, void 0, void 0, function* () {
      yield Promise.all([o.set([125, 140]), s.set([-125, -140])]), yield Promise.all([o.set([-125, 140]), s.set([125, -140])]), yield Promise.all([o.set([-125, 0]), s.set([125, -0])]), yield Promise.all([o.set([125, 0]), s.set([-125, 0])]);
    });
  }
  function m() {
    return f(this, void 0, void 0, function* () {
      yield a(), r || m();
    });
  }
  function w() {
    return f(this, void 0, void 0, function* () {
      yield Promise.all([o.set([125, 0]), s.set([-125, 0])]), m();
    });
  }
  return gs(() => (w(), () => r = !0)), t.$$set = (p) => {
    "margin" in p && e(0, u = p.margin);
  }, [u, n, i, o, s];
}
class ks extends _s {
  constructor(l) {
    super(), ms(this, l, ps, ws, hs, { margin: 0 });
  }
}
const {
  SvelteComponent: ys,
  append: Fe,
  attr: ae,
  binding_callbacks: dt,
  check_outros: tn,
  create_component: vs,
  create_slot: Cs,
  destroy_component: js,
  destroy_each: nn,
  detach: L,
  element: he,
  empty: Re,
  ensure_array_like: al,
  get_all_dirty_from_scope: qs,
  get_slot_changes: Ss,
  group_outros: sn,
  init: Es,
  insert: z,
  mount_component: Ns,
  noop: Vl,
  safe_not_equal: Fs,
  set_data: ne,
  set_style: qe,
  space: _e,
  text: D,
  toggle_class: te,
  transition_in: He,
  transition_out: Je,
  update_slot_base: Ls
} = window.__gradio__svelte__internal, { tick: zs } = window.__gradio__svelte__internal, { onDestroy: Ms } = window.__gradio__svelte__internal, Os = (t) => ({}), mt = (t) => ({});
function bt(t, l, e) {
  const n = t.slice();
  return n[39] = l[e], n[41] = e, n;
}
function ht(t, l, e) {
  const n = t.slice();
  return n[39] = l[e], n;
}
function As(t) {
  let l, e = (
    /*i18n*/
    t[1]("common.error") + ""
  ), n, i, f;
  const u = (
    /*#slots*/
    t[29].error
  ), o = Cs(
    u,
    t,
    /*$$scope*/
    t[28],
    mt
  );
  return {
    c() {
      l = he("span"), n = D(e), i = _e(), o && o.c(), ae(l, "class", "error svelte-1yserjw");
    },
    m(s, r) {
      z(s, l, r), Fe(l, n), z(s, i, r), o && o.m(s, r), f = !0;
    },
    p(s, r) {
      (!f || r[0] & /*i18n*/
      2) && e !== (e = /*i18n*/
      s[1]("common.error") + "") && ne(n, e), o && o.p && (!f || r[0] & /*$$scope*/
      268435456) && Ls(
        o,
        u,
        s,
        /*$$scope*/
        s[28],
        f ? Ss(
          u,
          /*$$scope*/
          s[28],
          r,
          Os
        ) : qs(
          /*$$scope*/
          s[28]
        ),
        mt
      );
    },
    i(s) {
      f || (He(o, s), f = !0);
    },
    o(s) {
      Je(o, s), f = !1;
    },
    d(s) {
      s && (L(l), L(i)), o && o.d(s);
    }
  };
}
function Vs(t) {
  let l, e, n, i, f, u, o, s, r, a = (
    /*variant*/
    t[8] === "default" && /*show_eta_bar*/
    t[18] && /*show_progress*/
    t[6] === "full" && gt(t)
  );
  function m(c, h) {
    if (
      /*progress*/
      c[7]
    ) return Ts;
    if (
      /*queue_position*/
      c[2] !== null && /*queue_size*/
      c[3] !== void 0 && /*queue_position*/
      c[2] >= 0
    ) return Bs;
    if (
      /*queue_position*/
      c[2] === 0
    ) return Ds;
  }
  let w = m(t), p = w && w(t), q = (
    /*timer*/
    t[5] && kt(t)
  );
  const k = [Is, Ps], d = [];
  function _(c, h) {
    return (
      /*last_progress_level*/
      c[15] != null ? 0 : (
        /*show_progress*/
        c[6] === "full" ? 1 : -1
      )
    );
  }
  ~(f = _(t)) && (u = d[f] = k[f](t));
  let g = !/*timer*/
  t[5] && Et(t);
  return {
    c() {
      a && a.c(), l = _e(), e = he("div"), p && p.c(), n = _e(), q && q.c(), i = _e(), u && u.c(), o = _e(), g && g.c(), s = Re(), ae(e, "class", "progress-text svelte-1yserjw"), te(
        e,
        "meta-text-center",
        /*variant*/
        t[8] === "center"
      ), te(
        e,
        "meta-text",
        /*variant*/
        t[8] === "default"
      );
    },
    m(c, h) {
      a && a.m(c, h), z(c, l, h), z(c, e, h), p && p.m(e, null), Fe(e, n), q && q.m(e, null), z(c, i, h), ~f && d[f].m(c, h), z(c, o, h), g && g.m(c, h), z(c, s, h), r = !0;
    },
    p(c, h) {
      /*variant*/
      c[8] === "default" && /*show_eta_bar*/
      c[18] && /*show_progress*/
      c[6] === "full" ? a ? a.p(c, h) : (a = gt(c), a.c(), a.m(l.parentNode, l)) : a && (a.d(1), a = null), w === (w = m(c)) && p ? p.p(c, h) : (p && p.d(1), p = w && w(c), p && (p.c(), p.m(e, n))), /*timer*/
      c[5] ? q ? q.p(c, h) : (q = kt(c), q.c(), q.m(e, null)) : q && (q.d(1), q = null), (!r || h[0] & /*variant*/
      256) && te(
        e,
        "meta-text-center",
        /*variant*/
        c[8] === "center"
      ), (!r || h[0] & /*variant*/
      256) && te(
        e,
        "meta-text",
        /*variant*/
        c[8] === "default"
      );
      let S = f;
      f = _(c), f === S ? ~f && d[f].p(c, h) : (u && (sn(), Je(d[S], 1, 1, () => {
        d[S] = null;
      }), tn()), ~f ? (u = d[f], u ? u.p(c, h) : (u = d[f] = k[f](c), u.c()), He(u, 1), u.m(o.parentNode, o)) : u = null), /*timer*/
      c[5] ? g && (g.d(1), g = null) : g ? g.p(c, h) : (g = Et(c), g.c(), g.m(s.parentNode, s));
    },
    i(c) {
      r || (He(u), r = !0);
    },
    o(c) {
      Je(u), r = !1;
    },
    d(c) {
      c && (L(l), L(e), L(i), L(o), L(s)), a && a.d(c), p && p.d(), q && q.d(), ~f && d[f].d(c), g && g.d(c);
    }
  };
}
function gt(t) {
  let l, e = `translateX(${/*eta_level*/
  (t[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      l = he("div"), ae(l, "class", "eta-bar svelte-1yserjw"), qe(l, "transform", e);
    },
    m(n, i) {
      z(n, l, i);
    },
    p(n, i) {
      i[0] & /*eta_level*/
      131072 && e !== (e = `translateX(${/*eta_level*/
      (n[17] || 0) * 100 - 100}%)`) && qe(l, "transform", e);
    },
    d(n) {
      n && L(l);
    }
  };
}
function Ds(t) {
  let l;
  return {
    c() {
      l = D("processing |");
    },
    m(e, n) {
      z(e, l, n);
    },
    p: Vl,
    d(e) {
      e && L(l);
    }
  };
}
function Bs(t) {
  let l, e = (
    /*queue_position*/
    t[2] + 1 + ""
  ), n, i, f, u;
  return {
    c() {
      l = D("queue: "), n = D(e), i = D("/"), f = D(
        /*queue_size*/
        t[3]
      ), u = D(" |");
    },
    m(o, s) {
      z(o, l, s), z(o, n, s), z(o, i, s), z(o, f, s), z(o, u, s);
    },
    p(o, s) {
      s[0] & /*queue_position*/
      4 && e !== (e = /*queue_position*/
      o[2] + 1 + "") && ne(n, e), s[0] & /*queue_size*/
      8 && ne(
        f,
        /*queue_size*/
        o[3]
      );
    },
    d(o) {
      o && (L(l), L(n), L(i), L(f), L(u));
    }
  };
}
function Ts(t) {
  let l, e = al(
    /*progress*/
    t[7]
  ), n = [];
  for (let i = 0; i < e.length; i += 1)
    n[i] = pt(ht(t, e, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      l = Re();
    },
    m(i, f) {
      for (let u = 0; u < n.length; u += 1)
        n[u] && n[u].m(i, f);
      z(i, l, f);
    },
    p(i, f) {
      if (f[0] & /*progress*/
      128) {
        e = al(
          /*progress*/
          i[7]
        );
        let u;
        for (u = 0; u < e.length; u += 1) {
          const o = ht(i, e, u);
          n[u] ? n[u].p(o, f) : (n[u] = pt(o), n[u].c(), n[u].m(l.parentNode, l));
        }
        for (; u < n.length; u += 1)
          n[u].d(1);
        n.length = e.length;
      }
    },
    d(i) {
      i && L(l), nn(n, i);
    }
  };
}
function wt(t) {
  let l, e = (
    /*p*/
    t[39].unit + ""
  ), n, i, f = " ", u;
  function o(a, m) {
    return (
      /*p*/
      a[39].length != null ? Zs : Us
    );
  }
  let s = o(t), r = s(t);
  return {
    c() {
      r.c(), l = _e(), n = D(e), i = D(" | "), u = D(f);
    },
    m(a, m) {
      r.m(a, m), z(a, l, m), z(a, n, m), z(a, i, m), z(a, u, m);
    },
    p(a, m) {
      s === (s = o(a)) && r ? r.p(a, m) : (r.d(1), r = s(a), r && (r.c(), r.m(l.parentNode, l))), m[0] & /*progress*/
      128 && e !== (e = /*p*/
      a[39].unit + "") && ne(n, e);
    },
    d(a) {
      a && (L(l), L(n), L(i), L(u)), r.d(a);
    }
  };
}
function Us(t) {
  let l = Ue(
    /*p*/
    t[39].index || 0
  ) + "", e;
  return {
    c() {
      e = D(l);
    },
    m(n, i) {
      z(n, e, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && l !== (l = Ue(
        /*p*/
        n[39].index || 0
      ) + "") && ne(e, l);
    },
    d(n) {
      n && L(e);
    }
  };
}
function Zs(t) {
  let l = Ue(
    /*p*/
    t[39].index || 0
  ) + "", e, n, i = Ue(
    /*p*/
    t[39].length
  ) + "", f;
  return {
    c() {
      e = D(l), n = D("/"), f = D(i);
    },
    m(u, o) {
      z(u, e, o), z(u, n, o), z(u, f, o);
    },
    p(u, o) {
      o[0] & /*progress*/
      128 && l !== (l = Ue(
        /*p*/
        u[39].index || 0
      ) + "") && ne(e, l), o[0] & /*progress*/
      128 && i !== (i = Ue(
        /*p*/
        u[39].length
      ) + "") && ne(f, i);
    },
    d(u) {
      u && (L(e), L(n), L(f));
    }
  };
}
function pt(t) {
  let l, e = (
    /*p*/
    t[39].index != null && wt(t)
  );
  return {
    c() {
      e && e.c(), l = Re();
    },
    m(n, i) {
      e && e.m(n, i), z(n, l, i);
    },
    p(n, i) {
      /*p*/
      n[39].index != null ? e ? e.p(n, i) : (e = wt(n), e.c(), e.m(l.parentNode, l)) : e && (e.d(1), e = null);
    },
    d(n) {
      n && L(l), e && e.d(n);
    }
  };
}
function kt(t) {
  let l, e = (
    /*eta*/
    t[0] ? `/${/*formatted_eta*/
    t[19]}` : ""
  ), n, i;
  return {
    c() {
      l = D(
        /*formatted_timer*/
        t[20]
      ), n = D(e), i = D("s");
    },
    m(f, u) {
      z(f, l, u), z(f, n, u), z(f, i, u);
    },
    p(f, u) {
      u[0] & /*formatted_timer*/
      1048576 && ne(
        l,
        /*formatted_timer*/
        f[20]
      ), u[0] & /*eta, formatted_eta*/
      524289 && e !== (e = /*eta*/
      f[0] ? `/${/*formatted_eta*/
      f[19]}` : "") && ne(n, e);
    },
    d(f) {
      f && (L(l), L(n), L(i));
    }
  };
}
function Ps(t) {
  let l, e;
  return l = new ks({
    props: { margin: (
      /*variant*/
      t[8] === "default"
    ) }
  }), {
    c() {
      vs(l.$$.fragment);
    },
    m(n, i) {
      Ns(l, n, i), e = !0;
    },
    p(n, i) {
      const f = {};
      i[0] & /*variant*/
      256 && (f.margin = /*variant*/
      n[8] === "default"), l.$set(f);
    },
    i(n) {
      e || (He(l.$$.fragment, n), e = !0);
    },
    o(n) {
      Je(l.$$.fragment, n), e = !1;
    },
    d(n) {
      js(l, n);
    }
  };
}
function Is(t) {
  let l, e, n, i, f, u = `${/*last_progress_level*/
  t[15] * 100}%`, o = (
    /*progress*/
    t[7] != null && yt(t)
  );
  return {
    c() {
      l = he("div"), e = he("div"), o && o.c(), n = _e(), i = he("div"), f = he("div"), ae(e, "class", "progress-level-inner svelte-1yserjw"), ae(f, "class", "progress-bar svelte-1yserjw"), qe(f, "width", u), ae(i, "class", "progress-bar-wrap svelte-1yserjw"), ae(l, "class", "progress-level svelte-1yserjw");
    },
    m(s, r) {
      z(s, l, r), Fe(l, e), o && o.m(e, null), Fe(l, n), Fe(l, i), Fe(i, f), t[30](f);
    },
    p(s, r) {
      /*progress*/
      s[7] != null ? o ? o.p(s, r) : (o = yt(s), o.c(), o.m(e, null)) : o && (o.d(1), o = null), r[0] & /*last_progress_level*/
      32768 && u !== (u = `${/*last_progress_level*/
      s[15] * 100}%`) && qe(f, "width", u);
    },
    i: Vl,
    o: Vl,
    d(s) {
      s && L(l), o && o.d(), t[30](null);
    }
  };
}
function yt(t) {
  let l, e = al(
    /*progress*/
    t[7]
  ), n = [];
  for (let i = 0; i < e.length; i += 1)
    n[i] = St(bt(t, e, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      l = Re();
    },
    m(i, f) {
      for (let u = 0; u < n.length; u += 1)
        n[u] && n[u].m(i, f);
      z(i, l, f);
    },
    p(i, f) {
      if (f[0] & /*progress_level, progress*/
      16512) {
        e = al(
          /*progress*/
          i[7]
        );
        let u;
        for (u = 0; u < e.length; u += 1) {
          const o = bt(i, e, u);
          n[u] ? n[u].p(o, f) : (n[u] = St(o), n[u].c(), n[u].m(l.parentNode, l));
        }
        for (; u < n.length; u += 1)
          n[u].d(1);
        n.length = e.length;
      }
    },
    d(i) {
      i && L(l), nn(n, i);
    }
  };
}
function vt(t) {
  let l, e, n, i, f = (
    /*i*/
    t[41] !== 0 && Hs()
  ), u = (
    /*p*/
    t[39].desc != null && Ct(t)
  ), o = (
    /*p*/
    t[39].desc != null && /*progress_level*/
    t[14] && /*progress_level*/
    t[14][
      /*i*/
      t[41]
    ] != null && jt()
  ), s = (
    /*progress_level*/
    t[14] != null && qt(t)
  );
  return {
    c() {
      f && f.c(), l = _e(), u && u.c(), e = _e(), o && o.c(), n = _e(), s && s.c(), i = Re();
    },
    m(r, a) {
      f && f.m(r, a), z(r, l, a), u && u.m(r, a), z(r, e, a), o && o.m(r, a), z(r, n, a), s && s.m(r, a), z(r, i, a);
    },
    p(r, a) {
      /*p*/
      r[39].desc != null ? u ? u.p(r, a) : (u = Ct(r), u.c(), u.m(e.parentNode, e)) : u && (u.d(1), u = null), /*p*/
      r[39].desc != null && /*progress_level*/
      r[14] && /*progress_level*/
      r[14][
        /*i*/
        r[41]
      ] != null ? o || (o = jt(), o.c(), o.m(n.parentNode, n)) : o && (o.d(1), o = null), /*progress_level*/
      r[14] != null ? s ? s.p(r, a) : (s = qt(r), s.c(), s.m(i.parentNode, i)) : s && (s.d(1), s = null);
    },
    d(r) {
      r && (L(l), L(e), L(n), L(i)), f && f.d(r), u && u.d(r), o && o.d(r), s && s.d(r);
    }
  };
}
function Hs(t) {
  let l;
  return {
    c() {
      l = D(" /");
    },
    m(e, n) {
      z(e, l, n);
    },
    d(e) {
      e && L(l);
    }
  };
}
function Ct(t) {
  let l = (
    /*p*/
    t[39].desc + ""
  ), e;
  return {
    c() {
      e = D(l);
    },
    m(n, i) {
      z(n, e, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && l !== (l = /*p*/
      n[39].desc + "") && ne(e, l);
    },
    d(n) {
      n && L(e);
    }
  };
}
function jt(t) {
  let l;
  return {
    c() {
      l = D("-");
    },
    m(e, n) {
      z(e, l, n);
    },
    d(e) {
      e && L(l);
    }
  };
}
function qt(t) {
  let l = (100 * /*progress_level*/
  (t[14][
    /*i*/
    t[41]
  ] || 0)).toFixed(1) + "", e, n;
  return {
    c() {
      e = D(l), n = D("%");
    },
    m(i, f) {
      z(i, e, f), z(i, n, f);
    },
    p(i, f) {
      f[0] & /*progress_level*/
      16384 && l !== (l = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[41]
      ] || 0)).toFixed(1) + "") && ne(e, l);
    },
    d(i) {
      i && (L(e), L(n));
    }
  };
}
function St(t) {
  let l, e = (
    /*p*/
    (t[39].desc != null || /*progress_level*/
    t[14] && /*progress_level*/
    t[14][
      /*i*/
      t[41]
    ] != null) && vt(t)
  );
  return {
    c() {
      e && e.c(), l = Re();
    },
    m(n, i) {
      e && e.m(n, i), z(n, l, i);
    },
    p(n, i) {
      /*p*/
      n[39].desc != null || /*progress_level*/
      n[14] && /*progress_level*/
      n[14][
        /*i*/
        n[41]
      ] != null ? e ? e.p(n, i) : (e = vt(n), e.c(), e.m(l.parentNode, l)) : e && (e.d(1), e = null);
    },
    d(n) {
      n && L(l), e && e.d(n);
    }
  };
}
function Et(t) {
  let l, e;
  return {
    c() {
      l = he("p"), e = D(
        /*loading_text*/
        t[9]
      ), ae(l, "class", "loading svelte-1yserjw");
    },
    m(n, i) {
      z(n, l, i), Fe(l, e);
    },
    p(n, i) {
      i[0] & /*loading_text*/
      512 && ne(
        e,
        /*loading_text*/
        n[9]
      );
    },
    d(n) {
      n && L(l);
    }
  };
}
function Js(t) {
  let l, e, n, i, f;
  const u = [Vs, As], o = [];
  function s(r, a) {
    return (
      /*status*/
      r[4] === "pending" ? 0 : (
        /*status*/
        r[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(e = s(t)) && (n = o[e] = u[e](t)), {
    c() {
      l = he("div"), n && n.c(), ae(l, "class", i = "wrap " + /*variant*/
      t[8] + " " + /*show_progress*/
      t[6] + " svelte-1yserjw"), te(l, "hide", !/*status*/
      t[4] || /*status*/
      t[4] === "complete" || /*show_progress*/
      t[6] === "hidden"), te(
        l,
        "translucent",
        /*variant*/
        t[8] === "center" && /*status*/
        (t[4] === "pending" || /*status*/
        t[4] === "error") || /*translucent*/
        t[11] || /*show_progress*/
        t[6] === "minimal"
      ), te(
        l,
        "generating",
        /*status*/
        t[4] === "generating"
      ), te(
        l,
        "border",
        /*border*/
        t[12]
      ), qe(
        l,
        "position",
        /*absolute*/
        t[10] ? "absolute" : "static"
      ), qe(
        l,
        "padding",
        /*absolute*/
        t[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(r, a) {
      z(r, l, a), ~e && o[e].m(l, null), t[31](l), f = !0;
    },
    p(r, a) {
      let m = e;
      e = s(r), e === m ? ~e && o[e].p(r, a) : (n && (sn(), Je(o[m], 1, 1, () => {
        o[m] = null;
      }), tn()), ~e ? (n = o[e], n ? n.p(r, a) : (n = o[e] = u[e](r), n.c()), He(n, 1), n.m(l, null)) : n = null), (!f || a[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      r[8] + " " + /*show_progress*/
      r[6] + " svelte-1yserjw")) && ae(l, "class", i), (!f || a[0] & /*variant, show_progress, status, show_progress*/
      336) && te(l, "hide", !/*status*/
      r[4] || /*status*/
      r[4] === "complete" || /*show_progress*/
      r[6] === "hidden"), (!f || a[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && te(
        l,
        "translucent",
        /*variant*/
        r[8] === "center" && /*status*/
        (r[4] === "pending" || /*status*/
        r[4] === "error") || /*translucent*/
        r[11] || /*show_progress*/
        r[6] === "minimal"
      ), (!f || a[0] & /*variant, show_progress, status*/
      336) && te(
        l,
        "generating",
        /*status*/
        r[4] === "generating"
      ), (!f || a[0] & /*variant, show_progress, border*/
      4416) && te(
        l,
        "border",
        /*border*/
        r[12]
      ), a[0] & /*absolute*/
      1024 && qe(
        l,
        "position",
        /*absolute*/
        r[10] ? "absolute" : "static"
      ), a[0] & /*absolute*/
      1024 && qe(
        l,
        "padding",
        /*absolute*/
        r[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(r) {
      f || (He(n), f = !0);
    },
    o(r) {
      Je(n), f = !1;
    },
    d(r) {
      r && L(l), ~e && o[e].d(), t[31](null);
    }
  };
}
var Rs = function(t, l, e, n) {
  function i(f) {
    return f instanceof e ? f : new e(function(u) {
      u(f);
    });
  }
  return new (e || (e = Promise))(function(f, u) {
    function o(a) {
      try {
        r(n.next(a));
      } catch (m) {
        u(m);
      }
    }
    function s(a) {
      try {
        r(n.throw(a));
      } catch (m) {
        u(m);
      }
    }
    function r(a) {
      a.done ? f(a.value) : i(a.value).then(o, s);
    }
    r((n = n.apply(t, l || [])).next());
  });
};
let il = [], El = !1;
function Xs(t) {
  return Rs(this, arguments, void 0, function* (l, e = !0) {
    if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && e !== !0)) {
      if (il.push(l), !El) El = !0;
      else return;
      yield zs(), requestAnimationFrame(() => {
        let n = [0, 0];
        for (let i = 0; i < il.length; i++) {
          const u = il[i].getBoundingClientRect();
          (i === 0 || u.top + window.scrollY <= n[0]) && (n[0] = u.top + window.scrollY, n[1] = i);
        }
        window.scrollTo({ top: n[0] - 20, behavior: "smooth" }), El = !1, il = [];
      });
    }
  });
}
function Ys(t, l, e) {
  let n, { $$slots: i = {}, $$scope: f } = l;
  this && this.__awaiter;
  let { i18n: u } = l, { eta: o = null } = l, { queue_position: s } = l, { queue_size: r } = l, { status: a } = l, { scroll_to_output: m = !1 } = l, { timer: w = !0 } = l, { show_progress: p = "full" } = l, { message: q = null } = l, { progress: k = null } = l, { variant: d = "default" } = l, { loading_text: _ = "Loading..." } = l, { absolute: g = !0 } = l, { translucent: c = !1 } = l, { border: h = !1 } = l, { autoscroll: S } = l, y, N = !1, j = 0, E = 0, T = null, U = null, le = 0, F = null, I, H = null, de = !0;
  const pe = () => {
    e(0, o = e(26, T = e(19, b = null))), e(24, j = performance.now()), e(25, E = 0), N = !0, ke();
  };
  function ke() {
    requestAnimationFrame(() => {
      e(25, E = (performance.now() - j) / 1e3), N && ke();
    });
  }
  function ye() {
    e(25, E = 0), e(0, o = e(26, T = e(19, b = null))), N && (N = !1);
  }
  Ms(() => {
    N && ye();
  });
  let b = null;
  function G(C) {
    dt[C ? "unshift" : "push"](() => {
      H = C, e(16, H), e(7, k), e(14, F), e(15, I);
    });
  }
  function K(C) {
    dt[C ? "unshift" : "push"](() => {
      y = C, e(13, y);
    });
  }
  return t.$$set = (C) => {
    "i18n" in C && e(1, u = C.i18n), "eta" in C && e(0, o = C.eta), "queue_position" in C && e(2, s = C.queue_position), "queue_size" in C && e(3, r = C.queue_size), "status" in C && e(4, a = C.status), "scroll_to_output" in C && e(21, m = C.scroll_to_output), "timer" in C && e(5, w = C.timer), "show_progress" in C && e(6, p = C.show_progress), "message" in C && e(22, q = C.message), "progress" in C && e(7, k = C.progress), "variant" in C && e(8, d = C.variant), "loading_text" in C && e(9, _ = C.loading_text), "absolute" in C && e(10, g = C.absolute), "translucent" in C && e(11, c = C.translucent), "border" in C && e(12, h = C.border), "autoscroll" in C && e(23, S = C.autoscroll), "$$scope" in C && e(28, f = C.$$scope);
  }, t.$$.update = () => {
    t.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    218103809 && (o === null && e(0, o = T), o != null && T !== o && (e(27, U = (performance.now() - j) / 1e3 + o), e(19, b = U.toFixed(1)), e(26, T = o))), t.$$.dirty[0] & /*eta_from_start, timer_diff*/
    167772160 && e(17, le = U === null || U <= 0 || !E ? null : Math.min(E / U, 1)), t.$$.dirty[0] & /*progress*/
    128 && k != null && e(18, de = !1), t.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (k != null ? e(14, F = k.map((C) => {
      if (C.index != null && C.length != null)
        return C.index / C.length;
      if (C.progress != null)
        return C.progress;
    })) : e(14, F = null), F ? (e(15, I = F[F.length - 1]), H && (I === 0 ? e(16, H.style.transition = "0", H) : e(16, H.style.transition = "150ms", H))) : e(15, I = void 0)), t.$$.dirty[0] & /*status*/
    16 && (a === "pending" ? pe() : ye()), t.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    10493968 && y && m && (a === "pending" || a === "complete") && Xs(y, S), t.$$.dirty[0] & /*status, message*/
    4194320, t.$$.dirty[0] & /*timer_diff*/
    33554432 && e(20, n = E.toFixed(1));
  }, [
    o,
    u,
    s,
    r,
    a,
    w,
    p,
    k,
    d,
    _,
    g,
    c,
    h,
    y,
    F,
    I,
    H,
    le,
    de,
    b,
    n,
    m,
    q,
    S,
    j,
    E,
    T,
    U,
    f,
    i,
    G,
    K
  ];
}
class Gs extends ys {
  constructor(l) {
    super(), Es(
      this,
      l,
      Ys,
      Js,
      Fs,
      {
        i18n: 1,
        eta: 0,
        queue_position: 2,
        queue_size: 3,
        status: 4,
        scroll_to_output: 21,
        timer: 5,
        show_progress: 6,
        message: 22,
        progress: 7,
        variant: 8,
        loading_text: 9,
        absolute: 10,
        translucent: 11,
        border: 12,
        autoscroll: 23
      },
      null,
      [-1, -1]
    );
  }
}
class Ks {
  constructor({
    name: l,
    token: e,
    param_specs: n
  }) {
    this.name = l, this.token = e, this.param_specs = n || new Object();
  }
}
const {
  SvelteComponent: Qs,
  append: on,
  attr: V,
  bubble: Ws,
  check_outros: xs,
  create_slot: fn,
  detach: el,
  element: hl,
  empty: $s,
  get_all_dirty_from_scope: un,
  get_slot_changes: rn,
  group_outros: eo,
  init: lo,
  insert: ll,
  listen: to,
  safe_not_equal: no,
  set_style: Q,
  space: an,
  src_url_equal: _l,
  toggle_class: Ze,
  transition_in: cl,
  transition_out: dl,
  update_slot_base: _n
} = window.__gradio__svelte__internal;
function io(t) {
  let l, e, n, i, f, u, o = (
    /*icon*/
    t[7] && Nt(t)
  );
  const s = (
    /*#slots*/
    t[12].default
  ), r = fn(
    s,
    t,
    /*$$scope*/
    t[11],
    null
  );
  return {
    c() {
      l = hl("button"), o && o.c(), e = an(), r && r.c(), V(l, "class", n = /*size*/
      t[4] + " " + /*variant*/
      t[3] + " " + /*elem_classes*/
      t[1].join(" ") + " svelte-8huxfn"), V(
        l,
        "id",
        /*elem_id*/
        t[0]
      ), l.disabled = /*disabled*/
      t[8], Ze(l, "hidden", !/*visible*/
      t[2]), Q(
        l,
        "flex-grow",
        /*scale*/
        t[9]
      ), Q(
        l,
        "width",
        /*scale*/
        t[9] === 0 ? "fit-content" : null
      ), Q(l, "min-width", typeof /*min_width*/
      t[10] == "number" ? `calc(min(${/*min_width*/
      t[10]}px, 100%))` : null);
    },
    m(a, m) {
      ll(a, l, m), o && o.m(l, null), on(l, e), r && r.m(l, null), i = !0, f || (u = to(
        l,
        "click",
        /*click_handler*/
        t[13]
      ), f = !0);
    },
    p(a, m) {
      /*icon*/
      a[7] ? o ? o.p(a, m) : (o = Nt(a), o.c(), o.m(l, e)) : o && (o.d(1), o = null), r && r.p && (!i || m & /*$$scope*/
      2048) && _n(
        r,
        s,
        a,
        /*$$scope*/
        a[11],
        i ? rn(
          s,
          /*$$scope*/
          a[11],
          m,
          null
        ) : un(
          /*$$scope*/
          a[11]
        ),
        null
      ), (!i || m & /*size, variant, elem_classes*/
      26 && n !== (n = /*size*/
      a[4] + " " + /*variant*/
      a[3] + " " + /*elem_classes*/
      a[1].join(" ") + " svelte-8huxfn")) && V(l, "class", n), (!i || m & /*elem_id*/
      1) && V(
        l,
        "id",
        /*elem_id*/
        a[0]
      ), (!i || m & /*disabled*/
      256) && (l.disabled = /*disabled*/
      a[8]), (!i || m & /*size, variant, elem_classes, visible*/
      30) && Ze(l, "hidden", !/*visible*/
      a[2]), m & /*scale*/
      512 && Q(
        l,
        "flex-grow",
        /*scale*/
        a[9]
      ), m & /*scale*/
      512 && Q(
        l,
        "width",
        /*scale*/
        a[9] === 0 ? "fit-content" : null
      ), m & /*min_width*/
      1024 && Q(l, "min-width", typeof /*min_width*/
      a[10] == "number" ? `calc(min(${/*min_width*/
      a[10]}px, 100%))` : null);
    },
    i(a) {
      i || (cl(r, a), i = !0);
    },
    o(a) {
      dl(r, a), i = !1;
    },
    d(a) {
      a && el(l), o && o.d(), r && r.d(a), f = !1, u();
    }
  };
}
function so(t) {
  let l, e, n, i, f = (
    /*icon*/
    t[7] && Ft(t)
  );
  const u = (
    /*#slots*/
    t[12].default
  ), o = fn(
    u,
    t,
    /*$$scope*/
    t[11],
    null
  );
  return {
    c() {
      l = hl("a"), f && f.c(), e = an(), o && o.c(), V(
        l,
        "href",
        /*link*/
        t[6]
      ), V(l, "rel", "noopener noreferrer"), V(
        l,
        "aria-disabled",
        /*disabled*/
        t[8]
      ), V(l, "class", n = /*size*/
      t[4] + " " + /*variant*/
      t[3] + " " + /*elem_classes*/
      t[1].join(" ") + " svelte-8huxfn"), V(
        l,
        "id",
        /*elem_id*/
        t[0]
      ), Ze(l, "hidden", !/*visible*/
      t[2]), Ze(
        l,
        "disabled",
        /*disabled*/
        t[8]
      ), Q(
        l,
        "flex-grow",
        /*scale*/
        t[9]
      ), Q(
        l,
        "pointer-events",
        /*disabled*/
        t[8] ? "none" : null
      ), Q(
        l,
        "width",
        /*scale*/
        t[9] === 0 ? "fit-content" : null
      ), Q(l, "min-width", typeof /*min_width*/
      t[10] == "number" ? `calc(min(${/*min_width*/
      t[10]}px, 100%))` : null);
    },
    m(s, r) {
      ll(s, l, r), f && f.m(l, null), on(l, e), o && o.m(l, null), i = !0;
    },
    p(s, r) {
      /*icon*/
      s[7] ? f ? f.p(s, r) : (f = Ft(s), f.c(), f.m(l, e)) : f && (f.d(1), f = null), o && o.p && (!i || r & /*$$scope*/
      2048) && _n(
        o,
        u,
        s,
        /*$$scope*/
        s[11],
        i ? rn(
          u,
          /*$$scope*/
          s[11],
          r,
          null
        ) : un(
          /*$$scope*/
          s[11]
        ),
        null
      ), (!i || r & /*link*/
      64) && V(
        l,
        "href",
        /*link*/
        s[6]
      ), (!i || r & /*disabled*/
      256) && V(
        l,
        "aria-disabled",
        /*disabled*/
        s[8]
      ), (!i || r & /*size, variant, elem_classes*/
      26 && n !== (n = /*size*/
      s[4] + " " + /*variant*/
      s[3] + " " + /*elem_classes*/
      s[1].join(" ") + " svelte-8huxfn")) && V(l, "class", n), (!i || r & /*elem_id*/
      1) && V(
        l,
        "id",
        /*elem_id*/
        s[0]
      ), (!i || r & /*size, variant, elem_classes, visible*/
      30) && Ze(l, "hidden", !/*visible*/
      s[2]), (!i || r & /*size, variant, elem_classes, disabled*/
      282) && Ze(
        l,
        "disabled",
        /*disabled*/
        s[8]
      ), r & /*scale*/
      512 && Q(
        l,
        "flex-grow",
        /*scale*/
        s[9]
      ), r & /*disabled*/
      256 && Q(
        l,
        "pointer-events",
        /*disabled*/
        s[8] ? "none" : null
      ), r & /*scale*/
      512 && Q(
        l,
        "width",
        /*scale*/
        s[9] === 0 ? "fit-content" : null
      ), r & /*min_width*/
      1024 && Q(l, "min-width", typeof /*min_width*/
      s[10] == "number" ? `calc(min(${/*min_width*/
      s[10]}px, 100%))` : null);
    },
    i(s) {
      i || (cl(o, s), i = !0);
    },
    o(s) {
      dl(o, s), i = !1;
    },
    d(s) {
      s && el(l), f && f.d(), o && o.d(s);
    }
  };
}
function Nt(t) {
  let l, e, n;
  return {
    c() {
      l = hl("img"), V(l, "class", "button-icon svelte-8huxfn"), _l(l.src, e = /*icon*/
      t[7].url) || V(l, "src", e), V(l, "alt", n = `${/*value*/
      t[5]} icon`);
    },
    m(i, f) {
      ll(i, l, f);
    },
    p(i, f) {
      f & /*icon*/
      128 && !_l(l.src, e = /*icon*/
      i[7].url) && V(l, "src", e), f & /*value*/
      32 && n !== (n = `${/*value*/
      i[5]} icon`) && V(l, "alt", n);
    },
    d(i) {
      i && el(l);
    }
  };
}
function Ft(t) {
  let l, e, n;
  return {
    c() {
      l = hl("img"), V(l, "class", "button-icon svelte-8huxfn"), _l(l.src, e = /*icon*/
      t[7].url) || V(l, "src", e), V(l, "alt", n = `${/*value*/
      t[5]} icon`);
    },
    m(i, f) {
      ll(i, l, f);
    },
    p(i, f) {
      f & /*icon*/
      128 && !_l(l.src, e = /*icon*/
      i[7].url) && V(l, "src", e), f & /*value*/
      32 && n !== (n = `${/*value*/
      i[5]} icon`) && V(l, "alt", n);
    },
    d(i) {
      i && el(l);
    }
  };
}
function oo(t) {
  let l, e, n, i;
  const f = [so, io], u = [];
  function o(s, r) {
    return (
      /*link*/
      s[6] && /*link*/
      s[6].length > 0 ? 0 : 1
    );
  }
  return l = o(t), e = u[l] = f[l](t), {
    c() {
      e.c(), n = $s();
    },
    m(s, r) {
      u[l].m(s, r), ll(s, n, r), i = !0;
    },
    p(s, [r]) {
      let a = l;
      l = o(s), l === a ? u[l].p(s, r) : (eo(), dl(u[a], 1, 1, () => {
        u[a] = null;
      }), xs(), e = u[l], e ? e.p(s, r) : (e = u[l] = f[l](s), e.c()), cl(e, 1), e.m(n.parentNode, n));
    },
    i(s) {
      i || (cl(e), i = !0);
    },
    o(s) {
      dl(e), i = !1;
    },
    d(s) {
      s && el(n), u[l].d(s);
    }
  };
}
function fo(t, l, e) {
  let { $$slots: n = {}, $$scope: i } = l, { elem_id: f = "" } = l, { elem_classes: u = [] } = l, { visible: o = !0 } = l, { variant: s = "secondary" } = l, { size: r = "lg" } = l, { value: a = null } = l, { link: m = null } = l, { icon: w = null } = l, { disabled: p = !1 } = l, { scale: q = null } = l, { min_width: k = void 0 } = l;
  function d(_) {
    Ws.call(this, t, _);
  }
  return t.$$set = (_) => {
    "elem_id" in _ && e(0, f = _.elem_id), "elem_classes" in _ && e(1, u = _.elem_classes), "visible" in _ && e(2, o = _.visible), "variant" in _ && e(3, s = _.variant), "size" in _ && e(4, r = _.size), "value" in _ && e(5, a = _.value), "link" in _ && e(6, m = _.link), "icon" in _ && e(7, w = _.icon), "disabled" in _ && e(8, p = _.disabled), "scale" in _ && e(9, q = _.scale), "min_width" in _ && e(10, k = _.min_width), "$$scope" in _ && e(11, i = _.$$scope);
  }, [
    f,
    u,
    o,
    s,
    r,
    a,
    m,
    w,
    p,
    q,
    k,
    i,
    n,
    d
  ];
}
class uo extends Qs {
  constructor(l) {
    super(), lo(this, l, fo, oo, no, {
      elem_id: 0,
      elem_classes: 1,
      visible: 2,
      variant: 3,
      size: 4,
      value: 5,
      link: 6,
      icon: 7,
      disabled: 8,
      scale: 9,
      min_width: 10
    });
  }
}
const {
  SvelteComponent: ro,
  attr: ao,
  detach: _o,
  element: co,
  init: mo,
  insert: bo,
  noop: Lt,
  safe_not_equal: ho,
  toggle_class: Ae
} = window.__gradio__svelte__internal;
function go(t) {
  let l;
  return {
    c() {
      l = co("div"), l.textContent = `${/*names_string*/
      t[2]}`, ao(l, "class", "svelte-1gecy8w"), Ae(
        l,
        "table",
        /*type*/
        t[0] === "table"
      ), Ae(
        l,
        "gallery",
        /*type*/
        t[0] === "gallery"
      ), Ae(
        l,
        "selected",
        /*selected*/
        t[1]
      );
    },
    m(e, n) {
      bo(e, l, n);
    },
    p(e, [n]) {
      n & /*type*/
      1 && Ae(
        l,
        "table",
        /*type*/
        e[0] === "table"
      ), n & /*type*/
      1 && Ae(
        l,
        "gallery",
        /*type*/
        e[0] === "gallery"
      ), n & /*selected*/
      2 && Ae(
        l,
        "selected",
        /*selected*/
        e[1]
      );
    },
    i: Lt,
    o: Lt,
    d(e) {
      e && _o(l);
    }
  };
}
function wo(t, l, e) {
  let { value: n } = l, { type: i } = l, { selected: f = !1 } = l, { choices: u } = l, r = (n ? Array.isArray(n) ? n : [n] : []).map((a) => {
    var m;
    return (m = u.find((w) => w[1] === a)) === null || m === void 0 ? void 0 : m[0];
  }).filter((a) => a !== void 0).join(", ");
  return t.$$set = (a) => {
    "value" in a && e(3, n = a.value), "type" in a && e(0, i = a.type), "selected" in a && e(1, f = a.selected), "choices" in a && e(4, u = a.choices);
  }, [i, f, r, n, u];
}
class Yo extends ro {
  constructor(l) {
    super(), mo(this, l, wo, go, ho, {
      value: 3,
      type: 0,
      selected: 1,
      choices: 4
    });
  }
}
const {
  SvelteComponent: po,
  append: fe,
  attr: P,
  binding_callbacks: ko,
  check_outros: ml,
  create_component: We,
  destroy_component: xe,
  destroy_each: yo,
  detach: ge,
  element: ue,
  ensure_array_like: zt,
  group_outros: bl,
  init: vo,
  insert: we,
  listen: me,
  mount_component: $e,
  prevent_default: Mt,
  run_all: Pl,
  safe_not_equal: Co,
  set_data: Il,
  set_input_value: Ot,
  space: Pe,
  text: Hl,
  toggle_class: Ve,
  transition_in: J,
  transition_out: ee
} = window.__gradio__svelte__internal, { afterUpdate: jo, createEventDispatcher: qo } = window.__gradio__svelte__internal;
function At(t, l, e) {
  const n = t.slice();
  return n[40] = l[e], n;
}
function So(t) {
  let l;
  return {
    c() {
      l = Hl(
        /*label*/
        t[0]
      );
    },
    m(e, n) {
      we(e, l, n);
    },
    p(e, n) {
      n[0] & /*label*/
      1 && Il(
        l,
        /*label*/
        e[0]
      );
    },
    d(e) {
      e && ge(l);
    }
  };
}
function Eo(t) {
  let l = (
    /*s*/
    t[40] + ""
  ), e;
  return {
    c() {
      e = Hl(l);
    },
    m(n, i) {
      we(n, e, i);
    },
    p(n, i) {
      i[0] & /*selected_indices*/
      4096 && l !== (l = /*s*/
      n[40] + "") && Il(e, l);
    },
    d(n) {
      n && ge(e);
    }
  };
}
function No(t) {
  let l = (
    /*choices_names*/
    t[15][
      /*s*/
      t[40]
    ] + ""
  ), e;
  return {
    c() {
      e = Hl(l);
    },
    m(n, i) {
      we(n, e, i);
    },
    p(n, i) {
      i[0] & /*choices_names, selected_indices*/
      36864 && l !== (l = /*choices_names*/
      n[15][
        /*s*/
        n[40]
      ] + "") && Il(e, l);
    },
    d(n) {
      n && ge(e);
    }
  };
}
function Vt(t) {
  let l, e, n, i, f, u;
  e = new $t({});
  function o() {
    return (
      /*click_handler*/
      t[31](
        /*s*/
        t[40]
      )
    );
  }
  function s(...r) {
    return (
      /*keydown_handler*/
      t[32](
        /*s*/
        t[40],
        ...r
      )
    );
  }
  return {
    c() {
      l = ue("div"), We(e.$$.fragment), P(l, "class", "token-remove svelte-xtjjyg"), P(l, "role", "button"), P(l, "tabindex", "0"), P(l, "title", n = /*i18n*/
      t[9]("common.remove") + " " + /*s*/
      t[40]);
    },
    m(r, a) {
      we(r, l, a), $e(e, l, null), i = !0, f || (u = [
        me(l, "click", Mt(o)),
        me(l, "keydown", Mt(s))
      ], f = !0);
    },
    p(r, a) {
      t = r, (!i || a[0] & /*i18n, selected_indices*/
      4608 && n !== (n = /*i18n*/
      t[9]("common.remove") + " " + /*s*/
      t[40])) && P(l, "title", n);
    },
    i(r) {
      i || (J(e.$$.fragment, r), i = !0);
    },
    o(r) {
      ee(e.$$.fragment, r), i = !1;
    },
    d(r) {
      r && ge(l), xe(e), f = !1, Pl(u);
    }
  };
}
function Dt(t) {
  let l, e, n, i;
  function f(r, a) {
    return typeof /*s*/
    r[40] == "number" ? No : Eo;
  }
  let u = f(t), o = u(t), s = !/*disabled*/
  t[4] && Vt(t);
  return {
    c() {
      l = ue("div"), e = ue("span"), o.c(), n = Pe(), s && s.c(), P(e, "class", "svelte-xtjjyg"), P(l, "class", "token svelte-xtjjyg");
    },
    m(r, a) {
      we(r, l, a), fe(l, e), o.m(e, null), fe(l, n), s && s.m(l, null), i = !0;
    },
    p(r, a) {
      u === (u = f(r)) && o ? o.p(r, a) : (o.d(1), o = u(r), o && (o.c(), o.m(e, null))), /*disabled*/
      r[4] ? s && (bl(), ee(s, 1, 1, () => {
        s = null;
      }), ml()) : s ? (s.p(r, a), a[0] & /*disabled*/
      16 && J(s, 1)) : (s = Vt(r), s.c(), J(s, 1), s.m(l, null));
    },
    i(r) {
      i || (J(s), i = !0);
    },
    o(r) {
      ee(s), i = !1;
    },
    d(r) {
      r && ge(l), o.d(), s && s.d();
    }
  };
}
function Bt(t) {
  let l, e, n, i, f = (
    /*selected_indices*/
    t[12].length > 0 && Tt(t)
  );
  return n = new xt({}), {
    c() {
      f && f.c(), l = Pe(), e = ue("span"), We(n.$$.fragment), P(e, "class", "icon-wrap svelte-xtjjyg");
    },
    m(u, o) {
      f && f.m(u, o), we(u, l, o), we(u, e, o), $e(n, e, null), i = !0;
    },
    p(u, o) {
      /*selected_indices*/
      u[12].length > 0 ? f ? (f.p(u, o), o[0] & /*selected_indices*/
      4096 && J(f, 1)) : (f = Tt(u), f.c(), J(f, 1), f.m(l.parentNode, l)) : f && (bl(), ee(f, 1, 1, () => {
        f = null;
      }), ml());
    },
    i(u) {
      i || (J(f), J(n.$$.fragment, u), i = !0);
    },
    o(u) {
      ee(f), ee(n.$$.fragment, u), i = !1;
    },
    d(u) {
      u && (ge(l), ge(e)), f && f.d(u), xe(n);
    }
  };
}
function Tt(t) {
  let l, e, n, i, f, u;
  return e = new $t({}), {
    c() {
      l = ue("div"), We(e.$$.fragment), P(l, "role", "button"), P(l, "tabindex", "0"), P(l, "class", "token-remove remove-all svelte-xtjjyg"), P(l, "title", n = /*i18n*/
      t[9]("common.clear"));
    },
    m(o, s) {
      we(o, l, s), $e(e, l, null), i = !0, f || (u = [
        me(
          l,
          "click",
          /*remove_all*/
          t[21]
        ),
        me(
          l,
          "keydown",
          /*keydown_handler_1*/
          t[36]
        )
      ], f = !0);
    },
    p(o, s) {
      (!i || s[0] & /*i18n*/
      512 && n !== (n = /*i18n*/
      o[9]("common.clear"))) && P(l, "title", n);
    },
    i(o) {
      i || (J(e.$$.fragment, o), i = !0);
    },
    o(o) {
      ee(e.$$.fragment, o), i = !1;
    },
    d(o) {
      o && ge(l), xe(e), f = !1, Pl(u);
    }
  };
}
function Fo(t) {
  let l, e, n, i, f, u, o, s, r, a, m, w, p, q, k;
  e = new Wt({
    props: {
      show_label: (
        /*show_label*/
        t[5]
      ),
      info: (
        /*info*/
        t[1]
      ),
      $$slots: { default: [So] },
      $$scope: { ctx: t }
    }
  });
  let d = zt(
    /*selected_indices*/
    t[12]
  ), _ = [];
  for (let h = 0; h < d.length; h += 1)
    _[h] = Dt(At(t, d, h));
  const g = (h) => ee(_[h], 1, 1, () => {
    _[h] = null;
  });
  let c = !/*disabled*/
  t[4] && Bt(t);
  return w = new Gt({
    props: {
      show_options: (
        /*show_options*/
        t[14]
      ),
      choices: (
        /*choices*/
        t[3]
      ),
      filtered_indices: (
        /*filtered_indices*/
        t[11]
      ),
      disabled: (
        /*disabled*/
        t[4]
      ),
      selected_indices: (
        /*selected_indices*/
        t[12]
      ),
      active_index: (
        /*active_index*/
        t[16]
      )
    }
  }), w.$on(
    "change",
    /*handle_option_selected*/
    t[20]
  ), {
    c() {
      l = ue("label"), We(e.$$.fragment), n = Pe(), i = ue("div"), f = ue("div");
      for (let h = 0; h < _.length; h += 1)
        _[h].c();
      u = Pe(), o = ue("div"), s = ue("input"), a = Pe(), c && c.c(), m = Pe(), We(w.$$.fragment), P(s, "class", "border-none svelte-xtjjyg"), s.disabled = /*disabled*/
      t[4], P(s, "autocomplete", "off"), s.readOnly = r = !/*filterable*/
      t[8], Ve(s, "subdued", !/*choices_names*/
      t[15].includes(
        /*input_text*/
        t[10]
      ) && !/*allow_custom_value*/
      t[7] || /*selected_indices*/
      t[12].length === /*max_choices*/
      t[2]), P(o, "class", "secondary-wrap svelte-xtjjyg"), P(f, "class", "wrap-inner svelte-xtjjyg"), Ve(
        f,
        "show_options",
        /*show_options*/
        t[14]
      ), P(i, "class", "wrap svelte-xtjjyg"), P(l, "class", "svelte-xtjjyg"), Ve(
        l,
        "container",
        /*container*/
        t[6]
      );
    },
    m(h, S) {
      we(h, l, S), $e(e, l, null), fe(l, n), fe(l, i), fe(i, f);
      for (let y = 0; y < _.length; y += 1)
        _[y] && _[y].m(f, null);
      fe(f, u), fe(f, o), fe(o, s), Ot(
        s,
        /*input_text*/
        t[10]
      ), t[34](s), fe(o, a), c && c.m(o, null), fe(i, m), $e(w, i, null), p = !0, q || (k = [
        me(
          s,
          "input",
          /*input_input_handler*/
          t[33]
        ),
        me(
          s,
          "keydown",
          /*handle_key_down*/
          t[23]
        ),
        me(
          s,
          "keyup",
          /*keyup_handler*/
          t[35]
        ),
        me(
          s,
          "blur",
          /*handle_blur*/
          t[18]
        ),
        me(
          s,
          "focus",
          /*handle_focus*/
          t[22]
        )
      ], q = !0);
    },
    p(h, S) {
      const y = {};
      if (S[0] & /*show_label*/
      32 && (y.show_label = /*show_label*/
      h[5]), S[0] & /*info*/
      2 && (y.info = /*info*/
      h[1]), S[0] & /*label*/
      1 | S[1] & /*$$scope*/
      4096 && (y.$$scope = { dirty: S, ctx: h }), e.$set(y), S[0] & /*i18n, selected_indices, remove_selected_choice, disabled, choices_names*/
      561680) {
        d = zt(
          /*selected_indices*/
          h[12]
        );
        let j;
        for (j = 0; j < d.length; j += 1) {
          const E = At(h, d, j);
          _[j] ? (_[j].p(E, S), J(_[j], 1)) : (_[j] = Dt(E), _[j].c(), J(_[j], 1), _[j].m(f, u));
        }
        for (bl(), j = d.length; j < _.length; j += 1)
          g(j);
        ml();
      }
      (!p || S[0] & /*disabled*/
      16) && (s.disabled = /*disabled*/
      h[4]), (!p || S[0] & /*filterable*/
      256 && r !== (r = !/*filterable*/
      h[8])) && (s.readOnly = r), S[0] & /*input_text*/
      1024 && s.value !== /*input_text*/
      h[10] && Ot(
        s,
        /*input_text*/
        h[10]
      ), (!p || S[0] & /*choices_names, input_text, allow_custom_value, selected_indices, max_choices*/
      38020) && Ve(s, "subdued", !/*choices_names*/
      h[15].includes(
        /*input_text*/
        h[10]
      ) && !/*allow_custom_value*/
      h[7] || /*selected_indices*/
      h[12].length === /*max_choices*/
      h[2]), /*disabled*/
      h[4] ? c && (bl(), ee(c, 1, 1, () => {
        c = null;
      }), ml()) : c ? (c.p(h, S), S[0] & /*disabled*/
      16 && J(c, 1)) : (c = Bt(h), c.c(), J(c, 1), c.m(o, null)), (!p || S[0] & /*show_options*/
      16384) && Ve(
        f,
        "show_options",
        /*show_options*/
        h[14]
      );
      const N = {};
      S[0] & /*show_options*/
      16384 && (N.show_options = /*show_options*/
      h[14]), S[0] & /*choices*/
      8 && (N.choices = /*choices*/
      h[3]), S[0] & /*filtered_indices*/
      2048 && (N.filtered_indices = /*filtered_indices*/
      h[11]), S[0] & /*disabled*/
      16 && (N.disabled = /*disabled*/
      h[4]), S[0] & /*selected_indices*/
      4096 && (N.selected_indices = /*selected_indices*/
      h[12]), S[0] & /*active_index*/
      65536 && (N.active_index = /*active_index*/
      h[16]), w.$set(N), (!p || S[0] & /*container*/
      64) && Ve(
        l,
        "container",
        /*container*/
        h[6]
      );
    },
    i(h) {
      if (!p) {
        J(e.$$.fragment, h);
        for (let S = 0; S < d.length; S += 1)
          J(_[S]);
        J(c), J(w.$$.fragment, h), p = !0;
      }
    },
    o(h) {
      ee(e.$$.fragment, h), _ = _.filter(Boolean);
      for (let S = 0; S < _.length; S += 1)
        ee(_[S]);
      ee(c), ee(w.$$.fragment, h), p = !1;
    },
    d(h) {
      h && ge(l), xe(e), yo(_, h), t[34](null), c && c.d(), xe(w), q = !1, Pl(k);
    }
  };
}
function Lo(t, l, e) {
  let { label: n } = l, { info: i = void 0 } = l, { value: f = [] } = l, u = [], { value_is_output: o = !1 } = l, { max_choices: s = null } = l, { choices: r } = l, a, { disabled: m = !1 } = l, { show_label: w } = l, { container: p = !0 } = l, { allow_custom_value: q = !1 } = l, { filterable: k = !0 } = l, { i18n: d } = l, _, g = "", c = "", h = !1, S, y, N = [], j = null, E = [], T = [];
  const U = qo();
  Array.isArray(f) && f.forEach((v) => {
    const Z = r.map((ve) => ve[1]).indexOf(v);
    Z !== -1 ? E.push(Z) : E.push(v);
  });
  function le() {
    q || e(10, g = ""), q && g !== "" && (I(g), e(10, g = "")), e(14, h = !1), e(16, j = null), U("blur");
  }
  function F(v) {
    e(12, E = E.filter((Z) => Z !== v)), U("select", {
      index: typeof v == "number" ? v : -1,
      value: typeof v == "number" ? y[v] : v,
      selected: !1
    });
  }
  function I(v) {
    (s === null || E.length < s) && (e(12, E = [...E, v]), U("select", {
      index: typeof v == "number" ? v : -1,
      value: typeof v == "number" ? y[v] : v,
      selected: !0
    })), E.length === s && (e(14, h = !1), e(16, j = null), _.blur());
  }
  function H(v) {
    const Z = parseInt(v.detail.target.dataset.index);
    de(Z);
  }
  function de(v) {
    E.includes(v) ? F(v) : I(v), e(10, g = "");
  }
  function pe(v) {
    e(12, E = []), e(10, g = ""), v.preventDefault();
  }
  function ke(v) {
    e(11, N = r.map((Z, ve) => ve)), (s === null || E.length < s) && e(14, h = !0), U("focus");
  }
  function ye(v) {
    e(14, [h, j] = ln(v, j, N), h, (e(16, j), e(3, r), e(27, a), e(10, g), e(28, c), e(7, q), e(11, N))), v.key === "Enter" && (j !== null ? de(j) : q && (I(g), e(10, g = ""))), v.key === "Backspace" && g === "" && e(12, E = [...E.slice(0, -1)]), E.length === s && (e(14, h = !1), e(16, j = null));
  }
  function b() {
    f === void 0 ? e(12, E = []) : Array.isArray(f) && e(12, E = f.map((v) => {
      const Z = y.indexOf(v);
      if (Z !== -1)
        return Z;
      if (q)
        return v;
    }).filter((v) => v !== void 0));
  }
  jo(() => {
    e(25, o = !1);
  });
  const G = (v) => F(v), K = (v, Z) => {
    Z.key === "Enter" && F(v);
  };
  function C() {
    g = this.value, e(10, g);
  }
  function R(v) {
    ko[v ? "unshift" : "push"](() => {
      _ = v, e(13, _);
    });
  }
  const A = (v) => U("key_up", { key: v.key, input_value: g }), M = (v) => {
    v.key === "Enter" && pe(v);
  };
  return t.$$set = (v) => {
    "label" in v && e(0, n = v.label), "info" in v && e(1, i = v.info), "value" in v && e(24, f = v.value), "value_is_output" in v && e(25, o = v.value_is_output), "max_choices" in v && e(2, s = v.max_choices), "choices" in v && e(3, r = v.choices), "disabled" in v && e(4, m = v.disabled), "show_label" in v && e(5, w = v.show_label), "container" in v && e(6, p = v.container), "allow_custom_value" in v && e(7, q = v.allow_custom_value), "filterable" in v && e(8, k = v.filterable), "i18n" in v && e(9, d = v.i18n);
  }, t.$$.update = () => {
    t.$$.dirty[0] & /*choices*/
    8 && (e(15, S = r.map((v) => v[0])), e(29, y = r.map((v) => v[1]))), t.$$.dirty[0] & /*choices, old_choices, input_text, old_input_text, allow_custom_value, filtered_indices*/
    402656392 && (r !== a || g !== c) && (e(11, N = zl(r, g)), e(27, a = r), e(28, c = g), q || e(16, j = N[0])), t.$$.dirty[0] & /*selected_indices, old_selected_index, choices_values*/
    1610616832 && JSON.stringify(E) != JSON.stringify(T) && (e(24, f = E.map((v) => typeof v == "number" ? y[v] : v)), e(30, T = E.slice())), t.$$.dirty[0] & /*value, old_value, value_is_output*/
    117440512 && JSON.stringify(f) != JSON.stringify(u) && (en(U, f, o), e(26, u = Array.isArray(f) ? f.slice() : f)), t.$$.dirty[0] & /*value*/
    16777216 && b();
  }, [
    n,
    i,
    s,
    r,
    m,
    w,
    p,
    q,
    k,
    d,
    g,
    N,
    E,
    _,
    h,
    S,
    j,
    U,
    le,
    F,
    H,
    pe,
    ke,
    ye,
    f,
    o,
    u,
    a,
    c,
    y,
    T,
    G,
    K,
    C,
    R,
    A,
    M
  ];
}
class Go extends po {
  constructor(l) {
    super(), vo(
      this,
      l,
      Lo,
      Fo,
      Co,
      {
        label: 0,
        info: 1,
        value: 24,
        value_is_output: 25,
        max_choices: 2,
        choices: 3,
        disabled: 4,
        show_label: 5,
        container: 6,
        allow_custom_value: 7,
        filterable: 8,
        i18n: 9
      },
      null,
      [-1, -1]
    );
  }
}
const {
  SvelteComponent: zo,
  add_flush_callback: Mo,
  append: De,
  assign: Oo,
  attr: B,
  bind: Ao,
  binding_callbacks: Vo,
  check_outros: cn,
  create_component: gl,
  destroy_component: wl,
  detach: X,
  element: re,
  empty: dn,
  get_spread_object: Do,
  get_spread_update: Bo,
  group_outros: mn,
  init: To,
  insert: Y,
  listen: Dl,
  mount_component: pl,
  run_all: Uo,
  safe_not_equal: Zo,
  set_input_value: Ut,
  space: be,
  text: Po,
  transition_in: ce,
  transition_out: Se
} = window.__gradio__svelte__internal;
function Zt(t) {
  let l, e, n, i, f, u, o, s, r, a, m, w = (
    /*show_token_textbox*/
    t[9] && Pt(t)
  );
  function p(_) {
    t[20](_);
  }
  let q = {
    choices: (
      /*pipelines*/
      t[7]
    ),
    label: "",
    info: (
      /*info*/
      t[3]
    ),
    show_label: (
      /*show_label*/
      t[8]
    ),
    container: (
      /*container*/
      t[11]
    ),
    disabled: !/*interactive*/
    t[16]
  };
  /*value_is_output*/
  t[2] !== void 0 && (q.value_is_output = /*value_is_output*/
  t[2]), i = new as({ props: q }), Vo.push(() => Ao(i, "value_is_output", p)), i.$on(
    "input",
    /*input_handler*/
    t[21]
  ), i.$on(
    "select",
    /*select_handler*/
    t[22]
  ), i.$on(
    "blur",
    /*blur_handler*/
    t[23]
  ), i.$on(
    "focus",
    /*focus_handler*/
    t[24]
  ), i.$on(
    "key_up",
    /*key_up_handler*/
    t[25]
  );
  let k = (
    /*enable_edition*/
    t[10] && It(t)
  ), d = (
    /*value*/
    t[0].name !== "" && Ht(t)
  );
  return {
    c() {
      w && w.c(), l = be(), e = re("p"), e.innerHTML = 'Select the <a href="https://huggingface.co/pyannote" class="svelte-hyoir0">pipeline</a> to use:', n = be(), gl(i.$$.fragment), u = be(), k && k.c(), o = be(), s = re("div"), r = be(), d && d.c(), a = dn(), B(e, "id", "dropdown-label"), B(e, "class", "svelte-hyoir0"), B(s, "class", "params-control svelte-hyoir0"), B(s, "id", "params-control");
    },
    m(_, g) {
      w && w.m(_, g), Y(_, l, g), Y(_, e, g), Y(_, n, g), pl(i, _, g), Y(_, u, g), k && k.m(_, g), Y(_, o, g), Y(_, s, g), Y(_, r, g), d && d.m(_, g), Y(_, a, g), m = !0;
    },
    p(_, g) {
      /*show_token_textbox*/
      _[9] ? w ? w.p(_, g) : (w = Pt(_), w.c(), w.m(l.parentNode, l)) : w && (w.d(1), w = null);
      const c = {};
      g[0] & /*pipelines*/
      128 && (c.choices = /*pipelines*/
      _[7]), g[0] & /*info*/
      8 && (c.info = /*info*/
      _[3]), g[0] & /*show_label*/
      256 && (c.show_label = /*show_label*/
      _[8]), g[0] & /*container*/
      2048 && (c.container = /*container*/
      _[11]), g[0] & /*interactive*/
      65536 && (c.disabled = !/*interactive*/
      _[16]), !f && g[0] & /*value_is_output*/
      4 && (f = !0, c.value_is_output = /*value_is_output*/
      _[2], Mo(() => f = !1)), i.$set(c), /*enable_edition*/
      _[10] ? k ? k.p(_, g) : (k = It(_), k.c(), k.m(o.parentNode, o)) : k && (k.d(1), k = null), /*value*/
      _[0].name !== "" ? d ? (d.p(_, g), g[0] & /*value*/
      1 && ce(d, 1)) : (d = Ht(_), d.c(), ce(d, 1), d.m(a.parentNode, a)) : d && (mn(), Se(d, 1, 1, () => {
        d = null;
      }), cn());
    },
    i(_) {
      m || (ce(i.$$.fragment, _), ce(d), m = !0);
    },
    o(_) {
      Se(i.$$.fragment, _), Se(d), m = !1;
    },
    d(_) {
      _ && (X(l), X(e), X(n), X(u), X(o), X(s), X(r), X(a)), w && w.d(_), wl(i, _), k && k.d(_), d && d.d(_);
    }
  };
}
function Pt(t) {
  let l, e, n, i, f, u;
  return {
    c() {
      l = re("label"), l.textContent = "Enter your Hugging Face token:", e = be(), n = re("input"), B(l, "for", "token"), B(l, "class", "label svelte-hyoir0"), B(n, "data-testid", "textbox"), B(n, "type", "text"), B(n, "class", "text-area svelte-hyoir0"), B(n, "name", "token"), B(n, "id", "token"), B(n, "placeholder", "hf_xxxxxxx..."), B(n, "aria-label", "Enter your Hugging Face token"), B(n, "maxlength", "50"), n.disabled = i = !/*interactive*/
      t[16];
    },
    m(o, s) {
      Y(o, l, s), Y(o, e, s), Y(o, n, s), Ut(
        n,
        /*value*/
        t[0].token
      ), f || (u = Dl(
        n,
        "input",
        /*input_input_handler*/
        t[19]
      ), f = !0);
    },
    p(o, s) {
      s[0] & /*interactive*/
      65536 && i !== (i = !/*interactive*/
      o[16]) && (n.disabled = i), s[0] & /*value*/
      1 && n.value !== /*value*/
      o[0].token && Ut(
        n,
        /*value*/
        o[0].token
      );
    },
    d(o) {
      o && (X(l), X(e), X(n)), f = !1, u();
    }
  };
}
function It(t) {
  let l, e, n, i, f, u, o, s, r, a, m;
  return {
    c() {
      l = re("div"), e = re("p"), e.textContent = "Show configuration", n = be(), i = re("label"), f = re("input"), o = be(), s = re("span"), B(f, "type", "checkbox"), f.disabled = u = /*value*/
      t[0].name == "", B(f, "class", "svelte-hyoir0"), B(s, "class", "slider round svelte-hyoir0"), B(i, "class", "switch svelte-hyoir0"), B(i, "title", r = /*value*/
      t[0].name == "" ? "Please select a pipeline first" : "Show pipeline config"), B(l, "class", "toggle-config svelte-hyoir0");
    },
    m(w, p) {
      Y(w, l, p), De(l, e), De(l, n), De(l, i), De(i, f), f.checked = /*show_config*/
      t[1], De(i, o), De(i, s), a || (m = [
        Dl(
          f,
          "change",
          /*input_change_handler*/
          t[26]
        ),
        Dl(
          f,
          "input",
          /*input_handler_1*/
          t[27]
        )
      ], a = !0);
    },
    p(w, p) {
      p[0] & /*value*/
      1 && u !== (u = /*value*/
      w[0].name == "") && (f.disabled = u), p[0] & /*show_config*/
      2 && (f.checked = /*show_config*/
      w[1]), p[0] & /*value*/
      1 && r !== (r = /*value*/
      w[0].name == "" ? "Please select a pipeline first" : "Show pipeline config") && B(i, "title", r);
    },
    d(w) {
      w && X(l), a = !1, Uo(m);
    }
  };
}
function Ht(t) {
  let l, e, n;
  return e = new uo({
    props: {
      elem_id: (
        /*elem_id*/
        t[4]
      ),
      elem_classes: (
        /*elem_classes*/
        t[5]
      ),
      scale: (
        /*scale*/
        t[12]
      ),
      min_width: (
        /*min_width*/
        t[13]
      ),
      visible: (
        /*show_config*/
        t[1]
      ),
      $$slots: { default: [Io] },
      $$scope: { ctx: t }
    }
  }), e.$on(
    "click",
    /*click_handler*/
    t[28]
  ), {
    c() {
      l = re("div"), gl(e.$$.fragment), B(l, "class", "validation svelte-hyoir0");
    },
    m(i, f) {
      Y(i, l, f), pl(e, l, null), n = !0;
    },
    p(i, f) {
      const u = {};
      f[0] & /*elem_id*/
      16 && (u.elem_id = /*elem_id*/
      i[4]), f[0] & /*elem_classes*/
      32 && (u.elem_classes = /*elem_classes*/
      i[5]), f[0] & /*scale*/
      4096 && (u.scale = /*scale*/
      i[12]), f[0] & /*min_width*/
      8192 && (u.min_width = /*min_width*/
      i[13]), f[0] & /*show_config*/
      2 && (u.visible = /*show_config*/
      i[1]), f[1] & /*$$scope*/
      4 && (u.$$scope = { dirty: f, ctx: i }), e.$set(u);
    },
    i(i) {
      n || (ce(e.$$.fragment, i), n = !0);
    },
    o(i) {
      Se(e.$$.fragment, i), n = !1;
    },
    d(i) {
      i && X(l), wl(e);
    }
  };
}
function Io(t) {
  let l;
  return {
    c() {
      l = Po("Update parameters");
    },
    m(e, n) {
      Y(e, l, n);
    },
    d(e) {
      e && X(l);
    }
  };
}
function Ho(t) {
  let l, e, n, i;
  const f = [
    {
      autoscroll: (
        /*gradio*/
        t[15].autoscroll
      )
    },
    { i18n: (
      /*gradio*/
      t[15].i18n
    ) },
    /*loading_status*/
    t[14]
  ];
  let u = {};
  for (let s = 0; s < f.length; s += 1)
    u = Oo(u, f[s]);
  l = new Gs({ props: u });
  let o = (
    /*visible*/
    t[6] && Zt(t)
  );
  return {
    c() {
      gl(l.$$.fragment), e = be(), o && o.c(), n = dn();
    },
    m(s, r) {
      pl(l, s, r), Y(s, e, r), o && o.m(s, r), Y(s, n, r), i = !0;
    },
    p(s, r) {
      const a = r[0] & /*gradio, loading_status*/
      49152 ? Bo(f, [
        r[0] & /*gradio*/
        32768 && {
          autoscroll: (
            /*gradio*/
            s[15].autoscroll
          )
        },
        r[0] & /*gradio*/
        32768 && { i18n: (
          /*gradio*/
          s[15].i18n
        ) },
        r[0] & /*loading_status*/
        16384 && Do(
          /*loading_status*/
          s[14]
        )
      ]) : {};
      l.$set(a), /*visible*/
      s[6] ? o ? (o.p(s, r), r[0] & /*visible*/
      64 && ce(o, 1)) : (o = Zt(s), o.c(), ce(o, 1), o.m(n.parentNode, n)) : o && (mn(), Se(o, 1, 1, () => {
        o = null;
      }), cn());
    },
    i(s) {
      i || (ce(l.$$.fragment, s), ce(o), i = !0);
    },
    o(s) {
      Se(l.$$.fragment, s), Se(o), i = !1;
    },
    d(s) {
      s && (X(e), X(n)), wl(l, s), o && o.d(s);
    }
  };
}
function Jo(t) {
  let l, e;
  return l = new Wn({
    props: {
      visible: (
        /*visible*/
        t[6]
      ),
      elem_id: (
        /*elem_id*/
        t[4]
      ),
      elem_classes: (
        /*elem_classes*/
        t[5]
      ),
      padding: (
        /*container*/
        t[11]
      ),
      allow_overflow: !1,
      scale: (
        /*scale*/
        t[12]
      ),
      min_width: (
        /*min_width*/
        t[13]
      ),
      $$slots: { default: [Ho] },
      $$scope: { ctx: t }
    }
  }), {
    c() {
      gl(l.$$.fragment);
    },
    m(n, i) {
      pl(l, n, i), e = !0;
    },
    p(n, i) {
      const f = {};
      i[0] & /*visible*/
      64 && (f.visible = /*visible*/
      n[6]), i[0] & /*elem_id*/
      16 && (f.elem_id = /*elem_id*/
      n[4]), i[0] & /*elem_classes*/
      32 && (f.elem_classes = /*elem_classes*/
      n[5]), i[0] & /*container*/
      2048 && (f.padding = /*container*/
      n[11]), i[0] & /*scale*/
      4096 && (f.scale = /*scale*/
      n[12]), i[0] & /*min_width*/
      8192 && (f.min_width = /*min_width*/
      n[13]), i[0] & /*elem_id, elem_classes, scale, min_width, show_config, gradio, value, paramsViewNeedUpdate, enable_edition, pipelines, info, show_label, container, interactive, value_is_output, show_token_textbox, visible, loading_status*/
      262143 | i[1] & /*$$scope*/
      4 && (f.$$scope = { dirty: i, ctx: n }), l.$set(f);
    },
    i(n) {
      e || (ce(l.$$.fragment, n), e = !0);
    },
    o(n) {
      Se(l.$$.fragment, n), e = !1;
    },
    d(n) {
      wl(l, n);
    }
  };
}
function Bl(t) {
  const l = /* @__PURE__ */ new Map();
  if (!t)
    return l;
  for (const e in t)
    t.hasOwnProperty(e) && (typeof t[e] == "object" && t[e] !== null ? l.set(e, Bl(t[e])) : l.set(e, t[e]));
  return l;
}
function bn(t) {
  return Object.fromEntries(Array.from(t.entries(), ([e, n]) => n instanceof Map ? [e, bn(n)] : [e, n]));
}
function Tl(t, l) {
  const e = document.createElement("label");
  e.textContent = l, t.appendChild(e);
}
function Ro(t, l, e) {
  const n = document.createElement("input"), i = t.id;
  Tl(t, i.split("-").at(-1)), n.type = "number", n.value = l, n.contentEditable = String(e), t.appendChild(n);
}
function Xo(t, l, e) {
  let { info: n = void 0 } = l, { elem_id: i = "" } = l, { elem_classes: f = [] } = l, { visible: u = !0 } = l, { value: o = new Ks({ name: "", token: "" }) } = l, { value_is_output: s = !1 } = l, { pipelines: r } = l, { show_label: a } = l, { show_token_textbox: m } = l, { show_config: w = !1 } = l, { enable_edition: p = !1 } = l, { container: q = !0 } = l, { scale: k = null } = l, { min_width: d = void 0 } = l, { loading_status: _ } = l, { gradio: g } = l, { interactive: c } = l, h = !1;
  function S(b) {
    b !== "" && (e(0, o.name = b, o), e(0, o.param_specs = {}, o), g.dispatch("select", o), e(17, h = !0));
  }
  function y(b, G) {
    const K = b.split("-");
    let C = Bl(o.param_specs);
    var R = C;
    K.forEach((A) => {
      R = R.get(A);
    }), R.set("value", G), e(0, o.param_specs = bn(C), o);
  }
  function N(b, G, K) {
    const C = document.createElement("select"), R = b.id;
    Tl(b, R.split("-").at(-1)), G.forEach((A) => {
      const M = document.createElement("option");
      M.textContent = A, M.value = A, C.appendChild(M), A === K && (M.selected = !0);
    }), C.addEventListener("change", (A) => {
      y(R, C.value);
    }), b.appendChild(C);
  }
  function j(b, G, K, C, R) {
    const A = document.createElement("input"), M = document.createElement("input"), v = b.id;
    Tl(b, v.split("-").at(-1)), A.type = "range", A.min = G, A.max = K, A.value = C, A.step = R, A.addEventListener("input", (Z) => {
      M.value = A.value, y(v, A.value);
    }), b.appendChild(A), M.type = "number", M.min = G, M.max = K, M.value = C, M.step = R, M.contentEditable = "true", M.addEventListener("input", (Z) => {
      A.value = M.value, y(v, A.value);
    }), b.appendChild(M);
  }
  function E(b, G, K) {
    G.forEach((C, R) => {
      const A = (K ? K + "-" : "") + R;
      if (C.values().next().value instanceof Map) {
        const M = document.createElement("fieldset");
        M.innerHTML = "<legend>" + A + "<legend>", M.id = A, b.appendChild(M), E(M, C, R);
      } else {
        const M = document.createElement("div");
        switch (M.id = A, M.classList.add("param"), b.appendChild(M), C.get("component")) {
          case "slider":
            j(M, C.get("min"), C.get("max"), C.get("value"), C.get("step"));
            break;
          case "dropdown":
            N(M, C.get("choices"), C.get("value"));
            break;
          case "textbox":
            Ro(M, C.get("value"), !1);
            break;
        }
      }
    });
  }
  function T() {
    o.token = this.value, e(0, o);
  }
  function U(b) {
    s = b, e(2, s);
  }
  const le = () => g.dispatch("input"), F = (b) => S(b.detail.value), I = () => g.dispatch("blur"), H = () => g.dispatch("focus"), de = (b) => g.dispatch("key_up", b.detail);
  function pe() {
    w = this.checked, e(1, w);
  }
  const ke = () => {
    e(17, h = !0), e(1, w = !w);
  }, ye = () => g.dispatch("change", o);
  return t.$$set = (b) => {
    "info" in b && e(3, n = b.info), "elem_id" in b && e(4, i = b.elem_id), "elem_classes" in b && e(5, f = b.elem_classes), "visible" in b && e(6, u = b.visible), "value" in b && e(0, o = b.value), "value_is_output" in b && e(2, s = b.value_is_output), "pipelines" in b && e(7, r = b.pipelines), "show_label" in b && e(8, a = b.show_label), "show_token_textbox" in b && e(9, m = b.show_token_textbox), "show_config" in b && e(1, w = b.show_config), "enable_edition" in b && e(10, p = b.enable_edition), "container" in b && e(11, q = b.container), "scale" in b && e(12, k = b.scale), "min_width" in b && e(13, d = b.min_width), "loading_status" in b && e(14, _ = b.loading_status), "gradio" in b && e(15, g = b.gradio), "interactive" in b && e(16, c = b.interactive);
  }, t.$$.update = () => {
    if (t.$$.dirty[0] & /*value, paramsViewNeedUpdate, show_config*/
    131075 && Object.keys(o.param_specs).length > 0 && h) {
      const b = document.getElementById("params-control");
      if (b.replaceChildren(), w) {
        let G = Bl(o.param_specs);
        E(b, G), e(17, h = !1);
      }
    }
  }, [
    o,
    w,
    s,
    n,
    i,
    f,
    u,
    r,
    a,
    m,
    p,
    q,
    k,
    d,
    _,
    g,
    c,
    h,
    S,
    T,
    U,
    le,
    F,
    I,
    H,
    de,
    pe,
    ke,
    ye
  ];
}
class Ko extends zo {
  constructor(l) {
    super(), To(
      this,
      l,
      Xo,
      Jo,
      Zo,
      {
        info: 3,
        elem_id: 4,
        elem_classes: 5,
        visible: 6,
        value: 0,
        value_is_output: 2,
        pipelines: 7,
        show_label: 8,
        show_token_textbox: 9,
        show_config: 1,
        enable_edition: 10,
        container: 11,
        scale: 12,
        min_width: 13,
        loading_status: 14,
        gradio: 15,
        interactive: 16
      },
      null,
      [-1, -1]
    );
  }
}
export {
  as as BaseDropdown,
  Yo as BaseExample,
  Go as BaseMultiselect,
  Ko as default
};
