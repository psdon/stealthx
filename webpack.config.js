const path = require('path');
const webpack = require('webpack');

/*
 * Webpack Plugins
 */
const ManifestRevisionPlugin = require('manifest-revision-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const OptimizeCssAssetsPlugin = require('optimize-css-assets-webpack-plugin');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
const CompressionPlugin = require('compression-webpack-plugin');

// take debug mode from the environment
const debug = (process.env.NODE_ENV !== 'production');

// Development asset host (webpack dev server)
const publicHost = debug ? 'http://0.0.0.0:2992' : '';

const rootAssetPath = path.join(__dirname, 'assets');

const hashType = debug ? '[hash]': '[contentHash]'
console.log(hashType)

module.exports = {
  // configuration
  context: __dirname,
  entry: {
    main_js: path.join(__dirname, 'assets', 'js', 'main.js'),
    main_css: [
      path.join(__dirname, 'assets', 'css', 'main.css'),
    ],
  },
  output: {
    path: path.join(__dirname, 'stealthx', 'static'),
    publicPath: `${publicHost}/static/`,
    filename: '[name].' + hashType + '.js',
    chunkFilename: '[id].' + hashType + '.js',
  },
  optimization: {
  minimizer: [
   new UglifyJsPlugin({
        cache: true,
        parallel: true,
        sourceMap: true,
        uglifyOptions: {
          output: {
            comments: false
          }
        }
    }),
    new OptimizeCssAssetsPlugin({
      assetNameRegExp: /\.css$/g,
      cssProcessor: require('cssnano'),
      cssProcessorPluginOptions: {
        preset: ['default', { discardComments: { removeAll: true } }],
      },
      canPrint: true
    }),
  ],
},
  resolve: {
    extensions: ['.js', '.css'],
  },
  devtool: 'source-map',
  devServer: {
    headers: { 'Access-Control-Allow-Origin': '*' },
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
            options: {
              hmr: debug,
            },
          },
          'css-loader',
          {
            loader: 'postcss-loader'
          }
        ],
      },
      { test: /\.html$/, loader: 'raw-loader' },
      { test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: 'url-loader', options: { limit: 10000, mimetype: 'application/font-woff' } },
      {
        test: /\.(ttf|eot|svg|png|jpe?g|gif|ico)(\?.*)?$/i,
        loader: `file-loader?context=${rootAssetPath}&name=[path][name].${hashType}.[ext]`
      },
      { test: /\.js$/, exclude: /node_modules/, loader: 'babel-loader', query: { presets: ['@babel/preset-env'], cacheDirectory: true } },
    ],
  },
  plugins: [
    new MiniCssExtractPlugin({ filename: '[name].' + hashType + '.css', }),
//    new webpack.ProvidePlugin({ $: 'jquery', jQuery: 'jquery' }),
    new ManifestRevisionPlugin(path.join(__dirname, 'stealthx', 'webpack', 'manifest.json'), {
      rootAssetPath,
      ignorePaths: ['/js', '/css'],
      extensionsRegex: /\.(ttf|eot|svg|png|jpe?g|gif|ico)$/i,
    }),

  ].concat(debug ? [] : [
    // production webpack plugins go here
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: JSON.stringify('production'),
      } }),
//    new CompressionPlugin({
//          filename: '[path].gz[query]',
//          algorithm: 'gzip',
//          test: /\.js$|\.css$|\.html$|\.eot?.+$|\.ttf?.+$|\.woff?.+$|\.svg?.+$/,
//          threshold: 0,
//          minRatio: 0.8
//    }),
  ]),
};
