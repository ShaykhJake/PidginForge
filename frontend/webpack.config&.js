var path = require('path')
var webpack = require('webpack')

module.exports = {
  entry: './src/main.js',
  output: {
    path: path.resolve(__dirname, './dist'),
    publicPath: '/dist/',
    filename: 'build.js'
  },
  module: {
    rules: [
      {
        test: /\.s(c|a)ss$/,
        use: [
          'vue-style-loader',
          'css-loader',
          {
            loader: 'sass-loader',
            // Requires sass-loader@^7.0.0
            options: {
              implementation: require('sass'),
              fiber: require('fibers'),
              indentedSyntax: true // optional
            },
            // Requires sass-loader@^8.0.0
            options: {
              implementation: require('sass'),
              sassOptions: {
                fiber: require('fibers'),
                indentedSyntax: true // optional
              },
            },
          },
        ],
      },
      {
        test: /\.css$/,
        use: [
          'vue-style-loader',
          'css-loader'
        ],
      },      {
        test: /\.vue$/,
        loader: 'vue-loader',
        options: {
          loaders: {
          }
          // other vue-loader options go here
        }
      },
      {
        test: /\.js$/,
        loader: 'babel-loader',
        exclude: /node_modules/
      },
      {
        test: /\.(png|jpg|gif|svg)$/,
        loader: 'file-loader',
        options: {
          name: '[name].[ext]?[hash]'
        }
      }
    ]
  },
  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js'
    },
    extensions: ['*', '.js', '.vue', '.json']
  },
  devServer: {
    historyApiFallback: true,
    noInfo: true,
    overlay: true
  },
  performance: {
    hints: false
  },
  devtool: '#eval-source-map'
}

if (process.env.NODE_ENV === 'production') {
  module.exports.devtool = '#source-map'
  // http://vue-loader.vuejs.org/en/workflow/production.html
  module.exports.plugins = (module.exports.plugins || []).concat([
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: '"production"'
      }
    }),
    new webpack.optimize.UglifyJsPlugin({
      sourceMap: true,
      compress: {
        warnings: false
      }
    }),
    new webpack.LoaderOptionsPlugin({
      minimize: true
    })
  ])
}



// var path = require('path')
// var webpack = require('webpack')

// module.exports =
// {
//    "mode": "production",
//    "entry": "src/main.js",
//    "output": {
//        "path": __dirname+'/static',
//        "filename": "[name].[chunkhash:8].js"
//    },
//    "module": {
//        "rules": [
//            {
//                "test": /\.js$/,
//                "exclude": /node_modules/,
//                "use": {
//                    "loader": "babel-loader",
//                    "options": {
//                        "presets": [
//                            "env"
//                        ]
//                    }
//                }
//            },
//            {
//                "test": /\.css$/,
//                "use": [
//                    "style-loader",
//                    "css-loader"
//                ]
//            }
//        ]
//    }
// },
// {
//    "mode": "development",
//    "entry": "src/index.js",
//    "output": {
//        "path": __dirname+'/static',
//        "filename": "[name].[chunkhash:8].js"
//    },
//    "module": {
//        "rules": [
//            {
//                "enforce": "pre",
//                "test": /\.(js|jsx)$/,
//                "exclude": /node_modules/,
//                "use": "eslint-loader"
//            },
//            {
//                "test": /\.js$/,
//                "exclude": /node_modules/,
//                "use": {
//                    "loader": "babel-loader",
//                    "options": {
//                        "presets": [
//                            "env"
//                        ]
//                    }
//                }
//            },
//            {
//                "test": /\.css$/,
//                "use": [
//                    "style-loader",
//                    "css-loader"
//                ]
//            }
//        ]
//    }
// }