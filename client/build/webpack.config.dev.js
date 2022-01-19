'use strict'
const HtmlWebpackPlugin = require('html-webpack-plugin');
const path = require('path');

module.exports = {
  mode: 'development',
  devtool: "eval-source-map",
  entry: {
    base: './source/index',
  },
  output: {
    path: path.resolve(__dirname, '../distribution'),
    filename: '[name].js'
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        use: 'babel-loader'
      },
    ]
  },
  plugins: [
    new HtmlWebpackPlugin({
      filename: 'base.html',
      template: 'source/index.html',
      chunks: ['base'],
    }),
  ]
};