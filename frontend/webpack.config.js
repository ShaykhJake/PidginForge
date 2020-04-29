// webpack.config.js

module.exports = {
  build: {
    assetsRoot: path.resolve(__dirname, '../static/'),
    assetsSubDirectory: 'app_name',
    assetsPublicPath: '/static/',
    // ...
  },
  dev: {
    assetsPublicPath: 'http://localhost:8080/',
    // ...
  },
  resolve: {
    alias: {
      //...
      '__STATIC__': this.resolve('static'),
    }
  },
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
   ],
 }