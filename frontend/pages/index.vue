<template>
  <div>
    <!-- navbar -->
    <navbar :userBaseInfo="userBaseInfo" />

    <a-carousel autoplay class="carousel">
      <img src="https://s2.ax1x.com/2019/05/26/VV8t9s.jpg">
      <img src="https://s2.ax1x.com/2019/05/26/VV8Jhj.jpg">
      <img src="https://s2.ax1x.com/2019/05/26/VV8N3n.jpg">
    </a-carousel>

    <!-- statement -->
    <section class="section">
      <div class="container">
        <div class="col-md-8 col-md-offset-2 text-center">
          <h1>社区</h1>
          <p>ヽ(✿ﾟ▽ﾟ)ノ</p>
          <hr />
        </div>
        <!-- row_1 -->
        <div class="row text-center">
          <div class="col-md-4">
            <div class="section-item">
              <a-icon type="heart" theme="twoTone" class="section-icon" />
              <h2>表白墙</h2>
              <p>来表白墙敞开心扉表白吧～</p>
              <router-link to="/love">进入</router-link>
            </div>
          </div>
          <div class="col-md-4">
            <div class="section-item">
              <a-icon type="tags" theme="twoTone" class="section-icon" />
              <h2>失物墙</h2>
              <p>丢掉物品很伤心吧，来这里大家一起找找吧～</p>
              <router-link to="/lose">进入</router-link>
            </div>
          </div>
          <div class="col-md-4">
            <div class="section-item">
              <a-icon type="switcher" theme="twoTone" class="section-icon" />
              <h2>二手墙</h2>
              <p>旧东西也能焕发光彩呢～</p>
              <router-link to="/deal">进入</router-link>
            </div>
          </div>
        </div>
        <!-- row_2 -->
        <div class="row text-center">
          <div class="col-md-4">
            <div class="section-item">
              <a-icon type="switcher" theme="twoTone" class="section-icon" />
              <h2>求助墙</h2>
              <p>有问题找小伙伴们哦～</p>
              <router-link to="/deal">进入</router-link>
            </div>
          </div>
          <div class="col-md-4">
            <div class="section-item">
              <a-icon type="crown" theme="twoTone" class="section-icon" />
              <h2>大佬杂谈</h2>
              <p>大佬们的学习经验～</p>
              <router-link to="/article">进入</router-link>
            </div>
          </div>
          <div class="col-md-4">
            <div class="section-item">
              <a-icon type="database" theme="twoTone" class="section-icon" />
              <h2>题库</h2>
              <p>C位！万能的题库～</p>
              <router-link to="/bank">进入</router-link>
            </div>
          </div>
        </div>
        <!-- row_3 -->
        <div class="row text-center">
          <div class="col-md-4">
            <div class="section-item">
              <a-icon type="star" theme="twoTone" class="section-icon" />
              <h2>校园热点</h2>
              <p>吃第一口瓜～</p>
              <router-link to="/hot">进入</router-link>
            </div>
          </div>
          <div class="col-md-4">
            <div class="section-item">
              <a-icon type="api" theme="twoTone" class="section-icon" />
              <h2>讲座动态</h2>
              <p>抢在第一位～</p>
              <router-link to="/lecture">进入</router-link>
            </div>
          </div>
          <div class="col-md-4">
            <div class="section-item">
              <a-icon type="gold" theme="twoTone" class="section-icon" />
              <h2>社团</h2>
              <p>找找心爱的社团吧～</p>
              <a href="/club">进入</a>
            </div>
          </div>
        </div>
        <!-- row_4 -->
        <div class="row text-center">
          <div class="col-md-4">
            <div class="section-item">
              <a-icon type="highlight" theme="twoTone" class="section-icon" />
              <h2>安利墙</h2>
              <p>吃一口安利～</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="section-item">
              <a-icon type="smile" theme="twoTone" class="section-icon" />
              <h2>追剧墙</h2>
              <p>一起追剧吧～</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="section-item">
              <a-icon type="home" theme="twoTone" class="section-icon" />
              <h2>组队墙</h2>
              <p>找找队友吧～</p>
            </div>
          </div>
        </div>
      </div>
    </section>
    <!-- about us -->
    <section class="section">
      <div class="container">
        <div class="row text-center">
          <div class="col-md-8 col-md-offset-2">
            <h1>你问我答</h1>
            <p>(๑•̀ㅂ•́)و✧</p>
            <hr />
          </div>
        </div>
        <div class="row">
          <div class="col-md-6">
            <h4><a-icon type="check" /> 墙墙们有什么用？</h4>
            <p>墙墙可以帮你表白，寻找失物，出售二手物品，求助别人！</p>
            <h4><a-icon type="check" /> 题库使用效果怎么样？</h4>
            <p>我们的题库收录了几乎练习册上的所有题目，当然您也可以上传自己的题目，更厉害的是，你可以组织一场自我考试！</p>
          </div>
          <div class="col-md-6">
            <h4><a-icon type="check" /> 大佬杂谈有用么？</h4>
            <p>我们会邀请校内的优秀学子分享他们的学习经验，看得多了，总会有用的！</p>
            <h4><a-icon type="check" /> 我们应该还要有XXX功能！</h4>
            <p>如果你想拥有其他的板块或功能，在页面最下方就可以看到我的联系方式了！</p>
          </div>
        </div>
      </div>
    </section>

    <Footer></Footer>

  </div>
</template>

<script>
import qs from 'qs'
import { mapState } from 'vuex'
import navbar from '~/components/navbar'
import Footer from '~/components/footer'

export default {
  components: {
    navbar,
    Footer
  },
  data() {
    return {
    }
  },
  async asyncData({ $axios }) {
    let userBaseInfo = null

    await $axios.get('getUserBaseInfo')
    .then((response) => {
      userBaseInfo = response.data
    })

    return {
      userBaseInfo: userBaseInfo
    }
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
.section h2 {
  color: #0099FF;
}
.section h4 {
  color: #0099FF;
}
.section-item {
  position: relative;
  padding: 30px;
  margin-bottom: 30px;
  float: left;
  width: 100%;
}
.section-icon {
  font-size: 64px;
}

.ant-carousel >>> .slick-dots {
  height: auto
}
.carousel {
  height: 300px;
}
.carousel img {
  height: 300px;
  opacity: 0.7;
  overflow: hidden;
}

@media (min-width: 992px) {
  .carousel {
    height: 600px;
  }
  .carousel img {
    height: 600px;
  }
}
</style>
