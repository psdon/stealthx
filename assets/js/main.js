/*
 * Main Javascript file for stealthx.
 *
 * This file bundles all of your javascript together using webpack.
 */
__webpack_nonce__ = window.NONCE

function supportsDynamicImport() {
    try{
    import("./module/empty.js")
    return true
    }
    catch{
        return false
    }
}

let redirect_to = "/not-supported";
let current_url = window.location.pathname

if (current_url != redirect_to){
    if (!supportsDynamicImport()){
        window.location.replace(redirect_to);
    }
}

import('fg-loadcss/src/cssrelpreload.js')
    .catch( err => {})

let view = document.getElementById('main_js').getAttribute('data-view')
var data_routes = [`${view}`]

const loadModules = (modules) =>
  Promise.all(modules.map((module) =>
    import(`./view/${module}.js`)
        .then(obj => {
            obj.default()
        }).catch( err => {})
  ));

loadModules(data_routes)







// Your own code
//require('./plugins.js');
