<template>
    <div>
        <!-- banner -->
        <div class="main-wrapper">
            <div class="page-title">
                <div class="container">
                    <div class="title-holder">
                        <div class="title-text text-center">
                            <h1>求助墙</h1>
                            <p class="subheading">有问题找小伙伴们哦～</p>
                            <br />
                            <a-button type="primary" @click="$router.push({ path: '/help/new' })" style="margin-top: 20px">发布求助</a-button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div style="margin-top: 50px"></div>
        <!-- container -->
        <div class="container">
            <div class="row">
                <div class="col-md-6 col-md-offset-3">
                    <a-spin :spinning="spinning">
                        <RecycleScroller
                            v-if="hackReset"
                            :items="helpList"
                            :item-size="1"
                            v-slot="{ item, index }"
                            v-infinite-scroll="infiniteLoadList"
                            infinite-scroll-disabled="busy"
                            :infinite-scroll-distance="20"
                            style="height: 100%"
                        >
                            <a-card hoverable @click="$router.push({ path: '/help/detail', query: { id: item.id } })">
                                <a-card-meta
                                    :title="item.title"
                                    :description="item.content"
                                >
                                    <div slot="avatar" class="text-center">
                                        <a-avatar :src="baseUrl + item.user.avatar" @click="$router.push({ path: '/profile', query: { id: item.user.id } })" />
                                        <br />
                                        <nuxt-link :to="{ path: '/profile', query: { id: item.user.id } }">{{ item.user.username }}</nuxt-link>
                                    </div>
                                </a-card-meta>
                                <div style="margin-top: 20px">
                                    <span style="float: left">
                                        <a-icon key="message" type="message" /> {{ item.comments }}
                                    </span>
                                
                                    <span style="float: right">{{ moment(item.date).format('lll') }}</span>
                                </div>
                            </a-card>
                            <hr />
                        </RecycleScroller>
                    </a-spin>
                    <a-spin v-if="loading" class="loading" />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import qs from 'qs'
import moment from 'moment'
import { mapState } from 'vuex'
import { max } from 'moment'

export default {
  layout: 'common',
  data() {
    return {
        moment,

        hackReset: true,
        spinning: false,
        loading: false,
        busy: false,
    }
  },
  async asyncData({ $axios, error }) {
    let helpList = []

    await $axios.get('getHelpList', {
        params: {
            page_number: 1
        }
    })
    .then((response) => {
        if (response.data.code == 200 && response.data.status == 'success') {
            helpList = response.data.data
        }
    })

    return {
        helpList: helpList
    }
  },
  methods: {
      infiniteLoadList() {
        this.loading = true
        this.$axios.get('getHelpList', {
              params: {
                  page_number: Math.ceil(this.helpList.length / 10 + 1)
              }
          })
          .then((response) => {
              this.loading = false
              this.spinning = false
              if (response.data.code == 200) {
                if (response.data.status == 'success') {
                    this.helpList = this.helpList.concat(response.data.data)
                }
                else if (response.data.status == 'none') {
                    this.busy = true
                    this.$message.warning('到底啦～')
                }
            }
          })
    },
  },
  computed: {
      ...mapState({
          baseUrl: state => state.baseUrl
      })
  }
}
</script>

<style scoped>
a {
    text-decoration: none;
}

.loading {
  position: absolute;
  bottom: 40px;
  width: 100%;
  text-align: center;
}
</style>
