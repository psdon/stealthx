(window["webpackJsonp"] = window["webpackJsonp"] || []).push([[2],{

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

/***/ "./assets/js/script.js":
/*!*****************************!*\
  !*** ./assets/js/script.js ***!
  \*****************************/
/*! exports provided: hasClass, addClass, removeClass, showHide, addEventByElementId */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "hasClass", function() { return hasClass; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "addClass", function() { return addClass; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "removeClass", function() { return removeClass; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "showHide", function() { return showHide; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "addEventByElementId", function() { return addEventByElementId; });
// App initialization code goes here
function hasClass(ele, cls) {
  return ele.className.match(new RegExp('(\\s|^)' + cls + '(\\s|$)')) ? true : false;
}
function addClass(ele, cls) {
  if (!hasClass(ele, cls)) ele.className += " " + cls;
}
function removeClass(ele, cls) {
  if (hasClass(ele, cls)) {
    var reg = new RegExp('(\\s|^)' + cls + '(\\s|$)');
    ele.className = ele.className.replace(reg, ' ');
  }
}
function showHide(id) {
  var _element = document.getElementById(id);

  hasClass(_element, "hidden") ? removeClass(_element, "hidden") : addClass(_element, "hidden");
}
function addEventByElementId(elementId, evt, handler) {
  var _element = document.getElementById(elementId);

  _element.addEventListener(evt, function (event) {
    handler();
  });
}

/***/ }),

/***/ "./assets/js/view/home.js":
/*!********************************!*\
  !*** ./assets/js/view/home.js ***!
  \********************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return home; });
/* harmony import */ var _vimeo_player__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @vimeo/player */ "./node_modules/@vimeo/player/dist/player.es.js");
/* harmony import */ var _script__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../script */ "./assets/js/script.js");
/* harmony import */ var _module_invokeParticles__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../module/invokeParticles */ "./assets/js/module/invokeParticles.js");



function home() {
  var player;

  function renderPlayer() {
    player = new _vimeo_player__WEBPACK_IMPORTED_MODULE_0__["default"]('vimeo-player', {
      id: '362325129',
      responsive: true,
      autoplay: true
    });
    player.on('play', function () {
      var _element = document.getElementById('video-play-box');

      if (!Object(_script__WEBPACK_IMPORTED_MODULE_1__["hasClass"])(_element, 'hidden')) {
        Object(_script__WEBPACK_IMPORTED_MODULE_1__["showHide"])('video-play-box');
        Object(_script__WEBPACK_IMPORTED_MODULE_1__["showHide"])('video-reel-box');
      }
    });
    player.on('pause', function () {
      Object(_script__WEBPACK_IMPORTED_MODULE_1__["showHide"])('video-reel-box');
      Object(_script__WEBPACK_IMPORTED_MODULE_1__["showHide"])('video-play-box');
    });
  }

  Object(_module_invokeParticles__WEBPACK_IMPORTED_MODULE_2__["default"])('particles-1');
  Object(_module_invokeParticles__WEBPACK_IMPORTED_MODULE_2__["default"])('particles-2');
  var isRenderedPlayer = false;
  Object(_script__WEBPACK_IMPORTED_MODULE_1__["addEventByElementId"])('video-play-box', 'click', function (e) {
    Object(_script__WEBPACK_IMPORTED_MODULE_1__["showHide"])('video-play-box');
    Object(_script__WEBPACK_IMPORTED_MODULE_1__["showHide"])('video-reel-box');

    if (isRenderedPlayer == false) {
      renderPlayer();
      isRenderedPlayer = true;
    } else {
      player.play();
    }
  });
}

/***/ })

}]);
//# sourceMappingURL=2.9f21ec78f50ac9ac0dfd.js.map