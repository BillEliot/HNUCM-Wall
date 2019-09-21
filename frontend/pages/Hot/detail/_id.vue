<template>
    <div>
        <!-- navbar -->
        <navbar :userBaseInfo="userBaseInfo" />
        <!-- banner -->
        <div class="main-wrapper">
            <div class="page-title">
                <div class="container">
                    <div class="title-holder">
                        <div class="title-text text-center">
                            <h1>{{ hotDetail.title }}</h1>
                            <p class="subheading">{{ hotDetail.date }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div style="margin-top: 50px"></div>
        <!-- container -->
        <div class="container">
            <div class="row">
                <div class="text-center col-md-12">
                    <no-ssr placeholder='Loading'>
                        <mavon-editor
                            v-model="hotDetail.content"
                            :subfield="false"
                            defaultOpen="preview"
                            :toolbarsFlag="false"
                            :editable="false"
                            class="editor"
                        />
                    </no-ssr>
                    <hr />
                    <div>
                        <!-- icon-share -->
                        <div class="icon-share">
                            <a target='_blank' href="http://connect.qq.com/widget/shareqq/index.html?url=http://127.0.0.1&sharesource=qzone&title=湖南中医药大学失物墙&summary=描述&desc=简述">
                                <icon-font type="icon-qq" />
                            </a>
                            <icon-font type="icon-wechat" />
                            <a target='_blank' href="https://sns.qzone.qq.com/cgi-bin/qzshare/cgi_qzshare_onekey?url=http://127.0.0.1&sharesource=qzone&title=湖南中医药大学失物墙&summary=描述">
                                <icon-font type="icon-qzone" />
                            </a>
                            <icon-font type="icon-pyq" />
                            <icon-font type="icon-weibo" />
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <Footer />

    </div>
</template>

<script>
import qs from 'qs'
import moment from 'moment'
import { Icon } from 'ant-design-vue'
import { mapState } from 'vuex'
import navbar from '~/components/navbar'
import Footer from '~/components/footer'

const IconFont = Icon.createFromIconfontCN({
  scriptUrl: '//at.alicdn.com/t/font_1211094_e7pjz6z6y7.js'
})
export default {
  components: {
    IconFont,
    navbar,
    Footer
  },
  data() {
    return {
        moment,
    }
  },
  async asyncData({ $axios, query, redirect }) {
      if (!query.id) {
          redirect('/hot')
      }

      let hotDetail = null
      await $axios.post('getHotDetail', qs.stringify({
          id: query.id
      }))
      .then((response) => {
          if (response.data == 1) {
              redirect('/hot')
          }
          else {
              hotDetail = response.data
          }
      })
      let userBaseInfo = null
      await $axios.get('getUserBaseInfo')
      .then((response) => {
          userBaseInfo = response.data
      })

      return {
          hotDetail: hotDetail,
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
    text-decoration: none;
}

.author {
    margin: 10px;
}
.author a {
    font-size: 24px;
}
.author p {
    color: gray;
}

.editor {
    margin-top: 10px;
    z-index: inherit;
}

.icon-share {
    position: absolute;
    right: 10px;
}
.icon-share >>> .anticon {
    font-size: 24px;
    cursor: pointer;
}
</style>
