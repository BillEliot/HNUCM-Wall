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
                        <h1>查题</h1>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div style="margin-top: 50px"></div>
    <!-- statement -->
    <section class="section">
      <div class="container">
          <a-input-search placeholder="请输入要查询的题目" @search="onSearch" enterButton />
          <hr />
          <a-spin :spinning="spinning">
            <a-table :columns="columns" :dataSource="data">
                <a-tag slot="chapter" slot-scope="text" :color="randomColor()">{{ text }}</a-tag>
                <a-tag slot="subject" slot-scope="text" :color="randomColor()">{{ text }}</a-tag>
                <!--<p slot="expandedRowRender" slot-scope="record" style="margin: 0">{{ record.answer }}</p>-->
            </a-table>
          </a-spin>
      </div>
    </section>

    <Footer></Footer>

  </div>
</template>

<script>
import qs from 'qs'
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
      columns: [{
        dataIndex: 'key'
      }, {
        title: '题目',
        dataIndex: 'title'
      }, {
        title: '答案',
        dataIndex: 'answer'
      },{
        title: '章节',
        dataIndex: 'chapter',
        scopedSlots: { customRender: 'chapter' }
      }, {
        title: '科目',
        dataIndex: 'subject',
        scopedSlots: { customRender: 'subject' }
      }],
      data: null,
      spinning: false
    }
  },
  async asyncData({ $axios }) {
    let userBaseInfo = null

    await $axios.get('getUserBaseInfo')
    .then((response) => {
      userBaseInfo = response.data
    })

    return {
      userBaseInfo: userBaseInfo
    }
  },
  methods: {
      randomColor() {
        let color = ['pink', 'red', 'orange', 'green', 'cyan', 'blue', 'purple']
        return color[Math.round(Math.random() * (color.length - 1))]
      },
      onSearch(title) {
          if (this.userBaseInfo.uid == -1) {
            this.$message.warning('先登录吧～')
          }
          else {
            if (!!title) {
              this.spinning = true
              this.$axios.post('searchQuestion', qs.stringify({
                title: title
              }))
              .then((response) => {
                  this.spinning = false
                  if (response.data == 1) {
                    this.$message.error('未知错误')
                  }
                  else {
                    this.data = response.data.info
                    this.$notification.open({
                      message: '查询结果',
                      description: '共查询到' + this.data.length.toString() + '个结果',
                      icon: <a-icon type="smile" style="color: #108ee9" />,
                    })
                  }
              })
            }
            else {
              this.$message.warning('请输入题目')
            }
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
</style>
