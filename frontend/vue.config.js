const BundleTracker = require("webpack-bundle-tracker");


module.exports = {
  // on Windows you might want to set publicPath: "http://127.0.0.1:8080/"
  
  // Set the following directory to a place where Django can easily find it:
  outputDir: "../static/dist/",
  
  // Production
  // publicPath: "dist/",
  publicPath: "https://jakesdesk-media.s3.amazonaws.com/static/dist/",
  // publicPath: "./",
  //Development
  // publicPath: "http://0.0.0.0:8080/",
  

  chainWebpack: config => {
    config
      .plugin("BundleTracker")
      .use(BundleTracker, [{ filename: "./webpack-stats.json" }]);

    // config.output.filename("bundle.js");
    config.output.filename("[name].[hash:8].bundle.js");

    config.optimization.splitChunks(false);
    // config.optimization
    // .splitChunks({
    //     cacheGroups: {
    //         vendor: {
    //             test: /[\\/]node_modules[\\/]/,
    //             name: "chunk-vendors",
    //             chunks: "all",
    //             priority: 1
    //         },
    //     },
    // });


    config.resolve.alias.set("__STATIC__", "../");

    config.devServer
      // .public('http://localhost:8080')
      // .host('localhost')
      // .port(8080)
      .hotOnly(true)
      .watchOptions({ poll: 1000 })
      .https(false)
      .disableHostCheck(true)
      .headers({ "Access-Control-Allow-Origin": ["*"] });
  },

  // uncomment before executing 'npm run build'
  css: {
    extract: {
      // filename: "bundle.css",
      filename: "[name].[hash:8].css",
      // chunkFilename: "bundle.css",
      // chunkFilename: "[id].[hash:8].css"
    }
  },

};
