<template>
    <div>
        <!-- banner -->
        <div class="main-wrapper">
            <div class="page-title">
                <div class="container">
                    <div class="title-holder">
                        <div class="title-text text-center">
                            <h1>(＞﹏＜)</h1>
                            <p class="subheading">要尽快找回来啊～</p>
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
                    <a-row>
                        <a-col :span="12">
                            <p class="losetime text-left">丢失时间：{{ moment(loseDetail.loseDate).format('lll') }}</p>
                        </a-col>
                        <a-col :span="12">
                            <p v-if="loseDetail.isFound" class="found">已找到</p>
                            <p v-else class="notfound">未找到</p>
                        </a-col>
                    </a-row>
                    <a-avatar :size="64" :src="baseUrl + loseDetail.user.avatar" />
                    <div>
                        <a @click="$router.push({ path: '/profile', query: { id: loseDetail.user.id } })">{{ loseDetail.user.username }}</a>
                        <br />
                        <a-tag v-for="tag in loseDetail.user.auth" :color="randomColor()" :key="tag">{{ tag }}</a-tag>
                        <p class="bio">{{ loseDetail.user.bio }}</p>
                    </div>
                    <hr />
                    <a-card :title="loseDetail.name">
                        <p>{{ loseDetail.description }}</p>
                    </a-card>
                    <hr />
                    <a-carousel arrows dotsClass="slick-dots slick-thumb">
                        <a slot="customPaging" slot-scope="props">
                            <img :src="baseUrl + '/media/' + loseDetail.images[props.i]" />
                        </a>
                        <div v-for="image in loseDetail.images">
                            <img :src="baseUrl + '/media/' + image" />
                        </div>
                    </a-carousel>
                    <hr />
                    <a-descriptions bordered title="联系方式" size="small">
                        <a-descriptions-item label="手机">
                            {{ loseDetail.user.phone }}
                        </a-descriptions-item>
                        <a-descriptions-item label="qq">
                           {{ loseDetail.user.qq }}
                        </a-descriptions-item>
                        <a-descriptions-item label="微信">
                            {{ loseDetail.user.wechat }}
                        </a-descriptions-item>
                    </a-descriptions>
                    <hr style="margin-top: 70px" />
                    <div class="icon-share">
                        <a target='_blank' :href="`http://connect.qq.com/widget/shareqq/index.html?url=https://hnucmwall.top/lose/detail%3fid%3d${loseDetail.id}&sharesource=qzone&title=湖南中医药大学失物墙&summary=描述&desc=简述`">
                                <icon-font type="icon-qq" />
                            </a>
                            <a target='_blank' :href="`https://sns.qzone.qq.com/cgi-bin/qzshare/cgi_qzshare_onekey?url=https://hnucmwall.top/lose/detail%3fid%3d${loseDetail.id}&sharesource=qzone&title=湖南中医药大学失物墙&summary=湖南中医药大学校园墙`">
                                <icon-font type="icon-qzone" />
                            </a>
                            <a href="javascript:void((function(s,d,e,r,l,p,t,z,c) {var%20f='http://v.t.sina.com.cn/share/share.php?appkey=962772401',u=z||d.location,p=['&url=',e(u),'& title=',e(t||d.title),'&source=',e(r),'&sourceUrl=',e(l),'& content=',c||'gb2312','&pic=',e(p||'')].join('');function%20a() {if(!window.open([f,p].join(''),'mb', ['toolbar=0,status=0,resizable=1,width=600,height=500,left=',(s.width- 600)/2,',top=',(s.height-600)/2].join('')))u.href=[f,p].join('');}; if(/Firefox/.test(navigator.userAgent))setTimeout(a,0);else%20a();}) (screen,document,encodeURIComponent,'','','https://hnucmwall.top','湖南中医药大学失物墙','','utf-8'));" alt="分享到新浪微博" title="分享到新浪微博">
                                <icon-font type="icon-weibo" />
                            </a>
                    </div>
                    <div v-if="loseDetail.isOwnLose" class="text-left" style="margin-top: 10px;">
                        <a-button type="primary" @click="editLose">编辑</a-button>
                        <a-popconfirm
                            title="确定删除失物吗？"
                            @confirm="confirm_removeLose()"
                            okText="是"
                            cancelText="否"
                        >
                            <a-icon slot="icon" type="question-circle-o" style="color: red" />
                            <a-button type="danger">删除</a-button>
                        </a-popconfirm>
                    </div>
                    <div id="comment" style="margin-top: 50px">
                        <a-list
                            v-if="loseDetail.comments.length"
                            :pagination="commentPagination"
                            :dataSource="loseDetail.comments"
                            :header="`${loseDetail.comments.length} 条回复`"
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
    IconFont,
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
          redirect('/lose')
      }

      let loseDetail = null
      await $axios.get('getLoseDetail', {
          params: {
              id: query.id
          }
      })
      .then((response) => {
          if (response.data.code == 200 && response.data.status == 'success') {
              loseDetail = response.data.data
          }
      })

      return {
          loseDetail: loseDetail
      }
  },
  methods: {
      randomColor() {
          let color = ['pink', 'red', 'orange', 'green', 'cyan', 'blue', 'purple']
          return color[Math.round(Math.random() * (color.length - 1))]
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
              this.$axios.post('submitLoseComment', qs.stringify({
                  id: this.loseDetail.id,
                  content: this.commentContent
              }))
              .then((response) => {
                  this.commenting = false
                  if (response.data.code == 200 && response.data.status == 'success') {
                      this.loseDetail.comments.unshift({
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
      confirm_removeLose() {
          this.$axios.get('removeLose', {
              params: {
                  id: this.loseDetail.id
              }
          })
          .then((response) => {
              if (response.data.code == 200 && response.data.status == 'success') {
                  this.$message.success('删除成功')
                  this.$router.push({ path: '/lose' })
              }
          })
      },
      editLose() {
          this.$router.push({ path: '/lose/new', query: { isEdit: true, id: this.loseDetail.id } })
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
a:hover {
    color: blue;
}

.losetime {
    color: indigo;
    font-size: 28px;
    font-weight: bold;
}
.found {
    margin-top: 0;
    float: right;
    color: green;
    font-size: 28px;
    font-weight: bold;
}
.notfound {
    margin-top: 0;
    float: right;
    color: red;
    font-size: 28px;
    font-weight: bold;
}

.anchor >>> .ant-anchor-link-title {
    text-decoration: none;
}

.icon-share {
    position: absolute;
    right: 10px;
}
.icon-share >>> .anticon {
    font-size: 24px;
    cursor: pointer;
}

.ant-carousel >>> .slick-dots {
    height: auto
}
.ant-carousel >>> .slick-slide img{
    border: 5px solid #FFF;
    display: block;
    margin: auto;
    max-width: 300px;
}
.ant-carousel >>> .slick-thumb {
    bottom: -45px;
}
.ant-carousel >>> .slick-thumb li {
    width: 60px;
    height: 45px;
}
.ant-carousel >>> .slick-thumb li img {
    width: 100%;
    height: 100%;
    filter: grayscale(100%);
}
.ant-carousel >>> .slick-thumb li.slick-active img{
    filter: grayscale(0%);
}

.date {
    font-style: italic;
    color: gray;
}

@media (min-width: 992px) {
    .ant-carousel >>> .slick-slide img{
        max-width: 600px;
    }
}
</style>
