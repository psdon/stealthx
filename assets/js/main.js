/* eslint-disable camelcase */
/*
 * Main Javascript file for stealthx.
 *
 * This file bundles all of your javascript together using webpack.
 */

// eslint-disable-next-line no-undef
__webpack_nonce__ = window.NONCE;


// load static files
require.context(
  '../', // context folder
  true, // include subdirectories
  /\.(ttf|eot|svg|png|jpe?g|gif|ico)(\?.*)?$/i, // RegExp
);


function supportsDynamicImport() {
  try {
    import('./module/empty.js');
    return true;
  } catch {
    return false;
  }
}

const redirectTo = '/not-supported';
const currentUrl = window.location.pathname;

if (currentUrl !== redirectTo) {
  if (!supportsDynamicImport()) {
    window.location.replace(redirectTo);
  }
}

const view = document.getElementById('main_js').getAttribute('data-view');
const dataRoutes = [`${view}`];

const loadModules = (modules) => Promise.all(
    modules.map((module) => import(`./view/${module}.js`)
        .then((obj) => {
          obj.default();
        })
        .catch(() => {}),),
  );

loadModules(dataRoutes);

// Your own code
// require('./plugins.js');
