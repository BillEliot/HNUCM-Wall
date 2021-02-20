<template>
    <div>
        <!-- banner -->
        <div class="main-wrapper">
            <div class="page-title">
                <div class="container">
                    <div class="title-holder">
                        <div class="title-text text-center">
                            <h1>{{ hotDetail.title }}</h1>
                            <a-tag>{{ hotDetail.type }}</a-tag>
                            <br />
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
                    <client-only placeholder='Loading'>
                        <mavon-editor
                            v-model="hotDetail.content"
                            :subfield="false"
                            defaultOpen="preview"
                            :toolbarsFlag="false"
                            :editable="false"
                            class="editor"
                        />
                    </client-only>
                    <hr />
                    <div>
                        <!-- icon-share -->
                        <div class="icon-share">
                            <a target='_blank' :href="`http://connect.qq.com/widget/shareqq/index.html?url=https://hnucmwall.top/hot/detail%3fid%3d${hotDetail.id}&sharesource=qzone&title=湖南中医药大学校园墙-热点&summary=描述&desc=简述`">
                                <icon-font type="icon-qq" />
                            </a>
                            <a target='_blank' :href="`https://sns.qzone.qq.com/cgi-bin/qzshare/cgi_qzshare_onekey?url=https://hnucmwall.top/hot/detail%3fid%3d${hotDetail.id}&sharesource=qzone&title=湖南中医药大学校园墙-热点&summary=湖南中医药大学校园墙`">
                                <icon-font type="icon-qzone" />
                            </a>
                            <a href="javascript:void((function(s,d,e,r,l,p,t,z,c) {var%20f='http://v.t.sina.com.cn/share/share.php?appkey=962772401',u=z||d.location,p=['&url=',e(u),'& title=',e(t||d.title),'&source=',e(r),'&sourceUrl=',e(l),'& content=',c||'gb2312','&pic=',e(p||'')].join('');function%20a() {if(!window.open([f,p].join(''),'mb', ['toolbar=0,status=0,resizable=1,width=600,height=500,left=',(s.width- 600)/2,',top=',(s.height-600)/2].join('')))u.href=[f,p].join('');}; if(/Firefox/.test(navigator.userAgent))setTimeout(a,0);else%20a();}) (screen,document,encodeURIComponent,'','','https://hnucmwall.top','湖南中医药大学校园墙-热点','','utf-8'));" alt="分享到新浪微博" title="分享到新浪微博">
                                <icon-font type="icon-weibo" />
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import qs from 'qs'
import moment from 'moment'
import { Icon } from 'ant-design-vue'
import { mapState } from 'vuex'

const IconFont = Icon.createFromIconfontCN({
  scriptUrl: '//at.alicdn.com/t/font_1211094_e7pjz6z6y7.js'
})
export default {
  layout: 'common',
  components: {
    IconFont
  },
  data() {
    return {
        moment
    }
  },
  async asyncData({ $axios, query }) {
      let hotDetail = null

      await $axios.get('getHotDetail', {
          params: {
              id: query.id
          }
      })
      .then((response) => {
          if (response.data.code == 200 && response.data.status == 'success') {
              hotDetail = response.data.data
          }
      })

      return {
          hotDetail: hotDetail
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
