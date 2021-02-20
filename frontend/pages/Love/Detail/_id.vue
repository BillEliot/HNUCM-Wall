<template>
    <div>
        <!-- drawer - more userto -->
        <a-drawer
            title="所有被表白人"
            placement="right"
            :width="300"
            :closable="false"
            @close="visibleMoreUserTo = false"
            :visible="visibleMoreUserTo"
        >
            <div class="row">
                <div class="col-md-4 col-md-offset-4 col-xs-4 col-xs-offset-4 c text-center">
                    <div v-for="user in loveDetail.userTo" :key="user.username">
                        <a-avatar :size="64" :src="baseUrl + '/media/' + user.avatar" />
                        <nuxt-link :to="{ path: '/profile', query: { id: user.id } }">{{ user.username }}</nuxt-link>
                        <p class="bio">{{ user.bio }}</p>
                    </div>
                </div>
            </div>
        </a-drawer>
        <!-- banner -->
        <div class="main-wrapper">
            <div class="page-title">
                <div class="container">
                    <div class="title-holder">
                        <div class="title-text text-center">
                            <h1>（づ￣3￣）づ╭❤～</h1>
                            <p class="subheading">说出来了呢～</p>
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
                            <a-avatar v-if="loveDetail.userFrom_id == -1" :size="64" :src="baseUrl + loveDetail.userFrom_avatar" />
                            <a-avatar v-else :size="64" :src="baseUrl + loveDetail.userFrom_avatar" @click="$router.push({ path: '/profile', query: { id: loveDetail.userFrom_id } })" style="cursor: pointer;" />
                            <div>
                                <a v-if="loveDetail.userFrom_username == 'Anony'">匿名</a>
                                <a v-else @click="$router.push({ path: '/profile', query: { id: loveDetail.userFrom_id } })">{{ loveDetail.userFrom_username }}</a>
                                <p class="bio">{{ loveDetail.userFrom_bio }}</p>
                            </div>
                        </a-col>
                        <a-col :span="12">
                            <a-avatar v-if="loveDetail.userTo[0].id == -1" :size="64" :src="baseUrl + '/media/' + loveDetail.userTo[0].avatar" />
                            <a-avatar v-else :size="64" :src="baseUrl + '/media/' + loveDetail.userTo[0].avatar" @click="$router.push({ path: '/profile', query: { ud: loveDetail.userTo[0].id } })" style="cursor: pointer;" />
                            <a-avatar v-if="loveDetail.userTo.length > 1" :size="64" @click="moreUserTo" class="more-avatar">更多</a-avatar>
                            <div>
                                <a v-if="loveDetail.userTo[0].id == -1">{{ loveDetail.userTo[0].username }}</a>
                                <a v-else @click="$router.push({ path: '/profile', query: { id: loveDetail.userTo[0].id } })">{{ loveDetail.userTo[0].username }}</a>
                                <p class="bio">{{ loveDetail.userTo[0].bio }}</p>
                            </div>
                        </a-col>
                    </a-row>
                    <hr />
                    <a-card title="对Ta的话">
                        <p>{{ loveDetail.content }}</p>
                    </a-card>
                    <hr />
                    <a-carousel arrows dotsClass="slick-dots slick-thumb">
                        <a slot="customPaging" slot-scope="props">
                            <img :src="baseUrl + '/media/' + loveDetail.images[props.i]" />
                        </a>
                        <div v-for="image in loveDetail.images">
                            <img :src="baseUrl + '/media/' + image" />
                        </div>
                    </a-carousel>
                    <hr style="margin-top: 60px" />
                    <div style="margin-bottom: 60px">
                        <div class="icon-left">
                            <a-icon type="like-o" :theme="loveDetail.isThumbsUp ? 'filled' : 'outlined'" @click="ThumbsUp(loveDetail)" /> {{ loveDetail.thumbsUp }}
                        </div>
                        <div class="icon-share">
                            <a target='_blank' :href="`http://connect.qq.com/widget/shareqq/index.html?url=https://hnucmwall.top/love/detail%3fid%3d${loveDetail.id}&sharesource=qzone&title=湖南中医药大学表白墙&summary=描述&desc=简述`">
                                <icon-font type="icon-qq" />
                            </a>
                            <a target='_blank' :href="`https://sns.qzone.qq.com/cgi-bin/qzshare/cgi_qzshare_onekey?url=https://hnucmwall.top/love/detail%3fid%3d${loveDetail.id}&sharesource=qzone&title=湖南中医药大学表白墙&summary=湖南中医药大学表白墙`">
                                <icon-font type="icon-qzone" />
                            </a>
                            <a href="javascript:void((function(s,d,e,r,l,p,t,z,c) {var%20f='http://v.t.sina.com.cn/share/share.php?appkey=962772401',u=z||d.location,p=['&url=',e(u),'& title=',e(t||d.title),'&source=',e(r),'&sourceUrl=',e(l),'& content=',c||'gb2312','&pic=',e(p||'')].join('');function%20a() {if(!window.open([f,p].join(''),'mb', ['toolbar=0,status=0,resizable=1,width=600,height=500,left=',(s.width- 600)/2,',top=',(s.height-600)/2].join('')))u.href=[f,p].join('');}; if(/Firefox/.test(navigator.userAgent))setTimeout(a,0);else%20a();}) (screen,document,encodeURIComponent,'','','https://hnucmwall.top','湖南中医药大学表白墙','','utf-8'));" alt="分享到新浪微博" title="分享到新浪微博">
                                <icon-font type="icon-weibo" />
                            </a>
                        </div>
                    </div>
                    <div v-if="loveDetail.isOwnLove" class="text-left" style="margin-top: 10px;">
                        <a-button type="primary" @click="editLove">编辑</a-button>
                        <a-popconfirm
                            title="确定删除表白吗？"
                            @confirm="confirm_removeLove()"
                            okText="是"
                            cancelText="否"
                        >
                            <a-icon slot="icon" type="question-circle-o" style="color: red" />
                            <a-button type="danger">删除</a-button>
                        </a-popconfirm>
                    </div>
                    <div id="comment" style="margin-top: 50px">
                        <a-list
                            v-if="loveDetail.comments.length"
                            :pagination="commentPagination"
                            :dataSource="loveDetail.comments"
                            :header="`${loveDetail.comments.length} 条回复`"
                            itemLayout="horizontal"
                        >
                            <div slot="footer"><b>友善的回复是交流的起点</b></div>
                            <a-list-item slot="renderItem" slot-scope="item, index">
                                <a-comment style="padding-left: 35px">
                                    <a-avatar slot="avatar" :src="baseUrl + '/media/' + item.avatar" @click="$router.push({ path: '/profile', query: { id: item.id } })"></a-avatar>
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
        showAnchor: false,

        visibleMoreUserTo: false
    }
  },
  async asyncData({ $axios, query, redirect }) {
      if (!query.id) {
          redirect('/love')
      }

      let loveDetail = null
      await $axios.get('getLoveDetail', {
          params: {
              id: query.id
          }
      })
      .then((response) => {
          if (response.data.code == 200 && response.data.status == 'success') {
              loveDetail = response.data.data
          }
      })

      return {
          loveDetail: loveDetail
      }
  },
  methods: {
      ThumbsUp (loveDetail) {
        if (this.userBaseInfo.id == -1) {
            this.$message.warning('先登录吧～')
        }
        else {
            if (loveDetail.isThumbsUp) {
                loveDetail.isThumbsUp = false
                loveDetail.thumbsUp -= 1
                this.$axios.post('thumbsUpLove', qs.stringify({
                    id: loveDetail.id,
                    isThumbsUp: false
                }))
            }
            else {
                loveDetail.isThumbsUp = true
                loveDetail.thumbsUp += 1
                this.$axios.post('thumbsUpLove', qs.stringify({
                    id: loveDetail.id,
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
              this.$axios.post('submitLoveComment', qs.stringify({
                  id: this.loveDetail.id,
                  content: this.commentContent
              }))
              .then((response) => {
                  this.commenting = false
                  if (response.data.code == 200 && response.data.status == 'success') {
                      this.loveDetail.comments.unshift({
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
      moreUserTo() {
          this.visibleMoreUserTo = true
      },
      editLove() {
          this.$router.push({ path: '/love/new', query: { isEdit: true, id: this.loveDetail.id } })
      },
      confirm_removeLove() {
          this.$axios.get('removeLove', {
              params: {
                  id: this.loveDetail.id
              }
          })
          .then((response) => {
              if (response.data.code == 200 && response.data.status == 'success') {
                  this.$message.success('删除成功')
                  this.$router.push({ path: '/love' })
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
a:hover {
    color: blue;
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
.icon-left {
    position: absolute;
    left: 10px;
    font-size: 18px;
}

.more-avatar {
    cursor: pointer;
    color: white;
}
.more-avatar:hover {
    color: blueviolet;
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
