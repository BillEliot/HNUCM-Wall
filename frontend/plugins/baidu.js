if (process.client && process.env.NODE_ENV === 'production') {
   var _hmt = _hmt || [];
   (function() {
     var hm = document.createElement("script");
     hm.src = "https://hm.baidu.com/hm.js?ba7fa11f108ef2e9e582e443adc33ceb";
     hm.id = "baidu_tj";
     var s = document.getElementsByTagName("script")[0];
     s.parentNode.insertBefore(hm, s);
   })()
}

export default ({ app: { router }, store }) => {
   if (process.client && process.env.NODE_ENV === 'production') {
    router.afterEach((to, from) => {
      var _hmt = _hmt || [];
      (function() {
        document.getElementById('baidu_tj') && document.getElementById('baidu_tj').remove();
        var hm = document.createElement("script");
        hm.src = "https://hm.baidu.com/hm.js?ba7fa11f108ef2e9e582e443adc33ceb";
        hm.id = "baidu_tj";
        var s = document.getElementsByTagName("script")[0];
        s.parentNode.insertBefore(hm, s);
      })()
    })
  }
}
