const {
  SvelteComponent: y,
  append: J,
  attr: d,
  bubble: p,
  check_outros: x,
  create_slot: K,
  detach: q,
  element: I,
  empty: $,
  get_all_dirty_from_scope: M,
  get_slot_changes: O,
  group_outros: ee,
  init: le,
  insert: S,
  listen: ie,
  safe_not_equal: ne,
  set_style: h,
  space: Q,
  src_url_equal: C,
  toggle_class: k,
  transition_in: T,
  transition_out: A,
  update_slot_base: R
} = window.__gradio__svelte__internal;
function te(i) {
  let e, l, s, o, a, r, u = (
    /*icon*/
    i[7] && F(i)
  );
  const t = (
    /*#slots*/
    i[12].default
  ), f = K(
    t,
    i,
    /*$$scope*/
    i[11],
    null
  );
  return {
    c() {
      e = I("button"), u && u.c(), l = Q(), f && f.c(), d(e, "class", s = /*size*/
      i[4] + " " + /*variant*/
      i[3] + " " + /*elem_classes*/
      i[1].join(" ") + " svelte-8huxfn"), d(
        e,
        "id",
        /*elem_id*/
        i[0]
      ), e.disabled = /*disabled*/
      i[8], k(e, "hidden", !/*visible*/
      i[2]), h(
        e,
        "flex-grow",
        /*scale*/
        i[9]
      ), h(
        e,
        "width",
        /*scale*/
        i[9] === 0 ? "fit-content" : null
      ), h(e, "min-width", typeof /*min_width*/
      i[10] == "number" ? `calc(min(${/*min_width*/
      i[10]}px, 100%))` : null);
    },
    m(n, c) {
      S(n, e, c), u && u.m(e, null), J(e, l), f && f.m(e, null), o = !0, a || (r = ie(
        e,
        "click",
        /*click_handler*/
        i[13]
      ), a = !0);
    },
    p(n, c) {
      /*icon*/
      n[7] ? u ? u.p(n, c) : (u = F(n), u.c(), u.m(e, l)) : u && (u.d(1), u = null), f && f.p && (!o || c & /*$$scope*/
      2048) && R(
        f,
        t,
        n,
        /*$$scope*/
        n[11],
        o ? O(
          t,
          /*$$scope*/
          n[11],
          c,
          null
        ) : M(
          /*$$scope*/
          n[11]
        ),
        null
      ), (!o || c & /*size, variant, elem_classes*/
      26 && s !== (s = /*size*/
      n[4] + " " + /*variant*/
      n[3] + " " + /*elem_classes*/
      n[1].join(" ") + " svelte-8huxfn")) && d(e, "class", s), (!o || c & /*elem_id*/
      1) && d(
        e,
        "id",
        /*elem_id*/
        n[0]
      ), (!o || c & /*disabled*/
      256) && (e.disabled = /*disabled*/
      n[8]), (!o || c & /*size, variant, elem_classes, visible*/
      30) && k(e, "hidden", !/*visible*/
      n[2]), c & /*scale*/
      512 && h(
        e,
        "flex-grow",
        /*scale*/
        n[9]
      ), c & /*scale*/
      512 && h(
        e,
        "width",
        /*scale*/
        n[9] === 0 ? "fit-content" : null
      ), c & /*min_width*/
      1024 && h(e, "min-width", typeof /*min_width*/
      n[10] == "number" ? `calc(min(${/*min_width*/
      n[10]}px, 100%))` : null);
    },
    i(n) {
      o || (T(f, n), o = !0);
    },
    o(n) {
      A(f, n), o = !1;
    },
    d(n) {
      n && q(e), u && u.d(), f && f.d(n), a = !1, r();
    }
  };
}
function oe(i) {
  let e, l, s, o, a = (
    /*icon*/
    i[7] && G(i)
  );
  const r = (
    /*#slots*/
    i[12].default
  ), u = K(
    r,
    i,
    /*$$scope*/
    i[11],
    null
  );
  return {
    c() {
      e = I("a"), a && a.c(), l = Q(), u && u.c(), d(
        e,
        "href",
        /*link*/
        i[6]
      ), d(e, "rel", "noopener noreferrer"), d(
        e,
        "aria-disabled",
        /*disabled*/
        i[8]
      ), d(e, "class", s = /*size*/
      i[4] + " " + /*variant*/
      i[3] + " " + /*elem_classes*/
      i[1].join(" ") + " svelte-8huxfn"), d(
        e,
        "id",
        /*elem_id*/
        i[0]
      ), k(e, "hidden", !/*visible*/
      i[2]), k(
        e,
        "disabled",
        /*disabled*/
        i[8]
      ), h(
        e,
        "flex-grow",
        /*scale*/
        i[9]
      ), h(
        e,
        "pointer-events",
        /*disabled*/
        i[8] ? "none" : null
      ), h(
        e,
        "width",
        /*scale*/
        i[9] === 0 ? "fit-content" : null
      ), h(e, "min-width", typeof /*min_width*/
      i[10] == "number" ? `calc(min(${/*min_width*/
      i[10]}px, 100%))` : null);
    },
    m(t, f) {
      S(t, e, f), a && a.m(e, null), J(e, l), u && u.m(e, null), o = !0;
    },
    p(t, f) {
      /*icon*/
      t[7] ? a ? a.p(t, f) : (a = G(t), a.c(), a.m(e, l)) : a && (a.d(1), a = null), u && u.p && (!o || f & /*$$scope*/
      2048) && R(
        u,
        r,
        t,
        /*$$scope*/
        t[11],
        o ? O(
          r,
          /*$$scope*/
          t[11],
          f,
          null
        ) : M(
          /*$$scope*/
          t[11]
        ),
        null
      ), (!o || f & /*link*/
      64) && d(
        e,
        "href",
        /*link*/
        t[6]
      ), (!o || f & /*disabled*/
      256) && d(
        e,
        "aria-disabled",
        /*disabled*/
        t[8]
      ), (!o || f & /*size, variant, elem_classes*/
      26 && s !== (s = /*size*/
      t[4] + " " + /*variant*/
      t[3] + " " + /*elem_classes*/
      t[1].join(" ") + " svelte-8huxfn")) && d(e, "class", s), (!o || f & /*elem_id*/
      1) && d(
        e,
        "id",
        /*elem_id*/
        t[0]
      ), (!o || f & /*size, variant, elem_classes, visible*/
      30) && k(e, "hidden", !/*visible*/
      t[2]), (!o || f & /*size, variant, elem_classes, disabled*/
      282) && k(
        e,
        "disabled",
        /*disabled*/
        t[8]
      ), f & /*scale*/
      512 && h(
        e,
        "flex-grow",
        /*scale*/
        t[9]
      ), f & /*disabled*/
      256 && h(
        e,
        "pointer-events",
        /*disabled*/
        t[8] ? "none" : null
      ), f & /*scale*/
      512 && h(
        e,
        "width",
        /*scale*/
        t[9] === 0 ? "fit-content" : null
      ), f & /*min_width*/
      1024 && h(e, "min-width", typeof /*min_width*/
      t[10] == "number" ? `calc(min(${/*min_width*/
      t[10]}px, 100%))` : null);
    },
    i(t) {
      o || (T(u, t), o = !0);
    },
    o(t) {
      A(u, t), o = !1;
    },
    d(t) {
      t && q(e), a && a.d(), u && u.d(t);
    }
  };
}
function F(i) {
  let e, l, s;
  return {
    c() {
      e = I("img"), d(e, "class", "button-icon svelte-8huxfn"), C(e.src, l = /*icon*/
      i[7].url) || d(e, "src", l), d(e, "alt", s = `${/*value*/
      i[5]} icon`);
    },
    m(o, a) {
      S(o, e, a);
    },
    p(o, a) {
      a & /*icon*/
      128 && !C(e.src, l = /*icon*/
      o[7].url) && d(e, "src", l), a & /*value*/
      32 && s !== (s = `${/*value*/
      o[5]} icon`) && d(e, "alt", s);
    },
    d(o) {
      o && q(e);
    }
  };
}
function G(i) {
  let e, l, s;
  return {
    c() {
      e = I("img"), d(e, "class", "button-icon svelte-8huxfn"), C(e.src, l = /*icon*/
      i[7].url) || d(e, "src", l), d(e, "alt", s = `${/*value*/
      i[5]} icon`);
    },
    m(o, a) {
      S(o, e, a);
    },
    p(o, a) {
      a & /*icon*/
      128 && !C(e.src, l = /*icon*/
      o[7].url) && d(e, "src", l), a & /*value*/
      32 && s !== (s = `${/*value*/
      o[5]} icon`) && d(e, "alt", s);
    },
    d(o) {
      o && q(e);
    }
  };
}
function fe(i) {
  let e, l, s, o;
  const a = [oe, te], r = [];
  function u(t, f) {
    return (
      /*link*/
      t[6] && /*link*/
      t[6].length > 0 ? 0 : 1
    );
  }
  return e = u(i), l = r[e] = a[e](i), {
    c() {
      l.c(), s = $();
    },
    m(t, f) {
      r[e].m(t, f), S(t, s, f), o = !0;
    },
    p(t, [f]) {
      let n = e;
      e = u(t), e === n ? r[e].p(t, f) : (ee(), A(r[n], 1, 1, () => {
        r[n] = null;
      }), x(), l = r[e], l ? l.p(t, f) : (l = r[e] = a[e](t), l.c()), T(l, 1), l.m(s.parentNode, s));
    },
    i(t) {
      o || (T(l), o = !0);
    },
    o(t) {
      A(l), o = !1;
    },
    d(t) {
      t && q(s), r[e].d(t);
    }
  };
}
function ue(i, e, l) {
  let { $$slots: s = {}, $$scope: o } = e, { elem_id: a = "" } = e, { elem_classes: r = [] } = e, { visible: u = !0 } = e, { variant: t = "secondary" } = e, { size: f = "lg" } = e, { value: n = null } = e, { link: c = null } = e, { icon: b = null } = e, { disabled: w = !1 } = e, { scale: z = null } = e, { min_width: E = void 0 } = e;
  function L(m) {
    p.call(this, i, m);
  }
  return i.$$set = (m) => {
    "elem_id" in m && l(0, a = m.elem_id), "elem_classes" in m && l(1, r = m.elem_classes), "visible" in m && l(2, u = m.visible), "variant" in m && l(3, t = m.variant), "size" in m && l(4, f = m.size), "value" in m && l(5, n = m.value), "link" in m && l(6, c = m.link), "icon" in m && l(7, b = m.icon), "disabled" in m && l(8, w = m.disabled), "scale" in m && l(9, z = m.scale), "min_width" in m && l(10, E = m.min_width), "$$scope" in m && l(11, o = m.$$scope);
  }, [
    a,
    r,
    u,
    t,
    f,
    n,
    c,
    b,
    w,
    z,
    E,
    o,
    s,
    L
  ];
}
class se extends y {
  constructor(e) {
    super(), le(this, e, ue, fe, ne, {
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
  SvelteComponent: ae,
  append: D,
  attr: B,
  create_component: _e,
  destroy_component: ce,
  detach: U,
  element: H,
  init: me,
  insert: V,
  listen: re,
  mount_component: de,
  safe_not_equal: be,
  set_data: W,
  space: he,
  text: X,
  transition_in: ve,
  transition_out: ge
} = window.__gradio__svelte__internal;
function ke(i) {
  let e = (
    /*value*/
    (i[3] ? (
      /*gradio*/
      i[14].i18n(
        /*value*/
        i[3]
      )
    ) : "") + ""
  ), l;
  return {
    c() {
      l = X(e);
    },
    m(s, o) {
      V(s, l, o);
    },
    p(s, o) {
      o & /*value, gradio*/
      16392 && e !== (e = /*value*/
      (s[3] ? (
        /*gradio*/
        s[14].i18n(
          /*value*/
          s[3]
        )
      ) : "") + "") && W(l, e);
    },
    d(s) {
      s && U(l);
    }
  };
}
function we(i) {
  let e, l, s, o, a, r, u, t, f;
  return l = new se({
    props: {
      value: (
        /*value*/
        i[3]
      ),
      variant: (
        /*variant*/
        i[4]
      ),
      elem_id: (
        /*elem_id*/
        i[0]
      ),
      elem_classes: (
        /*elem_classes*/
        i[1]
      ),
      size: (
        /*size*/
        i[6]
      ),
      scale: (
        /*scale*/
        i[7]
      ),
      link: (
        /*link*/
        i[9]
      ),
      icon: (
        /*icon*/
        i[8]
      ),
      min_width: (
        /*min_width*/
        i[10]
      ),
      visible: (
        /*visible*/
        i[2]
      ),
      disabled: !/*interactive*/
      i[5],
      $$slots: { default: [ke] },
      $$scope: { ctx: i }
    }
  }), l.$on(
    "click",
    /*click_handler*/
    i[18]
  ), {
    c() {
      e = H("div"), _e(l.$$.fragment), s = he(), o = H("span"), a = X(
        /*tooltip*/
        i[11]
      ), B(o, "class", "tooltip-text svelte-1svhrw5"), B(e, "class", "tooltip-container svelte-1svhrw5"), B(e, "style", r = `--tooltip-color: ${/*tooltip_color*/
      i[12]}; --tooltip-background-color: ${/*tooltip_background_color*/
      i[13]}`);
    },
    m(n, c) {
      V(n, e, c), de(l, e, null), D(e, s), D(e, o), D(o, a), u = !0, t || (f = re(
        e,
        "mouseenter",
        /*calculateTooltipPosition*/
        i[15]
      ), t = !0);
    },
    p(n, [c]) {
      const b = {};
      c & /*value*/
      8 && (b.value = /*value*/
      n[3]), c & /*variant*/
      16 && (b.variant = /*variant*/
      n[4]), c & /*elem_id*/
      1 && (b.elem_id = /*elem_id*/
      n[0]), c & /*elem_classes*/
      2 && (b.elem_classes = /*elem_classes*/
      n[1]), c & /*size*/
      64 && (b.size = /*size*/
      n[6]), c & /*scale*/
      128 && (b.scale = /*scale*/
      n[7]), c & /*link*/
      512 && (b.link = /*link*/
      n[9]), c & /*icon*/
      256 && (b.icon = /*icon*/
      n[8]), c & /*min_width*/
      1024 && (b.min_width = /*min_width*/
      n[10]), c & /*visible*/
      4 && (b.visible = /*visible*/
      n[2]), c & /*interactive*/
      32 && (b.disabled = !/*interactive*/
      n[5]), c & /*$$scope, value, gradio*/
      1064968 && (b.$$scope = { dirty: c, ctx: n }), l.$set(b), (!u || c & /*tooltip*/
      2048) && W(
        a,
        /*tooltip*/
        n[11]
      ), (!u || c & /*tooltip_color, tooltip_background_color*/
      12288 && r !== (r = `--tooltip-color: ${/*tooltip_color*/
      n[12]}; --tooltip-background-color: ${/*tooltip_background_color*/
      n[13]}`)) && B(e, "style", r);
    },
    i(n) {
      u || (ve(l.$$.fragment, n), u = !0);
    },
    o(n) {
      ge(l.$$.fragment, n), u = !1;
    },
    d(n) {
      n && U(e), ce(l), t = !1, f();
    }
  };
}
function ze(i, e, l) {
  let { elem_id: s = "" } = e, { elem_classes: o = [] } = e, { visible: a = !0 } = e, { value: r } = e, { variant: u = "secondary" } = e, { interactive: t } = e, { size: f = "lg" } = e, { scale: n = null } = e, { icon: c = null } = e, { link: b = null } = e, { min_width: w = void 0 } = e, { tooltip: z } = e, { tooltip_color: E = "white" } = e, { tooltip_background_color: L = "black" } = e, { x: m = null } = e, { y: j = null } = e, { gradio: N } = e;
  function P(_) {
    const v = _.currentTarget, g = v.querySelector(".tooltip-text");
    v && g && m !== null && j !== null && (g.style.left = `${m}px`, g.style.top = `${j}px`);
  }
  window.addEventListener("resize", () => {
    document.querySelectorAll(".tooltip-text").forEach((v) => {
      const g = v.parentElement;
      P({ currentTarget: g });
    });
  });
  function Y() {
    document.querySelectorAll(".tooltip-container button").forEach((v) => {
      v.addEventListener("mouseenter", P), v.addEventListener("mouseleave", () => {
        const g = v.querySelector(".tooltip-text");
        g.style.visibility = "hidden";
      });
    });
  }
  window.addEventListener("load", Y);
  const Z = () => N.dispatch("click");
  return i.$$set = (_) => {
    "elem_id" in _ && l(0, s = _.elem_id), "elem_classes" in _ && l(1, o = _.elem_classes), "visible" in _ && l(2, a = _.visible), "value" in _ && l(3, r = _.value), "variant" in _ && l(4, u = _.variant), "interactive" in _ && l(5, t = _.interactive), "size" in _ && l(6, f = _.size), "scale" in _ && l(7, n = _.scale), "icon" in _ && l(8, c = _.icon), "link" in _ && l(9, b = _.link), "min_width" in _ && l(10, w = _.min_width), "tooltip" in _ && l(11, z = _.tooltip), "tooltip_color" in _ && l(12, E = _.tooltip_color), "tooltip_background_color" in _ && l(13, L = _.tooltip_background_color), "x" in _ && l(16, m = _.x), "y" in _ && l(17, j = _.y), "gradio" in _ && l(14, N = _.gradio);
  }, [
    s,
    o,
    a,
    r,
    u,
    t,
    f,
    n,
    c,
    b,
    w,
    z,
    E,
    L,
    N,
    P,
    m,
    j,
    Z
  ];
}
class Ee extends ae {
  constructor(e) {
    super(), me(this, e, ze, we, be, {
      elem_id: 0,
      elem_classes: 1,
      visible: 2,
      value: 3,
      variant: 4,
      interactive: 5,
      size: 6,
      scale: 7,
      icon: 8,
      link: 9,
      min_width: 10,
      tooltip: 11,
      tooltip_color: 12,
      tooltip_background_color: 13,
      x: 16,
      y: 17,
      gradio: 14
    });
  }
}
export {
  se as BaseButton,
  Ee as default
};
