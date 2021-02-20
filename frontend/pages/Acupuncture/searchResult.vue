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
                            <h1>查穴位</h1>
                            <p class="subheading"></p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div style="margin-top: 50px"></div>
        <div class="container text-center result">
            <a-spin :spinning="spinning">
                <a-auto-complete
                    v-model="keyword"
                    :dataSource="completeResult"
                    @search="autoComplete"
                    placeholder="输入关键字"
                    :allowClear="true"
                    class="auto-complete"
                />
                <a-button type="primary" @click="search" style="margin-left: 10px">搜索</a-button>
                
            </a-spin>
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
        spinning: false,
        keyword: '',
        completeResult: [],
        
    }
  },

  async asyncData({ $axios, query }) {
      let userBaseInfo = null
      let searchResult = null

      await $axios.get('getUserBaseInfo')
      .then((response) => {
          userBaseInfo = response.data
      })
      
      if (!!query.keyword) {
          await $axios.get('searchAcupoint', {
              keyword: query.keyword
          })
          .then((response) => {
            searchResult = response.data.info
          })
      }
      
      return {
          userBaseInfo: userBaseInfo,
          searchResult: searchResult
      }
  },

  methods: {
      search() {
        if (!!this.keyword) {
            
        }
        else {
            this.$message.warning('输入些关键字吧～')
        }
      },
      autoComplete(value) {
          this.$axios.post('autoComplete_searchAcupoint', qs.stringify({
            keyword: value
          }))
          .then((res) => {
            this.completeResult = res.data.info
          })
      }
  }
}
</script>

<style scoped>
a {
    text-decoration: none;
}

.result {
    margin-top: 100px;
}

.auto-complete {
  width: 600px;
  margin-left: 10px
}

.table {
    margin-top: 20px;
}
.table >>> .ant-pagination {
    margin: 16px auto;
    float: none;
}

@media screen and (max-width: 768px) {
    .auto-complete {
        width: 100px;
    }
}
@media screen and (max-width: 970px) {
    .auto-complete {
        width: 250px;
    }

    .rule {
        margin-bottom: 10px;
    }
}
</style>
