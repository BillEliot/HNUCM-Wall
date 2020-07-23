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
                            <h1>金匮打卡</h1>
                            <span class="date">发布时间: {{ moment(detail.date).format("llll") }}</span>
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
                        <a-avatar :size="64" :src="baseUrl + detail.user.avatar" />
                        <br />
                        <a @click="$router.push({ path: '/profile', query: { uid: detail.user.uid } })">{{ detail.user.nickname }}</a>
                        <br />
                        <a-tag v-for="tag in detail.user.auth" :color="randomColor()" :key="tag">{{ tag }}</a-tag>
                        <p>{{ detail.user.bio }}</p>
                    </div>
                    <no-ssr placeholder='Loading'>
                        <mavon-editor
                            v-model="detail.content"
                            :subfield="false"
                            defaultOpen="preview"
                            :toolbarsFlag="false"
                            :editable="false"
                            class="editor"
                        />
                    </no-ssr>
                </div>
            </div>
        </div>

        <Footer />

    </div>
</template>

<script>
import qs from 'qs'
import moment from 'moment'
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
        moment
    }
  },
  async asyncData({ $axios, query, redirect }) {
      if (!query.uid) {
          redirect('/activity/jingui/statistics')
      }

      let detail = null
      await $axios.post('detail_JinGui', qs.stringify({
          uid: query.uid
      }))
      .then((response) => {
          if (response.data == 1) {
              redirect('/activity/jingui/statistics')
          }
          else {
              detail = response.data
          }
      })
      let userBaseInfo = null
      await $axios.get('getUserBaseInfo')
      .then((response) => {
          userBaseInfo = response.data
      })

      return {
          detail: detail,
          userBaseInfo: userBaseInfo
      }
  },
  methods: {
      randomColor() {
        let color = ['pink', 'red', 'orange', 'green', 'cyan', 'blue', 'purple']
        return color[Math.round(Math.random() * (color.length - 1))]
      },
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
    font-style: italic;
    color: gray;
}
.editor {
    margin-top: 10px;
    z-index: inherit;
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
</style>
