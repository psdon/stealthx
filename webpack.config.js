const path = require('path');
const webpack = require('webpack');

/*
 * Webpack Plugins
 */
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const OptimizeCssAssetsPlugin = require('optimize-css-assets-webpack-plugin');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');

// take debug mode from the environment
const debug = (process.env.NODE_ENV !== 'production');

const rootAssetPath = path.join(__dirname, 'assets');

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
    path: path.join(__dirname, 'stealthx', 'static', "pack"),
    publicPath: "/static/pack/",
    filename: "[name].js",
    chunkFilename: "[id].js"
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
        loader: `file-loader?context=${rootAssetPath}&name=[path][name].[ext]`
      },
      { test: /\.js$/, exclude: /node_modules/, loader: 'babel-loader', query: { presets: ['@babel/preset-env'], cacheDirectory: true } },
    ],
  },
  plugins: [
    new MiniCssExtractPlugin({ filename: '[name].css', }),
//    new webpack.ProvidePlugin({ $: 'jquery', jQuery: 'jquery' }),
  ].concat(debug ? [] : [
    // production webpack plugins go here
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: JSON.stringify('production'),
      } }),
  ]),
};
