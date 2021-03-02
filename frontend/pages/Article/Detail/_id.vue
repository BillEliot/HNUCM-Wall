<template>
    <div>
        <!-- banner -->
        <div class="main-wrapper">
            <div class="page-title">
                <div class="container">
                    <div class="title-holder">
                        <div class="title-text text-center">
                            <h1>{{ articleDetail.title }}</h1>
                            <span class="date">发布时间: {{ moment(articleDetail.publicDate).format("llll") }}</span>
                            <br />
                            <span class="date">最后编辑: {{ moment(articleDetail.editDate).format("llll") }}</span>
                            <hr />
                            <span>所需硬币: {{ articleDetail.neededCoin }}</span>
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
                        <a-avatar :size="64" :src="baseUrl + articleDetail.user.avatar" />
                        <br />
                        <a @click="$router.push({ path: '/profile', query: { id: articleDetail.user.id } })">{{ articleDetail.user.username }}</a>
                        <br />
                        <a-tag v-for="tag in articleDetail.user.auth" :color="randomColor()" :key="tag">{{ tag }}</a-tag>
                        <p>{{ articleDetail.user.bio }}</p>
                    </div>
                    <!-- tags -->
                    <div class="text-left" style="margin-top: 20px">
                        <a-tag v-for="tag in articleDetail.tags" :color="randomColor()" :key="tag">{{ tag }}</a-tag>
                    </div>
                    <client-only placeholder='Loading'>
                        <mavon-editor
                            v-model="articleDetail.content"
                            :subfield="false"
                            defaultOpen="preview"
                            :toolbarsFlag="false"
                            :editable="false"
                            class="editor"
                        />
                    </client-only>
                    <div v-if="articleDetail.isOwnArticle" class="text-left" style="margin-top: 10px;">
                        <a-button type="primary" @click="editArticle">编辑</a-button>
                        <a-popconfirm
                            title="确定删除文章吗？"
                            @confirm="confirm_removeArticle()"
                            okText="是"
                            cancelText="否"
                        >
                            <a-icon slot="icon" type="question-circle-o" style="color: red" />
                            <a-button type="danger">删除</a-button>
                        </a-popconfirm>
                    </div>
                    <hr />
                    <div>
                        <!-- icon-left -->
                        <div class="icon-left">
                            <a-icon type="like-o" :theme="articleDetail.isThumbsUp ? 'filled' : 'outlined'" @click="ThumbsUp(articleDetail)" /> {{ articleDetail.thumbsUp }}
                        </div>
                        <!-- icon-share -->
                        <div class="icon-share">
                            <a target='_blank' :href="`http://connect.qq.com/widget/shareqq/index.html?url=https://hnucmwall.top/article/detail%3fid%3d${articleDetail.id}&sharesource=qzone&title=湖南中医药大学校园墙-大佬杂谈&summary=描述&desc=简述`">
                                <icon-font type="icon-qq" />
                            </a>
                            <a target='_blank' :href="`https://sns.qzone.qq.com/cgi-bin/qzshare/cgi_qzshare_onekey?url=https://hnucmwall.top/article/detail%3fid%3d${articleDetail.id}&sharesource=qzone&title=湖南中医药大学校园墙-大佬杂谈&summary=湖南中医药大学校园墙`">
                                <icon-font type="icon-qzone" />
                            </a>
                            <a href="javascript:void((function(s,d,e,r,l,p,t,z,c) {var%20f='http://v.t.sina.com.cn/share/share.php?appkey=962772401',u=z||d.location,p=['&url=',e(u),'& title=',e(t||d.title),'&source=',e(r),'&sourceUrl=',e(l),'& content=',c||'gb2312','&pic=',e(p||'')].join('');function%20a() {if(!window.open([f,p].join(''),'mb', ['toolbar=0,status=0,resizable=1,width=600,height=500,left=',(s.width- 600)/2,',top=',(s.height-600)/2].join('')))u.href=[f,p].join('');}; if(/Firefox/.test(navigator.userAgent))setTimeout(a,0);else%20a();}) (screen,document,encodeURIComponent,'','','https://hnucmwall.top','湖南中医药大学校园墙-大佬杂谈','','utf-8'));" alt="分享到新浪微博" title="分享到新浪微博">
                                <icon-font type="icon-weibo" />
                            </a>
                        </div>
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
                                    <a-avatar slot="avatar" :src="baseUrl + item.avatar" @click="$router.push({ path: '/profile', query: { id: item.id } })"></a-avatar>
                                    <a slot="author" style="font-size: 15px" @click="$router.push({ path: '/profile', query: { id: item.id } })">{{ item.username }}</a>
                                    <p slot="content" class="text-left">{{ item.content }}</p>
                                    <span class="date">{{ moment(item.date).format('lll') }}</span>
                                </a-comment>
                            </a-list-item>
                        </a-list>
                        <a-comment :avatar="baseUrl + userBaseInfo.avatar" :author="userBaseInfo.username">
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
      
      await $axios.get('addArticleViewCount', {
          params: {
              id: query.id
          }
      })

      let articleDetail = null
      await $axios.get('getArticleDetail', {
          params: {
              id: query.id
          }
      })
      .then((response) => {
          if (response.data.code == 200 && response.data.status == 'success') {
              articleDetail = response.data.data
          }
      })

      return {
          articleDetail: articleDetail
      }
  },
  methods: {
      randomColor() {
        let color = ['pink', 'red', 'orange', 'green', 'cyan', 'blue', 'purple']
        return color[Math.round(Math.random() * (color.length - 1))]
      },
      ThumbsUp (articleDetail) {
        if (this.userBaseInfo.id == -1) {
            this.$message.warning('先登录吧～')
        }
        else {
            if (articleDetail.isThumbsUp) {
                articleDetail.isThumbsUp = false
                articleDetail.thumbsUp -= 1
                this.$axios.post('thumbsUpArticle', qs.stringify({
                    id: articleDetail.id,
                    isThumbsUp: false
                }))
            }
            else {
                articleDetail.isThumbsUp = true
                articleDetail.thumbsUp += 1
                this.$axios.post('thumbsUpArticle', qs.stringify({
                    id: articleDetail.id,
                    isThumbsUp: true
                }))
            }
        }
      },
      submitComment() {
          if (!this.commentContent) {
              this.$message.warning('说点什么吧～')
          }
          else if (this.userBaseInfo.id == -1) {
              this.$message.warning('登录之后再评论吧～')
          }
          else {
              this.commenting = true
              this.$axios.post('submitArticleComment', qs.stringify({
                  id: this.articleDetail.id,
                  content: this.commentContent
              }))
              .then((response) => {
                  this.commenting = false
                  if (response.data.code == 200 && response.data.status == 'success') {
                      this.articleDetail.comments.unshift({
                          avatar: this.userBaseInfo.avatar,
                          username: this.userBaseInfo.username,
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
      },
      editArticle() {
          this.$router.push({ path: '/article/new', query: { isEdit: true, id: this.articleDetail.id } })
      },
      confirm_removeArticle() {
          this.$axios.post('removeArticle', {
              params: {
                  id: this.articleDetail.id
              }
          })
          .then((response) => {
              if (response.data.code == 200 && response.data.status == 'success') {
                  this.$message.success('删除成功')
                  this.$router.push({ path: '/article' })
              }
          })
      }
  },
  computed: mapState({
      baseUrl: state => state.baseUrl,
      userBaseInfo: state => state.userBaseInfo
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

.icon-left {
    position: absolute;
    left: 10px;
    font-size: 18px;
}
.icon-share {
    position: absolute;
    right: 10px;
}
.icon-share >>> .anticon {
    font-size: 24px;
    cursor: pointer;
}

.date {
    font-style: italic;
    color: gray;
}
</style>
