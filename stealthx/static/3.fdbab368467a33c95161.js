(window["webpackJsonp"] = window["webpackJsonp"] || []).push([[3],{

/***/ "./assets/js/module/invokeParticles.js":
/*!*********************************************!*\
  !*** ./assets/js/module/invokeParticles.js ***!
  \*********************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return invokeParticles; });
__webpack_require__(/*! particles.js */ "./node_modules/particles.js/particles.js");

function invokeParticles(id) {
  particlesJS(id, {
    particles: {
      number: {
        value: 80,
        density: {
          enable: true,
          value_area: 750
        }
      },
      color: {
        value: "#ff0000"
      },
      shape: {
        type: "circle",
        stroke: {
          width: 8,
          color: "#ff0000"
        },
        polygon: {
          nb_sides: 5
        },
        image: {
          src: "img/github.svg",
          width: 100,
          height: 100
        }
      },
      opacity: {
        value: 0.37090524554716386,
        random: false,
        anim: {
          enable: false,
          speed: 1,
          opacity_min: 0.08306820730501813,
          sync: false
        }
      },
      size: {
        value: 1,
        random: true,
        anim: {
          enable: false,
          speed: 40,
          size_min: 0.1,
          sync: false
        }
      },
      line_linked: {
        enable: true,
        distance: 163.9787811457196,
        color: "#ffffff",
        opacity: 0.4,
        width: 1.8037665926029156
      },
      move: {
        enable: true,
        speed: 6,
        direction: "none",
        random: false,
        straight: false,
        out_mode: "out",
        bounce: false,
        attract: {
          enable: false,
          rotateX: 600,
          rotateY: 1200
        }
      }
    },
    interactivity: {
      detect_on: "canvas",
      events: {
        onhover: {
          enable: true,
          mode: "grab"
        },
        onclick: {
          enable: true,
          mode: "push"
        },
        resize: true
      },
      modes: {
        grab: {
          distance: 400,
          line_linked: {
            opacity: 1
          }
        },
        bubble: {
          distance: 400,
          size: 40,
          duration: 2,
          opacity: 8,
          speed: 3
        },
        repulse: {
          distance: 200,
          duration: 0.4
        },
        push: {
          particles_nb: 4
        },
        remove: {
          particles_nb: 2
        }
      }
    },
    retina_detect: true
  });
}

/***/ }),

/***/ "./assets/js/view/particlesOnly.js":
/*!*****************************************!*\
  !*** ./assets/js/view/particlesOnly.js ***!
  \*****************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return signIn; });
/* harmony import */ var _module_invokeParticles__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../module/invokeParticles */ "./assets/js/module/invokeParticles.js");

function signIn() {
  Object(_module_invokeParticles__WEBPACK_IMPORTED_MODULE_0__["default"])("particles");
}

/***/ })

}]);
//# sourceMappingURL=3.fdbab368467a33c95161.js.map