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
                            <h1>大佬杂谈</h1>
                            <p class="subheading">努力提高自己吧～</p>
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
                    <div class="author">
                        <a-avatar :size="64" :src="baseUrl + articleDetail.avatar" />
                        <br />
                        <a @click="$router.push({ path: '/profile', query: { uid: articleDetail.uid } })">{{ articleDetail.nickname }}</a>
                        <p>{{ articleDetail.bio }}</p>
                    </div>
                    <h1>{{ articleDetail.title }}</h1>
                    <span class="date">发布时间: {{ moment(articleDetail.publicDate).format("llll") }}</span>
                    <br />
                    <span class="date">最后编辑: {{ moment(articleDetail.editDate).format("llll") }}</span>
                    <no-ssr placeholder='Loading'>
                        <mavon-editor
                            v-model="articleDetail.content"
                            :subfield="false"
                            defaultOpen="preview"
                            :toolbarsFlag="false"
                            :editable="false"
                            class="editor"
                        />
                    </no-ssr>
                    <hr />
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
                    <div id="comment" style="margin-top: 50px">
                        <a-list
                            v-if="articleDetail.comments.length"
                            :pagination="commentPagination"
                            :dataSource="articleDetail.comments"
                            :header="`${articleDetail.comments.length} 条回复`"
                            itemLayout="horizontal"
                        >
                            <div slot="footer"><b>友善的回复是交流的起点</b></div>
                            <a-list-item slot="renderItem" slot-scope="item, index">
                                <a-comment style="padding-left: 35px">
                                    <a-avatar slot="avatar" :src="baseUrl + item.avatar" @click="$router.push({ path: '/profile', query: { uid: item.uid } })"></a-avatar>
                                    <a slot="author" style="font-size: 15px" @click="$router.push({ path: '/profile', query: { uid: item.uid } })">{{ item.nickname }}</a>
                                    <p slot="content" class="text-left">{{ item.content }}</p>
                                </a-comment>
                            </a-list-item>
                        </a-list>
                        <a-comment :avatar="baseUrl + userBaseInfo.avatar" :author="userBaseInfo.nickname">
                            <div slot="content">
                                <a-form-item>
                                    <a-textarea :rows="4" v-model="commentContent" ></a-textarea>
                                </a-form-item>
                                <a-form-item class="text-left">
                                    <a-button htmlType="submit" :loading="commenting" @click="submitComment" type="primary">评论</a-button>
                                    <a-anchor v-if="showAnchor" :affix="false" class="anchor" @click="commentPagination.current=1">
                                        <a-anchor-link href="#comment" title="查看评论" />
                                    </a-anchor>
                                </a-form-item>
                            </div>
                        </a-comment>
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
        commenting: false,
        commentContent: null,
        commentPagination: {
            current: 1,
            pageSize: 10,
            onChange (page) {
                this.current = page
            }
        },
        showAnchor: false
    }
  },
  async asyncData({ $axios, query, redirect }) {
      if (!query.id) {
          redirect('/article')
      }

      let articleDetail = null
      await $axios.post('getArticleDetail', qs.stringify({
          id: query.id
      }))
      .then((response) => {
          if (response.data == 1) {
              redirect('/article')
          }
          else {
              articleDetail = response.data
          }
      })
      let userBaseInfo = null
      await $axios.get('getUserBaseInfo')
      .then((response) => {
          userBaseInfo = response.data
      })

      return {
          articleDetail: articleDetail,
          userBaseInfo: userBaseInfo
      }
  },
  methods: {
      submitComment() {
          if (!this.commentContent) {
              this.$message.warning('说点什么吧～')
          }
          else if (this.userBaseInfo.uid == -1) {
              this.$message.warning('登录之后再评论吧～')
          }
          else {
              this.commenting = true
              this.$axios.post('submitArticleComment', qs.stringify({
                  id: this.articleDetail.id,
                  uid: this.userBaseInfo.uid,
                  content: this.commentContent
              }))
              .then((response) => {
                  this.commenting = false
                  if (response.data == 1) {
                      this.$message.error('未知错误')
                  }
                  else {
                      this.articleDetail.comments.unshift({
                          avatar: this.userBaseInfo.avatar,
                          nickname: this.userBaseInfo.nickname,
                          content: this.commentContent
                      })
                      this.commentContent = ''
                      this.showAnchor = true
                      setTimeout(() => {
                          this.showAnchor = false
                      }, 3000)
                      this.$message.success('评论成功')
                  }
              })
          }
      }
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

.date {
    color: gray;
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
    margin-top: 20px;
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
