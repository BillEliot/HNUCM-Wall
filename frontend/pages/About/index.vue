<template>
  <div>
    <!-- banner -->
    <div class="main-wrapper">
        <div class="page-title">
            <div class="container">
                <div class="title-holder">
                    <div class="title-text text-center">
                        <h1>关于我们</h1>
                        <p class="subheading">About Us</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div style="margin-top: 50px"></div>
    <!-- statement -->
    <section class="section">
      <div class="container">
          <a-card title="关于社区">
            <p>该社区为在校学生创建之个人网站，非官方合作网站，日后有望合作。</p>
            <p>社区现有“表白墙”、“失物墙”、“交易墙”、“求助墙”四面墙墙，希望可以帮助同学们解决一些问题。</p>
            <p>在“大佬杂谈”中，我们会定期邀请大佬来分享学习经验，也会转发一些精品文章，当然还有期末考试的重点。</p>
            <p>“热点”和“讲座动态”可以帮助你了解最新的新闻和讲座情况。</p>
            <p>“题库”中我们收录了练习册的大部分题目，可助你刷题、改错和回顾。</p>
            <p>“中药库”、“方剂库”、“经络库”可帮助你快速查询相关知识。</p>
            <p>“虚拟仿真”是我们研究的前沿，希望借助3d技术进行学习研究。</p>
          </a-card>
          <hr />
          <a-card title="商务广告">
            <p>广告投放、商务合作邮箱：eliotwjz@gmail.com / 1161142536@qq.com</p>
            <p>合作qq：1161142536</p>
            <p>合作微信：EliotDrizzle</p>
          </a-card>
          <hr />
          <a-card title="捐赠">
            <img src="~assets/img/alipay.jpg" class="alipay">
            <img src="~assets/img/wechatpay.jpg" class="wechatpay">
          </a-card>
      </div>
    </section>
  </div>
</template>

<script>
import qs from 'qs'
import { mapState } from 'vuex'

export default {
  layout: 'common',
  data() {
    return {
    }
  },
  async asyncData({ $axios }) {
  },
  methods: {

  },
  computed: mapState({
    baseUrl: state => state.baseUrl
  })
}
</script>

<style scoped>
a {
  text-decoration: none
}

.section {
  padding: 2em 0;
  position: relative;
}
.alipay {
  width: 30%;
  float: left;
}
.wechatpay {
  width: 30%;
  float: right;
}
</style>
