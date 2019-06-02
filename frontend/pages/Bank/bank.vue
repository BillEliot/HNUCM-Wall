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
                            <h1>开始刷题</h1>
                            <p class="subheading">(￣_,￣ )</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div style="margin-top: 50px"></div>
        <!-- container -->
        <div class="container">
            <div class="row">
                <div class="text-center">
                    <a-list
                        itemLayout="vertical"
                        size="large"
                        :pagination="pagination"
                        :dataSource="questions"
                    >
                        <div slot="footer"><b>ant design vue</b> footer part</div>
                        <a-list-item slot="renderItem" slot-scope="item, index" key="item.title">
                        <template slot="actions" v-for="{type, text} in actions">
                            <span :key="type">
                            <a-icon :type="type" style="margin-right: 8px" />
                            {{text}}
                            </span>
                        </template>
                        <img slot="extra" width="272" alt="logo" src="https://gw.alipayobjects.com/zos/rmsportal/mqaQswcyDLcXyDKnZfES.png" />
                        <a-list-item-meta
                            :description="item.description"
                        >
                            <a slot="title" :href="item.href">{{item.title}}</a>
                            <a-avatar slot="avatar" :src="item.avatar" />
                        </a-list-item-meta>
                        {{item.content}}
                        </a-list-item>
                    </a-list>
                </div>
            </div>
        </div>

        <Footer />

    </div>
</template>

<script>
import qs from 'qs'
import Footer from '~/components/footer.vue'
import navbar from '~/components/navbar'

export default {
  components: {
      Footer,
      navbar
  },
  data() {
    return {
        pagination: {
            current: 0,
            onChange(page) {
                current = page
            },
            pageSize: 10
        }
    }
  },
  async asyncData({ $axios }) {
    let userBaseInfo = null

    await $axios.get('getUserBaseInfo')
    .then((response) => {
        userBaseInfo = response.data
    })

    return {
        userBaseInfo: userBaseInfo,
    }
  },
  methods: {
  }
}
</script>

<style scoped>
</style>
