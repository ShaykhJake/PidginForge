// webpack.config.js
// const WorkerPlugin = require('worker-plugin');

module.exports = {
  // plugins: [
  //   new WorkerPlugin()
  // ],
  // loader: 'worker-loader',
  // options: { inline: true },
  rules: [
    // {
    //   test: /\.worker\.js$/,
    //   use: { loader: 'worker-loader' }
    // },
    {
      test: /\.s(c|a)ss$/,
      use: [
        "vue-style-loader",
        "css-loader",
        {
          loader: "sass-loader",
          // Requires sass-loader@^8.0.0
          options: {
            implementation: require("sass"),
            sassOptions: {
              fiber: require("fibers"),
              indentedSyntax: true // optional
            }
          }
        }
      ]
    }
  ]
};
